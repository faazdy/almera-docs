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
6. Recursos
7. Términos y definiciones
8. Configurar códigos consecutivos automáticos
9. Preguntas frecuentes
10. Temas pendientes de validar con soporte Almera

> **Guías separadas:** el *Mapa de procesos* (`mapa-procesos-almera.md`) y los *Modelos de gestión* (`modelos-gestion-almera.md`) tienen su propia guía. Si el usuario pregunta por ellos, indícalo.

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
## Navbar (Menú superior de navegación)
```
1. Gestión de Calidad
    - Mapa de procesos
    - Listados maestros
        - listado maestro de documentos
        - listado maestro de registros
 
    - Glorasio de terminos
    - Evaluacion
    - Reportes
        - General
            - Seguimiento MOP
            - Consolidado Estrategia
            - Utility Almera
            - Bitácora por usuario
            - Atributos sin calificar
 
        - Privilegios y Accesos
            -Privilegios
            - Súper usuarios
 
2. Documentos
    -Mis solicitudes
    - Mis pendientes
    - Elaborar
        - Documento especifico
    - Buscar
    - Estadísticas
 
3. Riesgos / Oportunidades
    - Matriz de riesgos
    - Controles
    - Evaluación Controles
 
4. Cuadro de Mando
    - Seguimiento
    - Mis tableros
 
5. Salir  / {nombre usuario} <- el logout
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
6. Presionar **Grabar y Enrutar**, para enviar la solicitud a aprobación. Al enrutar se elige a quién se envía la solicitud para revisión.
7. Quien recibe la solicitud tiene 3 opciones: **aprobar**, **rechazar** o **devolver** la solicitud.
8. Una vez aprobada la solicitud, el documento pasa a **Mis pendientes** del usuario que realizó la solicitud.
   - Abrir el documento y hacer clic en **Editar**.
   - Completar los campos adicionales que se habilitan, como la **Fecha** del documento y el **Responsable** (la persona o cargo responsable de la ejecución del documento; por ejemplo, el coordinador del área, no necesariamente quien redactó el documento).
   - Hacer clic en **Enviar a revisión**, ubicado en la parte superior.
   - En el campo **Ruta**, seleccionar el usuario que será el responsable del documento.
   - Completar obligatoriamente el campo **Observaciones**.
   - Hacer clic en **Grabar**.
9. Abrir la plantilla de Word y continuar la elaboración del documento desde el **editor en línea**.

> **Nota:** Una vez asignado el responsable, este podrá visualizar el documento en **Documentos → Mis pendientes**, desde donde podrá enviarlo a coordinación para aprobación o devolverlo a revisión si requiere ajustes.

### Código del documento

- El código puede diligenciarse manualmente o **generarse automáticamente**; es una configuración parametrizable por Almera (no algo que cada usuario active).
- La estructura más común es: **inicial del proceso + inicial del subproceso + inicial del tipo de documento + consecutivo**, pero es 100% ajustable a como la organización lo maneje internamente (p. ej. `PL-001-SIG` = Política – consecutivo – siglas del proceso).
- **Importante:** si la organización ya tiene documentos codificados manualmente antes de activar la generación automática, hay que pedirle a soporte que revise la parametrización para evitar que se generen códigos duplicados con los ya existentes.
- Para que el código automático **continúe la numeración existente** (p. ej. que después de `FR-030-SGC` siga `FR-031-SGC`), se configura el campo **Consecutivo** de cada tipo documental. Ver **"Configurar códigos consecutivos automáticos"** más abajo.

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

## Exportar a Excel

Existen dos formas de exportar la información a Excel.

### Opción 1: Exportar desde la lista de documentos

1. Aplique los filtros que necesite o déjelos vacíos para exportar todos los documentos.
2. Si la lista tiene varias páginas, aumente la cantidad de registros mostrados por página (por ejemplo, 100) para visualizar más documentos en una sola página.
3. Seleccione los documentos:
   - Para exportar todos los documentos visibles, utilice **Seleccionar → Todos**.
   - Si solo necesita algunos documentos, márquelos manualmente mediante las casillas de selección.
4. En el menú **Documentos seleccionados**, elija una de las siguientes opciones:
   - **Exportar todos:** exporta todos los documentos registrados en la plataforma.
   - **Exportar seleccionados:** exporta únicamente los documentos marcados con la casilla de selección.
5. En la ventana de exportación, **no marque la opción "Incluir archivos"**.
   > **Importante:** Esta opción incorpora los archivos adjuntos al reporte, lo que incrementa considerablemente el tamaño del archivo y puede hacer que la generación y descarga tarden mucho tiempo.

---

### Opción 2: Exportar desde el Listado Maestro de Documentos

1. Desde el menú superior ingrese a **Gestión de calidad → Listados maestros → Listado maestro de documentos**.
2. Si desea exportar documentos específicos, complete los filtros según su necesidad:

   | Campo | Descripción |
   |--------|-------------|
   | **Tipo** | Seleccione el tipo de documento (Proceso, Documento específico, etc.). |
   | **Filtro** | Permite buscar documentos por nombre. |
   | **Proceso** | Seleccione el proceso correspondiente. |
   | **Origen** | Seleccione el proceso o subproceso de origen. |
   | **Clase** | Seleccione la clase de documento. |
   | **Fecha** | Defina el rango de fechas para la búsqueda. |

Se recomienda que en el campo **Tipo** se seleccione el tipo de documentos que se desea exportar en Excel, ya que si se omite este paso, en el Excel aparecerán tambien los Procesos y Subprocesos (cosas que no son documentos en sí) y pueden afectar al analisis del estado DOCUMENTAL de Almera. Pero en caso de necesitar tambien Procesos y Subprocesos en el listado, puede omitir esta recomendacion.

3. Si aplicó filtros en el paso anterior: Haga clic en **Buscar** para visualizar los documentos que cumplen con los criterios establecidos.
4. Haga clic en el botón **Exportar** (ícono de Excel), ubicado en la parte superior derecha.

> **Nota:** El archivo de Excel incluirá únicamente los documentos que se encuentren visibles en la lista después de aplicar los filtros. Si no aplica filtros, se exportarán todos los documentos mostrados en el listado.

### Notas / advertencias

- La única forma de generar un reporte del listado de documentos es exportarlo a Excel; no hay reportes visuales adicionales dentro del módulo.
- El "listado maestro" que se genera en la OPCION 2 solo muestra documentos con estado **Vigente** por defecto — si se necesita ver la traza completa (incluyendo obsoletos/anulados/no publicados), hay que moverse a esas pestañas o quitar filtros según corresponda.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~14–20).

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

## Configurar códigos consecutivos automáticos (punto de partida del consecutivo)

**Cuándo se usa:** cuando un tipo documental (formatos, procedimientos, anexos, etc.) va a recibir códigos automáticos y ya existen documentos de ese tipo codificados. Se le indica a Almera desde qué número debe seguir, para que los documentos nuevos continúen la numeración y no repitan códigos existentes.

**Ruta:** entrar al **proceso o subproceso** y abrir la carpeta del tipo documental.

### Pasos

1. Entrar al **proceso o subproceso**.
2. En cada **carpeta de documentos** (las carpetas donde están los tipos de documento del proceso o subproceso), revisar cuál es el **número consecutivo más alto**. Ese número es el punto de partida.
   - Ejemplo: en la carpeta de Formatos, el documento con el número más alto es `FR-030-SGC`, así que el consecutivo más alto es **30**.
3. Hacer clic en el documento que tiene ese número más alto.
4. Dentro del documento, hacer clic en **Administrar** y, en el campo **Consecutivo**, escribir el **número siguiente** (en el ejemplo, **31**).
5. Hacer clic en **Grabar**.

### Resultado

A partir de ese momento, los documentos nuevos de ese tipo se crean desde el número que se escribió en el campo **Consecutivo**. En el ejemplo, el próximo formato queda con el código `FR-031-SGC`.

### Notas / advertencias

- El consecutivo se configura **por tipo documental**. Hay que repetir los pasos en cada tipo que vaya a recibir códigos automáticos (formatos, procedimientos, anexos, etc.).
- Tome como referencia el número **más alto** de la carpeta, no el último documento de la lista. Si escribe un número menor o igual al más alto, Almera puede generar un código que ya existe.
- Esto define **desde qué número** sigue el consecutivo. La **estructura** del código (siglas del tipo, consecutivo, siglas del proceso) la parametriza Almera (ver "Código del documento" en *Crear un documento*).

**Fuente:** apuntes internos del área de Calidad (`gestion-documentos/new.txt`, nov 2026).

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

### 2. ¿Qué diferencia hay entre los menús (superior/navbar o lateral/arbol de opciones) u opciones para los documentos?

**Cuándo se usa:** para cuando el usuario pregunte cual de las dos opciones de 'Documentos' utilizar en ciertos contextos.

**Menú superior -> Documentos:**
1. Crear documentos.
2. Ver documentos o tramites documentales pendientes (aprobar, rechazar o mandar a revision documentos).
3. Ver solicitudes de tramites documentales.
4. Estadisticas: Ver historico de tramites documentales en la plataforma, cuantos documentos hay por Subproceso, etc. En resumen, estadisticas de los documentos en la plataforma.
5. Buscar.

**Menú Lateral (Arbol de navegacion lateral). Admin -> Calidad -> Documentos:**
1. Ver todos los documentos subidos a la plataforma (Vigentes, No Publicados, Obsoletos, Anulados).
2. Descargar listado maestro de documentos (Excel con los datos de los documentos montados).
3. Filtrar documentos por Proceso/Subproceso.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

### 3. ¿Qué pasa si rechazo, apruebo o retorno una solicitud de documento?

**Cuándo se usa:** cuando un usuario encargado de revisar una solicitud de trámite documental desea conocer el resultado de cada acción disponible.

**Rechazar solicitud:**

Al rechazar una solicitud:

- La solicitud queda **cerrada definitivamente**.
- Se mueve a **Documentos → Mis Solicitudes → Solicitudes históricas** con el estado **Rechazado**.
- No es posible continuar el trámite sobre esa misma solicitud.

Si posteriormente se requiere continuar con el proceso, será necesario **crear una nueva solicitud desde cero**.

**Aprobar solicitud:**

Al aprobar una solicitud:

1. La solicitud queda aprobada y muestra la información registrada, como:
   - Tipo de solicitud.
   - Solicitud.
   - Tipo de documento asociado.
   - Clase de documento.
   - Subproceso.
   - Justificación.
   - Usuario que registra.
   - Fecha y hora.
   - Documento asociado.
2. Para anexar el documento, hacer clic sobre el nombre de la solicitud en la columna **Documento asociado**.
3. Dentro de la solicitud, hacer clic en **Editar**.
4. Completar o verificar la información del documento (Origen, Emisor, Clase, Código, Fecha, Título, Subproceso y Responsable).
5. En la sección **Archivos**, hacer clic en **Seleccionar archivo**.
6. Adjuntar el archivo correspondiente.
7. Hacer clic en **Grabar**.

El documento quedará cargado en la plataforma y asociado al proceso y subproceso correspondiente.

> **Nota:** Se recomienda acordar previamente con el coordinador quién será el responsable del documento.

**Retornar solicitud:**

Al retornar una solicitud para correcciones:

1. La solicitud vuelve al usuario que la creó.
2. El creador debe ingresar a **Documentos → Mis Solicitudes → Solicitudes en trámite**.
3. Allí encontrará la solicitud con estado **Borrador**.
4. Debe realizar los cambios necesarios.
5. Finalmente deberá volver a enrutar la solicitud al aprobador.

> Mientras la solicitud permanezca en estado **Borrador**, el aprobador que la retornó no podrá verla nuevamente hasta que el creador la envíe otra vez para aprobación.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 4. ¿El rechazo de una solicitud cierra definitivamente el trámite?

**Cuándo se usa:** cuando se desea saber si una solicitud rechazada puede continuar su proceso.

Sí.

Al rechazar una solicitud:

- El trámite queda finalizado.
- La solicitud pasa a **Solicitudes históricas** con estado **Rechazado**.
- No puede volver a enviarse para aprobación.

Si se requiere continuar con el trámite, será necesario crear una nueva solicitud.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 5. ¿Se puede modificar una solicitud rechazada?

**Cuándo se usa:** cuando un usuario desea realizar cambios sobre una solicitud que fue rechazada.

No.

Las solicitudes rechazadas quedan cerradas definitivamente y no pueden editarse ni reutilizarse.

Si es necesario realizar nuevamente el trámite, deberá crearse una nueva solicitud.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 6. Si recibo una solicitud para aprobar, ¿qué pasos debo seguir?

**Cuándo se usa:** cuando un usuario recibe una solicitud documental para revisarla y decidir si la aprueba, la retorna o la rechaza.

**Pasos:**

1. Ir al menú superior **Documentos → Mis Solicitudes → Solicitudes pendientes**.
2. Seleccionar la solicitud que desea revisar.
3. Al abrirla estarán disponibles las siguientes acciones:
   - **Editar solicitud.**
   - **Aprobar solicitud.**
   - **Retornar solicitud.**
   - **Rechazar solicitud.**
4. Seleccionar la acción correspondiente.
5. Registrar las **observaciones** justificando la decisión tomada.
6. Hacer clic en **Grabar**.

**Resultado de cada acción:**

- **Aprobar:** la solicitud vuelve al creador para que adjunte el documento y posteriormente lo envíe a coordinación para su aprobación final.
- **Retornar:** la solicitud vuelve al creador para que realice las correcciones necesarias y la envíe nuevamente.
- **Rechazar:** el trámite finaliza y la solicitud queda en estado **Rechazado**.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 7. ¿Puedo borrar una solicitud?

**Cuándo se usa:** cuando un usuario desea eliminar una solicitud documental creada previamente.

Sí, pero únicamente si la solicitud aún no ha sido enviada para aprobación.

**Pasos:**

1. Ir a **Documentos → Mis Solicitudes → Solicitudes en trámite**.
2. Verificar que la solicitud tenga estado **Borrador**.
3. Si se encuentra en ese estado, podrá eliminarse.
4. Se elimina dando clic en el ícono del bote de basura (ubicado en el costado derecho).

> Si la solicitud ya fue enrutada para revisión o aprobación, ya no podrá borrarse.

En ese caso, si se requiere eliminar el trámite, lo recomendable es solicitar al aprobador que **rechace la solicitud**.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 8. Después de aprobar una solicitud, ¿cómo anulo un documento para que deje de aparecer como vigente?

**Cuándo se usa:** cuando un documento ya fue publicado, pero debe quedar con estado **Anulado**.

**Pasos:**

1. Verificar que el usuario tenga permisos para administrar documentos.
2. Ir a **Admin → Calidad → Documentos**.
3. Buscar y abrir el documento que se desea anular.
4. Hacer clic en el botón **Anular**.
5. Completar la información solicitada.
6. Hacer clic en **Grabar**.

Para confirmar la anulación:

1. Regresar a **Admin → Calidad → Documentos**.
2. Abrir la pestaña **Anulados**.
3. Verificar que el documento aparezca en dicho listado.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

### 9. ¿Cómo actualizo la versión de un documento?

**Cuándo se usa:** cuando se requiere reemplazar el archivo de un documento vigente por una nueva versión, manteniendo el mismo registro del documento en la plataforma.

**Pasos:**

1. Ir a **Admin → Calidad → Documentos**.
2. Buscar y seleccionar el documento que desea actualizar.
3. Hacer clic en el botón **Corrección**, ubicado en la parte superior.
4. Se abrirá la vista de edición del documento, donde estarán disponibles:
   - **Botones:** Seguimiento, Anular y Administrar.
   - **Pestañas:** Documento específico(pestaña actual), Contenido y Seguridad.
   - **Información del documento:** Origen, Emisor, Clase, Código, Fecha, Título, Subproceso, Responsable y la sección **Archivos**.
5. En la sección **Archivos**, ubicar el archivo actualmente adjunto.
6. Hacer clic en los **tres puntos (⋮)** ubicados junto al nombre del archivo.
7. Seleccionar la opción **Actualizar versión**.
8. Adjuntar el nuevo archivo que reemplazará la versión anterior.
9. Hacer clic en **Grabar** para guardar los cambios.

> **Nota:** La plataforma debería actualizar automáticamente el número de versión del documento una vez se guarden los cambios. Esta información puede verificarse posteriormente en los detalles del documento.

## Temas pendientes de validar con soporte Almera

Estas son dudas que quedaron **abiertas** en la capacitación del 25 de junio de 2026 (Carlos, de Almera, dijo que las iba a confirmar pero no quedó registrada la respuesta en esta grabación). El asistente debe avisar explícitamente que esto no está confirmado si alguien pregunta por estos temas — no dar la respuesta como un hecho.

### Marca de agua en documentos derogados/obsoletos

**Contexto:** al descargar un documento vigente, sale la marca de agua "Copia no controlada". Se preguntó si los documentos en estado Obsoleto/Anulado descargan con una marca distinta (p. ej. "Derogado"), para poder demostrarle a un ente de control que ese documento ya no es el vigente.

**Estado:** Carlos respondió "buena pregunta" y dijo que lo iba a validar — no quedó una respuesta confirmada en esta sesión.

**Fuente:** transcripción cruda, min ~1:11–1:12.

### Generación automática de código con estructura personalizada

**Contexto:** la organización usa una estructura de código específica (tipo-consecutivo-siglas del proceso, ej. `PL-001-SIG`) y ya tiene documentos codificados manualmente. Se preguntó si Almera puede parametrizar la generación automática para replicar exactamente esa estructura sin generar códigos duplicados con los ya existentes.

**Estado:** Carlos confirmó que es parametrizable, pero pidió que se enviara una **solicitud formal a soporte** para hacer el ajuste, ya que hay que revisar los códigos ya existentes antes de activarlo.

**Actualización (nov 2026):** la parte de **no repetir códigos existentes** ya tiene procedimiento: se configura el campo **Consecutivo** de cada tipo documental (ver "Configurar códigos consecutivos automáticos"). Sigue sin confirmar si la **estructura** del código se puede cambiar a la medida sin pasar por soporte.

**Fuente:** transcripción cruda, min ~1:03–1:07.

> El pendiente "Mapa con ID mal vinculado" ahora vive en la guía `mapa-procesos-almera.md`.
