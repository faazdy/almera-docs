# 2. Informes (dashboards)

Hay **dos informes** en `almera/`. Son páginas estáticas que leen un Excel y calculan indicadores de calidad de datos **en el navegador**: el archivo nunca sale del equipo ni se sube a ningún servidor.

| | Informe de documentos Almera | Informe de Control de documentos del SGC |
|---|---|---|
| Carpeta | `almera/informe-documentos/` | `almera/control-documentos-sgc/` |
| Fuente de datos | Export de Almera | Listado maestro que se consolida en la **carpeta local compartida** (no sale de Almera) |
| Cómo obtener el archivo | `Gestión de calidad → Listados maestros → Listado maestro de documentos` → botón Exportar (ícono Excel) | `LISTADO MAESTRO DE CONTROL DE DOCUMENTOS DEL SGC.xls(x)`, hoja `LISTADO_MAESTRO`, sin modificar encabezados |
| Pregunta que responde | ¿Qué hay montado en Almera y en qué estado de calidad de datos está? | ¿Cómo está la vigencia y actualización de los documentos del SGC? |

Cada página enlaza a la otra en el hero ("¿Necesitas el informe de…?").

## 1. Cómo se usa

1. Abrir `index.html` en el navegador (doble clic; no requiere servidor ni internet para el análisis).
2. Arrastrar el Excel a la zona de carga o hacer clic para elegirlo (`.xlsx` / `.xls`).
3. Leer los indicadores; clic en cualquier indicador, barra o sector abre un **modal con la lista de documentos** de esa categoría (hasta 300 filas; se puede exportar a Excel).
4. Filtrar la tabla de detalle y exportar la vista (`Exportar vista (.xlsx)`).
5. **Descargar informe (PDF)** usa la impresión del navegador (`window.print()`): se elige "Guardar como PDF".

> Si aparece "No se pudieron cargar los componentes necesarios", falta la carpeta `vendor/` junto al `index.html`. No separes el HTML de su carpeta.

Secciones de ambas páginas: 01 Cargar · 02 Indicadores generales · 03 Antigüedad · 04 Distribución por categoría · 05 Calidad de datos (+ botón PDF) · 06 Detalle de documentos (filtros, orden, paginación de 50).

## 2. Estructura técnica

```
informe-documentos/  (igual en control-documentos-sgc/)
├── index.html          Maqueta y ids que usa main.js
├── main.js             Toda la lógica (IIFE, JS plano, sin build)
├── styles/style.css
└── vendor/
    ├── xlsx.full.min.js    SheetJS: lee el Excel
    └── chart.umd.min.js    Chart.js: gráficos
```

Sin backend, sin `package.json`, sin build. Fuentes de Google Fonts (DM Sans, JetBrains Mono) son lo único que pide red y el informe funciona sin ellas.

**Flujo de `main.js`** (`handleFile`):
1. Lee el Excel con SheetJS (`cellDates: true`, primera hoja).
2. **Valida** que sea el archivo correcto y, si no, avisa con `alert` qué falta y de dónde exportar.
3. Procesa cada fila (`processRow`): normaliza fechas, extensión, banderas (`_sinCodigo`, `_sinArchivo`, …), marca códigos duplicados.
4. Renderiza KPIs, calidad de datos y tabla; los gráficos van en un `try/catch` aparte para que, si Chart.js falla, el resto del informe siga visible.

Los campos calculados llevan prefijo `_` (`_fechaModificacion`, `_extension`, `_codigoDuplicado`…). Las funciones de render son `renderKPIs`, `renderCharts`, `renderDataQuality`, `renderTable`; los filtros pasan por `applyFilters()`, que vuelve a pintar todo.

## 3. Informe de documentos Almera

**Columnas que usa del export:** `ID`, `Código`, `Nombre`, `Clasificación`, `Tipo`, `Clase`, `Asociado a` (= proceso/subproceso de referencia), `Origen`, `Emisor`, `Estado`, `Versión`, `Fecha creación`, `Fecha documento`, `Fecha modificación`, `Nombres archivos`.
- Obligatorias para aceptar el archivo: `Nombre` y `Asociado a`.
- `Clasificación` es opcional: si no está, se oculta ese filtro y esa gráfica.

**Indicadores generales (KPIs clicables):**

| KPI | Severidad | Definición |
|---|---|---|
| Sin código asignado | Requiere acción | Campo `Código` vacío |
| Códigos duplicados | Requiere acción | Mismo código en varios registros |
| Sin archivo adjunto | Requiere acción | `Nombres archivos` vacío |
| Más de 2 años de antigüedad | Atención | Antigüedad > 2 años según el campo de fecha elegido |
| Cargados como PDF | Informativo | Primera extensión del archivo = `pdf` (sin edición en línea) |

