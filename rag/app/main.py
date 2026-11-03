"""Servidor de SABIA: sirve el sitio estático y el asistente (RAG-lite) en un solo origen.

Ejecutar desde rag/:  python -m app.main

    /              → portada de SABIA (index.html del repo)
    /almera/...    → documentación (archivos del repo, sin copias)
    /asistente/    → chat
    /api/...       → API del chat y de "Aportar un documento"
"""

import asyncio
import json
import logging
import os
import re
import threading
import uuid
from contextlib import asynccontextmanager
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import config, etl
from .knowledge import KnowledgeBase
from .llm import LLMError, stream_chat
from .prompts import build_system_prompt

# Lo único del repo que se publica. Nunca montar la raíz: expondría rag/.env y .git.
SITE_DIRS = ("styles", "almera", "calidad-ai-agents")

log = logging.getLogger("sabia")

# La base se reemplaza entera cuando el ETL publica cambios; cada request toma la
# referencia vigente al empezar, así nunca ve una base a medio construir.
state = {"kb": KnowledgeBase(etl.load_published(config.ETL_OUTPUT_DIR))}
# El ciclo periódico y las subidas comparten manifest.json: nunca dos ETL a la vez
etl_lock = threading.Lock()


def refresh_knowledge() -> list[etl.Result]:
    if not config.KNOWLEDGE_DIR.is_dir():
        log.warning("ETL: no encuentro la carpeta %s (¿ruta mal escrita o servidor sin conexión?)",
                    config.KNOWLEDGE_DIR)
        return []
    with etl_lock:
        results, changed = etl.run(config.KNOWLEDGE_DIR, config.ETL_OUTPUT_DIR)
        if changed:
            state["kb"] = KnowledgeBase(etl.load_published(config.ETL_OUTPUT_DIR))
    counts = {s: sum(r.status == s for r in results) for s in ("verde", "amarillo", "rojo")}
    log.info("ETL: %s · base %s", counts, "actualizada" if changed else "sin cambios")
    return results


async def etl_loop():
    while True:
        try:
            await asyncio.to_thread(refresh_knowledge)
        except Exception:  # carpeta de red caída, etc.: se reintenta en la próxima vuelta
            log.exception("ETL falló")
        await asyncio.sleep(config.ETL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(_app):
    task = asyncio.create_task(etl_loop()) if config.KNOWLEDGE_DIR else None
    yield
    if task:
        task.cancel()


app = FastAPI(title="SABIA", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)


@app.middleware("http")
async def revalidate_assistant(request: Request, call_next):
    """Sin esto el navegador guarda el app.js viejo y no ve los cambios del chat hasta un Ctrl+F5."""
    response = await call_next(request)
    if request.url.path.startswith("/asistente"):
        response.headers["Cache-Control"] = "no-cache"  # sigue usando ETag: si no cambió, responde 304
    return response


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=20000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)
    module: str | None = None  # None = enrutamiento automático


def sse(event: str, data) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/api/modules")
def modules():
    return {
        "model": config.OPENROUTER_MODEL,
        "modules": state["kb"].catalog(),
        "upload": bool(config.KNOWLEDGE_DIR),
        "max_upload_mb": config.MAX_UPLOAD_MB,
    }


# ---------- Aportar un documento ----------
@app.get("/api/descargas/{key}")
def download(key: str):
    path = config.DOWNLOADS.get(key)
    if not path or not path.is_file():
        raise HTTPException(404, "Archivo no disponible")
    return FileResponse(path, filename=path.name)


def safe_filename(raw: str) -> str:
    """Solo el nombre (sin carpetas), sin caracteres que Windows no acepta."""
    name = re.split(r"[\\/]", raw)[-1]
    name = re.sub(r'[<>:"|?*\x00-\x1f]', "", name).strip().strip(".")
    stem, dot, ext = name.rpartition(".")
    return f"{stem[:100].strip()}{dot}{ext}" if stem else name[:100]


def module_folder(module_id: str):
    """Carpeta del módulo dentro de la carpeta compartida; la crea si no existe."""
    lookup = etl.module_lookup()
    for entry in sorted(config.KNOWLEDGE_DIR.iterdir()):
        if entry.is_dir() and etl.folder_module(entry.name, lookup) == module_id:
            return entry
    folder = config.KNOWLEDGE_DIR / state["kb"].modules[module_id].name.split("/")[0].strip()
    folder.mkdir(exist_ok=True)
    return folder


