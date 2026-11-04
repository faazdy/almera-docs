# SABIA — Cómo alimentar al asistente

Esta guía explica cómo enseñarle cosas nuevas a SABIA (el asistente "Pregúntale a SABIA"): cómo agregar información nueva, cómo actualizar la que ya tiene y cómo quitar la que ya no sirve. No hace falta saber código, instalar nada ni tener cuentas en otros sistemas.

## De dónde aprende SABIA

SABIA solo responde con lo que está en su base de conocimiento. Esa base tiene dos fuentes:

1. **Documentos que aporta el área de Calidad.** Se suben con el botón **+ Aportar un documento** del chat. Es el camino para cualquier persona.
2. **Guías curadas del equipo técnico.** Son los archivos `.md` del repositorio de SABIA (carpetas `almera/…/AI/`). Solo las cambia el equipo técnico (ver "Para el equipo técnico" al final).

Lo que no esté en ninguna de las dos fuentes, SABIA no lo sabe y responde "Eso no está en la documentación de SABIA".

Todos los profesionales usan la misma SABIA: lo que una persona aporta lo ven todos en cuanto se publica.

## Módulos a los que se puede aportar

Cada documento pertenece a un solo módulo. Los módulos son:

- Documentos
- Mapa de procesos
- Mecanismos de integración
- Modelos de gestión
- Evaluaciones
- Indicadores
- Planes de mejora
- Proyectos
- General (información de Almera que no pertenece a un solo módulo)

## Preparar el documento antes de subirlo

1. Descarga la plantilla: en el chat pulsa **+ Aportar un documento** → **↓ Descargar plantilla (.docx)**.
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

1. Descarga el prompt: en el chat pulsa **+ Aportar un documento** → **¿Es una transcripción o un PDF escaneado? Descarga el prompt para ordenarlo con IA**.
2. Abre la IA aprobada por la entidad. No uses cuentas personales para información interna.
3. Copia el texto del prompt (entre las líneas "COPIAR DESDE AQUÍ") y pégalo en el chat de la IA.
4. Debajo pega el contenido del documento o adjunta el archivo.
5. Revisa la respuesta: los pasos deben ser los mismos del documento original.
6. Pega la respuesta en el Bloc de notas y guárdala con extensión .txt (ejemplo: "Crear un comité.txt").
7. Súbela como cualquier documento nuevo (ver "Agregar información nueva").

## Agregar información nueva

1. Abre el chat de SABIA y pulsa **+ Aportar un documento** (barra superior, junto al selector de módulo).
2. En **¿De qué módulo es?** elige el módulo al que pertenece el documento.
3. En **Elige el archivo** selecciona el documento.
4. En **Tu nombre** escribe tu nombre. Queda registrado junto al documento, para saber a quién preguntar si hay dudas. SABIA lo recuerda para la próxima vez en ese mismo navegador.
5. En **Clave para aportar** escribe la clave que te dio quien administra SABIA en el área de Calidad. Si no aparece ese campo, no hace falta clave.
6. Pulsa **Publicar**.
7. Espera unos segundos mientras dice "Revisando…". SABIA muestra el resultado con el semáforo (ver "Qué significa el semáforo").
8. Si sale 🔴, corrige lo que dice la nota y vuelve a subirlo con el mismo nombre.

**Notas:**

- Si aparece "La clave para aportar no es correcta", revisa mayúsculas y minúsculas o pide la clave de nuevo a quien administra SABIA.
- Si aparece "No se pudo guardar … en el almacén de SABIA", no se publicó nada. Intenta de nuevo en unos minutos; si sigue, avisa al equipo técnico.

## Actualizar información que ya existe

1. Corrige el documento en tu equipo **sin cambiarle el nombre**.
2. Pulsa **+ Aportar un documento**, elige el **mismo módulo** y el archivo.
3. Pulsa **Publicar**.
4. SABIA avisa: "Ya existe "…" en … ¿Reemplazarlo por esta versión?". Pulsa **Aceptar**.
5. Revisa el semáforo del resultado.

**Notas:**

- No hace falta borrar nada antes: SABIA reemplaza la versión anterior. La versión anterior queda guardada en el historial por si hay que recuperarla.
- Si subes la versión nueva **con otro nombre**, SABIA tendrá las dos versiones y podría responder con la vieja. Pide que borren la anterior (ver "Eliminar información").
- Si una versión nueva sale 🔴, SABIA deja de usar ese documento hasta que lo corrijas.

## Eliminar información

El botón **+ Aportar un documento** solo agrega y reemplaza. Para eliminar un documento:

1. Escríbele al equipo técnico de SABIA con el **módulo** y el **nombre exacto del archivo** (ejemplo: Indicadores / crear-indicadores.docx).
2. El equipo técnico lo borra (ver "Para el equipo técnico").
3. En unos minutos SABIA deja de usarlo.

**Notas:** Para quitar solo una parte de un documento no hace falta borrarlo: edítalo y súbelo con el mismo nombre (ver "Actualizar información que ya existe").

## Cambiar un documento de módulo

1. Súbelo de nuevo con **+ Aportar un documento**, eligiendo el módulo correcto.
2. Pide al equipo técnico que borre el del módulo equivocado (ver "Eliminar información").

**Notas:** Mientras esté en los dos módulos, SABIA lo usa en los dos.

## Qué significa el semáforo

