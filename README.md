# Almera Docs

Documentación operativa del sistema Almera (SGI), módulo por módulo, con una habilidad de inteligencia artificial asociada a cada uno.

## De qué va esto

Cuando alguien tiene una duda sobre cómo usar Almera, la opción de siempre es ponerse a buscar en un repositorio de grabaciones de capacitación: videos de una hora, de los cuales solo dos minutos responden la pregunta puntual que se tiene. Y casi nadie usa todos los módulos de Almera — un usuario de Evaluaciones probablemente nunca toca Mecanismos de Integración, pero igual tendría que revisar una grabación genérica para encontrar su respuesta.

Este proyecto reemplaza eso. Por cada módulo de Almera (Gestión documental, Evaluaciones, Indicadores, Mecanismos de integración, Planes de mejora) hay:

- Una **guía web** navegable (`index.html`), con procedimientos paso a paso, rutas exactas dentro del sistema y advertencias de cosas que suelen salir mal.
- Un **documento de referencia completo** (`.md`) construido a partir de documentación limpia, guías internas y la transcripción completa de las capacitaciones con soporte de Almera.
- Una **habilidad de IA instalable** (`.skill`), empaquetada para que Claude la cargue automáticamente cuando alguien pregunta por ese módulo — sin tener que adjuntar nada ni buscar nada manualmente.

El objetivo final: que alguien con una duda sobre un módulo específico se la resuelva un asistente en segundos, con el procedimiento exacto y la fuente de dónde salió, en vez de tener que rastrear una grabación vieja que probablemente ni siquiera recuerda dónde quedó guardada.

## Cómo está armado

Cada módulo sigue la misma estructura:

```
modulo/
├── index.html          # guía web, para leer en el navegador
└── AI/
    ├── modulo.md        # documento de referencia completo (para cualquier IA)
    └── almera-modulo.skill  # el mismo contenido empaquetado como Agent Skill de Claude
```

El `.md` de cada módulo sigue una misma plantilla, para que cualquier IA que lo lea sepa cómo comportarse:

1. **Instrucciones para la IA** — responder solo con lo documentado, avisar si algo no está cubierto, no inventar botones ni pasos.
2. **Árbol de navegación de Admin** — el mapa completo de todos los módulos de Almera, no solo el propio, para que la IA pueda ubicar cualquier opción que le pregunten aunque sea de otro módulo.
3. **Conceptos básicos, procedimientos paso a paso y preguntas frecuentes** — todo con la ruta exacta dentro del sistema.
4. **Temas pendientes de validar con soporte Almera** — las dudas que quedaron abiertas en la capacitación. Esto es clave: la IA avisa explícitamente cuando algo no está confirmado, en vez de presentarlo como un hecho.

## Estado actual de los módulos

| Módulo | Guía web | Documento `.md` | Habilidad `.skill` |
|---|---|---|---|
| Gestión documental | Completa | Completo | Disponible |
| Evaluaciones | Completa | Completo | Disponible |
| Indicadores | Completa | Completo | Disponible |
| Mecanismos de integración | Completa | Completo | Disponible |
| Planes de mejora | Completa | Completo | **Pendiente de empaquetar** |
| Códigos de estructura organizacional | Completa | — | Fuera del sistema de IA (página de referencia) |

## Cómo se construye cada módulo

1. Se parte de la grabación de la capacitación con soporte de Almera y de cualquier documentación limpia o guía interna que ya exista.
2. Se arma el `.md` de referencia: procedimientos, reglas del sistema, y una sección aparte para lo que quedó sin resolver en la capacitación (para no presentarlo como confirmado).
3. Se empaqueta ese contenido como `.skill` para Claude (el `.md` sirve igual para cualquier otro agente de IA que lo pueda leer).
4. Se construye la guía web (`index.html`) como versión curada y visual del mismo contenido, para quien prefiera leerlo directamente en el navegador.

## Lo que falta

- Empaquetar el `.skill` de Planes de mejora (el `.md` ya está listo).
- Ampliar la cobertura más allá de Calidad, Evaluaciones e Indicadores — las categorías General, Proyectos y Riesgos del árbol de Admin todavía no tienen documentación propia.


