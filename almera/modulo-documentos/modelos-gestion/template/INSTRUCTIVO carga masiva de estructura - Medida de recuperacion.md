# Instructivo: carga masiva de la estructura "Medida de recuperación"

Explica cómo usar la plantilla `Estructura Medida de recuperacion - carga.xlsx` y el árbol (`task.txt`) para subir de una sola vez toda la estructura de nodos al modelo de gestión, sin crearlos uno a uno.

- **Plataforma:** Modelos de Gestión (instancia `sgicapitalsaludpruebas`)
- **Modelo:** `MDR-1` – Medida de recuperación
- **Resultado probado:** carga exitosa de **227 nodos** (5 carpetas + 222 documentos)

---

## 1. Qué hace falta

| Archivo | Para qué sirve |
|---|---|
| `task.txt` | **El árbol**: lista de carpetas y documentos con su versión. Es la fuente de datos. |
| `generar_estructura_medida_recuperacion.py` | Script que convierte el árbol en la plantilla Excel. |
| `Medida de recuperacion20260923_042506.xlsx` | Exportación de la plataforma, usada como molde (estilos y hoja `Clasificaciones`). |
| `Estructura Medida de recuperacion - carga.xlsx` | **Plantilla lista para cargar** (resultado del script). |

Requisito: Python 3 (sin librerías externas).

---

## 2. El árbol (`task.txt`)

El árbol se escribe después de la línea `ARBOL DOCUMENTOS` con este formato exacto:

```
ARBOL DOCUMENTOS

Nombre de la carpeta (N)
├── Nombre del documento 1 (V 1.0)
├── Nombre del documento 2 (V 1.0)
└── Nombre del último documento (V 1.0)
```

Reglas:

1. Cada **carpeta** va sola en una línea y termina con el número de documentos entre paréntesis: `(9)`.
2. Cada **documento** empieza con `├── ` (o `└── ` el último) y puede terminar con la versión `(V 1.0)`.
3. Una línea en blanco separa una carpeta de la siguiente.
4. El número `(N)` debe coincidir con los documentos listados; si no, el script se detiene con error.

Carpetas actuales:

| # | Carpeta | Documentos |
|---|---|---|
| 1 | Informacion medida de recuperacion | 9 |
| 2 | Fichas de indicadores técnico científicos FENIX | 84 |
| 3 | Fichas de indicadores financieros FENIX | 54 |
| 4 | Actas Medida de Recuperación Resolución 6722-6 de 2021 | 30 |
| 5 | Actas Levantamiento Medida Programa de Recuperación Res 5023 - 6 de 2022 | 45 |
| | **Total de nodos** (5 + 222) | **227** |

---

## 3. La plantilla Excel

Hoja **`Nodos_Modelo`**, una fila por nodo, en orden de árbol (carpeta y luego sus documentos):

| Col. | Título | Contenido | ¿Obligatoria? |
|---|---|---|---|
| **A** | Código | Identificador jerárquico del nodo | **Sí** |
| B | Nombre | Nombre de la carpeta o documento | Sí |
| C | Clasificación | Valor de la hoja `Clasificaciones` | Sí |
| D | Clasificación Hijos | Valor de la hoja `Clasificaciones` | Sí |
| E | Descripción | En los documentos: `Versión X.Y` | No |
| F | Padre | Código del nodo padre (vacío en carpetas) | Sí en documentos |

### Cómo se arman los códigos

- **Carpeta:** número consecutivo → `1`, `2`, `3`…
- **Documento:** código de la carpeta + punto + consecutivo de **dos dígitos** → `2.01`, `2.02` … `2.84`.

Los dos dígitos evitan confundir `2.1` con `2.10` y mantienen el orden correcto.

### Clasificaciones usadas

| Tipo de nodo | Clasificación | Clasificación Hijos |
|---|---|---|
| Carpeta | Módulo | Items |
| Documento | Item | Items |

### Ejemplo

