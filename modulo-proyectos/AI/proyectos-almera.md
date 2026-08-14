# Almera — Módulo de Proyectos — guía de referencia completa

> Este documento reúne todo el conocimiento operativo del módulo de Proyectos de Almera: procedimientos paso a paso, reglas del sistema y dudas que quedaron abiertas en la capacitación con soporte. Se construyó a partir de un documento limpio de pasos (extraído previamente de la capacitación) y de la transcripción cruda de **tres sesiones** de capacitación con soporte de Almera: 23 de junio de 2026, 30 de julio de 2026 (continuidad) y 4 de agosto de 2026 (tercer espacio, con refuerzo de soporte).

**Instrucciones para la IA que use este documento:**
- Responde siempre con el procedimiento exacto documentado aquí, paso a paso, antes de sugerir cualquier otra cosa.
- No inventes pasos, botones o menús que no estén mencionados en este documento.
- Si la pregunta no está cubierta aquí, dilo explícitamente — no improvises.
- Si preguntan dónde encontrar una opción o módulo dentro de Admin, revisa primero el **Árbol de Navegación** al inicio de este documento.
- Revisa siempre la sección final **"Temas pendientes de validar"** antes de responder sobre notificaciones automáticas al cierre de un proyecto — quedó un punto sin resolver en la capacitación.

---

## Qué es este módulo

Gestiona **proyectos institucionales** entendidos como **cronogramas de trabajo**: planeación, seguimiento de actividades, presupuesto, indicadores asociados y (opcionalmente) un flujo de estados/transiciones para darle trazabilidad al proyecto. El módulo opera bajo una jerarquía lógica de **cuatro niveles** que debe respetarse para que reportes y seguimiento funcionen correctamente:

1. **Tipo de Proyecto** — define las "reglas de juego" y parámetros generales (qué campos tiene, si tiene flujo, cómo se codifica, qué pestañas de actividad se habilitan).
2. **Proyecto** — la iniciativa específica, asociada a un tipo, con nombre y fechas globales de implementación.
3. **Cronogramas** — fases o etapas en las que se divide el proyecto, cada una con su propio peso porcentual.
4. **Actividades** — tareas puntuales dentro de un cronograma, con responsable, fechas y (si se habilita) presupuesto, entregables, recursos e indicadores.

---

## Índice

0. Árbol de navegación de Admin (todos los módulos)
1. Conceptos básicos y ruta de acceso
2. Configuración del "Tipo de Proyecto" (parametrización)
3. Flujo de trabajo — Estados y transiciones
4. Privilegios (dos niveles: tipo de proyecto y proyecto)
5. Crear el proyecto y sus cronogramas
6. Actividades: creación manual, masiva, hitos y campos adicionales
7. Indicadores asociados a actividades
8. Seguimiento y cierre de actividades
9. Seguimientos generales del proyecto (con estados propios)
10. Gestión presupuestal (dos niveles)
11. Visualización de resultados — pestaña Resumen
12. Relación entre tipos de proyecto y organización de proyectos similares
13. Integración con Plan Estratégico (Cuadros de Mando)
14. Reglas del sistema — qué no se puede hacer directamente
15. Temas pendientes de validar con soporte Almera

---

## Árbol de Opciones y Módulos Principales de Almera

Estructura de la pestaña 'Admin', donde se alojan las opciones y módulos del sistema. Usar esta guía para rutas requeridas por el usuario que aparezcan en este árbol, aunque sean de otro módulo distinto a Proyectos.

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
    │   ├── 📄 Página de inicio
    │   ├── 📄 Parametrización cargos
    │   ├── 📄 Privilegios Generales del Sistema
    │   ├── 📄 Reglas de acceso
    │   ├── 📄 Reporte General de Acciones
    │   ├── 📄 Términos Ayuda
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

## 1. Conceptos básicos y ruta de acceso

**Ruta de acceso:** Panel lateral izquierdo → **Admin → Proyectos**. La pantalla se divide en dos:

