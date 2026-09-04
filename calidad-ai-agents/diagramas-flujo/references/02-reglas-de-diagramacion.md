# Reglas de diagramación

## Límite de 100 caracteres (regla del encargo)

- Toda **actividad** o **acción** ≤ **100 caracteres**, contando espacios.
- Si no cabe: partir en dos pasos, o reescribir más directo. Nunca abreviar con siglas no
  estándar ni recortar hasta que quede ambiguo.
- **Antes de partir un paso en dos, recorta primero.** El párrafo completo de la fuente suele
  incluir referencias que no son la acción en sí — nombre/código de formato, texto de apoyo,
  ejemplos — y esas se descartan del texto de la caja (no se diagraman, no se dividen en un paso
  aparte). Split solo si la frase de acción, YA recortada de esas referencias, sigue sin caber en
  100 caracteres. Confirmado con un procedimiento real: dos pasos se habían partido en dos cajas
  por la longitud del párrafo completo, pero el diagrama real de la organización usaba una sola
  caja para cada uno — la frase de acción sola cabía sobrada.
- Redacción: **verbo en infinitivo + objeto**. "Registrar la solicitud en el sistema", no
  "Registro de solicitud" ni "El analista registra la solicitud que llega...".
- Las **decisiones** se escriben como pregunta cerrada: "¿La solicitud está completa?".
- Las **etiquetas de las salidas** de una decisión: cortas ("Sí" / "No", o la opción real).
- **Numeración de actividades:** toda actividad lleva al inicio de la etiqueta el número del paso
  **tal como aparece en la fuente** (el documento/tabla de donde salió el procedimiento), no una
  renumeración propia — así se puede trazar cada caja del diagrama contra su fila de origen. Si un
  paso original se partió en dos por el límite de 100 caracteres, usa sufijo decimal: paso 6 →
  "6.1", "6.2". Si el insumo no trae numeración propia (ej. texto corrido sin lista), numera
  1, 2, 3... en el orden en que se redactan los pasos (ver `01-flujo-de-trabajo.md`, paso 2).

## Nomenclatura

| Elemento | Cómo se nombra |
|---|---|
| Evento inicial | Sustantivo del disparador: "Solicitud recibida". |
| Actividad | "N. Verbo infinitivo + objeto" — N es el número de la fuente, no uno inventado. ≤ 100 car. |
| Decisión (compuerta) | Pregunta cerrada terminada en "?". |
| Subproceso | Nombre del procedimiento referenciado. |
| Evento final | Resultado alcanzado: "Solicitud archivada". |
| Conector | Número o letra corta: "①", "②"; sin texto descriptivo. |

## Tipos de nodo (equivalencia BPMN / Bizagi)

- **Evento** (círculo): inicio, fin, y esperas/temporizadores si aplica.
- **Actividad** (rectángulo redondeado): un paso de trabajo.
- **Decisión** (rombo): bifurcación exclusiva. Toda rama debe reconectarse o terminar en un fin.
- **Subproceso** (rectángulo con marca +): paso que es en sí otro procedimiento.
- **Cruce entre grupos (responsable o fase): flecha punteada directa, actividad a actividad.**
  Nunca un símbolo que haya que emparejar por número — así el rastro nunca se pierde. Dentro del
  mismo grupo: flecha sólida. Al cambiar de grupo: flecha punteada directa entre esos dos nodos
  concretos. Mismo criterio ya usado para notas de validación ("esto es un salto estructural, no
  una continuación directa").
- **Conector** (círculo pequeño numerado, ver `assets/paleta-bizagi.md`): alternativa de reserva
  poco recomendada, no la opción por defecto. Marca un punto de salida/entrada sin dibujar la
  línea completa. Es la técnica documentada en un export real de Bizagi para el "retorno de
  subsanación" **dentro de un mismo carril sin `subgraph`** (el export real no agrupa por
  responsable con recuadros). Evítala si el diagrama va a tener `subgraph` de por medio — ver
  advertencia debajo.
- **Carril** (*lane*): responsable/rol. **Un responsable es SIEMPRE un solo grupo**, incluso si el
  flujo lo abandona y vuelve más adelante — nunca partir el mismo responsable en dos carriles
  separados.
