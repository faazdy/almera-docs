# Almera — Módulo de Indicadores (guía de referencia completa)

> Este documento reúne todo el conocimiento operativo del módulo de Indicadores de Almera: procedimientos paso a paso, reglas del sistema y dudas que quedaron abiertas en la capacitación con soporte. Fue construido a partir de documentación limpia, una guía interna y la transcripción completa de una capacitación con soporte de Almera (25 jun 2026).

**Instrucciones para la IA que use este documento:**
- Responde siempre con el procedimiento exacto documentado aquí, paso a paso, antes de sugerir cualquier otra cosa.
- No inventes pasos, botones o menús que no estén mencionados en este documento.
- Si la pregunta no está cubierta aquí, dilo explícitamente — no improvises.
- Revisa siempre la sección final **"Temas pendientes de validar"** antes de responder sobre semaforización o notificaciones — hay comportamientos del sistema que quedaron identificados como fallas o dudas sin confirmar. No los presentes como si funcionaran correctamente.

---

## Índice

1. Conceptos básicos (ficha técnica, agrupadores, asociación a subproceso)
2. Crear campos adicionales en la ficha técnica
3. Actualizar opciones (ítems) de un campo existente
4. Configurar unidades de medida
5. Metas y semaforización
6. Privilegios y responsables
7. Control de fechas del indicador
8. Notificaciones y alertas de atraso
9. Clasificar indicadores y generar reportes filtrados
10. Preguntas puntuales por correo
11. Temas pendientes de validar con soporte Almera

---

## Conceptos básicos — Módulo Indicadores (Almera)

### Ficha técnica: agrupadores "Definición" vs. "Información adicional"

Todo indicador se registra en una **ficha técnica** compuesta de campos (clase, objetivo, línea base, dominio, etc.). Cada campo pertenece a uno de dos **agrupadores**, y esto determina en qué pestaña aparece al abrir la ficha de un indicador:

- **Definición:** el campo aparece en la primera pestaña/hoja de la ficha técnica (la que se ve de entrada).
- **Información adicional:** el campo queda en una pestaña aparte llamada "Información adicional".

> Es una decisión de organización interna: algunos clientes reparten los campos entre las dos pestañas, otros prefieren tener todos los campos en "Definición" para no dividir la información. Ninguna de las dos formas es "la correcta" — se define según cómo la organización quiera navegar la ficha.

### Asociación obligatoria a un subproceso

Todo indicador **debe crearse asociado a un proceso o subproceso** — no hay forma de crearlo "suelto". Actualmente **no existe una función de carpetas/subcarpetas** dentro de un subproceso para separar visualmente grupos de indicadores (por ejemplo, "normativos" vs. "de gestión propia del proceso"). El listado de indicadores de un subproceso siempre se muestra plano. Para lograr algo parecido a una separación, ver `09-clasificacion-y-reportes.md`.

### Clasificación automática por módulo de origen

Dentro de la ficha, en la sección de administración, existe un listado de "clase" que **no se puede editar manualmente**: refleja el módulo del sistema desde el cual se generó el indicador (por ejemplo, si el indicador se creó desde el módulo de Riesgos, ahí va a aparecer "Riesgos"; si se creó desde un proceso, aparece como "Proceso"). El sistema lo asigna automáticamente según el origen — no es un campo de negocio que la organización configure.

> No confundir esta "clase de origen" (automática, no editable) con el campo **Clase** de la ficha técnica (editable, sirve para categorizar el tipo de indicador — ver `09-clasificacion-y-reportes.md`).

### Permisos para ver secciones de administración

El acceso a algunas secciones de `Admin → Indicadores` (por ejemplo, "Categorías y tipos de indicador") es en sí mismo un privilegio que debe asignarse usuario por usuario. Si un administrador del módulo no ve alguna de estas opciones en su panel, probablemente le falta ese permiso — hay que solicitarlo a soporte o a quien administre los accesos.

**Fuente:** transcripción cruda de la capacitación de Indicadores, 25 jun 2026 (min ~1:25–1:31, ~1:39, ~2:29).

---

## Crear campos adicionales en la ficha técnica

**Cuándo se usa:** cuando se necesita personalizar la información que se solicita al crear un indicador (agregar una categoría o dato propio de la organización que no existe todavía).

**Ruta:** `Admin → Indicadores → Categorías y tipos de indicador → Indicador → Campos adicionales`

### Pasos

