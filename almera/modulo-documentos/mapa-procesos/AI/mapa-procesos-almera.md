# Almera — Mapa de procesos (guía de referencia)

> Procedimientos para administrar el mapa de procesos de Almera: mover un subproceso a otro proceso padre, cambiar la imagen del mapa, vincular sus áreas y montar las tablas de Salidas No Conformes (SNC). Fue extraído de la guía del módulo de Documentos y de la capacitación con soporte de Almera (25 jun 2026).

**Instrucciones para la IA que use este documento:**
- Responde siempre con el procedimiento exacto documentado aquí, paso a paso.
- No inventes pasos, botones o menús que no estén mencionados en este documento.
- Si la pregunta no está cubierta aquí, dilo explícitamente — no improvises.
- La sección **"Pendiente de validar"** contiene un comportamiento que quedó sin confirmar con soporte. No lo presentes como hecho resuelto.
- Si la pregunta es sobre documentos, emisores, clases, flujo de aprobación u otros temas, indica que corresponde a la guía de **Documentos** (`documentos-almera.md`).

---

## Índice

1. Modificar la jerarquía de un proceso (mover un subproceso)
2. Actualizar la imagen del mapa y vincular las áreas
3. Procesos obsoletos o renombrados
4. Salidas No Conformes (SNC) de un subproceso
5. Pendiente de validar con soporte Almera

---

## 1. Modificar la jerarquía de un proceso (mover un subproceso)

**Cuándo se usa:** para trasladar un subproceso a un nuevo "proceso padre" (por ejemplo, si un subproceso pasó de depender de "Planeación estratégica" a depender de "Organización y métodos").

**Ruta:** `Admin → Procesos`

Hay **dos formas equivalentes** de hacerlo:

**Opción A — desde la sección Procesos:**
1. Ir a **Admin → Procesos**.
2. Buscar y seleccionar el subproceso que se quiere mover (se puede filtrar por nombre).
3. En el campo **Padre**, quitar el proceso actual y buscar/seleccionar el nuevo proceso del cual va a depender.
4. Presionar **Grabar**.

**Opción B — desde el mapa de procesos:**
1. Ir al mapa de procesos y ubicar el subproceso.
2. Darle **Editar** al subproceso — esto habilita, en la parte superior, la pestaña de **Administración**.
3. Desde ahí, cambiar el campo **Padre** de la misma forma.

> El mapa de procesos se actualiza automáticamente al guardar el cambio de jerarquía — no requiere reemplazar la imagen del mapa.

---

## 2. Actualizar la imagen del mapa y vincular las áreas

**Cuándo se usa:** cuando se sube una imagen nueva del mapa de procesos y hay que hacer que sus zonas/botones lleven al proceso correcto.

**Ruta:** `Admin → Calidad → Parametrización de procesos`

1. **Reemplazar la imagen:** en la vista del mapa, seleccionar **Administrar archivos**, eliminar la imagen anterior y subir la nueva.
2. **Vincular las áreas:** hacer clic en **Administrar áreas** (esto abre un panel).
3. En otra pestaña del navegador, abrir el proceso específico (sección **Procesos**) y entrar a su pestaña **Seguimiento**; copiar la URL de esa página.
4. En el panel de "Administrar áreas", seleccionar la zona del mapa correspondiente a ese proceso y pegar la URL copiada en el campo **Dirección**.
5. Presionar **Grabar**.
6. Repetir los pasos 3–5 para cada área/proceso del mapa.

### Notas / advertencias

- **El mapa solo carga procesos, no subprocesos** en el listado de "Administrar áreas". Si un área del mapa en realidad corresponde a un subproceso (y no tiene su propio "proceso" creado formalmente), no debe vincularse ese subproceso directamente ahí — lo correcto ("deber ser") es que tanto el proceso como el subproceso existan como entidades separadas en la sección **Procesos**.
- **Al reemplazar la imagen del mapa, las áreas/vínculos anteriores no se conservan** — hay que volver a vincular cada zona manualmente.

---

## 3. Procesos obsoletos o renombrados

Si un proceso quedó obsoleto o cambió de nombre tras una reestructuración del mapa (y ya no debería aparecer como vigente), la forma correcta de "retirarlo" es cambiarle el estado a **Anulado** — no eliminarlo — siempre que no tenga documentos ni indicadores asociados, para no perder trazabilidad.

