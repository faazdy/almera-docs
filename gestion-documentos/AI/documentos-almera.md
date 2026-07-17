# Almera — Módulo de Documentos (guía de referencia completa)

> Este documento reúne todo el conocimiento operativo del módulo de Documentos de Almera: procedimientos paso a paso, reglas del sistema y dudas que quedaron abiertas en la capacitación con soporte. Fue construido a partir de documentación limpia, una guía interna y la transcripción completa de una capacitación con soporte de Almera (25 jun 2026).

**Instrucciones para la IA que use este documento:**
- Responde siempre con el procedimiento exacto documentado aquí, paso a paso, antes de sugerir cualquier otra cosa.
- No inventes pasos, botones o menús que no estén mencionados en este documento.
- Si la pregunta no está cubierta aquí, dilo explícitamente — no improvises.
- Si preguntan dónde encontrar una opción o módulo dentro de Admin, revisa primero el **Árbol de Navegación** al inicio de este documento.
- La sección final **"Temas pendientes de validar"** contiene comportamientos del sistema que quedaron sin confirmar en la capacitación. No los presentes como hechos resueltos.

---

## Índice

0. Árbol de navegación de Admin (todos los módulos)
1. Conceptos básicos (estados de un documento, tipo adjunto vs. tipo plantilla)
2. Crear un documento (solicitud → aprobación → edición → plantilla online)
3. Crear un emisor (interno/externo)
4. Crear una clase de documento (tipo documental)
5. Buscar, filtrar y exportar documentos
6. Procesos y mapa de procesos
7. Modelos de gestión
8. Recursos
9. Términos y definiciones
10. Preguntas frecuentes
11. Temas pendientes de validar con soporte Almera

---

## Árbol de Opciones y Módulos Principales de Almera

Estructura de la pestaña 'Admin', donde se alojan las opciones y módulos del sistema. Usar esta guia para rutas requeridas por el usuario que aparezcan en este árbol.

---

### Árbol de Navegación

```
└── 📁 Admin (Pestaña Principal)
    ├── 📂 1. Calidad
    │   ├── 📄 Clases y Emisores de Documentos
    │   ├── 📄 Directorios
    │   ├── 📄 Documentos
    │   ├── 📄 Manejo de registros
    │   ├── 📄 Mecanismos de integración
    │   ├── 📄 Modelos de gestión
    │   ├── 📄 Parametrización procesos
    │   ├── 📄 Parametrizar Mecanismos de Integración
    │   ├── 📄 Procesos
    │   ├── 📄 Recursos
    │   └── 📄 Términos & Definiciones
    │
    ├── 📂 2. Evaluaciones
    │   ├── 📄 Administrar planes
    │   ├── 📄 Evaluaciones
    │   ├── 📄 Parametrización de Puntos de Atención
    │   ├── 📄 Parámetros generales evaluación
    │   ├── 📄 Reporte atenciones
    │   ├── 📄 Sistema de referencia
    │   ├── 📄 Tablero atenciones
    │   ├── 📄 Tipos de Evaluación
    │   └── 📄 Unidades auditables
    │
    ├── 📂 3. General
    │   ├── 📄 Bitácora
    │   ├── 📄 Cargos
    │   ├── 📄 Centro de seguridad
    │   ├── 📄 Correos
    │   ├── 📄 Empresas
    │   ├── 📄 Estructura organizacional
    │   ├── 📄 Favoritos
    │   ├── 📄 Grupos de cargos
    │   ├── 📄 Grupos de usuarios
    │   ├── 📄 Manual del sistema
    │   ├── 📄 Pagina de inicio
    │   ├── 📄 Parametrización cargos
    │   ├── 📄 Privilegios Generales del Sistema
    │   ├── 📄 Reglas de acceso
    │   ├── 📄 Reporte General de Acciones
    │   ├── 📄 Terminos Ayuda
    │   └── 📄 Usuarios
    │
    ├── 📂 4. Indicadores
    │   ├── 📄 Clasificaciones de Objetivos Estratégicos
    │   ├── 📄 Planeación estratégica
    │   ├── 📄 Reporte de indicadores
    │   └── 📄 Unidades y categorías
    │
    ├── 📂 5. Proyectos
    │   ├── 📄 Proyectos
    │   └── 📄 Tipos de Proyecto
    │
    └── 📂 6. Riesgos
        ├── 📄 Evaluación de Controles
        └── 📄 Sistemas de referencia
```

---

