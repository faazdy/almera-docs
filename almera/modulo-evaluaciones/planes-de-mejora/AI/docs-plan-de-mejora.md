# Planes de mejora

**Sistema:** Almera

Guía para registrar informes de evaluación y sus hallazgos en Almera, así como configurar evaluadores, sistemas de referencia, campos personalizados y demás parámetros relacionados con el módulo de Planes de Mejora.

---

# Índice

1. [Crear un informe de evaluación](#1-crear-un-informe-de-evaluación)
2. [Crear un hallazgo](#2-crear-un-hallazgo-para-el-informe)

## Configuración avanzada

A.1. [Adicionar evaluadores](#a1-adicionar-nuevos-evaluadores)

A.2. [Configurar sistemas de referencia](#a2-adicionar-o-ajustar-un-sistema-de-referencia)

A.3. [Configurar puntos de atención](#a3-adicionar-o-ajustar-puntos-de-atención)

---

# Reunión de capacitación

Para conocer el funcionamiento completo del módulo consulte la grabación de la reunión de capacitación.

> **Enlace:** *(Agregar URL de la grabación aquí.)*

---

# 1. Crear un informe de evaluación

El informe es el contenedor principal de una evaluación. Una vez creado, permitirá registrar los hallazgos asociados.

## Ruta

`Admin → Evaluaciones → Administrar planes`

## Pasos

1. Seleccione **Nuevo informe**.
2. Complete el formulario.

### Campos obligatorios

- Nombre
- Evaluador
- Sistema de referencia
- Descripción
- Fecha

> **Si el evaluador no aparece**, consulte la sección **A.1 Adicionar nuevos evaluadores**.

> **Si necesita crear un sistema de referencia**, consulte la sección **A.2 Adicionar o ajustar un sistema de referencia**.

3. Presione **Grabar**.

> **Importante**
>
> El rango de fechas definido en el informe determina qué hallazgos serán consolidados automáticamente dentro de ese informe.

---

# 2. Crear un hallazgo para el informe

Los hallazgos únicamente pueden registrarse sobre informes previamente creados y guardados.

## Pasos

1. Abra el informe correspondiente.
2. Seleccione **Adicionar**.
3. Complete la información del hallazgo.

### Campos principales

- Código
- Clasificación
- Nombre
- Descripción

4. Adjunte archivos de soporte si es necesario.
5. Busque y seleccione la **Unidad Auditable** correspondiente.

> **Obligatorio**
>
> Todo hallazgo debe estar asociado a una Unidad Auditable.

## Observaciones

- La **Clasificación** del hallazgo es completamente parametrizable desde la configuración del sistema.

---

# Configuración avanzada

Las siguientes opciones corresponden a tareas de parametrización del sistema y normalmente son realizadas por administradores.

---

# A.1 Adicionar nuevos evaluadores

Utilice esta opción cuando el evaluador requerido no aparezca disponible al crear un informe.

## Ruta

`Admin → Evaluaciones → Parámetros generales evaluación`

## Pasos

1. Seleccione **Crear emisor**.
2. Complete la información requerida.
3. Presione **Grabar**.

---

# A.2 Adicionar o ajustar un sistema de referencia

Utilice esta opción para crear nuevas normas, metodologías o sistemas de referencia utilizados durante las evaluaciones.

## Ruta

`Admin → Evaluaciones → Sistema de referencia`

## Pasos

1. Seleccione **Adicionar sistema de referencia**.
2. Complete la información.
3. Presione **Grabar**.

> **Nota**
>
> Un sistema de referencia que ya tenga hallazgos asociados no podrá eliminarse.

---

## Configurar transiciones

Las transiciones determinan a qué usuario o cargo se enviará un hallazgo durante el flujo de trabajo.

### Pasos

1. Abra el sistema de referencia.
2. Ingrese a la pestaña **Privilegios**.
3. Localice la sección **Transiciones**.
4. Asigne las acciones correspondientes.

Ejemplos de acciones:

- Enviar
- Devolver
- Aprobar

Es posible asignar múltiples responsables para una misma transición.

---

## Configurar niveles de respuesta

Los niveles de respuesta permiten clasificar el resultado de una auditoría.

## Pasos

1. Abra la pestaña **Niveles de respuesta**.
2. Seleccione **Nuevo nivel de respuesta**.
3. Configure:

- Código
- Nombre
- Peso
- Color

### Generar punto de atención

Si activa la opción **Genera punto de atención**, el sistema creará automáticamente un hallazgo cuando se seleccione dicho nivel.

Ejemplo:

- No cumple

---

## Crear campos personalizados

Permite agregar información adicional durante el registro de un hallazgo.

### Pasos

1. Abra la pestaña **Grupos**.
2. Seleccione **Nuevo agrupador**.
3. Configure:

- Nombre
- Ubicación
- Mostrar nombre (opcional)

4. Cree un **Nuevo campo adicional**.
5. Configure:

- Nombre
- Tipo de campo
- Selección múltiple
- Texto
- Número
- Fecha
- Etc.

---

# A.3 Adicionar o ajustar puntos de atención

Permite administrar las clasificaciones automáticas utilizadas por el sistema.

## Ruta

`Admin → Evaluaciones → Parametrización de puntos de atención`

## Crear una clasificación

1. Seleccione **Crear clasificación**.
2. Complete la información requerida.
3. Guarde los cambios.

La nueva clasificación quedará disponible para todos los sistemas de referencia.

---

## Desactivar una clasificación

1. Abra la clasificación.
2. Deseleccione todos los sistemas de referencia asociados.
3. Guarde los cambios.

---

## Eliminar una clasificación

1. Seleccione el icono de eliminar.
2. Confirme la operación.

---
## Añadir o dar seguimiento a un plan de mejora

**Cuándo se usa:** para configurar, por cada sistema de referencia (ej. "Auditoría interna"), qué información se pide y cómo se califica cada auditoría que use ese sistema.
**Ruta:** Evaluaciones -> Administrar planes -> **Seleccionar el plan de interés (ej. Plan de Mejora ICONTEC-2025-2026, PAMEC, etc)**

Pasos:
1. Entrar al plan de mejora de interés.
2. Dentro de los detalles auditables, dar clic en el numero de 'Acciones de mejora', y entramos en la respectiva acción.
3. Dirigirse a la prestaña 'Seguimiento' o 'Seguimientos de control' según la necesidad.
4. Dar clic en **Adicionar** y llenar los campos requeridos.
5. Grabar


### Configurar seguimientos y privilegios
**Cuándo se usa:** para configurar, por cada sistema de referencia (ej. "Auditoría interna"), quienes pueden hacer seguimientos y como habilitarles permisos sobre los planes.
**Ruta:** Evaluaciones -> Sistemas de referencia -> **Seleccionar el sistema de interés (ej. Auditoría Interna, PAMEC, etc)**

Pasos:
1. Dentro de Sistemas de Referencia, seleccionar el sistema al que está relacionada la evaluación para hacerle seguimiento.
2. Dentro del sistema seleccionado, vamos a la pestaña **Privilegios**, y le damos clic al botón **Administrar Privilegios**.
3. Cuando se abra la ventana de los privilegios, metemos en el buscador el usuario, luego seleccionamos que privilegios tendrá (administración, consulta o adicion de evaluación).
4. Luego le damos clic al botón con el símbolo del mas '+' de color verde.
5. Dar clic en cerrar.

Para comprobarlo, vamos a **Evaluaciones -> Administrar planes**, seleccionamos algún plan que tenga el sistema de referencia al que tengamos privilegios configurados. Entramos a algun Plan de accion, y nos dirigimos a la pestaña 'Seguimientos' y a la pestaña 'Seguimientos de control'. En ambos debemos tener el botón **Adicionar**.

>Nota: en caso de no tener el botón **Adicionar** se deben seguir los pasos anteriores.


# Resumen de rutas

| Funcionalidad | Ruta |
|--------------|------|
| Crear informe | `Admin → Evaluaciones → Administrar planes` |
| Evaluadores | `Admin → Evaluaciones → Parámetros generales evaluación` |
| Sistemas de referencia | `Admin → Evaluaciones → Sistema de referencia` |
| Puntos de atención | `Admin → Evaluaciones → Parametrización de puntos de atención` |

---

# Buenas prácticas

- Cree primero el informe y posteriormente registre los hallazgos.
- Mantenga actualizados los evaluadores disponibles.
- Configure correctamente el sistema de referencia antes de iniciar una evaluación.
- Defina las transiciones para automatizar el flujo de aprobación.
- Utilice niveles de respuesta para estandarizar las auditorías.
- Cree campos personalizados únicamente cuando la información no pueda almacenarse con los campos existentes.
- No elimine configuraciones utilizadas en evaluaciones históricas.

---

# Notas importantes

- Los hallazgos siempre deben estar asociados a una Unidad Auditable.
- La clasificación de los hallazgos es completamente parametrizable.
- Los sistemas de referencia con información histórica no pueden eliminarse.
- Los puntos de atención pueden activarse automáticamente mediante los niveles de respuesta.
- Las transiciones permiten asignar diferentes responsables según la acción realizada sobre un hallazgo.