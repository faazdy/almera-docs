---
name: diagramas-flujo
description: >-
  Genera diagramas de flujo de procedimientos, visualmente consistentes con los diagramados en
  Bizagi Modeler, y los exporta a PDF, JPG o PNG. Úsala cuando el usuario pida "un diagrama de
  flujo", "diagramar un procedimiento", "un flujgrama", "el flujo de un proceso", pase la
  descripción textual de un procedimiento y pida representarlo, o pida revisar/validar un
  diagrama existente. Aplica reglas fijas: máximo 100 caracteres por actividad, validación por
  colores (verde/amarillo/rojo), paleta consistente, y manejo de variaciones del procedimiento
  (un diagrama general + N diagramas por variación). Siempre parte de un diagrama de referencia.
---

# Diagramas de flujo de procedimientos

Produce diagramas de flujo que se ven como los del repositorio de procedimientos en Bizagi
Modeler, aunque el entregable sea una imagen o un PDF (no un archivo `.bpm` editable).

## Antes de generar nada

Revisa que existan en `assets/`:

- `assets/diagrama-referencia.*` — export (PDF/PNG) de un procedimiento ya diagramado en Bizagi,
  que fija el estilo.
- `assets/paleta-bizagi.md` — colores por tipo de elemento (evento, actividad, decisión, carril…).

Si falta alguno, díselo al usuario. Ver `assets/PENDIENTE.md`.

## Flujo de trabajo

1. **Preguntar la estructura general** antes de diagramar (`references/01-flujo-de-trabajo.md`):
   - ¿El procedimiento tiene **fases** (etapas macro)?
   - ¿Hay **responsables / roles** que separen el flujo en carriles (*lanes*)?
   - ¿Otras divisiones generales (sistemas, ubicaciones)?
   - ¿El procedimiento tiene **variaciones**? (con ciertas entidades o casos, los pasos cambian).
2. **Redactar los pasos** cumpliendo las reglas de diagramación (`references/02-reglas-de-diagramacion.md`):
   toda actividad/acción **≤ 100 caracteres**, en infinitivo o verbo + objeto.
3. **Construir el diagrama**:
   - Si **no hay variaciones**: un diagrama.
   - Si **hay variaciones**: un **diagrama general** que respeta los pasos comunes + **un diagrama
     por cada variación** (`references/04-variaciones-de-procedimiento.md`).
4. **Validar por colores** (`references/03-validacion-por-colores.md`): marcar cada paso como
   verde / amarillo / rojo con un comentario. Entregar esa tabla junto al diagrama.
5. **Exportar** al formato pedido: **PDF, JPG o PNG** (`references/05-formatos-de-salida.md`).
6. **Entregar** el/los diagrama(s) + la tabla de validación + los pasos en texto.

## Reglas que no se negocian

- **≤ 100 caracteres** por actividad o acción. Si un paso no cabe, se parte en dos pasos o se
  reescribe; no se abrevia con jerga.
- Paleta y estilo de `assets/` para todo elemento. Nada de colores por defecto del renderizador.
- Validación por colores en **todos** los diagramas entregados, con leyenda visible:
  - 🟢 **Verde:** todo correcto.
  - 🟡 **Amarillo:** parcialmente correcto, requiere revisar.
  - 🔴 **Rojo:** revisar obligatoriamente.
- Con variaciones: siempre diagrama general **+** los diagramas de cada variación. No mezclar todas
  las variaciones en un solo diagrama con mil compuertas.
- Preguntar la estructura general **antes** de dibujar, no después.
- **Sintaxis Mermaid válida, siempre**: nunca un salto de línea real dentro de una etiqueta
  (usa `<br/>`); en aristas con etiqueta, el tipo de línea de apertura y cierre debe coincidir
  (sólida↔sólida, punteada↔punteada — nunca `-- "texto" -.->`). Relee el `.mmd` completo contra
  esto antes de entregarlo: un solo carácter mal puesto hace que el cliente muestre el código en
  vez del diagrama. Ver `references/02-reglas-de-diagramacion.md` → "bug confirmado".

## Índice de referencias

| Tema | Archivo |
|---|---|
| Flujo de trabajo y preguntas de estructura | `references/01-flujo-de-trabajo.md` |
| Reglas de diagramación (100 caracteres, nomenclatura, tipos de nodo) | `references/02-reglas-de-diagramacion.md` |
| Validación por colores (verde / amarillo / rojo) | `references/03-validacion-por-colores.md` |
| Variaciones del procedimiento (general + N) | `references/04-variaciones-de-procedimiento.md` |
| Formatos de salida: PDF / JPG / PNG y cómo se generan | `references/05-formatos-de-salida.md` |

## Cómo se actualiza esta skill

Cuando cambie el estándar de Bizagi Modeler, se reemplaza `assets/diagrama-referencia.*` y se
actualiza `assets/paleta-bizagi.md`.
