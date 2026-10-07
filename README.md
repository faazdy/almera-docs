# SABIA

**S**istema de **A**utomatización, **B**ase de información e **I**nteligencia **A**rtificial — el proyecto de conocimiento y automatización del área de Calidad, construido inicialmente sobre Almera (SGI).

> **¿Retomas el proyecto?** Empieza por [`docs/`](docs/README.md): skills, informes y módulos de Almera, con pendientes y riesgos del traspaso.

---

## 1. Resumen ejecutivo

**El problema:** cuando alguien en Capital Salud tiene una duda puntual sobre cómo usar un módulo de Almera, la única fuente disponible son grabaciones de capacitación de una hora, de las cuales dos minutos responden la pregunta real. Y casi nadie usa todos los módulos — un usuario de Evaluaciones nunca toca Mecanismos de Integración, pero igual tendría que revisar una grabación genérica para resolver algo suyo.

**Qué se construyó:** por cada módulo de Almera hay una guía web navegable, un documento de referencia técnico y una **habilidad de IA instalable** (Claude Agent Skill) que responde preguntas sobre ese módulo con la documentación real del sistema — rutas exactas, procedimientos paso a paso, y avisando explícitamente cuándo algo no está confirmado con soporte de Almera, en vez de inventarlo.

**Por qué ya no es "solo documentación":** el proyecto creció en tres direcciones:

- **Base de conocimiento** — guías y documentos de referencia por módulo (el núcleo original).
- **Automatización** — herramientas que generan entregables siguiendo lineamientos institucionales (presentaciones, diagramas de flujo), y un dashboard que procesa el Listado Maestro de Documentos exportado de Almera para dar indicadores de calidad de datos al instante.
- **Agentes de IA** — cada módulo y cada capacidad de automatización queda empaquetado como skill, instalable en Claude, para que cualquiera con acceso resuelva sus dudas o genere su entregable sin depender de otra persona del equipo.

**Impacto esperado:** menos tiempo de soporte interno para preguntas repetitivas de Almera, curva de aprendizaje más corta para usuarios nuevos de cada módulo, y un canal de autoservicio (vía IA) para tareas de Calidad que hoy dependen de una sola persona (diagramar en Bizagi, armar una presentación institucional, etc.).

---

## 2. Cómo está construido (parte técnica)

### 2.1 Arquitectura

- **Sitio 100% estático**: HTML/CSS/JS plano, sin backend, sin build step, sin `package.json`.
- **Sin base de datos ni servidor propio** → no hay superficie de ataque de almacenamiento de datos que asegurar. Toda la "inteligencia" vive en documentos versionados en Git, no en infraestructura.
- **Procesamiento 100% en el navegador**: el dashboard de `informe-documentos/` y `control-documentos-sgc/` (Chart.js + SheetJS/xlsx.js, ambos vendored localmente) lee el Excel exportado anclado y calcula todo client-side — el archivo nunca sale del equipo del usuario ni se sube a ningún servidor. Cero riesgo de fuga de datos por esta vía.
- **Agent Skills como formato de distribución de conocimiento**: cada `.skill` es un paquete comprimido con `SKILL.md` (instrucciones + flujo, lo primero que carga el agente), `references/` (detalle bajo demanda) y `assets/` (plantillas). Es el mismo formato para las skills de módulo (conocimiento) y las skills de producción (generación de entregables).

### 2.2 Estructura del repositorio

```
almera-docs/
├── index.html                          # landing general, enlaces a todos los módulos
├── modulo-*/                           # un directorio por módulo de Almera
│   └── <submódulo>/
│       ├── index.html                  # guía web navegable
│       ├── styles/
│       └── AI/
│           ├── <modulo>.md             # GuIA: documento de referencia completo
│           └── almera-<modulo>.skill   # el mismo contenido empaquetado como Agent Skill
├── informe-documentos/                 # dashboard interactivo (Listado Maestro → KPIs)
├── codigos-estructura-organizacional/  # referencia de codificación organizacional
├── design/                             # mockups y canvases de Claude Design
└── assets/                             # estilos e íconos compartidos
```