- **Sección derecha:** configurar el **Tipo de Proyecto** (parametrización — las "reglas de juego").
- **Sección izquierda:** gestionar los **Proyectos** específicos (la creación y operación diaria).

### El acceso a "Tipos de Proyecto" es por privilegios

No todos los usuarios que ven la pestaña "Proyectos" ven también "Tipos de Proyecto". En la primera sesión, dos usuarias con acceso a Proyectos no tenían habilitada la pestaña de Tipos de Proyecto — Carlos confirmó que **eso es un tema de privilegios**, no un error del sistema. Se recomienda que el acceso a Tipos de Proyecto quede limitado a los administradores del módulo (ver sección 4 — Privilegios), porque ahí se define toda la estructura que después usan los demás.

### Regla de jerarquía obligatoria

**Todo proyecto debe estar asociado a un Tipo de Proyecto.** Por eso el orden de trabajo siempre es:

1. Crear (o verificar que ya exista) el **Tipo de Proyecto**.
2. Crear el **Proyecto**, asociado a ese tipo.
3. Dentro del proyecto, crear **Cronogramas**.
4. Dentro de cada cronograma, crear **Actividades**.

**Fuente:** transcripción sesión 1 (23 jun 2026, min ~0:04–4:13) y sesión 2 (30 jul 2026, min ~1:18–1:26).

---

## 2. Configuración del "Tipo de Proyecto" (parametrización)

**Cuándo se usa:** antes de crear cualquier proyecto de un tipo nuevo, para definir su estructura y comportamiento.

**Ruta:** `Admin → Proyectos` → pantalla derecha → **Adicionar tipo** (botón en la parte superior).

### Pasos para crear un tipo de proyecto

1. Clic en **Adicionar tipo** y registrar el **nombre** del tipo de proyecto.
2. Configurar los **parámetros generales** (todos vienen desactivados por defecto — hay que marcarlos si aplican):
   - ¿Va a tener **indicadores** asociados?
   - ¿Se va a poder asociar a **múltiples años**?
   - ¿Se va a poder asociar a **procesos**?
   - **Marco estratégico** (habilita la opción de vincular el proyecto a un cuadro de mando/plan estratégico — ver sección 13). Está en el primer desplegable de **Parámetros generales**. Si no se va a usar, se recomienda dejarlo desmarcado para no generar pestañas vacías o confusión.
3. Definir la **codificación** del proyecto:
   - Patrón con `%Y` (año en curso) y `%C` (consecutivo). Ejemplo: patrón `%Y-%C` produce algo como `2026-00001`.
   - Definir la **cantidad de dígitos** (padding) del consecutivo.
   - Elegir si el consecutivo es **anual** (se reinicia cada año) o **único** (nunca se reinicia).
4. **Aceptar/Grabar.**

### Recomendación importante — evitar sobreparametrizar

Soporte de Almera (María Camila Martínez, sesión 3) fue explícita en esto: **es mejor habilitar solo los parámetros que realmente se van a usar.** Si se activan muchas opciones sin necesidad, quedan pestañas vacías en el proyecto y genera confusión al usuario final. La recomendación es partir de lo mínimo necesario e ir habilitando sobre la marcha, no activar todo "para probar" y dejarlo así.

**Fuente:** transcripción sesión 1 (min ~4:13–8:47), sesión 3 (min ~9:30–13:42, ~20:05–20:27).

---

## 3. Flujo de trabajo — Estados y transiciones

**Cuándo se usa:** cuando un tipo de proyecto necesita trazabilidad institucional — que se sepa en qué fase está (registro, revisión, aprobación, cierre) y, opcionalmente, que se enrute a un usuario específico en cada fase.

**No todos los tipos de proyecto necesitan flujo.** Puede haber proyectos donde simplemente se definen cronogramas y actividades, sin pasar por ninguna revisión — eso depende de la necesidad de cada tipo de proyecto.

**Ruta:** `Admin → Proyectos` → Tipos de Proyecto → entrar al tipo → pestaña **Configuración → Estados** / **Transiciones**.

### Crear estados