## Conceptos básicos — Módulo Documentos (Almera)

### Estados de un documento

Todo documento en Almera pasa por alguno de estos 4 estados. Todos son consultables (nada se pierde), pero solo un estado representa el documento "oficial" en uso:

| Estado | Qué significa |
|---|---|
| **Vigente** | Es la versión activa y oficial del documento en este momento. |
| **No publicado** | El documento ya se solicitó/creó pero todavía está dentro del flujo de aprobación (por ejemplo, esperando revisión de un líder). Para el sistema todavía no es "vigente", por eso no aparece en la pestaña de vigentes aunque ya exista y tenga trazabilidad de a quién se envió y en qué estado va. |
| **Obsoleto** | Cuando se sube una nueva versión de un documento, la versión anterior pasa automáticamente a este estado. Sigue siendo consultable, pero ya no es la oficial. |
| **Anulado** | El documento ya no aplica (se descontinuó). El sistema **no permite eliminar documentos por completo**, solo anularlos, para no perder la trazabilidad. Solo se elimina definitivamente (papelera) si de verdad se quiere perder ese rastro — no es lo recomendado. |

**Fuente:** Transcripción capacitación módulo Documentos, 25 jun 2026 (min ~17–19, ~46–47).

### Tipo de documento: "Adjunto" vs. "Plantilla"

Almera maneja (o manejaba) dos formas de construir un documento. Es importante que el usuario final entienda cuál está usando la organización:

**Tipo Adjunto (= "Documento específico")** — es el que se debe usar:
- El documento vive como una plantilla Word que se edita **online**, con un editor que funciona parecido a Google Docs (autoguardado, no hay que descargar para conservar cambios).
- Es el único tipo que trae el flujo completo de aprobación (solicitud → aprobación → edición → elaboración).
- Es hacia donde se están migrando todos los clientes de Almera.

**Tipo Plantilla** (forma antigua, en desuso):
- El documento se llenaba directamente dentro del sistema, campo por campo (un campo de texto para "Objetivo", otro para "Alcance", etc.), sin usar un archivo Word.
- Problema principal: al exportar el documento (especialmente con tablas o imágenes), el formato se desconfiguraba (márgenes asimétricas, etc.), generando muchos tickets de soporte.
- Por eso se está reemplazando por el tipo Adjunto.

> Si en el listado de "clases de documento" aparecen varios tipos documentales (instructivo, procedimiento, protocolo, etc.) pero solo uno de ellos tiene habilitado el flujo de elaboración, es porque los demás quedaron parametrizados como tipo Plantilla en algún momento y no se han migrado.

**Fuente:** Transcripción capacitación módulo Documentos, 25 jun 2026 (min ~52–57).

### Reglas generales a tener en cuenta

- Los documentos siempre deben quedar asociados a un **proceso o subproceso**.
- Cuando se busca el proceso/subproceso al crear un documento, el buscador hace match tanto por nombre de proceso como de subproceso — conviene que la organización defina una directriz interna de a cuál de los dos se debe amarrar siempre (por ejemplo: "siempre al subproceso"), porque el sistema no lo obliga.
- Los administradores del módulo (rol calidad) acceden a las funciones de configuración desde el panel lateral izquierdo, pestaña **Admin → Calidad**.

---

## Crear un documento (Elaboración)

**Cuándo se usa:** cuando se necesita un documento nuevo (política, guía, manual, procedimiento, etc.) dentro del sistema de gestión.

**Ruta:** `Documentos → Elaborar → Documento específico`

### Pasos

1. Ir a **Documentos → Elaborar → Documento específico**.
2. Seleccionar el **proceso o subproceso** al que quedará asociado el documento (el buscador encuentra coincidencias tanto en nombres de proceso como de subproceso — ver directriz en `01-conceptos-basicos.md`).
3. Ingresar el **nombre** del documento.
4. Elegir la **clase documental** (guía, manual, política, etc.). Si la clase no existe, ver `04-crear-clase-documento.md`.
5. Diligenciar la **justificación** de creación (por qué se necesita este documento). El campo "descripción" puede quedar en blanco si el contenido real se va a construir en la plantilla — no es obligatorio llenarlo en la solicitud.
6. Presionar **Grabar** y luego **Enrutar**, en la parte superior, para enviar la solicitud a aprobación. Al enrutar se elige a quién se envía la solicitud para revisión.
7. Quien recibe la solicitud tiene 3 opciones: **aprobar**, **rechazar** o **devolver** la solicitud.
8. Una vez aprobada, el documento pasa a **Mis pendientes** del usuario que lo solicitó:
   - Abrir el documento y darle **Editar**.
   - Completar los campos adicionales que se habilitan: **fecha** del documento y **responsable** (la persona o cargo dueño de la ejecución del documento — p. ej. el coordinador del área, no necesariamente quien lo redacta).
