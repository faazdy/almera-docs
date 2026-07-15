# Almera — Módulo de Mecanismos de Integración (Comités y Actas) — guía de referencia completa

> Este documento reúne todo el conocimiento operativo del módulo de Mecanismos de Integración de Almera: procedimientos paso a paso, reglas del sistema y dudas que quedaron abiertas en la capacitación con soporte. No hubo un documento limpio disponible para este módulo — todo salió de una guía interna en HTML y de la transcripción completa de una capacitación con soporte de Almera (26 jun 2026).

**Instrucciones para la IA que use este documento:**
- Responde siempre con el procedimiento exacto documentado aquí, paso a paso, antes de sugerir cualquier otra cosa.
- No inventes pasos, botones o menús que no estén mencionados en este documento.
- Si la pregunta no está cubierta aquí, dilo explícitamente — no improvises.
- Si preguntan dónde encontrar una opción o módulo dentro de Admin, revisa primero el **Árbol de Navegación** al inicio de este documento.
- Revisa siempre la sección final **"Temas pendientes de validar"** antes de responder sobre los 4 tipos de privilegio o sobre la nueva función de plantilla en línea — hay puntos que quedaron sin resolver en la capacitación.

---

## Qué es este módulo

Gestiona **comités y sus actas de reunión** (juntas, comités estratégicos, operativos, grupos primarios, etc.). Es un módulo **privado por diseño**: un usuario solo ve los comités de los que es integrante, según los privilegios que se le asignen.

---

## Índice

0. Árbol de navegación de Admin (todos los módulos)
1. Conceptos básicos (acceso, privilegios, qué puede hacer cada rol)
2. Crear y configurar un nuevo comité/mecanismo
3. Crear una nueva clasificación de mecanismo
4. Campos "de cara al acta" vs. "de cara a la reunión"
5. Autenticación de usuarios externos (miembros de junta)
6. Elaborar un acta
7. Plantilla institucional del acta (variables, dónde se edita, función nueva de edición en línea)
8. Temas pendientes de validar con soporte Almera
9. Preguntas puntuales por correo

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

## Conceptos básicos — Módulo Mecanismos de Integración (Almera)

### Es un módulo privado

No cualquier usuario puede consultar actas o comités. Depende de:
- Los **privilegios/permisos** que se le hayan asignado.
- Si es **integrante** de ese comité específico.

### Cómo acceden los usuarios generales (integrantes)

Los integrantes de un comité ingresan a través de su **Plan Individual de Trabajo**, donde se les habilita una carpeta llamada **"Mecanismos de integración"**. Ahí ven únicamente los comités en los que participan — no el listado completo de todos los comités de la organización.

### Los privilegios por comité

Existen 4 tipos de privilegio asignables por comité (ver nota de confirmación abajo). Los dos que más se usan son:

| Privilegio | Qué puede hacer |
|---|---|
| **Miembro** | Solo consultar las actas, en modo lectura. No puede crear ni editar actas. |
| **Admin miembro** | Puede crear actas nuevas, editarlas, registrar compromisos, etc. Es el privilegio operativo del día a día. |

Además existe un privilegio especial:

| Privilegio | Qué puede hacer |
|---|---|
| **Administrador (solo)** | Se sugiere asignarlo únicamente al usuario administrador general del sistema, para que pueda dar soporte entrando a cualquier comité. Este usuario **no aparece en el listado de asistentes** de las actas, porque no es un integrante real del comité — solo tiene acceso administrativo. |

> **Nota de confirmación:** en la capacitación se mencionó explícitamente que existen "cuatro privilegios", pero solo se detallaron con claridad tres roles (Miembro, Admin miembro, Administrador). El cuarto no quedó identificado por su nombre exacto en la sesión — ver `08-pendientes-validar.md`.

### Solo los administradores de un comité pueden

- **Crear actas nuevas** (botón "Adicionar soportes" — ver `06-elaborar-acta.md`).
- **Editar la configuración del comité** (botón "Editar" en la parte superior del comité): información general, documento del acto administrativo de conformación, y la pestaña de **Privilegios**.
- **Actualizar el listado de integrantes** desde la pestaña "Privilegios" → "Administrar privilegios":
  - Para **quitar** a alguien del comité: buscarlo en el listado y quitarle el check de selección.
  - Para **agregar** a alguien: buscar el usuario en la parte superior, seleccionarlo, elegir su privilegio (Miembro o Admin miembro), y hacer clic en el ícono verde de **Adicionar**.

