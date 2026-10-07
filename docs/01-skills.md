# 1. Skills de SABIA

Una **skill** (archivo `.skill`) es un paquete que Claude carga solo cuando el pedido del usuario lo requiere. En SABIA hay dos familias:

| Familia | Qué hace | Cuántas | Dónde vive |
|---|---|---|---|
| **A. Skills de módulo Almera** | *Responden preguntas* sobre cómo usar un módulo de Almera, con rutas y pasos exactos. | 8 | `almera/modulo-*/**/AI/*.skill` |
| **B. Skills de entregables** | *Generan un archivo* (presentación, diagrama de flujo) siguiendo lineamientos institucionales. | 2 | `calidad-ai-agents/<skill>/*.skill` |

---

## 0. Cómo es un `.skill` (aplica a todas)

Un `.skill` es un **zip** cuya carpeta raíz se llama igual que la skill:

```
<nombre-skill>/
├── SKILL.md        Frontmatter (name, description) + instrucciones. Es lo primero que lee Claude.
├── references/     Detalle que Claude abre solo cuando lo necesita
└── assets/         Plantillas, ejemplos, marca (solo en las de entregables)
```

- El campo `description` del frontmatter es lo que decide **cuándo se activa** la skill. Si una skill no se dispara, casi siempre es la descripción.
- Instalación: `Claude → Configuración → Habilidades → Subir habilidad`. Se instala una vez y queda disponible en chats nuevos. Capturas paso a paso: `almera/almera-IA/index.html`.
- Para **crear o editar** una skill con asistencia, usa la skill `skill-creator` de Claude.

### Empaquetar un `.skill` a mano

No hay script de build en el repo. Desde la carpeta que contiene la carpeta de la skill:

```bash
python -c "
import zipfile, os, sys
nombre = sys.argv[1]                      # ej. diagramas-flujo
with zipfile.ZipFile(nombre + '.skill', 'w', zipfile.ZIP_DEFLATED) as z:
    for r, _, fs in os.walk(nombre):
        for f in fs:
            p = os.path.join(r, f)
            z.write(p, p.replace(os.sep, '/'))   # raíz del zip = nombre/
" diagramas-flujo
```

Verifica después con `unzip -l` que la primera ruta sea `<nombre>/SKILL.md`. Excluye lo regenerable y pesado (p. ej. `Tema1.thmx`, 34 MB).

---

## 2. Familia B — Skills de entregables

Las dos están descritas para usuarios en `calidad-ai-agents/entregables/index.html`. Aquí va lo que necesita quien las mantiene.

### 2.1 Qué tienen en común

- Siempre **preguntan antes de producir** (formato, modalidad, estructura) y no generan el archivo final sobre algo que el usuario no confirmó.
- Siempre parten de **insumos de referencia** (plantilla, paleta, ejemplo). Sin ellos, no se improvisa.
- No tienen GuIA `.md`: necesitan ejecutar código.
- Cada una tiene su `assets/PENDIENTE.md`, que es **bitácora de decisiones y pruebas**, no solo lista de pendientes. Léelo antes de cambiar reglas: documenta por qué se descartó cada alternativa.

### 2.2 `presentaciones-institucionales`

**Para qué:** convierte un texto/informe/idea en diapositivas con la plantilla y paleta oficiales, o **consolida** presentaciones ya hechas en un solo deck.

**Flujo (resumen de `SKILL.md`):**
1. Pregunta **formato** (PPTX / HTML / PDF; por defecto PPTX) y **modalidad** (gerencial, informativa, capacitación). Luego audiencia, contenido base y extensión.
2. Propone un **esquema numerado** donde cada diapositiva lleva su layout `L01`–`L14`. Espera visto bueno.
3. Redacta el contenido con las reglas de `references/02` y la **receta del layout** en `references/06` (slots, proporciones y helper exacto de `pptx_kit.py`).
4. Genera en el formato pedido y ofrece ajustes.

**Los 14 layouts** son recetas de composición (no layouts de PowerPoint) que se arman sobre el layout `Contenido Tabla 4` de la plantilla. Se elige por la pregunta que responde la lámina (¿cuánto en total? → L01; ¿cómo se reparte el 100 %? → L06; ¿qué pasos? → L13…). Tabla completa en `SKILL.md` y catálogo de slots en `assets/layouts-gerenciales.md`.

**Archivos clave de `assets/`:**