9. Abrir la plantilla Word y continuar la redacción desde el **editor en línea**.

### Código del documento

- El código puede diligenciarse manualmente o **generarse automáticamente**; es una configuración parametrizable por Almera (no algo que cada usuario active).
- La estructura más común es: **inicial del proceso + inicial del subproceso + inicial del tipo de documento + consecutivo**, pero es 100% ajustable a como la organización lo maneje internamente (p. ej. `PL-001-SIG` = Política – consecutivo – siglas del proceso).
- **Importante:** si la organización ya tiene documentos codificados manualmente antes de activar la generación automática, hay que pedirle a soporte que revise la parametrización para evitar que se generen códigos duplicados con los ya existentes.

### Editor en línea

- Funciona parecido a un documento de Google: **guarda automáticamente**, no es necesario descargar el archivo para conservar los cambios.
- Para retomar la edición más adelante, se abre el documento y se usa la opción **Editar online**; recupera todos los cambios previos.

### Vincular otro documento o formato dentro de la plantilla

- Dentro del editor en línea, si se necesita referenciar/enlazar otro documento del sistema (por ejemplo un formato o un manual relacionado), la única forma disponible es:
  1. Buscar el documento en el listado de Documentos.
  2. Copiar su enlace (URL).
  3. Pegar ese enlace dentro del texto de la plantilla que se está editando.
- No existe (al momento de esta capacitación) una forma de vincularlo por código o de forma automática — es siempre copiando y pegando el enlace.

### Documentos antiguos cargados en PDF

- Si un documento existente fue cargado originalmente como PDF, **no se puede activar la edición en línea** sobre él.
- Para habilitarla: hay que reconstruir el contenido en una plantilla Word editable y volver a cargarlo, reemplazando el PDF.

### Notas / advertencias

- El sistema no permite eliminar documentos, solo anularlos (ver estados en `01-conceptos-basicos.md`).
- Cuando un documento vigente se reemplaza por una nueva versión, la anterior pasa a estado "Obsoleto" automáticamente.
- El historial/versiones anteriores de un documento normalmente solo lo pueden consultar y descargar los administradores del sistema, no cualquier usuario.
- Al descargar un documento vigente (fuera del editor online) sale una marca de agua de **"Copia no controlada"**. **Sin confirmar todavía:** si esa misma marca de agua (o una distinta, tipo "Derogado") aplica también a documentos en estado Obsoleto/Anulado — quedó como pregunta abierta en la capacitación. Ver `11-pendientes-validar.md`.

**Fuente:** `docs-gestor-documento.md` (transcripción limpia) + HTML de documentación interna + transcripción cruda de la capacitación del 25 jun 2026 (min ~0–1:18).

---

## Crear un emisor (interno o externo)

**Cuándo se usa:** para registrar quién emite un documento. Aplica sobre todo a documentos externos (por ejemplo una resolución del INVIMA, un decreto, una norma de un ente de control) que se quieren tener dentro del sistema.

**Ruta:** `Admin → Calidad → Clases y emisores de documentos`

### Pasos

1. Ingresar a **Admin → Calidad → Clases y emisores de documentos**.
2. Seleccionar **Crear emisor** (botón a la derecha).
3. Registrar el **nombre** del emisor.
4. Asignar un **código** (puede ser un consecutivo numérico o unas iniciales, como se prefiera internamente).
5. Definir el **origen**: Interno / Externo / Ambos.
6. Presionar **Grabar**.

### Notas / advertencias

- Cuando un documento es **interno**, el campo de emisor siempre queda por defecto en el nombre de la propia organización — no se elige.
- Cuando un documento es **externo**, ahí sí se puede (y se debe) elegir quién es el emisor real (INVIMA, Servicio Geológico Colombiano, etc.).
- Si el emisor que se necesita no existe todavía en el listado, se crea desde aquí antes de subir el documento.

**Fuente:** `docs-gestor-documento.md` + transcripción cruda (min ~0–6).

---

## Crear una clase de documento (tipo documental)