### Quién puede crear comités nuevos

Los **administradores del módulo completo de mecanismos** (no de un comité en particular) son quienes pueden crear comités/tipos de reunión nuevos, desde `Admin → Calidad → Mecanismos de integración → Parametrizar mecanismos de integración`. Cada organización debe definir internamente quién tiene ese rol.

**Fuente:** transcripción cruda de la capacitación, 26 jun 2026 (min ~0:09–9:57).

---

## Crear y configurar un nuevo comité/mecanismo

**Cuándo se usa:** para dar de alta un nuevo comité o tipo de reunión (junta, comité estratégico, operativo, etc.).

**Ruta:** `Admin → Calidad → Mecanismos de integración → Parametrizar mecanismos de integración`

### Pasos

1. Ir a `Admin → Calidad → Mecanismos de integración → Parametrizar mecanismos de integración`.
2. Elegir la clasificación correspondiente (ej. "Comités estratégicos", "Comités de junta") y hacer clic en **Adicionar**.
3. Registrar el **nombre** del comité.
4. Configurar las casillas de funcionalidad:
   - **Control de compromisos** — habilitarla.
   - **Aprobación de actas y firmas** — habilitarla.
   - **Realizar seguimiento** y **Mostrar tipo** — normalmente **no** se seleccionan.
   - **Mostrar logo** en el acta.
   - **Notificar cierre de acciones**: si se activa, cuando un responsable cierra un compromiso, el sistema envía una notificación por correo a los usuarios con privilegio **Admin miembro** de ese comité.
   - Permitir que los **miembros** (no solo los admin miembro) puedan adicionar compromisos/tareas.
5. Configurar la **codificación** de las actas:
   - **Manual** o **Automática**.
   - Si es automática: elegir si el consecutivo es **único** (nunca se reinicia) o se **reinicia cada año** (recomendado por buenas prácticas de gestión documental).
   - Definir el **patrón** de codificación, combinando:
     - `%C` = el consecutivo.
     - `%Y` = el año en curso.
     - **Padding** = cantidad de dígitos que tendrá el consecutivo (ej. padding 3 → el acta 1 se codifica como `001`).
   - Ejemplo de patrón: `%Y-%C` con padding 3 → el acta 1 del año 2026 queda como `2026-001`.
   - Definir el **consecutivo inicial** (ej. 1, si se reinicia cada año).
6. Definir si se quiere **restringir la descarga** de las actas.
7. Configurar el **pie de página**: mostrar quién generó/creó el acta originalmente, o mostrar el nombre del usuario que está haciendo la descarga en ese momento.
8. Presionar **Grabar**.

### Después de grabar la configuración

Se habilita la información de definición del comité:
- Datos generales del comité (fecha de creación, versión, normatividad, objetivo, etc. — según la estructura definida para esa clasificación).
- Adjuntar el **acto administrativo** con el que se conformó el comité.
- Definir los **cargos** (principal y suplente) de ese comité.
- Ir a la pestaña **Privilegios** para empezar a agregar los integrantes (ver `01-conceptos-basicos.md`).

**Fuente:** transcripción cruda de la capacitación, 26 jun 2026 (min ~10:20–17:09).

---

## Crear una nueva clasificación de mecanismo (más allá de "comité")

**Cuándo se usa:** cuando se necesita un tipo de mecanismo de integración completamente nuevo, distinto a los ya existentes (ej. "Grupos primarios"), con su propia estructura de campos.

**Ruta:** `Admin → Calidad → Mecanismos de integración → Parametrizar mecanismos de integración`

### Pasos

1. Ir a `Parametrizar mecanismos de integración` y adicionar una **nueva clasificación**.
2. Registrar:
   - **Nombre singular** (ej. "Grupo primario").
   - **Nombre plural** (ej. "Grupos primarios").
   - Nombre que tendrá el "documento de reunión" para esa clasificación — por ejemplo, si para comités se llama "Acta", para otra clasificación puede llamarse "Soporte" (singular) / "Soportes" (plural).
