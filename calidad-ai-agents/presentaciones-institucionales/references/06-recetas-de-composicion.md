# Recetas de composición — contenido → layout

Esta referencia responde a **"tengo este pedazo de información, ¿cómo lo armo en
la diapositiva?"**. Es la capa de arquitectura de información; es distinta de:

- `02-reglas-de-diseno.md` — umbrales de densidad y jerarquía (cuánto texto cabe).
- `04-tipos-de-diapositiva.md` — catálogo grueso de tipos (portada, sección, cierre…).
- `05-mapa-de-layouts.md` — qué layout de `plantilla.pptx` y qué helper de
  `pptx_kit.py` para cada tipo (la capa de implementación PPTX).

El catálogo detallado de estructuras está en **`assets/layouts-gerenciales.md`**
(14 layouts L01–L14, cada uno con: cuándo usar, cuándo evitar, lista de slots y
reglas de proporción). Salió de diseños reales aprobados.

> **La piel de marca no se toca.** Colores, tipografías y el marco de plantilla
> (banda de título, logo, franja de sellos) vienen de `assets/paleta.md` y
> `05-mapa-de-layouts.md`. De `layouts-gerenciales.md` se toma **la estructura**
> de la zona de contenido — proporciones, qué va dónde, cuántos elementos — no
> sus valores hex.

## Elegir el layout por la pregunta que responde

| La pregunta del comité | Layout | Contenido típico |
|---|---|---|
| ¿Cuánto es en total? | L01 `kpi-hero` | una cifra que sostiene la decisión |
| ¿Cómo vamos en general? | L02 `kpi-row` | 3–4 indicadores independientes con su variación |
| ¿Cuál de las dos? | L03 `compare-2` | dos escenarios/proveedores/opciones |
| ¿Dónde está concentrado? | L04 `ranking-bars` | conceptos ordenados de mayor a menor |
| ¿Por qué se movió? | L05 `split-half` | una serie temporal + su interpretación |
| ¿Cómo se reparte? | L06 `share-100` | partes de un total conocido (100%) |
| ¿Cuánto por cada línea? | L07 `table-lite` | cifras exactas por fila, ≤5 filas |
| ¿Para cuándo y quién? | L08 `stages` | secuencia de etapas con fecha y responsable |
| ¿Qué necesitan de nosotros? | L09 `closing` | decisión que se pide + próximos pasos |
| ¿De qué se trata esto? | L10 `text-image` | contexto sin cifras + imagen real |
| ¿Quién lo respalda? | L11 `quote-avatar` | declaración con vocero identificable |
| ¿Por qué hacemos esto? (sólo texto) | L12 `plain-text` | justificación / objetivo / marco normativo |
| ¿Cuáles son los pasos o criterios? | L13 `plain-bullets` | requisitos o criterios numerados (≤4) |
| ¿Cuál es la postura del área? | L14 `plain-statement` | un mensaje que debe quedar sonando |

Reglas para no caer siempre en "viñetas":

- Si el contenido tiene **una cifra dominante** → L01, no viñetas.
- Si son **varias cifras** → L02 (independientes) o L06 (partes de un total).
- Si hay **magnitudes comparables** → L04 (ranking) o L07 (tabla con valores exactos).
- Si hay **evolución en el tiempo** → L05.
- Si es **una decisión entre opciones** → L03.
- Viñetas de texto plano: sólo L12–L14, y con personaje institucional.

## Mapeo a los helpers de `pptx_kit.py`

Estado: ✅ el helper lo cubre · ⚠️ se compone con helpers + coordenadas · ❌ falta un helper (hoy se aproxima o se hace por coordenadas).

| Layout | Helpers de `pptx_kit.py` | Estado | Nota |
|---|---|---|---|
| L01 `kpi-hero` | `kpi_gigante` + `kpi_tiles` (2 de apoyo) | ✅ | cifra grande + ≤2 tarjetas de apoyo |
| L02 `kpi-row` | `kpi_tiles([(label, valor, delta, nota, alerta), …])` | ✅ | match directo; es el layout de referencia del kit |
| L03 `compare-2` | `tarjetas([(A, [...], "blanco"), (B, [...], "inst")])` + `caja_texto` (recomendación) | ✅ | la tira "Recomendación" con borde izq. de acento es una mejora pendiente |
| L04 `ranking-bars` | `barras_horizontales([(rótulo, %), …])` + `kpi_tiles`/`kpi_gigante` al lado | ⚠️ | la barra sí; la **columna lateral** (total + lectura clave) hay que colocarla por coordenadas |
| L05 `split-half` | `caja_texto` (texto 32%) + `grafica_barras(cats, [(serie, vals)], highlight=-1)` (68%) | ⚠️ | el split y los 2 mini-datos se colocan por coordenadas |
| L06 `share-100` | `barra_apilada([(nombre, pct, valor, nota), …], total=(label, valor))` | ✅ | barra apilada 100% + tarjeta por segmento con borde superior del color del segmento; % dentro del segmento sólo si ≥ 10 |
| L07 `table-lite` | `tabla(headers, rows, total_rows=(…))` | ✅ | incl. fila de total; el chip de estado en la última columna es mejora pendiente |
| L08 `stages` | `etapas([(fecha, nombre, desc, responsable, cumplida), …], hito="…")` | ✅ | barra de avance segmentada, etapas pendientes atenuadas, responsable anclado al pie, hito crítico en franja azul |
| L09 `closing` | `tarjetas([(decisión, [...], "inst")])` + `tabla` (pasos: nº/acción/responsable/fecha) | ⚠️ | componible; el bloque de decisión azul al 34% se coloca por coordenadas |
| L10 `text-image` | `caja_texto`/`vinetas` + `imagen(ruta, credito="…")` | ✅ | `imagen()` coloca una imagen de contenido (no personaje) por defecto en la columna derecha (~38%); si la ruta no existe dibuja un marcador punteado |
| L11 `quote-avatar` | `cita(mensaje, nombre, cargo, avatar=…, chips=[(label, valor), …])` | ✅ | avatar circular (o círculo con iniciales si no hay imagen), mensaje grande sin cifras nuevas, hasta 2 chips |
| L12 `plain-text` | `Deck.texto_pleno(titulo, encabezado=…, cuerpo=[…], figura=…)` | ✅ | marco estándar (topbar redondeado + logo, **sin banda a sangre** desde v2); personaje al piso, tarjeta de texto a la derecha |
| L13 `plain-bullets` | `Deck.texto_pleno(titulo, encabezado=…, cuerpo=[…], numerada=True)` | ✅ | cada punto con numeral |
| L14 `plain-statement` | `Deck.texto_pleno(titulo, mensaje="…", apoyos=[…])` | ✅ | mensaje central + viñetas de apoyo |

