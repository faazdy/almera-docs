"""ETL de conocimiento: carpeta compartida → Markdown limpio → RAG.

    Extraer      Word, PDF, PowerPoint, Excel (MarkItDown) y .md/.txt tal cual
    Transformar  quita imágenes, números de página y encabezados/pies repetidos;
                 convierte "títulos falsos" (líneas solo en negrita) en títulos reales
    Validar      semáforo 🟢 publica · 🟡 publica con advertencias · 🔴 no publica
    Cargar       escribe el .md en rag/generado/ y deja "ESTADO SABIA.txt" en la carpeta

No toca ni mueve los archivos originales. Solo reprocesa lo que cambió.
Ejecutar una vez desde rag/:  python -m app.etl
"""

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from . import config
from .knowledge import Doc, load_catalog, normalize

# Subir cuando cambie la limpieza o el semáforo: obliga a reprocesar todo
ETL_VERSION = "1"

SUPPORTED = {".docx", ".pdf", ".pptx", ".xlsx", ".md", ".txt"}
LEGACY = {
    ".doc": "Es un Word antiguo (.doc). Ábrelo y usa Guardar como → Documento de Word (.docx).",
    ".ppt": "Es un PowerPoint antiguo (.ppt). Guárdalo como .pptx.",
    ".xls": "Es un Excel antiguo (.xls). Guárdalo como .xlsx.",
}
REPORT_NAME = "ESTADO SABIA.txt"
# Archivos de ayuda que viven en la raíz de la carpeta y no son conocimiento
ROOT_HELPERS = ("leeme", "prompt", "plantilla", "estado")
PROMPT_HINT = 'usa "PROMPT para limpiar con IA.txt" y guarda el resultado en esta misma carpeta'

STATUS_ORDER = {"rojo": 0, "amarillo": 1, "verde": 2}


@dataclass
class Result:
    source: str  # ruta relativa dentro de la carpeta compartida
    module: str | None
    status: str  # verde | amarillo | rojo
    notes: list[str] = field(default_factory=list)
    output: str | None = None  # ruta relativa dentro de rag/generado
    sha: str = ""
    mtime: float = 0.0
    size: int = 0
    version: str = ETL_VERSION


# ---------- Extraer ----------
_markitdown = None


def extract(path: Path) -> str:
    if path.suffix.lower() in (".md", ".txt"):
        raw = path.read_bytes()
        try:
            return raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            return raw.decode("cp1252", errors="replace")  # Bloc de notas antiguo
    global _markitdown
    if _markitdown is None:
        from markitdown import MarkItDown  # import perezoso: tarda en cargar

        _markitdown = MarkItDown(enable_plugins=False)
    return _markitdown.convert(str(path)).markdown


# ---------- Transformar ----------
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
PAGE_NUM_RE = re.compile(r"^\s*(p[aá]g(ina)?\.?\s*)?\d{1,4}(\s*(de|/)\s*\d{1,4})?\s*$", re.I)
FAKE_HEADING_RE = re.compile(r"^\*\*([^*\n]{3,80}?)\*\*:?\s*$")
HEADING_LINE_RE = re.compile(r"^#{1,6}\s")


def clean(text: str, title: str, ext: str) -> tuple[str, dict]:
    info = {"images": 0, "fake_headings": 0, "repeated": 0, "page_numbers": 0}

    text, info["images"] = IMAGE_RE.subn("", text)
    if ext == ".xlsx":  # restos de pandas: celdas vacías y columnas sin nombre
        text = re.sub(r"(?<=\|) NaN (?=\|)", "  ", text)
        text = re.sub(r"(?<=\|) Unnamed: \d+ (?=\|)", "  ", text)
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").split("\n")]

    # Títulos falsos: un párrafo que es solo negrita → "## título"
    for i, ln in enumerate(lines):
        m = FAKE_HEADING_RE.match(ln.strip())
        if m and (i == 0 or not lines[i - 1].strip()):
            lines[i] = f"## {m.group(1).strip()}"
            info["fake_headings"] += 1

    # Encabezados/pies de página: líneas cortas idénticas que se repiten 3+ veces.
    # Solo en PDF y PowerPoint: en un Word podría borrar un paso legítimo repetido.
    counts: dict[str, int] = {}
    for ln in lines if ext in (".pdf", ".pptx") else ():
        s = ln.strip()
        if 3 <= len(s) <= 80 and not HEADING_LINE_RE.match(s) and not re.match(r"[-*|]|\d+[.)]\s", s):
            counts[s] = counts.get(s, 0) + 1
    repeated = {s for s, n in counts.items() if n >= 3}

    out = []
    for ln in lines:
        s = ln.strip()
        if s in repeated:
            info["repeated"] += 1
            continue
        if PAGE_NUM_RE.match(s):
            info["page_numbers"] += 1
            continue
        out.append(ln)

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    if not text.startswith("# "):
        text = f"# {title}\n\n{text}"
    return text, info


# ---------- Validar ----------
TIMESTAMP_LINE_RE = re.compile(r"\b\d{1,2}:\d{2}(:\d{2})?\s*$")


