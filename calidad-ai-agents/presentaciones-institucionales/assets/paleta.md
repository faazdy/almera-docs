# Paleta y tipografías institucionales

> Fuente de verdad: el tema de `plantilla.pptx` (esquema de color **"Capital 2025 octubre"**,
> esquema de fuentes **"Fuente Capital"**). Los usos prácticos (qué color/fuente se aplica a qué)
> están calibrados contra `ejemplo1_presentacion.pptx`.
> Los valores hex de la versión anterior de este archivo eran un muestreo manual aproximado;
> quedan reemplazados por los del tema.

## Colores del tema (canónicos)

Los 10 colores del esquema del tema, en el orden en que PowerPoint los expone.

| Slot del tema | Nombre | Hex | Rol |
|---|---|---|---|
| `dk1` / texto 1 | Negro | `#000000` | Color de texto por defecto sobre fondo claro |
| `lt1` / fondo 1 | Azul hielo | `#D6F0F5` | Fondo institucional de diapositiva / bandas |
| `dk2` / texto 2 | Azul marino | `#004C97` | Texto sobre fondo claro cuando se quiere azul; = `accent1` |
| `lt2` / fondo 2 | Azul hielo | `#D6F0F5` | Fondo alternativo (mismo que `lt1`) |
| `accent1` | Azul marino | `#004C97` | **Acento principal**: títulos, barras de sección, encabezados de tabla |
| `accent2` | Azul eléctrico | `#0085CF` | Acento secundario / 2ª serie de gráfica |
| `accent3` | Azul cielo | `#5AB5E6` | 3ª serie de gráfica |
| `accent4` | Turquesa | `#33B4CF` | 4ª serie de gráfica |
| `accent5` | Cian pálido | `#B9E5E5` | Rellenos suaves / 5ª serie |
| `accent6` | Azul grisáceo claro | `#9DCDEA` | Rellenos suaves / 6ª serie |
| `hlink` | Cian enlace | `#00ABD1` | Hipervínculos |
| `folHlink` | Azul profundo | `#002060` | Hipervínculos visitados |

## Roles de trabajo (lo que se usa al redactar diapositivas)

| Rol | Hex | Uso |
|---|---|---|
| Primario | `#004C97` | Títulos, barras de sección, encabezado de tabla, línea/elemento de marca |
| Azul encabezado (variante oscura) | `#003971` | Subtítulos y encabezados largos — variante más oscura que usa la presentación de referencia. Opcional; si hay duda, usar el primario `#004C97` |
| Neutro oscuro (texto) | `#000000` | Cuerpo de texto |
| Fondo institucional | `#D6F0F5` | Fondo de diapositiva y bandas del tema |
| Zona de contenido | `#FFFFFF` | Fondo de cajas/paneles de contenido sobre el fondo institucional |
| Panel gris suave | `#F8F8F8` | Fondo de recuadros neutros, notas al pie, anexos |
| Acento | `#0085CF` | Resaltar **un** dato por diapositiva (una cifra, una palabra, una barra) |

- No introducir ningún color que no esté en este archivo.
- El acento es para una sola cosa por diapositiva. Si todo está resaltado, nada lo está.

## Colores para gráficas (en este orden)

`#004C97` · `#0085CF` · `#5AB5E6` · `#33B4CF` · `#B9E5E5` · `#9DCDEA`

- Serie única: `#004C97`. La barra/segmento a resaltar: `#0085CF`; el resto en `#B9E5E5` o gris `#F8F8F8`.
- Nada de colores por defecto de Excel / de la librería de gráficas.

## Tipografías

Esquema de fuentes del tema: **"Fuente Capital"** → **Verdana** como fuente mayor y menor.
La presentación de referencia usa además **Roboto Slab** para títulos y encabezados.

| Rol | Fuente | Peso | Notas |
|---|---|---|---|
| Título de diapositiva / encabezados | Roboto Slab | Bold | Como en `ejemplo1_presentacion.pptx`. Fallback si no está instalada: **Verdana Bold** |
| Cuerpo de texto, viñetas, tablas | Verdana | Regular / Bold para énfasis | Fuente del tema |
| Cifras destacadas (KPI) | Verdana | Bold | Consistente con el título de esa diapositiva |
| Notas al pie / fuentes / pie de página | Verdana | Regular | — |

- No sustituir por otras fuentes. Calibri / Aptos aparecen como restos en algunos layouts de la
  plantilla: son solo *fallback* del sistema, no se usan a propósito.
- No mezclar más de estas dos familias (Roboto Slab + Verdana) en una misma presentación.

## Tamaños de referencia

Diapositiva 16:9 (33,87 × 19,05 cm / 13,33″ × 7,5″). Tamaños en puntos, calibrados contra
`ejemplo1_presentacion.pptx`. Ajustar dentro de estos rangos; **no** reducir la fuente por
debajo del mínimo para forzar contenido (se parte la diapositiva).

| Elemento | Tamaño | Rango aceptable |
|---|---|---|
| Título de portada | 54 pt | 44–54 pt |
| Subtítulo de portada | 24 pt | 20–24 pt |
| Fecha / evento en portada | 18 pt | 16–18 pt |
| Título de sección (divisoria) | 28 pt | 24–32 pt |
| Título de diapositiva de contenido | 28–32 pt | 24–36 pt |
| Cifra destacada (KPI) | 48–54 pt | 36–54 pt |
| Cuerpo / viñetas | 14 pt | 12–18 pt |
| Texto de tabla | 12–14 pt | 10–14 pt |
| Notas al pie / fuente | 9 pt | 8–10 pt |

## Cómo se actualiza

Si cambia la plantilla institucional, volver a extraer el esquema de color y de fuentes del
`theme` de `plantilla.pptx` y recalibrar los usos y tamaños contra la nueva presentación de
referencia.
