"""Almacén de la nube: los documentos aportados se guardan en un repo privado de GitHub.

En la nube (Render, plan gratis) el disco se borra en cada reinicio. Por eso:

- Cada aporte se guarda como commit en GITHUB_REPO ("Aporte: Indicadores/x.docx · por Ana").
- Al arrancar, y cada ETL_INTERVAL_SECONDS, SABIA revisa el último commit. Si cambió
  (otro aporte, o alguien borró o movió un archivo desde github.com), descarga el repo a
  rag/nube/ y el ETL publica los cambios.

Nadie del área necesita cuenta de GitHub: el único que escribe es este servidor, con un
token limitado a ese repo. Solo cuentan los archivos dentro de una carpeta de módulo; lo
que esté suelto en la raíz del repo (README, LEEME) se ignora.
"""

import base64
import io
import logging
import ssl
import tarfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote

import httpx
import truststore

from . import config
from .etl import REPORT_NAME

log = logging.getLogger("sabia.almacen")

ENABLED = bool(config.GITHUB_REPO)
_synced = {"sha": None}  # último commit que tiene la copia local


def _client() -> httpx.Client:
    return httpx.Client(
        base_url=f"https://api.github.com/repos/{config.GITHUB_REPO}",
        headers={
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=httpx.Timeout(60, connect=10),
        verify=truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT),
        follow_redirects=True,  # el tarball redirige a codeload.github.com
    )


def pull(dest: Path) -> bool:
    """Deja dest igual al repo si hubo commits nuevos. Devuelve True si descargó."""
    with _client() as c:
        r = c.get(f"/commits/{quote(config.GITHUB_BRANCH)}", headers={"Accept": "application/vnd.github.sha"})
        if r.status_code == 409:  # repo vacío: todavía no hay nada que descargar
            dest.mkdir(parents=True, exist_ok=True)
            return False
        r.raise_for_status()
        sha = r.text.strip()
        if sha == _synced["sha"] and dest.is_dir():
            return False
        r = c.get(f"/tarball/{sha}")
        r.raise_for_status()
    apply_tarball(r.content, dest)
    _synced["sha"] = sha
    log.info("Conocimiento descargado de GitHub (commit %s)", sha[:7])
    return True


def apply_tarball(content: bytes, dest: Path) -> None:
    """Copia el tarball en dest. Solo reescribe lo que cambió: si se reescribiera todo, la
    fecha de cada archivo cambiaría y el ETL volvería a procesar la carpeta entera."""
    dest.mkdir(parents=True, exist_ok=True)
    keep: set[Path] = set()
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as tar:
        for m in tar.getmembers():
            parts = PurePosixPath(m.name).parts[1:]  # quita la carpeta "usuario-repo-sha/"
            # Solo archivos dentro de una carpeta de módulo; nada oculto ni con ".."
            if not m.isfile() or len(parts) < 2 or any(p.startswith(".") for p in parts):
                continue
            rel = Path(*parts)
            keep.add(rel)
            data = tar.extractfile(m).read()
            target = dest / rel
            if target.is_file() and target.read_bytes() == data:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    # Lo que ya no está en el repo (borrado o movido desde github.com) se quita de la copia
    for f in list(dest.rglob("*")):
        rel = f.relative_to(dest)
        if f.is_file() and rel not in keep and rel.name != REPORT_NAME and not rel.name.startswith("."):
            f.unlink()


def save(rel: str, data: bytes, author: str, replace: bool) -> bool:
    """Guarda el original en el repo. False si ya existe y no se pidió reemplazarlo."""
    path = quote(rel)
    with _client() as c:
        r = c.get(f"/contents/{path}", params={"ref": config.GITHUB_BRANCH})
        if r.status_code not in (200, 404):
            r.raise_for_status()
        sha = r.json().get("sha") if r.status_code == 200 else None
        if sha and not replace:
            return False
        body = {
            "message": f"{'Actualiza' if sha else 'Aporte'}: {rel} · por {author}",
            "content": base64.b64encode(data).decode("ascii"),
            "branch": config.GITHUB_BRANCH,
        }
        if sha:
            body["sha"] = sha
        r = c.put(f"/contents/{path}", json=body)
        r.raise_for_status()
    # La copia local ya tiene este archivo. Si nadie más cambió el repo entretanto, no hace
    # falta descargarlo todo otra vez en la próxima revisión.
    commit = r.json()["commit"]
    if [p["sha"] for p in commit.get("parents", [])] == [_synced["sha"]]:
        _synced["sha"] = commit["sha"]
    return True
