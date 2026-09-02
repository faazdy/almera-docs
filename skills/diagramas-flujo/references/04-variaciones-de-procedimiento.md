# Variaciones del procedimiento

Un procedimiento tiene **variaciones** cuando, según la entidad, el tipo de caso o el canal, los
pasos cambian (no solo una decisión puntual, sino un tramo distinto del flujo).

Ejemplos: "si el proveedor es extranjero, el flujo de pago es otro"; "para contratos de obra hay
dos aprobaciones extra"; "las PQR por canal telefónico saltan el registro web".

## Regla de entrega

Cuando hay variaciones se entregan:

1. **Un diagrama general** — el tronco común del procedimiento, respetando los pasos que aplican
   siempre. En el punto donde el flujo se bifurca por variación, se marca con una decisión o una
   nota que remite a los diagramas específicos ("Ver diagrama: proveedor extranjero").
2. **Un diagrama por cada variación** — el flujo completo de ese caso, resaltando (con nota o
   color de anotación, no de tipo) los pasos que difieren del general.

No se mete todo en un solo diagrama lleno de compuertas: se vuelve ilegible y rompe la regla de
"la información respira".

## Cómo decidir si es variación o solo una decisión

| Situación | Tratamiento |
|---|---|
| Cambia 1 salida de 1 decisión, luego el flujo se reúne | Decisión normal dentro de **un** diagrama. |
| Cambia un tramo de varios pasos / carriles según el caso | **Variación** → general + diagrama propio. |
| El evento inicial o final es distinto según el caso | **Variación**. |

## Nomenclatura

- Diagrama general: `<Procedimiento> — General`.
- Variaciones: `<Procedimiento> — <Nombre de la variación>` (p. ej. "— Proveedor extranjero").
- Numeración de pasos consistente entre general y variaciones cuando el paso es el mismo.

## Validación

Cada diagrama (general y cada variación) lleva su propia tabla de validación por colores
(`03-validacion-por-colores.md`).
