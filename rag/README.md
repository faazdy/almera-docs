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

Desde la raíz del repo, cualquiera de estas tres formas hace lo mismo:

| Forma | Comando |
|---|---|
| Doble clic | `iniciar.bat` (en la raíz) |
| npm (requiere Node) | `npm start` |
| PowerShell | `cd rag; .\iniciar.ps1` |

La primera vez crea `rag\.venv`, instala las dependencias y crea `rag\.env`, y se detiene. Edita `rag\.env` → `OPENROUTER_API_KEY=sk-or-v1-...` y vuelve a arrancar.

`iniciar.bat` y `npm start` ejecutan `rag\iniciar.ps1` con `-ExecutionPolicy Bypass`, así que no hace falta cambiar la política de PowerShell del equipo.

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
| `conocimiento/alimentar-sabia.md` | Guía del módulo "SABIA (cómo alimentarlo)": cómo agregar, actualizar y eliminar conocimiento |
| `app/knowledge.py` | Junta guías curadas y documentos del ETL, los parte por encabezados (`#`–`###`), índice BM25 y enrutamiento |
| `app/etl.py` | Convierte lo que llega a la carpeta compartida en `.md` limpio, con semáforo |
| `carpeta-compartida/` | Plantilla de la carpeta que va en el servidor del área (LEEME, prompt, plantilla de Word) |
| `app/prompts.py` | Reglas del asistente (mismas de las skills: procedimiento exacto, no inventar, advertir pendientes, citar fuente) |
| `app/llm.py` | Cliente de OpenRouter con streaming |
| `app/main.py` | API FastAPI (`/api/chat`, `/api/modules`, `/api/upload`, `/api/descargas/…`) y servidor de la página |
| `static/` | Interfaz de chat (HTML/CSS/JS plano, `marked` y `DOMPurify` locales en `vendor/`) |

## Agregar o actualizar conocimiento

Hay dos caminos, y el asistente usa los dos a la vez:

**A. Carpeta compartida (personas no técnicas).** Guardan un Word, PDF, PowerPoint, Excel o `.txt` en la subcarpeta de su módulo. El servidor la revisa cada `ETL_INTERVAL_SECONDS` y lo publica sin reiniciar. Las instrucciones para ellos están en `carpeta-compartida/LEEME.txt`.

**A'. Botón "Aportar un documento" del chat (lo más fácil).** Aparece cuando `KNOWLEDGE_DIR` está configurado. La persona descarga la plantilla, elige el módulo en una lista y sube el archivo. El servidor lo guarda en la subcarpeta correcta de la carpeta compartida (la crea si falta), corre el ETL en ese momento y muestra el semáforo con las notas, sin esperar a `ESTADO SABIA.txt`. Evita los errores típicos de la carpeta: archivo suelto en la raíz, carpeta mal escrita, formato viejo o reemplazar algo sin querer (si el nombre ya existe, pide confirmación). La plantilla y el prompt se descargan de la copia del repo (`config.DOWNLOADS`), así que siguen funcionando aunque alguien los borre o los dañe en la carpeta compartida. Tope de tamaño: `MAX_UPLOAD_MB` (20 por defecto).

**B. Guías curadas del repo (técnico).** Edita el `.md` en `almera/...`. Si es un archivo nuevo, agrégalo a `sources.json` y reinicia el servidor.

**Módulo "SABIA (cómo alimentarlo)".** Responde preguntas sobre cómo alimentar al propio asistente, con la guía `conocimiento/alimentar-sabia.md`. En `sources.json` tiene `"uploads": false`, así que no aparece en la lista del botón "Aportar un documento", `/api/upload` lo rechaza y el ETL no lo acepta como carpeta de la carpeta compartida. Si cambias cómo se sube, actualiza o borra conocimiento (botón, carpeta, semáforo, mensajes del ETL), actualiza también esa guía.

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
  - Quita los textos de ejemplo de `Plantilla guía SABIA.docx` que quedaron sin borrar (`TEMPLATE_LINES` en `etl.py`), los `<…>` de los títulos y las secciones que quedan vacías. Si cambias el texto de la plantilla, actualiza esa lista.
  - Agrega un título si el documento no tiene.
- **Validar (semáforo):**
  - 🔴 No se publica: plantilla sin llenar, casi sin texto (escaneado), transcripción de reunión, texto desarmado (marca de agua o columnas), largo y sin títulos, formato antiguo (`.doc`), carpeta que no es un módulo o archivo suelto en la raíz.
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
- **Carpeta compartida:** todo lo que se guarde ahí termina en las respuestas del asistente. Dale permiso de escritura solo a quienes deben publicar. El servidor necesita leer la carpeta, escribir `ESTADO SABIA.txt` y, para el botón "Aportar un documento", escribir en las subcarpetas de los módulos.
- **Subidas:** `/api/upload` no tiene autenticación, igual que el chat. Con `HOST=0.0.0.0`, cualquiera en la red puede publicar documentos. Solo acepta los formatos del ETL, hasta `MAX_UPLOAD_MB`, y guarda únicamente el nombre del archivo (sin rutas) dentro de la carpeta del módulo elegido.
