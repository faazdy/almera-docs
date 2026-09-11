# Layouts para presentaciones gerenciales · referencia v2

> Catálogo importado del proyecto de Claude Design **"Tres diseños de diapositivas
> gerenciales"** → `Layouts Gerenciales v2.dc.html`. Este `.md` es la
> especificación portable; el catálogo visual vive en ese proyecto.
> **La paleta, las tipografías y el marco de plantilla de la skill mandan sobre
> los valores hex de este documento** — ver `assets/paleta.md` y
> `references/05-mapa-de-layouts.md`. De aquí se toma la **estructura** de la
> zona de contenido (qué va dónde, proporciones, cuándo usar cada una), no los
> colores. El mapeo a los helpers de `assets/pptx_kit.py` está en
> `references/06-recetas-de-composicion.md`.
>
> **Cambio v2 (última sincronización):** L12–L14 ya **no** usan banda a sangre.
> Comparten el mismo marco estándar que L01–L11 (banda de título con radio,
> dentro del margen, + logo). Lo único propio de cada layout es la zona de
> contenido.

Catorce estructuras de contenido sobre la plantilla institucional. L12–L14 son las variantes simples de sólo texto con personajes institucionales; todas comparten el mismo marco. Catálogo visual: `Layouts Gerenciales v2.dc.html`.

## Contrato de render

- Los placeholders se escriben como `[nombre]`.
- Cada diapositiva es **un solo contenedor**: `container-type:inline-size; width:100%; aspect-ratio:16/9; box-sizing:border-box`.
- Toda medida interna (tipografía, padding, gap, alto de barra) se expresa en **cqw** → escala igual a 800px, 1600px o 1920px. `1cqw = 1% del ancho`; a 1600px, `1cqw = 16px`.
- Sólo estilos inline. Sin sombras, sin degradados.

## Marco fijo de la plantilla

No cambia entre layouts. Lo único que varía es la zona de contenido.

| Zona | Especificación |
|---|---|
| Fondo de diapositiva | `#f2f7fb` |
| Padding de diapositiva | `2.6cqw` vertical, `2.8cqw` horizontal; `gap 2cqw` entre zonas |
| Banda de título | `#0b3b70`, radio `1.6cqw`, padding `2.1cqw 2.6cqw`; titular 2.6cqw/800 blanco; bajada 1.55cqw `#b8d3ea`. **Igual en L12–L14** (sin banda a sangre). |
| Logo | arriba a la derecha, `13cqw × 5.6cqw`, alineado al tope de la banda |
| Zona de contenido | `flex:1`, alto útil ≈ 27cqw |
| Nota al pie | 1.5cqw, `#2f7fbf` |
| Franja de logos | dos bloques `#eceff1`, radio `1cqw`, alto `4.4cqw`, proporción 2.2 / 1.4 |
| Tarjeta de contenido | `#fff`, borde 1px `#dbe6f0`, radio `1cqw`, padding `1.6–2.2cqw` |
| Tarjeta destacada | `#0b3b70` sólido, mismo radio; texto blanco, labels `#8fc0e8` |
| Placeholder de imagen | `#eef4fa` con borde `1px dashed #b9cfe3`, radio `1cqw` |

**Paleta:** `#0b3b70` (institucional) · `#1a5f9e` · `#1a7fc1` (acento) · `#8fc0e8` · `#cfe2f3` · `#eef4fa` (relleno) · `#eceff1` (franja).
**Texto:** tinta `#0b3b70` · secundario `#4a5f7a` · gris de nota `#8a9099` · sobre azul `#fff` y `#b8d3ea`.

### Escala tipográfica (cqw)

| Rol | Tamaño | Peso |
|---|---|---|
| Cifra hero (L01) | 8.4 | 800 · −0.04em |
| KPI en tarjeta | 4.4 | 800 · −0.035em |
| Cifra media | 2.6 – 4 | 800 |
| Titular de la banda | 2.6 | 800 · −0.015em |
| Mensaje de vocería | 2.2 | 600 |
| Nombre de bloque / segmento | 1.75 – 2 | 700 |
| Cuerpo, celda, viñeta | 1.55 – 1.7 | 400–600 |
| Label mono, eje, nota al pie | **1.4 – 1.5 (mínimo)** | 400–600 · mayúsculas · tracking 0.1–0.14em |

