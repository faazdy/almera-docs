# Instructivo: carga masiva de la estructura "Medida de recuperación"

Explica cómo usar la plantilla Excel `Estructura Medida de recuperacion - carga.xlsx` para subir de una sola vez toda la estructura de nodos al modelo de gestión, y cómo apoyarte en un asistente de IA para armarla: **le pasas el árbol y la IA te devuelve la tabla lista para el Excel**. No necesitas programar ni ejecutar nada.

- **Plataforma:** Modelos de Gestión
- **Modelo:** `MDR-1` – Medida de recuperación
- **Caso probado:** carga exitosa de 227 nodos (5 carpetas + 222 documentos)

---

## 1. Flujo en 4 pasos

1. **Arma el árbol** de carpetas y documentos en texto (sección 2).
2. **Pásale el árbol a la IA** con el prompt de la sección 5. Te devuelve la tabla con la estructura armada.
3. **Pega la tabla en la plantilla Excel** (sección 6).
4. **Carga el Excel en la plataforma** (sección 7).

---

## 2. El árbol

Es la lista de carpetas y, debajo de cada una, sus documentos. Formato:

```
Nombre de la carpeta (N)
├── Nombre del documento 1 (V 1.0)
├── Nombre del documento 2 (V 1.0)
└── Último documento (V 1.0)

Otra carpeta (N)
├── Documento A (V 1.0)
└── Documento B (V 1.0)
```

- Cada carpeta va en una línea y termina con el número de documentos entre paréntesis: `(9)`.
- Cada documento empieza con `├── ` (o `└── ` el último) y puede terminar con su versión `(V 1.0)`.
- Una línea en blanco separa una carpeta de la siguiente.
- El número `(N)` debe coincidir con los documentos que hay debajo. La IA lo revisa y te avisa si no.

---

## 3. La plantilla Excel

Hoja **`Nodos_Modelo`**, con una fila por nodo, en orden de árbol (una carpeta y justo debajo sus documentos):

| Col. | Título | Qué lleva | ¿Obligatoria? |
|---|---|---|---|
| **A** | Código | Identificador jerárquico del nodo | **Sí** |
| B | Nombre | Nombre de la carpeta o del documento | Sí |
| C | Clasificación | Valor permitido (hoja `Clasificaciones`) | Sí |
| D | Clasificación Hijos | Valor permitido (hoja `Clasificaciones`) | Sí |
| E | Descripción | En documentos: `Versión X.Y` | No |
| F | Padre | Código de la carpeta a la que pertenece el documento | Sí en documentos |

### Cómo se arman los códigos

| Nodo | Código | Ejemplo |
|---|---|---|
| Carpeta | Número consecutivo | `1`, `2`, `3` |
| Documento | Código de su carpeta + punto + consecutivo de **dos dígitos** | `2.01`, `2.02` … `2.84` |

Los dos dígitos evitan confundir `2.1` con `2.10` y mantienen el orden.

### Clasificaciones

| Tipo de nodo | Clasificación (C) | Clasificación Hijos (D) |
|---|---|---|
| Carpeta | Módulo | Items |
| Documento | Item | Items |

### Ejemplo

| Código | Nombre | Clasificación | Clasificación Hijos | Descripción | Padre |
|---|---|---|---|---|---|
| 1 | Informacion medida de recuperacion | Módulo | Items | | |
| 1.01 | Matriz Financiera Capital Salud | Item | Items | Versión 1.0 | 1 |
| 1.02 | Matriz Técnico Científico 2022 | Item | Items | Versión 1.0 | 1 |
| 2 | Fichas de indicadores técnico científicos FENIX | Módulo | Items | | |
| 2.01 | BAJO PESO AL NACER CORTE MAYO 2023 | Item | Items | Versión 1.0 | 2 |

Así queda en la plataforma:

```
Medida de recuperación
├─ Informacion medida de recuperacion                 (1)
│  ├─ Matriz Financiera Capital Salud                 (1.01)
│  └─ Matriz Técnico Científico 2022                  (1.02)
└─ Fichas de indicadores técnico científicos FENIX    (2)
   └─ BAJO PESO AL NACER CORTE MAYO 2023              (2.01)
```

---

## 4. Reglas que no se pueden romper

