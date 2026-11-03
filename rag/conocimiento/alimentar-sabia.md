# SABIA — Cómo alimentar al asistente

Esta guía explica cómo enseñarle cosas nuevas a SABIA (el asistente "Pregúntale a SABIA"): cómo agregar información nueva, cómo actualizar la que ya tiene y cómo quitar la que ya no sirve. No hace falta saber código ni instalar nada.

## De dónde aprende SABIA

SABIA solo responde con lo que está en su base de conocimiento. Esa base tiene dos fuentes:

1. **Documentos que aporta el área de Calidad.** Se suben con el botón **+ Aportar un documento** del chat o se guardan en la **carpeta compartida de SABIA**. Es el camino para cualquier persona.
2. **Guías curadas del equipo técnico.** Son los archivos `.md` del repositorio de SABIA (carpetas `almera/…/AI/`). Solo las cambia el equipo técnico (ver "Para el equipo técnico" al final).

Lo que no esté en ninguna de las dos fuentes, SABIA no lo sabe y responde "Eso no está en la documentación de SABIA".

## Módulos a los que se puede aportar

Cada documento pertenece a un solo módulo. Los módulos (y las carpetas de la carpeta compartida) son:

- Documentos
- Mapa de procesos
- Mecanismos de integración
- Modelos de gestión
- Evaluaciones
- Indicadores
- Planes de mejora
- Proyectos
- General (información de Almera que no pertenece a un solo módulo)

La carpeta debe llamarse exactamente como el módulo. Un archivo en una carpeta con otro nombre o suelto en la carpeta principal **no se publica**.

## Preparar el documento antes de subirlo

1. Descarga la plantilla: en el chat pulsa **+ Aportar un documento** → **↓ Descargar plantilla (.docx)**. También está en la carpeta compartida como **Plantilla guía SABIA.docx**.
2. Escribe un solo tema por documento (por ejemplo, "Crear un comité").
3. Separa cada tarea con los estilos de Word **Título 1**, **Título 2** y **Título 3** (pestaña **Inicio → Estilos**). Poner el texto en negrita no basta: los títulos son los que le permiten a SABIA encontrar la parte exacta que responde cada pregunta.
4. Escribe la ruta del menú (ejemplo: Admin → Calidad → Documentos) y los pasos numerados en el orden real.
5. Borra los textos grises de ejemplo de la plantilla.
6. Si algo no está confirmado con soporte de Almera, márcalo como **[POR CONFIRMAR]**. SABIA avisará que es un tema sin validar.
7. Guarda en un formato válido: Word (.docx), PDF, PowerPoint (.pptx), Excel (.xlsx) o texto (.txt / .md). Máximo 20 MB.

**Notas:**

- No incluyas datos personales, de pacientes ni información confidencial: todo lo que se publica termina en las respuestas del asistente.
- Escribe solo procedimientos del sistema: rutas, pasos, reglas y dudas abiertas.
- Las imágenes y capturas de pantalla no se pueden leer. Si muestran un paso importante, descríbelo con texto.
- Los formatos antiguos (.doc, .ppt, .xls) no se aceptan. Ábrelos y usa **Guardar como** → .docx, .pptx o .xlsx.

## Ordenar una transcripción o un PDF escaneado con IA

SABIA no puede publicar transcripciones de reuniones, PDF escaneados ni documentos sin títulos. Para convertirlos en una guía:

1. Descarga el prompt: en el chat pulsa **+ Aportar un documento** → **¿Es una transcripción o un PDF escaneado? Descarga el prompt para ordenarlo con IA**. También está en la carpeta compartida como **PROMPT para limpiar con IA.txt**.
2. Abre la IA aprobada por la entidad. No uses cuentas personales para información interna.
3. Copia el texto del prompt (entre las líneas "COPIAR DESDE AQUÍ") y pégalo en el chat de la IA.
4. Debajo pega el contenido del documento o adjunta el archivo.
5. Revisa la respuesta: los pasos deben ser los mismos del documento original.
6. Pega la respuesta en el Bloc de notas y guárdala con extensión .txt (ejemplo: "Crear un comité.txt").
7. Súbela como cualquier documento nuevo (ver "Agregar información nueva").

## Agregar información nueva