**Antigüedad:** se calcula sobre el campo elegido con las pastillas (por defecto `Fecha modificación`; también `Fecha documento` y `Fecha creación`). Rangos: `< 6 meses`, `6 meses - 1 año`, `1 - 2 años`, `2 - 3 años`, `> 3 años`, `Sin fecha`. El punto de color de la tabla: verde < 1 año, amarillo 1–2, rojo > 2, gris sin fecha.

**Gráficos:** antigüedad (barras), por clasificación (dona), por tipo de archivo (dona), top 10 procesos (`Asociado a`) y top 10 clases.

**Calidad de datos (automática, sobre el archivo completo, sin filtros):** códigos duplicados, registros sin código, documentos específicos sin archivo, fechas de documento futuras, filas estructurales Proceso/Subproceso (no son documentos), aviso si el listado trae un único estado (el export de Almera trae por defecto solo "Vigente"; para ver Obsoletos/Anulados hay que exportar sin ese filtro) y coincidencia de `Origen` con `Asociado a`.

**Filtros de la tabla:** Clasificación, Tipo, Proceso, Clase, Antigüedad y búsqueda por nombre/código.

## 4. Informe de Control de documentos del SGC

**Detección de columnas:** el listado de la carpeta compartida tiene encabezados con saltos de línea y espacios inconsistentes, así que `resolveColumns()` los **normaliza** (minúsculas, sin tildes ni símbolos) y busca por nombre exacto, prefijo o términos contenidos. Columnas que reconoce: `Proceso`, `SubProceso`, `Tipo de documento`, `Código del documento`, `Nombre del documento`, `Estado del documento`, `Seguimiento al estado del documento`, `Fecha de elaboración`, `Fecha última actualización`, `Fecha de derogación`, `Versión inicial`, `Última versión`, `Observación`, cargos de elaboración y aprobación, profesional DEP, `Cons` y las columnas históricas `Fecha N Actualización`.

- Obligatorias para aceptar el archivo: nombre del documento, código, estado y al menos una de Proceso/SubProceso. Se descartan las filas sin nombre ni código.
- Filtros de la tabla: Estado, Tipo de documento, Proceso, SubProceso, Requiere actualización, Antigüedad y búsqueda por nombre/código.
- Mismos rangos de antigüedad y colores de punto que el informe de Almera.
- `Requiere actualización` puede aparecer varias veces (una por vigencia); el informe usa **la del año más alto**.
- Es un campo de **texto libre**; se agrupa en cuatro categorías: Sí / No / Derogado / Otro (en gestión).
- `Tipo de documento` se normaliza ("procedimiento" = "Procedimiento").
- Si falta la fecha de última actualización se usa la de elaboración.

**Indicadores generales:**

| KPI | Severidad | Definición |
|---|---|---|
| Sin código asignado | Requiere acción | `Código` vacío |
| Códigos duplicados | Requiere acción | Mismo código en varios registros |
| Vigentes marcados para actualizar | Atención | Estado = Vigente y Requiere actualización = Sí |
| Vigentes con más de 2 años sin tocar | Atención | Solo documentos **vigentes**, antigüedad > 2 años |
| Derogados sin fecha de derogación | Informativo | Estado = Derogado y sin `Fecha de derogación` |

**Antigüedad:** por `Fecha última actualización` (por defecto) o `Fecha de elaboración`.
**Gráficos:** antigüedad, por estado (Vigente/Derogado), por tipo de documento, top 10 procesos y top 10 subprocesos.
**Calidad de datos:** códigos duplicados (puede ser un derogado y su reemplazo con el mismo código), sin código, derogados sin fecha, derogados sin observación (motivo), variantes de texto en `Tipo de documento` y en `Requiere actualización`.

## 5. Mantenimiento

**Agregar un KPI:** en `renderKPIs()` añade el conjunto en `sets` y una entrada en `cardDefs` (`key`, `sev`, `title`, `subtitle`, `modalTitle`). Severidades: `problem`, `warn`, `info`.

**Agregar una regla de calidad de datos:** añade un objeto `{type: 'warn'|'good'|'note', text}` a `items` en `renderDataQuality()`.

**Cambiar un umbral de antigüedad:** `ageBucketLabel()` (rangos) y `ageDotClass()` (colores del punto).

**Si Almera cambia el export** (nombres de columnas): en el informe de Almera ajusta `REQUIRED_COLS` y las claves leídas en `processRow`/`buildExportRows`; en el del SGC ajusta `resolveColumns()`.

**Pruebas:** se realizaron con los listados maestros disponibles (Almera y el listado de SGC de planeación).


## 6. Buenas prácticas y datos

- No subas el Excel a otros servicios para "probarlo": el valor del informe es que corre local.
- Si compartes el informe como PDF, revisa antes que los filtros activos son los que quieres mostrar (el PDF refleja la vista actual).
