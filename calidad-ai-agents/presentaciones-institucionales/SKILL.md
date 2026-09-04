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
   - **Pregunta siempre el formato de entrega: ¿PPTX, HTML o PDF?** No lo asumas
     (ver `references/03-formatos-de-salida.md`). Si el usuario no tiene
     preferencia, usa PPTX.
   - Pregunta además, si no está claro:
     - Objetivo y audiencia (comité directivo, capacitación, cliente externo…).
     - Contenido base: ¿hay un texto, informe o bullets de partida, o se construye desde cero?
     - Extensión aproximada (nº de diapositivas) y si hay fecha/evento.
2. **Proponer un esquema** (título por diapositiva + idea central de cada una) y esperar visto bueno
   antes de producir. No generes el archivo final sobre un esquema no confirmado.
3. **Redactar el contenido** aplicando las reglas de diseño (`references/02-reglas-de-diseno.md`):
   una idea por diapositiva, poco texto, apoyo visual.
4. **Generar el entregable** en el formato pedido (`references/03-formatos-de-salida.md`):
   - **PPTX** — escribe un script que importe `assets/pptx_kit.py` y componga el deck
     con `Deck.portada / .separador / .contenido` + helpers de cuerpo. Guía completa
     (layouts, geometría, qué helper para qué contenido) en `references/05-mapa-de-layouts.md`;
     modelo de script en `assets/ejemplos-generados/pptx/ejemplo-gestion-integral-pptx.py`.
     Entrega solo el `.pptx`. Renderiza a PNG/PDF **solo si el usuario lo pide** (consume tokens revisarlos).
   - **HTML** — archivo autocontenido; marca incrustada con `assets/empaquetar-html.js`.
     Modelo en `assets/ejemplos-generados/html/ejemplo-gestion-integral.src.html`.
   - **PDF** — desde HTML (headless) o desde PPTX (PowerPoint COM en Windows / LibreOffice).
5. **Entregar y ofrecer ajustes** (reordenar, condensar, cambiar formato).

Detalle en `references/01-flujo-de-trabajo.md`.

## Reglas que no se negocian

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

## Cómo se actualiza esta skill

Cuando se apruebe una presentación nueva que marque estilo, se reemplaza o complementa
`assets/referencia.pptx` y se recalibran los umbrales de `references/02-reglas-de-diseno.md`.
