# 7. SABIA — Documentación completa del proyecto

**Sistema de Automatización, Base de información e Inteligencia Artificial**
Área de Calidad · Capital Salud

| | |
|---|---|
| **Fecha de corte** | 4 de noviembre de 2026 |
| **Último commit documentado** | `29979ee` (rama `master` de `faazdy/almera-docs`) |
| **Reemplaza a** | [05-corte-2026-11-03.md](05-corte-2026-11-03.md) como foto vigente (los cortes anteriores quedan como histórico) |
| **Para quién** | Quien herede, mantenga, despliegue o evalúe el proyecto |

Este documento junta en un solo lugar **todo** el proyecto: por qué existe, qué tiene, en qué estado está, cómo está construido, cómo se despliega y opera, y qué falta. Los documentos de detalle siguen vigentes y se enlazan en cada sección:

| Tema | Detalle en |
|---|---|
| Skills de Claude | [01-skills.md](01-skills.md) |
| Informes (dashboards) | [02-informes.md](02-informes.md) |
| Documentación de módulos de Almera | [03-almera.md](03-almera.md) |
| Soporte técnico por síntoma | [06-soporte-tecnico.md](06-soporte-tecnico.md) |
| Operación del asistente y del ETL | [`rag/README.md`](../rag/README.md) |
| Rutas del sitio y menú | [`routes.md`](../routes.md) |
| Guía para alimentar a SABIA (usuarios) | [`rag/conocimiento/alimentar-sabia.md`](../rag/conocimiento/alimentar-sabia.md) |

---

## Tabla de contenido