1. En **Configuración → Estados**, adicionar cada fase por la que pasará el proyecto (ejemplo real usado en capacitación: **Registrado → Seguimiento → Cumplimiento → Cerrado**).
2. Al crear un estado, se pueden definir parámetros como si ese estado **tiene seguimientos** habilitados o no (ver nota crítica más abajo) y si **tiene resumen**.
3. **Marcar "Tiene resumen" es importante** en el estado que corresponda — es lo que permite que se muestre el resumen de avance en ese estado (ver sección 11).

### Crear transiciones

1. En **Transiciones**, adicionar una transición nueva indicando desde qué estado sale y a qué estado llega (ejemplo: "Enviar a revisión" va de *Registrado* a *Seguimiento*).
2. Después de grabar la transición, se puede definir el **enrutamiento**: buscar el usuario (o varios) que deben recibir el proyecto en esa transición, y agregarlos con el ícono verde **Agregar**.
   - Si se enruta a **varios usuarios**, cuando alguien aplique la transición el sistema le mostrará el listado completo para que **elija a cuál de ellos enrutarlo** — no se envía a todos automáticamente.
3. Al aplicar una transición ya creada, el campo de **observaciones es obligatorio**.
4. El sistema envía una **notificación de correo informativa** al usuario que recibe el enrutamiento — es solo un aviso, no un flujo de aprobación con firma.

### Nota crítica — "tiene seguimientos" es por estado, no global

Si en un estado del flujo no aparece el botón **Adicionar seguimiento** dentro del proyecto, es porque ese estado específico no tiene habilitada la opción de seguimientos en su configuración. Hay que entrar a `Configuración del tipo → Estados`, editar el estado en cuestión, y activar la casilla correspondiente (aparece como "tiene seguimientos" / "permite editar seguimientos" — puede llamar "Habilitar edición"). Esto se debe repetir **para cada estado** en el que se quiera permitir registrar seguimientos, no queda activado automáticamente para todo el flujo.

**Fuente:** transcripción sesión 1 (min ~8:47–12:25), sesión 2 (min ~25:21–33:22, confirmación del detalle "tiene seguimientos" min ~39:42–41:08).

---

## 4. Privilegios (dos niveles)

Existen **dos niveles de privilegios**, independientes entre sí:

### A. Privilegios sobre el Tipo de Proyecto

**Se recomienda que sean limitados** — no todos los usuarios deberían poder crear o modificar tipos de proyecto, porque ahí se define toda la estructura.

**Ruta:** dentro de **Tipos de Proyecto** → pestaña **Privilegios** → **Administrar privilegios**.

1. Buscar el usuario.
2. Definir el tipo de privilegio: consulta, administrador, editar, o registrar.
3. Agregar.

### B. Privilegios sobre un Proyecto específico

Una vez creado el proyecto, este también tiene su propia pestaña **Privilegios**.

1. Buscar el usuario.
2. Definir el privilegio: administrador del proyecto, consulta, o si puede adicionar seguimientos, etc.
3. Clic en el ícono verde **Adicionar**.

**Fuente:** transcripción sesión 2 (min ~33:06–35:19).

---

## 5. Crear el proyecto y sus cronogramas

### Crear el proyecto

**Ruta:** `Admin → Proyectos` → pantalla izquierda → **Adicionar**.

1. Elegir a qué **Tipo de Proyecto** va a quedar asociado.
2. Definir el **consecutivo** (según la codificación del tipo).
3. Asociar a un **proceso**, si aplica.
4. Registrar el **nombre** del proyecto.
5. Registrar las **fechas** del proyecto (puede corresponder a un solo año o abarcar varios, según la duración real de la iniciativa).
6. **Grabar.**

Al grabar, se habilitan las pestañas superiores del proyecto: Cronogramas, Actividades (dentro de cada cronograma), Indicadores, Privilegios, Presupuesto (si está habilitado), Seguimiento general, etc.

### Adicionar cronograma

Un proyecto puede tener **n cantidad de cronogramas**.

**Ruta:** dentro del proyecto → pestaña **Cronogramas** → **Adicionar cronograma**.

