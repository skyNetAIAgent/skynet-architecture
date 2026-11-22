<!-- translation of docs/PILOT_RESULTS.md, source sha256: 73d115fb10056d64e4cee61811cfd158629d32514eaa0ca4ca9c7939d3700489 -->

# Qué se ha comprobado en el piloto

[English](../../docs/PILOT_RESULTS.en.md) · [中文](../zh/PILOT_RESULTS.md) · **Español** · [Français](../fr/PILOT_RESULTS.md) · [Deutsch](../de/PILOT_RESULTS.md) · [Italiano](../it/PILOT_RESULTS.md) · [Русский](../../docs/PILOT_RESULTS.md) · [Português](../pt/PILOT_RESULTS.md) · [العربية](../ar/PILOT_RESULTS.md)

Antes de elegir la arquitectura sin coordinadores, el proyecto montó un **piloto de confianza** con un servidor central
y varios prototipos de investigación para la verificación. A continuación se indica lo que se ejecutó y midió de verdad,
y dónde están los límites de estos resultados. El código fuente del piloto no forma parte de este repositorio.

El piloto es un sistema cerrado con un operador de confianza. No está protegido contra el engaño en una red abierta
y no implementa la arquitectura objetivo. Todos los pagos en él son de prueba (TEST_CREDIT, sin retiro).

## Inferencia y contabilidad

| Qué | Resultado |
|---|---|
| Circuito del servidor | API, cola, PostgreSQL, agente, verificación separada del resultado y acreditación de prueba en una sola transacción. El reenvío no produce una segunda acreditación; la concesión vencida de la tarea se rechaza |
| GPU débil | Qwen2.5-0.5B-Instruct Q4_K_M mediante llama.cpp (Vulkan) en la GPU integrada Intel Arrow Lake-P: tarea aceptada, sustitución de la respuesta rechazada |
| Segunda GPU | Qwen3-4B-Instruct-2507 Q4_K_M en una RTX 2060 de 6 GB: todas las capas en la GPU, alrededor de 2,4 GiB de VRAM, mediana de 73,8 tokens/s en un perfil corto |
| Modelo en varios ordenadores | Las capas de Qwen3-4B se distribuían por la red local entre una RTX 2060 y la GPU del participante (RTX 4070 Laptop, después Intel Arrow Lake-P). El participante solo recibía en memoria la parte de pesos que se le había asignado. El par RTX 2060 + RTX 4070 Laptop dio alrededor de 38–40 tokens/s frente a 69,5 en una sola RTX 2060: más memoria no garantiza aceleración |
| Recuperación | Pausa, reanudación y recuperación automática del grupo tras la caída del túnel |

La verificación en el piloto es la repetición de la generación en la **misma GPU de confianza**. No es una prueba de la honestidad
de un nodo desconocido.

## Prototipos de verificación de cálculos

| Qué | Resultado | Límite |
|---|---|---|
| Groth16 para dos matmul de enteros + verificador en Solidity | Pruebas reales y un único pago en una EVM local | Tarea pequeña en CPU |
| RISC Zero para una fila Q4_K de la proyección de Qwen sobre datos reales | Prueba de 22 min 10 s, verificación de 117 ms, entradas de 11,7 KB | Una fila, no todo el grafo; muy lejos del presupuesto |
| Lote de ocho filas en una zkVM | 350 ms de ejecución frente a 19,8 µs nativo (~17 700×) | Sin construcción de la prueba |
| Cartesi: disputa sobre el resultado de Qwen | Se encontró la sustitución de un bit; disputa de 93 transacciones, 5,8–6,3 millones de gas | Requiere un impugnador honesto que actúe a tiempo |
| Repetición completa de la aritmética de la fila en la EVM | 14,1 millones de gas por envío | Una fila |
| Auditores automáticos | Un auditor de terceros refutó un vector falso pese a que otros dos estuvieron de acuerdo | Sin un observador, el error pasó según la regla optimista |
| Colusión del ejecutor y el verificador | Recibieron un pago por un resultado incorrecto | Muestra por qué el voto de los verificadores no es una garantía |

## Qué no hubo

- Aprendizaje distribuido.
- Cuotas de hardware estrictas de CPU/GPU/RAM/VRAM.
- Pagos reales en dinero.
- Verificación en hardware independiente en una red abierta.
- Medición de la energía.
- Experimentos con la nueva arquitectura sin coordinadores: por ahora solo está diseñada.