1. [Resumen](#1-resumen)
2. [Por qué se hizo](#2-por-qué-se-hizo)
3. [Estado actual](#3-estado-actual)
4. [Componentes funcionales](#4-componentes-funcionales)
5. [Arquitectura](#5-arquitectura)
6. [Referencia técnica del servidor](#6-referencia-técnica-del-servidor)
7. [Stack tecnológico](#7-stack-tecnológico)
8. [DevOps: repositorios, despliegue y operación](#8-devops-repositorios-despliegue-y-operación)
9. [Seguridad](#9-seguridad)
10. [Decisiones de diseño y por qué](#10-decisiones-de-diseño-y-por-qué)
11. [Costos](#11-costos)
12. [Pendientes, riesgos y deuda técnica](#12-pendientes-riesgos-y-deuda-técnica)
13. [Tareas frecuentes (guía rápida)](#13-tareas-frecuentes-guía-rápida)
14. [Mapa del repositorio](#14-mapa-del-repositorio)
15. [Historia del proyecto](#15-historia-del-proyecto)
16. [Glosario](#16-glosario)

---

## 1. Resumen

SABIA es el proyecto del área de Calidad para que **nadie tenga que volver a ver una grabación de capacitación de una hora para resolver una duda de Almera (SGI)**, y para automatizar entregables repetitivos del área.

Tiene seis piezas:

| # | Pieza | Qué es | Dónde vive |
|---|---|---|---|
| 1 | **Documentación de Almera** | Guías web y documentos de referencia (GuIA `.md`) de 8 módulos | `almera/` |
| 2 | **Skills de Claude** | 8 skills de módulo + 2 de entregables (presentaciones, diagramas de flujo) | `almera/**/AI/*.skill`, `calidad-ai-agents/` |
| 3 | **Informes** | 2 dashboards que analizan listados maestros en el navegador | `almera/informe-documentos/`, `almera/control-documentos-sgc/` |
| 4 | **Asistente "Pregúntale a SABIA"** | Chat web con RAG-lite sobre la documentación, vía OpenRouter | `rag/` |
| 5 | **ETL de conocimiento** | Convierte Word/PDF/PPT/Excel del área en conocimiento del asistente, con semáforo | `rag/app/etl.py` |
| 6 | **Infraestructura en la nube** | Servidor en Render + repo privado de GitHub como almacén de documentos aportados | `render.yaml`, `rag/app/almacen.py`, repo `sabia-conocimiento` |

**En producción hoy:** un único servicio web en **Render** (plan gratis) sirve el sitio y el chat, protegido con clave. Los documentos que aporta el área se guardan como commits en el repo privado **`faazdy/sabia-conocimiento`**. El código y las guías curadas viven en **`faazdy/almera-docs`**, y cada push a `master` vuelve a desplegar el servicio.

---

## 2. Por qué se hizo

### 2.1 El problema

- La única fuente para resolver una duda de Almera eran **grabaciones de capacitación de 1 a 3 horas**, de las que normalmente **dos minutos** respondían la pregunta real.
- **Nadie usa todos los módulos**, pero todos dependían de la misma grabación genérica que mezcla temas.
- El conocimiento operativo vivía en la cabeza de pocas personas. Tareas recurrentes (diagramar en Bizagi, armar una presentación institucional, revisar el listado maestro) dependían de que esa persona estuviera disponible.
- La curva de aprendizaje de un usuario nuevo era alta: no había una guía de referencia rápida por módulo.

### 2.2 Los objetivos

1. **Autoservicio:** que cualquiera resuelva su duda de Almera en segundos, con la ruta exacta del menú y los pasos documentados.
2. **No inventar:** si algo no está documentado o no está confirmado con soporte de Almera, el sistema lo dice en vez de suponer.
3. **Conocimiento vivo:** que el área agregue y actualice conocimiento sin depender de un desarrollador.
4. **Automatizar entregables** respetando los lineamientos institucionales (plantilla, paleta, estándar de diagramación).
5. **Trazabilidad:** que el procedimiento quede versionado en Git y no solo en la memoria de quien capacitó.

### 2.3 Cómo evolucionó la solución

| Etapa | Qué se construyó | Limitación que llevó a la siguiente |
|---|---|---|
| 1. Documentación (jul–ago 2026) | Guías web + GuIA `.md` por módulo | Hay que leer; no responde preguntas |
| 2. Skills de Claude (jul–sep 2026) | Cada GuIA empaquetada como `.skill`; skills de entregables | Solo sirven a quien tiene **cuenta de Claude** y sabe instalarlas |
| 3. Asistente web local (oct 2026) | Chat RAG-lite en un servidor Python, con ETL de carpeta compartida | Corre en un solo equipo; publicarlo en la red dependía de TI |
| 4. Asistente en la nube (nov 2026) | Despliegue en Render + GitHub como almacén + login | **Estado actual** |

**Por qué un asistente propio si ya existían las skills:** las skills exigen cuenta de Claude e instalación. El asistente web abre SABIA a **cualquier persona de la entidad desde el navegador**, sin cuenta ni instalación. Las dos cosas conviven y usan la misma documentación.

**Por qué la nube y no el servidor del área:** dejarlo en la red interna requería un equipo siempre encendido, permisos de carpeta de red, abrir el puerto y gestión con TI. Render + GitHub resolvió eso sin costo, con HTTPS y despliegue automático. El precio es que el disco de Render se borra en cada reinicio, y por eso los documentos aportados viven en GitHub (§5.5).

---

## 3. Estado actual

### 3.1 Por pieza

| Pieza | Estado | Notas |
|---|---|---|
| Documentación de Almera (8 módulos) | ✔ Completa | Dudas abiertas con soporte de Almera en varios módulos ([03-almera.md](03-almera.md)) |
| Skills de módulo (8) | ✔ Funcionales | ⚠️ Los `.skill` de **Evaluaciones** y **Planes de mejora** no traen los pasos de seguimiento agregados el 3 de noviembre |
| Skill `presentaciones-institucionales` | ✔ Funcional | Pendientes menores (PDF desde HTML, tamaño de personajes) |
| Skill `diagramas-flujo` | ✔ Funcional | ⚠️ El `.skill` es la **única copia completa** del generador (§12) |
| Informes (2) | ✔ Funcionales | KPIs personalizados sin código; campos DEP en el del SGC |
| Asistente "Pregúntale a SABIA" | ✔ **Desplegado en Render** | Con login (sesión de 30 días) y clave para aportar |
| ETL + aportes | ✔ Funcional en la nube | Documentos en `faazdy/sabia-conocimiento` |
| Pruebas automatizadas | ✘ No existen | Las verificaciones han sido manuales o scripts de un solo uso |
| CI/CD | Parcial | Despliegue automático por push (Render). Sin pipeline de pruebas |

### 3.2 Conocimiento cargado en el asistente

**Guías curadas** (en `almera-docs`, catálogo `rag/sources.json`): 10 módulos.

| Módulo (`id`) | Guías curadas | Acepta aportes |
|---|---|---|
| Documentos (`documentos`) | `documentos-almera.md` | Sí |
| Mapa de procesos (`mapa-procesos`) | `mapa-procesos-almera.md` + instructivo de SNC | Sí |
| Mecanismos de integración (`mecanismos-integracion`) | `mecanismos-integracion.md` | Sí |
| Modelos de gestión (`modelos-gestion`) | `modelos-gestion-almera.md` + instructivo de carga masiva | Sí |
| Evaluaciones / Auditorías (`evaluaciones`) | `evaluaciones-almera.md` | Sí |
| Indicadores (`indicadores`) | `indicadores.md` | Sí |
| Planes de mejora (`planes-mejora`) | `docs-plan-de-mejora.md` | Sí |
| Proyectos (`proyectos`) | `proyectos-almera.md` | Sí |
| SABIA (cómo alimentarlo) (`sabia`) | `rag/conocimiento/alimentar-sabia.md` | **No** (`"uploads": false`) |
| General (`general`) | — | Sí |

Además, `almera/assets/almera-structure.md` (árbol de navegación de Admin) se inyecta en **todas** las respuestas (`"shared"`).

**Documentos aportados** (en `faazdy/sabia-conocimiento`, commit `e94bb2c`):

| Archivo | Módulo | Semáforo | Nota |
|---|---|---|---|
| `General/Administracion_Usuarios.docx` | General | 🟢 | — |
| `Indicadores/crear-indicadores.docx` | Indicadores | 🟡 | Pocos títulos; quedaron 6 textos de ejemplo de la plantilla (el ETL los quita) |

Tamaño aproximado del conocimiento curado: ~240 KB (~65 000 tokens). El módulo más grande (Documentos) ronda los 37 KB.

### 3.3 Qué cambió desde el corte del 3 de noviembre

| Área | Cambio | Commit |
|---|---|---|
| Despliegue | SABIA corre en **Render** (`render.yaml`, Blueprint) | `f9309b3` |
| Almacenamiento | Los aportes se guardan como commits en el repo privado `sabia-conocimiento` y se descargan a `rag/nube/` (`app/almacen.py`) | `f9309b3` |
| Aportes | El diálogo pide **nombre** (queda en el mensaje del commit) y **clave para aportar** (`UPLOAD_PASSWORD`) | `f9309b3` |
| Acceso | Página **`/login`** con `SITE_PASSWORD`, sesión firmada de 30 días, `/salir`, bloqueo tras 30 intentos fallidos en 10 min | `29979ee` |
| Modelo | En Render el modelo es `nvidia/nemotron-3-ultra-550b-a55b:free` con `OPENROUTER_DENY_DATA_COLLECTION=false` | `29979ee` |
| Almera | Gestión documental: códigos consecutivos automáticos | `f870ad6` |
| Documentación | `alimentar-sabia.md` reescrito para el flujo en la nube; `rag/README.md` con la sección "Desplegar en la nube" | `f9309b3` |

---

## 4. Componentes funcionales

### 4.1 Documentación de Almera (`almera/`)

Cada módulo existe en **tres copias del mismo contenido**, que se sincronizan **a mano**:

| Copia | Archivo | Para quién |
|---|---|---|
| Guía web | `almera/<grupo>/<módulo>/index.html` | Personas, en el navegador |
| GuIA | `almera/<grupo>/<módulo>/AI/*.md` | El asistente web y cualquier IA (es la fuente de verdad) |
| Skill | `almera/<grupo>/<módulo>/AI/almera-*.skill` | Claude (la GuIA partida en `references/`) |

| Grupo | Módulos |
|---|---|
| `modulo-documentos/` | Gestión documental, Mapa de procesos (incluye SNC), Mecanismos de integración, Modelos de gestión |
| `modulo-evaluaciones/` | Evaluaciones / Auditorías, Indicadores, Planes de mejora |
| `modulo-proyectos/` | Proyectos |

**Estructura obligatoria de una GuIA** (es lo que impide que la IA invente):

1. Instrucciones para la IA (responder solo con lo documentado, no inventar botones ni pasos).
2. Índice.
3. Árbol de navegación de Admin completo.
4. Conceptos básicos.
5. Procedimientos paso a paso, cada uno con su ruta exacta.
6. Preguntas frecuentes.
7. **Temas pendientes de validar con soporte de Almera**, con contexto, estado y fuente (minuto de la transcripción).

Otras páginas: `codigos-estructura-organizacional/` (referencia de codificación, sin skill), `almera-IA/` (cómo instalar las skills, con capturas), `assets/almera-structure.md` (árbol de Admin: Calidad, Evaluaciones, General, Indicadores, Proyectos, Riesgos) y `design/` (mockups de Claude Design, no enlazados).

Entornos de Almera: [producción](https://sgi.almeraim.com/sgi/?conid=sgicapitalsalud) y [pruebas](https://sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas). Los flujos se prueban en pruebas antes de documentarlos.

Detalle, estado por módulo y dudas abiertas: [03-almera.md](03-almera.md).

### 4.2 Skills de Claude

Un `.skill` es un **zip** cuya carpeta raíz se llama como la skill y contiene `SKILL.md` (frontmatter `name` + `description` + instrucciones), `references/` (detalle bajo demanda) y, en las de entregables, `assets/`. El campo `description` decide cuándo Claude activa la skill. Se instalan en `Claude → Configuración → Habilidades → Subir habilidad`. No hay script de build: se empaquetan a mano ([01-skills.md §0](01-skills.md)).

| Familia | Skills | Qué hacen |
|---|---|---|
| A. Módulo Almera | `almera-documentos`, `almera-mapa-procesos`, `almera-mecanismos`, `almera-modelos-gestion`, `almera-evaluaciones`, `almera-indicadores`, `almera-planes-mejora`, `almera-proyectos` | Responden preguntas con la GuIA del módulo |
| B. Entregables | `presentaciones-institucionales` | Texto → PPTX/HTML/PDF con plantilla y paleta oficiales (14 layouts `L01`–`L14`, `pptx_kit.py`); también **consolida** presentaciones existentes (`consolidar.py`) |
| | `diagramas-flujo` | Cuadro de actividades → diagrama estilo Bizagi con carriles por responsable, fases opcionales, validación 🟢🟡🔴, ≤ 100 caracteres por actividad. Salidas: PDF, PNG, JPG, SVG, **BPMN 2.0** y tabla de validación |

Las skills de entregables **ejecutan código** (Python, `python-pptx`, `cairosvg`), así que solo funcionan dentro de Claude. Detalle: [01-skills.md](01-skills.md). Uso con datos reales: [`calidad-ai-agents/SEGURIDAD.md`](../calidad-ai-agents/SEGURIDAD.md).

### 4.3 Informes (dashboards)

| | Informe de documentos Almera | Control de documentos del SGC |
|---|---|---|
| Carpeta | `almera/informe-documentos/` | `almera/control-documentos-sgc/` |
| Entrada | Export del listado maestro de Almera | `LISTADO MAESTRO DE CONTROL DE DOCUMENTOS DEL SGC.xlsx` (hoja `LISTADO_MAESTRO`) |
| Pregunta | ¿Qué hay en Almera y qué calidad de datos tiene? | ¿Cómo va la vigencia y actualización de los documentos del SGC? |

- **Todo corre en el navegador** con SheetJS y Chart.js (`vendor/`). El Excel nunca sale del equipo.
- KPIs clicables (abren el detalle y se exportan a Excel), antigüedad por rangos, gráficos, reglas de calidad de datos, tabla con filtros y exportación, PDF por impresión del navegador.
- **Indicadores personalizados sin código** (`custom-kpis.js`): campo + condición + severidad, guardados en `localStorage`, con exportar/importar `.json`. Comparan sin importar mayúsculas, tildes, espacios ni coma o punto decimal.
- No cargan el menú compartido a propósito: son herramientas autocontenidas.

Detalle: [02-informes.md](02-informes.md).

### 4.4 Sitio y navegación

- **Portada** (`index.html`) con 4 entradas: Almera, Agentes de IA, Control de documentos SGC y Pregúntale a SABIA.
- **HTML, CSS y JS plano**, sin framework ni build. Tipografía DM Sans + JetBrains Mono.
- **Menú compartido** (`almera/assets/nav.js`, diseño "1c"): un solo script que cada página incluye con `data-base` (ruta relativa a la raíz). Se monta en `[data-sabnav]`, en el header o fijo arriba a la derecha.
- **Todos los enlaces son relativos y sin puertos**, así el sitio funciona igual en local, en Render o con cualquier servidor de archivos.
- Sin el servidor de `rag/` (por ejemplo con `npx serve`) funciona todo menos el chat.

Detalle: [`routes.md`](../routes.md).

### 4.5 Asistente "Pregúntale a SABIA"

- Chat en **`/asistente/`**, con la identidad visual del sitio y el mismo menú.
- Responde con **ruta exacta y pasos numerados**, advierte cuando algo está "pendiente de validar", y termina con una línea **"Fuente:"**.
- Muestra en qué módulo buscó y qué secciones consultó. Un **selector** permite fijar el módulo si el enrutador se equivoca.
- Respuesta en *streaming* (va apareciendo mientras se genera). Markdown pintado con `marked` y sanitizado con `DOMPurify`.
- El servidor **no guarda conversaciones**: el historial vive en la página y se envía en cada pregunta (máximo los últimos 8 mensajes).
- Botón **"+ Aportar un documento"**: descarga la plantilla de Word y el prompt de limpieza, pide módulo, archivo, nombre y clave, publica y muestra el semáforo al instante. Si el nombre ya existe, pide confirmación para reemplazar. Recuerda el nombre del autor en el navegador (`localStorage`, clave `sabia-autor`).
- Si la sesión vence (respuesta 401), redirige a `/login`.

### 4.6 ETL de conocimiento

```
Extraer (MarkItDown) ──► Transformar (código, sin IA) ──► Validar (semáforo) ──► Cargar
```

- **Formatos:** `.docx`, `.pdf`, `.pptx`, `.xlsx`, `.md`, `.txt`. Los antiguos (`.doc`, `.ppt`, `.xls`) salen en 🔴 con la instrucción de "Guardar como".
- **Transformar sin IA**, para no alterar nunca un procedimiento: quita imágenes y números de página, encabezados y pies repetidos (solo PDF y PPTX), textos de ejemplo de la plantilla, `<…>` en títulos y secciones vacías; convierte en título los párrafos que son solo negrita; limpia `NaN` de Excel; agrega un título si no hay.
- **Semáforo:** 🟢 publica · 🟡 publica con advertencias · 🔴 no publica (reglas completas en §6.7).
- **Cargar:** escribe `rag/generado/<módulo>/<slug>-<sha8>.md` con una ficha de origen y un `manifest.json`. **Nunca modifica los originales.** Solo reprocesa lo que cambió (fecha y tamaño), salvo que suba `ETL_VERSION`.
- **Disparadores:** ciclo periódico (`ETL_INTERVAL_SECONDS`, 300 s) y cada subida por el chat.
- Lo que no se puede limpiar por código (transcripciones, PDF escaneados) se convierte con el **prompt de limpieza** en la IA aprobada por la entidad y se sube como `.txt`.

---

## 5. Arquitectura

### 5.1 Vista general (producción)

```
                          Internet (HTTPS)
 Profesional del área ───────────────────────►  Render · servicio web "sabia" (plan free, Virginia)
 (navegador, cualquier equipo)                  ┌────────────────────────────────────────────────────────┐
                                                │ FastAPI + Uvicorn (rag/app/main.py)                    │
                                                │                                                        │
                                                │  middleware require_login ── cookie sabia_sesion (HMAC)│
                                                │                                                        │
                                                │  /, /almera, /styles, /calidad-ai-agents ── sitio      │
                                                │  /asistente/ ── chat (rag/static)                      │
                                                │  /api/chat ──► BM25 ──► prompt ──► OpenRouter ─────────┼──► Modelo LLM
                                                │                  ▲                                     │
                                                │        KnowledgeBase (en memoria)                      │
                                                │          ▲                    ▲                        │
                                                │   guías curadas        rag/generado/*.md ◄── ETL       │
                                                │   (sources.json)                            ▲          │
                                                │                                  rag/nube/ (copia)     │
                                                │  /api/upload ── almacen.save ──┐            ▲          │
                                                └────────────────────────────────┼────────────┼──────────┘
                                                                                 │ PUT        │ tarball
                                                                                 ▼ contents   │ (si hay commit nuevo)
                                                          GitHub · faazdy/sabia-conocimiento (privado)
                                                          una carpeta por módulo · cada aporte = 1 commit

           push a master                                  auto-deploy
 Equipo técnico ─────────► GitHub · faazdy/almera-docs ─────────────► Render (build + start)
                           (código, sitio, guías curadas, render.yaml)
```

### 5.2 Vista local (desarrollo y respaldo)

```
 Navegador ──► http://127.0.0.1:8800 ──► mismo servidor FastAPI
                                          KNOWLEDGE_DIR = rag/carpeta-compartida  (o \\servidor\Calidad\SABIA)
                                          ESTADO SABIA.txt se escribe en esa carpeta
```

El mismo código decide el modo por configuración:

| Variable | Modo | Carpeta de documentos aportados |
|---|---|---|
| `GITHUB_REPO` con valor | **Nube** | `rag/nube/` (copia del repo, se rehace al arrancar) |
| `GITHUB_REPO` vacío y `KNOWLEDGE_DIR` con valor | **Carpeta** (local o red) | La ruta de `KNOWLEDGE_DIR` |
| Las dos vacías | **Solo guías curadas** | — (el botón de aportar no aparece) |

### 5.3 Qué pasa en cada pregunta

1. **Navegador:** `POST /api/chat` con el historial y, si se fijó, el módulo.
2. **Autenticación:** el middleware valida la cookie de sesión; si no es válida responde 401 y el chat redirige a `/login`.
3. **Validar:** se toman los últimos 8 mensajes; el último debe ser del usuario y tener máximo 4000 caracteres.
4. **Enrutar** (`knowledge.py`):
   - Une las dos últimas preguntas del usuario (para que "¿y cómo lo apruebo?" siga en el mismo módulo).
   - Normaliza (minúsculas, sin tildes), quita palabras vacías y recorta terminaciones (`stem()`).
   - Puntúa con **BM25** (`k1=1.5`, `b=0.75`) todas las secciones (`#`–`###`) de todas las guías. El título pesa 3 veces más que el cuerpo; el nombre y la descripción del catálogo, 2 veces.
   - Suma los 3 mejores puntajes de cada módulo. Elige el mejor y un segundo si saca ≥ 60 % del primero. Si el usuario fijó un módulo, usa solo ese.
5. **Armar el contexto:** el árbol de Admin + los **documentos completos** de los módulos elegidos, cada uno dentro de `<documento>`. Si no caben en `MAX_CONTEXT_CHARS` (120 000), se meten primero los documentos con mejor puntaje.
6. **Prompt de sistema** (`prompts.py`): 7 reglas (ruta y pasos exactos, no inventar, decir cuando no está, advertir pendientes, línea "Fuente:", español claro, avisar si es otro módulo) + lista de módulos + contexto.
7. **Modelo** (`llm.py`): POST a OpenRouter desde el servidor, con *streaming*, `temperature 0.2` y, si se configuró, `provider.data_collection = deny`.
8. **Respuesta:** eventos SSE `meta` (módulos y fuentes) → `delta` (texto, varios) → `error` (si falla) → `done`.

El modelo **no lee archivos ni recuerda nada**: en cada pregunta el servidor le pega el texto relevante.

### 5.4 Qué pasa en cada aporte (modo nube)

1. El chat envía `POST /api/upload?module=…&filename=…&replace=…&autor=…` con el archivo como cuerpo crudo y la cabecera `X-Clave-Aportes`.
2. El servidor valida: clave para aportar, nombre del autor (obligatorio en la nube), módulo que acepta aportes, extensión soportada, tamaño ≤ `MAX_UPLOAD_MB` (20 MB), archivo no vacío. El nombre se limpia: sin carpetas ni caracteres prohibidos en Windows.
3. Con el candado del ETL tomado:
   1. Si el archivo ya existe y no se pidió reemplazar → **409** (el chat pregunta "¿Reemplazarlo?").
   2. **Primero GitHub:** `almacen.save()` hace `PUT /repos/{repo}/contents/{módulo}/{archivo}` con el mensaje `Aporte: Indicadores/x.docx · por Ana` (o `Actualiza: …`). Si GitHub falla, no se publica nada (**503**).
   3. Escribe la copia local en `rag/nube/<módulo>/` de forma atómica (archivo temporal `.subida-*.tmp` + `os.replace`).
   4. Corre el ETL en ese momento y devuelve el semáforo con sus notas.
4. Si nadie más cambió el repo entretanto, actualiza el sha sincronizado para no volver a descargar todo en la próxima revisión.

### 5.5 Sincronización con GitHub (`app/almacen.py`)

El disco de Render (plan gratis) se borra en cada reinicio o despliegue. Por eso el repo `sabia-conocimiento` es **la única copia persistente** de los documentos aportados.

- **Al arrancar y cada 300 s** (`etl_loop` → `refresh_knowledge(pull=True)`):
  1. `GET /repos/{repo}/commits/{rama}` con `Accept: application/vnd.github.sha` → sha del último commit.
  2. Si es igual al último sincronizado y `rag/nube/` existe, no hace nada.
  3. Si cambió, descarga el **tarball** del commit y lo aplica sobre `rag/nube/`:
     - Solo archivos **dentro de una carpeta** (los sueltos en la raíz del repo, como `README.md`, `LEEME.txt` o la plantilla, se ignoran).
     - Ignora todo lo que empiece por `.` (por ejemplo `.gitkeep`) y rutas con `..`.
     - Solo reescribe los archivos que cambiaron, para que el ETL no reprocese todo.
     - Borra de la copia local lo que ya no está en el repo (borrado o movido desde github.com).
  4. Corre el ETL.
- Un repo vacío (sin commits) responde 409 y se trata como "nada que descargar". Por eso el repo se crea con *Add a README*.
- **Consecuencia operativa:** cualquier cambio hecho directamente en github.com (subir, borrar, mover) llega a SABIA en máximo 5 minutos, sin reiniciar.

### 5.6 Autenticación

| Mecanismo | Protege | Cómo funciona |
|---|---|---|
| `SITE_PASSWORD` | Todo: sitio, chat y API | Formulario HTML `/login` → `POST /api/login`. Si la clave es correcta, cookie `sabia_sesion` = `<vencimiento>.<HMAC-SHA256>`, con llave derivada de `SITE_PASSWORD`. `HttpOnly`, `SameSite=Lax`, `Secure` si llega por HTTPS (`X-Forwarded-Proto`). Dura 30 días |
| `UPLOAD_PASSWORD` | Solo `/api/upload` | Cabecera `X-Clave-Aportes`, comparada en tiempo constante |
| Token de GitHub | Escritura en `sabia-conocimiento` | Solo lo usa el servidor; nunca llega al navegador |

- **Sin base de datos de sesiones:** la cookie lleva su vencimiento firmado. Cambiar `SITE_PASSWORD` invalida **todas** las sesiones.
- **Antifuerza bruta:** 30 intentos fallidos en 10 minutos bloquean el login unos minutos. Es un tope **global**, no por IP, porque detrás del proxy de Render la IP se puede falsear. Las sesiones abiertas siguen funcionando.
- `/login?next=…` solo redirige a rutas del mismo sitio (evita redirecciones abiertas).
- `/salir` borra la cookie.
- Con las claves vacías (modo local) no se pide nada.

### 5.7 Ciclo de vida del proceso

- Un solo proceso Uvicorn, un solo worker.
- Al arrancar, `state["kb"]` se construye con las guías curadas + lo que haya en `rag/generado/`. En Render ese disco empieza vacío, así que **los primeros segundos tras despertar solo hay guías curadas** hasta que el primer ciclo del ETL descarga y procesa los aportes.
- `lifespan` lanza `etl_loop` como tarea de fondo si hay carpeta de documentos. Cada vuelta corre en un hilo (`asyncio.to_thread`). Si falla (GitHub o la red caídos), se registra y se reintenta en la siguiente.
- Cuando el ETL publica cambios, se construye una **base nueva** y se reemplaza la referencia entera. Cada petición toma la referencia vigente al empezar, así nunca ve una base a medio construir.
- `etl_lock` (reentrante) evita que el ciclo periódico y una subida trabajen a la vez sobre la carpeta y el `manifest.json`.

### 5.8 Dónde vive cada dato

No hay base de datos. Todo son archivos.

| Dato | Dónde | Persistente en Render | Respaldo |
|---|---|---|---|
| Código, sitio, guías curadas | Repo `almera-docs` | Sí (viene del repo en cada build) | Git |
| Documentos aportados (originales) | Repo `sabia-conocimiento` | Sí (fuente de verdad) | Git (historial completo) |
| Copia local de aportes | `rag/nube/` | **No** (se rehace) | No hace falta |
| Salida del ETL | `rag/generado/` + `manifest.json` | **No** (se regenera) | No hace falta |
| Configuración y secretos | Variables de entorno de Render / `rag/.env` en local | Sí (en Render) | Gestor de contraseñas |
| Sesiones | Cookie del navegador | — | — |
| Conversaciones | Solo en la página del navegador | No se guardan | — |
| Autor recordado | `localStorage` del navegador | — | — |
| KPIs personalizados de los informes | `localStorage` del navegador | — | Exportar `.json` desde el panel |
| Intentos fallidos de login | Memoria del proceso | No | — |

---

## 6. Referencia técnica del servidor

### 6.1 Archivos del servidor (`rag/`)

| Archivo | Responsabilidad |
|---|---|
| `app/main.py` | App FastAPI: login y sesión, cabecera `no-cache`, `/api/chat`, `/api/modules`, `/api/upload`, `/api/descargas/*`, chat estático, sitio (`SITE_DIRS`), ciclo del ETL |
| `app/config.py` | Lee `rag/.env` y el entorno; rutas; límites fijos (`MAX_QUESTION_CHARS=4000`, `MAX_HISTORY_MESSAGES=8`) |
| `app/knowledge.py` | Carga el catálogo y las guías, parte por secciones, índice BM25, `route()`, `build_context()`, `catalog()` |
| `app/etl.py` | Extraer, limpiar, semáforo, publicar en `generado/`, `manifest.json`, `ESTADO SABIA.txt`. Ejecutable con `python -m app.etl` |
| `app/almacen.py` | Modo nube: `pull()` (descarga el repo si hay commit nuevo), `apply_tarball()`, `save()` (commit de un aporte) |
| `app/llm.py` | Cliente de OpenRouter con *streaming*, `truststore` y manejo de errores |
| `app/prompts.py` | Prompt de sistema |
| `sources.json` | Catálogo de módulos y guías curadas |
| `static/index.html`, `app.js`, `style.css` | Interfaz del chat y del diálogo de aportes |
| `static/login.html` | Página de entrada |
| `static/vendor/` | `marked` 12.0.2 y `DOMPurify` 3.1.6, locales |
| `conocimiento/alimentar-sabia.md` | Guía del módulo "SABIA (cómo alimentarlo)" |
| `carpeta-compartida/` | Modelo de carpeta: subcarpetas por módulo, `LEEME.txt`, `PROMPT para limpiar con IA.txt`, `Plantilla guía SABIA.docx`. Las descargas del chat salen de aquí |
| `iniciar.ps1` | Arranque en Windows: crea `.venv`, instala dependencias, crea `.env`, arranca |
| `requirements.txt` | Dependencias fijadas |
| `.env.example` | Plantilla de configuración |

### 6.2 Endpoints

| Método y ruta | Auth | Qué hace | Respuesta |
|---|---|---|---|
| `GET /login` | Abierta | Página de entrada (redirige a `/` si no hay `SITE_PASSWORD`) | HTML |
| `POST /api/login` | Abierta | Formulario `clave`, `next` | 303 a `next` con cookie, o a `/login?error=clave\|bloqueo` |
| `GET /salir` | — | Cierra la sesión | 303 a `/login` |
| `GET /`, `/index.html` | Sesión | Portada | `index.html` |
| `GET /almera/…`, `/styles/…`, `/calidad-ai-agents/…` | Sesión | Sitio estático | Archivos |
| `GET /asistente/` | Sesión | Chat | `rag/static/index.html` |
| `GET /asistente/static/…` | Sesión | CSS/JS del chat | Archivos |
| `GET /api/modules` | Sesión | Catálogo para el chat | `{model, modules[], upload, upload_key, max_upload_mb}` |
| `POST /api/chat` | Sesión | Pregunta. Cuerpo `{messages:[{role, content}], module}` | SSE: `meta`, `delta`*, `error`?, `done` |
| `POST /api/upload` | Sesión + `X-Clave-Aportes` | Query `module`, `filename`, `replace`, `autor`; cuerpo = bytes | `{file, module, status, notes}` o 400/403/409/413/423/503 |
| `GET /api/descargas/plantilla`, `/prompt` | Sesión | Plantilla de Word y prompt de limpieza | Archivo |

Sin sesión, las rutas `/api/*` responden **401** y las demás redirigen a `/login?next=…`. Todo lo que no es `/api/` sale con `Cache-Control: no-cache` (el navegador revalida con ETag y recibe 304 si no cambió). `/docs`, `/redoc` y `/openapi.json` están desactivados.

### 6.3 Variables de configuración

| Variable | Por defecto (código) | Render | Qué hace |
|---|---|---|---|
| `OPENROUTER_API_KEY` | — | Secreta | Llave de OpenRouter |
| `OPENROUTER_MODEL` | `anthropic/claude-haiku-5.5` | `nvidia/nemotron-3-ultra-550b-a55b:free` | Modelo del asistente |
| `OPENROUTER_DENY_DATA_COLLECTION` | `true` | `false` | `true` = solo proveedores que no guardan ni entrenan con los prompts |
| `HOST` | `127.0.0.1` | `0.0.0.0` | Interfaz de escucha |
| `PORT` | `8800` | La pone Render | Puerto |
| `MAX_CONTEXT_CHARS` | `120000` | — | Tope de documentación por pregunta (~4 caracteres por token) |
| `KNOWLEDGE_DIR` | vacío (el `.env.example` trae `carpeta-compartida`) | Se ignora | Carpeta de aportes en modo local. Ruta de red **sin comillas** |
| `ETL_INTERVAL_SECONDS` | `300` | — | Cada cuánto se revisan la carpeta o el repo |
| `MAX_UPLOAD_MB` | `20` | — | Tamaño máximo de un aporte |
| `GITHUB_REPO` | vacío | Secreta (`usuario/sabia-conocimiento`) | Activa el modo nube |
| `GITHUB_TOKEN` | vacío | Secreta | Token *fine-grained*: solo ese repo, *Contents: Read and write* |
| `GITHUB_BRANCH` | `main` | — | Rama del repo de conocimiento |
| `SITE_PASSWORD` | vacío | Secreta | Clave de entrada; también llave de firma de las sesiones |
| `UPLOAD_PASSWORD` | vacío | Secreta | Clave para aportar |
| `PYTHON_VERSION` | — | `3.13.15` | Versión de Python en Render |

### 6.4 Catálogo (`rag/sources.json`)

```json
{
  "shared": ["almera/assets/almera-structure.md"],
  "modules": [
    {
      "id": "indicadores",                 // identificador estable (carpeta y API)
      "name": "Indicadores",               // nombre visible y nombre de carpeta
      "description": "Ficha técnica, …",   // pesa en el enrutamiento: usar las palabras de la gente
      "files": ["almera/…/indicadores.md"],// guías curadas, rutas desde la raíz del repo ([] si no hay)
      "uploads": true                      // opcional; false = no acepta aportes
    }
  ]
}
```

- Las carpetas de aportes se reconocen por `id`, por `name` o por cada parte de un nombre con `/` ("Evaluaciones / Auditorías" acepta `Evaluaciones`). No importan mayúsculas, tildes, guiones ni guiones bajos.
- Si una ruta de `files` no existe, el servidor **no arranca** (`FileNotFoundError`). Un JSON mal formado tampoco.

### 6.5 Enrutador (`knowledge.py`)

| Parámetro | Valor | Dónde |
|---|---|---|
| Niveles de título que parten secciones | `#`, `##`, `###` (fuera de bloques de código) | `HEADING_RE`, `split_sections()` |
| Secciones ignoradas | Las que empiezan por "Árbol de…" o "Índice" | `NOISY_SECTIONS` |
| Palabras vacías | Español común + "almera", "sistema", "modulo", "opcion", "te", "ti"… | `STOPWORDS` |
| Recorte de terminaciones | De la más larga a la más corta, una sola vez, dejando ≥ 4 letras | `SUFFIXES`, `stem()` |
| BM25 | `k1=1.5`, `b=0.75` | `_bm25()` |
| Puntaje de módulo | Suma de sus 3 mejores secciones | `route()` |
| Segundo módulo | Si alcanza ≥ 60 % del primero (máximo 2 módulos) | `route()` |
| Fuentes mostradas | Las 4 secciones con mejor puntaje de lo enviado | `route()` |

**Cuándo pasar a un RAG con embeddings:** si el conocimiento supera ~150 000 tokens o cientos de documentos. El punto de cambio es `KnowledgeBase.route()`.

### 6.6 Cliente del modelo (`llm.py`)

- Endpoint `https://openrouter.ai/api/v1/chat/completions` (formato compatible con OpenAI).
- `stream: true`, `temperature: 0.2`, cabecera `X-Title: SABIA - Almera RAG`.
- Timeout de 120 s (10 s para conectar).
- Certificados del sistema con `truststore` (la red corporativa inspecciona TLS).
- Errores HTTP de OpenRouter → mensaje legible dentro del stream (`OpenRouter respondió 4xx: …`).

### 6.7 Reglas del semáforo (`etl.py`)

| Color | Condición |
|---|---|
| 🔴 | Plantilla sin llenar (poco texto + ≥ 5 textos de ejemplo) |
| 🔴 | Casi sin texto: cuerpo < 80 caracteres, o < 200 sin títulos (escaneado o imagen) |
| 🔴 | ≥ 10 líneas que terminan en hora (`12:34`): transcripción de reunión |
| 🔴 | ≥ 10 líneas de 1–2 caracteres y > 8 % del total: texto desarmado |
| 🔴 | > 20 000 caracteres sin ningún título |
| 🔴 | Formato antiguo, no soportado, archivo suelto en la raíz o carpeta que no es un módulo |
| 🔴 | No se pudo abrir (dañado o con contraseña) |
| 🟡 | Menos de 2 títulos |
| 🟡 | Hubo títulos que estaban solo en negrita y se convirtieron |
| 🟡 | Tenía imágenes (no se pueden leer) |
| 🟡 | Alguna sección de más de 15 000 caracteres |
| 🟢 | Ninguna de las anteriores |

Notas informativas (no cambian el color): encabezados, pies y números de página quitados; textos de ejemplo de la plantilla quitados.

`ETL_VERSION` (hoy `"2"`): súbelo cuando cambie la limpieza, el semáforo o la versión de MarkItDown, para que se reprocese todo.

### 6.8 Frontend del chat (`rag/static/app.js`)

- `api()` envuelve `fetch` y redirige a `/login` ante un 401.
- `loadModules()` llena el selector de módulo y la lista del diálogo de aportes (solo módulos con `uploads ≠ false`), y muestra u oculta el botón de aportar y el campo de clave según `/api/modules`.
- `ask()` lee el stream SSE y va pintando el Markdown sanitizado.
- `sendFile()` sube el archivo con `Content-Type: application/octet-stream` y `X-Clave-Aportes`. Ante un 409 pregunta si reemplazar.

---

## 7. Stack tecnológico

| Capa | Tecnología | Versión | Para qué |
|---|---|---|---|
| Frontend | HTML, CSS, JavaScript plano | — | Sitio, informes, chat, menú (sin framework ni build) |
| | DM Sans, JetBrains Mono (Google Fonts) | — | Tipografía |
| | Chart.js, SheetJS | Locales en `vendor/` | Gráficos y lectura de Excel en los informes |
| | marked, DOMPurify | 12.0.2, 3.1.6 | Markdown seguro en el chat |
| Backend | Python | 3.13 (3.13.15 en Render) | Servidor |
| | FastAPI + Uvicorn | 0.115.12, 0.34.2 | Web, API, archivos estáticos |
| | httpx | 0.28.1 | OpenRouter (*streaming*) y API de GitHub |
| | python-dotenv | 1.1.0 | `rag/.env` |
| | truststore | 0.10.1 | Certificados del sistema operativo |
| | MarkItDown (Microsoft) | 0.1.9 | Word/PDF/PPT/Excel → Markdown |
| IA | OpenRouter | — | Acceso a modelos con una sola llave |
| | Modelo en producción | `nvidia/nemotron-3-ultra-550b-a55b:free` | Respuestas del asistente |
| | Claude Agent Skills | — | Las 10 skills |
| Búsqueda | BM25 propio en Python puro | — | Enrutamiento sin base vectorial |
| Datos | Markdown y archivos de Office en Git | — | No hay base de datos |
| Infraestructura | Render (Web Service, plan free) | Blueprint `render.yaml` | Hosting con HTTPS y auto-deploy |
| | GitHub | `faazdy/almera-docs`, `faazdy/sabia-conocimiento` | Código y almacén de aportes |
| Herramientas | Git, Claude Code, Claude Design, Node.js (opcional) | — | Desarrollo, diseño, `npm start`, PDF de los docs |

**Lo que deliberadamente NO se usó:** base de datos, base vectorial ni embeddings, framework de frontend, LangChain u otro framework de LLM, Docker. Con el volumen actual no se justifican y cada uno suma mantenimiento (§10).

---

## 8. DevOps: repositorios, despliegue y operación

### 8.1 Repositorios

| | `faazdy/almera-docs` | `faazdy/sabia-conocimiento` |
|---|---|---|
| Visibilidad | Privado | **Privado** |
| Rama | `master` | `main` (`GITHUB_BRANCH`) |
| Qué contiene | Código del servidor, sitio, guías curadas, skills, informes, documentación, `render.yaml` | Documentos aportados por el área (originales), una carpeta por módulo |
| Quién escribe | Equipo técnico (git push) | El servidor de SABIA (token) y el equipo técnico desde github.com o git |
| Efecto de un cambio | Render vuelve a desplegar el servicio (1–3 min) | SABIA lo toma en la siguiente revisión (≤ 5 min), sin redesplegar |
| Qué NO va aquí | `rag/.env`, `.venv/`, `generado/`, `nube/`, `ESTADO SABIA.txt` (en `.gitignore`) | Nada de datos personales ni confidenciales: todo termina en las respuestas |

**Estructura actual de `sabia-conocimiento`:**

```
sabia-conocimiento/
├── README.md                          (ignorado: está en la raíz)
├── LEEME.txt                          (ignorado)
├── PROMPT para limpiar con IA.txt     (ignorado)
├── Plantilla guía SABIA.docx          (ignorado)
├── Documentos/.gitkeep
├── Evaluaciones/.gitkeep
├── General/Administracion_Usuarios.docx
├── Indicadores/crear-indicadores.docx
├── Mapa de procesos/.gitkeep
├── Mecanismos de integración/.gitkeep
├── Modelos de gestión/.gitkeep
├── Planes de mejora/.gitkeep
└── Proyectos/.gitkeep
```

**Mensajes de commit:** los del servidor siguen el formato `Aporte: <Módulo>/<archivo> · por <Nombre>` o `Actualiza: …`. El autor técnico del commit es la cuenta dueña del token; la persona que aportó queda en el mensaje.

### 8.2 Render

**Blueprint (`render.yaml` en la raíz de `almera-docs`):**

| Campo | Valor | Por qué |
|---|---|---|
| `type` | `web` | Servicio HTTP público |
| `name` | `sabia` | Nombre del servicio y prefijo de la URL `https://sabia-xxxx.onrender.com` |
| `runtime` | `python` | Entorno nativo, sin Docker |
| `plan` | `free` | Costo cero (§8.7) |
| `region` | `virginia` | Región de Render |
| `buildCommand` | `pip install -r rag/requirements.txt` | Instala dependencias en cada despliegue |
| `startCommand` | `cd rag && python -m app.main` | Mismo arranque que en local |
| `PYTHON_VERSION` | `3.13.15` | Versión fija y probada |
| `HOST` | `0.0.0.0` | Escuchar fuera del contenedor |
| `OPENROUTER_MODEL`, `OPENROUTER_DENY_DATA_COLLECTION` | Valores fijos en el archivo | Iguales al `.env` local; sin esto el servicio caía al modelo por defecto |
| `OPENROUTER_API_KEY`, `GITHUB_REPO`, `GITHUB_TOKEN`, `SITE_PASSWORD`, `UPLOAD_PASSWORD` | `sync: false` | Secretos: Render los pide al crear el servicio y **nunca** se escriben en el repo |

`PORT` lo inyecta Render y `config.py` lo lee. El servidor detecta HTTPS por `X-Forwarded-Proto` para marcar la cookie como `Secure`.

**Ciclo de despliegue:**

```
git push origin master ──► Render detecta el commit ──► build (pip install) ──► start (python -m app.main)
                                                                                  │
                                       al arrancar: guías curadas en memoria ◄────┤
                                       primer ciclo ETL: pull de sabia-conocimiento ──► rag/nube/ ──► generado/ ──► base actualizada
```

- No hay pipeline de pruebas: lo que llega a `master` se despliega. **Prueba en local antes de hacer push** (§8.5).
- Si el arranque falla (por ejemplo `sources.json` apunta a un archivo inexistente o falta `GITHUB_TOKEN`), Render lo marca como fallido y deja corriendo la versión anterior.

### 8.3 Instalación desde cero (una sola vez)

1. **Repo de conocimiento:** en GitHub crear `sabia-conocimiento` **privado**, marcando *Add a README* (un repo vacío no tiene rama `main` y la API responde 409).
2. **Token:** GitHub → *Settings → Developer settings → Fine-grained tokens → Generate new token*:
   - *Repository access*: **Only select repositories** → `sabia-conocimiento`.
   - *Permissions → Contents*: **Read and write**. Nada más.
   - Anotar la **fecha de vencimiento** (§8.6).
3. **OpenRouter:** crear una llave en <https://openrouter.ai/keys>, con **límite de gasto**.
4. **Render:** crear la cuenta con GitHub → *New → Blueprint* → repo `almera-docs`. Render lee `render.yaml` y pide los 5 secretos:

   | Variable | Valor |
   |---|---|
   | `OPENROUTER_API_KEY` | Llave del paso 3 |
   | `GITHUB_REPO` | `faazdy/sabia-conocimiento` |
   | `GITHUB_TOKEN` | Token del paso 2 |
   | `SITE_PASSWORD` | Clave de entrada para todo el personal (mínimo 12 caracteres) |
   | `UPLOAD_PASSWORD` | Clave para quienes publican documentos |

5. Esperar el primer despliegue, abrir la URL, entrar con `SITE_PASSWORD` y hacer la prueba de humo (§8.5).
6. Opcional: crear en `sabia-conocimiento` las carpetas de los módulos (con un `.gitkeep`) y subir el material inicial.

### 8.4 Operación diaria

| Tarea | Cómo |
|---|---|
| Aportar o reemplazar un documento | Botón **+ Aportar un documento** del chat (nombre + `UPLOAD_PASSWORD`) |
| Aportar directo al repo | github.com → `sabia-conocimiento` → carpeta del módulo → *Add file → Upload files* → *Commit changes*. O con `git clone` / `git push`. Siempre **dentro** de una carpeta de módulo |
| Borrar o mover un documento aportado | Borrarlo o moverlo en `sabia-conocimiento`. SABIA lo retira en ≤ 5 min |
| Deshacer un aporte | Revertir el commit o restaurar la versión anterior del archivo en `sabia-conocimiento` |
| Ver quién aportó qué | Historial de commits de `sabia-conocimiento` |
| Cambiar una guía curada o el código | Commit y push a `master` de `almera-docs` → despliegue automático |
| Agregar una guía curada nueva | Crear el `.md`, sumarlo a `files` de su módulo en `rag/sources.json`, push |
| Agregar un módulo | Entrada nueva en `modules` de `sources.json`, push. Su carpeta en `sabia-conocimiento` se crea con el primer aporte |
| Cambiar una clave | Render → servicio `sabia` → *Environment*. Al guardar reinicia. Cambiar `SITE_PASSWORD` cierra todas las sesiones |
| Cambiar de modelo | Editar `OPENROUTER_MODEL` en `render.yaml` (y push) o en *Environment* de Render. Repetir la prueba de humo |
| Cerrar sesión en un equipo | Abrir `/salir` |
| Ver el semáforo de un aporte hecho por github.com | Render → *Logs* (`ETL: {...}`), o simular localmente (§8.5) |

### 8.5 Desarrollo local y prueba antes de publicar

**Arrancar** (desde la raíz de `almera-docs`): `iniciar.bat` (doble clic), `npm start` o `cd rag; .\iniciar.ps1`. La primera vez crea `rag\.venv`, instala dependencias, crea `rag\.env` y se detiene para que pongas la llave. Luego: <http://127.0.0.1:8800/> y <http://127.0.0.1:8800/asistente/>.

Por defecto el modo local usa `rag/carpeta-compartida/` y no pide claves. Para probar contra el repo de conocimiento real, pon `GITHUB_REPO` y `GITHUB_TOKEN` en `rag/.env` (ojo: las subidas que hagas **sí** quedan como commits en el repo).

**Probar el semáforo sin servidor:** `cd rag; .venv\Scripts\python -m app.etl` procesa `KNOWLEDGE_DIR` una vez e imprime el resultado. Hazlo con el servidor detenido (los dos escriben el mismo `manifest.json`).

**Prueba de humo** (local antes del push, y en Render después):

| # | Qué | Esperado |
|---|---|---|
| 1 | Abrir la URL | Página **Entrar a SABIA** (en la nube) o portada (local) |
| 2 | Entrar con la clave | Portada; la sesión se mantiene al recargar |
| 3 | `/api/modules` | JSON con el modelo, 10 módulos y `"upload": true` |
| 4 | Preguntar "¿cómo creo un comité?" | Pasos + línea "Fuente:"; arriba "Mecanismos de integración" |
| 5 | Preguntar "¿cómo te alimento?" | Responde con la guía "SABIA (cómo alimentarlo)" |
| 6 | Aportar un `.docx` de prueba | Semáforo en pantalla y commit en `sabia-conocimiento`. **Borrarlo después** |
| 7 | Abrir `/rag/.env` | **404** |
| 8 | Abrir cada informe y cargar su Excel | KPIs, gráficos y filtros con valores |

### 8.6 Secretos y rotación

| Secreto | Dónde vive | Rotación | Si se filtra |
|---|---|---|---|
| `OPENROUTER_API_KEY` | Render *Environment*; `rag/.env` en local | Cuando haga falta | Revocarla en OpenRouter **de inmediato**, crear otra con límite de gasto, revisar el consumo |
| `GITHUB_TOKEN` | Render *Environment* | **Antes de su fecha de vencimiento** | Revocarlo en GitHub y generar otro (§8.3 paso 2) |
| `SITE_PASSWORD` | Render *Environment* | Cuando salga alguien del área o se comparta por fuera | Cambiarla: cierra todas las sesiones |
| `UPLOAD_PASSWORD` | Render *Environment* | Igual | Cambiarla y revisar el historial de `sabia-conocimiento` |

⚠️ **Cuando el token de GitHub vence**, los aportes fallan con "No se pudo guardar … en el almacén de SABIA" y el ciclo del ETL registra errores 401. El asistente sigue respondiendo con lo último descargado mientras el proceso no se reinicie; tras un reinicio, **sin token válido no tiene los documentos aportados**.

Nunca subir secretos a Git, ni pegarlos en correos, chats o capturas.

### 8.7 Plan gratis: comportamiento y límites

- **Se duerme** tras ~15 minutos sin tráfico. La siguiente visita tarda ~1 minuto en despertar.
- Al despertar, el disco está vacío: el servidor arranca con las guías curadas y, en el primer ciclo del ETL, descarga y reprocesa los aportes. **Durante esos primeros segundos los documentos aportados no están disponibles.**
- Un solo proceso: los intentos fallidos de login y el sha sincronizado viven en memoria y se pierden al reiniciar (no es un problema).
- Las horas gratuitas mensuales de Render alcanzan para un servicio encendido todo el mes; verificar los límites vigentes en el panel de Render.
- Si la latencia del primer acceso molesta, el plan pago más barato no se duerme.
- Los modelos `:free` de OpenRouter tienen **límites de peticiones por minuto y por día**. Si el uso crece, aparecerán errores 429: pasar a un modelo de pago (§11).

### 8.8 Logs y monitoreo

En la nube: Render → servicio `sabia` → *Logs*. En local: la consola donde se arrancó.

| Mensaje | Significa |
|---|---|
| `SABIA en http://0.0.0.0:…` + `Documentos aportados: GitHub faazdy/sabia-conocimiento (revisión cada 300s)` | Arranque correcto en modo nube |
| `Conocimiento descargado de GitHub (commit abc1234)` | Hubo commits nuevos y se descargaron |
| `ETL: {'verde': N, 'amarillo': N, 'rojo': N} · base actualizada` | El ETL publicó cambios |
| `ETL: … · base sin cambios` | Ciclo normal |
| `ETL falló` + traza | Error en el ciclo (por ejemplo GitHub 401/404). Se reintenta en 5 min |
| `Subida: <archivo> → <semáforo> (por <nombre>)` | Aporte publicado por el chat |
| `Subida: GitHub no respondió` + traza | Token vencido, sin permiso, conflicto o GitHub caído |
| `Login: demasiados intentos fallidos…` | Se activó el bloqueo de 10 minutos |
| `Falta GITHUB_TOKEN…` (y el servicio no arranca) | Falta el secreto en Render |

No hay alertas automáticas ni métricas de uso. Para saber si SABIA está arriba, abrir la URL.

### 8.9 Respaldo y recuperación

| Escenario | Qué hacer |
|---|---|
| Render caído o cuenta perdida | Arrancar SABIA en un equipo con `GITHUB_REPO` y `GITHUB_TOKEN` en `rag/.env`: tendrá exactamente el mismo conocimiento. O recrear el servicio desde el Blueprint (§8.3) |
| Despliegue roto | Render conserva la versión anterior corriendo. Corregir y hacer push, o usar *Rollback* en Render |
| Aporte borrado por error | Restaurarlo desde el historial de `sabia-conocimiento` |
| Repo de conocimiento perdido | Cualquier clon local lo contiene completo; volver a subirlo |
| Secreto comprometido | §8.6 |

Lo único que **no** tiene respaldo automático son los secretos: guardarlos en un gestor de contraseñas.

---

## 9. Seguridad

| Tema | Medida |
|---|---|
| Acceso | Todo el sitio, el chat y la API requieren `SITE_PASSWORD` en la nube. Sesión firmada con HMAC, `HttpOnly`, `Secure`, `SameSite=Lax` |
| Publicar conocimiento | Requiere además `UPLOAD_PASSWORD`, porque lo que se aporta termina en las respuestas |
| Fuerza bruta | 30 intentos fallidos en 10 minutos bloquean el login (global) |
| Transporte | HTTPS de Render |
| Qué publica el servidor | Solo `index.html`, `styles/`, `almera/`, `calidad-ai-agents/` (`SITE_DIRS`) y el chat. `rag/.env`, `rag/app/`, `.git/`, `docs/` y la raíz dan 404, también con `../` codificado |
| Secretos | Solo en variables de entorno o `rag/.env` (en `.gitignore`). La llave de OpenRouter y el token de GitHub nunca llegan al navegador |
| Mínimo privilegio | Token de GitHub limitado a un repo y a *Contents* |
| Contenido del modelo | Markdown sanitizado con DOMPurify antes de mostrarse |
| Límites de entrada | Pregunta ≤ 4000 caracteres, historial ≤ 8 mensajes, archivo ≤ 20 MB, solo formatos del ETL, solo el nombre del archivo (sin rutas) |
| Redirecciones | `next` del login restringido a rutas del mismo sitio |
| Historial | El servidor no guarda conversaciones. Un usuario técnico podría enviar un historial inventado: solo gasta créditos, no da acceso a nada más |
| Informes | El Excel se procesa en el navegador. El listado del SGC trae nombres de profesionales de la DEP: no subirlo al repo |

⚠️ **Privacidad del modelo en producción.** Con `OPENROUTER_DENY_DATA_COLLECTION=false` y un modelo `:free`, los proveedores **pueden guardar los prompts**, y cada prompt incluye la pregunta y la documentación enviada. Por eso:

- **No escribir datos personales, de afiliados, de pacientes ni información confidencial en el chat** (ver `calidad-ai-agents/SEGURIDAD.md` y la Ley 1581 de 2012).
- Los documentos aportados también viajan al modelo: deben ser solo procedimientos del sistema.
- Para usar información más sensible, cambiar a un modelo de pago y poner `OPENROUTER_DENY_DATA_COLLECTION=true`.

---

## 10. Decisiones de diseño y por qué

| Decisión | Por qué | Cuándo revisarla |
|---|---|---|
| **RAG-lite** (elegir el módulo e inyectar su guía completa) en vez de fragmentos con embeddings | El conocimiento cabe entero (~65 000 tokens). Partir en fragmentos corta procedimientos paso a paso, el peor error posible en este dominio | Si pasa de ~150 000 tokens o cientos de documentos |
| **BM25 léxico** para enrutar | Sin dependencias ni costo, determinista y fácil de depurar | Si el enrutador se equivoca seguido con preguntas reales |
| **Recorte de terminaciones propio** | Resolvía conjugaciones ("¿cómo te alimento?") sin dependencias. Medido con los títulos de las guías: perdió 4 de 291 aciertos | Si aparecen palabras que se confunden al recortarlas |
| **Render + GitHub** en vez del servidor del área | Sin infraestructura propia, sin costo, HTTPS y despliegue automático, sin depender de TI | Si se necesita red interna, más privacidad o sin tiempo de arranque en frío |
| **GitHub como almacén** de aportes | El disco gratis de Render es efímero. GitHub da persistencia, historial, autor y deshacer gratis; nadie del área necesita cuenta | Si el volumen de archivos o binarios crece mucho |
| **Primero commit, después publicar** | Si GitHub falla, no queda nada publicado que se pierda al reiniciar | — |
| **Polling cada 5 min** en vez de webhooks | No requiere endpoint público adicional ni secreto de webhook; 12 peticiones por hora a la API | Si se necesita que un cambio en github.com se vea al instante |
| **Login con formulario** en vez de *basic auth* del navegador | El navegador ofrece guardar la clave y la sesión dura 30 días | — |
| **Sesión firmada sin base de datos** | Sin estado que persistir en un disco efímero. Cambiar la clave cierra todo | Si se necesitan usuarios individuales |
| **Una clave compartida** en vez de cuentas | El área no tiene que crear cuentas; la clave de aportes separa a quienes publican | Si se requiere trazabilidad por persona en las preguntas |
| **Módulo de autoayuda** ("SABIA (cómo alimentarlo)") | Las preguntas sobre el propio asistente siguen el mismo camino; la guía se edita como cualquier `.md` | — |
| **`"uploads": false`** por módulo | Evita aportes a módulos cuyo contenido controla el equipo técnico | — |
| **OpenRouter** en vez de un proveedor fijo | Cambiar de modelo es una línea de configuración | — |
| **Modelo `:free` en producción** | Costo cero mientras se valida el uso | Si hay errores 429 o se necesita no retención de datos |
| **Un solo servidor** para sitio y chat | Enlaces relativos, sin puertos fijos entre sitio y chat | — |
| **Lista cerrada de carpetas publicadas** (`SITE_DIRS`) | Montar la raíz expondría `rag/.env` y `.git` | Al agregar una carpeta de primer nivel |
| **ETL sin IA y que no toca los originales** | La limpieza por código no altera procedimientos; mover archivos ajenos genera conflictos | — |
| **`no-cache` en el sitio** en vez de versionar archivos | No hay build; el navegador revalida y recibe 304 si no cambió | Si el sitio se sirve desde otro servidor web |
| **`truststore`** en vez de desactivar SSL | La red corporativa inspecciona TLS con un certificado propio | — |
| **Sin framework, sin build, sin Docker** | Cualquiera puede abrir y editar un archivo; menos piezas que mantener | Si el frontend crece mucho |

---

## 11. Costos

| Concepto | Hoy | Alternativa |
|---|---|---|
| Hosting (Render) | US$0 (plan free) | Plan pago más barato: sin arranque en frío |
| Almacén (GitHub privado) | US$0 | — |
| Modelo | US$0 (`nemotron … :free`), con límites de uso y sin garantía de no retención | `anthropic/claude-haiku-5.5`: unos **US$0,002 por pregunta** (8–17 mil tokens de entrada). Mil preguntas al mes ≈ US$2 |
| **Total** | **US$0 / mes** | |

Con un modelo de pago, configurar **siempre un límite de gasto** en la llave de OpenRouter.

---

## 12. Pendientes, riesgos y deuda técnica

### 12.1 Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **El `.skill` de `diagramas-flujo` es la única copia del generador** | Perder la skill | Extraerlo sobre `calidad-ai-agents/diagramas-flujo/` y commitear ([01-skills.md §3.4](01-skills.md)) |
| **Vencimiento del token de GitHub** | Fallan los aportes; tras un reinicio se pierden los aportes del asistente | Anotar la fecha y renovarlo antes (§8.6) |
| **Privacidad del modelo `:free`** | Los prompts pueden quedar guardados en el proveedor | Regla de no escribir datos personales; pasar a modelo de pago con `deny` si hace falta (§9) |
| **Límites del modelo gratis** | Errores 429 con más usuarios | Pasar a un modelo de pago con límite de gasto |
| **Tres copias por módulo de Almera** sincronizadas a mano | Respuestas distintas según el canal | Ya hay desfase en Evaluaciones y Planes de mejora |
| **Sin pruebas automatizadas ni CI** | Un push roto se despliega directo | Prueba de humo local antes del push (§8.5) |
| **Una sola persona con acceso** a Render, GitHub y OpenRouter (si es el caso) | Dependencia de una persona | Dar acceso a un segundo administrador y guardar los secretos en un gestor compartido |
| **Clave compartida** | Sin trazabilidad individual de quién pregunta | Aceptable para el uso actual |

### 12.2 Pendientes

**Contenido y skills**
- [ ] Reempaquetar los `.skill` de **Evaluaciones** y **Planes de mejora** con los pasos de seguimiento.
- [ ] Corregir la GuIA de Planes de mejora: en "Añadir o dar seguimiento a un plan de mejora", el texto de *Cuándo se usa* es el de la sección siguiente.
- [ ] Confirmar el prefijo de las rutas nuevas (`Evaluaciones → …` vs. `Admin → Evaluaciones → …`).
- [ ] Mejorar `Indicadores/crear-indicadores.docx` (🟡): estilos Título 1 y 2 y borrar los textos de ejemplo.
- [ ] Llenar el módulo **General** (hoy tiene un solo documento).
- [ ] Verificar los módulos **Proyectos** y **Mecanismos de integración** con pruebas y correos (`to-do`).
- [ ] Meter el árbol de Admin en la skill general (`to-do`).
- [ ] Documentar las categorías **General** y **Riesgos** de Almera.
- [ ] Integrar los apuntes sueltos (`pulir.txt`, `add.txt`, `steps.txt`) en sus GuIA.
- [ ] Presentaciones: probar PDF desde HTML; tamaño de personajes en PPTX.

**Asistente y operación**
- [ ] Validar la calidad de las respuestas con preguntas reales del área por módulo (piloto).
- [ ] Registrar las preguntas que el asistente no pudo responder, para saber qué documentar.
- [ ] Decidir el modelo definitivo (gratis vs. de pago con `deny`).
- [ ] Dar acceso a un segundo administrador en Render, GitHub y OpenRouter.
- [ ] Pruebas automatizadas del ETL, del enrutador y de los informes; correrlas antes de desplegar.
- [ ] Opcional: bajar `ETL_INTERVAL_SECONDS` a 60 s.

**Documentación desactualizada**
- [ ] `README.md` raíz y `sabia.MD` todavía describen SABIA como sitio 100 % estático, sin servidor.
- [ ] `docs/README.md`, el corte 05 y `docs/06-soporte-tecnico.md` (§9 y partes de §3–§5) todavía hablan del asistente como "pendiente de publicar en el servidor del área". Este documento refleja el estado real.
- [ ] `almera/README.md` no lista Mapa de procesos ni Modelos de gestión.

### 12.3 Ideas a futuro (`to-do`)

- Skills de automatización para **ChatGPT Pro**.
- CLI con modelo local (Qwen + LM Studio).
- **RAG para la DEP**: puede reutilizar casi todo `rag/` cambiando `sources.json`, el repo de conocimiento y el prompt.

---

## 13. Tareas frecuentes (guía rápida)

| Quiero… | Hago… | Detalle |
|---|---|---|
| Corregir un paso de Almera | Editar la GuIA `.md`, la guía web y el `.skill`; push | [06 §6.1](06-soporte-tecnico.md) |
| Que el asistente sepa algo nuevo (área) | Aportar por el chat o subir al repo `sabia-conocimiento` | §8.4 |
| Agregar una guía curada | Crear `.md` + `sources.json` + push | §8.4 |
| Agregar un módulo | `sources.json` + push | [06 §6.3](06-soporte-tecnico.md) |
| Que el enrutador acierte más | Títulos descriptivos, `description` del módulo, `STOPWORDS` | [06 §6.4](06-soporte-tecnico.md) |
| Cambiar de modelo | `OPENROUTER_MODEL` en `render.yaml` o Render | §8.4 |
| Rotar una clave o token | Render → *Environment* | §8.6 |
| Reprocesar todos los aportes | Subir `ETL_VERSION` en `etl.py` y push | §6.7 |
| Publicar una carpeta nueva del sitio | Agregarla a `SITE_DIRS` en `main.py` | [06 §6.7](06-soporte-tecnico.md) |
| Ajustar un informe a un export nuevo | `REQUIRED_COLS` / `resolveColumns()` | [02 §6](02-informes.md) |
| Empaquetar una skill | Zip con la carpeta raíz de la skill | [01 §0](01-skills.md) |
| Generar el PDF de un doc | `node docs/generar-pdf.js docs/<doc>.md <salida>.pdf` | [06 §6.12](06-soporte-tecnico.md) |
| Diagnosticar un error | Buscar el síntoma | [06 §5](06-soporte-tecnico.md) y §8.8 |

**Problemas específicos de la nube:**

| Síntoma | Causa | Solución |
|---|---|---|
| La primera visita tarda ~1 min | El servicio estaba dormido | Normal en el plan gratis |
| Recién despierto no conoce un documento aportado | El primer ciclo del ETL aún no termina | Esperar unos segundos |
| "No se pudo guardar … en el almacén de SABIA" | Token vencido o sin permiso, conflicto o GitHub caído | Revisar *Logs*; renovar el token |
| Logs: `ETL falló` con 401 de `api.github.com` | Token vencido o revocado | Renovar `GITHUB_TOKEN` |
| Logs: `ETL falló` con 404 | `GITHUB_REPO` o `GITHUB_BRANCH` mal escritos | Corregir en *Environment* |
| Todos tuvieron que volver a entrar | Cambió `SITE_PASSWORD` | Normal |
| "Demasiados intentos" en el login | 30 fallos en 10 min (de cualquiera) | Esperar unos minutos |
| Un archivo subido por github.com no aparece | Está suelto en la raíz o en una carpeta que no es un módulo | Moverlo a la carpeta del módulo |
| El servicio no arranca tras un push | Error en el código o en `sources.json` | Ver *Logs* de Render; Render mantiene la versión anterior |
| "OpenRouter respondió 429" | Límite del modelo gratis | Esperar o cambiar a un modelo de pago |

---

## 14. Mapa del repositorio

```
almera-docs/
├── index.html                    Portada de SABIA
├── render.yaml                   Blueprint de Render (servicio "sabia")
├── package.json                  npm start → rag\iniciar.ps1
├── iniciar.bat                   Doble clic → rag\iniciar.ps1
├── README.md, sabia.MD           Presentación del proyecto (desactualizados: sin servidor)
├── routes.md                     Rutas del sitio y menú compartido
├── to-do                         Backlog informal
├── styles/                       Estilos de la portada
├── docs/                         Documentación de traspaso
│   ├── README.md                 Índice
│   ├── 01-skills.md … 03-almera.md
│   ├── 04-corte-2026-10-28.md, 05-corte-2026-11-03.md   Cortes históricos
│   ├── 06-soporte-tecnico.md
│   ├── 07-documentacion-completa.md   ← este documento
│   └── generar-pdf.js            Markdown → PDF con la marca de SABIA
├── almera/                       Documentación de Almera
│   ├── index.html                Landing de módulos
│   ├── assets/                   nav.js (menú), almera-structure.md (árbol de Admin), estilos
│   ├── modulo-documentos/        gestion-documentos, mapa-procesos, mecanismos-integracion, modelos-gestion
│   ├── modulo-evaluaciones/      evaluaciones, indicadores, planes-de-mejora
│   ├── modulo-proyectos/
│   │   └── (cada módulo)         index.html · styles/ · AI/<guía>.md · AI/almera-<módulo>.skill
│   ├── informe-documentos/       Dashboard del export de Almera
│   ├── control-documentos-sgc/   Dashboard del listado maestro del SGC
│   ├── codigos-estructura-organizacional/
│   ├── almera-IA/                Cómo instalar las skills
│   └── design/                   Mockups (no publicados en el menú)
├── calidad-ai-agents/            Skills de entregables
│   ├── index.html, entregables/  Páginas web
│   ├── presentaciones-institucionales/   SKILL.md, references/, assets/ (pptx_kit.py, consolidar.py…), .skill
│   ├── diagramas-flujo/          Fuentes DESACTUALIZADAS + diagramas-flujo-v3.skill vigente
│   └── SEGURIDAD.md              Uso de las skills con datos reales
└── rag/                          Servidor SABIA
    ├── app/                      main, config, knowledge, etl, almacen, llm, prompts
    ├── static/                   Chat, login y vendor/ (marked, DOMPurify)
    ├── conocimiento/             Guía "SABIA (cómo alimentarlo)"
    ├── carpeta-compartida/       Modelo de carpeta + plantilla y prompt de las descargas
    ├── sources.json              Catálogo de módulos
    ├── requirements.txt, .env.example, iniciar.ps1, README.md
    ├── generado/                 Salida del ETL (no está en Git)
    └── nube/                     Copia de sabia-conocimiento (no está en Git)
```

---

## 15. Historia del proyecto

| Fecha | Hito |
|---|---|
| 10 jul 2026 | Primer commit: documentación de Planes de mejora |
| jul 2026 | Mecanismos de integración, Evaluaciones, Documentos; primeras skills `.skill`; guía Almera + IA |
| ago 2026 | Informe de documentos (KPIs, filtros), Proyectos, rediseño completo de la interfaz, estilos por módulo |
| sep 2026 | Landing de Agentes de IA, skills de presentaciones institucionales (con modo consolidar) y diagramas de flujo, guía de seguridad, asignación masiva de privilegios en Indicadores |
| 5–7 oct 2026 | Diagramas de flujo v2.5/v3, documento de presentación de SABIA, carpeta `docs/` |
| 14–16 oct 2026 | Filtros y gráficos del control SGC, KPIs personalizados, menú compartido `nav.js` |
| 28 oct 2026 | **Asistente RAG-lite** con OpenRouter, menú 1c en todo el sitio, **ETL de carpeta compartida**, `routes.md`, corte 04 |
| 3 nov 2026 | `npm start` / `iniciar.bat`, botón "Aportar un documento", módulos General y SABIA, enrutador con conjugaciones, `no-cache`, campos DEP, corte 05, soporte técnico, generador de PDF |
| 4 nov 2026 | Códigos consecutivos automáticos (Documentos), **despliegue en Render con GitHub como almacén**, **login con sesión de 30 días**, primeros documentos en `sabia-conocimiento` |

El desarrollo se apoyó en Claude: Claude Code para el código y la documentación, y Claude Design para los mockups.

---

## 16. Glosario

| Término | Significado |
|---|---|
| **Almera (SGI)** | Sistema de gestión institucional sobre el que opera el Sistema de Gestión de Calidad de Capital Salud |
| **SGC** | Sistema de Gestión de Calidad |
| **DEP** | Área cuyo profesional asignado figura en el listado maestro del SGC (columna "Nombre profesional asignado de la DEP") |
| **GuIA** | Documento `.md` de referencia de cada módulo; fuente de verdad del contenido |
| **Skill (`.skill`)** | Paquete zip que Claude carga cuando el pedido lo requiere |
| **RAG** | *Retrieval-Augmented Generation*: buscar la información relevante y dársela al modelo con la pregunta |
| **RAG-lite** | Variante de SABIA: elige el módulo y le pasa su documentación completa, sin fragmentos ni embeddings |
| **BM25** | Algoritmo clásico de búsqueda por palabras clave |
| **Stemming / recorte de terminaciones** | Quitar la terminación de una palabra para que conjugaciones y plurales cuenten igual |
| **ETL** | *Extract, Transform, Load*: extraer el contenido, limpiarlo y cargarlo donde se usa |
| **Semáforo** | 🟢 publicado · 🟡 publicado con advertencias · 🔴 no publicado |
| **Aporte** | Documento que el área sube a SABIA (por el chat o al repo `sabia-conocimiento`) |
| **Guía curada** | `.md` mantenido por el equipo técnico en `almera-docs` y listado en `sources.json` |
| **OpenRouter** | Servicio que da acceso a muchos modelos de IA con una sola llave |
| **SSE / streaming** | La respuesta llega por partes mientras se genera |
| **Render** | Plataforma de hosting donde corre el servidor de SABIA |
| **Blueprint** | Archivo `render.yaml` que describe el servicio para que Render lo cree y lo despliegue |
| **Token fine-grained** | Credencial de GitHub limitada a repositorios y permisos concretos |
| **Arranque en frío** | El minuto que tarda Render en despertar un servicio gratis dormido |
| **HMAC** | Firma criptográfica con una clave secreta; aquí, la de la cookie de sesión |