1. **Código** del cronograma (importante definirlo).
2. **Nombre** del cronograma (ej. "Seguimiento", "Ajustes", "Almera Fase 1").
3. **Responsable** general de ese cronograma.
4. **Peso** — importancia porcentual de esa fase sobre el total del proyecto. Se define según la necesidad: puede ser 100% para cada cronograma si se miden de forma independiente, o repartirse (ej. 20% cada uno si hay 5 cronogramas) si se quiere que el avance total del proyecto sea un promedio ponderado.
5. **Fecha de inicio** y **fecha final** de ese cronograma.
6. **Grabar.**

**Fuente:** transcripción sesión 1 (min ~20:42–27:38), sesión 2 (min ~7:21–9:04).

---

## 6. Actividades: creación manual, masiva, hitos y campos adicionales

### Crear actividad manualmente

**Ruta:** dentro del cronograma → ícono **Adicionar actividad**.

1. **Ítem/consecutivo** de la actividad.
2. **Nombre** de la actividad.
3. **Descripción** — para ampliar qué se debe hacer.
4. **Fecha de inicio** y **fecha final** de la actividad — *o*, si se marca la opción **Hito** (ver abajo), solo una fecha.
5. Buscar y seleccionar el **usuario responsable**.
6. **Adicionar.**

### Hitos

Si una actividad **no tiene un rango de fechas sino una fecha única de entrega**, marcar la opción **Hito** en la parte superior del formulario. Al marcarla, el formulario deja solo una fecha (la fecha planeada de cierre) en vez de fecha inicio + fecha final.

### Carga masiva por Excel

**Ruta:** dentro del cronograma → ícono de Excel (**Cargar desde archivo**), parte superior derecha.

1. **Descargar la plantilla** del sistema (siempre debe partir de la plantilla de Almera, no de un Excel propio).
2. Completar la información siguiendo exactamente la misma estructura que trae la plantilla (incluye las actividades que ya existan).
3. La fecha debe registrarse en **formato tipo fecha**.
4. El **responsable** se registra con el **login** del usuario en el sistema (no el nombre completo).
5. Volver a la opción **Cargar desde archivo**, seleccionar el archivo diligenciado y **Cargar**.

### Campos adicionales a nivel de actividad

**Cuándo se usa:** cuando se necesita un campo extra en el formulario de "Adicionar actividad" que no viene por defecto (ej. "Cumplimiento", "Ciclo PHVA").

**Ruta:** `Tipo de Proyecto → Configuración → pestaña Actividades` → bajar hasta el final → **Nuevo campo adicional**.

**Importante — orden obligatorio:** antes de crear un campo, **primero hay que crear un Grupo** (agrupador/clasificación al que debe quedar asociado el campo). Pasos:

1. Crear el **Grupo** primero (ej. "Información general") y **Grabar**.
2. Luego crear el **campo**: nombre, tipo de dato, código, marcar **Requerido** si aplica.
3. **Grabar.**
4. El campo nuevo aparecerá automáticamente al adicionar una actividad nueva de ese tipo de proyecto.

**Fuente:** transcripción sesión 1 (min ~19:42–29:02), sesión 2 (min ~9:04–13:38).

---

## 7. Indicadores asociados a actividades

**Cuándo se usa:** cuando una actividad debe medirse a través de un indicador de gestión existente (o nuevo) en Almera.

**Ruta:** dentro de la actividad → pestaña **Indicadores**.

1. Si el indicador **ya existe**: buscarlo y seleccionarlo. Con eso el sistema lo relaciona al proyecto.
2. Si el indicador **es nuevo**: hay que **crearlo diligenciando la ficha técnica completa** — no se puede omitir este paso para indicadores nuevos.

### Aclaración clave — el indicador NO se mide desde Proyectos

Vincular un indicador a una actividad **solo relaciona** ese indicador con el proyecto — no genera ahí un seguimiento numérico de variables frente a meta. La **medición real del indicador** (registrar variables, calcular cumplimiento frente a la meta) se hace **exclusivamente en el Módulo de Indicadores**, no dentro de Proyectos. El porcentaje de avance que se ve dentro del proyecto corresponde al **cumplimiento de las actividades**, no al cumplimiento del indicador.

