# Insumos pendientes — diagramas de flujo

La skill no está completa hasta que estos archivos estén en esta carpeta `assets/`.

## Obligatorios

| Archivo | Qué es | Estado |
|---|---|---|
| `paleta-bizagi.md` | Colores por tipo de elemento del estándar de Bizagi. | 🟡 Actividad y decisión: calibradas por muestreo de píxeles (alta confianza). Evento inicial/final: **dos exports reales dan colores distintos** (ver hallazgo abajo) — hay un default, pero no es universal. Subproceso, evento intermedio, carril y banda de fase siguen provisionales. |
| `plantilla.mmd` | Esqueleto Mermaid con `classDef` calibrado a la paleta. | 🟢 Actualizado con los hex default vigentes + técnica de carril único (ver hallazgo abajo) |
| `diagrama-referencia-ejemplo/` | Ejemplo trabajado (PQRS) como referencia temporal. | 🟡 Sigue con la paleta vieja — falta re-generarlo con los colores calibrados (ver `ejemplos-reales/`) |
| `ejemplos-reales/diagrama-de-flujo-bizaggi.png` | Export **real** de un procedimiento ya diagramado en Bizagi Modeler ("Retiro parcial de cesantías"). | 🟢 Recibido y usado para calibrar la paleta (actividad/decisión/evInicio/evFin, este último ahora documentado como variante alterna) |
| `ejemplos-reales/ejemplo-de-resultados-esperados-skill.pdf` | Caso resuelto de referencia: mismo procedimiento, diagrama general + 4 variaciones. | 🟡 Recibido — ver nota abajo sobre estilo de validación, diverge de `03-validacion-por-colores.md` |
| `ejemplos-reales/actividades-para-diagrama.xlsx` | Insumo crudo real (67 actividades, 5 fases, texto sin estructurar) para probar la skill de punta a punta. | 🟢 Recibido — pendiente usarlo como caso de prueba |
| `test-actividades-diagrama.pdf` | Procedimiento real de prueba: "Inducción a nuevos funcionarios de Servicio al Cliente" (P02-AU). | 🟢 Usado en `pruebas/induccion-nuevos-funcionarios/` — primera corrida completa de la skill de punta a punta |
| Imagen del diagrama real de "Inducción..." | Export real de Bizagi de ese mismo procedimiento, compartido **inline en el chat** (sin archivo guardado). | 🟡 Usado para corregir carriles y paleta de evInicio/evFin (ver hallazgos abajo) — si se sube como archivo a `ejemplos-reales/` se puede muestrear por píxel en vez de a ojo |

## v6 — corregido contra el diagrama real de "Documentación de Software"

El usuario compartió el diagrama real (export de Bizagi) de este mismo procedimiento. Confirma:
4 carriles correctos, secuencia de cruces correcta, y el paso 4 correctamente NO modelado como
decisión (la fuente tampoco lo hace — mismo criterio que ya se seguía). Corrige un error: los
pasos 8 y 12 estaban partidos en dos cajas cada uno (8.1/8.2, 12.1/12.2) por precaución de
longitud, pero el diagrama real usa una sola caja para cada uno — la frase de acción principal
cabe sobrada en 100 caracteres; el resto (nombre de formato, texto de apoyo) se descarta como
referencia adicional, igual que en el resto de actividades. **Lección: no partir un paso en dos
solo porque el párrafo completo de la fuente es largo — split solo si la frase de acción en sí
(ya recortada de referencias/formatos) no cabe en 100 caracteres.** `documentacion-software.mmd`,
`.html` y `.bpmn` vuelven a 12 cajas, 1:1 con las 12 actividades fuente.

## Export nativo a Bizagi — DESCARTADO, confirmado

Se probó si la skill puede exportar a un formato que Bizagi Modeler importe directamente, en vez
de solo producir una imagen con estilo similar. Resultado:

- Se escribió a mano un archivo **BPMN 2.0 XML** (`pruebas/documentacion-software/documentacion-software.bpmn`)
  — el estándar abierto de la OMG que Bizagi anuncia soportar para import. XML bien formado y
  validado internamente (referencias `sourceRef`/`targetRef`/`flowNodeRef` cruzadas, 14 tasks, 4
  carriles, 15 flujos, 2 anotaciones) antes de entregarlo.
- **El usuario lo probó en Bizagi Modeler real: no lo acepta.** Bizagi Modeler solo importa su
  formato nativo `.bpm` — BPMN 2.0 XML estándar no sirvió, al menos en la instalación que se
  probó.
