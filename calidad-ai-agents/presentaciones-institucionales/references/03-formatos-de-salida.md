# Formatos de salida

El usuario elige — **pregúntale siempre** (PPTX / HTML / PDF). Si no tiene
preferencia: **PPTX**. Entrega solo el archivo del formato pedido; no generes
PDF ni PNG sin haberlo solicitado previamente.

## PPTX (nativo, editable)

Se genera con **`assets/pptx_kit.py`** (envuelve `python-pptx`). Detalle de
layouts y helpers en `references/05-mapa-de-layouts.md`. Lo esencial:

- La base **siempre** es `assets/plantilla.pptx` (tema *"Capital 2025 octubre"* +
  Arial). No se crea un `Presentation()` vacío y **no** se parte de
  `assets/referencia.pptx` (tema Office genérico).
- `pptx_kit.Deck()` abre la plantilla y borra sus 43 diapositivas de ejemplo.
- **Los placeholders de `plantilla.pptx` no se usan** (todos tienen `idx=0`, se
  apilan al instanciar). El contenido se **compone con formas por coordenadas**;
  de eso se encargan los helpers del kit. Cada layout aporta solo el mobiliario
  heredado: fondo, franja de sellos, logo, chip de número, "Vigilado Supersalud".
- Colores y fuentes: los de `assets/paleta.md`, ya codificados en el kit. Títulos
  en **Arial Bold** (si la máquina tiene *Roboto Slab*, cambiar `F_TIT` en el kit).
- Estructura de un generador: ver `assets/ejemplos-generados/pptx/ejemplo-gestion-integral-pptx.py`
  (replica el ejemplo HTML). Se escribe un script nuevo por deck
  que importa el kit y llama `Deck.portada / .separador / .contenido` + helpers de
  cuerpo (`vinetas`, `kpi_tiles`, `tarjetas`, `tabla`, `grafica_barras`,
  `grafica_dona`, `barras_horizontales`, `kpi_gigante`, `fuente`).
- Entregar el `.pptx`.

## HTML (para ver en navegador / incrustar)

- Un único archivo `.html` autocontenido (CSS embebido, sin dependencias externas).
- Una `<section>` por diapositiva, tamaño 16:9, navegación con teclado (flechas) y scroll.
- Replica la paleta y las tipografías de `assets/paleta.md` mediante variables CSS.
- La marca (`assets/marca/`) se incrusta como `data:` URIs con
  `assets/empaquetar-html.js` (fuente `*.src.html` con tokens `{{ruta}}` →
  `node empaquetar-html.js entrada.src.html salida.html`; rutas relativas a `assets/`).
- Debe verse bien tanto en pantalla completa como impreso (media print = una diapositiva por página).
- Ejemplo: `assets/ejemplos-generados/html/ejemplo-gestion-integral.html` (+ su `.src.html`).

## PDF (para distribuir, no editable)

Dos rutas según de dónde se parta:

1. **Desde HTML** → render con navegador headless (Chromium/Puppeteer), una
   diapositiva por página, 16:9. Ruta preferida cuando ya se generó el HTML.
2. **Desde PPTX**:
   - **Windows con PowerPoint** (caso habitual de Claude Code aquí) → automatización
     COM, sin LibreOffice:
     ```powershell
     $pp = New-Object -ComObject PowerPoint.Application
     $d  = $pp.Presentations.Open((Resolve-Path salida.pptx), $true, $false, $false)
     $d.SaveAs((Join-Path $pwd "salida.pdf"), 32)   # 32 = ppSaveAsPDF
     $d.Close(); $pp.Quit()
     ```
   - **Otros entornos** → LibreOffice: `soffice --headless --convert-to pdf salida.pptx`.
   Usar la ruta desde PPTX cuando el usuario quiere el PPTX editable **y** un PDF idéntico.

## Revisar el resultado del PPTX

`python-pptx` no renderiza. Para verlo, exportar cada diapositiva a PNG con el
mismo objeto COM (`$d.Slides.Item($i).Export("slide$i.png","PNG",1600,900)`).
Hacerlo **solo si el usuario lo pide** o si hay dudas de maquetación — abrir cada
PNG consume tokens.

## Dependencias de entorno

| Formato | Necesita |
|---|---|
| PPTX | `python-pptx` (+ `assets/plantilla.pptx`) |
| HTML | nada (Node solo para `empaquetar-html.js`) |
| PDF desde HTML | navegador headless (Puppeteer / Chromium) |
| PDF desde PPTX | PowerPoint (COM, Windows) **o** LibreOffice (`soffice`) |
| Revisión visual del PPTX | PowerPoint (COM, Windows) |

Si el entorno no tiene la dependencia, avisar y ofrecer la ruta alternativa
(p. ej. PDF desde HTML) o entregar solo PPTX/HTML.