**Fuente:** transcripción sesión 1 (min ~27:40–43:52), sesión 2 (min ~41:14–46:27).

---

## 8. Seguimiento y cierre de actividades

El sistema muestra el proyecto en **dos visuales**:

- **Edición** — para planear (crear/editar cronogramas y actividades, sin ver porcentajes de cumplimiento).
- **Seguimiento** — para ejecutar (ver avance ponderado, gráficos, filtros por fecha, y registrar el cierre).

### Cerrar una actividad

1. Entrar a la actividad. Según si tiene una o dos fechas, el botón visible será distinto:
   - Si la actividad tiene **fecha de inicio y fecha final** (no es hito): aparece el botón **Iniciar actividad**.
   - Si la actividad es **Hito** (una sola fecha): aparece directamente **Terminar actividad**.
2. Registrar la **fecha** en la que se realiza el avance/cierre.
3. Registrar el **porcentaje de avance** — **es acumulativo**: se debe ir sumando en sucesivos registros hasta llegar al 100%.
4. Adjuntar **evidencias** si aplica.
5. **Grabar.**
6. Cuando la actividad llega al **100%**, el sistema la marca como **finalizada**.

### Plan Individual de Trabajo

Los responsables ven sus actividades asignadas en el panel lateral izquierdo, en **Plan Individual**, y también en la pestaña **Personal** en formato calendario. Al cerrar una actividad al 100%, **desaparece automáticamente** del Plan Individual del responsable — aunque, si la persona ya tenía la pantalla cargada, es posible que necesite refrescar o hacer alguna acción para que el listado se actualice.

### No hay notificación automática al asignar una actividad

Cuando se registra el responsable de una actividad nueva, **no existe una opción de correo automático** que le avise de inmediato. Siempre debe usarse la opción manual de notificación disponible en el sistema.

**Fuente:** transcripción sesión 1 (min ~31:24–33:22), sesión 2 (min ~13:42–20:44).

---

## 9. Seguimientos generales del proyecto (con estados propios)

**Cuándo se usa:** para registrar seguimientos generales sobre el estado de la iniciativa (no ligados a una actividad puntual), con evidencias y comentarios.

**Ruta:** dentro del proyecto, en la **visual de Seguimiento** → pestaña **Información general** → botón **Adicionar seguimiento** (parte inferior).

1. Registrar la **fecha**.
2. Describir el **seguimiento realizado**.
3. Adjuntar **evidencias**, si aplica.
4. Opcionalmente, indicar a qué **estado del seguimiento** corresponde ese registro (ver abajo).
5. **Grabar.**

### Estados propios para los seguimientos (trazabilidad por etapas)

Además del flujo del proyecto (sección 3), se pueden crear **estados específicos para los seguimientos** — por ejemplo: "Etapa de revisión", "Etapa de control de cambios", "Cumplimiento". Esto permite que cada seguimiento quede etiquetado con la etapa a la que corresponde.

**Ruta:** `Tipo de Proyecto → Configuración → pestaña Seguimiento`.

1. Crear cada estado necesario (ej. Estado 1: "Etapa de revisión", Estado 2: "Etapa de control de cambios", Estado 3: "Cumplimiento").
2. Al registrar un seguimiento desde el proyecto, ahora se podrá indicar a cuál de esos estados pertenece.

### Sobre el requisito de "segunda/tercera línea" de seguimiento

Varios usuarios preguntaron si existe, como en Planes de Mejora, una pestaña fija de "seguimiento de control" (segunda línea que valida lo que reportó el responsable). **En Proyectos esta pestaña fija no existe por defecto.** La forma de lograr ese control de varias líneas es **crear un flujo con más estados** (sección 3) — por ejemplo: Registro → Seguimiento (primera línea) → Cumplimiento (segunda/tercera línea, validado por control interno u otra área) → Cerrado. Cada organización nombra esos estados como necesite.