def assess(text: str, info: dict) -> tuple[str, list[str]]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    body = "\n".join(lines[1:])  # sin el título del documento
    headings = [ln for ln in lines[1:] if HEADING_LINE_RE.match(ln)]
    red, yellow, notes = [], [], []

    if len(body) < 80 or (len(body) < 200 and not headings):
        red.append("Casi no tiene texto. Si es un PDF escaneado o una imagen, el sistema no lo puede leer: "
                   "usa el Word original o " + PROMPT_HINT + ".")
    if sum(1 for ln in lines if TIMESTAMP_LINE_RE.search(ln)) >= 10:
        red.append("Parece la transcripción de una reunión. Para convertirla en una guía, " + PROMPT_HINT + ".")
    short = sum(1 for ln in lines if len(ln) <= 2)
    if short >= 10 and short / max(len(lines), 1) > 0.08:
        red.append("El texto salió desarmado (marca de agua, columnas o tablas complejas). "
                   "Usa el Word original o " + PROMPT_HINT + ".")
    if not headings and len(body) > 20000:
        red.append("Es largo y no tiene títulos, así que el asistente no puede ubicar los temas. "
                   "Sepáralo con los estilos Título 1 y Título 2 de Word, o " + PROMPT_HINT + ".")

    if not red:
        if len(headings) < 2:
            yellow.append("Tiene pocos títulos. Usa los estilos Título 1 y Título 2 de Word para separar los "
                          "temas: así el asistente encuentra la sección correcta.")
        if info["fake_headings"]:
            yellow.append(f"{info['fake_headings']} título(s) estaban solo en negrita y se convirtieron en títulos. "
                          "Revisa que tenga sentido, o usa los estilos Título de Word.")
        if info["images"]:
            yellow.append(f"{info['images']} imagen(es) no se pueden leer. Si muestran pasos o pantallas "
                          "importantes, descríbelos con texto.")
        longest = max((len(s) for s in re.split(r"\n#{1,3} ", text)), default=0)
        if longest > 15000:
            yellow.append("Hay una sección muy larga. Dividirla con más títulos mejora las respuestas.")

    if not red and (info["repeated"] or info["page_numbers"]):
        notes.append("Se quitaron encabezados, pies y números de página repetidos.")

    status = "rojo" if red else "amarillo" if yellow else "verde"
    return status, red + yellow + notes


# ---------- Cargar ----------
def module_lookup() -> dict[str, str]:
    """Nombre de carpeta normalizado → id de módulo. Acepta el id, el nombre o cada parte de "A / B"."""
    lookup = {}
    for spec in load_catalog()["modules"]:
        for alias in [spec["id"], spec["name"], *spec["name"].split("/")]:
            lookup[normalize(alias).strip().replace("-", " ")] = spec["id"]
    return lookup


def folder_module(name: str, lookup: dict[str, str]) -> str | None:
    return lookup.get(normalize(name).strip().replace("-", " ").replace("_", " "))


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize(text)).strip("-")[:60] or "documento"


def front_matter(r: Result) -> str:
    return (
        "---\n"
        f"origen: {r.source}\n"
        f"modulo: {r.module}\n"
        f"estado: {r.status}\n"
        f"convertido: {datetime.now():%Y-%m-%d %H:%M}\n"
        f"sha256: {r.sha}\n"
        "---\n\n"
    )


FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n+", re.S)


def iter_sources(root: Path):
    """(archivo, carpeta de módulo o None si está suelto en la raíz)."""
    for entry in sorted(root.iterdir()):
        if entry.name.startswith((".", "~$")) or entry.name == REPORT_NAME:
            continue
        if entry.is_file():
            if entry.suffix.lower() in SUPPORTED | set(LEGACY) and not normalize(entry.stem).startswith(ROOT_HELPERS):
                yield entry, None
        elif entry.is_dir():
            for f in sorted(entry.rglob("*")):
                if f.is_file() and not any(p.startswith((".", "~$")) for p in f.relative_to(root).parts):
                    yield f, entry


def process(path: Path, rel: str, module: str, out_dir: Path) -> Result:
    data = path.read_bytes()
    r = Result(rel, module, "rojo", sha=hashlib.sha256(data).hexdigest())
    try:
        text, info = clean(extract(path), path.stem, path.suffix.lower())
    except Exception as exc:  # archivo dañado, con contraseña, etc.
        r.notes.append(f"No se pudo abrir el archivo ({exc.__class__.__name__}). "
                       "Revisa que no tenga contraseña y que abra bien en Office.")
        return r
    r.status, r.notes = assess(text, info)
    if r.status != "rojo":
        out = Path(module) / f"{slug(path.stem)}-{r.sha[:8]}.md"
        (out_dir / out).parent.mkdir(parents=True, exist_ok=True)
        (out_dir / out).write_text(front_matter(r) + text + "\n", encoding="utf-8")
        r.output = out.as_posix()
    return r