| Archivo | Para qué |
|---|---|
| `plantilla.pptx` | Base del PPTX (tema "Capital 2025 octubre", Verdana). Versión adelgazada (~0,8 MB). Los placeholders no se usan; todo se compone por coordenadas. |
| `referencia.pptx` | Presentación aprobada: guía de estética y densidad. **No** es base de generación (su tema es Office genérico). |
| `paleta.md` | Colores oficiales (hex) y tipografías. |
| `pptx_kit.py` | Librería de generación: `Deck` (`portada`, `separador`, `contenido`, `texto_pleno`) + helpers (`kpi_tiles`, `barra_apilada`, `etapas`, `cita`, `tabla`, `grafica_barras`, …). |
| `consolidar.py` | Modo consolidar (abajo). |
| `empaquetar-html.js` + `marca/` | Genera el HTML autocontenido incrustando la marca como `data:` URIs. Deben vivir juntos. |
| `optimizar-plantilla.ps1` | Regenera `plantilla.pptx` adelgazada (PowerPoint COM) si cambia la plantilla institucional. |
| `ejemplos-generados/` | Deck de ejemplo (20 diapositivas) en PPTX y HTML, con su script generador. Úsalo como modelo y como prueba de regresión. |

**Modo consolidar** (dispara con "consolidar / unificar / juntar presentaciones"): no cambia contenido, solo reencuadra cada diapositiva bajo la bandera de títulos institucional. Dos pasos con aprobación del usuario entre ambos:

```bash
python assets/consolidar.py inventario a.pptx b.pptx -o plan.json   # analiza y arma un plan editable
python assets/consolidar.py generar plan.json -o consolidado.pptx   # genera el deck + informe
```

Los separadores saturados se limpian solos (los puntos pasan a una diapositiva aparte) y `--portada-consolidada` antepone una portada del consolidado. Detalle en `references/07-consolidar-presentaciones.md` (léelo antes de la primera corrida).

**Entorno:** diseñada para correr en **Claude Code sobre Windows** con Python 3.13 + `python-pptx` y PowerPoint instalado. El PDF desde PPTX usa PowerPoint COM (`SaveAs … 32`); no usa LibreOffice. Si se corre en otro entorno (claude.ai, Linux), hay que resolver el toolchain de PDF.

**Pendientes** (de `assets/PENDIENTE.md` y `context.txt`):
- [ ] Probar la ruta **PDF desde HTML** (puppeteer/Chromium) en la máquina de trabajo.
- [ ] **Tamaño de personajes en PPTX:** salen más grandes que en HTML (en HTML: `.visual img{width:55%; max-height:65%; object-fit:contain}`). Esperado en PPTX: alto máx. 10 cm, ancho automático. Llevar esa regla a `pptx_kit._add_personaje`.
- [ ] Documentar en `references/02` y `04` el uso de `marca/` (fondo de portada vs. separador, un personaje máx. por diapositiva, íconos en títulos, franja de sellos en el pie).
- [ ] Calibrar los umbrales de densidad de `references/02-reglas-de-diseno.md` contra `referencia.pptx`.
- [ ] Si se aprueba instalar la fuente *Roboto Slab*, cambiar `F_TIT` en `pptx_kit.py` y recalibrar tamaños de título.
- Quedan por coordenadas (sin helper propio) L04 columna lateral, L05 split y L09 bloque de decisión.

### 2.3 `diagramas-flujo`

**Para qué:** convierte el cuadro de actividades de un procedimiento (`.doc/.docx`, Excel o texto) en un diagrama estilo Bizagi Modeler.

**Estándar vigente (el del `.skill`):**

| Tema | Regla |
|---|---|
| Estructura | Pool con el nombre del procedimiento + **carriles horizontales por responsable**. **Fases** como bandas verticales *solo si la fuente las define* (nunca se infieren). |
| Texto | ≤ 100 caracteres por actividad (el script falla si se pasa). Verbo en infinitivo + objeto. Se recorta antes de partir. |
| Numeración | La de la fuente (8.1, 8.2 si se parte un paso). Nunca renumerar. |
| Decisiones | Rombo solo si la fuente define la bifurcación. Decisión implícita → actividad plana + nota amarilla. |
| Validación | Punto 🟢 verde (correcto) / 🟡 amarillo (revisar) / 🔴 rojo (revisión obligatoria) en la esquina de cada paso, con leyenda y tabla. El color va en el punto, nunca como relleno. |
| Variaciones | Un diagrama general + uno por variación. |
| Salidas | **Siempre** PDF + PNG + JPG + SVG + **BPMN 2.0** + tabla de validación `.md`. |
| Comentarios de revisión | Se pregunta siempre dónde van: solo PDF (default), solo BPMN, o ambos. |