**Fuente:** transcripción sesión 1 (min ~44:19–50:24), sesión 2 (min ~20:44–33:22).

---

## 10. Gestión presupuestal (dos niveles)

El sistema permite controlar costos de **dos maneras**, según el nivel de detalle que se necesite:

### A. A nivel de Actividad (detallado, con suma automática)

1. Habilitar el campo de **presupuesto** en la configuración de actividades del tipo de proyecto.
2. Dentro de cada actividad, en la pestaña **Costos**, registrar el **presupuesto planeado** (ej. 20.000).
3. Al reportar el avance de la actividad (pestaña **Seguimientos** de la actividad → **Adicionar**), además del porcentaje de avance se registra el **valor ejecutado** y una observación → **Grabar**.
4. El sistema **suma automáticamente** los valores ejecutados de todas las actividades para mostrar el total ejecutado a nivel de cronograma y de proyecto. Puede ser necesario volver a la pestaña **Seguimiento** del proyecto (o recargar) para que la vista se actualice.

### B. A nivel de Atributos (manual, sin desglose por actividad)

**Cuándo se usa:** cuando el proyecto **no** requiere desglosar el presupuesto actividad por actividad.

1. En `Tipo de Proyecto → Configuración → pestaña Atributos`, crear (o usar el existente) un campo tipo **"Presupuesto estimado/aprobado"**.
2. Crear un segundo campo nuevo, tipo numérico, llamado **"Presupuesto ejecutado"**.
3. Ambos campos se **diligencian manualmente** en la ficha general del proyecto — no hay suma automática, porque no hay de dónde traer el valor.

### Recomendación de soporte Almera

Si se opta por la opción B (campos manuales a nivel de atributos), **se recomienda inactivar la opción de presupuesto a nivel de actividad** para ese tipo de proyecto, de manera que no queden dos lugares distintos donde registrar presupuesto y se genere confusión al usuario.

**Fuente:** transcripción sesión 2 (min ~46:27–48:58), sesión 3 (min ~1:05–9:08).

---

## 11. Visualización de resultados — pestaña Resumen

### Parámetro obligatorio — "Mostrar resumen de cronogramas"

Para que el proyecto muestre el resumen automático de avance, **es indispensable activar el parámetro "Mostrar resumen de cronogramas"**, ubicado en la **Configuración general** del tipo de proyecto (o del proyecto). Sin este parámetro activo, la información general del proyecto no mostrará el resumen gráfico de cumplimiento.

### Qué muestra el resumen

Una vez activo, en la pestaña **Información general** (visual de Seguimiento) o en la pestaña **Resumen**, el sistema genera automáticamente:

- El **porcentaje de avance total** del proyecto.
- El avance de **cada cronograma** por separado, y su **peso** dentro del total.
- Comparativo de **ejecución física real vs. esperada**, según las fechas definidas.
- Filtros por **rangos de fecha**.
- Opción de **descargar el gráfico**.
- **Zoom** a las actividades para identificar cuáles están atrasadas o finalizadas.

**Fuente:** transcripción sesión 2 (min ~43:52–46:27), documento limpio de pasos.

---

## 12. Relación entre tipos de proyecto y organización de proyectos similares

### Marcar un tipo de proyecto como "dependiente" de otro

**Cuándo se usa:** cuando existen varios tipos de proyecto que en realidad pertenecen a una misma línea o iniciativa macro, pero que a lo largo de los años cambiaron de nombre por temas normativos (caso real de la capacitación: "PAT" → "PTEP" → "Iniciativas", que en realidad correspondían al mismo tema de transparencia).

**Ruta:** dentro del **Tipo de Proyecto**, en la sección de relación con otros tipos.

1. Se puede ver el listado de tipos de proyecto ya creados.
2. Marcar la opción **"Depende de"** y seleccionar el tipo de proyecto "macro" del cual depende este tipo.

Esto crea una relación de dependencia entre tipos, útil para dejar registrado que varios tipos corresponden al mismo tema aunque tengan nombres distintos por año.

### Error común — crear varios tipos de proyecto en vez de uno con categorías

