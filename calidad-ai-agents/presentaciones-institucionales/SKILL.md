---
name: presentaciones-institucionales
description: >-
  Genera presentaciones institucionales (diapositivas) respetando la plantilla y la paleta de
  colores oficiales. Úsala siempre que el usuario pida "una presentación", "unas diapositivas",
  "un PPT", "un deck", "slides", pase un texto/informe y pida convertirlo a presentación, o
  pida exportar una presentación a PPTX, HTML o PDF. La skill produce diapositivas limpias, muy
  visuales y comprensibles, sin saturar de información, y siempre parte de una presentación de
  referencia aprobada.
---

# Presentaciones institucionales

Genera presentaciones que se ven como las hace la organización: misma plantilla, misma paleta,
misma estética sobria donde la información respira.

## Antes de generar nada

Esta skill **no funciona sin sus insumos de referencia**. Revisa que existan en `assets/`:

- `assets/plantilla.pptx` — plantilla PPTX institucional. **Es la base del formato PPTX**
  (tema de color y fuentes correctos). Sus placeholders no se usan; ver `references/05-mapa-de-layouts.md`.
- `assets/referencia.pptx` — presentación aprobada. Sirve de guía de **estética y densidad**.
  Ojo: su *tema* es Office genérico, no el institucional — no se usa como base de generación.
- `assets/paleta.md` — colores oficiales (hex) y tipografías.
- `assets/pptx_kit.py` — utilidades de generación PPTX. `assets/marca/` + `assets/empaquetar-html.js` — marca para HTML.

Si falta alguno, díselo al usuario y no improvises una plantilla propia. Ver `assets/PENDIENTE.md`.

## Flujo de trabajo

1. **Entender el encargo.**
   - **Pregunta siempre el formato de entrega: ¿PowerPoint (PPTX), Web (HTML) o PDF?** No lo asumas
     (ver `references/03-formatos-de-salida.md`). Si el usuario no tiene
     preferencia, usa PPTX.
   - **Justo después, pregunta la modalidad de la presentación: ¿gerencial,
     informativa o de capacitación?** Fija el enfoque de diseño, qué layouts se
     favorecen y el ritmo del deck (sección "Modalidad de la presentación" abajo).
     Si es mixta o no encaja, pídele al usuario que lo aclare; no lo asumas.
   - Pregunta además, si no está claro:
     - Audiencia y objetivo concretos (comité directivo, socialización a usuarios,
       inducción de personal, cliente externo…).
     - Contenido base: ¿hay un texto, informe o bullets de partida, o se construye desde cero?
     - Extensión aproximada (nº de diapositivas) y si hay fecha/evento.
2. **Proponer un esquema** y esperar visto bueno antes de producir. No generes el archivo final
   sobre un esquema no confirmado. Parte de la **secuencia base de la modalidad** (sección
   "Modalidad de la presentación") y ajústala al contenido. El esquema es una lista numerada
   donde **cada línea lleva su layout `L01`–`L14`** (ver sección "Layout de cada diapositiva"), así:

   ```
   1. Portada — Informe de gestión 2T-2026 · Comité Directivo
   2. L02 kpi-row — El trimestre cierra con utilidad y productividad al alza
   3. L05 split-half — Las solicitudes se concentraron en marzo
   4. L06 share-100 — Tecnología concentra el 63 % del cupo asignado
   5. L08 stages — La ruta de aprobación va en la etapa 3 de 5
   6. L11 quote-avatar — La dirección respalda la ampliación del programa
   7. L09 closing — Tres decisiones para el Comité
   ```

   Elige el layout por la **pregunta que responde** la diapositiva. Si una diapositiva de
   contenido no tiene layout asignado, no pases al paso 3.
3. **Redactar el contenido** aplicando las reglas de diseño (`references/02-reglas-de-diseno.md`):
   una idea por diapositiva, poco texto, apoyo visual. **Abre `references/06-recetas-de-composicion.md`
   y sigue la receta del layout elegido**: sus slots, sus proporciones y **el helper exacto** de
   `pptx_kit.py` (`barra_apilada`, `etapas`, `cita`, `Deck.texto_pleno`, …). No compongas de
   memoria ni sustituyas el helper de la receta por otro más familiar. El catálogo detallado de
   slots está en `assets/layouts-gerenciales.md`.