1. Ingresar al componente **Indicador** dentro de `Admin → Indicadores → Categorías y tipos de indicador`.
2. Abrir la pestaña **Campos adicionales**.
3. Seleccionar **Nuevo campo**.
4. Configurar el nuevo campo:
   - **Tipo de campo** — opciones disponibles:
     - Texto (una sola línea o múltiples líneas, según el tamaño que se necesite).
     - Fecha (selector de calendario).
     - Numérico.
     - Lista de selección única.
     - Lista de selección múltiple.
   - **Código o consecutivo**, respetando el orden existente (el siguiente número disponible).
   - **Nombre** del campo (el "alias" es opcional, no es obligatorio llenarlo).
   - **Agrupador**: elegir **Definición** o **Información adicional** — ver la diferencia en `01-conceptos-basicos.md`.
5. Indicar si el campo es **obligatorio**.
6. Presionar **Grabar**.

### Si el campo es de tipo selección (única o múltiple)

Después de grabar el campo, se habilitan al pie las opciones **Nuevo ítem** y **Múltiple**:
- **Nuevo ítem**: agrega las opciones de respuesta una por una (orden, código, nombre).
- **Múltiple**: permite escribir varias opciones de una sola vez (una por línea, con Enter) y grabarlas todas juntas — es más rápido cuando se necesitan varias opciones.

### Notas / advertencias

- Un campo de tipo texto no necesita crear opciones (es de respuesta abierta).
- Para ver el campo nuevo reflejado en una ficha ya abierta, hay que refrescar la página.

**Fuente:** `docs-indicadores.md` + HTML de documentación interna + transcripción cruda (min ~1:25–1:39).

---

## Actualizar opciones (ítems) de un campo existente

**Cuándo se usa:** para agregar, inactivar o entender por qué no se puede eliminar una opción de un campo de selección (única o múltiple) que ya existe en la ficha técnica.

**Ruta:** `Admin → Indicadores → Categorías y tipos de indicador → Indicador → Campos adicionales`

### Agregar una opción nueva

1. Desde **Campos adicionales**, ubicar el campo que se desea modificar (por ejemplo, "Clase").
2. Hacer clic sobre el nombre del campo para ver sus opciones actuales.
3. Seleccionar **Nuevo ítem**.
4. Completar: **orden**, **código**, **nombre**.
5. Si aplica, asignar un **peso** para que el sistema calcule automáticamente una calificación a partir de esa respuesta (ejemplo: "Cumple" = peso 1, "No cumple" = peso 0).
6. Guardar.

### Eliminar o inactivar una opción existente

- **Si la opción tiene el ícono de papelera habilitado a la derecha**, significa que ningún indicador la está usando actualmente — se puede eliminar sin problema.
- **Si no tiene el ícono de papelera**, quiere decir que ya hay indicadores usando esa opción — el sistema no permite eliminarla. La alternativa es **inactivarla** (quitarle el check/chulito de activa) para que deje de ofrecerse como opción nueva, sin afectar los indicadores que ya la tienen asignada.

**Fuente:** `docs-indicadores.md` + transcripción cruda (min ~1:49–1:51).

---

## Configuración de unidades de medida

**Cuándo se usa:** para definir cómo se van a visualizar los valores de un indicador (porcentaje, pesos colombianos, tasas, cantidades, horas, etc.).

**Ruta:** `Admin → Indicadores → Unidades y categorías`

### Pasos

1. Hacer clic en **Adicionar unidad** (esquina superior derecha).
2. Asignar el **nombre** de la unidad.
3. Configurar el **formato** usando la variable `{valor}`. Por defecto aparece como `{0}` — se reemplaza por `{valor}` y se le puede agregar cualquier texto o sigla alrededor.

#### Ejemplos

| Nombre | Formato | Resultado |
|---|---|---|
| Tasa | `{valor} TZ` | `4.5 TZ` |
| COP | `$ {valor}` | `$ 1.500.000` |
| Porcentaje | (formato ya trae el símbolo %) | `85%` |

4. Definir la cantidad de **decimales**.
5. Presionar **Grabar**.

### Notas / advertencias

- El texto/sigla que se agregue en el formato aparece pegado al resultado final del indicador — útil para que quede claro de un vistazo qué tipo de unidad es.
- Después de crear una unidad, hay que refrescar la ficha técnica para que aparezca disponible en el selector.

**Fuente:** `docs-indicadores.md` + transcripción cruda (min ~1:37–1:39).

---

## Gestión de metas y semaforización

### Meta única vs. Meta periódica — por qué importa la diferencia

**Meta única:** se define un solo valor de meta para el indicador (ej. 90%). Si en algún momento esa meta cambia (ej. sube a 95% el año siguiente), **el sistema recalcula todo el histórico hacia atrás** con la nueva meta — es decir, modifica cómo se ven las mediciones ya registradas.