**Cómo funciona:** Claude lee la fuente, escribe un **spec JSON** y corre `scripts/generar_diagrama.py spec.json --salida <dir> --comentarios <pdf|bpmn|ambos>`. El script dibuja SVG → PDF/PNG/JPG con `cairosvg` y escribe el BPMN con coordenadas. Formato del spec en `references/06-generador-y-spec.md`; modo automático (procedimientos lineales) vs. manual (`col`/`fila` + `flujos`, con decisiones y retornos).

**Dependencias del generador:** Pillow, `cairosvg`, fuentes DejaVu. Verificado en el sandbox de claude.ai (no hace falta Mermaid CLI ni Chromium). El entorno decidido es **Claude web/app**, no Claude Code local.

**Pruebas de regresión:** `assets/specs/` tiene 4 specs reales (PR-016-RIS con fases; PR-003-GRI con 3 decisiones y retorno; PR-007-GRI con 4 carriles; PR-004-ADM con 9 carriles y 13 notas). Tras cualquier cambio al script, regenera los cuatro y revisa los PNG.

**Historia que conviene conocer** (detalle en `assets/PENDIENTE.md`):
- La skill nació con **Mermaid** y pasó a un generador propio (`generar_diagrama.py`). Una causa documentada en `PENDIENTE.md`: en Mermaid las flechas hacia un nodo dentro de un `subgraph` podían terminar en el borde del clúster, lo que hacía poco fiables los cruces de carril. Mermaid queda solo como reserva si no hay entorno de código.
- **BPMN y Bizagi:** una primera prueba de BPMN 2.0 escrito a mano no fue aceptada por Bizagi; en pruebas posteriores con el BPMN que genera el script, Bizagi Modeler sí lo importó (confirmado por el usuario). Se descartó generar el formato nativo `.bpm` calcado de un export real (dos rondas). No lo reintentes sin un export de Bizagi donde se vean las fases y sin saber qué se veía mal.
- Tras importar el BPMN en Bizagi conviene revisar etiquetas de rombos, grupos de fase y notas.
- Los colores de inicio/fin **varían entre exports reales de Bizagi**: si hay un export del procedimiento concreto, usar sus colores; si no, el default de `assets/paleta-bizagi.md`.
- El diagrama incrustado en el `.doc` fuente suele estar **desactualizado**: manda el cuadro de actividades de la versión vigente.
- Si el usuario sube dos veces el mismo procedimiento, se avisa y no se rehace.

### 2.4 Estado de cada skill

| Skill | `.skill` | Estado |
|---|---|---|
| presentaciones-institucionales | Vigente, coincide con las fuentes del repo | Funcional; quedan los pendientes de §2.2 |
| diagramas-flujo | Vigente (v2.5), **más nuevo que las fuentes del repo** | Funcional; urgente reconciliar (§3.4) |

---

## 3. Familia A — Skills de módulo Almera

### 3.1 Inventario

| Módulo | Skill (`name`) | GuIA `.md` fuente | Carpeta |
|---|---|---|---|
| Gestión documental | `almera-documentos` | `documentos-almera.md` | `almera/modulo-documentos/gestion-documentos/AI/` |
| Mapa de procesos | `almera-mapa-procesos` | `mapa-procesos-almera.md` | `…/mapa-procesos/AI/` |
| Mecanismos de integración | `almera-mecanismos` | `mecanismos-integracion.md` | `…/mecanismos-integracion/AI/` |
| Modelos de gestión | `almera-modelos-gestion` | `modelos-gestion-almera.md` | `…/modelos-gestion/AI/` |
| Evaluaciones | `almera-evaluaciones` | `evaluaciones-almera.md` | `almera/modulo-evaluaciones/evaluaciones/AI/` |
| Indicadores | `almera-indicadores` | `indicadores.md` | `…/indicadores/AI/` |
| Planes de mejora | `almera-planes-mejora` | `docs-plan-de-mejora.md` | `…/planes-de-mejora/AI/` |
| Proyectos | `almera-proyectos` | `proyectos-almera.md` | `almera/modulo-proyectos/AI/` |

### 3.2 Anatomía

- `SKILL.md` es corto: cuándo usar la skill, reglas de comportamiento y un **índice de `references/`**.
- `references/` parte la GuIA en archivos temáticos numerados: `00-mapa-navegacion-admin.md`, `01-conceptos-basicos.md`, un archivo por procedimiento, `…-preguntas-frecuentes.md` y `…-pendientes-validar.md`. Mapa de procesos y Modelos de gestión usan un solo archivo de referencia.
- Reglas de comportamiento que **todas** comparten (vienen de la plantilla de GuIA):
  1. Responder solo con lo documentado, paso a paso, con la ruta exacta.
  2. No inventar botones, menús ni pasos.
  3. Si no está cubierto, decirlo.
  4. Lo que está en **"Temas pendientes de validar"** no se presenta como hecho confirmado.

