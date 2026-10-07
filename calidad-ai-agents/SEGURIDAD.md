# Seguridad de la información — uso de las skills de IA

Aplica a `presentaciones-institucionales/` y `diagramas-flujo/`, y a cualquier skill de
producción que se agregue después a esta carpeta.

El repo es **privado** y los ejemplos en `assets/` están basados en documentos reales pero con
datos censurados — eso no es lo que hay que vigilar. Lo que hay que vigilar es **el momento en que
alguien del área usa la skill con información real y delicada** (un procedimiento con datos de
afiliados, un informe de gestión con cifras sensibles) para producir un diagrama o una
presentación. Esta guía es para ese momento.

## Principio general: minimizar lo que entra al chat

La skill no necesita el documento completo, necesita la estructura. Antes de pegar el insumo,
quita lo que no aporta al entregable:

- **`diagramas-flujo`**: el skill necesita los *pasos* y *roles* del procedimiento. Si el
  documento fuente trae, como ejemplo dentro de un paso, el nombre/cédula/caso puntual de un
  afiliado o cliente real, esa parte se quita — el diagrama no cambia si el ejemplo es genérico.
- **`presentaciones-institucionales`**: el skill necesita el *mensaje y las cifras agregadas*. Si
  el informe de partida trae una tabla nominal (nombres, cédulas, salarios individuales) para
  sustentar un punto, se sube el KPI agregado a la diapositiva, no la tabla con personas
  identificables.

Regla simple: si un dato no cambia lo que el diagrama o la diapositiva necesita comunicar, no
tiene por qué pasar por el prompt.

## Datos sensibles bajo la ley colombiana (Ley 1581 de 2012)

Salud, datos biométricos, origen étnico, orientación sexual/política/religiosa y datos de menores
son "datos sensibles" con protección reforzada (requieren consentimiento explícito para tratarse).
Dado que varios procedimientos de esta organización tocan datos de salud de afiliados (p. ej. algo
como lo visto en `diagramas-flujo/assets/ejemplos-reales/`), el punto de control es: **el caso que
se usa como insumo del diagrama o la presentación no debe traer identificación real de la
persona** — solo el proceso (qué pasa, en qué orden, quién es responsable por rol). Si hace falta
un caso concreto para ilustrar una variación del procedimiento, se usa uno inventado o
completamente anonimizado, nunca un caso real "porque es más claro".

## Dónde corre esto y quién ve los datos en tránsito

Esto es independiente de que el repo sea privado — importa **la herramienta con la que se está
corriendo la skill en el momento**, porque de eso depende qué pasa con lo que se pega en el chat:

- Si se usa Claude Code local, la cuenta de Claude (Pro/Max) o la API de Anthropic sin acuerdo
  empresarial, aplica la política estándar de retención de datos de Anthropic para consumidores/
  desarrolladores individuales — no la misma que un acuerdo empresarial con control de retención.
- Antes de pegar información real y delicada (no un ejemplo anonimizado) en cualquiera de las dos
  skills, confirma con quien gestione la cuenta de Claude en la organización si hay un plan
  empresarial con acuerdo de no retención/no entrenamiento.
- Esto aplica igual a `presentaciones-institucionales`, que además ejecuta scripts propios
  (`pptx_kit.py`) que leen/escriben archivos localmente. Confirmar que esos archivos temporales no
  queden en una carpeta compartida sin control de acceso.

## El entregable hereda la sensibilidad del input

Un PPTX o un diagrama generado a partir de un procedimiento con datos reales sigue siendo un
documento sensible — no se vuelve "solo una imagen" o "solo unas diapositivas" por haber pasado por la
skill. Antes de subirlo a Teams/SharePoint/correo o de compartirlo fuera del área, se aplica el
mismo control de acceso que al documento fuente, y se revisa que no haya quedado ningún dato real
que debía anonimizarse en el insumo.

## Checklist antes de usar la skill con info real

- [ ] ¿El insumo trae datos identificables de una persona (nombre, cédula, historia clínica,
      salario) que no son necesarios para el diagrama/presentación? → quítalos antes de pegarlo.
- [ ] ¿El caso trata datos sensibles de la Ley 1581 (salud, biométricos, menores, etc.)? →
      verifica que el insumo esté anonimizado, no solo "resumido".
- [ ] ¿Sabes si la cuenta de Claude con la que corre esto tiene acuerdo empresarial de no
      retención? Si no, no pegues el dato real — usa un caso equivalente inventado.
- [ ] El entregable final, ¿se va a compartir fuera del área o de la organización? → revisión
      extra de que no quedó nada sin anonimizar.
- [ ] El archivo generado (PPTX/PDF/PNG), ¿queda en un lugar con el mismo control de acceso que
      tendría el documento fuente?

## Qué se puede hacer sin restricción

- Diagramar o presentar procesos, KPIs agregados y roles (no personas) sin ningún cuidado especial
  — ahí no hay dato de terceros identificable.
- Usar casos ficticios o con marcadores genéricos ("Afiliado A", "Colaborador X") para ilustrar
  variaciones del procedimiento — cumple el mismo propósito que un caso real sin el riesgo.
