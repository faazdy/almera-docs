"""Servidor de SABIA: sirve el sitio estático y el asistente (RAG-lite) en un solo origen.

Ejecutar desde rag/:  python -m app.main

    /              → portada de SABIA (index.html del repo)
    /almera/...    → documentación (archivos del repo, sin copias)
    /asistente/    → chat
    /api/...       → API del chat
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException
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


def refresh_knowledge():
    if not config.KNOWLEDGE_DIR.is_dir():
        log.warning("ETL: no encuentro la carpeta %s (¿ruta mal escrita o servidor sin conexión?)",
                    config.KNOWLEDGE_DIR)
        return
    results, changed = etl.run(config.KNOWLEDGE_DIR, config.ETL_OUTPUT_DIR)
    if changed:
        state["kb"] = KnowledgeBase(etl.load_published(config.ETL_OUTPUT_DIR))
    counts = {s: sum(r.status == s for r in results) for s in ("verde", "amarillo", "rojo")}
    log.info("ETL: %s · base %s", counts, "actualizada" if changed else "sin cambios")


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
    return {"model": config.OPENROUTER_MODEL, "modules": state["kb"].catalog()}


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