- `.bpm` es un formato **propietario sin documentación pública conocida** por esta skill. No se
  intentó fabricar uno a ciegas — un archivo inventado sin conocer su esquema real casi con
  seguridad sale corrupto y no abre, lo cual es peor que no intentarlo.
- **Conclusión: la skill no exporta a un formato nativo de Bizagi.** Se mantiene el alcance
  original de `SKILL.md`: producir diagramas con estilo visual fiel a Bizagi (Mermaid → PDF/JPG/PNG
  o artifact), no un proyecto editable dentro de Bizagi Modeler. Si en el futuro se consigue un
  `.bpm` real exportado desde Bizagi (no solo el PNG/PDF de export visual que ya se tiene), se
  podría inspeccionar su estructura interna y reconsiderar — pero eso es un insumo nuevo, no algo
  para intentar de nuevo a ciegas.

## Opcional pero útil

| Archivo | Qué es |
|---|---|
| `diagrama-referencia.bpm` | El archivo Bizagi original, para leer colores/estilos exactos. |

## Formato sugerido para `paleta-bizagi.md`

```markdown
# Paleta Bizagi Modeler — repositorio de procedimientos

| Elemento | Relleno (hex) | Borde (hex) | Texto (hex) |
|---|---|---|---|
| Evento inicial | #xxxxxx | #xxxxxx | #xxxxxx |
| Evento final | #xxxxxx | #xxxxxx | #xxxxxx |
| Actividad | #xxxxxx | #xxxxxx | #xxxxxx |
| Decisión (compuerta) | #xxxxxx | #xxxxxx | #xxxxxx |
| Subproceso | #xxxxxx | #xxxxxx | #xxxxxx |
| Carril (lane) — encabezado | #xxxxxx | #xxxxxx | #xxxxxx |
| Fase — banda | #xxxxxx | #xxxxxx | #xxxxxx |

## Marcas de validación (independientes del relleno)
| Estado | Color |
|---|---|
| Verde | #xxxxxx |
| Amarillo | #xxxxxx |
| Rojo | #xxxxxx |
```

## Decisión pendiente — estilo de validación por colores

`ejemplos-reales/ejemplo-de-resultados-esperados-skill.pdf` es un caso resuelto completo del
mismo procedimiento del PNG real. Confirma la estructura de
`../references/04-variaciones-de-procedimiento.md` (general con carriles + un diagrama por
variación, sin carriles), pero su forma de mostrar la validación **no coincide** con
`../references/03-validacion-por-colores.md`:

- La referencia actual pide marcar **cada** paso con verde/amarillo/rojo + una tabla aparte.
- El PDF de ejemplo solo cuelga una nota punteada amarilla o roja junto al paso puntual que
  tiene un problema (sin marcar los pasos correctos, sin tabla separada), y usa verde/rojo
  únicamente en los eventos de inicio/fin (trámite completo vs. fin por negativa).

- [ ] Decidir cuál es el estilo real que debe seguir la skill: ¿el PDF manda como ejemplo de
  estilo esperado y hay que reescribir `03-validacion-por-colores.md`, o el PDF es solo un
  boceto y se mantiene la regla actual (marca en cada nodo + tabla)?

## Hallazgos de la primera corrida completa (procedimiento "Inducción...")

Prueba end-to-end en `pruebas/induccion-nuevos-funcionarios/` (fuente: `test-actividades-diagrama.pdf`,
10 actividades reales, 2 carriles, sin variaciones). El usuario compartió el diagrama real de ese
mismo procedimiento y confirmó tres cosas:

- **Confirmado — límite de 100 caracteres y sin paréntesis se mantiene tal cual está en
  `02-reglas-de-diagramacion.md`**, aunque el diagrama real de referencia no lo respeta (usa cajas
  largas con paréntesis). El diagrama real no es el estándar a copiar en ese punto.
- **Corregido — un carril es SIEMPRE un solo clúster**, aunque el flujo lo abandone y vuelva a él
  (ej. "Profesional de Capacitación" hace los pasos 1-8, se lo pasa a "Supervisor PAU" en el paso 9,
  y vuelve a "Profesional de Capacitación" en 10-12). La v1 de la prueba partió esto en dos subgraphs
  con el mismo nombre (workaround visual, no un carril real). La técnica correcta — ya aplicada en
  `plantilla.mmd` — es declarar cada nodo una vez fuera de cualquier subgraph, y dentro del subgraph
  del carril solo referenciar su id.
- **Confirmado — evInicio/evFin varían entre exports reales de Bizagi**, no hay un color único
  organización-wide (ver fila de `paleta-bizagi.md` arriba). Si hay un export real del procedimiento
  específico que se va a diagramar, usar SUS colores; si no, usar el default de `paleta-bizagi.md`.