### Estado de los helpers

Los 5 helpers que faltaban ya están en `assets/pptx_kit.py`: `barra_apilada`
(L06), `etapas` (L08), `imagen` (L10), `cita` (L11) y `Deck.texto_pleno`
(L12–L14; desde "Layouts Gerenciales v2" usa el marco estándar, sin banda a
sangre). El deck de ejemplo
(`assets/ejemplos-generados/pptx/ejemplo-gestion-integral-pptx.py`) usa
`barra_apilada`, `etapas` y `cita` en las diapositivas 15, 16 y 18.

Siguen componiéndose por coordenadas (filas ⚠️): la columna lateral de L04, el
split de L05 y el bloque de decisión al 34% de L09. Para eso, usar las constantes
de geometría de `pptx_kit` (`MX`, `CANVAS_Y`, `CANVAS_H`, `CONTENT_W`).

## Modalidad de la presentación

Es lo primero que se define (paso 1 del flujo en `SKILL.md`, **justo después del
formato de entrega**). Cada modalidad tiene un enfoque de diseño y una paleta de
layouts propia; de ahí sale la secuencia base del esquema.

### Gerencial — decidir / rendir cuentas

Audiencia directiva, poco tiempo. Un hallazgo por lámina, titular que afirma, la
cifra a la vista, y cierre con la decisión y sus responsables.

- **Favorecer:** L01, L02, L04, L05, L06, L07, L09, L11.
- **Evitar:** L12–L14 y toda narrativa larga; sub-viñetas; una lámina sin lectura clave.
- **Secuencias:**
  - Comité directivo: L02 → L04 → L05 → L06 → L11 → L09
  - Solicitud de aprobación: L10 → L01 → L07 → L03 → L09
  - Seguimiento de proyecto: L02 → L08 → L05 → L11 → L09

### Informativa — divulgar / socializar

Público amplio, no necesariamente experto. El objetivo es que **entiendan**, no que
decidan: más contexto, imagen real de apoyo, una gráfica clara por tema, y cierre
con un mensaje que quede sonando (no con "decisión solicitada").

- **Favorecer:** L10, L12, L02, L05, L06, L11, L14.
- **Evitar:** L07 y tablas densas; L09 con decisión; L01 (cifra sola sin contexto).
- **Secuencia:** L12 → L10 → L02 → L05 → L06 → L14

### Capacitación — formar / instruir

Aprendices; el objetivo es que **sepan hacer y recuerden**. Paso a paso, criterios
numerados, proceso por etapas, ejemplos de contraste. Ritmo más lento: más
diapositivas, menos contenido por lámina; refuerzo con un mensaje central.

- **Favorecer:** L13, L08, L10, L12, L03, L07 (como checklist), L14.
- **Evitar:** L01, L04, L06 salvo que el dato sea parte de la lección; L09 con decisión.
- **Secuencia:** L12 → L10 → L13 → L08 → L03 → L14

Las secuencias son punto de partida, no una plantilla rígida: se ajustan al
contenido real, pero manteniendo la paleta de layouts de la modalidad.

## Reglas transversales (además de las de `02-reglas-de-diseno.md`)

1. El **titular afirma un hallazgo**, no nombra la tabla de origen: «Tecnología
   concentra 77% del cupo», no «Distribución por dirección».
2. Toda cifra lleva **unidad y periodo** explícitos, en el label o en la nota al pie.
3. **Redondeo a la precisión que soporta la decisión**: millones sin decimales,
   porcentajes con un decimal.
4. Un solo color de acento por diapositiva; el azul institucional marca lo destacado.
5. Ningún elemento sin propósito: si un bloque no cambia una decisión, se elimina.
6. Toda imagen o avatar es **material real de la entidad**, con crédito al pie.

## Cómo se actualiza

Si se rediseñan los layouts en el proyecto de Claude Design
("Layouts Gerenciales v2"), regenerar `assets/layouts-gerenciales.md` desde ahí y
revisar la tabla de mapeo de arriba (helpers y estado).