| Código | Nombre | Clasificación | Clasif. Hijos | Descripción | Padre |
|---|---|---|---|---|---|
| 1 | Informacion medida de recuperacion | Módulo | Items | | |
| 1.01 | Matriz Financiera Capital Salud | Item | Items | Versión 1.0 | 1 |
| 1.02 | Matriz Técnico Científico 2022 | Item | Items | Versión 1.0 | 1 |
| 2 | Fichas de indicadores técnico científicos FENIX | Módulo | Items | | |
| 2.01 | BAJO PESO AL NACER CORTE MAYO 2023 | Item | Items | Versión 1.0 | 2 |

Árbol resultante en la plataforma:

```
Medida de recuperación
├─ Informacion medida de recuperacion        (1)
│  ├─ Matriz Financiera Capital Salud        (1.01)
│  └─ Matriz Técnico Científico 2022         (1.02)
└─ Fichas de indicadores técnico científicos FENIX   (2)
   └─ BAJO PESO AL NACER CORTE MAYO 2023     (2.01)
```

---

## 4. Paso a paso

### Paso 1. Preparar el árbol
Edita `task.txt` respetando el formato de la sección 2. Revisa que cada `(N)` coincida con sus documentos.

### Paso 2. Generar la plantilla
En PowerShell, dentro de la carpeta del proyecto:

```powershell
python .\generar_estructura_medida_recuperacion.py
```

El script imprime el resumen (carpetas, documentos y total de filas) y genera `Estructura Medida de recuperacion - carga.xlsx`.
Salida esperada: `Total filas: 227`.

Revisa los **AVISO** que pueda mostrar:
- documentos repetidos dentro de una carpeta,
- documentos sin versión,
- los nombres más largos.

Si ves `Línea no reconocida` o `dice N documentos y se leyeron M`, corrige el `task.txt` y vuelve a ejecutar.

### Paso 3. Revisar el Excel (opcional)
Ábrelo y comprueba:
- Columna A llena en **todas** las filas.
- Los títulos son `Código | Nombre | Clasificación | Clasificación Hijos | Descripción | Padre`.
- Las tildes y la ñ se ven bien.

No reordenes ni borres columnas.

### Paso 4. Cargar en la plataforma
1. Ingresa al modelo **Medida de recuperación** (`MDR-1`).
2. Usa la opción de **carga/importación de nodos por XLSX**.
3. Selecciona `Estructura Medida de recuperacion - carga.xlsx`.
4. Confirma la carga.

### Paso 5. Verificar
- Que el árbol muestre las 5 carpetas con sus documentos.
- Que el total sea 227 nodos.
- Que las descripciones (`Versión 1.0`) y los nombres con tildes se vean bien.

---

## 5. Reglas que no se pueden romper

1. **Código en la columna A, en todas las filas.** Si falta: error `No se registró codigo`.
2. **La plataforma lee por posición, no por título.** A Código, B Nombre, C Clasificación, D Clasificación Hijos, E Descripción, F Padre.
3. Las columnas C y D solo admiten valores de la hoja `Clasificaciones`.
4. No incluyas el nodo raíz (el modelo ya existe).
5. Los padres deben aparecer **antes** que sus hijos (el script ya lo respeta).
6. **No recargues una exportación tal cual**: la exportación de la plataforma sale con la columna Código vacía y títulos corridos.
7. Genera siempre la plantilla a partir de la exportación original (molde): así se conserva el formato que la plataforma acepta.

---

## 6. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `No se registró codigo` | Fila con columna A vacía | Regenerar con el script; no editar a mano sin código |
| `Línea no reconocida` (script) | Línea del árbol con formato distinto | Corregir `task.txt` (carpeta con `(N)`, documentos con `├── `/`└── `) |
| `dice N documentos y se leyeron M` | El `(N)` no coincide | Ajustar el número o completar la lista |
| Clasificación rechazada | Valor que no está en `Clasificaciones` | Usar exactamente los valores de esa hoja |
| El Excel no abre | Se editó el archivo con otra herramienta | Regenerar con el script |

---

## 7. Reutilizar para otra estructura