Antes de anular o unificar procesos, conviene validar que no tengan documentos o indicadores todavía asociados.

---

## 4. Salidas No Conformes (SNC) de un subproceso

**Cuándo se usa:** para montar en Almera la tabla de Salidas No Conformes de un subproceso, inyectándola como HTML en su sección de Salidas No Conformes.

> Fuente: *Instructivo montaje de tablas de Salidas No Conformes (SNC) en Almera* (5 oct 2026). El instructivo original deja pendiente confirmar la ruta exacta hasta el campo de HTML; no la inventes.

### Objetivo y alcance

Este instructivo permite que cualquier persona monte en Almera la tabla de Salidas No Conformes (SNC) de un subproceso, sin saber HTML, con ayuda de una IA.

Cada subproceso tiene su propia tabla, que se inyecta como HTML en su sección de Salidas No Conformes. Todas llevan el mismo aviso azul de registro y la misma tabla de siete columnas, para que se vean uniformes en toda la plataforma.

### Antes de empezar

Ten a la mano estos cuatro elementos:

- Los datos del subproceso en Excel o texto: salida/producto/servicio, situación que puede presentarse y las X del tratamiento inmediato de cada fila.
- El nombre exacto del subproceso, tal como aparece en el mapa de procesos de Almera.
- Permiso para editar la sección Salidas No Conformes del subproceso y acceso al campo donde Almera permite inyectar HTML.
- Acceso a una IA de chat (Claude u otra) para convertir los datos a HTML.

Pendiente de completar: la ruta exacta en Almera hasta el campo de HTML.

### Estructura estándar de la tabla

Toda tabla SNC tiene siete columnas, siempre en este orden, aunque la fuente venga con menos.

| Columna | Qué se escribe |
| --- | --- |
| Subproceso | Nombre del subproceso, igual en todas las filas y sin punto final |
| Salida / producto / servicio (Definido en la caracterización) | La salida tal como está definida en la caracterización del subproceso |
| Situación que puede presentarse | Descripción del incumplimiento; termina en punto |
| Corrección | X si aplica este tratamiento inmediato; vacío si no |
| Devolución | X si aplica; vacío si no |
| Reproceso | X si aplica; vacío si no |
| Informar al usuario (Concesión) | X si aplica; vacío si no |

Tres reglas de llenado:

- Una fila por cada situación distinta. Si una celda mezcla dos situaciones, confirma con el dueño del proceso si van en una fila o en dos.
- La X siempre va en mayúscula, una por celda. Una "x" minúscula del Excel se normaliza a "X".
- Si la fuente no trae la columna Subproceso o le falta una columna de tratamiento, no la inventes: pregunta primero o deja la celda vacía.

### Paso a paso con IA

Sigue estos pasos en orden, una tabla por subproceso.

1. Abre el Excel del subproceso y copia el bloque completo: encabezados y todas las filas.
2. Abre una conversación nueva con la IA y pega el prompt de la sección siguiente.
3. Debajo del prompt, pega los datos copiados del Excel.
4. Revisa la respuesta: debe ser un solo bloque de código HTML y una lista corta de las correcciones de texto hechas.
5. Recorre la lista de verificación del final de este instructivo.
6. Copia el bloque de código completo, desde el aviso azul hasta el cierre de la tabla.
7. En Almera, entra a la sección Salidas No Conformes del subproceso, abre el campo de HTML, pega el bloque y guarda.
8. Recarga la página y confirma que el aviso y la tabla se ven completos.

### Prompt para la IA

Copia todo el bloque, pégalo en la IA y, al final, añade los datos del subproceso. El bloque ya incluye el HTML de la plantilla.

