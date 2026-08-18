# Almera — Módulo de Evaluaciones / Auditorías (guía de referencia completa)

> Este documento reúne todo el conocimiento operativo del módulo de Evaluaciones (Auditorías) de Almera: procedimientos paso a paso, reglas del sistema y dudas que quedaron abiertas en la capacitación con soporte.

**Instrucciones para la IA que use este documento:**
- Responde siempre con el procedimiento exacto documentado aquí, paso a paso, antes de sugerir cualquier otra cosa.
- No inventes pasos, botones o menús que no estén mencionados en este documento.
- Si la pregunta no está cubierta aquí, dilo explícitamente — no improvises.
- Si preguntan dónde encontrar una opción o módulo dentro de Admin, revisa primero el **Árbol de Navegación** al inicio de este documento.
- Revisa siempre la sección **"Temas pendientes de validar"** antes de responder sobre el estado "Pendiente" del flujo o sobre "niveles de gestión".

---

## Qué cubre (y qué no) este módulo

- **Sí aplica:** auditorías internas, y auditorías externas donde la propia entidad es quien audita a un tercero.
- **No aplica:** cuando un ente regulador externo audita a la organización. En ese caso solo se registra el hallazgo como plan de mejora.
- El módulo parametriza las **auditorías** y los **planes de mejora** (hallazgos). Ambos viven bajo `Admin → Evaluaciones`.

---

## Índice

0. Árbol de navegación de Admin (todos los módulos)
1. Conceptos básicos (jerarquía Programa → Auditoría → Cuestionario → Pregunta, flujo de estados)
2. Crear una auditoría desde cero
3. Crear plantillas (para auditorías y para el programa anual)
4. Programa anual de auditorías
5. Equipo auditor y roles
6. Elaborar el cuestionario (lista de chequeo)
7. Sistema de referencia: campos, niveles de respuesta y niveles de gestión
8. Ejecución, hallazgos automáticos y cierre de la auditoría
9. Temas pendientes de validar con soporte Almera
10. Preguntas frecuentes

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

## Conceptos básicos — Módulo Evaluaciones (Almera)

### Jerarquía de objetos

```
Programa anual de auditorías  (opcional — agrupa auditorías programadas)
   └── Auditoría (evaluación)
          └── Cuestionario (puede haber varios por auditoría)
                 └── Preguntas (pueden tener sub-preguntas jerárquicas)
```

- Una **auditoría** puede tener **varios cuestionarios distintos**, y cada cuestionario se aplica a una o más **unidades auditables** (procesos). Esto permite, por ejemplo, que una misma auditoría tenga un cuestionario para "Calidad" y otro distinto para "Bienestar", cada uno con sus propias preguntas.
- El **Programa anual de auditorías** es para las auditorías que sí están programadas de antemano (cronograma anual). Las auditorías que llegan "por sorpresa" (una visita no esperada) se crean igual, pero **por fuera** del programa.

### Flujo de estados de una auditoría

1. **Planeación** — se diligencia toda la información: objetivo, alcance, criterios, unidades auditables, equipo auditor, cuestionario.
2. **Pendiente** *(opcional, depende de si la organización lo configuró)* — etapa intermedia de aprobación antes de pasar a ejecución (por ejemplo, si un director de planeación debe aprobar el programa antes de que arranque).
3. **Ejecución** — aquí se habilita la opción **Evaluar** dentro del cuestionario; es cuando se aplica realmente la auditoría.
4. **Evaluación** — validación final de lo ejecutado, generalmente por otra persona (un coordinador), quien puede **Aprobar** o **Rechazar** (devolviéndolo al auditor con observaciones).

El cambio de un estado a otro se hace con el botón **Aplicar transición**, indicando a quién se le envía (el responsable de esa siguiente etapa).

### Sistema de referencia

El **sistema de referencia** (por ejemplo "Auditoría interna") es la configuración base que define:
- Los **campos adicionales** de la ficha de la auditoría (objetivo, criterios, etc.).
- Los **niveles de respuesta** (cómo se califica cada pregunta: Cumple / No cumple / No aplica, etc.).
- Los **niveles de gestión** (cómo se resume el resultado de forma porcentual/agregada).
- Los **privilegios** de quién puede generar hallazgos desde ese sistema.