4. **Generar el entregable** en el formato pedido (`references/03-formatos-de-salida.md`):
   - **PPTX** — escribe un script que importe `assets/pptx_kit.py` y componga el deck
     con `Deck.portada / .separador / .contenido / .texto_pleno` + los helpers de cuerpo
     **que pide la receta de cada layout** (`kpi_tiles`, `barra_apilada`, `etapas`, `cita`,
     `tabla`, `grafica_barras`, …). Guía completa (layouts, geometría, qué helper para qué
     contenido) en `references/05-mapa-de-layouts.md`; modelo de script en
     `assets/ejemplos-generados/pptx/ejemplo-gestion-integral-pptx.py` (usa `barra_apilada`,
     `etapas` y `cita` en las diapositivas 15, 16 y 18).
     Entrega solo el `.pptx`. Renderiza a PNG/PDF **solo si el usuario lo pide** (consume tokens revisarlos).
   - **HTML** — archivo autocontenido; marca incrustada con `assets/empaquetar-html.js`.
     Modelo en `assets/ejemplos-generados/html/ejemplo-gestion-integral.src.html`.
   - **PDF** — desde HTML (headless) o desde PPTX (PowerPoint COM en Windows / LibreOffice).
5. **Entregar y ofrecer ajustes** (reordenar, condensar, cambiar formato).

Detalle en `references/01-flujo-de-trabajo.md`.

## Modalidad de la presentación

Se pregunta en el paso 1, **justo después del formato**. Fija el enfoque de diseño,
qué layouts se favorecen y el ritmo del deck. Detalle y variantes de secuencia en
`references/06-recetas-de-composicion.md` → "Modalidad de la presentación".

| Modalidad | Para qué | Enfoque de diseño | Layouts a favorecer | Evitar |
|---|---|---|---|---|
| **Gerencial** | Comité directivo, rendición de cuentas, pedir una decisión | Un hallazgo por lámina, titular que afirma, la cifra a la vista, cierre con decisión y responsables | L01 L02 L04 L05 L06 L07 L09 L11 | Texto plano largo (L12–L14), narrativa extensa, sub-viñetas |
| **Informativa** | Socialización, divulgación, dar contexto a público amplio | Contexto antes que cifras, imagen real de apoyo, una gráfica clara por tema, cierre con un mensaje (no con "decisión solicitada") | L10 L12 L02 L05 L06 L11 L14 | Tablas densas (L07), cierre tipo L09 con decisión, L01 cifra sola sin contexto |
| **Capacitación** | Formación, inducción, instructivo | Paso a paso, criterios numerados, proceso por etapas, ejemplos de contraste; más láminas y menos contenido por lámina; refuerzo con mensaje central | L13 L08 L10 L12 L03 L07 L14 | L01/L04/L06 salvo que el dato sea parte de la lección; cierre tipo L09 con decisión |

Secuencias base (punto de partida del esquema del paso 2):

- **Gerencial:** L02 → L04 → L05 → L06 → L11 → L09  ·  *aprobación:* L10 → L01 → L07 → L03 → L09  ·  *seguimiento:* L02 → L08 → L05 → L11 → L09
- **Informativa:** L12 → L10 → L02 → L05 → L06 → L14
- **Capacitación:** L12 → L10 → L13 → L08 → L03 → L14

## Layout de cada diapositiva (L01–L14)

Los layouts **no** son plantillas de PowerPoint que se seleccionen: son **recetas de
composición** (qué va dónde, en qué proporción, con qué helper) que se arman sobre el layout
`Contenido Tabla 4`. Salieron de diseños aprobados en Claude Design. La receta completa de cada
uno está en `references/06-recetas-de-composicion.md`; el catálogo de slots, en
`assets/layouts-gerenciales.md`.

Elige el layout por la **pregunta que responde** la diapositiva:

| La pregunta que responde la diapositiva | Layout | Helper de `pptx_kit.py` |
|---|---|---|
| ¿Cuánto es en total? (una cifra que sostiene la decisión) | `L01` kpi-hero | `kpi_gigante` + `kpi_tiles` |
| ¿Cómo vamos en general? (3–4 indicadores independientes) | `L02` kpi-row | `kpi_tiles` |
| ¿Cuál de las dos opciones? | `L03` compare-2 | `tarjetas` |
| ¿Dónde está concentrado? (ranking de mayor a menor) | `L04` ranking-bars | `barras_horizontales` |
| ¿Por qué se movió? (serie temporal + interpretación) | `L05` split-half | `caja_texto` + `grafica_barras` |
| ¿Cómo se reparte el 100 %? (partes de un total) | `L06` share-100 | **`barra_apilada`** |
| ¿Cuánto por cada línea? (cifras exactas, ≤5 filas) | `L07` table-lite | `tabla` |
| ¿Para cuándo y quién? (secuencia de etapas) | `L08` stages | **`etapas`** |
| ¿Qué necesitan de nosotros? (decisión + próximos pasos) | `L09` closing | `tarjetas` + `tabla` |
| ¿De qué se trata? (contexto sin cifras + imagen real) | `L10` text-image | `vinetas` + **`imagen`** |
| ¿Quién lo respalda? (declaración con vocero) | `L11` quote-avatar | **`cita`** |
| ¿Por qué hacemos esto? (solo texto) | `L12` plain-text | **`Deck.texto_pleno`** |
| ¿Cuáles son los pasos o criterios? (≤4 numerados) | `L13` plain-bullets | **`Deck.texto_pleno(..., numerada=True)`** |
| ¿Cuál es la postura del área? (un mensaje que quede sonando) | `L14` plain-statement | **`Deck.texto_pleno(..., mensaje=...)`** |

No caigas por defecto en viñetas ni en `kpi_tiles`. Si hay **una cifra dominante** → `L01`; si son
**partes de un total** → `L06` (no una dona); si hay **evolución en el tiempo** → `L05`; si es una
**secuencia con fechas y responsables** → `L08`. Viñetas de texto plano: solo `L12`–`L14`.

Secuencias tipo como punto de partida del esquema:

- **Comité directivo:** L02 → L04 → L05 → L06 → L11 → L09
- **Presentación con narrativa:** L12 → L13 → L02 → L05 → L14
- **Solicitud de aprobación:** L10 → L01 → L07 → L03 → L09
- **Seguimiento de proyecto:** L02 → L08 → L05 → L11 → L09

## Reglas que no se negocian

- **Cada diapositiva de contenido lleva un layout `L01`–`L14` asignado en el esquema.** Sin layout
  no se redacta ni se genera. La receta (slots + helper exacto) sale de
  `references/06-recetas-de-composicion.md`; no se sustituye ese helper por otro más familiar.
- Respetar la plantilla y la paleta de `assets/`. Nada de colores ni tipografías inventadas.
- **No saturar.** Una idea por diapositiva. Si una diapositiva necesita más de ~5 líneas de
  contenido, se parte en dos. (Umbrales exactos y ajustables en `references/02-reglas-de-diseno.md`,
  a calibrar contra `assets/referencia.pptx`.)
- No omitir datos relevantes: lo que no cabe en la diapositiva va en notas del orador o en un anexo,
  no se borra.
- Estética limpia: márgenes amplios, jerarquía tipográfica clara, la información respira.

## Índice de referencias

| Tema | Archivo |
|---|---|
| Flujo de trabajo detallado y preguntas de arranque | `references/01-flujo-de-trabajo.md` |
| Reglas de diseño (no saturación, jerarquía, uso de la paleta) | `references/02-reglas-de-diseno.md` |
| Formatos de salida: PPTX / HTML / PDF y cómo se generan | `references/03-formatos-de-salida.md` |
| Catálogo de tipos de diapositiva (portada, sección, contenido, cierre…) | `references/04-tipos-de-diapositiva.md` |
| Mapa de layouts PPTX: qué layout de `plantilla.pptx` para cada tipo y cómo se compone (`assets/pptx_kit.py`) | `references/05-mapa-de-layouts.md` |
| Recetas de composición: contenido → layout (L01–L14), elegir por la pregunta del comité, mapeo a helpers | `references/06-recetas-de-composicion.md` |
| Catálogo detallado de los 14 layouts gerenciales (slots, reglas, cuándo usar/evitar) | `assets/layouts-gerenciales.md` |

## Cómo se actualiza esta skill

Cuando se apruebe una presentación nueva que marque estilo, se reemplaza o complementa
`assets/referencia.pptx` y se recalibran los umbrales de `references/02-reglas-de-diseno.md`.
