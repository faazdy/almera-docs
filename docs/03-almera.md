# 3. Almera — documentación de módulos

Almera (SGI) es el sistema de gestión de calidad de Capital Salud. Esta parte del repo documenta **cómo usar cada módulo**, en tres formatos del mismo contenido (guía web, GuIA `.md`, skill). Las skills están explicadas en [01-skills.md §3](01-skills.md); aquí va el contenido, el estado y cómo ampliarlo.

- Producción: <https://sgi.almeraim.com/sgi/?conid=sgicapitalsalud>
- Pruebas: <https://sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas> (los procedimientos de flujo documental se probaron aquí)

## 1. Módulos documentados

Landing: `almera/index.html`. Cada módulo es una carpeta con `index.html`, `styles/` y `AI/`.

| Módulo | Ruta | Qué cubre |
|---|---|---|
| **Gestión documental** | `modulo-documentos/gestion-documentos/` | Crear un documento (solicitud → aprobación → edición → plantilla online), emisores, clases de documento, buscar/filtrar/exportar, recursos, términos y definiciones, estados, tipo adjunto vs. plantilla. La GuIA más larga (~650 líneas). |
| **Mapa de procesos** | `modulo-documentos/mapa-procesos/` | Mover un subproceso a otro proceso padre (`Admin → Procesos`), cambiar la imagen del mapa y vincular áreas, procesos obsoletos o renombrados, y montar las tablas de **Salidas No Conformes (SNC)** por subproceso (HTML inyectado en Almera, con ayuda de IA; instructivo aparte en la misma carpeta). |
| **Mecanismos de integración** | `modulo-documentos/mecanismos-integracion/` | Comités, clasificaciones, privilegios por comité, actas vs. reuniones, elaborar acta, plantilla institucional, autenticación de externos. |
| **Modelos de gestión** | `modulo-documentos/modelos-gestion/` | Cargar normas (ISO 9001, ISO 45001…), agregar nodos (por nodo o masivo con Excel), relacionar ítems con la caracterización de un proceso, carga masiva de estructura. |
| **Evaluaciones** | `modulo-evaluaciones/evaluaciones/` | Auditorías, plantillas, programa anual, equipo auditor, cuestionario, sistema de referencia, ejecución y hallazgos. |
| **Indicadores** | `modulo-evaluaciones/indicadores/` | Campos adicionales, unidades de medida, metas y semáforo, privilegios/responsables, fechas, notificaciones, clasificación y reportes, asignación masiva de privilegios. |
| **Planes de mejora** | `modulo-evaluaciones/planes-de-mejora/` | Informe de evaluación, hallazgos, evaluadores, sistemas de referencia, puntos de atención. Es el único módulo con capturas (`imgs/`). |
| **Proyectos** | `modulo-proyectos/` | Tipos de proyecto, flujo de estados y transiciones, privilegios, cronogramas, actividades, indicadores en actividades, seguimiento y cierre, gestión presupuestal, integración con plan estratégico. |

Páginas sin skill: `codigos-estructura-organizacional/` (referencia de codificación) y `almera-IA/` (guía de instalación y uso de las skills, con capturas `step-1…11`).

### Estado

| Módulo | Guía web | GuIA `.md` | `.skill` | Validación |
|---|---|---|---|---|
| Gestión documental | ✔ | ✔ | ✔ | Pendientes abiertos con soporte |
| Mapa de procesos | ✔ | ✔ | ✔ | — |
| Mecanismos de integración | ✔ | ✔ | ✔ | **Verificar con pruebas y correos** (`to-do`) |
| Modelos de gestión | ✔ | ✔ | ✔ | — |
| Evaluaciones | ✔ | ✔ | ✔ | Pendientes abiertos con soporte |
| Indicadores | ✔ | ✔ | ✔ | Pendientes abiertos con soporte |
| Planes de mejora | ✔ | ✔ | ✔ | — |
| Proyectos | ✔ | ✔ | ✔ | **Verificar** (`to-do`) |

> El `almera/README.md` y la tabla del README raíz están desfasados: no listan Mapa de procesos ni Modelos de gestión, y `almera/README.md` dice que el skill de Planes de mejora está "pendiente de empaquetar" (ya existe). Usa esta tabla.

## 2. Árbol de Admin

`almera/assets/almera-structure.md` contiene el árbol completo de la pestaña **Admin**, que se usa para ubicar rutas de cualquier módulo. Categorías: **1. Calidad**, **2. Evaluaciones**, **3. General**, **4. Indicadores**, **5. Proyectos** y **6. Riesgos**. Cada GuIA y cada skill repite este árbol en su sección/archivo `00-mapa-navegacion-admin`. Si Almera cambia el menú, actualiza el archivo fuente y las copias.

## 3. Plantilla de una GuIA

Todas siguen el mismo orden; respétalo en los módulos nuevos:

1. **Instrucciones para la IA** — responder solo con lo documentado, avisar si no está cubierto, no inventar botones ni pasos, no presentar lo pendiente como confirmado.
2. **Índice.**
3. **Árbol de navegación de Admin** (completo, no solo el del módulo).
4. **Conceptos básicos.**
5. **Procedimientos paso a paso**, cada uno con su ruta exacta.
6. **Preguntas frecuentes.**
7. **Temas pendientes de validar con soporte Almera**, cada uno con *Contexto*, *Estado* y *Fuente* (minuto de la transcripción).