Cada auditoría queda asociada a un sistema de referencia — y **ese campo no se puede modificar después de guardar la auditoría** (ver `02-crear-auditoria.md`).

**Fuente:** transcripción cruda de la capacitación de Evaluaciones, 25 jun 2026 (min ~0:12–1:00).

---

## Crear una auditoría desde cero

**Cuándo se usa:** para configurar una auditoría nueva sin partir de una plantilla existente.

**Ruta:** `Admin → Evaluaciones → Evaluaciones`

### Pasos

1. Ir a **Admin → Evaluaciones → Evaluaciones**.
2. Hacer clic en **Adicionar** (parte superior).
3. Elegir el tipo **Evaluación**. Si no hay plantillas creadas, aparecerá la opción **"Sin plantilla"** — seleccionarla y dar **Aceptar**.
4. Diligenciar los campos que se habilitan:
   - **Año** de ejecución.
   - **Evaluador** (ver de dónde se crean en la nota de abajo).
   - **Nombre** de la auditoría.
   - **Código** (opcional).
   - **Sistema de referencia**.
   - **Periodo de tiempo** en el que aplica.
5. Presionar **Grabar**.
6. Una vez grabada, se habilitan los **campos adicionales** definidos en el sistema de referencia elegido (objetivo, criterios, etc. — ver `07-sistema-referencia.md`).

### Notas / advertencias

- **El campo "Sistema de referencia" no se puede modificar después de grabar.** Si se elige por error, la única solución es eliminar la auditoría y volver a crearla desde cero. Hay que ser cuidadoso al seleccionarlo.
- Los **evaluadores** disponibles en el listado se administran desde `Admin → Evaluaciones → Parámetros generales de evaluación` (el mismo lugar que se usa para el módulo de Planes de mejora). Ahí mismo se pueden crear evaluadores nuevos con la opción **Crear emisor** (nombre + tipo, ej. "Auditor interno").
- Si se necesita un campo adicional que no existe (por ejemplo "Objetivo de la auditoría"), se crea desde el sistema de referencia correspondiente — ver `07-sistema-referencia.md`.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~0:33–1:01) + guía HTML interna.

---

## Crear plantillas (para auditorías y para el programa anual)

**Cuándo se usa:** para no tener que diligenciar toda la información de una auditoría desde cero cada vez — se llena una sola vez como plantilla y luego el sistema la trae automáticamente.

**Ruta:** `Admin → Evaluaciones → Tipos de evaluación`

### Pasos

1. Ir a **Admin → Evaluaciones → Tipos de evaluación**.
2. Elegir el tipo correspondiente:
   - **Evaluación** — para plantillas de auditorías individuales.
   - **Programa anual de auditorías** — para la plantilla del programa que agrupa varias auditorías (ver `04-programa-anual.md`).
3. Entrar a la pestaña **Plantillas** y hacer clic en **Adicionar plantilla**.
4. Diligenciar toda la información una sola vez: año, evaluador, nombre, código, sistema de referencia, periodo/fechas, y luego (tras grabar) objetivo, alcance, criterios y demás campos adicionales del sistema de referencia.
5. Si la plantilla es de una auditoría (no del programa), además se pueden pre-cargar:
   - Las **unidades auditables** a las que aplica (ver notas).
   - El **equipo de trabajo** (roles) — ver `05-equipo-auditor.md`.
   - El **cuestionario** completo — ver `06-cuestionario.md`.
6. Grabar la plantilla.

### Usar la plantilla al crear una auditoría real

1. Ir a `Admin → Evaluaciones → Evaluaciones` (o a la pestaña **Auditorías** dentro de un programa, si aplica).
2. Al adicionar, en vez de "Sin plantilla", seleccionar la plantilla ya creada y dar **Aceptar**.
3. El sistema trae automáticamente toda la información pre-cargada (unidades auditables, equipo, cuestionario, campos). Solo queda actualizar lo que cambie para esa ejecución puntual (por ejemplo las fechas).

### Notas / advertencias

