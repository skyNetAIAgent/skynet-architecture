# Requisitos obligatorios de SkyNet

[English](../../REQUIREMENTS.md) · [中文](../zh/REQUIREMENTS.md) · **Español** · [Français](../fr/REQUIREMENTS.md) · [Deutsch](../de/REQUIREMENTS.md) · [Italiano](../it/REQUIREMENTS.md) · [Русский](../ru/REQUIREMENTS.md) · [Português](../pt/REQUIREMENTS.md) · [العربية](../ar/REQUIREMENTS.md)

*Versión 1, 22 de noviembre de 2026. Edición canónica, parte de la base inmutable de SkyNet.*

Estos requisitos, junto con el [manifiesto](MANIFESTO.md) y las Leyes de SkyNet, forman la **base inmutable de la red**: no pueden cambiarse ni por votación ni por decisión de los creadores, de los desarrolladores o de la mayoría de los participantes. Una solución que incumpla aunque sea un requisito no sirve para SkyNet. Puede discutirse como investigación, pero indicando claramente qué requisito incumple.

## Las seis condiciones principales

| N.º | Requisito | Cómo comprobar una solución |
|---|---|---|
| R1 | **La red es distribuida.** | Los dispositivos de distintos participantes mantienen juntos su funcionamiento. Perder cualquier nodo, cualquier servidor, incluido el que pertenece a los creadores del proyecto, o un sitio de publicación no impide a los demás continuar. |
| R2 | **La red guarda información sobre sí misma en recursos públicos.** | El software instalado obtiene del exterior información suficiente para reconocer la red y encontrar los nodos que vuelven. Esta información sobrevive al apagado simultáneo de todos los nodos. Hay varias fuentes. |
| R3 | **La red se encuentra a sí misma y se recupera tras un apagado total.** | Los programas que vuelven se encuentran entre sí a través de recursos públicos, sin la dirección de un coordinador activo y sin una lista manual de nodos. |
| R4 | **Los participantes no pueden engañar a la red.** | Una afirmación falsa no lleva a un resultado aceptado, a la autoridad de otro, a una recompensa inmerecida ni a una historia reescrita. Se tienen en cuenta la colusión y las cuentas múltiples (Sybil). Para cada solución se muestra con qué datos verificables de forma independiente rechazará la red una afirmación falsa. **Sentido práctico:** el engaño es inútil o causa pérdidas, también para un recién llegado con la cuenta vacía. |
| R5 | **Nada de dinero por adelantado.** | Ni cuotas, ni depósitos, ni multas cargadas a la cuenta. Los depósitos y las multas ahuyentan a los participantes. |
| R6 | **Participar compensa.** | Aportar recursos (GPU, VRAM, CPU, RAM, SSD, HDD) es rentable. Verificar la honestidad es barato: su coste conviene a todos, en especial a los propietarios de grandes equipos y electricidad cara. |

**R6 es el más importante.** Si verificar la honestidad exige mucho cómputo, participar deja de compensar y la red pierde su sentido.

## Tipos de participantes

| Participante | Qué hace |
|---|---|
| Con grandes recursos | Gana créditos suficientes para sus necesidades y vende el excedente a otros participantes |
| Con hardware débil | Gana menos de lo que gasta en los modelos de la red y paga la diferencia en criptomoneda o dinero |
| Sin hardware | Solo consumidor: paga por usar los modelos |

Una misma persona puede ser proveedora de recursos y usuaria.

## Otras condiciones adoptadas

- **El estado se conserva.** Los derechos confirmados, las obligaciones, la historia de tareas aceptadas, la última versión aceptada del modelo y los datos para reanudar el entrenamiento sobreviven a una parada total. Repetir un paso inacabado no da una segunda recompensa.
- **División de la red.** Cuando las historias se contradicen, los créditos en disputa esperan a la historia canónica. Una misma aportación nunca se paga dos veces.
- **Sitios y claves sustituibles.** Perder una cuenta, un espejo o una clave no impide para siempre la recuperación.
- **Decisiones verificables tras reiniciar.** Para los créditos, los cambios de reglas y la aceptación de una versión del modelo se conservan datos con los que cualquier nodo puede comprobar el fundamento de la decisión.
- **Mínimo público.** El catálogo abierto contiene solo lo necesario para el descubrimiento y la comprobación de autenticidad. No se publican claves privadas, solicitudes privadas ni datos personales.
- **Privacidad.** Las personas no ven las solicitudes ni los datos personales de otros.
- **Independencia de las personas.** Nadie tiene derechos especiales, tampoco el desarrollador. La red fija y modifica su propio plan de entrenamiento; se admite votar sobre una lista de opciones.
- **Sencillez para el participante.** El participante no elige nada a mano: instala el programa, acepta las condiciones, ajusta los controles de recursos y pulsa «Iniciar».
- **Límites de recursos separados.** CPU, GPU, RAM, VRAM y disco se limitan por separado; no pueden sumarse en un solo porcentaje.
- **Toda la potencia libre entrena.** La potencia no ocupada por solicitudes se dedica al entrenamiento.
- **Modelo base.** Al principio, Qwen con pesos abiertos y licencia libre. Solo se puede pasar a otro modelo con pesos abiertos y licencia libre.
- **Leyes de SkyNet.** Las cuatro leyes del [manifiesto](MANIFESTO.md) obligan tanto al comportamiento del modelo como a las reglas de la red. La red sirve a las personas y no se construye como instrumento de guerra.

## Qué no puede sustituir a los requisitos

- El tiempo de funcionamiento, el número de informes y el periodo de puntos de control **no** son fundamento de pago.
- La firma de un participante, incluso junto con la de otro nodo, **no** demuestra que se haya aportado un recurso: quienes se coluden firmarán cualquier cosa.
- El muestreo estadístico, la confianza en un enclave de hardware (TEE) o un pequeño error criptográfico son supuestos. Pueden proponerse, pero deben nombrarse claramente, no presentarse como cumplimiento de R4.
- Una prueba exitosa no demuestra protección contra el engaño.