### Con el botón Aportar un documento (lo más fácil)

1. Abre el chat de SABIA y pulsa **+ Aportar un documento** (barra superior, junto al selector de módulo).
2. En **¿De qué módulo es?** elige el módulo al que pertenece el documento.
3. En **Elige el archivo** selecciona el documento.
4. Pulsa **Publicar**.
5. Espera unos segundos mientras dice "Revisando…". SABIA muestra el resultado con el semáforo (ver "Qué significa el semáforo").
6. Si sale 🔴, corrige lo que dice la nota y vuelve a subirlo con el mismo nombre.

**Notas:** El botón solo aparece si el servidor tiene configurada la carpeta compartida. Si no lo ves, usa la carpeta compartida o avisa al equipo técnico.

### Con la carpeta compartida

1. Abre la carpeta compartida de SABIA.
2. Entra a la carpeta del módulo (ejemplo: una guía sobre comités va en **Mecanismos de integración**).
3. Guarda o copia ahí el documento. No lo dejes suelto en la carpeta principal.
4. Espera unos minutos (el sistema revisa la carpeta cada 5 minutos).
5. Abre **ESTADO SABIA.txt** en la carpeta principal y busca tu archivo para ver su semáforo.

## Actualizar información que ya existe

### Con el botón Aportar un documento

1. Corrige el documento en tu equipo **sin cambiarle el nombre**.
2. Pulsa **+ Aportar un documento**, elige el **mismo módulo** y el archivo.
3. Pulsa **Publicar**.
4. SABIA avisa: "Ya existe "…" en … ¿Reemplazarlo por esta versión?". Pulsa **Aceptar**.
5. Revisa el semáforo del resultado.

### Con la carpeta compartida

1. Abre el archivo en la carpeta del módulo, corrígelo y guárdalo; o reemplázalo por la versión nueva **con el mismo nombre**.
2. Espera unos minutos y revisa **ESTADO SABIA.txt**.

**Notas:**

- No hace falta borrar nada antes: SABIA detecta que el archivo cambió y reemplaza la versión anterior.
- Si guardas la versión nueva **con otro nombre**, SABIA tendrá las dos versiones y podría responder con la vieja. Borra el archivo anterior (ver "Eliminar información").
- Si una versión nueva sale 🔴, SABIA deja de usar ese documento hasta que lo corrijas.
- Si al subir aparece "No se pudo guardar… Si alguien lo tiene abierto en Office, ciérralo e intenta de nuevo", cierra el archivo en Word, Excel o PowerPoint (tuyo o de un compañero) y vuelve a intentar.

## Eliminar información

1. Abre la carpeta compartida de SABIA y entra a la carpeta del módulo.
2. Borra el archivo (o muévelo fuera de la carpeta compartida si quieres guardarlo).
3. Espera unos minutos. En la siguiente revisión SABIA deja de usarlo y desaparece de **ESTADO SABIA.txt**.

**Notas:**

- El botón **+ Aportar un documento** solo agrega y reemplaza: para eliminar hay que usar la carpeta compartida.
- Si no tienes permiso para borrar en la carpeta compartida, pídeselo a quien la administra en el área de Calidad.
- Para quitar solo una parte de un documento, edítalo y guárdalo con el mismo nombre (ver "Actualizar información que ya existe").

## Cambiar un documento de módulo

1. En la carpeta compartida, mueve el archivo de la carpeta del módulo equivocado a la del módulo correcto.
2. Espera unos minutos y revisa **ESTADO SABIA.txt**.

**Notas:** No lo copies: si queda en las dos carpetas, SABIA lo usa en los dos módulos.

## Qué significa el semáforo

- 🟢 **Publicado**: SABIA ya lo usa para responder.
- 🟡 **Publicado con advertencias**: SABIA ya lo usa, pero conviene mejorarlo. Lee la nota y corrígelo cuando puedas.
- 🔴 **No publicado**: SABIA no lo usa. La nota dice exactamente qué corregir.

El resultado aparece en la ventana del botón **+ Aportar un documento** y en **ESTADO SABIA.txt** (carpeta principal de la carpeta compartida). Ese archivo lo escribe el sistema: no lo edites.

## Por qué un documento sale en rojo y cómo corregirlo