Nunca por debajo de 1.4cqw en labels mono ni 1.5cqw en texto corrido. Si no cabe, se recorta el contenido — jamás la tipografía.

## Anatomía común

1. **Titular** en la banda: afirmación, no etiqueta. «Tecnología concentra 77% del cupo», no «Distribución por dirección».
2. **Bajada** (1.55cqw): periodo, base de comparación, alcance.
3. **Zona de contenido**: la evidencia (tarjetas, barras, tabla, etapas, texto e imagen).
4. **Nota al pie**: unidades y fuente. L12 no la lleva.

## Catálogo

### L01 · `kpi-hero` — Cifra protagonista
**Usar:** una sola cifra sostiene la decisión (monto total, ahorro, cumplimiento). Primera diapositiva de resultado.
**Evitar:** tres o más cifras del mismo rango, o cifra que exige explicación previa → L02 / L05.
**Slots:** `titular`, `bajada`, `label_cifra`, `cifra`, `unidad`, `variacion`, `lectura_clave` (≤120 car.), `apoyo_1..2_label|valor|nota`, `nota_pie`.
**Reglas:** cifra 8.4cqw/800/−0.04em; tarjeta principal `1.55fr` frente a columna de apoyo `1fr`; máximo dos tarjetas de apoyo.

### L02 · `kpi-row` — Tres o cuatro KPIs en fila
**Usar:** tablero de apertura; indicadores independientes con su variación. Es el layout de la plantilla de referencia.
**Evitar:** partes de un mismo total → L06; más de cuatro KPIs.
**Slots:** `titular`, `bajada`, `kpi_N_label|valor|delta|nota` (N = 1..4), `nota_pie`.
**Reglas:** valor 4.4cqw, máx ~8 caracteres (`white-space:nowrap`); label mono en máx 2 líneas; delta con ▲/▼; tarjetas de igual alto, `gap 1.6cqw`.

### L03 · `compare-2` — Comparativo A vs B
**Usar:** decidir entre dos caminos (escenarios, proveedores, antes/después). La recomendada va a la derecha, en tarjeta azul sólida.
**Evitar:** tres o más alternativas, o más de cuatro criterios por lado → L07.
**Slots:** `titular`, `bajada` (criterio), `opcion_X_nombre|tag|cifra|unidad|a_favor_1|a_favor_2|en_contra` (X = a, b), `recomendacion` (≤90 car.).
**Reglas:** columnas simétricas `1fr / 1fr`; 2 a favor + 1 en contra por lado; viñeta circular 0.7cqw; recomendación en tarjeta blanca con borde izquierdo `0.6cqw #1a7fc1`.

### L04 · `ranking-bars` — Ranking en barras horizontales
**Usar:** orden por magnitud (conceptos de gasto, áreas, proveedores, causas), de mayor a menor.
**Evitar:** categorías que suman 100% → L06; más de siete filas (el resto va como «Otros»).
**Slots:** `titular`, `bajada`, `concepto_N|valor_N` (N = 1..7), `total_label`, `total_valor`, `lectura_clave`, `nota_pie`.
**Reglas:** grid `20cqw / 1fr / 9cqw`; barra 2.4cqw de alto, radio 0.3cqw, ancho relativo a la fila mayor; azul decreciente `#0b3b70 → #1a5f9e → #1a7fc1 → #6aa9db → #b3d3ee`; columna lateral (22%) con total en azul sólido y lectura clave.

### L05 · `split-half` — Texto + gráfico
**Usar:** la cifra necesita explicación (evolución, tendencia, causa). El texto interpreta, el gráfico evidencia.
**Evitar:** párrafo de más de cuatro líneas, o gráfico con más de dos series.
**Slots:** `titular`, `bajada`, `que_muestra`, `parrafo` (≤200 car.), `dato_1..2_label|valor`, `grafico_titulo`, `grafico_unidad`, `v1..v6`, `eje_1..6`.
**Reglas:** texto 32% / gráfico 68%; 6 a 8 barras verticales con radio superior 0.3cqw, la última en `#0b3b70`; eje base 2px `#dbe6f0`; valor rotulado sobre cada barra.

