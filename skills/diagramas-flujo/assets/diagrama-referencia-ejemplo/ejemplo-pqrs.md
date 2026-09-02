# Ejemplo de referencia — Atención de PQRS (General)

Diagrama de muestra que aplica todas las reglas de la skill. Sirve como referencia **provisional**
hasta tener un export real de Bizagi Modeler. Fuente: [`ejemplo-pqrs.mmd`](./ejemplo-pqrs.mmd).

## Estructura consultada al usuario

- **Inicio:** PQRS recibida. **Fin:** PQRS atendida y cerrada.
- **Fases:** Recepción → Análisis → Respuesta → Cierre.
- **Responsables (carriles):** Ciudadano, Ventanilla única, Analista del proceso, Líder de proceso.
- **Variaciones:** ninguna en este ejemplo (si las hubiera → un diagrama general + uno por variación,
  ver `../../references/04-variaciones-de-procedimiento.md`).

## Diagrama

```mermaid
---
title: Atención de PQRS — General
---
flowchart LR

  ini(["PQRS recibida"]):::evInicio

  subgraph L1["Ciudadano"]
    direction TB
    A1["Radicar la PQRS por el canal disponible: web, correo, presencial o telefónico"]:::actividad
    A2["Completar y reenviar la información solicitada"]:::actividad
  end

  subgraph L2["Ventanilla única"]
    direction TB
    B1["Registrar la PQRS en el sistema y asignar número de radicado"]:::actividad
    D1{"¿La PQRS tiene toda la información requerida?"}:::decision
    B2["🔴 Solicitar al ciudadano la información faltante"]:::actividad
    B3["Clasificar la PQRS por tipo y asignarla al proceso responsable"]:::actividad
    B4["🟡 Enviar la respuesta al ciudadano por el canal registrado"]:::actividad
    B5["Cerrar el radicado y notificar el cierre al ciudadano"]:::actividad
  end

  subgraph L3["Analista del proceso"]
    direction TB
    C1["Revisar la PQRS y determinar las áreas o personas a consultar"]:::actividad
    C2["Recopilar la información y preparar el proyecto de respuesta"]:::actividad
    C3["Ajustar el proyecto de respuesta según las observaciones"]:::actividad
    C4["Registrar la respuesta y los soportes en el expediente de la PQRS"]:::actividad
  end

  subgraph L4["Líder de proceso"]
    direction TB
    D2{"¿El proyecto de respuesta es adecuado?"}:::decision
    E1["Aprobar la respuesta definitiva"]:::actividad
  end

  fin(["PQRS atendida y cerrada"]):::evFin

  ini --> A1 --> B1 --> D1
  D1 -- "No" --> B2 --> A2 --> D1
  D1 -- "Sí" --> B3 --> C1 --> C2 --> D2
  D2 -- "No" --> C3 --> D2
  D2 -- "Sí" --> E1 --> B4 --> C4 --> B5 --> fin

  classDef evInicio    fill:#D5E8D4,stroke:#2E7D32,stroke-width:2px,color:#1B4332;
  classDef evFin       fill:#F8CECC,stroke:#C0392B,stroke-width:2px,color:#641E16;
  classDef actividad   fill:#EAF2FB,stroke:#3C78D8,stroke-width:1.5px,color:#1A2E4A;
  classDef decision    fill:#FFF2CC,stroke:#D6B656,stroke-width:1.5px,color:#5B4A16;
  classDef subproceso  fill:#E1D5E7,stroke:#9673A6,stroke-width:1.5px,color:#3D2C47;
```

## Pasos

| # | Fase | Responsable | Paso | Tipo | Caracteres |
|---|---|---|---|---|---|
| 1 | Recepción | Ciudadano | Radicar la PQRS por el canal disponible: web, correo, presencial o telefónico | Actividad | 76 |
| 2 | Recepción | Ventanilla única | Registrar la PQRS en el sistema y asignar número de radicado | Actividad | 59 |
| 3 | Recepción | Ventanilla única | ¿La PQRS tiene toda la información requerida? | Decisión | — |
| 4 | Recepción | Ventanilla única | Solicitar al ciudadano la información faltante | Actividad | 45 |
| 5 | Recepción | Ciudadano | Completar y reenviar la información solicitada | Actividad | 45 |
| 6 | Recepción | Ventanilla única | Clasificar la PQRS por tipo y asignarla al proceso responsable | Actividad | 61 |
| 7 | Análisis | Analista del proceso | Revisar la PQRS y determinar las áreas o personas a consultar | Actividad | 60 |
| 8 | Análisis | Analista del proceso | Recopilar la información y preparar el proyecto de respuesta | Actividad | 58 |
| 9 | Análisis | Líder de proceso | ¿El proyecto de respuesta es adecuado? | Decisión | — |
| 10 | Análisis | Analista del proceso | Ajustar el proyecto de respuesta según las observaciones | Actividad | 55 |
| 11 | Respuesta | Líder de proceso | Aprobar la respuesta definitiva | Actividad | 31 |
| 12 | Respuesta | Ventanilla única | Enviar la respuesta al ciudadano por el canal registrado | Actividad | 55 |
| 13 | Cierre | Analista del proceso | Registrar la respuesta y los soportes en el expediente de la PQRS | Actividad | 64 |
| 14 | Cierre | Ventanilla única | Cerrar el radicado y notificar el cierre al ciudadano | Actividad | 52 |

Todas las actividades ≤ 100 caracteres. ✅

## Tabla de validación

| # | Paso | Color | Comentario |
|---|---|---|---|
| 3 | ¿La PQRS tiene toda la información requerida? | 🟡 | No está definida la lista de campos obligatorios que hacen que una PQRS se considere "completa". |
| 4 | Solicitar al ciudadano la información faltante | 🔴 | No hay plazo ni número máximo de solicitudes; la PQRS puede quedar abierta indefinidamente sin respuesta del ciudadano. |
| 12 | Enviar la respuesta al ciudadano por el canal registrado | 🟡 | No se define el plazo máximo legal de respuesta ni qué ocurre si se vence. |
| Resto | — | 🟢 | Sin observaciones. |

**Leyenda:** 🟢 todo correcto · 🟡 parcialmente correcto, requiere revisar · 🔴 revisar obligatoriamente.

## Notas sobre este ejemplo

- Los carriles se representan con `subgraph`. Mermaid no permite anidar carriles y fases de forma
  legible, por eso la **fase** vive en la tabla de pasos, no en el lienzo.
- Las marcas 🟡 / 🔴 van como prefijo en la etiqueta del nodo; 🟢 no se marca. El detalle siempre
  en la tabla de validación.
- Sin paréntesis dentro de las etiquetas (rompen el parser de Mermaid); se usan dos puntos.
