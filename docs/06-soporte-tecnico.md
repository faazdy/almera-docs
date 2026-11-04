# 6. Soporte técnico de SABIA

Guía para quien tenga que **arrancar, revisar, arreglar o mantener** SABIA sin haber participado en su desarrollo. Está ordenada por tareas: busca el síntoma en la §5 o la tarea en la §6.

> **SABIA en producción corre en Render** (nube, plan gratis) y los documentos aportados se guardan en el repo privado `sabia-conocimiento` de GitHub. Despliegue, claves, token y tareas del día a día: [`rag/README.md` → "Desplegar en la nube"](../rag/README.md#desplegar-en-la-nube-render--github-gratis). Esta guía cubre sobre todo cómo correrlo en un equipo, que sigue sirviendo para desarrollo y pruebas. En la nube, los logs están en Render → servicio `sabia` → *Logs*.

Para entender **qué es** cada parte y **por qué** está hecha así, lee primero el [corte del proyecto](05-corte-2026-11-03.md). El detalle de cada pieza está en [01-skills](01-skills.md), [02-informes](02-informes.md), [03-almera](03-almera.md) y [`rag/README.md`](../rag/README.md).

---

## 1. Mapa rápido: qué hay y dónde se arregla

| Si falla… | La pieza es… | Vive en… | Necesita servidor |
|---|---|---|---|
| La portada, una guía de Almera o el menú | Sitio estático (HTML/CSS/JS plano) | `index.html`, `styles/`, `almera/`, `calidad-ai-agents/`, `almera/assets/nav.js` | No |
| Un informe (dashboard) | JavaScript en el navegador + SheetJS + Chart.js | `almera/informe-documentos/`, `almera/control-documentos-sgc/` | No |
| El chat "Pregúntale a SABIA" | Servidor Python (FastAPI) + OpenRouter | `rag/app/`, `rag/static/`, `rag/.env` | Sí |
| "Aportar un documento" o la carpeta compartida | ETL dentro del mismo servidor | `rag/app/etl.py`, `KNOWLEDGE_DIR`, `rag/generado/` | Sí |
| Una respuesta del asistente es incorrecta | Contenido (GuIA `.md` o documento de la carpeta) | `almera/**/AI/*.md`, carpeta compartida | — |
| Una skill de Claude | Paquete `.skill` (zip) | `almera/**/AI/*.skill`, `calidad-ai-agents/` | No |

**Regla de oro:** si el error es de **contenido** (un paso mal, una ruta que cambió), se corrige el `.md` y no el código. Si es de **comportamiento** (no arranca, no responde, filtros vacíos), sigue esta guía.

---

## 2. Requisitos

| Qué | Versión | Para qué |
|---|---|---|
| Windows 10/11 | — | Los lanzadores son de Windows (PowerShell / `.bat`) |
| Python | 3.13 (probado con 3.13.15) | Servidor del asistente. Debe estar en el `PATH` como `python` |
| Acceso a internet hacia `openrouter.ai` | HTTPS 443 | Llamadas al modelo |
| Llave de OpenRouter | — | En `rag/.env`; se crea en <https://openrouter.ai/keys> |
| Node.js | Opcional (probado con 24) | Solo para `npm start`; el servidor no lo usa |
| Navegador moderno | Edge o Chrome | Sitio, informes y chat |

Dependencias de Python (fijadas en `rag/requirements.txt`): `fastapi`, `uvicorn`, `httpx`, `python-dotenv`, `truststore` y `markitdown[docx,pdf,pptx,xlsx]`.

---

## 3. Arrancar, detener y reinstalar

### 3.1 Arrancar

Desde la raíz del repo, cualquiera de las tres (todas ejecutan `rag\iniciar.ps1`):

| Forma | Comando |
|---|---|
| Doble clic | `iniciar.bat` |
| npm | `npm start` |
| PowerShell | `cd rag; .\iniciar.ps1` |

Abre <http://127.0.0.1:8800/> (portada) y <http://127.0.0.1:8800/asistente/> (chat).

**Qué hace `iniciar.ps1`:**

1. Si no existe `rag\.venv`, lo crea e instala `requirements.txt`.
2. Si no existe `rag\.env`, lo copia de `.env.example`, avisa y **se detiene**: hay que poner la llave y volver a arrancar.
3. Ejecuta `.venv\Scripts\python.exe -m app.main`.

⚠️ **Solo instala dependencias la primera vez.** Si la instalación falló a medias o si `requirements.txt` cambió, ver §6.9.

**Arranque correcto:** la consola muestra algo como

```
SABIA en http://127.0.0.1:8800/  ·  asistente en /asistente/
Carpeta de conocimiento: …\rag\carpeta-compartida (revisión cada 300s)
INFO:     Uvicorn running on http://127.0.0.1:8800 (Press CTRL+C to quit)
INFO:     sabia: ETL: {'verde': 1, 'amarillo': 1, 'rojo': 0} · base sin cambios
```

### 3.2 Detener

`Ctrl+C` en la consola del servidor, o cerrar la ventana.

### 3.3 Cuándo hay que reiniciar

El servidor lee la configuración y el catálogo **solo al arrancar**. Reinicia después de cambiar:

- `rag/.env` (llave, modelo, puerto, carpeta…)
- `rag/sources.json` (módulos, guías curadas)
- Una GuIA `.md` del repo que use el asistente
- Cualquier archivo de `rag/app/`

**No** hace falta reiniciar para: documentos de la carpeta compartida (los toma el ETL), páginas del sitio, informes ni archivos de `rag/static/` (basta recargar el navegador).

### 3.4 Instalación manual (si `iniciar.ps1` no sirve)

```powershell
cd rag
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env      # y poner OPENROUTER_API_KEY
.venv\Scripts\python -m app.main
```

---

## 4. Revisar que todo está bien (prueba de humo)

Hazla después de arrancar en un equipo nuevo, después de cualquier cambio de código y cuando alguien reporte "no funciona".

| # | Qué revisar | Cómo | Resultado esperado |
|---|---|---|---|
| 1 | Servidor arriba | Abrir <http://127.0.0.1:8800/> | Portada de SABIA |
| 2 | API | Abrir <http://127.0.0.1:8800/api/modules> | JSON con `model`, 10 módulos y `"upload": true` |
| 3 | Llave y modelo | En el chat, preguntar "¿cómo creo un comité?" | Respuesta con pasos y línea "Fuente:"; arriba "Mecanismos de integración" |
| 4 | Enrutador | Preguntar "¿cómo te alimento?" | Responde con la guía de "SABIA (cómo alimentarlo)" |
| 5 | ETL | Abrir `ESTADO SABIA.txt` en la carpeta compartida | Hora de "Actualizado" de hace menos de `ETL_INTERVAL_SECONDS` |
| 6 | Subida | Botón "Aportar un documento" → subir un `.docx` de prueba a un módulo | Semáforo en pantalla; el archivo aparece en la subcarpeta. **Bórralo después** |
| 7 | Seguridad | Abrir <http://127.0.0.1:8800/rag/.env> | **404** |
| 8 | Informes | Abrir cada informe y cargar su Excel | KPIs, gráficos y filtros con valores |

---

## 5. Diagnóstico por síntoma

### 5.1 El servidor no arranca

| Síntoma en la consola | Causa | Solución |
|---|---|---|
| `python` no se reconoce, o se abre la Microsoft Store | Python no instalado o no está en el `PATH` | Instalar Python 3.13 marcando "Add python.exe to PATH" |
| "Se creo rag\.env a partir de .env.example…" | Primer arranque | Poner `OPENROUTER_API_KEY` en `rag\.env` y volver a arrancar |
| `ModuleNotFoundError: No module named 'fastapi'` (u otro) | La instalación de dependencias falló o cambió `requirements.txt` | §6.9 |
| Error de certificados (`SSL`, `CERTIFICATE_VERIFY_FAILED`) al instalar | La red inspecciona TLS y `pip` no confía en el certificado | Pedir a TI el proxy/certificado corporativo, o instalar desde una red sin inspección. **No** desactivar la verificación de forma permanente |
| `FileNotFoundError: sources.json apunta a un archivo inexistente: …` | Una ruta de `rag/sources.json` está mal o el archivo se movió | Corregir la ruta. Un módulo sin guía curada lleva `"files": []` |
| `[Errno 10048] error while attempting to bind` | El puerto 8800 ya está en uso (otro SABIA abierto) | Cerrar la otra ventana, o cambiar `PORT` en `rag\.env` |
| `json.decoder.JSONDecodeError` al arrancar | `sources.json` quedó con una coma o comilla de más | Validar el JSON (por ejemplo, abrirlo en VS Code) |
| La política de PowerShell bloquea `iniciar.ps1` | Se ejecutó `.\iniciar.ps1` directo en un equipo restringido | Usar `iniciar.bat` o `npm start`, que pasan `-ExecutionPolicy Bypass` |

### 5.2 El chat no responde o muestra un error

El mensaje de error aparece en la burbuja de la respuesta. Los más comunes:

| Mensaje | Causa | Solución |
|---|---|---|
| "Falta OPENROUTER_API_KEY en rag/.env" | Llave vacía | Poner la llave y reiniciar |
| "OpenRouter respondió 401: …" | Llave inválida o revocada | Crear una llave nueva en OpenRouter (§6.6) |
| "OpenRouter respondió 402: …" | Sin créditos o se alcanzó el límite de gasto de la llave | Recargar créditos o subir el límite en OpenRouter |
| "OpenRouter respondió 404: …" o "… model …" | `OPENROUTER_MODEL` no existe o fue retirado | Elegir un id vigente en <https://openrouter.ai/models> (§6.5) |
| "OpenRouter respondió 429: …" | Demasiadas peticiones o proveedor saturado | Esperar y reintentar. Si se repite, revisar en OpenRouter |
| Error 404 que menciona proveedores o *data policy* | Con `OPENROUTER_DENY_DATA_COLLECTION=true` ningún proveedor del modelo cumple la política | Elegir otro modelo. No desactivar la política sin aprobación |
| "No se pudo contactar el modelo (ConnectError) …" | Sin internet, proxy o firewall bloqueando `openrouter.ai` | Probar <https://openrouter.ai> en el navegador del mismo equipo; si no abre, es la red (TI) |
| "No se pudo contactar el modelo (… Timeout) …" | El modelo tardó más de 120 s o la red está lenta | Reintentar. Si es frecuente, probar otro modelo |
| … `CERTIFICATE_VERIFY_FAILED` … | Certificado corporativo no instalado en Windows | TI debe instalar el certificado raíz en el almacén de Windows. `truststore` lo toma de ahí |
| "La pregunta supera 4000 caracteres" | Pregunta muy larga | Acortarla. El límite es `MAX_QUESTION_CHARS` en `config.py` |
| El chat no carga la lista de módulos | El servidor está apagado o se abrió el HTML directo (sin servidor) | Entrar por `http://127.0.0.1:8800/asistente/` con el servidor arriba |

### 5.3 El asistente responde mal

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| "Eso no está en la documentación de SABIA" y sí está | El enrutador eligió otro módulo | Mirar el módulo que muestra la respuesta. Fijar el módulo en el selector y repetir: si así responde bien, el problema es el enrutamiento (§6.4) |
| Responde con un módulo equivocado | La pregunta usa palabras que pesan más en otra guía | Mejorar los títulos `##` de la guía correcta o la `description` del módulo en `sources.json` (§6.4) |
| Da pasos que ya no son así en Almera | La GuIA está desactualizada | Corregir el `.md` (§6.1) |
| No conoce un documento recién subido | El ETL no lo publicó o aún no pasa el ciclo | §5.4 |
| Inventa o mezcla módulos | Pregunta ambigua que trajo 2 módulos | Pedir al usuario que fije el módulo. Si es frecuente, reportar con la pregunta exacta |

### 5.4 La carpeta compartida o "Aportar un documento"

| Síntoma | Causa | Solución |
|---|---|---|
| Un documento no aparece en las respuestas | Está en 🔴, o no ha pasado el ciclo del ETL | Leer `ESTADO SABIA.txt`: dice el motivo y qué corregir. Esperar `ETL_INTERVAL_SECONDS` o reiniciar |
| "La carpeta X no corresponde a ningún módulo" | Nombre de carpeta mal escrito | Renombrar la carpeta a uno de los nombres válidos que lista el reporte. No importan tildes, mayúsculas ni guiones |
| "Está suelto en la carpeta principal" | El archivo está en la raíz y no en una subcarpeta | Moverlo a la carpeta del módulo |
| Log: "ETL: no encuentro la carpeta …" | `KNOWLEDGE_DIR` mal escrito o la red no está disponible | Revisar la ruta en `rag\.env` (**sin comillas**: `KNOWLEDGE_DIR=\\servidor\Calidad\SABIA`). Mientras tanto el asistente usa lo último publicado |
| No aparece el botón "Aportar un documento" | `KNOWLEDGE_DIR` vacío | Configurarlo y reiniciar |
| Subida: "La carpeta compartida no está disponible en este momento" (503) | Igual que el anterior, o la red cayó | Revisar la ruta y el acceso del equipo del servidor a la carpeta |
| Subida: "No se pudo guardar … Si alguien lo tiene abierto en Office…" (423) | El archivo con ese nombre está abierto en Word/Excel en otro equipo | Pedir que lo cierren y reintentar |
| Subida: "Ya existe … en …" (409) | Ya hay un archivo con ese nombre | El chat ofrece reemplazarlo; confirmar solo si es una versión nueva |
| Subida: "El archivo pesa más de 20 MB" (413) | Archivo grande (imágenes pesadas) | Comprimir imágenes o partir el documento; o subir `MAX_UPLOAD_MB` |
| Subida: "Formato no soportado" o "Es un Word antiguo (.doc)…" (400) | `.doc`, `.ppt`, `.xls` u otro formato | Guardar como `.docx`, `.pptx` o `.xlsx` |
| `ESTADO SABIA.txt` no se actualiza | El servidor no tiene permiso de escritura en la carpeta | Dar escritura al usuario con el que corre el servidor. El ETL sigue publicando aunque no pueda escribir el reporte |

### 5.5 El sitio o los informes

| Síntoma | Causa | Solución |
|---|---|---|
| Tras una actualización, filtros vacíos, botones que no hacen nada o errores en consola | El navegador mezcló un HTML nuevo con un JS viejo (caché) | `Ctrl+F5`. Con el servidor SABIA no debería pasar (manda `no-cache`); si el sitio se sirve desde otro servidor web, configurar allí `Cache-Control: no-cache` |
| El informe dice que el archivo no es el correcto | Se cargó otro Excel, o Almera / el SGC cambió los nombres de las columnas | Revisar el mensaje: lista las columnas que faltan. Si cambió el export, ver §6.8 |
| Un KPI personalizado da 0 | El valor no existe en ese campo, o se eligió el campo equivocado | Usar las sugerencias del campo *Valor* (salen del Excel cargado). En el export de Almera, "Formato" está en **Clase**, no en **Tipo** |
| Los KPIs personalizados desaparecieron | Se guardan en el navegador (`localStorage`): otro equipo, otro navegador o se borraron los datos de navegación | Importar el `.json` de respaldo desde el panel. Recomendar exportarlo después de crear indicadores |
| El menú no aparece en una página | La página no carga `almera/assets/nav.js` o la ruta relativa está mal | Revisar el `<script src=".../assets/nav.js" data-base="...">` de la página ([`routes.md`](../routes.md)). Los dos informes no tienen menú por diseño |
| Una carpeta nueva del sitio da 404 con el servidor | No está en la lista de carpetas publicadas | Agregarla a `SITE_DIRS` en `rag/app/main.py` (§6.7) |

---

## 6. Tareas de mantenimiento

### 6.1 Corregir o ampliar la guía de un módulo de Almera

Cada módulo tiene **tres copias** que se sincronizan a mano:

1. **GuIA** `almera/<grupo>/<módulo>/AI/*.md`: la que lee el asistente. Usa títulos `##`/`###` descriptivos; el enrutador decide por ellos.
2. **Guía web** `almera/<grupo>/<módulo>/index.html`: agregar la sección, su entrada en el índice lateral (`m-toc`) y, si aplica, en preguntas frecuentes (`faq-grid`).
3. **Skill** `AI/*.skill`: reempaquetar con la GuIA nueva ([01-skills.md §0](01-skills.md)).

Después: **reiniciar el servidor** y probar una pregunta del tema nuevo en el chat.

### 6.2 Agregar conocimiento sin tocar el repo

Lo hace el área: guardar el documento en la subcarpeta del módulo de la carpeta compartida o usar el botón "Aportar un documento". La guía para usuarios está en `rag/conocimiento/alimentar-sabia.md` (el propio asistente la explica si se le pregunta "¿cómo te alimento?").

- **Actualizar:** guardar encima con el mismo nombre.
- **Eliminar:** borrar el archivo de la carpeta compartida. En el siguiente ciclo el ETL retira su `.md` de `rag/generado/` y lo saca del asistente.

### 6.3 Agregar un módulo nuevo al asistente

1. En `rag/sources.json`, agregar `{"id": "…", "name": "…", "description": "…", "files": [...]}`.
   - `description` con las palabras con que la gente pregunta: pesa en el enrutamiento.
   - `files` puede ser `[]` si el módulo solo se alimenta desde la carpeta compartida.
   - `"uploads": false` si no debe aceptar documentos del área.
2. Si acepta documentos, crear su subcarpeta en la carpeta compartida (el botón la crea solo si falta).
3. Reiniciar y probar con 3–5 preguntas típicas del módulo.

### 6.4 El enrutador se equivoca

Lo más efectivo, en orden:

1. **Títulos de la guía:** que las secciones digan lo que la gente pregunta (`## Crear un comité`, no `## Paso 3`).
2. **`description` en `sources.json`:** sumar sinónimos y verbos ("crear, subir, aprobar, dar de baja…").
3. **Palabras vacías** (`STOPWORDS` en `rag/app/knowledge.py`): palabras que aparecen en todas las guías y confunden (por ejemplo "almera", "sistema").
4. **Recorte de terminaciones** (`SUFFIXES` / `stem()`): solo si el problema son conjugaciones. Cualquier cambio aquí afecta a todas las preguntas: medir antes y después enrutando los títulos de todas las guías y revisando que cada uno caiga en su módulo.

El umbral para traer un segundo módulo (60 % del puntaje del primero) está en `KnowledgeBase.route()`.

### 6.5 Cambiar de modelo

1. Elegir el id en <https://openrouter.ai/models> (por ejemplo `anthropic/claude-haiku-5.5`).
2. `OPENROUTER_MODEL=…` en `rag\.env` y reiniciar.
3. Repetir la prueba de humo (§4, pasos 3 y 4) y unas preguntas reales: cada modelo sigue las reglas del prompt de forma distinta.

### 6.6 Cambiar o rotar la llave de OpenRouter

1. En <https://openrouter.ai/keys>, crear una llave nueva con **límite de gasto**.
2. Ponerla en `rag\.env` y reiniciar.
3. Revocar la llave anterior.

Si una llave se filtró (correo, chat, captura, Git): revocarla **de inmediato** y revisar el consumo en OpenRouter.

### 6.7 Publicar una carpeta nueva del sitio

El servidor solo publica `index.html`, `styles/`, `almera/` y `calidad-ai-agents/`. Para una carpeta nueva de primer nivel, agregarla a `SITE_DIRS` en `rag/app/main.py`, reiniciar y comprobar que `/rag/.env` sigue dando 404. **Nunca** publicar la raíz del repo.

### 6.8 El export de Almera o el listado del SGC cambió de columnas

- **Informe de Almera:** ajustar `REQUIRED_COLS` y las claves de `processRow` / `buildExportRows` en `almera/informe-documentos/main.js`.
- **Informe del SGC:** ajustar `resolveColumns()` en `almera/control-documentos-sgc/main.js` (busca columnas por nombre normalizado, prefijo o términos).
- Probar con el Excel real: KPIs, filtros, tabla y exportación. Detalle en [02-informes.md §6](02-informes.md).

### 6.9 Reinstalar o actualizar dependencias de Python

`iniciar.ps1` solo instala la primera vez. Para reparar o actualizar:

```powershell
cd rag
.venv\Scripts\python -m pip install -r requirements.txt
```

Si el entorno está dañado, borrar la carpeta `rag\.venv` y volver a arrancar con `iniciar.bat`: se recrea solo.

Para subir de versión una dependencia: cambiarla en `requirements.txt`, instalar como arriba y repetir la prueba de humo completa. MarkItDown cambia la conversión de documentos: tras actualizarlo, subir `ETL_VERSION` (§6.10).

### 6.10 Forzar que el ETL reprocese todo

El ETL solo reprocesa lo que cambió (fecha y tamaño). Para reprocesar todo, por ejemplo tras cambiar la limpieza o el semáforo en `etl.py`:

- **Lo correcto:** subir `ETL_VERSION` en `rag/app/etl.py` y reiniciar.
- **Rápido, en un equipo de pruebas:** con el servidor detenido, borrar `rag\generado\` y arrancar.

Probar el ETL sin el servidor: `cd rag; .venv\Scripts\python -m app.etl`. Hazlo **con el servidor detenido**: los dos escribirían el mismo `manifest.json`.

### 6.11 Cambiar el texto de la plantilla de Word

`Plantilla guía SABIA.docx` trae textos de ejemplo que el ETL borra si alguien los deja. Si cambias esos textos en la plantilla, actualiza `TEMPLATE_LINES` en `rag/app/etl.py` y sube `ETL_VERSION`. Las descargas del botón salen de la copia del repo (`rag/carpeta-compartida/`), no de la carpeta de red.

### 6.12 Generar el PDF de un documento de `docs/`

```powershell
node docs/generar-pdf.js docs/05-corte-2026-11-03.md docs/SABIA-corte-2026-11-03.pdf
node docs/generar-pdf.js docs/06-soporte-tecnico.md docs/SABIA-soporte-tecnico.pdf
```

Convierte el Markdown con el mismo `marked` del chat, incrusta las fuentes de SABIA y lo imprime con Edge o Chrome en modo *headless*. Sin el segundo argumento, deja el PDF al lado del `.md`. Requiere Node.js. Detalle en el encabezado del script.

Para un corte nuevo: copiar el último `0X-corte-….md`, actualizarlo y generar `SABIA-corte-AAAA-MM-DD.pdf`. Los cortes anteriores se conservan como histórico.

---

## 7. Referencia técnica

### 7.1 Endpoints del servidor

| Método y ruta | Qué hace | Respuesta |
|---|---|---|
| `GET /` | Portada | `index.html` |
| `GET /almera/…`, `/styles/…`, `/calidad-ai-agents/…` | Sitio estático | Archivos del repo |
| `GET /asistente/` | Chat | `rag/static/index.html` |
| `GET /api/modules` | Catálogo para el chat | `{model, modules[], upload, max_upload_mb}` |
| `POST /api/chat` | Pregunta | Cuerpo `{messages: [{role, content}], module}` → SSE: `meta`, `delta`*, `error`?, `done` |
| `POST /api/upload?module=…&filename=…&replace=…` | Subir un documento (cuerpo = bytes del archivo) | `{file, module, status, notes}` o error 400/409/413/423/503 |
| `GET /api/descargas/plantilla` · `/prompt` | Plantilla de Word y prompt de limpieza | Archivo |

### 7.2 Archivos del servidor

| Archivo | Responsabilidad | Tocarlo cuando… |
|---|---|---|
| `rag/app/config.py` | Lee `rag/.env`; límites fijos (4000 caracteres, 8 mensajes) | Hay una variable nueva o cambia un límite |
| `rag/app/main.py` | Rutas, validación, subidas, ciclo del ETL, `SITE_DIRS`, cabecera `no-cache` | Endpoint nuevo o carpeta nueva del sitio |
| `rag/app/knowledge.py` | Carga guías, parte por secciones, BM25, enrutamiento, contexto | El enrutamiento se equivoca |
| `rag/app/prompts.py` | Reglas del asistente | Cambia cómo debe responder |
| `rag/app/llm.py` | Cliente de OpenRouter (streaming, SSL, errores) | Cambia el proveedor o sus parámetros |
| `rag/app/etl.py` | Extraer, limpiar, semáforo, publicar, `ESTADO SABIA.txt` | Cambian formatos, limpieza o reglas del semáforo |
| `rag/sources.json` | Catálogo de módulos | Módulo o guía nueva |
| `rag/static/app.js` | Chat y subida en el navegador | Cambia la interfaz |

### 7.3 Qué no está en Git y hay que respaldar

| Qué | Dónde | Notas |
|---|---|---|
| Llave y configuración | `rag/.env` | Guardar la llave en un gestor de contraseñas, no en correos ni documentos |
| Documentos del área | Carpeta compartida (`KNOWLEDGE_DIR`) | Es la fuente; el respaldo depende de la carpeta de red (TI) |
| Salida del ETL | `rag/generado/` | **No** necesita respaldo: se regenera desde la carpeta compartida |
| Entorno de Python | `rag/.venv/` | Se recrea con `iniciar.bat` |
| KPIs personalizados | `localStorage` de cada navegador | Exportar a `.json` desde el panel |
| Excels de los informes | Equipo de cada usuario | Pueden traer datos de personas: **no** subirlos al repo |

### 7.4 Logs

El servidor escribe en la consola donde se arrancó; no hay archivo de log. Mensajes útiles:

| Mensaje | Significa |
|---|---|
| `sabia: ETL: {'verde': N, …} · base actualizada` | El ETL publicó cambios y el asistente ya los usa |
| `sabia: ETL: … · base sin cambios` | Ciclo normal sin novedades |
| `sabia: ETL: no encuentro la carpeta …` | `KNOWLEDGE_DIR` inaccesible (§5.4) |
| `sabia: ETL falló` + traza | Error inesperado del ETL; se reintenta en el próximo ciclo. Copiar la traza al reportar |
| `sabia: Subida: <archivo> → <semáforo>` | Alguien subió un documento por el chat |
| `POST /api/chat … 200` | Pregunta atendida (el error de OpenRouter, si lo hubo, viaja dentro del stream y no cambia el 200) |

Para guardar el log en un archivo: `.venv\Scripts\python -m app.main *> sabia.log` desde `rag/`.

---

## 8. Cómo reportar un problema

Para que alguien pueda reproducirlo, incluir:

1. **Qué se hizo** (la pregunta exacta, el archivo subido o el informe y el Excel usado).
2. **Qué pasó y qué se esperaba.** Captura de pantalla si es visual.
3. **El mensaje de error** de la burbuja del chat o de la consola del servidor (la traza completa si la hay).
4. **El módulo** que mostró la respuesta, si es del asistente.
5. Para la carpeta compartida: el contenido de `ESTADO SABIA.txt`.
6. **Nunca** incluir la llave de OpenRouter ni datos personales.

| Tipo de problema | A quién |
|---|---|
| Red, proxy, certificados, permisos de la carpeta, servidor del área | TI |
| Llave, créditos, modelos | Administrador de la cuenta de OpenRouter |
| Un procedimiento de Almera no es como dice la guía | Soporte de Almera + quien mantiene la GuIA |
| Código de SABIA (servidor, ETL, informes) | Quien mantiene el repositorio `faazdy/almera-docs` |
