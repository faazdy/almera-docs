# Consolidar presentaciones ya hechas

Modo distinto al de generación (`01`–`06`): en vez de redactar contenido nuevo,
toma **presentaciones que ya hizo otro empleado** — con la plantilla vieja, con
otra plantilla, o incluso ya generadas con esta skill — y las pasa a la
plantilla y la paleta institucional para que una consolidación (varios
informes de área juntos en un solo deck, por ejemplo) se vea de una sola pieza.

**Por defecto, el contenido no cambia.** No se borra texto, no se quitan
imágenes, no se recorta información. Lo único que se ajusta es la forma: el
título pasa a la bandera institucional, y el resto del contenido se reencuadra
en la zona útil de `plantilla.pptx`. Ver también `SKILL.md` → "Consolidar
presentaciones existentes" (disparadores y flujo con el usuario) y
`05-mapa-de-layouts.md` (la plantilla y su geometría, que aquí se reutiliza tal
cual).

## Cuándo usarlo

- El usuario tiene 2+ archivos `.pptx` de distintos empleados/áreas y quiere
  **un solo deck** con la misma plantilla y la misma bandera de títulos.
- Uno o más de esos archivos **no** se hicieron con esta skill (plantilla
  institucional vieja, plantilla de Office genérica, o cualquier otra).
- También aplica si todos vienen de esta skill: sirve para juntarlos sin
  reabrir cada script generador.

No es el modo a usar si el pedido es "redactar" o "resumir" un informe en
diapositivas nuevas — eso es el flujo normal (`01-flujo-de-trabajo.md`).

## Herramienta: `assets/consolidar.py`

Dos pasos, con revisión del usuario entre uno y otro. **No se pasa directo al
paso 2 sin que el usuario apruebe el plan** — es la misma regla de "esquema
previo obligatorio" del flujo de generación, aplicada aquí al plan.

```
python assets/consolidar.py inventario area1.pptx area2.pptx area3.pptx -o plan.json
#  -> analiza cada diapositiva de cada archivo, imprime una tabla resumen y
#     escribe plan.json (editable) con una entrada por diapositiva

#  ... el usuario revisa/edita el plan (ver "El plan" abajo) ...

python assets/consolidar.py generar plan.json -o consolidado.pptx
#  -> genera el pptx consolidado sobre plantilla.pptx e imprime un informe:
#     que se hizo con cada diapositiva y que avisos quedaron
```

Si el consolidado junta varias áreas y conviene una portada propia del
consolidado (en vez de reusar la portada del primer archivo, que suele decir
el nombre de un área sola), `inventario` acepta:

```
python assets/consolidar.py inventario area1.pptx area2.pptx -o plan.json \
    --portada-consolidada --titulo-consolidado "Consolidado de presentaciones"
```

Antepone una portada nueva (`"tipo": "portada"`, `"archivo": null`) con ese
título y, en el subtítulo, las direcciones/áreas que detectó en la portada de
cada archivo (mejor esfuerzo — busca una línea con palabras como "Dirección",
"Gerencia", "Talento Humano"...; si no encuentra ninguna, deja el subtítulo
vacío). Queda marcada con un aviso para que el usuario la confirme o la
complete. Con esta opción, la portada propia de **todos** los archivos de
origen (incluido el primero) pasa a `separador` — el consolidado tiene una
sola portada, la nueva. `--titulo-consolidado` es opcional
(por defecto "Consolidado de presentaciones").

Ambos comandos imprimen una tabla Markdown: enséñasela al usuario tal cual (o
resúmela) en vez de reformularla — trae la información que necesita para
aprobar o corregir el plan.

## Qué hace, diapositiva por diapositiva

### Clasificación (paso `inventario`)

Cada diapositiva de cada archivo se clasifica en uno de cuatro tipos:

| Tipo | Señal |
|---|---|
| `portada` | Layout con nombre tipo "Portada"/"Title Slide", o es la diapositiva 1 del primer archivo con poco texto |
| `separador` | Layout con nombre tipo "Separador"/"Sección", o muy poco texto (nombre de sección nada más) |
| `cierre` | Layout con nombre tipo "Cierre"/"Closing", o texto tipo "Gracias" / "Preguntas" |
| `contenido` | Todo lo demás — la mayoría de las diapositivas |

Si una diapositiva parece portada pero **no es la primera del primer
archivo**, se reclasifica como `separador` (un deck consolidado tiene una sola
portada). Cuando la clasificación sale de una heurística de texto en vez del
nombre del layout, el plan lo marca con un aviso "confirmar".

Para diapositivas de **contenido**, se busca el título en este orden:

1. El placeholder de título del layout de origen, si lo tiene.
2. La bandera de título que ya pone esta misma skill (topbar azul con
   `roundRect`), si el archivo viene de una generación previa.
3. El bloque de texto más grande y/o más arriba de la diapositiva (heurística;
   el plan lo marca para que se confirme).