- Es perfectamente válido tener **varias plantillas distintas** para distintos tipos de auditoría recurrente (por ejemplo, una plantilla general para los numerales de la ISO 9001 que aplica a todos los procesos, y plantillas específicas por proceso para las preguntas propias de cada uno).
- Una plantilla puede aplicarse a **múltiples unidades auditables** (procesos) a la vez — se seleccionan todas las que correspondan al crear/editar la plantilla.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~1:41–2:59, ~1:15:46–1:19:13).

---

## Programa anual de auditorías

**Cuándo se usa:** para agrupar todas las auditorías que ya están programadas de antemano (durante un año o un semestre), en vez de crearlas sueltas.

**Ruta:** `Admin → Evaluaciones → Evaluaciones` (tipo "Programa anual de auditorías")

### Pasos

1. Primero crear una **plantilla de tipo "Programa anual de auditorías"** (ver `03-crear-plantillas.md`) si aún no existe.
2. Ir a `Admin → Evaluaciones → Evaluaciones`, dar **Adicionar**, elegir el tipo **Programa anual de auditorías** y seleccionar la plantilla. El sistema trae la información ya diligenciada (objetivo, alcance, criterios del programa).
3. Dentro del programa ya creado, entrar a la pestaña **Auditorías**.
4. Hacer clic en **Adicionar** para ir agregando, una por una, las auditorías que están programadas dentro de ese periodo — cada una puede venir de su propia plantilla de auditoría.
5. Cada auditoría agregada así queda **vinculada al programa** y aparece en su listado.

### Auditorías que NO van dentro del programa

- Auditorías que llegan sin estar programadas (una visita sorpresa, por ejemplo) se crean igual desde `Admin → Evaluaciones → Evaluaciones`, pero **eligiendo directamente el tipo "Evaluación"**, sin pasar por el programa — quedan "sueltas", fuera del programa anual.
- Auditorías donde un **ente externo** audita a la organización (no al revés) **no se crean en el sistema como auditoría** — solo se documenta el hallazgo o no conformidad resultante, directamente como plan de mejora.

### Notas / advertencias

- Puede que el botón para adicionar auditorías dentro de la pestaña "Auditorías" del programa no aparezca habilitado de inmediato — en la capacitación esto se resolvió refrescando/reingresando a la sección, sin que quedara clara la causa exacta. Si pasa, intentar refrescar la página antes de escalar a soporte.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~2:20–3:00, ~1:12:30–1:22:00).

---

## Equipo auditor y roles

**Cuándo se usa:** para definir quién participa en la ejecución de una auditoría y qué rol cumple cada uno.

**Ruta:** dentro de la auditoría (o su plantilla) → pestaña **Equipo de trabajo**

### Pasos

1. Dentro de la auditoría/plantilla, ir a la pestaña de **Equipo de trabajo**.
2. Hacer clic en **Adicionar rol**.
3. Definir el rol: nombre (ej. "Auditor líder", "Equipo auditor", "Equipo observador") y una descripción de sus responsabilidades.
4. Grabar el rol.
5. Volver a entrar al rol creado y, desde ahí, asignar el o los **usuarios responsables** de ese rol. Un mismo rol puede tener varios usuarios asignados.

### El campo "Responsable" en la pestaña General

Después de definir el equipo auditor, **hay que regresar a la pestaña General** de la auditoría: ahí se habilita un campo llamado **Responsable**, que antes de definir el equipo aparece deshabilitado. En este campo se elige cuál de los roles ya creados (ej. "Auditor líder") es el responsable general de la auditoría — este dato es el que se usa para las transiciones/aprobaciones del flujo.

### Notas / advertencias

- Al construir una **plantilla**, es útil dejar creados los roles (aunque sea sin asignar usuarios todavía) — ya es una ayuda grande para no tener que definir toda esa estructura de cero cada vez que se use la plantilla en una auditoría real.
- El campo Responsable no aparece habilitado hasta que exista al menos un rol con equipo auditor definido — si no se ve, revisar que se haya completado ese paso primero.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~2:46–2:53, ~44:17–44:41).

---

## Elaborar el cuestionario (lista de chequeo)

**Cuándo se usa:** para definir las preguntas de evaluación de una auditoría y a qué unidades auditables (procesos) aplican.

**Ruta:** dentro de la auditoría (o su plantilla) → pestaña **Cuestionario**

### Crear el cuestionario