```text
Actúa como asistente de formato HTML para Almera SGI (Capital Salud). Te voy a pasar los datos de una tabla de Salidas No Conformes (SNC) de un subproceso. Devuélveme UN solo bloque de código HTML listo para pegar en Almera.

REGLAS
1. Usa exactamente la plantilla de abajo: primero el aviso azul y luego la tabla.
2. La tabla siempre tiene 7 columnas, en este orden: Subproceso, Salida / producto / servicio (Definido en la caracterización), Situación que puede presentarse, Corrección, Devolución, Reproceso, Informar al usuario (Concesión).
3. Una fila <tr> por cada situación. Copia la fila de ejemplo y cambia solo el contenido.
4. En las 4 últimas columnas escribe X (mayúscula) donde yo marque el tratamiento. Si no aplica, deja &nbsp;. Normaliza las x minúsculas.
5. Corrige tildes y errores de digitación evidentes. Quita espacios dobles, comillas sueltas y saltos de línea que vengan del Excel. No cambies el sentido ni agregues información.
6. El nombre del subproceso va igual en todas las filas, con mayúsculas iniciales y sin punto final. Cada situación termina en punto.
7. Deja intactos los códigos y siglas (por ejemplo PR-022-ADM, FR-108-ADM, PAMEC, MIPRES).
8. Si falta la columna Subproceso o alguna columna de tratamiento, pregúntame antes de generar. Si una celda trae dos situaciones, pregúntame si van en una fila o en dos.
9. Mantén los estilos en línea (style="...") tal como están. No uses clases ni CSS externo.
10. Después del bloque de código, escribe una lista corta con las correcciones de texto que hiciste.

PLANTILLA
<div style="border:1px solid #c7d6e8; border-left:4px solid #2e6da4; background-color:#f2f7fc; border-radius:4px; padding:14px 18px; margin-bottom:16px; font-family:Verdana,sans-serif; font-size:12px; color:#000;">
  <p style="margin:0 0 8px 0; font-size:13px; color:#1e3a5f;"><strong>⚠️ Registro de Salidas No Conformes (SNC)</strong></p>
  <p style="margin:0 0 10px 0;">En caso de identificar una <strong>Salida No Conforme (SNC)</strong> asociada a alguno de los subprocesos establecidos (ver subproceso), se deberá realizar el registro correspondiente en el siguiente enlace:</p>
  <p style="margin:0 0 10px 0;">
    <a href="https://forms.office.com/pages/responsepage.aspx?id=dntcp1fBhkiX-RYm0OkvVV3cdYtfSbBKmMFhE6Y5wOVUN0RVR1dQWDJPSjlMTkNFMkU0OFcyTEhIRi4u&amp;origin=lprLink&amp;route=shorturl" style="display:inline-block; background-color:#2e6da4; color:#ffffff; text-decoration:none; padding:7px 14px; border-radius:3px; font-size:12px;">📋 Formulario: Reporte de Salidas No Conformes</a>
  </p>
  <p style="margin:0; font-size:11px; color:#555;">Ver la consolidación de las Salidas No Conformes de la Entidad - SNC: <a href="https://sgi.almeraim.com/sgi/secciones/?nid=424" style="color:#2e6da4;">clic aquí</a></p>
</div>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:100%; font-family:Verdana,sans-serif; font-size:12px; color:#000;">
  <thead>
    <tr style="background-color:#d9d9d9;">
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Subproceso</th>
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Salida / producto / servicio<br>(Definido en la caracterización)</th>
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Situación que puede presentarse</th>
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Corrección</th>
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Devolución</th>
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Reproceso</th>
      <th style="border:1px solid #999; text-align:center; vertical-align:middle;">Informar al usuario<br>(Concesión)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid #999; vertical-align:middle;">NOMBRE DEL SUBPROCESO</td>
      <td style="border:1px solid #999; vertical-align:middle;">SALIDA / PRODUCTO / SERVICIO</td>
      <td style="border:1px solid #999; vertical-align:middle;">SITUACIÓN QUE PUEDE PRESENTARSE.</td>
      <td style="border:1px solid #999; text-align:center; vertical-align:middle;">X</td>
      <td style="border:1px solid #999; text-align:center; vertical-align:middle;">&nbsp;</td>
      <td style="border:1px solid #999; text-align:center; vertical-align:middle;">X</td>
      <td style="border:1px solid #999; text-align:center; vertical-align:middle;">&nbsp;</td>
    </tr>
  </tbody>
</table>

DATOS DEL SUBPROCESO (pegados desde Excel)
[pega aquí los datos]
```
### Pasos para cargarlo en Almera

1. Abrir el proceso/subproceso, que tendrá la SNC.
2. Dar clic en 'Editar'
3. Nos desplazamos hasta el campo de **Salidas No Conformes**, y damos clic en el botón 'Fuente HTML'.
4. Dentro del campo de texto metemos el codigo HTML que nos da el asistente de IA.
5. Para verificar como queda, dar clic nuevamente en el botón de 'Fuente HTML'.
6. Una vez esté todo correcto le damos a 'Grabar'.