El resto del contenido de una diapositiva de `contenido` se separa en:

- **contenido** — todo lo que se copia tal cual (texto, imágenes, tablas,
  gráficas, SmartArt, grupos).
- **fuente** — la línea de "Fuente: ..." / nota al pie (por texto o por
  posición: una línea angosta y ancha muy abajo de la diapositiva). Va a la
  línea de fuente de la plantilla nueva.
- **decoración** — mobiliario de la plantilla vieja que no tiene equivalente
  en la nueva: fondos a toda la diapositiva, formas sin texto que se salen del
  borde, la banda que estaba detrás del título viejo. **Se descarta**, y cada
  una queda contada en los avisos. Con `"conservar_decoracion": true` en el
  plan, no se descarta nada (puede verse desordenado, pero nada se pierde).

Pie de página y fecha del layout viejo (placeholders `dt`/`ftr`) pasan a las
**notas del orador**, no se descartan ni se muestran en la diapositiva (la
plantilla nueva no tiene esos campos).

### Separadores limpios: los puntos a tratar van a otra diapositiva

Un separador solo debe anunciar el tema que viene — no cargar una agenda. Si
el separador de origen trae, además del título, una lista de puntos (viñeta o
numeral propios) o varias líneas de texto largas, esas líneas **no** se
amontonan en el subtítulo del separador: se sacan a una diapositiva de
contenido aparte, justo después, con esos puntos como viñetas normales
(`vinetas`). El separador queda con el título y, si tenía una sola línea corta
de metadato (área, fecha), esa línea sí se conserva como subtítulo — solo se
mueven los **puntos**, no cualquier segunda línea.

Se considera "saturado" (dispara la separación) cuando alguna de las líneas
extra trae viñeta/numeral propios en el XML, o hay más de 2 líneas extra, o su
texto combinado pasa de ~100 caracteres. Con 1–2 líneas cortas de metadato
(p. ej. "Dirección de Talento Humano · 24 de agosto de 2026"), el separador no
se toca — sigue como una sola línea bajo la raya, igual que antes.

La diapositiva de puntos generada aparece en el plan con `"tipo": "puntos"` y
`"archivo": null` (no copia nada de ningún origen; se arma con
`Deck.contenido()` + `vinetas()`):

```json
{ "archivo": null, "tipo": "puntos", "titulo": "Resultados del trimestre",
  "puntos": ["Avance de ingresos y egresos", "Cartera por edades", "..."],
  "_avisos": ["diapositiva generada con los puntos que traia el separador ..."] }
```

El título de esa diapositiva se copia del separador por defecto; el aviso
recuerda revisarlo (puede convenir algo más descriptivo que repetir el título
del separador) y, si el usuario prefiere, fusionar esos puntos con la primera
diapositiva de contenido real de la sección en vez de dejarlos aparte.

**Excepción:** cuando el "separador" en realidad es la portada de otro de los
archivos consolidados (se reclasifica por no ser el primer archivo — ver
"Clasificación" arriba), sus líneas de sobra (kicker, subtítulo, meta) **no**
son puntos a tratar, son metadatos de portada (tipo de informe, periodo,
audiencia...). En ese caso no se genera una diapositiva de viñetas: se deja
una sola línea corta (la que más suene a área/dirección) como subtítulo del
separador, y el resto va a las **notas del orador** — mismo criterio que el
pie/fecha de una plantilla vieja.

### Generación (paso `generar`)

- **`portada` / `separador` / `cierre`** se rehacen con `Deck.portada` /
  `Deck.separador` de `pptx_kit.py`. Todas las líneas de texto que traía la
  diapositiva original pasan a los campos del plan (`kicker`, `titulo`,
  `subtitulo`, `meta` en portada; `titulo`, `sub` en separador/cierre) — nada
  se pierde, solo cambia dónde va cada línea. Si la diapositiva original traía
  una foto de personaje razonable (no un logo ni la franja de sellos), se
  reutiliza en el mismo lugar que ocuparía el personaje institucional
  (`"figura": "original"` en el plan); si no, se usa un personaje de
  `marca/personajes/` o el que indique el plan.
- **`contenido`** se arma con `Deck.contenido(titulo, sub)` (la bandera) y
  luego el contenido separado en el paso anterior se **copia** a esa
  diapositiva — no se recompone con los helpers de `pptx_kit` (`kpi_tiles`,
  `tabla`, etc.), porque el contenido ya es el de otra persona y no se
  reinterpreta. Se reencuadra como bloque en la zona útil
  (`2.2 → 31.7 cm` × debajo de la bandera → `14.2 cm`, ver
  `05-mapa-de-layouts.md` → "Geometría"): si ya cabe (con un margen de
  tolerancia para holguras de diseño menores), no se toca ni la posición ni el
  tamaño; si no cabe, se escala **todo el bloque en conjunto** (nunca una
  forma sí y otra no) para que quepa, y el informe dice a qué porcentaje.