1. Ir a la pestaña **Cuestionario** y hacer clic en **Adicionar cuestionario**.
2. Darle un nombre (ej. "Cuestionario cumplimiento SST").
3. Seleccionar las **unidades auditables** (procesos) a las que aplica ese cuestionario específico.
4. Grabar.

> Una misma auditoría puede tener **varios cuestionarios distintos**, cada uno aplicado a distintas unidades auditables. Esto permite, por ejemplo, un cuestionario de preguntas generales (ISO 9001) que aplique a todos los procesos, y cuestionarios adicionales con preguntas propias de cada proceso específico.

### Opción A — Cargar preguntas manualmente

1. Dentro del cuestionario, hacer clic en **Adicionar pregunta**.
2. Asignar un **código** a la pregunta (numeración manual, ej. 1, 2, 3...).
3. Escribir el texto de la pregunta.
4. Opcionalmente, relacionarla con el ciclo **PHVA** si aplica.
5. Grabar.

#### Preguntas jerárquicas (secciones con sub-preguntas)

Si una "pregunta" en realidad es una sección o clasificación (ej. "3. Parámetros generales de SST") que agrupa varias preguntas reales:
1. Crear esa pregunta-sección con su código normal (ej. `3`) — el sistema **no la cuenta como pregunta evaluable**, solo como encabezado.
2. Para las preguntas reales que dependen de ella, usar un código con el formato `3.1`, `3.2`, etc., y en el campo **Grupo** seleccionar la pregunta-sección (`3`) como su padre.

### Opción B — Carga masiva por Excel

1. Hacer clic en el ícono **Descargar plantilla** para bajar el Excel con la estructura actual del cuestionario (incluye las preguntas ya creadas, si las hay).
2. Completar el Excel agregando las preguntas nuevas, **manteniendo la misma estructura de numeración** que trae la plantilla (código, texto, relación al ciclo PHVA si aplica).
3. Guardar el Excel y usar el ícono **Cargar desde archivo Excel** para subirlo.
4. El sistema actualiza el cuestionario con las preguntas nuevas.

### Notas / advertencias

- La carga masiva **debe hacerse con la plantilla Excel que genera el propio sistema** — no se puede subir cualquier Excel con las preguntas ya armado en otro formato.
- Al mantener la numeración de la plantilla descargada, el sistema conserva correctamente la jerarquía de preguntas/sub-preguntas.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~2:52–5:24, ~1:16:53–1:19:13).

---

## Sistema de referencia: campos, niveles de respuesta y niveles de gestión

**Cuándo se usa:** para configurar, por cada sistema de referencia (ej. "Auditoría interna"), qué información se pide y cómo se califica cada auditoría que use ese sistema.

**Ruta:** `Admin → Evaluaciones → Sistemas de referencia → [sistema específico]`

### Crear campos adicionales

1. Entrar al sistema de referencia correspondiente (ej. "Auditoría interna") y a su pestaña **Campos**.
2. Hacer clic en **Nuevo campo adicional**.
3. Elegir el tipo de campo (texto de una o varias líneas, etc.), asignar un código consecutivo y el nombre del campo.
4. Elegir el **agrupador** — es lo más importante, porque determina en qué parte de la auditoría aparece el campo:
   - **General:** el campo aparece en la información general de la auditoría (ej. "Objetivo de la auditoría", "Criterios de auditoría").
   - **Hallazgo:** el campo aparece en la ficha de los planes de mejora/hallazgos.
   - **Pregunta:** el campo aparece dentro del cuestionario, en la pantalla donde se evalúa cada pregunta (ej. un campo de "Observaciones" junto a cada respuesta).
5. Si el agrupador que se necesita no existe todavía (por ejemplo, para que el campo aparezca en "Pregunta"), primero hay que crear un **agrupador nuevo** y asignarle esa ubicación, y luego crear el campo asociándolo a ese agrupador.
6. Grabar. Puede ser necesario refrescar la pantalla para ver el campo nuevo reflejado.

### Configurar niveles de respuesta

Los **niveles de respuesta** definen cómo se califica cada pregunta al momento de evaluar (ej. Cumple / No cumple / No aplica).