3. Grabar la clasificación.
4. Antes de crear los campos, crear primero un **Grupo** (agrupador) — los campos que se creen deben quedar asociados a un grupo.
5. Dentro de **Campos**, crear cada campo necesario:
   - Elegir el **tipo de dato**: texto de una línea, texto de múltiples líneas (para campos más amplios como "objetivo"), fecha (calendario), selección única, o selección múltiple.
   - Asignar un **código** al campo.
   - Si el campo es de selección (única o múltiple), usar la opción **Múltiple** para crear varias opciones de respuesta de una sola vez (más rápido que agregarlas una por una).
6. Grabar cada campo.

### Resultado

Una vez creada la clasificación con sus grupos y campos, al ir a crear un nuevo mecanismo de ese tipo, aparecerá automáticamente la nueva sección/estructura definida.

**Fuente:** transcripción cruda de la capacitación, 26 jun 2026 (min ~17:12–23:18).

---

## Campos "de cara al acta" vs. "de cara a la reunión"

**Cuándo se usa:** cuando un campo personalizado no aparece donde se esperaba (por ejemplo, se quiere que aparezca una sola vez en la información general del comité, pero está pidiéndose en cada acta nueva, o viceversa).

### La diferencia clave

Al crear un campo adicional para un tipo de comité (desde `Parametrizar mecanismos de integración`), cada campo se clasifica en una de estas dos ubicaciones:

- **De cara al acta:** el campo se pide **cada vez que se crea una nueva acta** (en la planeación de esa acta puntual). Útil para datos que cambian de una reunión a otra.
- **De cara a la reunión:** el campo aparece **una sola vez**, en la **información general** del comité (no se repite en cada acta). Útil para datos fijos del comité, como por ejemplo "miembros con voz y voto".

### Cómo corregirlo si un campo quedó mal clasificado

1. Ir a `Parametrizar mecanismos de integración` y entrar al tipo de comité correspondiente.
2. Ubicar el campo en cuestión.
3. Cambiar su clasificación entre "de cara al acta" y "de cara a la reunión", según corresponda.
4. Grabar.

### Caso real de ejemplo

Un usuario necesitaba que el dato "miembros con voz y voto" apareciera una sola vez en la información general del comité (no en cada acta). El campo estaba mal configurado como "de cara al acta", por lo que el sistema lo pedía en cada reunión nueva. La solución fue cambiar su clasificación a "de cara a la reunión".

**Fuente:** transcripción cruda de la capacitación, 26 jun 2026 (min ~48:23–53:17).

---

## Autenticación de usuarios externos (miembros de junta)

**Cuándo se usa:** cuando un comité (típicamente comités de junta) incluye personas externas a la organización, que no tienen correo con el dominio institucional.

### La regla clave

Al crear el usuario en el sistema, la forma de autenticación depende de si su correo pertenece o no al **dominio institucional** de la organización:

| Tipo de correo del usuario | Tipo de autenticación a usar |
|---|---|
| Correo institucional (mismo dominio que usa la organización para autenticarse, ej. `@capitalsalud.gov.co`) | **Autenticación externa**, seleccionando ese dominio institucional. No requiere definir contraseña en Almera — usa las credenciales del dominio. |
| Correo externo/personal (Gmail u otro dominio que no es el institucional) | **Autenticación SGI** (propia del sistema): sí requiere definir un login y una contraseña dentro de Almera. |

### Pasos para un usuario externo (ej. miembro de junta)

1. Crear el usuario en el sistema con **autenticación SGI** (no autenticación externa, porque su correo no pertenece al dominio institucional).
2. Definir su login y contraseña.
3. Ir al comité correspondiente y, desde la pestaña **Privilegios**, agregarlo como integrante (normalmente con privilegio **Miembro**, ya que suele ser solo para consulta y/o firma — ver `01-conceptos-basicos.md`).

### Notas / advertencias

- Con que el usuario tenga su cuenta creada (sin importar el tipo de autenticación) y esté agregado como integrante en el comité correspondiente, es suficiente para que pueda ingresar y consultar sus actas — no se requiere ninguna configuración adicional.
- La autenticación externa con dominio **solo aplica** si el correo del usuario realmente pertenece a ese dominio institucional; no se puede usar autenticación externa con un correo personal.

**Fuente:** transcripción cruda de la capacitación, 26 jun 2026 (min ~23:18–29:47).