La parte 7 es la que evita que la IA invente: lo que soporte de Almera no confirmó queda ahí, marcado como tal.

## 4. Cómo agregar un módulo nuevo

1. **Insumos:** transcripción de la capacitación con soporte de Almera + cualquier guía interna. Prueba los flujos en el entorno de **pruebas**.
2. **Redactar la GuIA `.md`** con la plantilla de §3 en `almera/<modulo>/AI/<modulo>-almera.md`.
3. **Crear la skill:** carpeta `almera-<modulo>/` con `SKILL.md` (frontmatter `name` + `description` que liste los temas y disparadores) y `references/` partido por tema (empieza por `00-mapa-navegacion-admin.md`). Empaqueta con [01-skills.md §0](01-skills.md). Nombre del archivo: `almera-<modulo>.skill`.
4. **Crear la guía web:** copia el `index.html` y `styles/style.css` de un módulo existente (los de Indicadores o Planes de mejora son buenos modelos) y adapta contenido; incluye los botones de descarga de GuIA y Skill.
5. **Enlazar** el módulo en `almera/index.html` (lista de módulos con sus descargas).
6. **Probar** la skill en un chat nuevo con preguntas reales; si responde algo que no está en la GuIA, ajusta el `SKILL.md`.
7. **Actualizar** las tablas de estado (esta página y los README).

## 5. Carga masiva de modelos de gestión

En `modulo-documentos/modelos-gestion/template/` hay un caso trabajado completo: el modelo **"Medida de recuperación"** (`MDR-1`), con 227 nodos (5 carpetas + 222 documentos) cargados con éxito.

| Archivo | Para qué |
|---|---|
| `instructivo-simple.md` | Pasos para el usuario: armar el árbol en texto → pedir a la IA la tabla → pegarla en la plantilla Excel → cargarla en Almera. |
| `INSTRUCTIVO carga masiva de estructura - Medida de recuperacion.md` | Versión extensa. |
| `Estructura Medida de recuperacion - carga.xlsx` | Plantilla de carga (hoja `Nodos_Modelo`; columnas Código, Nombre, Clasificación, Clasificación Hijos, Descripción, Padre). |
| `Medida de recuperacion-ejemplo-REAL.xlsx` | Ejemplo real cargado. |
| `generar_estructura_medida_recuperacion.py` | Genera el XLSX desde un árbol en texto, reescribiendo `sheet1.xml` y `sharedStrings.xml` de un export de la plataforma. |

⚠️ El script tiene **rutas absolutas fijas** a la máquina original (`BASE = C:\Users\…\modelos-de-gestion`, y lee un `task.txt` que no está en el repo). Para reutilizarlo hay que cambiar `BASE`, `SRC` y `TASK`. Para casos nuevos, el flujo recomendado es el del instructivo (con IA, sin script).

## 6. Pendientes

**Tareas del equipo (`to-do`):**
- [ ] Meter el árbol de opciones de Admin en la skill general, de modo que todas las skills individuales conozcan la estructura completa de módulos de Almera.
- [ ] Verificar el módulo **Proyectos**.
- [ ] Con ayuda de correos y pruebas, verificar el correcto funcionamiento de **Mecanismos de integración**.
- [ ] Documentar las categorías **General** y **Riesgos** del árbol de Admin (hoy no tienen guía).

**Dudas abiertas con soporte de Almera** (sección "Temas pendientes de validar" de cada GuIA; ahí hay contexto, estado y minuto de la transcripción). Ejemplos:
- Gestión documental: marca de agua en documentos obsoletos/anulados; generación automática de código con estructura personalizada.
- Mecanismos de integración: el cuarto tipo de privilegio por comité no se identificó; error al editar una plantilla existente a nivel de tipo de comité.
- Evaluaciones: origen de un nivel de gestión ya creado ("Avance completo"); si el estado "Pendiente" del flujo es necesario.
- Indicadores: resultados que superan el 100 % de cumplimiento (parámetro por ubicar); notificaciones semanales de atraso que no llegaban.
- Proyectos: notificación automática al cerrar un proyecto (posible, falta validar cómo se configura).

Cuando soporte confirme alguna, pásala del apartado de pendientes al procedimiento correspondiente **en las tres copias** (GuIA, `.skill`, guía web).

**Apuntes sin integrar** (revisar y pasar a la GuIA o descartar): `gestion-documentos/new.txt` (pasos del flujo de documentos en pruebas, incluida una sugerencia de saltar el paso de enviar a revisión para ir directo al coordinador), `gestion-documentos/AI/pulir.txt` (FAQ en borrador: qué pasa al rechazar/aprobar/devolver), `indicadores/add.txt` y `modulo-proyectos/AI/steps.txt` (pasos de creación de tipo de proyecto).

## 7. Mockups

`almera/design/` guarda diseños hechos con Claude Design (`Design Minimal 1/` y `preview-gestion-documentos/`). Son referencia visual; no están enlazados desde las páginas publicadas.
