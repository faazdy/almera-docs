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