**Meta periódica (recomendada):** se define una meta para cada período (enero, febrero, marzo...). Si la meta cambia en el futuro, el histórico de los períodos ya registrados **se conserva tal cual estaba** — el sistema no lo recalcula.

> **Recomendación de Almera:** usar siempre **Meta periódica** + **Semáforo dinámico**. Si se usa Meta única, lo recomendado es **Semáforo lineal**.

### Cómo se relaciona la meta con el semáforo

El sistema toma el valor de la meta como el **100%** para efectos de cálculo porcentual. Es decir, si la meta es 90 y el resultado real es 90, el sistema lo muestra como 100% de cumplimiento — no como "90".

### Configurar meta periódica con semáforo dinámico

1. En la ficha técnica, en el tipo de meta, seleccionar **Periódica**.
2. Presionar **Definir metas**.
3. Registrar la meta correspondiente para cada período (mes a mes, si el indicador es mensual).
4. Configurar los rangos del semáforo (rojo / amarillo / verde) según el porcentaje de cumplimiento sobre la meta.

### Migrar un indicador de meta única a meta periódica sin perder el histórico

Si un indicador que ya se venía midiendo con **meta única** se cambia a **meta periódica**, hay que tener cuidado: al definir las metas periódicas, **hay que volver a ingresar, período por período, la meta que estuvo vigente en ese momento** (por ejemplo, si en 2025 la meta era 90%, hay que dejar 90% en esos meses de 2025), y no simplemente dejar la meta nueva aplicada a todo el histórico. Si no se hace así, el sistema sí modifica las mediciones ya registradas.

### Notas / advertencias

- Los indicadores pueden tener más de una variable en su fórmula (no solo numerador/denominador) — se van agregando las variables que se necesiten.
- **Sin confirmar todavía:** existe una necesidad reportada de limitar el resultado mostrado al 100% aunque el cálculo real supere ese valor (por ejemplo, que un resultado de 150% se muestre como "cumplido" en vez de "150%"). Esto surgió por una observación de auditoría. Quedó como tarea pendiente de Carlos (soporte Almera) validar si existe un parámetro global para activarlo — no se confirmó una solución en esta sesión. Ver `11-pendientes-validar.md`.

**Fuente:** `docs-indicadores.md` + HTML de documentación interna + transcripción cruda (min ~1:51–2:04, ~2:21–2:31).

---

## Asignación de privilegios y responsables

### Dos formas distintas de asignar "quién puede qué" sobre un indicador

**"Información adicional" (campo de responsable dentro de la ficha):**
- Solo permite asignar **cargos** (roles), no personas específicas.
- Solo admite **un cargo por campo** — no está pensado para múltiples personas.
- Cualquier usuario que tenga ese cargo va a poder actuar sobre el indicador.

**Pestaña "Privilegios" (dentro del indicador → Editar → Privilegios → Administrar):**
- Permite asignar permisos a **usuarios específicos** (por nombre), no solo por cargo.
- Se pueden agregar **varias personas**, cada una con sus propias acciones habilitadas.
- Las acciones disponibles son:
  - **Consultar**
  - **Agregar medición**
  - **Hacer análisis**

### Pasos para asignar privilegios por usuario

1. Dentro del indicador, ir a **Editar → Privilegios → Administrar**.
2. Buscar el usuario específico.
3. Marcar las acciones que le corresponden (Consultar / Agregar medición / Hacer análisis).
4. Presionar **Agregar** para guardar la asignación.
5. Repetir para cada usuario adicional que necesite acceso a ese indicador puntual.

### Notas / advertencias

- Si se necesita que **más de una persona** pueda cargar mediciones de un mismo indicador (por ejemplo, un titular y un suplente), la vía correcta es la pestaña de **Privilegios**, no el campo de responsable de "Información adicional".
- El **responsable** (definido por cargo o por privilegios) es también quien recibe las notificaciones automáticas de atraso — ver `08-notificaciones-alertas.md`.
- Si la pestaña de "Privilegios" no aparece habilitada para un usuario administrador, puede ser un tema de permisos del sistema — solicitar la validación a soporte (mismo caso que ocurre con permisos en el módulo de Documentos).

**Fuente:** `docs-indicadores.md` + transcripción cruda (min ~1:39–1:41, ~1:59, ~2:44).

---

## Control de fechas del indicador

**Cuándo se usa:** para definir desde cuándo y hasta cuándo un indicador acepta mediciones.

