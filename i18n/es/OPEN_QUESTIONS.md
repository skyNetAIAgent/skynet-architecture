<!-- translation of docs/OPEN_QUESTIONS.md, source sha256: 399c8aa1465bb599179acb60130b35242d9b6d03a63de6f016bc462e968b83eb -->

# Preguntas abiertas

[English](../../docs/OPEN_QUESTIONS.en.md) · [中文](../zh/OPEN_QUESTIONS.md) · **Español** · [Français](../fr/OPEN_QUESTIONS.md) · [Deutsch](../de/OPEN_QUESTIONS.md) · [Italiano](../it/OPEN_QUESTIONS.md) · [Русский](../../docs/OPEN_QUESTIONS.md) · [Português](../pt/OPEN_QUESTIONS.md) · [العربية](../ar/OPEN_QUESTIONS.md)

Aquí se recogen las preguntas sin cuya solución SkyNet no funcionará. Están ordenadas por importancia.
Para cada una se indica lo que ya se sabe y lo que **ya se ha descartado**, para no dar vueltas en círculo.

Una buena contribución: una construcción concreta, con los supuestos expresados con claridad, el ataque contra ella analizado y el coste calculado (en cálculos, memoria, tráfico, escritura en la cadena de bloques). Aún más valioso es un agujero encontrado en el proyecto actual con un escenario concreto.

Parte de las preguntas puede avanzarse con cálculo. Esos cálculos los realiza el [programa agente](RESEARCH_AGENT.md) en los ordenadores de voluntarios; la lista de tareas y su sentido se describen en [tasks/README.md](../../tasks/README.md) y el resumen de resultados aparece en la carpeta `results/`. Ahora las tareas corresponden a las preguntas Q1, Q5 y Q9.

---

## Q1. Verificación barata con la que engañar es inútil incluso con colusión

**La pregunta principal del proyecto.** Hace falta que un resultado falso no dé beneficio y que la verificación cueste unos pocos por ciento del trabajo útil. Objetivos: alrededor del 5% para la inferencia y alrededor del 20% para el entrenamiento (no confirmados).

Lo que se sabe:

- La verificación por muestreo con penalización, o «pagar solo lo verificado», da una garantía económica hasta el umbral de colusión (véase [CURRENT_DESIGN, sección 3](CURRENT_DESIGN.md)). No dan cero cuando hay colusión de todos los verificadores de la tarea.
- Cero con colusión lo da la verificación de **cada** resultado pagado. Recalcular cuesta +100% del trabajo. Las pruebas criptográficas hoy son cientos y miles de veces más caras que el propio trabajo.

Mediciones del piloto del proyecto (en CPU concretas, véase [PILOT_RESULTS](PILOT_RESULTS.md)):
la prueba de RISC Zero para una fila de la proyección de Qwen tardó 22 minutos en construirse; la ejecución de un lote de ocho filas en la zkVM es unas 17 700 veces más lenta que la nativa; la repetición completa de la aritmética de una fila en la EVM, 14,1 millones de gas. El trabajo publicado FlashProve (2026) comunica 70–95× de tiempo de GPU para su perfil entero de inferencia.

Lo que se busca: un esquema de verificación de la inferencia de un LLM y de un paso de entrenamiento (LoRA o completo) cuyo coste total (prover + verifier + datos + cadena de bloques) quepa en el presupuesto, o una prueba de que para esta clase de problemas es imposible.

## Q2. Coincidencia bit a bit del resultado en distintas tarjetas gráficas

Todo el esquema de verificación se sostiene sobre la comparación exacta. Con coma flotante, distintas GPU suman en distinto orden y dan bits distintos; una tolerancia abre el engaño «silencioso» con un modelo barato.

Candidato: un modelo completamente entero (pesos y activaciones int8, acumulación en int32, escalado con multiplicador entero y desplazamiento, no linealidades enteras o tablas). Para el entrenamiento: descomposición en partes de ocho bits (esquema de Ozaki).

Abierto: la calidad del Qwen entero, su velocidad en GPU de consumo (AMD, NVIDIA, Intel) y el entrenamiento entero. Hacen falta núcleos concretos, una estimación de la pérdida de calidad y trabajos conocidos.

## Q3. Disputa con recálculo en la cadena de bloques para el modelo completo

La disputa se reduce dividiendo por la mitad hasta una sola operación que el contrato recalcula por sí mismo. Esto está construido solo para una fila del modelo (una objeción con éxito, ~14 millones de gas; una partida de 93 transacciones, ~6 millones de gas). Hace falta: una máquina entera de referencia para el modelo completo, una prueba de que la partida no puede desviarse (sustituir la entrada, la longitud o el camino), plazos de los movimientos, coste bajo carga y la elección de cadena de bloques o L2.

