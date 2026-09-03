# Formatos de salida

> **Entorno objetivo: Claude web / app (claude.ai), no Claude Code local.** La ruta de generación
> de abajo (Mermaid + `mmdc`) es la que se documentó primero, pero **no está confirmado** que el
> sandbox de código de claude.ai permita instalar y correr `@mermaid-js/mermaid-cli` +
> Chromium headless igual que en un entorno local. Antes de asumir que esta ruta funciona tal cual,
> probarla directamente en claude.ai. Si el sandbox no lo permite, la alternativa es apoyarse en
> Artifacts (bloque ```mermaid```, que se renderiza nativo sin CLI) y dejar la exportación a
> PDF/PNG/JPG a cargo de lo que ofrezca esa UI, no de un comando de la skill. Ver
> `../assets/PENDIENTE.md`.

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

Si el sandbox de claude.ai no tiene `mmdc` disponible ni permite instalarlo, avisar y entregar el
código Mermaid + un render provisional vía Artifact (bloque ```mermaid```), en vez de asumir que el
export a PDF/JPG/PNG por CLI va a funcionar.