**Cuándo se usa:** cuando se necesita un tipo de documento que todavía no existe en el sistema (por ejemplo, un nuevo "Protocolo").

**Ruta:** `Admin → Calidad → Clases y emisores de documentos`

### Pasos

1. Ingresar a **Admin → Calidad → Clases y emisores de documentos**.
2. Seleccionar **Crear clase**.
3. Registrar:
   - **Nombre** de la clase.
   - **Código** (puede ser las iniciales del tipo de documento o un número, según la convención interna).
4. Definir el **origen**: Interno / Externo / Ambos.
5. Marcar si la clase:
   - Corresponde a un **formato**.
   - **Aplica para solicitudes** — es decir, si al elaborar un documento nuevo de este tipo, el flujo debe empezar con una solicitud de aprobación. **Esta casilla sí es necesaria**: aunque no esté marcada, la clase igual aparece disponible al elaborar un documento; pero para que pase por el flujo de aprobación (buena práctica recomendada), debe estar activada.
6. Si la clase aplica para solicitudes, se habilita la opción **Adjuntar archivo**: aquí se sube la plantilla estándar en formato **Word (.doc)** para que los usuarios puedan usar la edición en línea sobre esa base. Si no se carga la plantilla aquí, no va a ser posible editar el documento en línea cuando se cree.
7. Presionar **Grabar**.

### Notas / advertencias

- **Orden del listado:** las clases siempre aparecen en el orden en que fueron creadas cuando se abre la sección; no hay un orden personalizado permanente. Se puede reordenar temporalmente haciendo clic en el encabezado de la columna (por **código** o por **nombre**, ascendente o descendente), pero eso no se guarda como configuración fija.
- **Eliminar una clase:** no se puede eliminar directamente si tiene documentos vinculados. Primero hay que reclasificar (cambiarle la clase) a todos los documentos que la usan, y solo entonces se puede eliminar la clase.

**Fuente:** `docs-gestor-documento.md` + transcripción cruda (min ~6–13).

---

## Buscar, filtrar y exportar documentos

**Cuándo se usa:** para consultar el listado general de documentos, filtrarlo, o sacar un reporte en Excel.

**Ruta:** módulo **Documentos** (panel lateral)

### Consultar el listado

Por defecto el sistema muestra los documentos **vigentes**. En la parte superior hay pestañas para ver también:

- **No publicados**: documentos en trámite dentro del flujo de aprobación (aún no vigentes).
- **Obsoletos**: versiones anteriores ya reemplazadas.
- **Anulados**: documentos descontinuados (recuerda: el sistema no elimina documentos, solo los anula).

> Importante: cada pestaña respeta el filtro que se tenga activo. Si filtras por un proceso específico y cambias a la pestaña de "Anulados", solo verás los anulados de ese proceso — para ver todos, hay que quitar el filtro.

### Filtrar

Desde el encabezado del listado se puede filtrar por, entre otros:
- **Origen** (interno / externo).
- **Proceso** específico (seleccionar el proceso y darle **Filtrar**).

### Exportar a Excel

1. Aplicar los filtros que se necesiten (o dejarlo sin filtrar para exportar todo).
2. Si la lista tiene varias páginas, se puede cambiar la cantidad de registros mostrados por página (p. ej. a 100) para verlos todos en una sola hoja.
3. Seleccionar los documentos: usar la opción **Seleccionar → Todos** para marcar todo el listado visible, o marcar manualmente.
4. En **Documentos seleccionados**, elegir **Exportar todos** o **Exportar seleccionados**.
5. **Advertencia:** en el cuadro de exportación, **nunca marcar la opción "Incluir archivos"** — hace que el reporte se vuelva muy pesado y la descarga puede tardar muchísimo (se mencionó como ejemplo "toda una semana").

### Notas / advertencias

- La única forma de generar un reporte del listado de documentos es exportarlo a Excel; no hay reportes visuales adicionales dentro del módulo.
- El "listado maestro" que se genera desde arriba del módulo de Documentos solo muestra documentos **vigentes** por defecto — si se necesita ver la traza completa (incluyendo obsoletos/anulados/no publicados), hay que moverse a esas pestañas o quitar filtros según corresponda.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~14–20).

---

## Procesos y mapa de procesos

### Modificar la jerarquía de un proceso (mover un subproceso)

**Cuándo se usa:** para trasladar un subproceso a un nuevo "proceso padre" (por ejemplo, si un subproceso pasó de depender de "Planeación estratégica" a depender de "Organización y métodos").