---

## Elaborar un acta

**Cuándo se usa:** para registrar una reunión de un comité: planeación, asistentes, evidencias, contenido y compromisos.

**Quién puede hacerlo:** solo usuarios con privilegio **Admin miembro** (o Administrador) sobre ese comité, usando el botón **Adicionar soportes**.

### 1. Planeación

- Se registra: **fecha**, **hora de inicio**, **hora de finalización** y **lugar** de la reunión.
- La planeación se puede hacer **con anticipación**, incluso si la reunión todavía no ha ocurrido — se guarda como borrador y se retoma después con **Editar → Editar soportes**.
- Al grabar la planeación, el sistema genera automáticamente el **consecutivo del acta** (según el patrón configurado — ver `02-crear-comite.md`).
- No hay una única metodología correcta: algunos usuarios llenan el acta en vivo durante la reunión, otros toman notas aparte y las transcriben después.

### 2. Asistentes

- El sistema carga automáticamente todos los **integrantes del comité**.
- Se marca, para cada uno, si **asistió o no asistió** (esto alimenta los indicadores de asistencia a reuniones).
- Se pueden agregar **invitados** de dos tipos:
  - **Usuario del sistema:** buscar el usuario existente, seleccionarlo, y darle clic al ícono verde de **Adicionar**.
  - **Usuario externo:** registrar manualmente el nombre y datos adicionales (ej. empresa de la que viene), y darle clic al ícono de **Adicionar**.
- Desde esta pestaña también se puede **enviar una notificación de correo** a los asistentes (recordatorio de la reunión). Es un correo informativo editable — el sistema **no** lo agenda automáticamente en ningún calendario.

### 3. Archivos

- Aquí se adjuntan evidencias del comité (presentaciones, videos, soportes, etc.).
- **Importante:** después de seleccionar el archivo, hay que hacer clic en **Iniciar carga** — si no se hace, el archivo no queda subido.

### 4. Contenido

- Aquí se redacta el desarrollo de la reunión.
- **Recomendación:** si se necesita insertar imágenes o tablas, hacerlo **directamente desde las herramientas del editor** (no copiar y pegar desde Word), porque copiar/pegar a veces reduce la resolución de las imágenes.
- Las opciones de formato de texto son más limitadas que en Word, pero cubren lo básico.
- Ver `07-plantilla-institucional.md` para la función nueva que está reemplazando esta pestaña en algunos clientes.

### 5. Compromisos

- Se agregan compromisos/tareas con: nombre, fecha de cierre, y usuario responsable.
- **Importante — no es automático:** agregar un compromiso **no** notifica por correo al responsable. Para notificar:
  1. Usar el ícono del sobre, **Enviar notificaciones**.
  2. Escribir el mensaje (editable).
  3. Seleccionar cuál(es) compromiso(s) notificar — el sistema carga **todos los compromisos abiertos**, incluso de reuniones anteriores, no solo los de esta acta.
  4. Presionar **Enviar**.
- Cuando el responsable de un compromiso lo marca como cerrado, y si la opción "Notificar cierre de acciones" está activada para el comité, el sistema notifica automáticamente a los usuarios con privilegio Admin miembro (ver `02-crear-comite.md`).

### 6. Comentarios

- Los comentarios generales sobre el acta (no sobre un punto específico del contenido) se hacen desde el ícono de nube **Comentarios**, en la parte superior derecha — visible en el modo de visualización **Ver** (no en el modo Edición).
- Se puede escribir un comentario, grabarlo, y responder a comentarios existentes (hilo de respuestas). Queda registrado quién comentó y cuándo.
- Si se necesita que los comentarios queden anclados a una parte específica del contenido (no solo un comentario general), eso depende de si el comité usa la plantilla en línea nueva — ver `07-plantilla-institucional.md`.

### Generar el acta final

Cuando la elaboración está lista, usar **Generar informe** para producir el documento final del acta, en **Word** o en **PDF**, combinando todo lo diligenciado en el sistema con el formato de la plantilla institucional configurada para ese tipo de comité.

**Fuente:** transcripción cruda de la capacitación, 26 jun 2026 (min ~30:24–1:00:10).

---

## Plantilla institucional del acta

### Configurar el formato institucional (variables y tablas dinámicas)