### L06 · `share-100` — Distribución del 100%
**Usar:** partes de un total conocido (presupuesto por área, cartera por edad, población por régimen). La barra apilada se lee mejor que una dona.
**Evitar:** más de cuatro segmentos con detalle, o segmento < 3% (agrúpalo en «Otros»).
**Slots:** `titular`, `bajada`, `seg_N_pct|nombre|valor|nota` (N = 1..4), `total_label`, `total_valor`, `nota_pie`.
**Reglas:** `flex` de cada segmento = valor real; barra 3.6cqw de alto, `gap 0.3cqw`, extremos redondeados 0.4cqw; el `%` va dentro del segmento sólo si supera 10%; el borde superior `0.6cqw` de cada tarjeta repite el color de su segmento.

### L07 · `table-lite` — Tabla resumida
**Usar:** cifras exactas por línea y comparación de dos o tres magnitudes. La última columna es estado o plazo.
**Evitar:** más de cinco filas → resume y deja el detalle en anexo.
**Slots:** `titular`, `bajada` (unidad), `col_1..5`, `fN_c1..c5` (N = 1..5), `total_label`, `total_c2..c4`, `nota_pie`.
**Reglas:** grid `2.2fr / 1fr / 1fr / 1fr / 11cqw`; celda 1.6cqw, padding de fila 1.2cqw; números mono a la derecha; separadores 1px `#eef4fa`; encabezado y total con borde 2px `#0b3b70`; estado como chip radio 0.5cqw.

### L08 · `stages` — Proceso por etapas
**Usar:** secuencia con fechas y responsables (ruta de aprobación, implementación, cronograma). Cumplidas a color, pendientes atenuadas.
**Evitar:** etapas simultáneas, más de cinco pasos, o etapas con sub-actividades.
**Slots:** `titular`, `bajada` (horizonte), `etapa_N_fecha|nombre` (≤26 car.)`|desc` (≤100 car.)`|responsable` (N = 1..5), `hito_critico`.
**Reglas:** número 2.6cqw mono de dos dígitos; barra de avance segmentada 0.5cqw sobre las tarjetas; pendientes con `opacity:0.72`; responsable anclado al pie con `margin-top:auto`; hito crítico en franja azul sólida.

### L09 · `closing` — Cierre y próximos pasos
**Usar:** última diapositiva de todo comité: qué se pide aprobar, quién hace qué y para cuándo.
**Evitar:** no hay decisión concreta que pedir → cierra con L01 o L02.
**Slots:** `titular`, `bajada`, `decision_solicitada`, `decision_detalle`, `paso_N|responsable_N|fecha_N` (N = 1..4), `riesgo` (nota al pie).
**Reglas:** bloque de decisión 34% en azul sólido; máx 4 pasos, verbo en infinitivo; grid de paso `2.6cqw / 1fr / 13cqw / 10cqw`; fechas mono a la derecha.

### L10 · `text-image` — Título + texto + imagen
**Usar:** diapositiva sin cifras: contexto, marco normativo, alcance de un programa. La imagen acompaña, no decora.
**Evitar:** no hay imagen real disponible (queda un hueco); texto de más de un párrafo y tres viñetas.
**Slots:** `titular`, `bajada`, `antetitulo`, `parrafo` (≤220 car.), `punto_1..3`, `imagen` (4:3), `nota_pie` (crédito).
**Reglas:** texto 62% / imagen 38%; imagen con radio 1cqw sin marco; viñeta circular 0.7cqw; toda imagen lleva crédito al pie.

### L11 · `quote-avatar` — Mensaje con vocería
**Usar:** declaración con dueño: compromiso de la dirección, lineamiento, apertura o cierre de jornada.
**Evitar:** frase sin autor identificable; más de dos por presentación.
**Slots:** `titular`, `bajada`, `avatar`, `nombre`, `cargo`, `mensaje` (≤180 car.), `chip_1_label|valor`, `chip_2_label|valor`, `nota_pie`.
**Reglas:** avatar circular 14cqw con nombre y cargo debajo; mensaje 2.2cqw/600 en máx 3 líneas, sin cifras nuevas; máximo dos chips `#eef4fa`.

