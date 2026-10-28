"""Configuración leída desde rag/.env (la llave nunca sale del servidor)."""

import os
from pathlib import Path

from dotenv import load_dotenv

RAG_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = RAG_DIR.parent
SOURCES_FILE = RAG_DIR / "sources.json"
STATIC_DIR = RAG_DIR / "static"

load_dotenv(RAG_DIR / ".env")


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "si", "sí")


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-haiku-5.5").strip()
OPENROUTER_DENY_DATA_COLLECTION = _bool("OPENROUTER_DENY_DATA_COLLECTION", True)
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8800"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "120000"))

# Límites de entrada para que nadie dispare costos con mensajes enormes
MAX_QUESTION_CHARS = 4000
MAX_HISTORY_MESSAGES = 8