**Cuándo se usa:** para que las actas de un tipo de comité usen el formato Word institucional (logo, encabezados, estructura), con los datos de la reunión rellenados automáticamente.

**Ruta general (a nivel de tipo/clasificación de comité):** `Admin → Calidad → Parametrizar Mecanismos de Integración → [tipo de comité] → pestaña Plantilla`

1. Elegir el tipo de comité.
2. En la pestaña **Plantilla**, hacer clic en **Elegir archivo** y cargar el formato institucional en Word (con logo, encabezados y estructura requerida).
3. Presionar **Grabar**.

#### Alias (variables del sistema)

Se escriben entre dobles llaves `{{ }}` dentro del Word, y el sistema las reemplaza por la información real de la reunión al generar el acta. **No modificar la escritura exacta de estos códigos** — si se altera, el sistema no los reconoce y el campo queda vacío.

| Variable | Qué inserta |
|---|---|
| `{{actaFecha_d}}` | Día de la reunión. |
| `{{actaFecha_F}}` | Mes de la reunión. |
| `{{actaFecha_Y}}` | Año de la reunión. |
| `{{actaHora}}` | Hora de inicio. |
| `{{actaHoraFin}}` | Hora de finalización. |
| `{{lugar}}` | Sitio de la reunión. |
| `{{reunionNombre}}` | Nombre registrado para la sesión. |
| `{{observacionesacta}}` | Comentarios generales registrados en el sistema. |

#### Tablas dinámicas

| Tabla | Qué genera |
|---|---|
| `content_asistentes` | Lista automática de asistentes a la reunión. |
| `content_actaCronograma_actividades` | Lista de compromisos/tareas pactadas en la reunión. |

- La entidad puede personalizar libremente el diseño (logo, colores, títulos, secciones nuevas), siempre respetando los alias.
- Actualizar la plantilla **no afecta** las actas ya generadas anteriormente — solo aplica a las actas nuevas que se creen después del cambio.

### Dónde se edita una plantilla YA cargada — el error más común

Existen **dos niveles** en los que puede vivir una plantilla:

1. **A nivel de tipo/clasificación de comité** (ej. "todos los comités estratégicos"), configurada desde `Parametrizar Mecanismos de Integración`.
2. **A nivel de un comité específico** — si ese comité en particular ya tiene su propia plantilla cargada.

**Una vez un comité específico ya tiene una plantilla propia cargada, para editarla o reemplazarla hay que hacerlo desde dentro de ese comité puntual — no desde la pantalla general de `Parametrizar Mecanismos de Integración`.** Intentar editarla desde la parametrización general de tipo, cuando el comité ya tiene su propia plantilla, puede hacer que deje de visualizarse o que aparezca un error al intentar cargar una nueva. Esto generó confusión real en la capacitación (ver `08-pendientes-validar.md`).

### Función nueva: reemplazo de la pestaña "Contenido" por edición en línea

Almera está migrando hacia un modelo donde la pestaña **Contenido** del acta (ver `06-elaborar-acta.md`) desaparece y se reemplaza por un **archivo Word editable en línea**, similar al editor del módulo de Documentos:

- En la pestaña **Archivos** del acta se habilita una plantilla en formato Word con la opción **Editar online**.
- Al editar online, se ve casi como un Word real, pero **solo se edita el contenido** — el encabezado con los datos de planeación se maneja con las mismas variables/alias descritas arriba (aparecen como códigos dentro del documento, no hay que tocarlos).
- Funciona con autoguardado, como un documento de Google — no hace falta descargar para conservar cambios.
- Dentro de esa plantilla en línea sí se pueden dejar comentarios anclados a un punto específico del contenido (no solo comentarios generales del acta).

#### Estado de esta función — importante

- **Solo está disponible para clientes nuevos** de Almera por el momento. Para activarla en una organización que ya viene usando la pestaña "Contenido" tradicional, hay que escribir a soporte solicitando el cambio.
- **No se confirmó si tiene costo.** Según Carlos (soporte Almera), probablemente no, pero debe confirmarlo el equipo de soporte.
- **No se confirmó qué pasa con las actas históricas** ya elaboradas con el sistema de "Contenido" tradicional al activar esta función — quedó como pregunta explícitamente sin resolver, que la organización debe escalar a soporte.

