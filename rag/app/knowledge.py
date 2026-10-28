"""Base de conocimiento: carga las guías .md, las parte por secciones y enruta preguntas.

RAG-lite: las secciones solo sirven para *decidir* qué módulo(s) usar (BM25 léxico).
Al modelo se le inyecta el módulo completo, así los procedimientos paso a paso nunca
llegan cortados.
"""

import json
import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field

from . import config

STOPWORDS = set(
    """
    a al algo ante antes como con contra cual cuales cuando de del desde donde dos e el
    ella ellas ellos en entre era es esa esas ese eso esos esta estan estas este esto estos
    fue ha hace hacer hay la las le les lo los mas me mi mis muy ni no nos o para pero por
    porque puede pueden puedo que se segun ser si sin sobre su sus tambien tiene tienen
    todo todos tu un una unas uno unos y ya yo almera hago hacerlo quiero necesito
    debo sistema modulo opcion
    """.split()
)

HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$")
# Secciones que se repiten en casi todas las guías y ensucian el enrutamiento
NOISY_SECTIONS = ("arbol de", "indice")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def tokenize(text: str) -> list[str]:
    tokens = []
    for tok in re.findall(r"[a-z0-9]+", normalize(text)):
        if len(tok) < 2 or tok in STOPWORDS:
            continue
        # Stemming mínimo de plurales en español
        if len(tok) > 5 and tok.endswith("es"):
            tok = tok[:-2]
        elif len(tok) > 4 and tok.endswith("s"):
            tok = tok[:-1]
        tokens.append(tok)
    return tokens


@dataclass
class Section:
    module_id: str
    path: str  # "Título del documento › Sección › Subsección"
    tokens: list[str]
    label: str = ""  # lo que se muestra como fuente (sin el título del documento)


@dataclass
class Module:
    id: str
    name: str
    description: str
    files: list[str]
    content: str = ""
    sections: list[Section] = field(default_factory=list)


def split_sections(module_id: str, markdown: str) -> list[Section]:
    sections: list[Section] = []
    stack: list[tuple[int, str]] = []
    body: list[str] = []
    in_fence = False

    def flush():
        if not stack:
            return
        path = " › ".join(title for _, title in stack)
        if any(n in normalize(stack[-1][1]) for n in NOISY_SECTIONS):
            return
        # El título pesa más que el cuerpo
        tokens = tokenize(path) * 3 + tokenize("\n".join(body))
        if tokens:
            label = " › ".join(title for _, title in stack[1:]) or stack[0][1]
            sections.append(Section(module_id, path, tokens, label))

    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else HEADING_RE.match(line)
        if match:
            flush()
            level, title = len(match.group(1)), match.group(2).replace("**", "")
            stack = [(lvl, t) for lvl, t in stack if lvl < level] + [(level, title)]
            body = []
        else:
            body.append(line)
    flush()
    return sections


class KnowledgeBase:
    def __init__(self):
        data = json.loads(config.SOURCES_FILE.read_text(encoding="utf-8"))
        self.shared = "\n\n".join(self._read(p) for p in data.get("shared", []))
        self.modules: dict[str, Module] = {}
        for spec in data["modules"]:
            mod = Module(spec["id"], spec["name"], spec["description"], spec["files"])
            mod.content = "\n\n".join(
                f"<!-- archivo: {p} -->\n{self._read(p)}" for p in mod.files
            )
            mod.sections = split_sections(mod.id, mod.content)
            # El nombre y la descripción del catálogo también ayudan a enrutar
            mod.sections.append(
                Section(mod.id, mod.name, tokenize(f"{mod.name} {mod.description}") * 2)
            )
            self.modules[mod.id] = mod
        self._build_index()

    @staticmethod
    def _read(rel_path: str) -> str:
        path = config.REPO_ROOT / rel_path
        if not path.is_file():
            raise FileNotFoundError(f"sources.json apunta a un archivo inexistente: {rel_path}")
        return path.read_text(encoding="utf-8")

    def _build_index(self):
        self.sections = [s for m in self.modules.values() for s in m.sections]
        self.tf = [Counter(s.tokens) for s in self.sections]
        self.lengths = [len(s.tokens) for s in self.sections]
        self.avg_len = sum(self.lengths) / max(len(self.lengths), 1)
        df = Counter(tok for counts in self.tf for tok in counts)
        n = len(self.sections)
        self.idf = {tok: math.log(1 + (n - f + 0.5) / (f + 0.5)) for tok, f in df.items()}

    def _bm25(self, query_tokens: list[str], k1=1.5, b=0.75) -> list[float]:
        scores = []
        for counts, length in zip(self.tf, self.lengths):
            score = 0.0
            for tok in set(query_tokens):
                f = counts.get(tok)
                if f:
                    norm = f * (k1 + 1) / (f + k1 * (1 - b + b * length / self.avg_len))
                    score += self.idf[tok] * norm
            scores.append(score)
        return scores

    def route(self, query: str, pinned: str | None = None) -> dict:
        """Devuelve los módulos a inyectar y las secciones más relevantes (para mostrar como fuentes)."""
        scores = self._bm25(tokenize(query))
        ranked = sorted(zip(scores, self.sections), key=lambda x: x[0], reverse=True)

        per_module: dict[str, list[float]] = {}
        for score, sec in ranked:
            if score > 0:
                per_module.setdefault(sec.module_id, []).append(score)
        module_scores = {mid: sum(s[:3]) for mid, s in per_module.items()}
        order = sorted(module_scores, key=module_scores.get, reverse=True)

        if pinned in self.modules:
            selected = [pinned]
        elif order:
            top = module_scores[order[0]]
            selected = [order[0]] + [m for m in order[1:2] if module_scores[m] >= 0.6 * top]
        else:
            selected = []

        # Respetar el presupuesto de contexto
        budget, chosen = config.MAX_CONTEXT_CHARS - len(self.shared), []
        for mid in selected:
            size = len(self.modules[mid].content)
            if size <= budget or not chosen:
                chosen.append(mid)
                budget -= size

        sources = [
            {"module": self.modules[sec.module_id].name, "section": sec.label}
            for score, sec in ranked
            if score > 0 and sec.module_id in chosen and sec.label
        ][:4]
        return {"modules": chosen, "sources": sources}

    def build_context(self, module_ids: list[str]) -> str:
        parts = [f'<documento tipo="navegacion">\n{self.shared}\n</documento>']
        for mid in module_ids:
            mod = self.modules[mid]
            parts.append(f'<documento modulo="{mod.name}">\n{mod.content}\n</documento>')
        return "\n\n".join(parts)

    def catalog(self) -> list[dict]:
        return [
            {"id": m.id, "name": m.name, "description": m.description, "chars": len(m.content)}
            for m in self.modules.values()
        ]