1. **La columna A (Código) debe estar llena en todas las filas.** Si falta, la plataforma responde `No se registró codigo`.
2. **La plataforma lee las columnas por posición, no por el título.** El orden debe ser siempre: A Código, B Nombre, C Clasificación, D Clasificación Hijos, E Descripción, F Padre.
3. Las columnas C y D solo aceptan valores de la hoja `Clasificaciones`.
4. No incluyas el nodo raíz del modelo (ya existe).
5. Cada carpeta va antes que sus documentos.
6. No recargues una exportación de la plataforma tal cual: sale con la columna Código vacía y los títulos corridos.
7. No agregues columnas, filas de totales ni celdas combinadas.

---

## 5. Prompt para el asistente de IA

Abre un chat con tu asistente de IA, copia el prompt completo y **pega tu árbol al final**, donde dice `[PEGA AQUÍ EL ÁRBOL]`. No hace falta adjuntar ningún archivo.

````text
Actúa como asistente de datos. Voy a darte un árbol de carpetas y documentos y necesito que me entregues la tabla lista para pegar en una plantilla Excel de carga masiva de nodos de la plataforma "Modelos de Gestión".

FORMATO DEL ÁRBOL QUE TE ENTREGO
- Una carpeta por línea, terminada con el número de documentos entre paréntesis, p. ej. "Nombre de la carpeta (9)".
- Debajo, sus documentos, cada uno con "├── " o "└── " al inicio y, opcionalmente, la versión al final, p. ej. "├── Nombre del documento (V 1.0)".
- Las carpetas se separan por una línea en blanco.

TABLA QUE DEBES GENERAR
Una fila de títulos y una fila por cada nodo, en orden de árbol (cada carpeta seguida de sus documentos). Columnas, exactamente en este orden y con estos títulos:

Código | Nombre | Clasificación | Clasificación Hijos | Descripción | Padre

REGLAS DE LLENADO
- Carpeta número k (k = 1, 2, 3…):
    Código = k
    Nombre = nombre de la carpeta, sin el "(N)"
    Clasificación = Módulo
    Clasificación Hijos = Items
    Descripción = vacío
    Padre = vacío
- Documento número j de la carpeta k:
    Código = k.jj, con j SIEMPRE de dos dígitos (1.01, 1.02, … 2.84)
    Nombre = nombre del documento, sin la versión
    Clasificación = Item
    Clasificación Hijos = Items
    Descripción = "Versión X.Y" si el árbol trae "(V X.Y)"; si no trae versión, vacío
    Padre = código de su carpeta (k)
- Copia los nombres tal cual: no los corrijas, no los resumas ni cambies mayúsculas, tildes o la ñ.
- La columna Código nunca puede quedar vacía.
- No incluyas fila para el modelo raíz, ni filas de totales, ni columnas adicionales.

VALIDACIONES (hazlas antes de responder; si algo falla, dímelo y no inventes datos)
1. El número de documentos de cada carpeta coincide con su "(N)".
2. No hay códigos repetidos.
3. Total de filas de datos = carpetas + documentos.
4. Avísame de documentos repetidos dentro de la misma carpeta y de documentos sin versión.

FORMATO DE ENTREGA
1. Primero un resumen corto: cuántas carpetas, cuántos documentos por carpeta, total de filas y los avisos encontrados.
2. Luego la tabla completa en UN solo bloque de código, con las columnas separadas por TABULADOR (no por comas ni por barras), para que al pegarla en Excel cada valor caiga en su celda. Primera línea = los títulos.
3. Si puedes generar archivos, entrégame además el mismo contenido como un archivo .xlsx llamado "Estructura carga.xlsx", con la hoja "Nodos_Modelo" y las columnas Código y Padre en formato TEXTO.
4. No omitas filas ni abrevies con "..." aunque la tabla sea larga. Si no cabe en una respuesta, divídela en partes numeradas, sin repetir ni saltarte filas, y dime cuándo termina.

ÁRBOL:

[PEGA AQUÍ EL ÁRBOL]
````

---

## 6. Pasar la tabla a la plantilla Excel

**Si la IA te entregó un .xlsx:** revísalo (sección 8) y pasa al paso 7. Si el archivo no tiene el mismo formato que la plantilla, usa el procedimiento siguiente.

**Si la IA te entregó la tabla en texto:**