### Los dos campos de fecha

| Campo | Qué controla |
|---|---|
| **Fecha válido** | Cuándo **inicia** el reporte de ese indicador. A partir de esta fecha el sistema empieza a aceptar mediciones. |
| **Fecha de corte** | Cuándo **termina** la vigencia del indicador. A partir de esta fecha el sistema hace un cierre automático: el responsable ya no puede seguir registrando mediciones. |

### Pasos

1. Configurar la **Fecha válido** (inicio de vigencia).
2. Configurar la **Fecha de corte** (fin de vigencia / bloqueo).
3. Si el indicador puede tener períodos sin información, habilitar **Permitir períodos sin medición**.

### "Permitir períodos sin medición" — por qué es importante

Por defecto, si una medición queda en cero, el sistema **no muestra ese mes** en las tablas de resultados (lo omite, no lo muestra como cero). Si se activa esta opción, el sistema sí muestra el mes, con el valor en cero, en vez de omitirlo. Esto es clave para no perder la traza de meses realmente sin información.

### Caso de uso: indicadores de vigencia anual (ej. Plan Operativo Anual)

Si un indicador se mide solo durante un año específico (por ejemplo, un POA) y se quiere que después de una fecha límite (ej. 20 de enero del año siguiente) ya no se pueda seguir cargando información, eso se controla con la **Fecha de corte** — no con la Fecha válido. La Fecha válido solo determina cuándo *empieza* a poder reportarse.

### Notas / advertencias

- Al llegar la fecha de corte, el bloqueo es automático — no hace falta ninguna acción manual adicional.
- Si un indicador quedó con fechas mal configuradas y sigue midiéndose año tras año sin corte (por ejemplo, indicadores anuales que la gente sigue reportando indefinidamente porque nunca se les puso fecha de corte), la corrección es simplemente editar esas dos fechas en la ficha del indicador.

**Fuente:** `docs-indicadores.md` + transcripción cruda (min ~2:17–2:22).

---

## Notificaciones y alertas de atraso

**Cuándo se usa:** para entender cómo funciona (en teoría) el sistema de avisos automáticos cuando un indicador no ha sido medido a tiempo.

### Cómo está diseñado el sistema de alertas

- El sistema **no envía una alerta individual apenas se vence un indicador**. En su lugar, hace un barrido **semanal, todos los lunes**, y le envía al usuario responsable un solo correo consolidado con todos los indicadores que tiene vencidos o atrasados.
- La notificación llega **únicamente al responsable del indicador** (la persona asignada como responsable, ya sea por cargo o por privilegios — ver `06-privilegios-responsables.md`). No hay una opción de "copia" automática para un coordinador o supervisor que quiera enterarse de todos los atrasos de su equipo — para recibir esas alertas, esa persona tendría que figurar como responsable en cada uno de esos indicadores.
- Existe la posibilidad de que un administrador del sistema haga un **envío masivo manual** de la notificación de atraso a todos los usuarios con indicadores vencidos, como una acción puntual (no es automática, alguien la dispara).

### Notas / advertencias — esto no está funcionando de forma confirmada

Durante la capacitación se detectó que **las alertas semanales no estaban llegando** a varios usuarios que sí tenían indicadores atrasados desde meses atrás (algunos desde febrero). Se validó con al menos 3 personas y ninguna había recibido la notificación. Carlos (soporte Almera) quedó con la tarea de investigar qué estaba pasando — posibles causas mencionadas pero **sin confirmar**:
- Que el correo asociado al usuario en el sistema esté mal registrado.
- Que el usuario no esté correctamente marcado como "responsable" del indicador (la notificación solo llega a quien tiene ese rol).

**No presentes las alertas semanales como algo que funciona de forma confiable** a menos que el usuario confirme que ya fue validado y corregido por soporte. Ver el detalle en `11-pendientes-validar.md`.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~2:35–2:56).

---

## Clasificar indicadores y generar reportes filtrados

**Cuándo se usa:** cuando se necesita separar indicadores por tipo (por ejemplo, "normativos" que dependen de terceros vs. "de gestión" propios del proceso) para no evaluar el desempeño del proceso mezclando ambos tipos.

### No existe una función de carpetas — la alternativa es un campo + filtro

Como se explica en `01-conceptos-basicos.md`, Almera no tiene una función de carpetas/subcarpetas dentro de un subproceso para separar visualmente los indicadores. La forma de lograr algo equivalente es:

1. Usar (o crear) un **campo de selección** en la ficha técnica que sirva como etiqueta de clasificación — por ejemplo, el campo **Clase**, agregándole ítems como "Indicador normativo" e "Indicador de gestión" (ver `03-actualizar-opciones-campo.md` para agregar ítems a un campo existente).
2. Al crear o editar cada indicador, seleccionar la etiqueta que le corresponde.
3. A la hora de generar el reporte/listado de indicadores, **filtrar por ese campo** antes de exportar — así se puede sacar, por ejemplo, únicamente el reporte de los indicadores "de gestión" sin que los "normativos" afecten el cálculo de cumplimiento del proceso.

### Reportes que sí existen vs. los que no

- El sistema permite **filtrar y exportar** el listado de indicadores según los campos disponibles (incluida la clasificación que se cree, como la del punto anterior).
- **No existe (a la fecha de esta capacitación) un reporte consolidado automático** que calcule, por ejemplo, el promedio de cumplimiento trimestral o semestral de un indicador a partir de sus mediciones mensuales. Para obtener ese tipo de consolidado hoy en día hay que descargar todos los meses y promediarlos manualmente.
- Si se necesita ese tipo de reporte de forma recurrente, la recomendación de soporte Almera es **escribir una solicitud formal a soporte** para que evalúen construir un reporte específico — no es algo que se resuelva por configuración desde la interfaz.

**Fuente:** transcripción cruda de la capacitación, 25 jun 2026 (min ~2:04–2:15, ~2:22–2:24).

---

## Preguntas frecuentes puntuales (por correo)

Este archivo se va llenando con dudas específicas sobre Indicadores que lleguen por correo y ya estén resueltas. Mismo formato que el resto de la skill:

```markdown
### <Pregunta o tema del correo>

**Cuándo se usa:** <contexto>

**Respuesta / pasos:** ...

**Notas / advertencias:** ...

**Fuente:** Correo de <remitente>, <fecha>, asunto "<asunto>".
```

*(Todavía no hay contenido aquí — pendiente de que se compartan los correos.)*

---

## Temas pendientes de validar con soporte Almera

Estos son dudas y fallas detectadas que quedaron **abiertas** en la capacitación de Indicadores del 25 de junio de 2026. Carlos (soporte Almera) se comprometió a investigarlas, pero en esta grabación no quedó una respuesta ni una corrección confirmada. El asistente debe avisar explícitamente que esto no está resuelto si alguien pregunta por estos temas — no dar la respuesta como un hecho ni asumir que ya se corrigió.

### 1. Los resultados pueden superar el 100% de cumplimiento

**Contexto:** cuando el resultado real de un indicador supera su meta (por ejemplo, meta = 4 reuniones, se hicieron 5), el sistema muestra el cumplimiento como 125% en vez de mostrarlo simplemente como "cumplido" (tope en 100%). Esto generó observaciones en auditorías internas de la organización, que consideran ilógico un cumplimiento mayor a 100%.

**Estado:** Carlos dijo que existe un parámetro para esto pero necesitaba ubicarlo y validar que aplicara a **todos** los indicadores (no configurarlo uno por uno). Quedó como tarea pendiente de su parte — sin confirmar si ya se activó o cómo se activa.

**Fuente:** transcripción cruda, min ~2:00–2:01, ~2:21, ~2:30–2:31.

### 2. Las notificaciones semanales de atraso no estaban llegando

**Contexto:** el sistema debería enviar, todos los lunes, un correo al responsable de cada indicador atrasado. Durante la sesión se validó en vivo con varios usuarios (con indicadores atrasados desde febrero) y **ninguno había recibido la notificación**.

**Estado:** Carlos quedó con la tarea de investigar la causa — posibles hipótesis sin confirmar: correo mal registrado en el sistema, o el usuario no estaba correctamente marcado como "responsable" del indicador. No hay confirmación de que esto ya esté corregido.

**Fuente:** transcripción cruda, min ~2:35–2:56.

### 3. Recuperación de un indicador eliminado por error del todo (no solo desvinculado de un proceso)

**Contexto:** si por error se elimina un indicador completo del sistema (en vez de solo quitarlo/desvincularlo de un proceso específico, dejándolo activo en otros), **los administradores del módulo no pueden recuperarlo por sí mismos**.

**Estado:** esto no es una falla ni algo pendiente de validar — es una limitación confirmada: solo el equipo de soporte de Almera ("usuarios sistema") puede restaurar un indicador eliminado por completo. Se documenta aquí para que quede claro que ante ese error hay que escribir a soporte directamente, no buscar una opción dentro del sistema.

**Fuente:** transcripción cruda, min ~2:32–2:34.