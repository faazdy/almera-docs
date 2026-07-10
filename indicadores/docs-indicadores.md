# Indicadores

**Sistema:** Almera

Cómo personalizar la ficha técnica de un indicador, configurar unidades de medida, definir metas con semaforización dinámica y administrar quién puede medir y consultar un indicador.

---

## Índice

1. [Creación de campos adicionales en la ficha técnica](#1-creación-de-campos-adicionales-en-la-ficha-técnica)
2. [Actualización de opciones en campos existentes](#2-actualización-de-opciones-en-campos-existentes-ítems)
3. [Configuración de unidades de medida](#3-configuración-de-unidades-de-medida)
4. [Gestión de metas y semaforización](#4-gestión-de-metas-y-semaforización)
5. [Asignación de privilegios y responsables](#5-asignación-de-privilegios-y-responsables)
6. [Control de fechas del indicador](#6-control-de-fechas-del-indicador)

---

## Reunión de capacitación

Para conocer el funcionamiento completo del módulo, consulte la grabación de la reunión de capacitación.

> **Enlace:** *(pendiente de agregar)*

---

# 1. Creación de campos adicionales en la ficha técnica

Permite personalizar la información que se solicita al crear un indicador, por ejemplo agregando nuevas categorías o datos propios de la organización.

## Ruta

`Admin → Indicadores → Categorías y tipos de indicador`

## Pasos

1. Ingrese al componente **Indicador**.
2. Abra la pestaña **Campos adicionales**.
3. Seleccione **Nuevo campo**.
4. Configure el nuevo campo:
   - Seleccione el **tipo de campo** (texto, selección múltiple, etc.).
   - Asigne un **código o consecutivo**, respetando el orden existente.
   - Defina el **nombre** del campo.
   - Seleccione el **agrupador**. Si desea que aparezca en la primera pestaña de la ficha técnica, elija **Definición**.
5. Indique si el campo será obligatorio.
6. Pulse **Grabar**.

---

# 2. Actualización de opciones en campos existentes (ítems)

Permite agregar nuevas opciones a campos de selección existentes.

Ejemplo: añadir la opción **Indicador de gestión** a un campo llamado **Clase**.

## Pasos

1. Desde **Campos adicionales**, ubique el campo que desea modificar.
2. Abra el campo haciendo clic sobre su nombre.
3. Seleccione **Nuevo ítem**.
4. Complete la información:
   - Orden
   - Código
   - Nombre

### Ejemplo

| Campo | Valor |
|--------|-------|
| Nombre | Indicador de gestión |

5. Si corresponde, asigne un **peso** para que el sistema calcule automáticamente una calificación.

### Ejemplo de pesos

| Opción | Peso |
|---------|-----:|
| Cumple | 1 |
| No cumple | 0 |

6. Guarde el nuevo ítem.

---

# 3. Configuración de unidades de medida

Permite definir cómo se visualizarán los valores del indicador.

Ejemplos:

- Porcentaje
- Pesos colombianos
- Tasas
- Cantidades
- Horas

## Ruta

`Admin → Indicadores → Unidades y categorías`

## Pasos

1. Seleccione **Adicionar unidad**.
2. Asigne el nombre de la unidad.
3. Configure el formato utilizando la variable `{valor}`.

### Ejemplo 1

| Campo | Valor |
|--------|-------|
| Nombre | Tasa |
| Formato | `{valor} TZ` |

### Ejemplo 2

| Campo | Valor |
|--------|-------|
| Nombre | COP |
| Formato | `$ {valor}` |

4. Defina la cantidad de decimales.
5. Pulse **Grabar**.

---

# 4. Gestión de metas y semaforización

La configuración correcta de las metas permite conservar el histórico de mediciones cuando estas cambian con el tiempo.

> **Recomendación**
>
> Utilice siempre **Meta periódica** junto con **Semáforo dinámico**.

## Pasos

1. En la ficha técnica seleccione el tipo de meta **Periódica**.
2. Pulse **Definir metas**.
3. Registre la meta correspondiente para cada período (enero, febrero, marzo, etc.).
4. Configure los rangos del semáforo.

### Estados del semáforo

| Estado | Significado |
|---------|-------------|
| 🔴 Rojo | Bajo cumplimiento |
| 🟡 Amarillo | Cumplimiento parcial |
| 🟢 Verde | Meta cumplida |

> **Importante**
>
> Cuando la meta cambia durante el año (por ejemplo, de 90 % a 95 %), el sistema conserva el histórico de las mediciones anteriores y evita recalcular los períodos ya registrados.

---

# 5. Asignación de privilegios y responsables

Es importante diferenciar entre el responsable del indicador y los usuarios con permisos específicos.

## Responsables por cargo

Definen qué cargo es responsable del indicador.

No hacen referencia a una persona específica.

## Privilegios de usuarios

Permiten asignar permisos a usuarios concretos para trabajar sobre un indicador.

## Pasos

1. Dentro del indicador vaya a:

   `Editar → Privilegios → Administrar`

2. Busque el usuario y asígnele las acciones correspondientes.

Las acciones disponibles son:

- Consultar
- Agregar medición
- Hacer análisis

3. Pulse **Agregar** para guardar la asignación.

---

# 6. Control de fechas del indicador

Las fechas determinan el período durante el cual el indicador acepta mediciones.

## Pasos

1. Configure la **Fecha válido**, que corresponde al inicio de la vigencia del indicador.
2. Configure la **Fecha de corte**, que define el fin de su vigencia.
3. Si el indicador puede tener períodos sin información, habilite la opción:

   **Permitir períodos sin medición**

   Esto hará que el sistema muestre dichos períodos con valor cero.

> **Advertencia**
>
> Al llegar la fecha de corte, el sistema bloquea automáticamente el indicador y ya no será posible registrar nuevas mediciones.

---

# Resumen de rutas

| Funcionalidad | Ruta |
|---------------|------|
| Campos adicionales | `Admin → Indicadores → Categorías y tipos de indicador` |
| Unidades de medida | `Admin → Indicadores → Unidades y categorías` |
| Privilegios | `Indicador → Editar → Privilegios` |

---

# Buenas prácticas

- Mantenga un orden consecutivo en los códigos de los campos adicionales.
- Utilice nombres descriptivos para campos y opciones.
- Configure las metas como **Periódicas** para preservar el histórico.
- Utilice **Semáforo dinámico** para evaluar el cumplimiento.
- Defina correctamente la unidad de medida antes de comenzar a registrar mediciones.
- Asigne privilegios únicamente a los usuarios que realmente participarán en la medición o el análisis.
- Configure adecuadamente la fecha de corte para evitar bloqueos inesperados del indicador.

---

# Notas importantes

- Los cambios en las metas no modifican las mediciones históricas cuando se utiliza **Meta periódica**.
- Los pesos en listas de selección permiten calcular resultados automáticamente.
- Las unidades de medida utilizan la variable `{valor}` para mostrar el resultado con el formato definido.
- Después de la fecha de corte no será posible registrar nuevas mediciones.