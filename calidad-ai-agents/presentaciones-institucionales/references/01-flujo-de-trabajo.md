# Flujo de trabajo detallado

## 1. Preguntas de arranque

Antes de proponer un esquema, ten resueltos estos puntos. Pregunta solo lo que no se deduzca
del mensaje del usuario.

Pregunta el **formato** y, **justo después, la modalidad**; son las dos que no se asumen.

| Punto | Por qué importa |
|---|---|
| **Formato de entrega** | PowerPoint (PPTX), Web (HTML) o PDF. Si no lo dicen, PPTX por defecto. Ver `03-formatos-de-salida.md`. |
| **Modalidad** | Gerencial, informativa o de capacitación. Se pregunta justo después del formato. Fija qué layouts se favorecen, el ritmo y la secuencia base — ver `SKILL.md` → "Modalidad de la presentación" y `06-recetas-de-composicion.md`. Si es mixta, que el usuario lo aclare. |
| **Audiencia y objetivo** | Comité directivo ≠ socialización a usuarios ≠ inducción de personal ≠ cliente externo. Afina el nivel de detalle dentro de la modalidad. |
| **Contenido base** | ¿Hay un informe/texto de partida o se construye desde cero? Si hay texto, pídelo completo. |
| **Extensión** | Nº aproximado de diapositivas o duración de la exposición (regla: ~1–2 min por diapositiva de contenido). |
| **Evento / fecha** | Para la portada y para el tono. |

## 2. Esquema previo (obligatorio)

Entrega una lista numerada: por cada diapositiva, **layout `L01`–`L14`** + **título que afirma la
conclusión** + **idea central en una frase**. Marca las de portada, sección y cierre. **Parte de la
secuencia base de la modalidad** (`SKILL.md` / `06-recetas-de-composicion.md`) y ajústala al
contenido, sin salirte de la paleta de layouts de esa modalidad. Elige cada layout por la pregunta
que responde la diapositiva. Espera aprobación explícita antes de generar.

Ejemplo:

```
1. Portada — Informe de gestión 2T-2026 · Comité Directivo
2. Sección — Contexto
3. L10 text-image — El programa nace del acuerdo marco de teletrabajo
4. L02 kpi-row — El trimestre cierra con utilidad y productividad al alza
5. Sección — Resultados
6. L05 split-half — Las solicitudes se concentraron en marzo
7. L06 share-100 — Tecnología concentra el 63 % del cupo asignado
8. L08 stages — La ruta de aprobación va en la etapa 3 de 5
9. L11 quote-avatar — La dirección respalda la ampliación
10. L09 closing — Tres decisiones para el Comité
```

No uses etiquetas genéricas como "Contenido — 3 datos". Si no sabes qué layout va, es señal de
que la idea de esa diapositiva no está clara todavía.

## 3. Redacción del contenido

- Una idea por diapositiva. El título dice la conclusión, no el tema ("Las ventas subieron 12 %",
  no "Ventas").
- **Para cada diapositiva, abre la receta de su layout en `06-recetas-de-composicion.md`**: llena
  sus slots, respeta sus proporciones y usa **el helper de `pptx_kit.py` que indica la receta**
  (`barra_apilada` para L06, `etapas` para L08, `cita` para L11, `Deck.texto_pleno` para L12–L14, …).
  No compongas de memoria ni cambies ese helper por uno más conocido.
- Texto de apoyo en frases cortas, no párrafos. Datos concretos antes que adjetivos.
- Todo dato que se cite debe poder rastrearse: si viene del informe base, se conserva la cifra tal
  cual. Lo que no cabe → notas del orador.

## 4. Generación

Sigue `03-formatos-de-salida.md`. Usa siempre `assets/plantilla.pptx` y `assets/paleta.md`. En
PPTX, cada diapositiva se arma con el helper de la receta de su layout; el modelo de script es
`assets/ejemplos-generados/pptx/ejemplo-gestion-integral-pptx.py`.

## 5. Entrega

Devuelve el archivo y ofrece, en concreto: condensar diapositivas densas, añadir una diapositiva
de agenda, exportar a otro formato, ajustar la portada.
