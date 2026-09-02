# Formatos de salida

El usuario elige entre **PDF, JPG o PNG**. Si no dice nada, **PDF** (mejor para adjuntar a un
procedimiento) más **PNG** (para incrustar).

## Ruta de generación (Mermaid)

1. Escribir el diagrama en Mermaid (`flowchart`) con `classDef` aplicando `assets/paleta-bizagi.md`.
2. Renderizar con `@mermaid-js/mermaid-cli` (`mmdc`):
   - `mmdc -i flujo.mmd -o flujo.pdf` → **PDF** (vectorial, nítido a cualquier tamaño).
   - `mmdc -i flujo.mmd -o flujo.png -s 3` → **PNG** (escala 3x para buena resolución).
   - **JPG**: `mmdc` no lo exporta directo. Generar PNG y convertir
     (`sharp`, ImageMagick `convert flujo.png flujo.jpg`, o similar). Fondo blanco, sin transparencia.
3. Guardar el `.mmd` fuente junto al export.

## Ruta alternativa (draw.io)

- Construir el `.drawio` con la librería BPMN y exportar desde la CLI de draw.io a PDF/PNG/JPG.
- Útil si se necesita un layout más fiel al de Bizagi que el que da Mermaid.

## Múltiples diagramas (variaciones)

- Un archivo por diagrama: `procedimiento-general.pdf`, `procedimiento-proveedor-extranjero.pdf`, …
- Si el usuario quiere un solo PDF, concatenar al final (todas las páginas en un `.pdf`).

## Calidad

- PNG/JPG: mínimo 2000 px de ancho o escala 3x. Nada pixelado.
- Márgenes alrededor del diagrama; que no quede pegado al borde.
- Incluir en el lienzo: título del procedimiento, leyenda de colores de validación, y fecha/versión.

## Dependencias de entorno

| Formato | Necesita |
|---|---|
| PDF / PNG (Mermaid) | `@mermaid-js/mermaid-cli` (`mmdc`) + Chromium headless |
| JPG | lo anterior + un conversor de imagen (`sharp` / ImageMagick) |
| Ruta draw.io | `drawio` CLI (Electron) |

Si el entorno no tiene `mmdc` (p. ej. Windows local sin instalar), avisar y ofrecer entregar el
código Mermaid + un render provisional, o instalar el toolchain primero.