- **Corregido — cruce de carril con conector numerado en vez de flecha larga.** El usuario reportó
  que, al cruzar de carril y volver, la flecha se leía como si apuntara al carril completo y no a
  la actividad puntual (mismo problema con las notas de validación). Se resolvió reutilizando el
  "conector numerado" ya visto en el export de cesantías (①/②: un círculo en el punto de salida,
  otro igual en el punto de entrada, sin línea larga entre ambos) y agregando el número de paso al
  texto de cada nota de validación. Ya documentado como regla en `02-reglas-de-diagramacion.md` y
  como ejemplo en `plantilla.mmd`.

- **Agregado — cada actividad numerada con el número de la fuente, no una renumeración propia.**
  El usuario pidió enumerar las actividades para mejorar la traza. Se usó el número de la tabla del
  PDF original (no 1-12 secuencial): los pasos partidos en dos llevan sufijo decimal ("3.1"/"3.2",
  "6.1"/"6.2"). Esto también corrigió una inconsistencia que había quedado en las notas de
  validación del hallazgo anterior (decían "Paso 8"/"Paso 5"/"Paso 9" según mi numeración interna
  1-12, que no correspondía a ninguna fila real del PDF — ahora dicen "Paso 6"/"Paso 4"/"Paso 7").
  Ya documentado como regla en `02-reglas-de-diagramacion.md` (numeración de actividades) y como
  ejemplo en `plantilla.mmd`.

Sigue sin probarse (no se pudo verificar en esta sesión de Claude Code local):

- [ ] El título de "pool" (nombre completo del procedimiento, vertical, a la izquierda de los
  carriles) como subgraph anidado en Mermaid — se dejó como encabezado de página en vez de
  arriesgar un anidado sin poder renderizarlo.
- [ ] El layout serpenteado en zigzag del diagrama real (manual, hecho a mano en Bizagi) no lo
  replica el layout automático de Mermaid — hay que aceptar que el resultado es funcionalmente
  equivalente, no idéntico en posición.

## Segunda corrida completa (procedimiento "Documentación de Software")