def run(knowledge_dir: Path, out_dir: Path) -> tuple[list[Result], bool]:
    """Procesa la carpeta. Devuelve (resultados, ¿cambió lo publicado?)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"
    try:
        old = {k: Result(**{"version": "", **v}) for k, v in
               json.loads(manifest_path.read_text(encoding="utf-8")).items()}
    except (OSError, ValueError, TypeError):
        old = {}

    lookup = module_lookup()
    valid = sorted({spec["name"].split("/")[0].strip() for spec in load_catalog()["modules"]})
    results: dict[str, Result] = {}
    reprocessed = False

    for path, folder in iter_sources(knowledge_dir):
        rel = path.relative_to(knowledge_dir).as_posix()
        st = path.stat()
        ext = path.suffix.lower()
        module = folder_module(folder.name, lookup) if folder else None

        if folder is None:
            r = Result(rel, None, "rojo", ["Está suelto en la carpeta principal. Muévelo a la carpeta de su módulo."])
        elif module is None:
            r = Result(rel, None, "rojo", [f'La carpeta "{folder.name}" no corresponde a ningún módulo. '
                                           f"Carpetas válidas: {', '.join(valid)}."])
        elif ext in LEGACY:
            r = Result(rel, module, "rojo", [LEGACY[ext]])
        elif ext not in SUPPORTED:
            r = Result(rel, module, "rojo", ["Formato no soportado. Usa Word (.docx), PDF, PowerPoint (.pptx), "
                                             "Excel (.xlsx) o texto (.txt / .md)."])
        else:
            prev = old.get(rel)
            same = (prev and prev.version == ETL_VERSION and prev.module == module
                    and prev.mtime == st.st_mtime and prev.size == st.st_size)
            if same and (prev.output is None or (out_dir / prev.output).is_file()):
                r = prev  # sin cambios: no se reprocesa
            else:
                r = process(path, rel, module, out_dir)
                reprocessed = reprocessed or bool(r.output or (prev and prev.output))
        r.mtime, r.size = st.st_mtime, st.st_size
        results[rel] = r

    # Quitar lo publicado que ya no corresponde (archivo borrado, cambiado o ahora en rojo)
    live = {r.output for r in results.values() if r.output}
    for f in out_dir.rglob("*.md"):
        if f.relative_to(out_dir).as_posix() not in live:
            f.unlink()

    old_pub = {k: v.output for k, v in old.items() if v.output}
    new_pub = {k: v.output for k, v in results.items() if v.output}
    changed = reprocessed or old_pub != new_pub

    manifest_path.write_text(
        json.dumps({k: asdict(v) for k, v in results.items()}, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    write_report(knowledge_dir, list(results.values()))
    return list(results.values()), changed


def load_published(out_dir: Path) -> dict[str, list[Doc]]:
    """Lee lo publicado por el ETL, listo para KnowledgeBase(extra=...)."""
    try:
        manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    extra: dict[str, list[Doc]] = {}
    for rel, entry in sorted(manifest.items()):
        if not entry.get("output"):
            continue
        try:
            text = (out_dir / entry["output"]).read_text(encoding="utf-8")
        except OSError:
            continue
        extra.setdefault(entry["module"], []).append(Doc(f"carpeta compartida: {rel}", FRONT_MATTER_RE.sub("", text)))
    return extra


def write_report(knowledge_dir: Path, results: list[Result]):
    groups = {
        "rojo": "🔴 NO PUBLICADOS — corrige el archivo y vuelve a guardarlo",
        "amarillo": "🟡 PUBLICADOS CON ADVERTENCIAS — funcionan, pero conviene mejorarlos",
        "verde": "🟢 PUBLICADOS",
    }
    n = {k: sum(1 for r in results if r.status == k) for k in groups}
    lines = [
        "ESTADO DE LOS DOCUMENTOS DE SABIA",
        f"Actualizado: {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"{n['verde']} publicados · {n['amarillo']} con advertencias · {n['rojo']} no publicados",
        "Los cambios se revisan cada pocos minutos. Este archivo lo escribe el sistema: no lo edites.",
    ]
    for status, title in groups.items():
        items = sorted((r for r in results if r.status == status), key=lambda r: r.source.lower())
        if not items:
            continue
        lines += ["", "", title, ""]
        for r in items:
            lines.append(f"  {r.source}")
            lines += [f"      - {note}" for note in r.notes]
    if not results:
        lines += ["", "Todavía no hay documentos. Guárdalos dentro de la carpeta de su módulo."]
    try:
        (knowledge_dir / REPORT_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    except OSError:
        pass  # sin permiso de escritura en la carpeta: el RAG sigue funcionando


if __name__ == "__main__":
    if not config.KNOWLEDGE_DIR:
        raise SystemExit("KNOWLEDGE_DIR no está configurado en rag/.env")
    results, changed = run(config.KNOWLEDGE_DIR, config.ETL_OUTPUT_DIR)
    icons = {"verde": "🟢", "amarillo": "🟡", "rojo": "🔴"}
    for r in sorted(results, key=lambda r: (STATUS_ORDER[r.status], r.source)):
        print(f"{icons[r.status]} {r.source}")
        for note in r.notes:
            print(f"     - {note}")
    print(f"\n{len(results)} archivo(s) · publicado {'cambió' if changed else 'sin cambios'} · "
          f"reporte en {config.KNOWLEDGE_DIR / REPORT_NAME}")
