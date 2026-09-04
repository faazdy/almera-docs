# Validación por colores

Todo diagrama entregado lleva una capa de validación. Sirve para que quien revisa el
procedimiento vea de un vistazo qué está sólido y qué no.

## Significado

| Color | Significado | Cuándo se usa |
|---|---|---|
| 🟢 Verde | Todo correcto | El paso está claro, es correcto y no requiere acción. |
| 🟡 Amarillo | Parcialmente correcto, requiere revisar | Falta un dato, hay una redacción ambigua, o una suposición que confirmar. |
| 🔴 Rojo | Revisar obligatoriamente | Hay un error, un vacío que rompe el flujo, o contradice otra fuente. |

## Cómo se muestra

1. **Marca en el nodo**: un pequeño indicador de color junto a la actividad (borde de color,
   ícono o etiqueta), sin cambiar el color de relleno que indica el tipo de elemento.
2. **Tabla de validación** que acompaña al diagrama:

```markdown
| # | Paso | Color | Comentario |
|---|------|-------|------------|
| 3 | ¿La solicitud está completa? | 🟡 | No está definido qué campos son obligatorios. |
| 5 | Notificar al solicitante | 🔴 | No se indica por qué medio ni en qué plazo. |
| 7 | Archivar la solicitud | 🟢 | — |
```

3. **Leyenda** visible en el propio diagrama con los tres colores y su significado.

## Reglas

- Cada paso tiene exactamente un color.
- Amarillo y rojo **siempre** llevan comentario que diga qué revisar. Verde puede ir sin comentario.
- Si hay diagrama general + variaciones, cada diagrama lleva su propia tabla.
- Al re-generar un diagrama tras las correcciones, actualizar los colores (idealmente todo a verde).
