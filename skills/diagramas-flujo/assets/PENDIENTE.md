# Insumos pendientes — diagramas de flujo

La skill no está completa hasta que estos archivos estén en esta carpeta `assets/`.

## Obligatorios

| Archivo | Qué es | Estado |
|---|---|---|
| `paleta-bizagi.md` | Colores por tipo de elemento del estándar de Bizagi. | 🟡 Provisional (valores por defecto; falta confirmar contra export real) |
| `plantilla.mmd` | Esqueleto Mermaid con `classDef` calibrado a la paleta. | 🟡 Provisional (depende de `paleta-bizagi.md`) |
| `diagrama-referencia-ejemplo/` | Ejemplo trabajado (PQRS) como referencia temporal. | 🟢 Listo (provisional) |
| `diagrama-referencia.pdf` (o `.png`) | Export **real** de un procedimiento ya diagramado en Bizagi Modeler. | ⬜ Falta — lo tienes que subir tú |

## Opcional pero útil

| Archivo | Qué es |
|---|---|
| `diagrama-referencia.bpm` | El archivo Bizagi original, para leer colores/estilos exactos. |

## Formato sugerido para `paleta-bizagi.md`

```markdown
# Paleta Bizagi Modeler — repositorio de procedimientos

| Elemento | Relleno (hex) | Borde (hex) | Texto (hex) |
|---|---|---|---|
| Evento inicial | #xxxxxx | #xxxxxx | #xxxxxx |
| Evento final | #xxxxxx | #xxxxxx | #xxxxxx |
| Actividad | #xxxxxx | #xxxxxx | #xxxxxx |
| Decisión (compuerta) | #xxxxxx | #xxxxxx | #xxxxxx |
| Subproceso | #xxxxxx | #xxxxxx | #xxxxxx |
| Carril (lane) — encabezado | #xxxxxx | #xxxxxx | #xxxxxx |
| Fase — banda | #xxxxxx | #xxxxxx | #xxxxxx |

## Marcas de validación (independientes del relleno)
| Estado | Color |
|---|---|
| Verde | #xxxxxx |
| Amarillo | #xxxxxx |
| Rojo | #xxxxxx |
```

## Decisión de entorno pendiente

- [ ] ¿Dónde corre la skill? (Claude web / app, vs. Claude Code en Windows)
- [ ] Si es Windows local: instalar `@mermaid-js/mermaid-cli` y un conversor a JPG.