### L12 · `plain-text` — Texto con personajes
**Usar:** diapositiva de sólo texto (justificación, objetivo, alcance, marco normativo). Los personajes institucionales dan presencia sin competir con el contenido.
**Evitar:** hay cifras que sostienen el argumento (→ L01/L02) o el texto pasa de cinco líneas.
**Slots:** `titulo`, `subtitulo`, `encabezado`, `linea_1..5`, `personajes`.
**Reglas:** marco estándar (banda con radio + logo); personajes 34% alineados al piso; tarjeta de texto radio `1cqw` borde `#dbe6f0`; encabezado 2.6cqw/800 `#1a5f9e` en mayúsculas; líneas 1.7cqw `#3d4a57`; sin nota al pie.

### L13 · `plain-bullets` — Texto en viñetas con personaje
**Usar:** el texto se ordena en pasos, requisitos o criterios numerados. Un solo personaje acompaña.
**Evitar:** más de cuatro puntos, o puntos de más de dos líneas → L07 o dos diapositivas.
**Slots:** `titulo`, `subtitulo`, `encabezado`, `entrada` (≤110 car.), `punto_1..4` (≤90 car.), `personaje`.
**Reglas:** texto 74% / personaje 26%; numeral en círculo `2.2cqw` fondo `#eef4fa`; encabezado 2.4cqw mayúsculas; frase de entrada ≤110 car.; sin nota al pie.

### L14 · `plain-statement` — Mensaje central con personajes
**Usar:** apertura o cierre de un bloque narrativo: una postura, compromiso o definición que debe quedar sonando.
**Evitar:** el mensaje necesita datos para sostenerse, o hay más de tres apoyos.
**Slots:** `titulo`, `subtitulo`, `encabezado`, `mensaje` (2–3 líneas), `apoyo_1..3`, `personajes`.
**Reglas:** encabezado 2.4cqw mayúsculas; mensaje 1.9cqw en 2–3 líneas; máximo 3 apoyos con viñeta circular 0.7cqw; personajes 38% anclados al pie; sin nota al pie.

## Cómo elegir el layout

| La pregunta del comité | Layout |
|---|---|
| ¿Cuánto es en total? | L01 |
| ¿Cómo vamos en general? | L02 |
| ¿Cuál de las dos? | L03 |
| ¿Dónde está concentrado? | L04 |
| ¿Por qué se movió? | L05 |
| ¿Cómo se reparte? | L06 |
| ¿Cuánto por cada línea? | L07 |
| ¿Para cuándo y quién? | L08 |
| ¿Qué necesitan de nosotros? | L09 |
| ¿De qué se trata esto? | L10 |
| ¿Quién lo respalda? | L11 |
| ¿Por qué hacemos esto? (sólo texto) | L12 |
| ¿Cuáles son los pasos o criterios? | L13 |
| ¿Cuál es la postura del área? | L14 |

## Secuencias tipo

- **Comité directivo (6):** L02 → L04 → L05 → L06 → L11 → L09
- **Presentación con narrativa (5):** L12 → L13 → L02 → L05 → L14
- **Solicitud de aprobación (5):** L10 → L01 → L07 → L03 → L09
- **Seguimiento de proyecto (5):** L02 → L08 → L05 → L11 → L09

## Reglas transversales

1. El titular afirma un hallazgo; nunca nombra la tabla de origen.
2. Una idea por diapositiva. Si hay dos lecturas clave, hay dos diapositivas.
3. Toda cifra lleva unidad y periodo explícitos, en el label o en la nota al pie.
4. Redondea a la precisión que soporta la decisión: millones sin decimales, porcentajes con uno.
5. Un solo color de acento por diapositiva (`#1a7fc1`); el azul institucional marca lo destacado.
6. Ningún elemento sin propósito: si un bloque no cambia una decisión, se elimina.
7. Toda imagen o avatar es material real de la entidad, con crédito al pie.

---

## Apéndice · variante neutra (v1)

`Layouts Gerenciales.dc.html` conserva los layouts L01–L09 en una paleta neutra gris/azul, **sin** el marco institucional (sin banda de título, sin franja de logos) y con otra escala (padding `4cqw/4.5cqw`, cifra hero 9cqw, tinta `#16202b`, acento `#2f5d8a`). Sirve como alternativa para documentos fuera de la plantilla oficial; sus medidas **no** aplican a v2. L10–L14 existen sólo en v2.
