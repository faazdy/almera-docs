# Skills

Habilidades de IA (Agent Skills de Claude) de este proyecto que **no** corresponden a un módulo de Almera.

Los módulos de Almera (Gestión documental, Evaluaciones, Indicadores, etc.) tienen su skill de conocimiento dentro de su propia carpeta `modulo-*/.../AI/`. Esta carpeta es para skills **de producción**: las que generan un entregable (una presentación, un diagrama) siguiendo lineamientos institucionales.

## Skills en esta carpeta

| Carpeta | Qué hace | Estado |
|---|---|---|
| `presentaciones-institucionales/` | Genera presentaciones (PPTX / HTML / PDF) respetando plantilla y paleta institucional. | En construcción — faltan insumos de referencia |
| `diagramas-flujo/` | Genera diagramas de flujo de procedimientos (PDF / JPG / PNG), consistentes con los diagramados en Bizagi Modeler, con validación por colores. | En construcción — faltan insumos de referencia |

## Estructura de cada skill

Igual que las skills de módulo: se empaqueta como `.skill` (zip) para instalar en Claude.

```
<skill>/
├── SKILL.md          # instrucciones + flujo de trabajo (lo que Claude carga primero)
├── references/        # reglas detalladas, se leen bajo demanda
└── assets/            # plantillas y archivos de referencia obligatorios
```

## Entorno de ejecución (supuesto)

Estas skills asumen que corren en el entorno de ejecución de código de Claude (sandbox Linux con Python disponible: `python-pptx`, LibreOffice para conversión a PDF, y un renderizador de diagramas). Si se van a correr en Claude Code sobre Windows local, hay que resolver primero el toolchain (ver `assets/PENDIENTE.md` de cada skill).
