# Estado de insumos — presentaciones institucionales

## Estructura de `assets/`

```
assets/
  plantilla.pptx        insumo — plantilla ADELGAZADA (~0,8 MB): 6 layouts, sin diapos de
                        ejemplo, sin renders de personaje. Ruta fija (pptx_kit la carga).
  referencia.pptx       guía de estética (no es base de generación). Ruta fija.
  Tema1.thmx            tema Office exportado. NO va en el .skill (34 MB, no se usa en runtime).
  paleta.md
  marca/                fondos, personajes, iconos, logos. personajes/ los usa HTML y PPTX.
  pptx_kit.py           herramienta PPTX (Deck + helpers). La importan los generadores.
  consolidar.py         herramienta de consolidacion: pasa presentaciones ya hechas por
                        otros (con o sin la skill) a la plantilla institucional, sin
                        cambiar su contenido. Importa pptx_kit. Ver
                        references/07-consolidar-presentaciones.md.
  empaquetar-html.js    herramienta HTML (usa ./marca/). Debe vivir junto a marca/.
  optimizar-plantilla.ps1   regenera plantilla.pptx adelgazada (PowerPoint COM).
  PENDIENTE.md          este archivo
  ejemplos-generados/
    pptx/  ejemplo-gestion-integral-pptx.py  (generador; importa ../../pptx_kit)
           ejemplo-gestion-integral.pptx     (salida, 20 diapositivas, ~3,2 MB)
           ejemplo-gestion-integral-pptx.pdf (salida opcional; se puede borrar)
    html/  ejemplo-gestion-integral.src.html (fuente con tokens {{ruta}})
           ejemplo-gestion-integral.html     (salida empaquetada)
```

## Insumos montados

| Archivo | Qué es | Estado |
|---|---|---|
| `plantilla.pptx` | Plantilla PPTX **adelgazada** (~0,8 MB desde 46 MB): 6 layouts, sin diapos de ejemplo, sin renders de personaje. Tema "Capital 2025 octubre" + Verdana. Base del formato PPTX. | 🟢 Montado |
| `referencia.pptx` | Presentación aprobada; guía de estética y densidad. Su *tema* es Office genérico → no es base de generación. | 🟢 Montado |
| `paleta.md` | Colores oficiales (hex) + tipografías + tamaños. | 🟢 Montado — del tema "Capital 2025 octubre" |
| `Tema1.thmx` | Tema de Office exportado del pptx. No se usa en runtime; queda fuera del `.skill`. | 🟢 Montado |
| `marca/` | Fondos, personajes, iconos y logos. `personajes/` es la fuente de personajes para HTML **y** PPTX. Ver `marca/README.md`. | 🟢 Montado |
| `pptx_kit.py` | Utilidades de generación PPTX (`Deck` + helpers de cuerpo). Coloca los personajes desde `marca/personajes/`. | 🟢 Herramienta |
| `empaquetar-html.js` | Empaquetador Node: `*.src.html` con tokens `{{ruta}}` → HTML con la marca como `data:` URIs. | 🟢 Herramienta |
| `optimizar-plantilla.ps1` | Regenera `plantilla.pptx` adelgazada vía PowerPoint COM (si cambia la plantilla institucional). | 🟢 Herramienta |
| `ejemplos-generados/pptx/` | Generador de ejemplo PPTX (`ejemplo-gestion-integral-pptx.py`) + su salida (20 diapositivas, ~3,2 MB). | 🟢 Ejemplo |
| `ejemplos-generados/html/` | Ejemplo HTML: deck mixto talento humano + financiero (fichas KPI, barras 1 y 2 series, dona, tabla, cartera por edades, ejecución presupuestal). Datos ficticios. | 🟢 Ejemplo |

## Resuelto

### Estrategia de generación PPTX
- Base = `plantilla.pptx` (único con el tema institucional). `referencia.pptx` **no** se usa como base.
- Los placeholders de `plantilla.pptx` tienen todos `idx=0` → inservibles para posicionar. Se
  descartó (a) limpiar la plantilla y (b) clonar de `referencia.pptx`. Solución: **componer el
  contenido con formas por coordenadas** (opción (c) llevada al extremo). Implementado en `pptx_kit.py`.
- `Deck()` borra cualquier diapositiva al abrir (por robustez).
- Shortlist de layouts usados y mapa de contenido → `references/05-mapa-de-layouts.md`.