Cada `GuIA.md` sigue una plantilla fija para que cualquier IA que la lea sepa cómo comportarse:

1. **Instrucciones para la IA** — responder solo con lo documentado, avisar si algo no está cubierto, no inventar botones ni pasos.
2. **Árbol de navegación completo de Admin** — el mapa de todos los módulos de Almera (no solo el propio), para ubicar cualquier opción aunque sea de otro módulo.
3. **Conceptos, procedimientos paso a paso y preguntas frecuentes**, con ruta exacta dentro del sistema.
4. **Temas pendientes de validar con soporte Almera** — dudas abiertas en capacitación, marcadas explícitamente como no confirmadas.

### 2.3 Cómo se construye cada módulo

1. Se parte de la grabación de capacitación con soporte de Almera y de documentación/guías internas existentes.
2. Se arma la `GuIA.md`: procedimientos, reglas del sistema, y sección aparte de lo no resuelto en la capacitación.
3. Se empaqueta ese contenido como `.skill` de Claude (la `GuIA.md` sirve igual para cualquier otro agente de IA que la pueda leer — no hay lock-in de proveedor).
4. Se construye la guía web (`index.html`) como versión curada y visual del mismo contenido.

### 2.4 Dependencias externas

Ninguna que requiera instalación: dos librerías JS vendored (`chart.umd.min.js`, `xlsx.full.min.js`) para el dashboard, fuentes de Google Fonts. Sin frameworks, sin gestor de paquetes, sin pipeline de CI/CD todavía.

---

## 3. Estado actual

| Módulo | Guía web | GuIA `.md` | Habilidad `.skill` |
|---|---|---|---|
| Gestión documental | Completa | Completo | Disponible |
| Mapa de procesos | Completa | Completo | Disponible |
| Modelos de gestión | Completa | Completo | Disponible |
| Evaluaciones | Completa | Completo | Disponible |
| Indicadores | Completa | Completo | Disponible |
| Mecanismos de integración | Completa | Completo | Disponible |
| Planes de mejora | Completa | Completo | Disponible |
| Proyectos | Completa | Completo | Disponible |
| Códigos de estructura organizacional | Completa | — | Fuera del sistema de IA (página de referencia) |

**8 módulos documentados** (cada uno con guía web, GuIA y skill).

Skills de producción (`calidad-ai-agents/`): `presentaciones-institucionales` (PPTX / HTML / PDF, con modo consolidar) y `diagramas-flujo` (PDF / PNG / JPG / SVG / BPMN) — funcionales; ver pendientes en [`docs/01-skills.md`](docs/01-skills.md).

Informes: `almera/informe-documentos/` e `almera/control-documentos-sgc/` — ver [`docs/02-informes.md`](docs/02-informes.md).

---

## 4. Roadmap

- **Reorganización a monorepo**: separar `almera-docs/` (documentación pura de Almera) de `calidad-ia-agents/` (skills transversales de Calidad, no atadas a un módulo), con un `index.html` en la raíz como landing único con el mismo diseño.
- Cerrar `presentaciones-institucionales` y `diagramas-flujo` con sus insumos de referencia pendientes.
- Ampliar cobertura más allá de Calidad, Evaluaciones, Indicadores y Proyectos — las categorías **General** y **Riesgos** del árbol de Admin de Almera todavía no tienen documentación propia.

---

## 5. Cómo probarlo

- **Producción**: [sgi.almeraim.com/sgi/?conid=sgicapitalsalud](https://sgi.almeraim.com/sgi/?conid=sgicapitalsalud)
- **Pruebas**: [sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas](https://sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas)
- **Skills**: se descargan desde la página de cada módulo (botón `Skill`) y se instalan directamente en Claude — sin configuración adicional.