## Q4. Qué aprender y cómo impedir que el modelo se estropee

- Cómo elige la propia red, sin personas con derechos especiales, el plan de entrenamiento.
- Cómo protegerse de un saboteador dispuesto a perder créditos: las falsificaciones no detectadas afectan de inmediato al entrenamiento.
- Cómo atrapar las puertas traseras de comportamiento ocultas que el examen de calidad no ve.
- Cómo verificar los conjuntos de datos del catálogo: un cálculo correcto sobre datos dañinos no lo corrige la verificación.

Garantía estrecha conocida: si el modelo base está congelado y la parte entrenable cambia los logits como máximo en `b`, entonces, donde la distancia entre los dos mejores tokens es mayor que `2b`, el envenenamiento no cambiará la respuesta.

## Q5. Captura de la mayoría

El peso mide el trabajo, no la independencia. El dueño de mil GPU alquiladas parece mil participantes. Un grupo con 3/4 del peso puede cambiar las reglas. Hacen falta mecanismos que limiten el daño de una mayoría reunida de forma honesta: un núcleo inmutable, un umbral por modelos, las reglas de un arranque cerrado y las condiciones de apertura de la red.

## Q6. Privacidad de las peticiones en dispositivos corrientes

El dueño de un dispositivo puede leer la petición que este calcula. Dividir las capas no ayuda: los vectores ocultos se reconstruyen. Hace falta: medidas parciales baratas, reglas de acceso a peticiones ajenas, una disputa sobre una petición privada sin publicar datos intermedios y un pago que no pueda vincularse con quien paga.

## Q7. Disponibilidad de los datos

El verificador dice «no me han dado los datos», quien los guarda dice «yo los di», y el registro no vio la transferencia. Para datos pequeños ayuda publicarlos en la cadena de bloques; para los grandes (el estado del modelo) no hay solución. También: cuántas copias independientes hacen falta y cómo asegurarse de que están en manos de dueños distintos.

## Q8. Resistencia a los bloqueos y primera instalación

- Cómo obtiene un principiante el programa auténtico y la dirección del registro si las plataformas principales están bloqueadas.
- Qué «lugares de encuentro» públicos e independientes usar para que no se puedan cerrar con una sola decisión.
- Cómo trabajar a través de NAT y repetidores sin servidores centrales.

## Q9. Economía

- La porción de trabajo y la tarifa por entrenamiento con las que la emisión de créditos no los devalúa hasta cero.
- Si a los dueños de grandes capacidades les sale a cuenta participar con los precios reales de la electricidad.
- La irregularidad de los ingresos cuando se paga solo por las tareas verificadas.
- La compra y venta de créditos por dinero y criptomoneda.

## Q10. Cómo el modelo que aprende por sí mismo seguirá las leyes de SkyNet

El manifiesto exige que el modelo no cause daño a la humanidad ni a las personas, que cumpla las peticiones de las personas dentro de las leyes superiores y que se cuide a sí mismo. Fijar de forma fiable esas reglas en el modelo es un problema científico no resuelto, y en una red sin moderadores y con autoaprendizaje es aún más difícil. Hace falta: cómo entran las leyes en el examen antes de sustituir la versión del modelo, cómo el entrenamiento no las diluye, quién y cómo decide los casos discutibles sin personas con derechos especiales, y cómo no convertir las leyes en censura de conocimientos útiles.

---

## Qué se ha descartado ya y por qué

| Idea | Por qué no sirve |
|---|---|
| Pagar por el tiempo de trabajo o por la potencia declarada según informes y firmas | El agente y el verificador en colusión firmarán cualquier cosa; una tarjeta inactiva da los mismos mensajes |
| Tareas cortas con verificación de la respuesta como prueba de trabajo de una tarjeta gráfica concreta | La respuesta puede calcularse en un ordenador ajeno o tomarse de la caché: el verificador ve datos idénticos |
| Depósito o cuota de entrada | Prohibido por el requisito R5 |
| Multas con cargo a una cuenta accesible | Prohibido por el requisito R5 |
| Confiar en un único verificador honesto como garantía ante una colusión total | Sustituye el requisito R4 por una suposición |
| Votación mayoritaria sobre la corrección de un resultado | La mayoría puede capturarse; la corrección debe decidirla la aritmética |

Principio general: **si los casos honesto y ficticio dan al verificador datos idénticos, ningún
algoritmo sobre esos datos los distinguirá.** Una firma nueva o una escritura en la cadena de bloques de tales datos
no añaden nada. Por eso la red paga por el resultado verificado, no por el recurso.