- **Fase**: banda que agrupa varias actividades por etapa del proceso (no por responsable).

### ⚠️ `subgraph` (carril o fase) y flechas que cruzan hacia dentro: bug confirmado

**Confirmado con un procedimiento real, en dos intentos distintos:** una flecha (conector numerado
o flecha directa, da igual) hacia un nodo que vive DENTRO de un `subgraph` de Mermaid puede
renderizarse terminando visualmente en el borde del clúster, no en el nodo — el usuario lo vio dos
veces seguidas con técnicas de flecha distintas, y solo se resolvió al quitar el `subgraph` por
completo. Es un límite de Mermaid/dagre con grafos compuestos, no un error de sintaxis.

- **Si el diagrama va a tener cruces frecuentes entre responsables/fases** (más de 1 o 2): **no
  uses `subgraph` en absoluto.** Una sola cadena de cajas en el orden real de ejecución; el
  responsable o la fase de cada paso va como segunda línea de texto dentro de la propia caja
  ("👤 Responsable" o "📍 Fase", con `<br/>`) — esa línea es metadata, no cuenta para el límite de
  100 caracteres de la acción. Cada flecha conecta dos vecinos directos en la cadena, sin
  geometría de clúster de por medio, así que no puede fallar de esta forma. Ver
  `pruebas/documentacion-software/documentacion-software.mmd` (v4/v5) como ejemplo real
  reconstruido tras el bug, y la plantilla "sin agrupación" en `assets/plantilla.mmd`.
- **Si los cruces van a ser raros o el procedimiento es mayormente lineal dentro de cada grupo**,
  sí puedes usar `subgraph` de carril o fase (ver más abajo) — el riesgo es menor cuando hay pocas
  flechas cruzando hacia dentro de un clúster.
- Para armar un carril de todos modos: declarar cada nodo una vez fuera de cualquier `subgraph` y,
  dentro del `subgraph` del carril, solo referenciar su id (ver `assets/plantilla.mmd`).

### Agrupación primaria (solo si decidiste usar `subgraph`): ¿fase o carril?

Mermaid no permite anidar carriles y fases de forma legible (dos niveles de `subgraph` con
`direction` propia es frágil) — hay que elegir **uno solo** como la agrupación que estructura el
diagrama, y mostrar el otro como dato dentro de cada caja en vez de como agrupador visual.

- **Agrupa por CARRIL** cuando los responsables son la forma natural de leer el proceso.
- **Agrupa por FASE solo si la fuente las define explícitamente** (encabezado de sección propio,
  columna de fase en la tabla, o similar) — nunca las infieras de indicios débiles como una palabra
  suelta entre paréntesis dentro de la celda de una actividad. Un intento real infirió fases de
  ese tipo de menciones y el usuario las rechazó: ese procedimiento no tenía fases, solo
  responsables.
- Estilo: carril usa la fila "Carril — encabezado" de `assets/paleta-bizagi.md`; fase usa la fila
  "Fase — banda" (deliberadamente otro gris, para que un lector note que es otro tipo de
  agrupación).

## Layout

- Dirección principal: izquierda → derecha.
- Sin cruces de líneas cuando se pueda evitar; usar ruteo ortogonal.
- Una sola entrada y una sola salida por actividad (las múltiples salidas van por decisión).
- Todas las ramas de una decisión terminan (en un fin o reconectando al flujo). No dejar ramas
  colgando.
- Las notas de validación (`03-validacion-por-colores.md`) llevan el número de paso **de la
  fuente** en su propio texto ("Paso 6 — ..."), no solo la línea punteada que las conecta: en un
  carril con muchos nodos, esa línea puede verse ambigua sobre a cuál actividad exacta corresponde.

## Paleta

- Colores por tipo de elemento según `assets/paleta-bizagi.md`.
- El color de relleno indica **tipo de elemento**, no estado. El estado (verde/amarillo/rojo) va
  como **comentario/marca de validación**, no como relleno del nodo — ver `03-validacion-por-colores.md`.

## Herramienta de dibujo

- Mermaid (`flowchart`) como fuente del diagrama, con `classDef` para aplicar la paleta.
- Alternativa: draw.io/diagrams.net con la librería BPMN.
- La fuente (texto Mermaid o `.drawio`) se guarda junto al export para poder editar después.
