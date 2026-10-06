# SABIA
### Sistema de Automatización, Base de información e Inteligencia Artificial

**Capital Salud · Sistema de Gestión de Calidad (SGC)**

> Documento de presentación del proyecto — visión general, problema, solución, arquitectura, estado actual y hoja de ruta.

---

## Tabla de contenido

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [El problema](#2-el-problema)
3. [La solución](#3-la-solución)
4. [Qué es SABIA, en una frase](#4-qué-es-sabia-en-una-frase)
5. [Los tres componentes del proyecto](#5-los-tres-componentes-del-proyecto)
6. [Cómo funciona — el ciclo de una habilidad](#6-cómo-funciona--el-ciclo-de-una-habilidad)
7. [Arquitectura técnica](#7-arquitectura-técnica)
8. [Estado actual](#8-estado-actual)
9. [Casos de uso reales](#9-casos-de-uso-reales)
10. [Seguridad y manejo de información](#10-seguridad-y-manejo-de-información)
11. [Impacto esperado](#11-impacto-esperado)
12. [Hoja de ruta](#12-hoja-de-ruta)
13. [Cómo acceder y probarlo](#13-cómo-acceder-y-probarlo)
14. [Preguntas frecuentes](#14-preguntas-frecuentes)
15. [Glosario](#15-glosario)

---

## 1. Resumen ejecutivo

**SABIA** es el proyecto de conocimiento y automatización del área de Calidad de Capital Salud, construido inicialmente sobre **Almera (SGI)**, el sistema de gestión documental institucional.

Nació para resolver un problema puntual — que la única forma de resolver una duda sobre Almera fuera revisar una grabación de capacitación de una hora — y creció hasta convertirse en tres cosas a la vez:

| | |
|---|---|
| 📚 **Base de conocimiento** | Documentación operativa completa de 6 módulos de Almera, navegable en la web. |
| ⚙️ **Automatización** | Herramientas que generan entregables (informes, presentaciones, diagramas) siguiendo lineamientos institucionales. |
| 🤖 **Agentes de IA** | Cada módulo y cada capacidad de automatización empaquetada como habilidad instalable en Claude. |

Hoy existen **8 habilidades de IA publicadas**, **6 módulos de Almera documentados** en 33 secciones, y **2 herramientas web** que analizan datos exportados del sistema sin que la información salga del equipo del usuario.

No requiere infraestructura: es un sitio estático (HTML/CSS/JS), sin servidor propio, sin base de datos, construido y mantenido con herramientas de IA (Claude).

---

## 2. El problema

Capital Salud opera su Sistema de Gestión de Calidad sobre **Almera (SGI)**, una plataforma con múltiples módulos: Gestión documental, Evaluaciones, Indicadores, Mecanismos de integración, Planes de mejora, Proyectos, y más.

**Síntomas identificados:**

- Cuando alguien tiene una duda puntual ("¿cómo creo una clase documental?", "¿cómo configuro un indicador con semaforización?"), la única fuente disponible es una **grabación de capacitación de una hora**, de la cual normalmente solo **dos minutos** responden la pregunta real.
- **Nadie usa todos los módulos.** Un usuario de Evaluaciones nunca toca Mecanismos de Integración, pero si tiene una duda sobre Evaluaciones igual debe revisar una grabación genérica que mezcla todos los temas.
- El conocimiento operativo vive en la cabeza de pocas personas del equipo. Tareas recurrentes del área — diagramar un procedimiento en Bizagi, armar una presentación institucional, consolidar un informe — dependen de que esa persona específica esté disponible.
- La curva de aprendizaje de un usuario nuevo es alta: no hay una guía de referencia rápida por módulo, solo material de capacitación genérico y disperso.

**Consecuencia:** tiempo de soporte interno desperdiciado en preguntas repetitivas, dependencia de personas puntuales para tareas de producción, y fricción para cualquiera que necesite resolver algo específico y puntual.

---

## 3. La solución

Por cada módulo de Almera se construyó:

1. Una **guía web navegable** — versión curada y visual del procedimiento, para consulta rápida.
2. Un **documento de referencia técnico** (`GuIA.md`) — el contenido completo, estructurado para que cualquier IA lo pueda leer y usar como contexto.
3. Una **habilidad de IA instalable** (Claude Agent Skill) construida sobre ese mismo documento — responde preguntas sobre el módulo con la documentación real del sistema: rutas exactas, procedimientos paso a paso, y **avisando explícitamente cuándo algo no está confirmado con soporte de Almera**, en vez de inventarlo.

Sobre esa misma base se construyeron además **herramientas de automatización** que no solo responden preguntas sino que **producen el entregable terminado**: un informe de indicadores de calidad de datos, una presentación institucional, un diagrama de flujo.

---

## 4. Qué es SABIA, en una frase

> **SABIA es la documentación operativa de Almera, convertida en agentes de IA que cualquier persona del área puede instalar para resolver sus propias dudas y generar sus propios entregables, sin depender de otra persona del equipo.**

El nombre es un acrónimo deliberado:

- **S**istema de
- **A**utomatización,
- **B**ase de información e
- **I**nteligencia
- **A**rtificial

---

## 5. Los tres componentes del proyecto

### 5.1 Documentación de Almera (`almera/`)

El núcleo original del proyecto. Por cada módulo del sistema:

- Guía web paso a paso con capturas y rutas exactas de navegación.
- Árbol de navegación completo del panel de administración de Almera (no solo el módulo propio), para ubicar cualquier opción del sistema.
- Preguntas frecuentes y procedimientos documentados.
- Sección explícita de **temas pendientes de validar con soporte de Almera** — dudas abiertas en capacitación, nunca presentadas como respuesta confirmada.

### 5.2 Agentes de IA especializados (`calidad-ai-agents/`)

Dos familias de habilidades, empaquetadas en el formato estándar **Claude Agent Skill** (`.skill`):

- **Familia 1 — Conocimiento de módulo:** una habilidad por cada módulo de Almera documentado (Gestión documental, Indicadores, Evaluaciones, Planes de mejora, Proyectos, Mecanismos de integración). Responde consultas sobre el procedimiento real.
- **Familia 2 — Producción de entregables:** habilidades que generan el entregable terminado siguiendo lineamientos institucionales:
  - **Presentaciones institucionales** — convierte un texto o informe en diapositivas que respetan la plantilla y paleta oficiales, exporta a PPTX, HTML o PDF, y puede **consolidar varias presentaciones existentes** en un solo deck sin alterar su contenido.
  - **Diagramas de flujo** — levanta el flujo de un procedimiento a partir de su descripción textual y lo entrega diagramado, con reglas fijas de formato (máx. 100 caracteres por actividad, validación por colores verde/amarillo/rojo, paleta consistente con Bizagi Modeler) y manejo de variaciones del procedimiento.

### 5.3 Herramientas de informes (dashboards en el navegador)

- **Informe de Documentos** — sube el Listado Maestro de Documentos exportado de Almera y obtiene indicadores, antigüedad y distribución por categoría al instante.
- **Control de Documentos SGC** — sube el listado maestro de la carpeta local compartida (distinto del de Almera) y obtiene indicadores de vigencia, actualización y hallazgos de calidad de datos.

Ambas herramientas procesan el archivo **100% en el navegador del usuario** — el Excel nunca se sube a ningún servidor.

---

## 6. Cómo funciona — el ciclo de una habilidad

```
Grabación de capacitación          Documentación/guías
  con soporte Almera          +    internas existentes
            │                              │
            └──────────────┬───────────────┘
                            ▼
                 Se redacta la GuIA.md
   (procedimientos + reglas del sistema + dudas sin resolver)
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
   Se empaqueta como .skill      Se construye la guía web
   (Claude Agent Skill)          (index.html curado y visual)
              │                           │
              ▼                           ▼
   El usuario descarga el .skill   El usuario consulta la
   y lo instala en su asistente    guía directamente en el
   de IA para preguntar o          navegador, sin IA
   generar un entregable
```

La `GuIA.md` es el documento fuente único: de ahí sale tanto la habilidad de IA como la guía web. Esto garantiza que el agente de IA **nunca responda con una suposición** que no esté también publicada en la guía visual.

---

## 7. Arquitectura técnica

### 7.1 Principios de diseño

- **Sitio 100% estático** — HTML/CSS/JS plano. Sin backend, sin build step, sin `package.json`, sin framework.
- **Sin base de datos ni servidor propio** — no existe superficie de ataque de almacenamiento de datos que asegurar. Todo el conocimiento vive en documentos versionados en Git.
- **Procesamiento en el navegador** — los dashboards de informes usan Chart.js y SheetJS (vendored localmente) para leer y calcular todo client-side.
- **Agent Skills como formato de distribución** — cada `.skill` es un paquete comprimido con:
  - `SKILL.md` — instrucciones y flujo de trabajo, lo primero que carga el agente.
  - `references/` — detalle bajo demanda, para no saturar el contexto inicial.
  - `assets/` — plantillas y archivos de referencia obligatorios (p. ej. la plantilla PPTX institucional, la paleta de Bizagi).
- **Sin lock-in de proveedor** — la `GuIA.md` de cada módulo es markdown plano: sirve igual para Claude que para cualquier otro asistente de IA capaz de leer un documento de contexto.

### 7.2 Estructura del repositorio

```
almera-docs/
├── index.html                          # landing general del proyecto SABIA
├── almera/                             # documentación pura de Almera
│   ├── modulo-documentos/
│   │   ├── gestion-documentos/
│   │   │   ├── index.html              # guía web
│   │   │   └── AI/
│   │   │       ├── documentos-almera.md       # GuIA: referencia completa
│   │   │       └── almera-documentos.skill    # empaquetada como Agent Skill
│   │   └── mecanismos-integracion/
│   ├── modulo-evaluaciones/
│   │   ├── evaluaciones/
│   │   ├── indicadores/
│   │   └── planes-de-mejora/
│   ├── modulo-proyectos/
│   ├── almera-IA/                      # cómo instalar y usar las habilidades
│   ├── codigos-estructura-organizacional/
│   ├── informe-documentos/             # dashboard: Listado Maestro → KPIs
│   └── control-documentos-sgc/         # dashboard: control SGC → KPIs
├── calidad-ai-agents/                  # skills transversales, no atadas a un módulo
│   ├── presentaciones-institucionales/
│   ├── diagramas-flujo/
│   └── entregables/                    # explicación de cómo usar estas habilidades
└── styles/                             # estilos compartidos
```

### 7.3 Dependencias externas

Ninguna que requiera instalación: dos librerías JS vendored (`chart.umd.min.js`, `xlsx.full.min.js`) para los dashboards, fuentes de Google Fonts. Sin gestor de paquetes, sin pipeline de CI/CD todavía.

### 7.4 Entorno de ejecución de las skills de producción

Las habilidades de **presentaciones institucionales** y **diagramas de flujo** ejecutan scripts propios (Python — `python-pptx`, conversión a PDF, renderizado de diagramas) y asumen el entorno de ejecución de código de Claude. Se usan **exclusivamente desde Claude**, no desde cualquier asistente de IA genérico.

---

## 8. Estado actual

### 8.1 Documentación de módulos

| Módulo | Guía web | GuIA `.md` | Habilidad `.skill` | Secciones |
|---|---|---|---|---|
| Gestión documental | ✅ Completa | ✅ Completo | ✅ Publicada | 6 |
| Indicadores | ✅ Completa | ✅ Completo | ✅ Publicada | 6 |
| Evaluaciones | ✅ Completa | ✅ Completo | ✅ Publicada | 4 |
| Planes de mejora | ✅ Completa | ✅ Completo | ✅ Publicada | 3 |
| Proyectos | ✅ Completa | ✅ Completo | ✅ Publicada | 11 |
| Mecanismos de integración | ✅ Completa | ✅ Completo | ✅ Publicada | 3 |
| Códigos de estructura organizacional | ✅ Completa | — | Fuera del sistema de IA (página de referencia) | 3 |

**6 módulos documentados · 33 secciones cubiertas.**

### 8.2 Habilidades de IA

| # | Habilidad | Familia | Estado |
|---|---|---|---|
| 01 | Gestión documental | Conocimiento de módulo | Publicada |
| 02 | Indicadores | Conocimiento de módulo | Publicada |
| 03 | Planes de mejora | Conocimiento de módulo | Publicada |
| 04 | Evaluaciones | Conocimiento de módulo | Publicada |
| 05 | Proyectos | Conocimiento de módulo | Publicada |
| 06 | Mecanismo de integración | Conocimiento de módulo | Publicada |
| 07 | Presentaciones institucionales | Entregable | Publicada |
| 08 | Diagramas de flujo | Entregable | Publicada |
| 09 | Borradores de procedimientos | Entregable | En construcción |

**8 de 9 habilidades publicadas.**

### 8.3 Herramientas de informe

| Herramienta | Entrada | Qué entrega | Procesamiento |
|---|---|---|---|
| Informe de Documentos | Listado Maestro exportado de Almera | Indicadores, antigüedad, distribución por categoría | 100% en el navegador |
| Control de Documentos SGC | Listado maestro de carpeta local compartida | Vigencia, actualización, hallazgos de calidad de datos | 100% en el navegador |

---

## 9. Casos de uso reales

- **"¿Cómo creo una clase documental nueva en Almera?"** → se instala la habilidad de Gestión documental en Claude y se pregunta directamente; responde con la ruta exacta del sistema.
- **"Necesito armar la presentación trimestral de indicadores con la plantilla oficial."** → se usa la habilidad de Presentaciones institucionales: se pega el informe y se obtiene el PPTX terminado, con la paleta y el layout corporativo.
- **"Hay que diagramar este procedimiento nuevo para la caracterización del proceso."** → se describe el procedimiento en texto y la habilidad de Diagramas de flujo entrega el diagrama validado por colores, listo para anexar.
- **"¿Qué tan desactualizado está nuestro listado maestro de documentos?"** → se sube el Excel exportado al dashboard de Informe de Documentos y se obtienen los indicadores de calidad de datos al instante, sin depender de nadie más.
- **"Tengo cinco presentaciones sueltas de distintas personas del equipo y necesito un solo deck consolidado."** → la habilidad de Presentaciones institucionales las unifica bajo la misma plantilla y numeración de diapositivas, sin tocar el contenido.

---

## 10. Seguridad y manejo de información

El repositorio es **privado** y el proyecto no introduce infraestructura propia de almacenamiento — pero el uso de las habilidades con información real sí exige criterio:

- **Minimizar lo que entra al chat.** Las habilidades necesitan la *estructura* del insumo (pasos, roles, cifras agregadas), no el documento completo. Si un dato no cambia lo que el entregable necesita comunicar, no debe pasar por el prompt.
- **Datos sensibles (Ley 1581 de 2012).** Salud, datos biométricos, origen étnico, orientación sexual/política/religiosa y datos de menores tienen protección reforzada. Ningún caso usado como insumo debe traer identificación real de una persona — se usan casos ficticios o anonimizados (p. ej. "Afiliado A").
- **Dónde corre la skill importa.** Antes de pegar información real y delicada, se confirma si la cuenta de Claude de la organización tiene acuerdo empresarial de no retención/no entrenamiento. Si no se sabe, se trata como si no lo hubiera.
- **El entregable hereda la sensibilidad del input.** Un PPTX o un diagrama generado a partir de datos reales sigue siendo un documento sensible — se le aplica el mismo control de acceso que al documento fuente antes de compartirlo.

---

## 11. Impacto esperado

- **Menos tiempo de soporte interno** para preguntas repetitivas sobre Almera.
- **Curva de aprendizaje más corta** para usuarios nuevos de cada módulo — consulta puntual en vez de grabación completa.
- **Autoservicio para tareas de producción** del área de Calidad (diagramar, presentar, informar) que hoy dependen de una sola persona.
- **Trazabilidad del conocimiento** — el procedimiento documentado queda versionado en Git, no solo en la memoria de quien lo capacitó.
- **Reutilización del mismo conocimiento en dos formatos** — la misma `GuIA.md` sirve como guía web para humanos y como contexto para IA, sin mantener dos fuentes de verdad distintas.

---

## 12. Hoja de ruta

- Cerrar la habilidad de **borradores de procedimientos** (9ª habilidad, en construcción).
- Ampliar cobertura de Almera más allá de Calidad, Evaluaciones, Indicadores y Proyectos — las categorías **General** y **Riesgos** del árbol de administración todavía no tienen documentación propia.
- Evaluar un pipeline de CI/CD ligero para validar que los `.skill` y las `GuIA.md` se mantengan sincronizados.
- Explorar métricas de uso reales (descargas de `.skill`, consultas a los dashboards) para priorizar la siguiente habilidad a construir.

---

## 13. Cómo acceder y probarlo

| Recurso | Enlace / ruta |
|---|---|
| Producción de Almera | [sgi.almeraim.com/sgi/?conid=sgicapitalsalud](https://sgi.almeraim.com/sgi/?conid=sgicapitalsalud) |
| Pruebas de Almera | [sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas](https://sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas) |
| Landing del proyecto SABIA | `index.html` (raíz del repositorio) |
| Documentación de módulos | `almera/index.html` |
| Agentes de IA especializados | `calidad-ai-agents/index.html` |
| Informe de Documentos | `almera/informe-documentos/index.html` |
| Control de Documentos SGC | `almera/control-documentos-sgc/index.html` |
| Instalar una habilidad | Se descarga el `.skill` desde la página de cada módulo (botón **Skill**) y se adjunta directamente en la conversación con Claude — sin configuración adicional. |
| Proponer una nueva habilidad | Formulario disponible desde `calidad-ai-agents/index.html` (sección "Siguiente habilidad"). |

---

## 14. Preguntas frecuentes

**¿SABIA reemplaza a Almera?**
No. SABIA es una capa de documentación y automatización construida *sobre* Almera — no interactúa con el sistema ni modifica sus datos. Se consulta en paralelo.

**¿Las habilidades pueden inventar un procedimiento que no existe?**
Están instruidas explícitamente para no hacerlo: si algo no está documentado o no fue confirmado con soporte de Almera, lo avisan en vez de inventar un paso o un botón.

**¿Quién puede usar las habilidades de IA?**
Cualquier persona del área con acceso a un asistente de IA compatible con Agent Skills (Claude). Las de conocimiento de módulo (`.skill` + `.md`) son portables a otros asistentes; las de producción de entregables requieren el entorno de ejecución de Claude.

**¿Los archivos subidos a los dashboards quedan guardados en algún servidor?**
No. Todo el procesamiento de los Excel exportados ocurre en el navegador del usuario; el archivo nunca se transmite a un servidor.

**¿Qué pasa si encuentro un error en una guía?**
El proyecto se mantiene como documentación viva en Git — cualquier corrección se puede proponer y se refleja tanto en la guía web como en la `GuIA.md` y, por extensión, en la habilidad de IA correspondiente.

---

## 15. Glosario

| Término | Significado |
|---|---|
| **Almera (SGI)** | Sistema de Gestión Institucional sobre el que opera el Sistema de Gestión de Calidad de Capital Salud. |
| **GuIA.md** | Documento de referencia técnico por módulo; fuente única de la que salen tanto la guía web como la habilidad de IA. |
| **Agent Skill (`.skill`)** | Formato de empaquetado de Claude: instrucciones + flujo de trabajo + referencias + plantillas, instalable en una conversación. |
| **SKILL.md** | Archivo de entrada de un Agent Skill — lo primero que el agente lee al cargar la habilidad. |
| **Habilidad de conocimiento de módulo** | Skill que responde preguntas sobre un módulo de Almera usando su `GuIA.md`. |
| **Habilidad de producción / entregable** | Skill que genera un documento terminado (presentación, diagrama) siguiendo lineamientos institucionales. |
| **SGC** | Sistema de Gestión de Calidad. |

---

*Documento vivo — actualizado 2026. Para el detalle técnico de implementación, ver `README.md` en la raíz del repositorio.*