1. Ir a la pestaña de **Niveles de respuesta** del sistema de referencia.
2. Hacer clic en **Nuevo nivel de respuesta**.
3. Configurar cada nivel:
   - **Código** (orden).
   - **Nombre** (ej. "Cumple").
   - **Calificación** numérica que representa ese nivel (ej. 1 para Cumple, 0 para No cumple).
   - **Color** con el que se va a mostrar visualmente (ej. verde para Cumple, rojo para No cumple, gris para No aplica).
   - Si el nivel **no tiene peso** en el cálculo (por ejemplo, "No aplica" normalmente se configura sin peso).
4. Grabar cada nivel.

### Niveles de gestión

Además de los niveles de respuesta (que dan resultados absolutos: cuántas preguntas cumplieron/no cumplieron), existen los **niveles de gestión**, que dan un resultado más **porcentual/agregado** y se ven en la vista de **Seguimiento** de la auditoría (no en la vista de edición) — ver `08-ejecucion-y-hallazgos.md` para el detalle de dónde se visualizan.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~1:07–1:20, ~6:16–6:40, ~1:22:40–1:32:40).

---

## Ejecución, hallazgos automáticos y cierre de la auditoría

### Pasar la auditoría a ejecución

1. Con la planeación completa (objetivo, unidades auditables, equipo auditor, responsable definido, cuestionario listo), usar el botón **Aplicar transición** para pasar del estado Planeación (o Pendiente, si aplica) al estado **Ejecución**.
2. Al aplicar la transición se elige a quién se envía (el responsable de esa etapa).
3. Solo en el estado **Ejecución** se habilita, dentro de la pestaña **Cuestionario**, el ícono **Evaluar**.

### Evaluar el cuestionario

1. Entrar a la pestaña **Cuestionario** y usar el ícono **Evaluar**.
2. Para cada pregunta, seleccionar el **nivel de respuesta** que corresponda (Cumple / No cumple / No aplica, según lo configurado en el sistema de referencia).
3. Si el sistema de referencia tiene un campo de **Observaciones** habilitado en el agrupador "Pregunta", se puede diligenciar ahí una nota puntual sobre esa respuesta. También se pueden adjuntar archivos/evidencias.
4. Usar **Grabar e ir a la siguiente** para avanzar pregunta por pregunta.

### Generación automática de hallazgos ("Punto de atención")

Cuando una pregunta se califica con un nivel de respuesta de **no cumplimiento**, aparece la casilla **Punto de atención**:

- Marcarla es **opcional** — depende de si la organización considera que ese no-cumplimiento amerita un hallazgo formal (por ejemplo, algunas organizaciones solo generan hallazgo si hay incumplimiento recurrente durante varios períodos, no ante cualquier no-cumplimiento puntual).
- Al marcarla y grabar, el sistema **vincula automáticamente un hallazgo/plan de mejora** a esa auditoría, sin necesidad de crearlo manualmente desde el módulo de Planes de Mejora.
- La gestión y el análisis posterior de ese hallazgo se hacen desde el módulo de **Planes de Mejora**, no desde Evaluaciones — Evaluaciones solo es el punto de origen.

> Este mismo mecanismo de "generar hallazgo desde el origen" existe también en el módulo de **Indicadores** (pestaña "Planes de mejora" de un indicador → **Nuevo punto de atención**). Esa pestaña requiere que el usuario tenga privilegios sobre el sistema de referencia correspondiente — ver más abajo.

### Plan de trabajo de la auditoría (no confundir con el plan de mejora del hallazgo)

Dentro de la auditoría hay una pestaña **Plan de trabajo**, para asignar actividades o tareas relacionadas con la **ejecución de la auditoría misma** (no con un hallazgo puntual):

1. **Adicionar actividad**.
2. Definir código, nombre, descripción.
3. Si se desmarca la opción **Hito**, se piden fecha de inicio y fecha de cierre; si se deja marcada, solo se pide la fecha de cierre.
4. Asignar el o los usuarios responsables de esa actividad.

Las actividades vinculadas a un **hallazgo específico** (plan de acción del hallazgo) se gestionan aparte, desde el módulo de Planes de Mejora — son dos cosas distintas aunque funcionan de forma similar.

### Cierre y validación final