- 🟢 **Publicado**: SABIA ya lo usa para responder.
- 🟡 **Publicado con advertencias**: SABIA ya lo usa, pero conviene mejorarlo. Lee la nota y corrígelo cuando puedas.
- 🔴 **No publicado**: SABIA no lo usa. La nota dice exactamente qué corregir.

El resultado aparece en la ventana del botón **+ Aportar un documento**, apenas termina de revisarlo.

## Por qué un documento sale en rojo y cómo corregirlo

- **"Es un Word antiguo (.doc)"** (o .ppt / .xls): ábrelo y usa **Guardar como** → .docx (o .pptx / .xlsx).
- **"Formato no soportado"**: guárdalo como Word, PDF, PowerPoint, Excel o texto.
- **"Es la plantilla sin llenar"**: escribe los pasos de tu tema en la plantilla y vuelve a subirla.
- **"Casi no tiene texto"**: suele ser un PDF escaneado o una imagen. Usa el Word original o el prompt para ordenarlo con IA.
- **"Parece la transcripción de una reunión"**: conviértela en guía con el prompt para ordenarlo con IA.
- **"El texto salió desarmado"** (marca de agua, columnas o tablas complejas): usa el Word original o el prompt para ordenarlo con IA.
- **"Es largo y no tiene títulos"**: sepáralo con los estilos Título 1 y Título 2 de Word, o usa el prompt para ordenarlo con IA.
- **"Está suelto en la carpeta principal"** o **"La carpeta … no corresponde a ningún módulo"**: solo pasa si el archivo se agregó por fuera del botón. Avisa al equipo técnico.

## Por qué un documento sale en amarillo

- **Pocos títulos**: usa los estilos Título 1 y Título 2 para separar los temas.
- **Títulos que estaban solo en negrita**: el sistema los convirtió en títulos. Revisa que tenga sentido o usa los estilos de Word.
- **Imágenes que no se pueden leer**: describe con texto los pasos que muestran.
- **Una sección muy larga**: divídela con más títulos.

## Preguntas frecuentes

### ¿Cuánto tarda en aparecer lo que subo?

Unos segundos: el resultado aparece en la misma ventana y desde ese momento todos los profesionales lo ven en SABIA.

### ¿Necesito una cuenta para aportar?

No. Solo tu nombre y la clave para aportar. SABIA guarda el documento por ti.

### ¿SABIA cambia mi archivo original?

No. El sistema guarda el original tal cual, lo convierte en una copia limpia y publica esa copia.

### ¿Qué pasa si subo un archivo con el mismo nombre que ya existe?

El botón pregunta si quieres reemplazarlo. Si es un documento distinto, cancela y cámbiale el nombre.

### SABIA tardó mucho en abrir

Si nadie la ha usado en un rato, SABIA "se duerme" y la primera visita tarda alrededor de un minuto en responder. Después funciona normal.

### Subí un documento pero SABIA no lo usa al responder

1. Revisa el semáforo: si está en 🔴, SABIA no lo usa.
2. Revisa que lo hayas subido al módulo correcto.
3. Pregunta mencionando el módulo, o fija el módulo en el selector de la barra superior del chat.
4. Revisa que el documento tenga títulos descriptivos (ejemplo: "Crear un comité"): SABIA usa los títulos para encontrar la respuesta.

### ¿Puedo subir información de un módulo que no está en la lista?

No. Si necesitas un módulo nuevo, pídeselo al equipo técnico.

## Para el equipo técnico

Esta sección es para quien administra SABIA (Render y los repositorios de GitHub).

### Dónde quedan los documentos aportados

En el repositorio privado de GitHub `sabia-conocimiento`, una carpeta por módulo. Cada aporte es un commit con el autor en el mensaje ("Aporte: Indicadores/x.docx · por Ana Pérez").

### Eliminar o mover un documento aportado

1. Entra a `sabia-conocimiento` en github.com y abre la carpeta del módulo.
2. Abre el archivo → menú **⋯** → **Delete file** → **Commit changes**. Para moverlo, súbelo a la carpeta correcta (**Add file → Upload files**) y borra el original.
3. En la siguiente revisión (máximo 5 minutos) SABIA deja de usarlo.

### Deshacer un aporte

En el historial de commits de `sabia-conocimiento`, borra el archivo o restaura su versión anterior. SABIA toma el cambio en la siguiente revisión.

### Agregar o actualizar una guía curada

1. Edita el archivo `.md` del módulo (ejemplo: `almera/modulo-documentos/gestion-documentos/AI/documentos-almera.md`).
2. Si es un archivo nuevo, agrégalo a la lista `files` de su módulo en `rag/sources.json`.
3. Haz push a `master` de `almera-docs`. Render vuelve a desplegar SABIA solo.

### Quitar una guía curada

1. Quita la ruta del archivo de la lista `files` en `rag/sources.json`.
2. Haz push a `master`.

### Agregar un módulo nuevo a SABIA

1. Agrega el módulo en `modules` de `rag/sources.json` con `id`, `name`, `description` y `files` (las guías `.md` curadas; puede quedar `[]` si el módulo solo se alimenta con aportes, como General).
2. Haz push a `master`. La carpeta del módulo en `sabia-conocimiento` se crea sola con el primer aporte.

**Notas:** Los detalles técnicos (variables de Render, token de GitHub, claves, tamaño máximo) están en `rag/README.md`, sección "Desplegar en la nube".
