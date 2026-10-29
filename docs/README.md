# SABIA — documentación de traspaso

Guía para el equipo que continúa el proyecto. Si es la primera vez que abres el repo, lee esto y luego los documentos en este orden. Para una foto rápida del estado actual, empieza por el **corte** (4):

| # | Documento | Qué cubre |
|---|---|---|
| 1 | [01-skills.md](01-skills.md) | Las skills: las 2 de entregables (presentaciones, diagramas de flujo) y las 8 de módulos de Almera. Cómo funcionan, cómo se empaquetan, cómo se mantienen. |
| 2 | [02-informes.md](02-informes.md) | Los dos informes (dashboards): Informe de documentos Almera e Informe de Control de documentos del SGC. |
| 3 | [03-almera.md](03-almera.md) | Documentación de los módulos de Almera: estructura, estado, cómo agregar un módulo nuevo, pendientes. |
| 4 | [04-corte-2026-10-28.md](04-corte-2026-10-28.md) | **Corte del proyecto:** qué tiene, para qué se hizo, arquitectura, stack, decisiones, asistente RAG + ETL, pendientes. |

Operación del asistente y del ETL: [`rag/README.md`](../rag/README.md). Rutas del sitio y menú: [`routes.md`](../routes.md).

## Qué es SABIA

Sistema de Automatización, Base de información e Inteligencia Artificial del área de Calidad (Capital Salud). Tiene tres partes:

1. **Base de conocimiento de Almera** — guías web + documentos de referencia por módulo.
2. **Automatización** — skills de Claude que generan entregables (presentaciones y diagramas de flujo) y dashboards que procesan los listados maestros.
3. **Agentes de IA** — cada módulo y cada automatización queda empaquetada como skill (`.skill`) instalable en Claude, más el asistente web **"Pregúntale a SABIA"** (`rag/`), que responde dudas de Almera sin cuenta de Claude.

El resumen ejecutivo y la arquitectura están en el [README raíz](../README.md).

## Mapa del repositorio

```
almera-docs/
├── index.html                  Landing de SABIA (enlaza a Almera, Agentes de IA y el asistente)
├── README.md                   Resumen ejecutivo + arquitectura (desactualizado: no incluye rag/)
├── routes.md                   Rutas del sitio y menú compartido (nav.js)
├── to-do                       Backlog informal del proyecto (leerlo)
├── rag/                        Servidor SABIA: sitio + asistente RAG-lite + ETL de la carpeta compartida
├── docs/                       ← esta documentación
├── almera/                     Familia 01 · Documentación de Almera
│   ├── index.html              Landing de módulos
│   ├── modulo-documentos/      gestion-documentos, mapa-procesos, mecanismos-integracion, modelos-gestion
│   ├── modulo-evaluaciones/    evaluaciones, indicadores, planes-de-mejora
│   ├── modulo-proyectos/
│   ├── informe-documentos/     Dashboard del export de Almera
│   ├── control-documentos-sgc/ Dashboard del listado maestro SGC (carpeta compartida)
│   ├── codigos-estructura-organizacional/   Página de referencia (sin skill)
│   ├── almera-IA/              Guía de cómo instalar y usar las skills en Claude
│   ├── assets/                 Estilos, íconos y almera-structure.md (árbol de Admin)
│   └── design/                 Mockups de Claude Design
└── calidad-ai-agents/          Familia 02 · Agentes de IA / entregables
    ├── index.html, entregables/index.html   Páginas web de las skills
    ├── presentaciones-institucionales/      Skill (fuentes + .skill)
    ├── diagramas-flujo/                     Skill (fuentes DESACTUALIZADAS + .skill vigente — ver 01-skills.md §3.4)
    └── SEGURIDAD.md            Guía de uso con datos reales
```

## Lo primero que debes saber (riesgos del traspaso)

1. **El `.skill` de diagramas de flujo es la única copia completa de esa skill.** El generador (`scripts/generar_diagrama.py`), las referencias 06 y 07 y los specs de regresión existen solo dentro de `diagramas-flujo.skill`; la carpeta suelta del repo quedó con la versión anterior (basada en Mermaid). Antes de tocar nada, extrae el `.skill` sobre esa carpeta. Detalle en [01-skills.md §3.4](01-skills.md).
2. **Cada módulo de Almera vive en tres copias** (guía web `index.html`, GuIA `.md`, `.skill`) que se sincronizan a mano. No hay build ni script que las regenere. Si corriges un dato en una, corrígelo en las tres.
3. **El sitio no tiene build y es estático; el único backend es `rag/`.** El sitio funciona con cualquier servidor de archivos. Los dashboards procesan el Excel en el navegador y nada se sube. El asistente necesita el servidor de `rag/` (Python/FastAPI), que guarda la llave de OpenRouter en `rag/.env` (nunca se sube a Git).
4. **Las skills de entregables no tienen GuIA `.md`**: necesitan ejecutar código y plantillas, así que solo funcionan en Claude.
5. **Datos sensibles:** antes de usar las skills con información real (afiliados, salud), lee `calidad-ai-agents/SEGURIDAD.md`. Resumen en [01-skills.md §5](01-skills.md).

## Qué está pendiente (resumen; el detalle está en cada documento)

- Almera: verificar módulo Proyectos y Mecanismos de integración con pruebas y correos; documentar las categorías General y Riesgos; meter el árbol de Admin en la skill general ([03-almera.md §6](03-almera.md)).
- Presentaciones: probar PDF desde HTML, ajustar tamaño de personajes en PPTX ([01-skills.md §2.4](01-skills.md)).
- Asistente: publicarlo en el servidor del área con TI, agregar autenticación y validar respuestas con usuarios reales ([04-corte §9](04-corte-2026-10-28.md)).
- Ideas a futuro anotadas en `to-do`: skills para ChatGPT Pro, CLI con modelo local (LM Studio), RAG para la DEP con Ollama.

## Enlaces útiles

- Almera producción: <https://sgi.almeraim.com/sgi/?conid=sgicapitalsalud>
- Almera pruebas: <https://sgi.almeraim.com/sgi/?conid=sgicapitalsaludpruebas>
- Instalar skills en Claude: `Claude → Configuración → Habilidades → Subir habilidad` (capturas en `almera/almera-IA/index.html`).