- Las **notas del orador** originales se conservan; se les añade el pie/fecha
  del layout viejo si lo tenía.
- Las **diapositivas ocultas** siguen ocultas. Las **animaciones** no se
  conservan (no existen en formas compuestas por coordenadas) y quedan
  avisadas.
- Hipervínculos internos ("ir a la diapositiva X") se quitan porque el destino
  ya no corresponde; el texto del enlace se conserva. Hipervínculos externos
  (URLs) se conservan.

## El plan (`plan.json`)

```json
{
  "salida": "consolidado.pptx",
  "normalizar_fuentes": true,
  "conservar_decoracion": false,
  "trazabilidad_en_notas": false,
  "diapositivas": [
    { "archivo": "...", "n": 3, "tipo": "contenido",
      "titulo": "Telefonía voz y datos 2026-2027",
      "sub": "Para los periodos comprendidos entre...",
      "anexo": false,
      "_avisos": ["titulo deducido (texto dominante): confirmar"] }
  ]
}
```

Qué se puede editar antes de generar (y por qué el usuario, no la skill, debe
decidirlo):

- **`titulo` / `sub` / `kicker` / `subtitulo` / `meta`** — el título deducido
  por heurística puede no ser el correcto; corregirlo aquí no cambia nada más
  de la diapositiva.
- **`tipo`** — reclasificar una diapositiva (p. ej. de `contenido` a
  `separador` si la heurística se equivocó), o poner `"omitir"` para que esa
  diapositiva no pase al consolidado (el usuario decide qué se recorta, nunca
  la skill por su cuenta — mismo principio que "No omitir" de
  `02-reglas-de-diseno.md`). También existe `"puntos"` (sin `archivo`): una
  diapositiva de contenido sintética con una lista `"puntos"` como viñetas —
  la usa la skill para los puntos que saca de un separador saturado (ver
  arriba), pero se puede agregar una a mano igual que una portada/separador
  nuevos.
- **Reordenar** las entradas de la lista — el consolidado sale en ese orden.
- **`figura`** — `"original"` reutiliza la imagen que traía esa portada o
  separador; cualquier nombre de `assets/marca/personajes/` fuerza ese
  personaje; `null` deja que rote automáticamente.
- **`anexo`** (solo `contenido`) — `true` pone el topbar gris azulado de anexo
  en vez del azul institucional.
- **`conservar_decoracion`** — `true` si el usuario prefiere revisar él mismo
  qué decoración se descarta, en vez de que la skill lo haga.
- **`trazabilidad_en_notas`** — `true` añade a las notas del orador de dónde
  salió cada diapositiva (`archivo · diapositiva N`); útil si luego hay que
  rastrear un dato hasta el informe de origen.

**El plan se le muestra al usuario (la tabla resumen del paso `inventario`
basta) y se espera su aprobación o sus correcciones antes de generar.** Igual
que el esquema del flujo de generación normal.

## Diapositivas que no caben bien

Cuando el informe de `generar` marca "contenido reducido al NN % ... texto
mínimo X pt: considerar recomponer o partir", es porque la diapositiva de
origen ya estaba muy cargada en su plantilla vieja (letra pequeña, mucho
texto) y reencuadrarla en la zona más angosta de la plantilla nueva la deja
con letra demasiado chica para leerse cómodo. **No se resuelve encogiendo más
ni recortando texto por su cuenta.** Ofrecer al usuario, y esperar su
decisión:

1. **Recomponer** esa diapositiva con un layout `L01`–`L14` (ver
   `06-recetas-de-composicion.md`), redactando el contenido con las reglas
   normales de la skill — el dato no se pierde, cambia de forma.
2. **Partir** la diapositiva en dos (o más), una idea por diapositiva, sin
   quitar información — regla general de `02-reglas-de-diseno.md`.
3. Dejarla como está (con la letra reducida) si el usuario lo prefiere así.

## Diferencias con el modo de generación

| | Generación (`01`–`06`) | Consolidar (`07`, este archivo) |
|---|---|---|
| Contenido | Se redacta desde cero o desde un informe | Ya existe; se copia tal cual |
| Layout de cada diapositiva | Se elige uno de `L01`–`L14` | Se hereda la estructura original; solo cambia el marco |
| Herramienta | Se escribe un script nuevo que importa `pptx_kit` | `assets/consolidar.py` (no se escribe script) |
| Aprobación previa | Esquema (lista numerada con layouts) | Plan (`plan.json`, tabla resumen) |

## Limitaciones conocidas

- Formas con animaciones, transiciones o macros de PowerPoint no se
  conservan (quedan avisadas).
- Imágenes en formato no compatible con Pillow (p. ej. algunos EMF/WMF muy
  viejos) se copian igual, pero sin poder detectarse como duplicadas de otra
  diapositiva — no afecta el resultado visual, solo el peso del archivo.
- Si dos diapositivas de origen comparten una imagen idéntica, el consolidado
  la reutiliza una sola vez internamente (no engorda el archivo).