### Peso de la plantilla / empaquetado
- `plantilla.pptx` pasó de 46 MB a ~0,8 MB con `optimizar-plantilla.ps1`: se quitaron las 43
  diapositivas de ejemplo, 29 layouts que la skill no usa, y los 5 renders 3D de personaje
  incrustados en los layouts de portada/separador.
- Los personajes se colocan ahora en generación desde `marca/personajes/` (`pptx_kit._add_personaje`).
  Una sola copia, compartida con el formato HTML.
- El deck de ejemplo bajó de 9,6 MB a ~3,2 MB.
- `Tema1.thmx` (34 MB) y los renders `.html`/`.pptx`/`.pdf` de `ejemplos-generados/` quedan
  **fuera del `.skill`** (regenerables). El `.skill` empaquetado pesa ~8–9 MB (lo domina `marca/`).

### Entorno
- Corre en **Claude Code en Windows**. Instalados: Python 3.13 + `python-pptx`, y PowerPoint
  (automatización COM). No hay LibreOffice y no hace falta:
  - PPTX → `python-pptx` vía `pptx_kit.py`.
  - PDF desde PPTX → PowerPoint COM (`SaveAs … 32`).
  - Revisión visual del PPTX → PowerPoint COM (`Slides.Item(i).Export … "PNG"`).
  - PDF desde HTML → navegador headless (pendiente de probar con puppeteer).

### Documentación
- `references/05-mapa-de-layouts.md` — creado.
- `references/03-formatos-de-salida.md` — reescrito (kit PPTX, empaquetado HTML, PDF sin LibreOffice).
- `SKILL.md` — flujo con rama por formato; pregunta de formato obligatoria.

## Pendiente

- [ ] Añadir a `02-reglas-de-diseno.md` / `04-tipos-de-diapositiva.md` el uso de `marca/`
      (fondo de portada vs. separador, un personaje máx. por diapositiva, iconos en títulos,
      franja de sellos en el pie).
- [x] Helpers de `pptx_kit.py` que pedía `references/06-recetas-de-composicion.md`:
      `barra_apilada` (L06 · distribución 100%), `etapas` (L08 · proceso con avance),
      `imagen` (L10 · imagen de contenido, no personaje), `cita` (L11 · vocería con avatar) y
      `Deck.texto_pleno` (L12–L14 · marco estándar) — **añadidos y verificados con render**.
      El deck de ejemplo usa `barra_apilada`, `etapas` y `cita` (diapositivas 15, 16, 18).
      Quedan por coordenadas L04 (columna lateral), L05 (split) y L09 (bloque de decisión 34%).
- [ ] Probar la ruta **PDF desde HTML** con puppeteer/Chromium en esta máquina.
- [ ] `pptx_kit.py`: si se aprueba instalar *Roboto Slab*, cambiar `F_TIT` y recalibrar tamaños
      de título contra `referencia.pptx`.
- [ ] Calibrar umbrales de densidad de `02-reglas-de-diseno.md` contra `referencia.pptx`
      (nº máx. de viñetas, líneas por diapositiva, etc.).
- [x] Modo **consolidar** (`consolidar.py`): pasar presentaciones ya hechas por otros
      empleados (con o sin la skill) a `plantilla.pptx` sin tocar su contenido —
      `inventario` (clasifica y arma un plan editable) + `generar` (arma el pptx).
      Probado con `referencia.pptx` (plantilla vieja, 10 diapositivas) +
      `ejemplos-generados/pptx/ejemplo-gestion-integral.pptx` (20, generado con la skill):
      el segundo sale idéntico a como se generó; el primero conserva todo su contenido,
      reencuadrado bajo la bandera nueva (algunas diapositivas muy densas de la plantilla
      vieja quedan con letra chica y avisadas para recomponer o partir — decisión del
      usuario, no de la skill). Documentado en `references/07-consolidar-presentaciones.md`.
      Feedback de la primera revisión, ya aplicado y verificado con render:
      separadores saturados (con puntos a tratar) se limpian solos — los puntos se sacan
      a una diapositiva de contenido aparte (tipo "puntos") — y `inventario` acepta
      `--portada-consolidada` para anteponer una portada "Consolidado de presentaciones"
      con las direcciones detectadas.
