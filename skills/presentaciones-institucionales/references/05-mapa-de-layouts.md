# Mapa de layouts (PPTX)

Qué layout de `assets/plantilla.pptx` se usa para cada tipo de diapositiva, y
cómo se le pone el contenido. Aplica **solo al formato PPTX**. La generación está
resuelta en `assets/pptx_kit.py`; este documento explica el porqué.

## Regla base

- La base **siempre** es `assets/plantilla.pptx` (tema de color *"Capital 2025
  octubre"* + fuente *"Fuente Capital" → Arial*). No se crea un `Presentation()`
  vacío y **no** se parte de `assets/referencia.pptx` (ese archivo tiene el tema
  Office genérico: azul‑violáceo `#4472C4`, Calibri).
- **`plantilla.pptx` viene adelgazada** (798 KB, desde los 46 MB originales): sin
  las 43 diapositivas de ejemplo, con solo los **6 layouts** que la skill usa
  (`Portada`, `Contenido Tabla 4`, `Separador1`, `Separador2`, `1_Separador1`,
  `2_Separador1`) y **sin los renders de personaje** — esos se colocan en
  generación desde `assets/marca/personajes/` (`pptx_kit._add_personaje`, lo
  llaman `Deck.portada` y `Deck.separador`). Así los personajes viven una sola
  vez y se comparten con el formato HTML. `Deck` igual borra cualquier diapositiva
  al abrir, por robustez.
- **Los placeholders de `plantilla.pptx` no se usan.** Todos tienen `idx=0`; al
  instanciar una diapositiva se apilan en la misma coordenada y no se pueden
  direccionar. El contenido se **compone con formas colocadas por coordenadas**
  (cajas de texto, rectángulos, tablas y gráficas nativas). Cada layout aporta
  únicamente el *mobiliario*, que se hereda solo:
  - fondo (azul en portada/separadores, `#F5FAFD` claro en contenido),
  - franja de sellos institucionales al pie (ocupa los ~4,2 cm inferiores),
  - logo *Te Cuida* y `www.capitalsalud.gov.co`,
  - formas decorativas (círculos, esquinas),
  - chip con el número de diapositiva,
  - texto vertical *"Vigilado Supersalud"*.

### Regenerar la plantilla adelgazada

Si se actualiza `plantilla.pptx` (nueva versión institucional), volver a
adelgazarla con `assets/optimizar-plantilla.ps1` (PowerPoint COM: borra
diapositivas de ejemplo + layouts no usados + renders de personaje; PowerPoint
limpia los `ppt/media` huérfanos al guardar). Ajustar la lista `$KEEP` si cambian
los nombres de layout, y re‑verificar portadas y separadores.

## Geometría (diapositiva 33,87 × 19,05 cm — 16:9)

| Zona | Valor |
|---|---|
| Margen lateral | 2,2 cm por lado → ancho útil 29,5 cm |
| Topbar (banda azul del título) | y = 0,75 cm · alto 2,5 cm (2,85 con subtítulo) |
| Inicio del contenido | y ≈ 3,8 cm |
| Fin del contenido | y ≈ 14,2 cm (debajo va la franja de sellos) |
| Línea de fuente / nota | y ≈ 13,95 cm |

`pptx_kit` expone estas constantes (`MX`, `CANVAS_Y`, `CANVAS_H`, `CONTENT_W`, …);
los helpers ya colocan el contenido dentro de esta caja, no hay que calcular
coordenadas salvo para ajustes finos.

## Shortlist de layouts

| Tipo de diapositiva | Layout de `plantilla.pptx` | Helper de `pptx_kit` | Notas |
|---|---|---|---|
| Portada | `Portada` | `Deck.portada(kicker, titulo, subtitulo, meta=[], figura="trio-computador")` | Fondo azul + formas + sellos. El personaje se añade en generación desde `marca/personajes/` (`figura=` sin extensión; `None` = sin personaje). Título/subtítulo en texto blanco compuesto, a la derecha. |
| Sección / divisoria | `Separador1`, `Separador2`, `1_Separador1`, `2_Separador1` | `Deck.separador(num, titulo, figura=None, layout=None)` | Personaje a la izquierda (desde `marca/personajes/`); el número ("01") y el título van a la derecha (x ≈ 16,8 cm) para no pisarlo. Sin `figura=`, rota por `_SEP_FIGURAS`; sin `layout=`, rota por `SEPARADORES`. |
| Todo el contenido (texto, KPI, tabla, gráfica, comparación, cierre, anexo) | `Contenido Tabla 4` | `Deck.contenido()` + helpers | Fondo claro institucional, franja de sellos y logo; zona superior limpia. `Deck.contenido()` dibuja el topbar azul y devuelve la diapositiva para componerle el cuerpo. Para anexos: `dark=True` (topbar gris azulado). |

### Helpers de cuerpo (sobre una diapositiva de `Deck.contenido`)

| Contenido | Helper |
|---|---|
| Viñetas | `vinetas(s, [...])` |
| Fila de fichas KPI (2–4) | `kpi_tiles(s, [(rótulo, cifra, delta, pie, alerta), …])` |
| Una cifra grande + explicación | `kpi_gigante(s, "+12 %", "…")` |
| 1–3 tarjetas (comparación, cierre) | `tarjetas(s, [(título, [items], "blanco"|"inst"), …])` |
| Tarjeta ancha única (anexo) | `caja_texto(s, título, [items])` |
| Tabla nativa | `tabla(s, encabezados, filas, total_rows=(…))` |
| Barras verticales (1 o 2 series; resaltar una) | `grafica_barras(s, cats, [(serie, valores)], highlight=i, legend=True)` |
| Dona | `grafica_dona(s, [(cat, valor)], centro=("92,4 %", "…"))` — los % van en la leyenda |
| Barras horizontales | `barras_horizontales(s, [(rótulo, %), …])` |
| Línea de fuente / nota al pie | `fuente(s, "…")` |

## Los otros layouts (ya no están)

La `plantilla.pptx` original tenía 35 layouts (`Contenido 1`…`Contenido 10`,
`Contenido Cifras`, `Tabla Contenido`, `Mapa Bogota`, …): composiciones
pre‑diseñadas muy específicas que la skill nunca usó y que pesaban ~45 MB. La
plantilla adelgazada **solo conserva los 6 layouts de la tabla de arriba**. Si un
encargo necesitara uno de los otros, hay que regenerar la plantilla desde el
original (queda fuera de la skill) o —mejor— componer el layout sobre
`Contenido Tabla 4` con los helpers del kit.

## Fuentes

Los títulos usan **Arial Bold** (`F_TIT` en `pptx_kit.py`). La presentación de
referencia usa además *Roboto Slab* para títulos; si la máquina que genera el
PPTX la tiene instalada, cambiar `F_TIT = "Roboto Slab"`. PowerPoint la sustituye
por Arial si no está, así que dejar Arial es seguro. python‑pptx no incrusta
fuentes en el archivo.

## Verificar el resultado

`python-pptx` no renderiza. Para revisar visualmente en Windows con PowerPoint
instalado, exportar a imagen con COM (no requiere LibreOffice):

```powershell
$pp = New-Object -ComObject PowerPoint.Application
$d  = $pp.Presentations.Open((Resolve-Path salida.pptx), $true, $false, $false)
1..$d.Slides.Count | % { $d.Slides.Item($_).Export("slide$_.png","PNG",1600,900) }
$d.Close(); $pp.Quit()
```

El mismo objeto sirve para PDF: `$d.SaveAs((Join-Path $pwd "salida.pdf"), 32)`
(`ppSaveAsPDF = 32`). Hacerlo solo si el usuario pide PDF o pide revisión visual;
por defecto se entrega únicamente el `.pptx`.