**Ruta:** `Admin → Procesos`

Hay **dos formas equivalentes** de hacerlo:

**Opción A — desde la sección Procesos:**
1. Ir a **Admin → Procesos**.
2. Buscar y seleccionar el subproceso que se quiere mover (se puede filtrar por nombre).
3. En el campo **Padre**, quitar el proceso actual y buscar/seleccionar el nuevo proceso del cual va a depender.
4. Presionar **Grabar**.

**Opción B — desde el mapa de procesos:**
1. Ir al mapa de procesos y ubicar el subproceso.
2. Darle **Editar** al subproceso — esto habilita, en la parte superior, la pestaña de **Administración**.
3. Desde ahí, cambiar el campo **Padre** de la misma forma.

> El mapa de procesos se actualiza automáticamente al guardar el cambio de jerarquía — no requiere reemplazar la imagen del mapa.

### Actualizar la imagen del mapa y vincular las áreas

**Cuándo se usa:** cuando se sube una imagen nueva del mapa de procesos y hay que hacer que sus zonas/botones lleven al proceso correcto.

**Ruta:** `Admin → Calidad → Parametrización de procesos`

1. **Reemplazar la imagen:** en la vista del mapa, seleccionar **Administrar archivos**, eliminar la imagen anterior y subir la nueva.
2. **Vincular las áreas:** hacer clic en **Administrar áreas** (esto abre un panel).
3. En otra pestaña del navegador, abrir el proceso específico (sección **Procesos**) y entrar a su pestaña **Seguimiento**; copiar la URL de esa página.
4. En el panel de "Administrar áreas", seleccionar la zona del mapa correspondiente a ese proceso y pegar la URL copiada en el campo **Dirección**.
5. Presionar **Grabar**.
6. Repetir el paso 3–5 para cada área/proceso del mapa.

### Notas / advertencias

- **El mapa solo carga procesos, no subprocesos** en el listado de "Administrar áreas". Si un área del mapa en realidad corresponde a un subproceso (y no tiene su propio "proceso" creado formalmente), no debe vincularse ese subproceso directamente ahí — lo correcto ("deber ser") es que tanto el proceso como el subproceso existan como entidades separadas en la sección **Procesos**.
- **Al reemplazar la imagen del mapa, las áreas/vínculos anteriores no se conservan** — hay que volver a vincular cada zona manualmente.
- Si un proceso quedó obsoleto o cambió de nombre tras una reestructuración del mapa (y ya no debería aparecer como vigente), la forma correcta de "retirarlo" es cambiarle el estado a **Anulado** — no eliminarlo — siempre que no tenga documentos ni indicadores asociados, para no perder trazabilidad.
- Antes de anular o unificar procesos, conviene validar que no tengan documentos o indicadores todavía asociados.

**Fuente:** `docs-gestor-documento.md` + transcripción cruda (min ~22–48).

---

## Modelos de gestión (normas ISO y similares)

**Cuándo se usa:** para cargar un estándar o norma de gestión (ISO 9001, ISO 45001, etc.) y poder, luego, seleccionar desde la caracterización de cada proceso qué ítems de esa norma le aplican.

**Ruta:** `Admin → Calidad → Modelos de gestión`

### Pasos

1. Ir a **Admin → Calidad → Modelos de gestión**.
2. Adjuntar el archivo del modelo/norma que se quiere cargar.
3. Presionar **Guardar**.
4. Una vez cargado, desde la **caracterización de un proceso** se puede seleccionar cuáles ítems de ese modelo le aplican a ese proceso específico.

### Notas / advertencias

- **Antes de subir un modelo de gestión nuevo, se recomienda primero preguntarle a soporte de Almera si ya lo tienen disponible como plantilla.** Cargar un modelo desde cero (ítem por ítem) es bastante operativo si Almera ya tiene ese estándar pre-armado, es mucho más rápido cargarlo directamente.

**Fuente:** transcripción cruda de la capacitación (min ~20–23).

---

## Recursos (para caracterización de procesos)

**Cuándo se usa:** cuando al caracterizar un proceso no aparece habilitado el campo para indicar qué tipo de recursos necesita — normalmente es porque el recurso todavía no ha sido creado en el catálogo.

**Ruta:** `Admin → Calidad → Recursos`

### Pasos