### Hacerlo sin IA

La plantilla HTML vive dentro del prompt de la sección anterior, entre las líneas PLANTILLA y DATOS DEL SUBPROCESO. Para armarla a mano:

1. Copia la plantilla, desde la etiqueta `<div` del aviso hasta el cierre `</table>`.
2. Duplica el bloque `<tr>` de ejemplo, completo, una vez por cada situación.
3. En cada fila reemplaza el texto en mayúsculas de las tres primeras celdas.
4. En las cuatro últimas celdas deja `X` donde aplique el tratamiento y `&nbsp;` donde no aplique.
5. No borres comillas, signos `<` ni `>` de las etiquetas: un solo carácter faltante rompe la tabla.

### Reglas de limpieza de texto

Los datos de Excel suelen traer errores de digitación. Se corrigen al montar la tabla, sin cambiar el sentido.

- Tildes: auditorías, pérdida, técnico, científico, habilitación, órdenes.
- Typos evidentes: "inclumplimiento" pasa a "incumplimiento"; "Bse de datos" pasa a "Base de datos".
- Conectores: "y o" pasa a "y/o".
- Espacios dobles y espacios antes de una coma: se eliminan.
- Comillas sueltas y saltos de línea que Excel agrega al pegar: se eliminan.
- Punto final: las situaciones lo llevan; el nombre del subproceso y la salida no.
- Nombre del subproceso: el mismo en todas las filas, con tilde y mayúsculas iniciales.
- Siglas y códigos de procedimiento o formato (PR-, FR-, PAMEC, MIPRES, RIPS) se dejan intactos.
- Dato dudoso, como una X que parece faltar: se confirma con el dueño del proceso en vez de asumirlo.

### Lista de verificación

Recorre estos puntos antes de guardar en Almera y otra vez después de guardar.

- [ ] El aviso azul aparece antes de la tabla, con los dos enlaces.
- [ ] La tabla tiene siete columnas, en el orden estándar.
- [ ] Cada fila lleva el nombre del subproceso, igual en todas.
- [ ] Las X coinciden con el Excel, fila por fila.
- [ ] No quedan typos ni tildes faltantes.
- [ ] Los códigos de procedimiento y formato están intactos.
- [ ] El botón del formulario y el enlace de consolidación abren correctamente.
- [ ] Tras guardar, la tabla se ve completa en Almera, sin texto cortado.

### Errores comunes

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| Se ven etiquetas como `<td>` o `<div>` escritas en pantalla | El bloque se pegó en el editor visual y no en el campo de HTML | Borrar y volver a pegar en el campo de HTML |
| La tabla sale sin bordes o el botón sin color | Se perdieron los estilos en línea al copiar | Copiar de nuevo el bloque completo, sin recortar |
| Columnas descuadradas | Alguna fila tiene menos o más de siete celdas | Revisar que cada `<tr>` tenga siete `<td>` |
| Todo el contenido se ve roto desde cierto punto | Falta un cierre de etiqueta (`</tr>`, `</td>`, `</table>`) | Pedir a la IA que revise el HTML y señale la etiqueta sin cerrar |
| Letras raras en lugar de tildes | Problema de codificación al copiar | Pedir a la IA que escriba las tildes como entidades HTML (por ejemplo `&oacute;`) |
| La IA mezcla dos situaciones en una fila | La celda de origen traía dos líneas | Indicarle si van en una fila o en dos, y que no combine por su cuenta |

---

## 5. Pendiente de validar con soporte Almera

### Mapa con ID mal vinculado

**Contexto:** se detectaron procesos donde el mapa apunta al ID de un proceso "padre" en vez del subproceso correspondiente (por un ajuste antiguo al mapa), generando enlaces que llevan al lugar equivocado.

**Estado:** soporte dijo que había que "validarlo" caso por caso — es un tema de datos específico de esta organización, no un procedimiento general reutilizable. Si vuelve a surgir, contactar a soporte con el ID del proceso en cuestión. No dar esto como respuesta confirmada.

**Fuente:** transcripción de la capacitación, 25 jun 2026 (min ~22–48).