Soporte de Almera identificó (sesión 3) un error de parametrización frecuente: crear **un Tipo de Proyecto distinto por cada variante** (ej. 5 tipos de proyecto para PAT, PTEP, Iniciativas, etc.), en vez de crear **un solo Tipo de Proyecto** (ej. "Transparencia") con un **campo adicional de categoría** que permita clasificar cada proyecto (PAT, PTEP, etc.) dentro del mismo tipo. Crear tipos separados implica tener varias "plantillas" distintas y dificulta consolidar la información.

**Si ya se cometió este error y hay proyectos con información registrada:** no se pueden simplemente cambiar de tipo si la parametrización (los campos) no es exactamente igual entre los tipos — ver sección 14.

### Agrupar visualmente proyectos de distintos tipos ya existentes

Si ya existen varios tipos de proyecto que se quieren ver agrupados sin necesidad de fusionarlos, hay dos alternativas:

1. **Un campo "agrupador"** dentro del tipo de proyecto, para clasificar internamente.
2. **Un Cuadro de Mando** (módulo de Cuadros de Mando / Balanced Scorecard) — se crea un tablero nuevo, se le van asociando los tipos/proyectos relevantes como componentes, y se pueden agrupar visualmente ahí. Al desplegar un componente se ve el avance de sus cronogramas, y se puede entrar directamente al proyecto desde ese tablero. **Esto requiere apoyo del área que administra Cuadros de Mando** — se recomienda solicitar una capacitación puntual de ese módulo si se va a usar para este fin.

**Nota:** si luego se elimina una subpestaña de agrupación dentro de un cuadro de mando, los proyectos **no desaparecen** — simplemente dejan de estar sub-agrupados y quedan visibles junto con los demás del tipo padre. La información en Proyectos tampoco se pierde: el histórico (ej. proyectos de años anteriores) sigue existiendo y se puede consultar ajustando el filtro de **Vigencia** (ver nota de filtro abajo).

### Filtro de Vigencia — cómo encontrar proyectos "perdidos"

Si un proyecto no aparece en el listado, puede deberse a que el filtro superior de **Vigencia** está limitando el rango de años mostrado. Solución: en el filtro de **Vigencia**, seleccionar **"Todas"** y hacer clic en **Filtrar**.

**Fuente:** transcripción sesión 1 (min ~14:59–18:34), sesión 3 (min ~14:29–36:47).

---

## 13. Integración con Plan Estratégico (Cuadros de Mando)

### La vinculación NO se hace desde Proyectos

Este fue un punto de confusión real en la capacitación: dentro de un proyecto no existe una opción directa para "asociarlo al plan estratégico". **La vinculación se hace al revés — desde el módulo de Cuadros de Mando (Balanced Scorecard/BSC):**

1. Ir a un **cuadro de mando / planeación estratégica** ya creado (o crear uno nuevo).
2. Desde ahí, habilitar la opción de **"Asociar proyectos"**.
3. Una vez habilitado, recién ahí se pueden vincular proyectos a ese cuadro de mando — no al revés.

Si un usuario no ve ninguna opción para asociar su proyecto al plan estratégico, es porque **todavía no existe ningún cuadro de mando que tenga habilitada esa asociación** para su proyecto.

### Advertencia importante — no asociar sin alinear con el área de Planeación

Soporte de Almera fue enfática en esto: **no se debe habilitar "Asociar proyectos" en un cuadro de mando ya existente sin coordinar primero con el área dueña de ese tablero.** Si se asocian proyectos sin alineación, esos proyectos les van a aparecer a los dueños del cuadro de mando dentro de su estructura ya construida, sin que ellos lo hayan vinculado — lo que puede **entorpecer** su planeación estratégica ya armada.

### Resultado una vez habilitado

Cuando la asociación está correctamente habilitada y alineada, el proyecto aparece reflejado en el tablero de mando correspondiente, permitiendo ver cómo la ejecución física del proyecto aporta a las metas estratégicas de la entidad.

**Fuente:** transcripción sesión 3 (min ~9:08–14:29).

