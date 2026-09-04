# Paleta Bizagi Modeler — repositorio de procedimientos

> **Calibrada contra dos exports reales que NO coinciden en inicio/fin.** Actividad y decisión se
> obtuvieron por muestreo de píxeles directo sobre `ejemplos-reales/diagrama-de-flujo-bizaggi.png`
> ("Retiro parcial de cesantías") — ese muestreo se mantiene y es de alta confianza (±2-3 por
> canal). Pero un segundo export real, del procedimiento de "Inducción a nuevos funcionarios"
> (compartido como imagen en el chat, sin archivo para muestrear píxeles), usa un evento inicial
> verde saturado y un evento final rojo saturado — nada parecido al verde-lima y rosa-rojo pálidos
> del primer export. **Conclusión: Bizagi Modeler no fuerza un color único de inicio/fin a nivel
> organización — varía por diagrama o por quién lo dibujó.** La tabla de abajo usa como *default*
> los valores del segundo export (más reciente, y visualmente el más "estándar"/reconocible), pero
> quedan como **estimación visual** (no muestreo de píxeles — no hay archivo de esa imagen para
> samplear) y con el primer export documentado como variante alterna real. Si vas a diagramar un
> procedimiento con su propio export de Bizagi disponible, usa los colores de *ese* export, no los
> de esta tabla. Subproceso, evento intermedio, carril y banda de fase siguen sin confirmar contra
> ningún export real. Ver `PENDIENTE.md`.

## Colores por tipo de elemento

| Elemento | Relleno | Borde | Texto | Nota |
|---|---|---|---|---|
| Evento inicial | `#92D050` (aprox., a ojo) | `#548235` (aprox.) | `#26401A` (aprox.) | Círculo verde saturado — export "Inducción". Variante real alterna, más pálida: fill `#E8FFA6` / borde `#A0B16A` / texto `#4B5A2E` (export "Cesantías", muestreado por píxel) |
| Evento intermedio | `#FDE9D9` | `#E67E22` | `#6E3B10` | ⬜ Sin confirmar — no aparece en ningún export real visto hasta ahora |
| Evento final | `#C00000` (aprox., a ojo) | `#7F0000` (aprox.) | `#FFFFFF` (aprox.) | Círculo rojo saturado — export "Inducción". Variante real alterna, más pálida: fill `#E9B2AC` / borde `#9E4650` (export "Cesantías", muestreado por píxel) |
| Actividad / tarea | `#EAF0FC` | `#6F90AA` | negro/gris muy oscuro (sin confirmar exacto) | Rectángulo redondeado, azul-lavanda muy pálido |
| Subproceso | `#E1D5E7` | `#9673A6` | `#3D2C47` | ⬜ Sin confirmar — no aparece en el export real |
| Compuerta (decisión) | `#FFFFCE` | `#AEB578` | oliva oscuro (sin confirmar exacto) | Rombo amarillo pálido, borde oliva |
| Carril (*lane*) — encabezado | `#F5F5F5` | `#666666` | `#333333` | ⬜ Sin confirmar — el export recorta el encabezado del carril; solo se ve el divisor |
| Divisor de carril (línea) | — | `#A6A6A6` (aprox.) | — | Confirmado: línea gris fina horizontal entre carriles, sin relleno |
| Fase — banda | `#FAFAFA` | `#999999` | `#333333` | ⬜ Sin confirmar — no aparece en el export real |
| Flujo de secuencia | — | `#4D4D4D` | — | Línea sólida con punta |
| Flujo de mensaje | — | `#4D4D4D` (guiones) | — | Línea punteada |
| Objeto de datos / formato asociado | `#F5F5F5` (aprox.) | gris, borde punteado | — | Caja rectangular con esquina doblada, conectada por línea punteada (ver "Formato de Retiro Parcial de Cesantías" en el export) |
| Conector / evento de enlace numerado | `#F9F9F9` | `#909090` | `#404040` (aprox.) | Confirmado por muestreo de píxel (export "Cesantías", círculo pequeño numerado "1", debajo de INICIO). El PDF de ejemplo lo describe como "conector numerado para el retorno de subsanación": en vez de una flecha larga cruzando el diagrama, se usan dos círculos con el mismo número — uno donde el flujo sale, otro donde vuelve a entrar. Útil también para cruces de carril (ver `pruebas/induccion-nuevos-funcionarios/`). |

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
classDef evInicio    fill:#92D050,stroke:#548235,stroke-width:2px,color:#26401A;
classDef evIntermedio fill:#FDE9D9,stroke:#E67E22,stroke-width:2px,color:#6E3B10;
classDef evFin       fill:#C00000,stroke:#7F0000,stroke-width:2px,color:#FFFFFF;
classDef actividad   fill:#EAF0FC,stroke:#6F90AA,stroke-width:1.5px,color:#1A2E4A;
classDef subproceso  fill:#E1D5E7,stroke:#9673A6,stroke-width:1.5px,color:#3D2C47;
classDef decision    fill:#FFFFCE,stroke:#AEB578,stroke-width:1.5px,color:#5B5A2E;
classDef conector    fill:#F9F9F9,stroke:#909090,stroke-width:1.5px,color:#404040;

%% Variante real alterna de evInicio/evFin (export "Cesantías", muestreada por píxel):
%% classDef evInicio fill:#E8FFA6,stroke:#A0B16A,stroke-width:2px,color:#4B5A2E;
%% classDef evFin    fill:#E9B2AC,stroke:#9E4650,stroke-width:2px,color:#5A2226;
```

`evIntermedio` y `subproceso` siguen con los valores provisionales de antes — no aparecían en
ningún export real visto hasta ahora, así que no había nada que calibrar todavía.
