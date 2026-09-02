# Flujo de trabajo detallado

## 1. Preguntas de estructura (obligatorias, antes de dibujar)

| Pregunta | Para qué |
|---|---|
| ¿Cuál es el **nombre del procedimiento** y su objetivo en una frase? | Título y alcance. |
| ¿Dónde **empieza** (evento disparador) y dónde **termina** (resultado)? | Evento inicial y final. |
| ¿Tiene **fases** o etapas macro? ¿Cuáles? | Bandas/fases del diagrama. |
| ¿Qué **responsables o roles** intervienen? ¿Se quiere separar por carriles (*lanes*)? | Estructura de carriles. |
| ¿Hay otras divisiones (sistema, ubicación, área)? | Carriles adicionales o anotaciones. |
| ¿El procedimiento **cambia según la entidad, el caso o el tipo**? (variaciones) | Decide si es 1 diagrama o general + N. Ver `04-variaciones-de-procedimiento.md`. |
| ¿Formato de entrega: **PDF, JPG o PNG**? | Exportación. |

No sigas hasta tener respondidas al menos: inicio/fin, fases sí/no, responsables sí/no,
variaciones sí/no.

## 2. Redacción de los pasos

- Lista numerada de pasos, cada uno **≤ 100 caracteres** (`02-reglas-de-diagramacion.md`).
- Por cada paso: quién lo hace (rol) y si es actividad, decisión, subproceso o espera.
- Marca los puntos de decisión con sus salidas (Sí/No, o las opciones reales).

Devuelve esta lista al usuario para confirmar **antes** de construir el diagrama.

## 3. Construcción

- Un carril por responsable (si se pidió separación por roles).
- Fases como bandas verticales sobre los carriles (si aplica).
- Flujo de izquierda a derecha, de arriba abajo dentro del carril.
- Si hay variaciones: general + uno por variación (`04-variaciones-de-procedimiento.md`).

## 4. Validación por colores

Aplica `03-validacion-por-colores.md` a cada paso. Entrega la tabla de validación junto al diagrama.

## 5. Exportación y entrega

- Exporta al formato pedido (`05-formatos-de-salida.md`).
- Entrega: diagrama(s) + tabla de validación + lista de pasos en texto (para trazabilidad).