1. Ir a **Admin → Calidad → Recursos**.
2. Primero crear la **Clasificación** del recurso (categoría general), por ejemplo: Talento Humano, Infraestructura, Tecnológicos.
3. Luego crear el **Recurso** específico y asociarlo a una clasificación, por ejemplo: "Equipos de cómputo" asociado a la clasificación Infraestructura/Tecnológicos.
4. Una vez creado el recurso, ya queda disponible para seleccionarse (no crearse) desde la caracterización de cualquier proceso.

### Notas / advertencias

- Tener solo la **clasificación** creada no es suficiente — si el campo de recursos sigue sin habilitarse en la caracterización de procesos, revisar que exista también el **recurso** específico (no solo su categoría).

**Fuente:** transcripción cruda de la capacitación (min ~1:15–1:18).

---

## Gestión de términos y definiciones

**Cuándo se usa:** para mantener un glosario maestro de términos que se usan repetidamente en los documentos, y evitar que cada documento redefina el mismo término de formas distintas.

**Ruta:** `Admin → Calidad → Términos y definiciones`

### Pasos

1. Abrir el módulo.
2. Registrar el **término**.
3. Escribir la **definición**.
4. (Opcional) indicar la **fuente** de donde salió esa definición.
5. Presionar **Grabar**.

### Cómo se usa después

Una vez construido el listado, al redactar un documento no hay que volver a escribir la definición: simplemente se elige el término ya existente en el glosario y se vincula al documento.

**Fuente:** `docs-gestor-documento.md` + transcripción cruda (min ~48–51).

---

## Preguntas frecuentes — Documentos

---

### 1. ¿Cómo descargo los documentos de un proceso?

**Cuándo se usa:** para descargar en un solo archivo comprimido (.zip) todos los documentos asociados a un proceso específico.

**Pasos:**

1. Ir al **Mapa de procesos** y seleccionar el proceso de interés.
2. Dentro del proceso, dar clic en el botón **Editar** (parte superior izquierda, bajo la pestaña "General").
3. Ir a la pestaña **Documentación**.
4. En la parte superior derecha, hacer clic en el **ícono del .zip** (está al lado de un ícono de Excel) — es la opción para "Exportar archivos".
5. Se abre una ventana (modal) donde se puede seleccionar si se incluyen los **documentos obsoletos** y los **subprocesos**.
6. Dar clic en **Exportar**.
7. Se descargará un archivo comprimido (.zip) con todos los archivos.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

## Temas pendientes de validar con soporte Almera

Estas son dudas que quedaron **abiertas** en la capacitación del 25 de junio de 2026 (Carlos, de Almera, dijo que las iba a confirmar pero no quedó registrada la respuesta en esta grabación). El asistente debe avisar explícitamente que esto no está confirmado si alguien pregunta por estos temas — no dar la respuesta como un hecho.

### Marca de agua en documentos derogados/obsoletos

**Contexto:** al descargar un documento vigente, sale la marca de agua "Copia no controlada". Se preguntó si los documentos en estado Obsoleto/Anulado descargan con una marca distinta (p. ej. "Derogado"), para poder demostrarle a un ente de control que ese documento ya no es el vigente.

**Estado:** Carlos respondió "buena pregunta" y dijo que lo iba a validar — no quedó una respuesta confirmada en esta sesión.

**Fuente:** transcripción cruda, min ~1:11–1:12.

### Generación automática de código con estructura personalizada

**Contexto:** la organización usa una estructura de código específica (tipo-consecutivo-siglas del proceso, ej. `PL-001-SIG`) y ya tiene documentos codificados manualmente. Se preguntó si Almera puede parametrizar la generación automática para replicar exactamente esa estructura sin generar códigos duplicados con los ya existentes.

**Estado:** Carlos confirmó que es parametrizable, pero pidió que se enviara una **solicitud formal a soporte** para hacer el ajuste, ya que hay que revisar los códigos ya existentes antes de activarlo.

**Fuente:** transcripción cruda, min ~1:03–1:07.

### Migración de procesos con ID mal vinculado en el mapa

**Contexto:** se detectaron procesos donde el mapa apunta al ID de un proceso "padre" en vez del subproceso correspondiente (por un ajuste antiguo al mapa), generando enlaces que llevan al lugar equivocado.

**Estado:** Carlos dijo que había que "validarlo" caso por caso — es un tema de datos específico de esta organización, no un procedimiento general reutilizable. Si vuelve a surgir, contactar a soporte con el ID del proceso en cuestión.

**Fuente:** transcripción cruda, min ~38–44.