# Diagrama de referencia — ejemplo provisional

Este ejemplo (`ejemplo-pqrs.*`) es un **sustituto temporal** del diagrama de referencia real.
Existe para que la skill tenga contra qué calibrar mientras llega un export de Bizagi Modeler.

## Qué contiene

| Archivo | Qué es |
|---|---|
| `ejemplo-pqrs.mmd` | Fuente Mermaid del diagrama, lista para renderizar con `mmdc`. |
| `ejemplo-pqrs.md` | Diagrama renderizable + tabla de pasos + tabla de validación por colores. |

## Cuándo se reemplaza

Cuando se tenga un **export real** (PDF o PNG) de un procedimiento del repositorio de Bizagi:

1. Guardarlo aquí como `diagrama-referencia.<pdf|png>` (y el `.bpm` si se consigue).
2. Comparar colores, tipografía, grosores y forma de los nodos contra `../paleta-bizagi.md`
   y corregir los hex de esa tabla y de `../plantilla.mmd`.
3. Quitar la etiqueta "PROVISIONAL" de `../paleta-bizagi.md`.
4. Este ejemplo puede quedarse como caso de prueba de la skill.