Prueba end-to-end en `pruebas/documentacion-software/` (fuente: PDF "Procedimiento de
Documentación de Software", P06-TSI V2.0-2022, Capital Salud EPS-S — 12 actividades, 4 carriles).
El usuario pidió avanzar directo, sin repetir las preguntas ya resueltas en la primera corrida —
se aplicaron todas las reglas ya corregidas desde el primer intento (numeración de fuente, carril
único, conectores, notas con número de paso), sin volver a fallar en ninguna.

Esta corrida es un stress-test más duro que la primera: el flujo entra y sale del mismo carril
**tres veces no consecutivas** (Ing. Requerimientos, Ing. Programador y Coordinador de Desarrollo
se visitan cada uno dos veces). Esto obligó a precisar la regla de conectores:

- **Precisado — el conector es solo para RE-ENTRADAS a un carril ya visitado, no para todo cruce
  de carril.** La primera vez que el flujo entra a un carril (aunque sea un cruce), una flecha
  directa está bien — así lo hace el propio export real de Bizagi para los cruces "hacia
  adelante". El conector numerado se reserva para cuando el flujo vuelve a un carril que ya había
  usado antes, que es el caso que de verdad se presta a confusión. Esta corrida usó 3 pares (①②③),
  uno por cada retorno; los otros 3 cruces (primera visita a cada carril) van con flecha directa.
  Vale la pena promover esta precisión a `02-reglas-de-diagramacion.md` si se confirma en una
  tercera prueba.
- Mismo patrón que la primera corrida para el paso con validación implícita sin rama documentada
  ("Determinar si... cumple...", paso 4): se dejó como actividad plana con nota 🔴, no como
  decisión, para no inventar una rama "No" que la fuente no define.

## Reconstrucción v2 de "Documentación de Software" — agrupación por fase

El usuario compartió un HTML de referencia (otro procedimiento no relacionado, 67 actividades/5
fases) que organiza el diagrama por FASE con transición punteada entre fases, y pidió aplicar esa
idea a la prueba de "Documentación de Software" porque la v1 (agrupada por carril, con conectores
①②③) se sentía confusa — no se veía la continuidad del proceso de un vistazo.

- **Agregado — criterio "fase vs. carril" como agrupación primaria de la skill**, no solo para
  esta prueba. Mermaid no anida los dos, así que hay que elegir uno. Agrupar por fase evita
  conectores casi siempre (las fases no suelen revisitarse, aunque los responsables sí); se deja el
  responsable como segunda línea dentro de cada caja en vez de como carril. Documentado en
  `02-reglas-de-diagramacion.md` ("Agrupación primaria: ¿fase o carril?"), `01-flujo-de-trabajo.md`
  y como plantilla alternativa completa en `plantilla.mmd`.
- La reconstrucción v2 de `pruebas/documentacion-software/` pasó de 4 carriles + 3 pares de
  conectores a 6 fases + 0 conectores, mismo contenido/numeración/notas de validación.
- El tema visual (oscuro/naranja) del HTML de referencia **no se adoptó** — el usuario confirmó
  mantener la paleta clara calibrada de Bizagi; el HTML era solo referencia estructural.
- La prueba de "Inducción..." se queda como está (agrupada por carril): ahí el problema real era
  el carril, y esa prueba no tiene fases limpias que lo resuelvan mejor.

## Corrección v3 — vuelta a carril, flecha directa en vez de conector

El usuario corrigió dos cosas de la reconstrucción v2 (fase):

1. **v2 estaba mal fundamentada.** Las "fases" que usé (Detalle Requerimiento, Validación De
   Requerimiento, Proceso de Desarrollo, Proceso de Pruebas) eran menciones sueltas entre
   paréntesis dentro de la celda de cada actividad, no secciones formales como en el procedimiento
   de referencia (que sí tenía encabezados de fase explícitos). Este procedimiento solo tiene
   responsables. **Regla agregada:** no inferir fases de indicios débiles — solo agrupar por fase
   cuando la fuente las define explícitamente.
2. **Lo que sí había que copiar de la referencia no era "agrupar por fase"**, sino la técnica de
   conectar los grupos: flecha punteada **directa, actividad puntual a actividad puntual** (como
   `A11 -.-> B12` en la referencia), no el conector numerado ①②③ (dos círculos abstractos que hay
   que emparejar por número). **El conector numerado pasa a ser alternativa de reserva**, no la
   técnica por defecto — se documentó así en `02-reglas-de-diagramacion.md` y `plantilla.mmd`.

`pruebas/documentacion-software/` quedó en v3: carril por responsable (igual que v1), pero los 6
cruces de carril usan flecha punteada directa en vez de los 3 pares de conectores de v1. El
historial completo (v1→v2→v3, con el porqué de cada cambio) queda en el propio `.mmd` como
comentario, para que quede memoria de qué se descartó y por qué.

## v4/v5 — CONFIRMADO: el `subgraph` de carril era la causa raíz, no el estilo de flecha

Dos intentos distintos de resolver el cruce de carril en `documentacion-software` (conector
numerado en v1, flecha punteada directa en v3, ambos DENTRO de `subgraph` de carril) reportaron
el **mismo síntoma**: "las flechas no tocan las actividades". v4 quitó los `subgraph` de carril
por completo — cadena única de cajas en orden de ejecución, responsable como segunda línea dentro
de cada caja ("👤 Responsable"), cada flecha un salto directo entre dos vecinos sin geometría de
clúster de por medio. **El usuario confirmó que v4 se ve bien.** v5 solo cambió `flowchart LR` →
`TD` (presentación vertical, misma estructura), sin volver a tocar el problema.

Conclusión: en Mermaid, una flecha hacia un nodo DENTRO de un `subgraph` puede renderizarse
terminando en el borde del clúster en vez de en el nodo — pasa sin importar el estilo de flecha
(conector numerado o flecha directa). La técnica confirmada para evitarlo: **sin `subgraph` de
carril/fase cuando hay cruces frecuentes** — cadena única, responsable/fase como etiqueta de texto
dentro de la caja. Promovido a `02-reglas-de-diagramacion.md` y `plantilla.mmd` como técnica por
defecto para ese caso (reemplaza tanto al conector numerado como a la "agrupación primaria: fase o
carril" documentada antes — esa sigue aplicando solo cuando NO se prevén cruces frecuentes, ya que
ahí el `subgraph` no tiene por qué toparse con este problema).

## Decisión de entorno

- [x] ¿Dónde corre la skill? **Claude web / app (claude.ai)** — no Claude Code local.
- [ ] Confirmar el mecanismo real de exportación a PDF/JPG/PNG en ese entorno: si el sandbox de
  código de claude.ai permite instalar y correr `@mermaid-js/mermaid-cli` igual que en local, o si
  hay que apoyarse en Artifacts (Mermaid nativo, sin CLI) y dejar la exportación a la UI del
  artifact. **Pendiente de probar directamente en claude.ai** — ver la nota en
  `../references/05-formatos-de-salida.md`.