1. Abre `Estructura Medida de recuperacion - carga.xlsx` (o la exportación de la plataforma, para conservar la hoja `Clasificaciones`).
2. En la hoja `Nodos_Modelo`, borra las filas de datos anteriores (deja la fila 1 de títulos).
3. **Antes de pegar**, selecciona las columnas **A** y **F** y ponles formato **Texto** (Inicio → desplegable de formato de número → Texto). Si no lo haces, Excel convierte `2.10` en `2,1` y se pierden los códigos.
4. Copia el bloque de código de la IA, haz clic en la celda **A1** y pega. Cada valor debe caer en su columna.
5. Verifica que los títulos queden como `Código | Nombre | Clasificación | Clasificación Hijos | Descripción | Padre`.
6. Guarda como `.xlsx`.

---

## 7. Cargar en Almera

1. Ir a **Admin → Calidad → Modelos de gestión**.
2. Dar clic en el botón 'Nuevo Modelo' para crear el nuevo repositorio. En caso de querer cargar una estructura a uno ya exitente tenemos que entrar al que nos interese.
3. Llenar los campos solicitados dentro de la creación (codigo, nombre, descripcion) y Grabar.
4. Dentro de la pestaña 'Estructura', dar clic en el ícono de Excel para **Cargar nodos desde la plantilla xlsx**.
5. En la seccion de cargar, darle clic al botón de 'seleccionar archivo' para cargar la plantilla (generada por el asistente de IA, o la que se hizo manualmente por el usuario). 
6. Dar clic en 'Cargar' cuando se muestre la estructura Excel.
7. Si todo salió bien, el sistema mostrará la estructura con mensaje de 'Aprobado' en color verde, por cada ítem.
8. Dar clic en 'Grabar'.
9. Comprobar la estructura desde la pestaña 'Sistemas' en el menú lateral; o desde la misma ruta de 'Modelos de gestion'.
---

## 8. Revisión rápida antes de cargar

Revisa siempre lo que entrega la IA; puede equivocarse en árboles largos.

- [ ] La columna A no tiene celdas vacías.
- [ ] El total de filas coincide con carpetas + documentos.
- [ ] Los códigos de documentos tienen dos dígitos (`2.01`, no `2.1`) y `2.10` no aparece como `2,1`.
- [ ] Las columnas C y D solo tienen `Módulo`/`Item` e `Items`.
- [ ] En documentos, F trae el código de su carpeta; en carpetas, F está vacía.
- [ ] El último documento de cada carpeta sí está (en listas largas la IA puede cortar filas).
- [ ] Los nombres, tildes y ñ coinciden con el árbol original.
- [ ] No hay filas extra (totales, notas) ni columnas adicionales.

---

## 9. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `No se registró codigo` | Fila con la columna A vacía o desplazada | Revisar que la tabla se pegó desde A1 y que no hay filas en blanco |
| Códigos como `2,1` o `1.1` | Excel los volvió número | Poner A y F en formato Texto **antes** de pegar |
| Todo quedó en una sola columna | La IA separó con comas o barras | Pedirle "separa por TABULADOR" o usar Datos → Texto en columnas |
| Faltan filas | La IA cortó la respuesta | Pedirle continuar desde el último código entregado, o dividir el árbol por carpetas |
| Clasificación rechazada | Valor que no está en `Clasificaciones` | Usar exactamente `Módulo`, `Item`, `Items` |
| Nombres modificados | La IA "corrigió" el texto | Reforzar "copia los nombres tal cual" y comparar contra el árbol |

---

## 10. Árboles muy grandes

Con cientos de nodos (como los 227 de este caso) la IA puede cortar o alterar la salida. Si pasa:

- Envía el árbol **carpeta por carpeta** y pide en cada mensaje: "esta es la carpeta número K; empieza los códigos en K".
- Junta las tablas en el Excel en el orden de las carpetas.
- Si ya sabes cuántas filas debe tener cada carpeta (documentos + 1), verifica el conteo antes de unirlas.

---

## 11. Usar otra estructura distinta

Para otro modelo con otras clasificaciones, cambia en el prompt los valores `Módulo / Items` (carpetas) e `Item / Items` (documentos) por los de la hoja `Clasificaciones` de la plataforma. El resto del procedimiento es igual.