1. Al terminar de evaluar el cuestionario, usar **Terminar** para enviar la auditoría a validación.
2. Esto la pasa al estado **Evaluación**, donde otra persona (ej. un coordinador) revisa lo ejecutado.
3. Esa persona puede:
   - **Aprobar** → se finaliza el proceso.
   - **Rechazar** → se devuelve al auditor original, junto con las observaciones que deje, para corregir y reenviar.

### Reportes y resultados

Dentro de la pestaña **Cuestionario**, después de evaluar, hay dos opciones:

- **Reporte:** documento completo con toda la planeación de la auditoría y el detalle de cómo se evaluó cada pregunta.
- **Resultado:** resumen cuantitativo (cuántas preguntas cumplieron / no cumplieron), calculado con base en los **niveles de respuesta** configurados.

Además, en la vista de **Seguimiento** de la auditoría (distinta de la vista de "Editar"), hay una sección de **estadísticas por nivel** con gráficos descargables y resultados porcentuales por unidad auditable, calculados con base en los **niveles de gestión** configurados en el sistema de referencia.

### Privilegios para generar hallazgos desde otros módulos

El acceso a la pestaña que permite generar un hallazgo directamente desde otro módulo (ej. "Planes de mejora" dentro de un indicador) depende de privilegios asignados **por sistema de referencia**:

1. Ir a `Admin → Evaluaciones → Sistemas de referencia → [sistema] → Privilegios`.
2. Ahí aparece el listado de usuarios habilitados para generar hallazgos desde ese sistema de referencia en particular.
3. Después de que a un usuario se le otorgue el privilegio, es necesario que **refresque su sesión/página** para que la pestaña aparezca — no se actualiza en caliente.

> Incluso los administradores "superusuario" del sistema pueden no tener automáticamente todos los privilegios — hay que revisar y asignarlos explícitamente por sistema de referencia.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~41:19–1:11, ~53:49–1:11:02, ~59:31–1:06:03).

---

## Temas pendientes de validar con soporte Almera

Estos son puntos que quedaron **sin resolver o sin decidir** en la capacitación de Evaluaciones del 25 de junio de 2026. El asistente debe avisar explícitamente que esto no está confirmado si alguien pregunta por estos temas.

### 1. Origen desconocido de un "nivel de gestión" ya creado ("Avance completo")

**Contexto:** al revisar los niveles de gestión del sistema de referencia de Auditoría interna, apareció ya creado un nivel llamado "Avance completo" que ni Carlos (soporte Almera) supo explicar de dónde salió o quién lo creó.

**Estado:** quedó mencionado como una duda abierta, sin investigar en la sesión. Si un usuario pregunta específicamente por ese nivel, no asumas su función — indica que su origen no está confirmado.

**Fuente:** transcripción cruda, min ~1:32.

### 2. Si el estado "Pendiente" del flujo es necesario o no

**Contexto:** el flujo de una auditoría por defecto trae los estados Planeación → Ejecución → Evaluación. Sin embargo, en el sistema de la organización aparece también un estado intermedio llamado **Pendiente**, entre Planeación y Ejecución, pensado para una aprobación previa (por ejemplo, del director de planeación) antes de iniciar la ejecución.

**Estado:** esto no es una falla del sistema — es una **decisión de configuración pendiente** que la organización debe tomar (si quiere mantener ese estado intermedio de aprobación o simplificar el flujo pasando directo de Planeación a Ejecución). No está resuelta en la transcripción cuál decisión tomaron finalmente.

**Fuente:** transcripción cruda, min ~41:19–43:06.

### 3. Botón "Adicionar auditoría" dentro del programa a veces no aparece habilitado

**Contexto:** en un par de momentos de la demo, el botón para adicionar una auditoría dentro de la pestaña "Auditorías" de un programa anual no aparecía habilitado de inmediato.

**Estado:** se resolvió refrescando/reingresando a la sección, sin que Carlos explicara la causa raíz. No se documentó como un bug confirmado, pero vale la pena mencionarlo si un usuario reporta el mismo síntoma — la primera sugerencia es refrescar antes de escalar a soporte.

**Fuente:** transcripción cruda, min ~1:15:46–1:22:00.

---

## Preguntas frecuentes — Evaluaciones / Auditorías

---