@app.post("/api/upload")
async def upload(request: Request, module: str, filename: str, replace: bool = False):
    """Recibe el archivo como cuerpo crudo, lo guarda en la carpeta del módulo y corre el ETL ya mismo."""
    if not config.KNOWLEDGE_DIR or not config.KNOWLEDGE_DIR.is_dir():
        raise HTTPException(503, "La carpeta compartida no está disponible en este momento. Intenta más tarde.")
    if module not in state["kb"].modules or not state["kb"].modules[module].uploads:
        raise HTTPException(400, "Elige el módulo al que pertenece el documento.")
    name = safe_filename(filename)
    ext = os.path.splitext(name)[1].lower()
    if ext in etl.LEGACY:
        raise HTTPException(400, etl.LEGACY[ext])
    if ext not in etl.SUPPORTED or not name or name.startswith("~$"):
        raise HTTPException(400, "Formato no soportado. Usa Word (.docx), PDF, PowerPoint (.pptx), "
                                 "Excel (.xlsx) o texto (.txt).")

    limit = config.MAX_UPLOAD_MB * 1024 * 1024
    data = bytearray()
    async for chunk in request.stream():
        data += chunk
        if len(data) > limit:
            raise HTTPException(413, f"El archivo pesa más de {config.MAX_UPLOAD_MB} MB.")
    if not data:
        raise HTTPException(400, "El archivo está vacío.")

    def save_and_process():
        folder = module_folder(module)
        target = folder / name
        if target.exists() and not replace:
            return None
        tmp = folder / f".subida-{uuid.uuid4().hex}.tmp"  # el ETL ignora lo que empieza por "."
        try:
            tmp.write_bytes(data)
            os.replace(tmp, target)  # si el archivo está abierto en Word, falla aquí y no queda a medias
        finally:
            tmp.unlink(missing_ok=True)
        rel = target.relative_to(config.KNOWLEDGE_DIR).as_posix()
        return next((r for r in refresh_knowledge() if r.source == rel), None) or etl.Result(
            rel, module, "rojo", ["El archivo se guardó, pero no se pudo revisar. Mira ESTADO SABIA.txt en unos minutos."]
        )

    try:
        result = await asyncio.to_thread(save_and_process)
    except PermissionError:
        raise HTTPException(423, f'No se pudo guardar "{name}". Si alguien lo tiene abierto en Office, '
                                 "ciérralo e intenta de nuevo.")
    except OSError as exc:
        log.exception("Subida falló")
        raise HTTPException(503, f"No se pudo guardar en la carpeta compartida ({exc.__class__.__name__}).")
    if result is None:
        raise HTTPException(409, f'Ya existe "{name}" en {state["kb"].modules[module].name}.')
    log.info("Subida: %s → %s", result.source, result.status)
    return {"file": result.source, "module": state["kb"].modules[module].name,
            "status": result.status, "notes": result.notes}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    kb = state["kb"]
    history = req.messages[-config.MAX_HISTORY_MESSAGES :]
    question = history[-1]
    if question.role != "user":
        raise HTTPException(400, "El último mensaje debe ser del usuario")
    if len(question.content) > config.MAX_QUESTION_CHARS:
        raise HTTPException(400, f"La pregunta supera {config.MAX_QUESTION_CHARS} caracteres")

    # La pregunta anterior ayuda a enrutar seguimientos como "¿y cómo lo apruebo?"
    user_turns = [m.content for m in history if m.role == "user"]
    routing = kb.route(" ".join(user_turns[-2:]), pinned=req.module)

    messages = [
        {"role": "system", "content": build_system_prompt(kb.catalog(), kb.build_context(routing["plan"]))},
        *({"role": m.role, "content": m.content} for m in history),
    ]

    async def events():
        names = [kb.modules[m].name for m in routing["modules"]]
        yield sse("meta", {"modules": names, "sources": routing["sources"]})
        try:
            async for delta in stream_chat(messages):
                yield sse("delta", delta)
        except LLMError as exc:
            yield sse("error", str(exc))
        except Exception as exc:  # red caída, timeout, etc.
            yield sse("error", f"No se pudo contactar el modelo ({exc.__class__.__name__}): {exc}")
        yield sse("done", None)

    return StreamingResponse(events(), media_type="text/event-stream")


# ---------- Asistente ----------
@app.get("/asistente", include_in_schema=False)
def assistant_redirect():
    return RedirectResponse("/asistente/")


@app.get("/asistente/", include_in_schema=False)
def assistant():
    return FileResponse(config.STATIC_DIR / "index.html")


app.mount("/asistente/static", StaticFiles(directory=config.STATIC_DIR), name="assistant-static")


# ---------- Sitio estático ----------
@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
def home():
    return FileResponse(config.REPO_ROOT / "index.html")


for folder in SITE_DIRS:
    app.mount(f"/{folder}", StaticFiles(directory=config.REPO_ROOT / folder, html=True), name=f"site-{folder}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s: %(message)s")
    print(f"SABIA en http://{config.HOST}:{config.PORT}/  ·  asistente en /asistente/")
    if config.KNOWLEDGE_DIR:
        print(f"Carpeta de conocimiento: {config.KNOWLEDGE_DIR} (revisión cada {config.ETL_INTERVAL_SECONDS}s)")
    uvicorn.run(app, host=config.HOST, port=config.PORT)