---

## 14. Reglas del sistema — qué no se puede hacer directamente

Estas restricciones se confirmaron explícitamente en la capacitación (sesión 3) y son importantes porque **no tienen solución desde el usuario final** — deben escalarse a Soporte Almera.

### No se puede eliminar un Tipo de Proyecto ni un Proyecto que ya tenga registros

Una vez un Tipo de Proyecto o un Proyecto tiene **cualquier registro asociado** (así sea una sola actividad, incluso si luego se elimina esa actividad y queda "vacío"), el sistema **no permite eliminarlo** desde la interfaz. Hay que **solicitar la eliminación a Soporte Almera**, quienes lo hacen directamente en base de datos.

### No se puede cambiar el "Tipo" de un proyecto ya creado si la parametrización difiere

Desde la edición de un proyecto, el campo **"Tipo"** no se puede modificar libremente si el tipo de destino no tiene **exactamente los mismos campos** parametrizados que el tipo de origen — el sistema no deja hacer el cambio ("no deja cambiar"). Si se necesita mover un proyecto de un tipo a otro (por ejemplo, para consolidar varios tipos en uno solo — ver sección 12):

1. Verificar y garantizar que el tipo de destino tenga **exactamente la misma parametrización** (mismos campos) que el tipo de origen, para no perder información.
2. Solicitar el movimiento a **Soporte Almera**, indicando qué proyectos deben trasladarse y a qué tipo.

**Fuente:** transcripción sesión 3 (min ~16:09–19:00, ~23:12–23:53).

---

## 15. Temas pendientes de validar con soporte Almera

Estos son puntos que quedaron **sin resolver o sin confirmar del todo** en las tres sesiones de capacitación de Proyectos. El asistente debe avisar explícitamente que esto no está confirmado si alguien pregunta por estos temas.

### 1. Notificación automática al finalizar/cerrar un proyecto

**Contexto:** Sergio preguntó explícitamente cómo configurar que, al momento de finalizar/cerrar un proyecto (última transición del flujo), el sistema notifique automáticamente por correo a la Dirección de Estrategia y Planeación y a varios miembros de un equipo, sin que alguien tenga que enviarlo manualmente.

**Estado:** Carlos indicó que **sí es posible hacerlo**, pero que necesitaba **validar cómo se configura exactamente** esa notificación de cierre — no se llegó a demostrar en vivo ni se confirmó el paso a paso en ninguna de las tres sesiones.

**Fuente:** transcripción sesión 2, min ~27:41–28:47.

### 2. Pregunta de Planes de Mejora colada en la capacitación de Proyectos (no resuelta, pero no es de este módulo)

**Contexto:** Luz Mery aprovechó una sesión de Proyectos para preguntar por una pestaña de "seguimiento de control" que no se le habilitaba en el módulo de **Planes de Mejora** (no en Proyectos). Carlos no tuvo la respuesta en el momento y pidió el correo del equipo para hacer seguimiento aparte.

**Estado:** sin resolver a la fecha de estas sesiones. **Aclaración:** esta duda pertenece al módulo de Planes de Mejora, no al de Proyectos — se documenta aquí únicamente porque surgió en estas grabaciones, pero si un usuario pregunta por "seguimiento de control" refiriéndose a Planes de Mejora, esta skill de Proyectos no es la fuente correcta.

**Fuente:** transcripción sesión 2, min ~50:34–54:57.

---

## Preguntas frecuentes puntuales (por correo)

Este espacio se va llenando con dudas específicas sobre Proyectos que lleguen por correo y ya estén resueltas, siguiendo el mismo formato que el resto de la skill:

```markdown
### <Pregunta o tema del correo>

**Cuándo se usa:** <contexto>

**Respuesta / pasos:** ...

**Notas / advertencias:** ...

**Fuente:** Correo de <remitente>, <fecha>, asunto "<asunto>".
```

*(Todavía no hay contenido aquí — pendiente de que se compartan correos de seguimiento, incluyendo la respuesta de soporte al punto 1 de la sección de pendientes cuando llegue.)*