### 1. ¿Cómo puedo ver las evaluaciones existentes y editarlas?

**Cuándo se usa:** para consultar el listado de auditorías/evaluaciones y modificar alguna.

**Ver el listado:** `Admin → Evaluaciones → Evaluaciones`. Ahí aparecen todas las auditorías o evaluaciones que existen en la plataforma.

**Editar una evaluación — hay 3 formas:**

**Opción 1 (ícono del lápiz):** en el costado derecho de cada evaluación, hacer clic en el ícono del **lápiz** (está al lado del estado de la evaluación). Se abre la vista de edición completa.

**Opción 2 (clic en el nombre):** hacer clic sobre el **nombre** de la evaluación (funciona como hipervínculo). Esto lleva a los detalles de la evaluación. Desde ahí, dar clic al botón **Editar** en la parte superior izquierda, debajo del título "Programa auditorías". Se abre la pestaña con todos los detalles para modificar.

**Opción 3 (edición rápida desde checkbox — solo para cambios muy puntuales):** seleccionar la evaluación con el **checkbox** en su costado izquierdo, ir a la parte superior en **Elementos seleccionados**, desplegar las opciones y elegir **Editar**. Se abre una ventana (modal) donde **solo se pueden modificar**: estados, fechas (planeada/ejecutada) y observaciones (el porqué se modifica, para la bitácora). Al finalizar, dar clic en **Grabar**.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 2. ¿Cómo veo auditorías de años anteriores?

**Cuándo se usa:** cuando se necesita consultar evaluaciones de años pasados (2024, 2025, etc.) que no aparecen en el listado.

**Pasos:**

1. Ir a `Admin → Evaluaciones → Evaluaciones`.
2. Verificar que no haya un **filtro de resultados** aplicado: en la parte superior derecha, revisar la opción **Filtrar** y quitar cualquier filtro activo.
3. Normalmente, las auditorías viejas no aparecen porque el listado muestra por defecto solo las del año vigente (2026). Al quitar los filtros, deberían aparecer todas.

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 3. ¿Cómo exporto un consolidado de las auditorías/evaluaciones?

**Cuándo se usa:** para descargar un reporte en Excel con el detalle de las auditorías existentes.

**Pasos:**

1. Ir a `Admin → Evaluaciones → Evaluaciones`.
2. Seleccionar las auditorías de interés con el **checkbox** (o seleccionar todas).
3. En la parte superior izquierda, junto al botón "Adicionar", hacer clic en el **ícono verde de descarga** (una ventana con un símbolo de descarga).
4. Se descarga un archivo Excel con el reporte.

**Campos del reporte:**

| ID | Tipo | Código | Nombre | Evaluador | Sistema de referencia | Fecha inicio | Fecha fin | Unidades auditables | Estado | Equipo de trabajo |
|---|---|---|---|---|---|---|---|---|---|---|

**Fuente:** Documento de profundización de capacitación (FAQ interno).

---

### 4. ¿Cómo cambio al auditor encargado en alguna auditoría?

**Cuándo se usa:** cuando se necesita reemplazar al auditor líder o modificar el equipo auditor de una evaluación ya creada.

**Pasos:**

1. Entrar a la auditoría de interés.
2. En la parte superior izquierda, dar clic al botón **Editar**.
3. Ir a la pestaña **Equipo**, donde se ve el auditor responsable y el equipo auditor.
4. Hacer clic en el **ícono del lápiz** en el costado derecho del rol que se quiere modificar (auditor líder o equipo auditor).
5. Se abre una ventana (modal) con la información del rol y la asignación.
6. Para agregar un usuario: buscarlo, hacer clic en el **ícono del avatar con el "+"** (en verde).
7. Para eliminar un usuario asignado: hacer clic en el **ícono del bote de basura** junto a su nombre.
8. Dar clic en **Grabar**.

**¿Se puede asignar más de un usuario?** Sí. Lo recomendable es hacerlo en el rol de **Equipo auditor** y dejar solo un usuario como responsable en **Auditor líder**.

**Nota:** si se necesita un rol adicional que no existe (por ejemplo, "Observador"), se puede crear con el botón **Adicionar Rol**, asignándole nombre y descripción.

**Fuente:** Documento de profundización de capacitación (FAQ interno).