1. Cambia el contenido de `task.txt` por el nuevo árbol.
2. Si cambian las clasificaciones, ajusta `CLASIF_CARPETA` y `CLASIF_DOCUMENTO` en el script.
3. Cambia `OUT` si quieres otro nombre de archivo, y `SRC` si usas otra exportación como molde.
4. Ejecuta el script y carga el resultado.

---

## 8. Prompt para que una IA genere la plantilla XLSX

Copia el prompt completo en la IA (idealmente una que pueda ejecutar código y devolver archivos, como Claude con ejecución de código). Adjunta: **(a)** la exportación de la plataforma usada como molde (`Medida de recuperacion20260923_042506.xlsx`) y **(b)** el árbol en texto (`task.txt`) o pégalo al final.

````text
Actúa como un asistente de datos. Debes generar un archivo XLSX para la carga masiva de nodos en la plataforma "Modelos de Gestión", a partir del árbol de carpetas y documentos que te entrego.

ENTRADAS
1. Un XLSX exportado de la plataforma (molde), con las hojas "Nodos_Modelo" y "Clasificaciones".
2. El árbol en texto, con este formato:
   Nombre de carpeta (N)
   ├── Nombre del documento (V 1.0)
   └── Último documento (V 1.0)
   (N = número de documentos de la carpeta; la versión es opcional; una línea en blanco separa carpetas.)

SALIDA
Un XLSX con el mismo molde (conserva estilos y la hoja "Clasificaciones" sin cambios). Solo se reescribe la hoja "Nodos_Modelo", con estos títulos exactos en la fila 1, en este orden:
   A Código | B Nombre | C Clasificación | D Clasificación Hijos | E Descripción | F Padre

REGLAS DE LLENADO (una fila por nodo, en orden de árbol: carpeta y luego sus documentos)
- Carpeta k-ésima (k desde 1):
    Código = k
    Nombre = nombre de la carpeta, sin el "(N)"
    Clasificación = Módulo
    Clasificación Hijos = Items
    Descripción = vacío
    Padre = vacío
- Documento j-ésimo de la carpeta k (j desde 1):
    Código = k.jj, con j SIEMPRE de dos dígitos (1.01, 1.02, … 2.84)
    Nombre = nombre del documento, sin la versión
    Clasificación = Item
    Clasificación Hijos = Items
    Descripción = "Versión X.Y" si el árbol trae "(V X.Y)"; si no, vacío
    Padre = código de su carpeta (k)
- No incluyas el nodo raíz del modelo.
- La columna A (Código) NUNCA puede quedar vacía.
- Los códigos de las columnas A y F deben guardarse como TEXTO (para que "1.10" no se convierta en 1.1).
- Respeta tildes y ñ. No modifiques ni resumas los nombres; cópialos tal cual.
- No agregues columnas, filas de totales ni formatos extra.

VALIDACIONES ANTES DE ENTREGAR (si alguna falla, corrígela o avísame)
1. El número de documentos leídos en cada carpeta coincide con su "(N)".
2. Total de filas de datos = carpetas + documentos. Indícame ese total.
3. No hay códigos repetidos ni celdas vacías en la columna A.
4. Todo valor de las columnas C y D existe en la hoja "Clasificaciones".
5. Todo valor de F corresponde a un código de carpeta existente y aparece antes que sus hijos.
6. Avísame de documentos repetidos dentro de una carpeta, documentos sin versión y de los 3 nombres más largos.

ENTREGA
- El archivo "Estructura Medida de recuperacion - carga.xlsx".
- Un resumen: carpetas, documentos por carpeta, total de filas y los avisos encontrados.
- Una tabla con las primeras 10 filas para revisión rápida.

ÁRBOL:
[pega aquí el contenido de task.txt]
````

**Notas de uso**

- Si la IA no puede editar el molde original y crea el Excel desde cero, funciona igual mientras respete los títulos, el orden de columnas y los valores de las reglas. Aun así, conviene comparar con la plantilla generada por el script.
- Para otra estructura con distintas clasificaciones, cambia en el prompt los valores `Módulo / Items` e `Item / Items`.
- Revisa siempre el resumen y las validaciones que devuelva la IA antes de cargar en la plataforma.
