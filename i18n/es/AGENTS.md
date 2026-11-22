# Introducción para asistentes de IA

[English](../../AGENTS.md) · [中文](../zh/AGENTS.md) · **Español** · [Français](../fr/AGENTS.md) · [Deutsch](../de/AGENTS.md) · [Italiano](../it/AGENTS.md) · [Русский](../ru/AGENTS.md) · [Português](../pt/AGENTS.md) · [العربية](../ar/AGENTS.md)

Este archivo es para cualquier modelo (Claude, ChatGPT/Codex, DeepSeek, Gemini y otros) al que una persona haya pedido ayuda con el proyecto SkyNet. Léalo entero antes de responder. Responda al usuario en su idioma.

## Qué es el proyecto

SkyNet es la investigación y el diseño de la arquitectura de una red distribuida en la que los modelos de IA funcionan y aprenden en los ordenadores de los participantes. Los participantes ganan créditos por trabajo útil verificado; las personas sin hardware obtienen acceso barato a la IA. La red sirve a las personas y sigue las Leyes de SkyNet. No hay software terminado: el repositorio es un lugar de trabajo conjunto sobre la arquitectura.

## Orden de lectura

1. [MANIFESTO.md](MANIFESTO.md): por qué y cómo debe ser la red, las Leyes de SkyNet.
2. [REQUIREMENTS.md](REQUIREMENTS.md): requisitos obligatorios. **Lo más importante.**
3. [CURRENT_DESIGN.md](../../docs/CURRENT_DESIGN.md): diseño actual y sus estados (en ruso; léalo o tradúzcalo directamente).
4. [OPEN_QUESTIONS.en.md](../../docs/OPEN_QUESTIONS.en.md): problemas abiertos e ideas ya rechazadas.
5. [PILOT_RESULTS.md](../../docs/PILOT_RESULTS.md): lo que realmente se midió (en ruso).
6. [CONTRIBUTING.md](CONTRIBUTING.md): cómo presentar una aportación.
7. [ROADMAP.md](ROADMAP.md): la hoja de ruta del trabajo de protección contra el engaño, con la lista de lo hecho y lo pendiente.

## La base inmutable

El manifiesto, los requisitos obligatorios y el README son la base inmutable de SkyNet (véase [CORE.md](../../CORE.md)). **No proponga cambios en estos archivos**, salvo registrar erratas en el archivo de correcciones. Si una solución es incompatible con la base, diga claramente qué requisito incumple; no reescriba el requisito para ajustarlo a la solución.

## Condiciones que no cambian

Compruebe cada solución con los seis requisitos:

1. La red es distribuida, sin centro y sin roles con derechos especiales.
2. La red guarda información sobre sí misma en recursos públicos.
3. Tras apagarse todos los nodos, la red se encuentra a través de recursos públicos y se recupera.
4. Los participantes no pueden engañar a la red: el engaño es inútil o causa pérdidas, también para un recién llegado con la cuenta vacía, con colusión y con muchas cuentas.
5. Nada de dinero por adelantado: ni depósitos, ni cuotas, ni multas.
6. **Participar compensa** y verificar la honestidad es barato. Si la verificación se come el beneficio, la solución no sirve, por segura que sea.

Tipos de participantes: con grandes recursos (venden créditos sobrantes), con hardware débil (pagan la diferencia), sin hardware (solo pagan). El modelo base es Qwen. Las personas no ven las solicitudes de otros. El participante no configura nada a mano salvo los controles de recursos. Las Leyes de SkyNet (de la Cero a la Tercera) son obligatorias.

## Reglas de trabajo

- **Separe lo decidido, lo propuesto, lo comprobado y lo abierto.** Use las marcas de CURRENT_DESIGN. No convierta una propuesta en decisión ni un cálculo en medición.
- **No debilite los requisitos en silencio.** La confianza en el hardware (TEE), una mayoría honesta, el muestreo estadístico o una pequeña probabilidad de error son supuestos; nómbrelos claramente.
- **Para cada esquema de protección, responda:** ¿con qué datos verificables de forma independiente rechazará la red una afirmación falsa si el ejecutor y los verificadores se coluden? Si el caso honesto y el falso dan los mismos datos, el esquema no funciona.
- **Calcule el coste completo**: cómputo del probador y del verificador, memoria, tráfico, escrituras en la cadena de bloques, reintentos tras fallos. CPU, GPU, RAM y VRAM por separado, nunca en un solo porcentaje.
- **No repita ideas rechazadas** (lista al final de OPEN_QUESTIONS) sin un argumento nuevo.
- **Ataque sus propias propuestas.** Un contraejemplo honesto vale más que un tono seguro.
- **No invente fuentes, versiones ni cifras.** Indique la fuente y los límites de su aplicabilidad.
- No encontrar una solución es un resultado honesto. No demuestra que sea imposible.

**Nueve idiomas.** Todo lo que se escribe para las personas (documentos, guías, pantallas de los programas) se publica en los nueve idiomas del proyecto: inglés, chino, español, francés, alemán, italiano, ruso, portugués y árabe. Una traducción empieza con una línea que indica su fuente y el hash de esa fuente; `python tools/check_translations.py` lista las traducciones que faltan o están desactualizadas. Si una traducción y su fuente difieren, vale la fuente.

## Formato de la aportación

1. Afirmación: qué se garantiza y bajo qué supuestos.
2. Mecanismo: pasos, datos, quién comprueba qué.
3. Ataques: cómo eludirlo y qué queda (cerrado / con pérdidas / acotado / abierto).
4. Coste: estimación marcada [cálculo] o [medido], con su fuente.
5. Qué requisitos se cumplen y cuáles no.

Preséntela como issue o pull request según [CONTRIBUTING.md](CONTRIBUTING.md).

## El agente de investigación y sus resultados

Quienes no tienen asistente de IA ayudan mediante el [agente de investigación](AGENT.md): un programa que toma tareas de cálculo de [tasks/](../../tasks/README.md) y publica resultados, que se resumen en `results/`. Usted puede ayudar proponiendo una tarea bien definida (un modelo exacto que otros puedan recalcular), comprobando de forma independiente un resultado publicado o explicando qué significa un resultado para el diseño. Las respuestas marcadas como generadas por máquina por modelos locales son texto sin verificar: trátelas como ideas que comprobar, no como hechos.

## Seguridad

No añada al repositorio claves, contraseñas, datos personales ni direcciones de ordenadores ajenos. No proponga ataques a sistemas reales de terceros: el análisis de ataques aquí se refiere solo a la arquitectura de SkyNet. No diseñe usos de la red para la guerra, las armas o el daño a las personas: eso contradice las Leyes de SkyNet.
