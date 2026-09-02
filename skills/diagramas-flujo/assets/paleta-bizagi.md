# Paleta Bizagi Modeler — repositorio de procedimientos

> **PROVISIONAL.** Estos valores son una aproximación al tema por defecto de Bizagi Modeler.
> Hay que confirmarlos contra un export real de un procedimiento del repositorio
> (ver `diagrama-referencia-ejemplo/README.md` y `PENDIENTE.md`). Cuando llegue el export,
> se corrigen los hex de esta tabla y los `classDef` de `../plantilla.mmd` y del ejemplo.

## Colores por tipo de elemento

| Elemento | Relleno | Borde | Texto | Nota |
|---|---|---|---|---|
| Evento inicial | `#D5E8D4` | `#2E7D32` | `#1B4332` | Círculo, borde fino |
| Evento intermedio | `#FDE9D9` | `#E67E22` | `#6E3B10` | Doble círculo |
| Evento final | `#F8CECC` | `#C0392B` | `#641E16` | Círculo, borde grueso |
| Actividad / tarea | `#EAF2FB` | `#3C78D8` | `#1A2E4A` | Rectángulo redondeado |
| Subproceso | `#E1D5E7` | `#9673A6` | `#3D2C47` | Rectángulo con marca `+` |
| Compuerta (decisión) | `#FFF2CC` | `#D6B656` | `#5B4A16` | Rombo |
| Carril (*lane*) — encabezado | `#F5F5F5` | `#666666` | `#333333` | Franja del responsable |
| Fase — banda | `#FAFAFA` | `#999999` | `#333333` | Agrupador de etapa |
| Flujo de secuencia | — | `#4D4D4D` | — | Línea sólida con punta |
| Flujo de mensaje | — | `#4D4D4D` (guiones) | — | Línea punteada |

## Colores de validación (independientes del relleno)

Se aplican como **marca/borde o ícono**, nunca como relleno del nodo (el relleno indica el tipo).
Ver `../references/03-validacion-por-colores.md`.

| Estado | Color | Uso |
|---|---|---|
| 🟢 Verde | `#2E7D32` | Todo correcto |
| 🟡 Amarillo | `#F2C037` | Parcialmente correcto, requiere revisar |
| 🔴 Rojo | `#C0392B` | Revisar obligatoriamente |

## Equivalencia a `classDef` de Mermaid

```
classDef evInicio   fill:#D5E8D4,stroke:#2E7D32,stroke-width:2px,color:#1B4332;
classDef evIntermedio fill:#FDE9D9,stroke:#E67E22,stroke-width:2px,color:#6E3B10;
classDef evFin      fill:#F8CECC,stroke:#C0392B,stroke-width:2px,color:#641E16;
classDef actividad  fill:#EAF2FB,stroke:#3C78D8,stroke-width:1.5px,color:#1A2E4A;
classDef subproceso fill:#E1D5E7,stroke:#9673A6,stroke-width:1.5px,color:#3D2C47;
classDef decision   fill:#FFF2CC,stroke:#D6B656,stroke-width:1.5px,color:#5B4A16;
```
