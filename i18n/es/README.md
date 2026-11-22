# SkyNet: diseño abierto de la arquitectura

[English](../../README.md) · [中文](../zh/README.md) · **Español** · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Русский](../ru/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md)

## Qué es este repositorio

Aquí se diseña la arquitectura de SkyNet: una red distribuida en la que los modelos de IA funcionan y aprenden en los ordenadores de los participantes. Los participantes ceden a la red sus recursos de cómputo libres y reciben créditos a cambio, mientras que las personas sin hardware potente obtienen acceso barato a la IA.

Es un repositorio de **investigación**. Aquí no hay un programa terminado. Contiene:

- el [manifiesto](MANIFESTO.md): por qué hace falta la red, cómo debe ser y las Leyes de SkyNet;
- los [requisitos obligatorios](REQUIREMENTS.md), que no cambian;
- el [diseño actual de la arquitectura](../../docs/CURRENT_DESIGN.md) con marcas de «decidido», «propuesto» y «abierto»;
- las [preguntas abiertas](../../docs/OPEN_QUESTIONS.en.md) en las que necesitamos ayuda;
- [lo que se comprobó en el piloto](../../docs/PILOT_RESULTS.md) y lo que no;
- las [reglas de participación](CONTRIBUTING.md) y una [introducción para asistentes de IA](AGENTS.md);
- el [programa agente](AGENT.md): un pequeño programa para quienes no tienen asistente de IA.

## Para quién

- **Ingenieros de sistemas distribuidos, criptógrafos, investigadores de ML.** Los problemas principales están donde se cruzan estas áreas: verificación barata del cómputo, protección contra la colusión, recuperación de una red sin centro.
- **Propietarios de hardware** (GPU, servidores, PC domésticos). Su visión de la rentabilidad y del coste de la electricidad es necesaria para que la economía funcione en la práctica.
- **Quienes trabajan con un asistente de IA.** A su modelo (Claude, ChatGPT, DeepSeek y otros) le basta con leer [AGENTS.md](AGENTS.md) para ponerse en contexto y empezar a trabajar.
- **Quienes simplemente quieren ayudar con su ordenador o su teléfono.** No hacen falta conocimientos especiales: el trabajo lo hace el [programa agente](AGENT.md).

## El sentido

Hoy no todo el mundo tiene acceso a una IA potente: lo impiden el precio, las restricciones geográficas y políticas y los bloqueos de servicios. Al mismo tiempo, el mundo está lleno de tarjetas gráficas y ordenadores inactivos. SkyNet debe unir ambas cosas: una red sin dueño ni servidor central, difícil de apagar o bloquear, que se encuentra a sí misma tras un apagado total, planifica su propio entrenamiento, paga a cada uno con justicia por el trabajo útil verificado y sirve a las personas, no a la guerra ni a la destrucción.

## Lo más difícil, con honestidad

La condición principal es que **engañar a la red sea inútil o cause pérdidas, y que verificar la honestidad sea barato**; de lo contrario, participar no compensa. Una solución que cumpla de forma demostrada esta condición bajo colusión **aún no existe**. Hay candidatos sólidos y decenas de ataques analizados, pero los mecanismos clave no se han construido ni medido. El estado actual siempre se describe en [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md) y [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md). Si sabe cómo resolver aunque sea uno de estos problemas, le necesitamos.

## Cómo unirse

1. Lea el [manifiesto](MANIFESTO.md) y los [requisitos](REQUIREMENTS.md).
2. Elija una pregunta en [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md) o un ataque al [diseño actual](../../docs/CURRENT_DESIGN.md).
3. Abra un issue o un pull request según las [reglas](CONTRIBUTING.md). Lo más valioso: un fallo encontrado con un ejemplo concreto y una solución con su coste calculado.

Si trabaja con un asistente de IA, dígale: *«Estudia este repositorio siguiendo AGENTS.md y ayúdame con la pregunta N de OPEN_QUESTIONS».*

**¿No tiene asistente de IA?** Puede ayudar igualmente. Instale el [programa agente de SkyNet](AGENT.md): un pequeño programa de código abierto para Windows, macOS, Linux y Android. Consulta periódicamente este repositorio, toma tareas de investigación, las calcula en su dispositivo en los ratos libres y publica los resultados. Se actualiza solo desde este repositorio, y únicamente a versiones firmadas por el proyecto. La participación es voluntaria: en la etapa de investigación no hay recompensas.

## La base inmutable

El manifiesto, los requisitos obligatorios y este README forman la base inmutable de la red (versión 1). Sus huellas SHA-256 se publican en [CORE_HASHES.txt](../../CORE_HASHES.txt). La edición canónica es la rusa. Los detalles están en el [manifiesto](MANIFESTO.md) y en [CORE.md](../../CORE.md).

## Licencia

Los textos de la base se publican bajo CC BY-ND 4.0 (se permite copiarlos, no distribuir versiones modificadas); los demás documentos, bajo CC BY 4.0. Véase [LICENSE](../../LICENSE).