### 3.3 Cómo se actualiza el contenido de un módulo

Hay **tres copias** que se sincronizan a mano:

1. `AI/<modulo>.md` — GuIA completa.
2. `AI/almera-<modulo>.skill` — la GuIA partida en `references/`.
3. `index.html` — guía web curada.

Procedimiento recomendado:
1. Edita la GuIA `.md` (es la fuente de verdad).
2. Refleja el cambio en el `references/` correspondiente del `.skill` (descomprime, edita, vuelve a empaquetar con §0).
3. Refleja el cambio en el `index.html`.
4. Si el dato dejó de estar "pendiente de validar", muévelo de la sección de pendientes a su procedimiento en las tres copias.
5. Prueba la skill en un chat nuevo con 2–3 preguntas reales del módulo.

> Hay archivos de trabajo sueltos (`new.txt`, `pulir.txt`, `add.txt`, `steps.txt`) con apuntes que aún no se pasaron a la GuIA. Revísalos al retomar cada módulo.

### 3.4 ⚠️ `diagramas-flujo`: la carpeta del repo está desactualizada

Comparando `calidad-ai-agents/diagramas-flujo/` con `diagramas-flujo.skill`:

| Estado | Archivos |
|---|---|
| **Solo en el `.skill`** (no existen en el repo) | `scripts/generar_diagrama.py`, `references/06-generador-y-spec.md`, `references/07-lectura-de-fuentes.md`, `assets/specs/` (4 specs + README), `assets/ejemplos-reales/diagrama-ejemplo-comentarios-rev.bpmn` |
| **Distintos** (la versión del repo es la vieja) | `SKILL.md`, `references/01` a `05`, `assets/paleta-bizagi.md`, `assets/PENDIENTE.md` |
| **Solo en el repo** | `fix.md` (bug viejo de Mermaid, ya resuelto), `pruebas/diagrama-*.bpmn` |

Los commits recientes borraron las versiones intermedias del `.skill` (`-v2.skill`, `-v3.zip`), así que **hoy el `.skill` actual es la única copia del generador**.

**Qué hacer (hazlo antes de cualquier otro cambio):**
1. Haz una copia de seguridad de `diagramas-flujo.skill` fuera del repo.
2. Extrae el `.skill` sobre `calidad-ai-agents/` para que el repo refleje la versión vigente.
3. Commitea eso como un cambio aparte ("sincronizar fuentes de diagramas-flujo con .skill v2.5").
4. Elimina o archiva `fix.md`.
5. Desde ahí, edita las fuentes y re-empaqueta; el `.skill` deja de ser la única fuente.

---

## 4. Skills "generales" vs. específicas

Una tarea abierta (`to-do`, línea 1) pide **meter el árbol de opciones de Admin en la skill general**, de modo que cada skill de módulo conozca la estructura completa de Almera. Hoy cada skill tiene su `00-mapa-navegacion-admin.md`; la fuente del árbol es `almera/assets/almera-structure.md`. Si el árbol de Admin cambia en Almera, actualiza ese archivo y los `00-mapa-navegacion-admin.md` de cada skill.

---

## 5. Seguridad y datos (resumen de `calidad-ai-agents/SEGURIDAD.md`)

El repo es privado y los ejemplos están censurados. El riesgo está en el momento de **usar la skill con información real**.

- **Minimizar lo que entra al chat:** diagramas necesitan pasos y roles (no nombres/cédulas de afiliados); presentaciones necesitan mensaje y cifras agregadas (no tablas nominales).
- **Ley 1581 de 2012:** datos de salud, biométricos y de menores son sensibles. Los casos usados como insumo deben estar **anonimizados**, no solo resumidos. Para ilustrar variaciones, usar casos inventados ("Afiliado A").
- **Retención:** si la cuenta de Claude no tiene acuerdo empresarial de no retención/no entrenamiento, no pegar datos reales. Confirmarlo con quien administre la cuenta.
- **El entregable hereda la sensibilidad del insumo:** mismo control de acceso al subirlo a Teams/SharePoint/correo.
- Checklist completo de 5 puntos en `SEGURIDAD.md`.

---

## 6. Backlog de skills

Pendientes ya anotados arriba, más ideas del `to-do`:
- Skills de automatización para **ChatGPT Pro** (explorar cómo crear un agente especializado).
- Posible **CLI para agente local** (Qwen + LM Studio).
- **"Cerebro" RAG para la DEP** (pruebas con Ollama y archivos locales; definir alcance de los LLM).
- Ampliar la cobertura de Almera a las categorías **General** y **Riesgos** (ver `03-almera.md`).
