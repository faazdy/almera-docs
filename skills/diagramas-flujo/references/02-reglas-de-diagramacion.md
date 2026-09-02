# Reglas de diagramación

## Límite de 100 caracteres (regla del encargo)

- Toda **actividad** o **acción** ≤ **100 caracteres**, contando espacios.
- Si no cabe: partir en dos pasos, o reescribir más directo. Nunca abreviar con siglas no
  estándar ni recortar hasta que quede ambiguo.
- Redacción: **verbo en infinitivo + objeto**. "Registrar la solicitud en el sistema", no
  "Registro de solicitud" ni "El analista registra la solicitud que llega...".
- Las **decisiones** se escriben como pregunta cerrada: "¿La solicitud está completa?".
- Las **etiquetas de las salidas** de una decisión: cortas ("Sí" / "No", o la opción real).

## Nomenclatura

| Elemento | Cómo se nombra |
|---|---|
| Evento inicial | Sustantivo del disparador: "Solicitud recibida". |
| Actividad | Verbo infinitivo + objeto. ≤ 100 car. |
| Decisión (compuerta) | Pregunta cerrada terminada en "?". |
| Subproceso | Nombre del procedimiento referenciado. |
| Evento final | Resultado alcanzado: "Solicitud archivada". |

## Tipos de nodo (equivalencia BPMN / Bizagi)

- **Evento** (círculo): inicio, fin, y esperas/temporizadores si aplica.
- **Actividad** (rectángulo redondeado): un paso de trabajo.
- **Decisión** (rombo): bifurcación exclusiva. Toda rama debe reconectarse o terminar en un fin.
- **Subproceso** (rectángulo con marca +): paso que es en sí otro procedimiento.
- **Carril** (*lane*): responsable/rol. La actividad vive en el carril de quien la ejecuta.
- **Fase**: banda que agrupa varias actividades por etapa.

## Layout

- Dirección principal: izquierda → derecha.
- Sin cruces de líneas cuando se pueda evitar; usar ruteo ortogonal.
- Una sola entrada y una sola salida por actividad (las múltiples salidas van por decisión).
- Todas las ramas de una decisión terminan (en un fin o reconectando al flujo). No dejar ramas
  colgando.

## Paleta

- Colores por tipo de elemento según `assets/paleta-bizagi.md`.
- El color de relleno indica **tipo de elemento**, no estado. El estado (verde/amarillo/rojo) va
  como **comentario/marca de validación**, no como relleno del nodo — ver `03-validacion-por-colores.md`.

## Herramienta de dibujo

- Mermaid (`flowchart`) como fuente del diagrama, con `classDef` para aplicar la paleta.
- Alternativa: draw.io/diagrams.net con la librería BPMN.
- La fuente (texto Mermaid o `.drawio`) se guarda junto al export para poder editar después.