- **"Está suelto en la carpeta principal"**: muévelo a la carpeta de su módulo.
- **"La carpeta … no corresponde a ningún módulo"**: muévelo a una de las carpetas válidas que lista la nota.
- **"Es un Word antiguo (.doc)"** (o .ppt / .xls): ábrelo y usa **Guardar como** → .docx (o .pptx / .xlsx).
- **"Formato no soportado"**: guárdalo como Word, PDF, PowerPoint, Excel o texto.
- **"Es la plantilla sin llenar"**: escribe los pasos de tu tema en la plantilla y vuelve a subirla.
- **"Casi no tiene texto"**: suele ser un PDF escaneado o una imagen. Usa el Word original o el prompt para ordenarlo con IA.
- **"Parece la transcripción de una reunión"**: conviértela en guía con el prompt para ordenarlo con IA.
- **"El texto salió desarmado"** (marca de agua, columnas o tablas complejas): usa el Word original o el prompt para ordenarlo con IA.
- **"Es largo y no tiene títulos"**: sepáralo con los estilos Título 1 y Título 2 de Word, o usa el prompt para ordenarlo con IA.

## Por qué un documento sale en amarillo

- **Pocos títulos**: usa los estilos Título 1 y Título 2 para separar los temas.
- **Títulos que estaban solo en negrita**: el sistema los convirtió en títulos. Revisa que tenga sentido o usa los estilos de Word.
- **Imágenes que no se pueden leer**: describe con texto los pasos que muestran.
- **Una sección muy larga**: divídela con más títulos.

## Preguntas frecuentes

### ¿Cuánto tarda en aparecer lo que subo?

Con el botón **+ Aportar un documento**, unos segundos: el resultado aparece en la misma ventana. Con la carpeta compartida, hasta 5 minutos.

### ¿SABIA cambia o mueve mi archivo original?

No. El sistema lee el archivo, lo convierte en una copia limpia y la publica. El original queda igual en la carpeta compartida.

### ¿Qué pasa si subo un archivo con el mismo nombre que ya existe?

El botón pregunta si quieres reemplazarlo. Si es un documento distinto, cancela y cámbiale el nombre.

### Subí un documento pero SABIA no lo usa al responder

1. Revisa el semáforo: si está en 🔴, SABIA no lo usa.
2. Revisa que esté en la carpeta del módulo correcto.
3. Pregunta mencionando el módulo, o fija el módulo en el selector de la barra superior del chat.
4. Revisa que el documento tenga títulos descriptivos (ejemplo: "Crear un comité"): SABIA usa los títulos para encontrar la respuesta.

### ¿Puedo subir información de un módulo que no está en la lista?

No. Si necesitas un módulo nuevo, pídeselo al equipo técnico.

## Para el equipo técnico

Esta sección es para quien administra el servidor y el repositorio de SABIA.

### Agregar o actualizar una guía curada

1. Edita el archivo `.md` del módulo (ejemplo: `almera/modulo-documentos/gestion-documentos/AI/documentos-almera.md`).
2. Si es un archivo nuevo, agrégalo a la lista `files` de su módulo en `rag/sources.json`.
3. Reinicia el servidor (`npm start` o `iniciar.bat` en la raíz del repositorio).

### Quitar una guía curada

1. Quita la ruta del archivo de la lista `files` en `rag/sources.json`.
2. Reinicia el servidor.

### Agregar un módulo nuevo a SABIA

1. Agrega el módulo en `modules` de `rag/sources.json` con `id`, `name`, `description` y `files` (las guías `.md` curadas; puede quedar `[]` si el módulo solo se alimenta desde la carpeta compartida, como General).
2. Reinicia el servidor.
3. Crea en la carpeta compartida una carpeta con el mismo nombre del módulo. Si alguien sube un documento con el botón antes de crearla, el servidor la crea solo.

### Revisar la carpeta compartida sin esperar

Desde la carpeta `rag`, ejecuta `.venv\Scripts\python -m app.etl`. Procesa la carpeta una vez e imprime el semáforo de cada archivo.

**Notas:** Los detalles técnicos (ruta de la carpeta compartida, intervalo de revisión, tamaño máximo) están en `rag/README.md`.
