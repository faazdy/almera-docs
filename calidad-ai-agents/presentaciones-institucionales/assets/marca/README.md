# Biblioteca de marca — presentaciones institucionales

Recursos gráficos extraídos de `../referencia.pptx` (Capital Salud EPS-S). La skill los usa
para que las presentaciones se vean como las institucionales, no solo con la paleta correcta.

## Contenido

### `fondos/`
| Archivo | Uso | Notas |
|---|---|---|
| `portada.jpg` | Fondo **solo de la portada**. | Foto de un punto de atención con viraje azul. Encima va un degradado azul (`#003971`→`#007ACC`, ~80% opacidad) para contraste del texto blanco. |
| `separador.jpg` | Fondo de las **diapositivas separadoras / de sección**. | Degradado azul diagonal `#004C97`→`#5AB5E6`. Texto en blanco. |
| `uso/portada-main.png` | **Referencia de composición** de la portada. | Logo "Te Cuida" arriba-izq · personaje (trío) a la izquierda sobre óvalo claro · título en blanco, mayúsculas, alineado a la derecha · subtítulo (dirección) + fecha/evento · píldora `www.capitalsalud.gov.co` abajo-izq · franja de sellos abajo · microtexto "Vigilado Supersalud" rotado en el borde izquierdo. |
| `uso/separador.png` | **Referencia de composición** del separador de sección. | Igual que la portada pero sobre **fondo azul sólido** (sin foto): logo arriba-izq, **un** personaje a la izquierda sobre círculo tenue, título/nº de sección a la derecha en blanco, píldora de URL y franja de sellos abajo. |

### `personajes/` — "los muñequitos"
Ilustraciones 3D (estilo Pixar) de servidores con chaqueta azul de Capital Salud. PNG con
transparencia. **Uso decorativo: máximo uno por diapositiva**, anclado a una esquina inferior,
sin tapar texto. Van bien en separadores y en el cierre; en diapositivas de contenido, solo si
sobra espacio.

| Archivo | Descripción |
|---|---|
| `trio-computador.png` | Tres personas alrededor de un monitor. |
| `trio-sello.png` | Tres personas (médico, administrativo, brigadista) con un sello de verificación. |
| `hombre-checklist.png` | Hombre con gafas señalando una lista de chequeo. |
| `mujer-checklist.png` | Mujer señalando una lista de chequeo. |
| `duo-laptop-ok.png` | Mujer en portátil y hombre de pie con tablet haciendo señal de "OK". |

### `iconos/`
Iconos de línea a dos tonos de azul (trazo `#004C97` + acento `#5AB5E6`). PNG con transparencia,
~1:1. Se usan junto al título de una diapositiva de contenido (tamaño ~4 cqw) o para marcar
ítems de una lista. **No recolorear.**

| Archivo | Representa |
|---|---|
| `diamante.png` | Valor, calidad, resultado clave. |
| `formacion-salud.png` | Formación / capacitación en salud. |
| `portal-info.png` | Portal, información, canal digital. |
| `atencion-persona.png` | Atención a la persona / usuario. |
| `factura-ok.png` | Facturación, pago, cuenta validada. |
| `persona-busqueda.png` | Consulta, verificación, auditoría. |
| `documento-agenda.png` | Documento, plan, agenda, cronograma. |
| `menos-circulo.png` | Resta / exclusión / dato negativo. |

### `logos/`
| Archivo | Uso |
|---|---|
| `te-cuida.png` | Lockup "Capital Salud Te Cuida" (azul). Para fondos claros; en fondos azules va en blanco (`filter:brightness(0) invert(1)`). Esquina superior de cada diapositiva. |
| `sellos-institucionales.png` | Franja con sellos: Capital Salud, ICONTEC ISO 9001, IQNET, Alcaldía Mayor de Bogotá, Secretaría de Salud, Bogotá. Va en el pie de **todas** las diapositivas, centrada. |
| `url-blanco.png` | `www.capitalsalud.gov.co` en blanco. Pie de portada y separadores (fondo azul). |
| `uso/image.png` | **Referencia de composición** de una diapositiva de contenido: fondo azul muy claro · **banner azul oscuro redondeado arriba** con Título (blanco, negrita) + subtítulo/resumen dentro del mismo banner · logo "Te Cuida" arriba-derecha · área de contenido libre debajo · franja pálida de ancho completo con los sellos al pie · microtexto "Vigilado Supersalud" rotado en el borde izquierdo. |

## Cómo se actualiza

Si cambia la plantilla institucional, volver a extraer estos recursos del nuevo `referencia.pptx`
(descomprimir el `.pptx` y revisar `ppt/media/`), conservando los mismos nombres de archivo.

## `personajes/` — también los usa el PPTX

`plantilla.pptx` viene adelgazada y **sin** los renders de personaje en sus layouts.
Al generar PPTX, `pptx_kit` coloca el personaje de portada y de cada separador
tomándolo de `personajes/*.png` (`Deck.portada(..., figura=...)`,
`Deck.separador(..., figura=...)`, sin extensión). Es la misma carpeta que usa el
HTML, así que estos archivos son la única fuente de personajes para ambos formatos.

## Nota para el formato HTML

`03-formatos-de-salida.md` exige un `.html` autocontenido. Al generar HTML, estos archivos se
incrustan como `data:` URIs con `../empaquetar-html.js` (ver el ejemplo en
`../ejemplos-generados/html/`). No se enlazan como archivos externos.
