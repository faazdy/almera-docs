# SABIA · RAG-lite de Almera

Chat que responde dudas de Almera con la documentación de este repo, usando un modelo de [OpenRouter](https://openrouter.ai). Cualquier persona puede usarlo desde el navegador, sin cuenta de Claude ni skills instaladas.

Este servidor publica **todo SABIA en una sola dirección**: el sitio estático y el chat, sin puertos escritos en los enlaces.

| Ruta | Qué es |
|---|---|
| `/` | Portada de SABIA (`index.html` del repo) |
| `/almera/…`, `/calidad-ai-agents/…`, `/styles/…` | El sitio estático, servido directo desde las carpetas del repo (no hay copias) |
| `/asistente/` | El chat |
| `/api/…` | API del chat |

## Arrancar

```powershell
cd rag
.\iniciar.ps1          # la primera vez crea .venv y rag\.env
# edita rag\.env → OPENROUTER_API_KEY=sk-or-v1-...
.\iniciar.ps1
```

Abre <http://127.0.0.1:8800>: es la portada de SABIA, y el chat está en <http://127.0.0.1:8800/asistente/>.

El chat usa el mismo menú del sitio (`almera/assets/nav.js`, diseño 1c) y todos los enlaces son relativos (`asistente/`, `../index.html`). Por eso funciona igual en cualquier equipo o puerto donde se publique.

El sitio también puede servirse **solo**, sin el chat (`npx serve -l 8934 .` o GitHub Pages). En ese caso todo funciona excepto el enlace "Pregúntale a SABIA", que da 404 porque el chat necesita este servidor.

Manual: `python -m venv .venv`, `.venv\Scripts\pip install -r requirements.txt`, `copy .env.example .env`, `.venv\Scripts\python -m app.main`.

## Cómo funciona

```
pregunta ──► enrutador BM25 ──► módulo(s) elegidos ──► prompt = reglas + árbol de navegación + guía COMPLETA del módulo ──► OpenRouter ──► respuesta en streaming
             (sobre secciones)   (máx. 2)
```

- **Por qué "lite":** todo el conocimiento de Almera son ~240 KB (~65k tokens). Cada guía cabe entera en el contexto del modelo, así que no hay base vectorial ni embeddings. Las secciones solo se usan para *decidir* qué módulo enviar. Al modelo siempre le llega la guía completa, así los procedimientos paso a paso nunca llegan partidos.
- **Seguimientos:** para enrutar se usan las dos últimas preguntas del usuario, así "¿y cómo lo apruebo?" sigue en el mismo módulo.
- **Selector de módulo:** en la barra superior se puede fijar un módulo si el enrutador automático se equivoca.
- **Costo aproximado:** 8–17k tokens de entrada por pregunta. Con `claude-haiku-5.5` cuesta unos US$0,002 por pregunta.

| Archivo | Qué hace |
|---|---|
| `sources.json` | Catálogo: qué `.md` del repo forma cada módulo. **Para agregar conocimiento, edita solo este archivo.** |
| `app/knowledge.py` | Carga las guías, las parte por encabezados (`#`–`###`), índice BM25 y enrutamiento |
| `app/prompts.py` | Reglas del asistente (mismas de las skills: procedimiento exacto, no inventar, advertir pendientes, citar fuente) |
| `app/llm.py` | Cliente de OpenRouter con streaming |
| `app/main.py` | API FastAPI (`/api/chat`, `/api/modules`) y servidor de la página |
| `static/` | Interfaz de chat (HTML/CSS/JS plano, `marked` y `DOMPurify` locales en `vendor/`) |

## Agregar o actualizar conocimiento

1. Edita o crea el `.md` en `almera/...` como siempre. El RAG lee los archivos del repo; no hay copias.
2. Si es un archivo nuevo, agrégalo a `files` del módulo correspondiente en `sources.json`, o crea un módulo nuevo.
3. Reinicia el servidor.

Para que el enrutador funcione bien, conviene usar encabezados descriptivos (`## Crear un comité`). Las secciones "Árbol de…" e "Índice" se ignoran al enrutar porque se repiten en todas las guías.

**Cuándo pasar a un RAG "de verdad"** (con embeddings): si el contenido supera ~150k tokens o cientos de documentos, por ejemplo al sumar transcripciones de capacitaciones o procedimientos PR-0xx completos. El punto de cambio es `KnowledgeBase.route()` en `app/knowledge.py`.

## Seguridad

- La llave vive **solo** en `rag/.env`, que está en `.gitignore`. El navegador nunca la ve: todas las llamadas a OpenRouter salen del servidor.
- El servidor publica **solo** una lista cerrada del repo (`SITE_DIRS` en `app/main.py`: `styles/`, `almera/`, `calidad-ai-agents/` y el `index.html` raíz). La raíz no se monta, así que `rag/.env`, `rag/app/`, `.git/`, `docs/` y los archivos sueltos de la raíz responden 404, también ante intentos con `../`. Si se agrega una carpeta nueva al sitio, hay que sumarla a `SITE_DIRS`.
- `OPENROUTER_DENY_DATA_COLLECTION=true` limita el enrutamiento de OpenRouter a proveedores que no guardan ni entrenan con los prompts.
- Por defecto escucha en `127.0.0.1`, es decir, solo en este equipo. Para compartirlo en la red local usa `HOST=0.0.0.0`. **No tiene autenticación:** cualquiera en la red podría usarlo y gastar créditos. Configura un límite de gasto en la llave de OpenRouter.
- Las preguntas tienen un máximo de 4000 caracteres y solo se envían los últimos 8 mensajes del historial.
- Red corporativa: la conexión usa `truststore` (los certificados de Windows) porque la red inspecciona TLS. No desactives la verificación SSL.
- Ver también `calidad-ai-agents/SEGURIDAD.md`: no pegar datos personales ni información sensible en las preguntas.
