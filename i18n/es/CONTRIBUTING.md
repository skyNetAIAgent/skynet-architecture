# Cómo participar

[English](../../CONTRIBUTING.md) · [中文](../zh/CONTRIBUTING.md) · **Español** · [Français](../fr/CONTRIBUTING.md) · [Deutsch](../de/CONTRIBUTING.md) · [Italiano](../it/CONTRIBUTING.md) · [Русский](../ru/CONTRIBUTING.md) · [Português](../pt/CONTRIBUTING.md) · [العربية](../ar/CONTRIBUTING.md)

Gracias por querer ayudar. Aquí importa la precisión, no el volumen: un fallo encontrado con un escenario concreto vale más que diez páginas de razonamientos generales.

## Qué aportar

- **Un ataque al diseño actual.** Un escenario: quién actúa, qué hace, qué obtiene, por qué la red no lo detecta. Indique la sección de [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md).
- **Una solución a una [pregunta abierta](../../docs/OPEN_QUESTIONS.en.md).**
- **Una fuente**: un artículo, protocolo o proyecto que resuelva parte de un problema, con versión, fecha y lo que **no** demuestra para nuestro caso.
- **Un cálculo de costes** o una corrección de uno existente.
- **Una corrección de traducción**: una imprecisión en una traducción de la base (mediante el archivo de correcciones).
- **Una tarea para el agente de investigación**: un cálculo que responda a parte de una pregunta abierta (véase [tasks/README.md](../../tasks/README.md)).
- **Potencia de cálculo**: si no tiene asistente de IA ni tiempo para escribir, ejecute el [agente de investigación](AGENT.md) en su ordenador o teléfono.

## Cómo presentarlo

Abra un issue y empiece el título con una etiqueta:

| Etiqueta | Para |
|---|---|
| `[Attack]` | Una forma de engañar o perturbar la red |
| `[Q<N>]` | Una propuesta para la pregunta abierta N |
| `[Source]` | Un artículo o proyecto útil |
| `[Cost]` | Una estimación de costes o corrección de cifras |
| `[Translation]` | Una imprecisión de traducción |
| `[Task]` | Un cálculo para el agente de investigación |

En el texto, indique:

1. Qué se garantiza y bajo qué supuestos.
2. El mecanismo.
3. Los ataques conocidos y lo que queda.
4. El coste, marcado [cálculo] o [medido].
5. Cuáles de los seis [requisitos](REQUIREMENTS.md) se cumplen y cuáles no.

Los pull requests a los documentos de trabajo (`docs/`) son bienvenidos. Si cambia el estado de un punto, explique por qué. Los issues y pull requests pueden escribirse en cualquiera de los idiomas del repositorio.

## Reglas

- **La base no cambia.** No se aceptará un pull request que modifique el manifiesto, los requisitos, el README o sus huellas. Véase [CORE.md](../../CORE.md).
- Un cálculo no se presenta como medición, ni una propuesta como decisión.
- No publique claves, contraseñas, datos personales ni direcciones de ordenadores.
- Sea educado y vaya al grano. Critique ideas, no personas.

Si trabaja con un asistente de IA, dele [AGENTS.md](AGENTS.md). El autor de un issue es responsable de la exactitud de su texto.
