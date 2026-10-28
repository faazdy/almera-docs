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

El chat usa el mismo menú del sitio (`almera/assets/nav.js`, diseño 1c) y todos los enlaces son relativos. El detalle de rutas y del menú está en [`routes.md`](../routes.md), en la raíz del repo.

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
| `sources.json` | Catálogo: qué `.md` curados del repo forman cada módulo |
| `app/knowledge.py` | Junta guías curadas y documentos del ETL, los parte por encabezados (`#`–`###`), índice BM25 y enrutamiento |
| `app/etl.py` | Convierte lo que llega a la carpeta compartida en `.md` limpio, con semáforo |
| `carpeta-compartida/` | Plantilla de la carpeta que va en el servidor del área (LEEME, prompt, plantilla de Word) |
| `app/prompts.py` | Reglas del asistente (mismas de las skills: procedimiento exacto, no inventar, advertir pendientes, citar fuente) |
| `app/llm.py` | Cliente de OpenRouter con streaming |
| `app/main.py` | API FastAPI (`/api/chat`, `/api/modules`) y servidor de la página |
| `static/` | Interfaz de chat (HTML/CSS/JS plano, `marked` y `DOMPurify` locales en `vendor/`) |

## Agregar o actualizar conocimiento

Hay dos caminos, y el asistente usa los dos a la vez:

**A. Carpeta compartida (personas no técnicas).** Guardan un Word, PDF, PowerPoint, Excel o `.txt` en la subcarpeta de su módulo. El servidor la revisa cada `ETL_INTERVAL_SECONDS` y lo publica sin reiniciar. Las instrucciones para ellos están en `carpeta-compartida/LEEME.txt`.

**B. Guías curadas del repo (técnico).** Edita el `.md` en `almera/...`. Si es un archivo nuevo, agrégalo a `sources.json` y reinicia el servidor.

Para que el enrutador funcione bien, conviene usar títulos descriptivos (`## Crear un comité`). Las secciones "Árbol de…" e "Índice" se ignoran al enrutar porque se repiten en todas las guías.

## ETL de la carpeta compartida

```
carpeta compartida ──► Extraer ──► Transformar ──► Validar 🟢🟡🔴 ──► Cargar
 Indicadores/x.docx    MarkItDown   limpieza        semáforo           rag/generado/*.md + ESTADO SABIA.txt
```

- **Extraer:** Word, PDF, PowerPoint y Excel con [MarkItDown](https://github.com/microsoft/markitdown). `.txt` y `.md` se leen tal cual (es el formato que entrega el prompt de IA).
- **Transformar** (por código, sin IA, para no alterar nunca un procedimiento):
  - Quita imágenes y números de página.
  - En PDF y PowerPoint quita encabezados y pies repetidos. En Word no, para no borrar un paso legítimo que se repita.
  - Convierte en títulos los párrafos que son solo negrita.
  - Limpia los `NaN` de Excel.
  - Agrega un título si el documento no tiene.
- **Validar (semáforo):**
  - 🔴 No se publica: casi sin texto (escaneado), transcripción de reunión, texto desarmado (marca de agua o columnas), largo y sin títulos, formato antiguo (`.doc`), carpeta que no es un módulo o archivo suelto en la raíz.
  - 🟡 Se publica con aviso: pocos títulos, títulos falsos convertidos, imágenes perdidas o secciones muy largas.
  - 🟢 Se publica.
- **Cargar:**
  - Escribe el `.md` en `rag/generado/<módulo>/` (con ficha de origen al inicio) y el reporte `ESTADO SABIA.txt` en la carpeta compartida, para que quien subió el archivo vea el resultado.
  - **Nunca mueve ni modifica los originales.**
  - Solo reprocesa lo que cambió (fecha y tamaño). Si cambia la limpieza o el semáforo, sube `ETL_VERSION` en `etl.py` para reprocesar todo.
- **Para lo que no se puede limpiar por código** (transcripciones, PDF escaneados), el reporte manda a usar `carpeta-compartida/PROMPT para limpiar con IA.txt` en la IA que use el área y guardar el resultado como `.txt`.

Probarlo a mano, sin el servidor: `.venv\Scripts\python -m app.etl`. Procesa la carpeta una vez e imprime el semáforo.

En producción, `KNOWLEDGE_DIR` apunta a la carpeta de red **sin comillas**: `KNOWLEDGE_DIR=\\servidor\Calidad\SABIA`. Con comillas simples, `python-dotenv` se come una barra. Si la carpeta no está disponible (red caída), el asistente sigue respondiendo con lo último publicado y lo avisa en el log.

**Cuándo pasar a un RAG "de verdad"** (con embeddings): si el contenido supera ~150k tokens o cientos de documentos. Mientras tanto, si un módulo no cabe en `MAX_CONTEXT_CHARS`, se envían sus documentos más relevantes primero. El punto de cambio es `KnowledgeBase.route()` en `app/knowledge.py`.

## Seguridad

- La llave vive **solo** en `rag/.env`, que está en `.gitignore`. El navegador nunca la ve: todas las llamadas a OpenRouter salen del servidor.
- El servidor publica **solo** una lista cerrada del repo (`SITE_DIRS` en `app/main.py`: `styles/`, `almera/`, `calidad-ai-agents/` y el `index.html` raíz). La raíz no se monta, así que `rag/.env`, `rag/app/`, `.git/`, `docs/` y los archivos sueltos de la raíz responden 404, también ante intentos con `../`. Si se agrega una carpeta nueva al sitio, hay que sumarla a `SITE_DIRS`.
- `OPENROUTER_DENY_DATA_COLLECTION=true` limita el enrutamiento de OpenRouter a proveedores que no guardan ni entrenan con los prompts.
- Por defecto escucha en `127.0.0.1`, es decir, solo en este equipo. Para compartirlo en la red local usa `HOST=0.0.0.0`. **No tiene autenticación:** cualquiera en la red podría usarlo y gastar créditos. Configura un límite de gasto en la llave de OpenRouter.
- Las preguntas tienen un máximo de 4000 caracteres y solo se envían los últimos 8 mensajes del historial.
- Red corporativa: la conexión usa `truststore` (los certificados de Windows) porque la red inspecciona TLS. No desactives la verificación SSL.
- Ver también `calidad-ai-agents/SEGURIDAD.md`: no pegar datos personales ni información sensible en las preguntas.
- **Carpeta compartida:** todo lo que se guarde ahí termina en las respuestas del asistente. Dale permiso de escritura solo a quienes deben publicar. El servidor solo necesita leer la carpeta y escribir `ESTADO SABIA.txt`.