**Fuente:** guía interna HTML + transcripción cruda de la capacitación, 26 jun 2026 (min ~53:48–1:10:30).

---

## Temas pendientes de validar con soporte Almera

Estos son puntos que quedaron **sin resolver o sin confirmar** en la capacitación de Mecanismos de Integración del 26 de junio de 2026. El asistente debe avisar explícitamente que esto no está confirmado si alguien pregunta por estos temas.

### 1. El cuarto tipo de privilegio no quedó identificado

**Contexto:** Carlos mencionó que existen "cuatro privilegios" asignables por comité, pero en la explicación solo detalló con nombre y función tres: **Miembro**, **Admin miembro**, y el privilegio especial de **Administrador** (global, para soporte).

**Estado:** el cuarto privilegio de la lista no fue nombrado ni explicado explícitamente en la sesión. Si un usuario pregunta por un privilegio distinto a los tres documentados, no asumas cuál es — indica que no está confirmado en esta skill.

**Fuente:** transcripción cruda, min ~0:58–1:01.

### 2. Error al editar/cargar una plantilla ya existente a nivel de tipo de comité

**Contexto:** un usuario (Sergio) había cargado una plantilla institucional a nivel de "comités estratégicos" desde `Parametrizar Mecanismos de Integración`. Después, esa plantilla dejó de visualizarse y, al intentar cargar una nueva, el sistema mostró un error.

**Estado:** Carlos identificó la causa general (que una vez un comité específico tiene su propia plantilla, se debe editar desde el comité puntual, no desde la parametrización general — ver `07-plantilla-institucional.md`), pero **no se confirmó en la sesión si esa explicación resolvía el error puntual que Sergio reportó**, ni se completó una prueba en vivo que lo demostrara.

**Fuente:** transcripción cruda, min ~48:07–57:34.

### 3. Migración a la plantilla de edición en línea (reemplazo de "Contenido")

**Contexto:** ver el detalle completo en `07-plantilla-institucional.md`. Quedaron 3 preguntas explícitamente abiertas y remitidas a soporte por correo:
- ¿Tiene costo activar esta función para un cliente que ya está usando el sistema (no es cliente nuevo)?
- ¿Qué pasa con las actas ya elaboradas bajo el sistema anterior (pestaña "Contenido") al activar el cambio?
- ¿Quedaría temporalmente bloqueado el acceso a esa información histórica durante la migración?

**Estado:** ninguna de las tres fue respondida en la sesión — el equipo acordó enviar un correo consolidado a soporte para resolverlas. No presentes esta función como ya disponible o ya resuelta a menos que el usuario confirme que soporte ya respondió.

**Fuente:** transcripción cruda, min ~1:04:00–1:09:06.

### 4. Cómo enviar el acta a revisión/comentarios de todos los miembros antes de la firma

**Contexto:** Sergio explicó que en su comité operativo, solo firman presidente y secretario, pero antes de la firma se necesita que **todos** los miembros puedan revisar y comentar el contenido del acta (no solo quienes firman).

**Estado:** Carlos sugirió como única alternativa disponible usar el correo de notificación de la sección "Asistentes" (pensado originalmente para recordatorios de reunión) para pedirles a los miembros que ingresen y dejen sus comentarios/observaciones directamente en el acta. **No existe, a la fecha de esta capacitación, un flujo formal de "enviar a revisión de comentarios" distinto al de aprobación/firma.** Esto es una solución alterna, no una función dedicada.

**Fuente:** transcripción cruda, min ~40:03–47:40, ~1:11:44–1:12:47.

---

## Preguntas frecuentes puntuales (por correo)

Este archivo se va llenando con dudas específicas sobre Mecanismos de Integración que lleguen por correo y ya estén resueltas. Mismo formato que el resto de la skill:

```markdown
### <Pregunta o tema del correo>

**Cuándo se usa:** <contexto>

**Respuesta / pasos:** ...

**Notas / advertencias:** ...

**Fuente:** Correo de <remitente>, <fecha>, asunto "<asunto>".
```

*(Todavía no hay contenido aquí — pendiente de que se compartan los correos. Este es también el lugar donde debería quedar registrada la respuesta de soporte a los 3 puntos pendientes de `08-pendientes-validar.md` cuando llegue.)*