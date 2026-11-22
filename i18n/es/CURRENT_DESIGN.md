<!-- translation of docs/CURRENT_DESIGN.md, source sha256: a4c162fa040254e708d1d2a816f908416be83f27576a99e7dd1174c85218fced -->

# Diseño actual de la arquitectura

[English](../../docs/CURRENT_DESIGN.en.md) · [中文](../zh/CURRENT_DESIGN.md) · **Español** · [Français](../fr/CURRENT_DESIGN.md) · [Deutsch](../de/CURRENT_DESIGN.md) · [Italiano](../it/CURRENT_DESIGN.md) · [Русский](../../docs/CURRENT_DESIGN.md) · [Português](../pt/CURRENT_DESIGN.md) · [العربية](../ar/CURRENT_DESIGN.md)

Estado a 22 de noviembre de 2026. Es un **proyecto, no una implementación**. No se han
realizado experimentos sobre él. Las cifras con la marca [cálculo] se obtienen por fórmula,
no se miden.

## Dónde estamos

La idea está formulada en el [manifiesto](MANIFESTO.md), los requisitos obligatorios están
aprobados y la base de la arquitectura está elegida: una red sin coordinadores, un registro
común en una cadena de bloques pública, pago por trabajo verificado y pago diferido en lugar
de depósitos. Un pequeño piloto de confianza ya ha ejecutado un modelo Qwen en varios
ordenadores ([resultados del piloto](../../docs/PILOT_RESULTS.md)).

Lo más difícil está por delante. Aún no se ha encontrado una forma barata de verificar el
trabajo de modo que el engaño sea inútil incluso con colusión. Un modelo que se mejore a sí
mismo de forma fiable y siga las Leyes de SkyNet sigue siendo un objetivo de investigación.
Las tareas para los coautores están en las [preguntas abiertas](OPEN_QUESTIONS.md).

Marcas de estado:

| Marca | Significado |
|---|---|
| **Aceptado** | Aprobado en el proyecto como decisión |
| **Candidato** | Opción elegida, aún no aprobada o no construida |
| **Propuesta** | Presentada para decisión, no aprobada |
| **Abierto** | No hay decisión |

## 1. Esquema general (aceptado como base)

En la red **no hay coordinadores** ni roles con derechos especiales. Todos los participantes
tienen el mismo programa. Dentro de los límites de recursos, el propio programa:

| Trabajo | Qué hace | Por qué se le paga |
|---|---|---|
| Calcula | Ejecuta un paso de entrenamiento o la petición de un usuario | Por el resultado aceptado |
| Verifica | Recalcula un resultado ajeno si el sorteo elige a este participante como verificador | Por la verificación realizada |
| Vigila | Puede recalcular cualquier resultado e impugnarlo | Parte de lo descontado al descubrirse una falsificación |
| Almacena y reparte | Guarda los datos con los que trabaja | Paga el destinatario de los datos |
| Escribe en el registro | Reúne las entradas de los participantes en la cadena de bloques | Reembolso de gastos |
| Ayuda a ser encontrado | Retransmite conexiones para dispositivos detrás de un router | Se incluye en el pago de la entrega |

**Registro común**: un contrato en una cadena de bloques pública existente, sin clave de
administrador. Guarda las reglas y la huella del programa, las cuentas (créditos disponibles,
suma en espera, peso del trabajo verificado), las huellas de los resultados entregados, las
disputas, las votaciones, el catálogo de modelos y el plan de entrenamiento. El registro
funciona incluso cuando todos los nodos de SkyNet están apagados. La cadena de bloques
**no está elegida** (Abierto).

**La aleatoriedad pública** decide a quién le toca una tarea, qué se verifica y quién verifica.
Aparece después de que el resultado queda fijado. Candidata: una mezcla del faro drand y de la
aleatoriedad de la cadena de bloques (Candidato, fuentes no elegidas).

## 2. Vida de una tarea (candidato)

1. La tarea de entrenamiento se deriva del plan común de la red; la petición llega de un
   usuario con pago.
2. La aleatoriedad designa al ejecutor entre los dispositivos con recursos adecuados.
3. El programa calcula y registra las huellas de los estados intermedios.
4. La huella del resultado entra en un paquete, y el paquete, en el registro. La recompensa
   pasa a la suma «en espera».
5. La aleatoriedad, después de la entrega, decide si la tarea se verifica.
6. La tarea elegida la recalculan de forma independiente tres participantes aleatorios,
   a ciegas.
7. Coincide bit a bit: confirmado. No coincide: disputa, que se resuelve recalculando el paso
   elemental en disputa **en el propio registro**, y no mediante votación.
8. La ventana de verificación dura tres días: cualquiera puede impugnar el resultado.
9. Después de la ventana, la recompensa queda disponible.

**Pago diferido en lugar de depósito (aceptado).** Por el resultado, el participante responde
solo con la suma en espera: sus recompensas de los últimos tres días. No se cobra nada por
adelantado; los créditos ya disponibles nunca se descuentan.

## 3. Cómo hacer que el fraude sea deficitario: dos variantes

### Variante A. Verificación selectiva con descuento (especificación actual)

La proporción de verificación `p = 4R / (R + H)`, pero no inferior al 1%; el descuento por un
resultado incorrecto `B = 4R/p − R`, no mayor que la suma en espera `H` (`R` es el precio de
la tarea). Entonces cada falsificación cuesta en promedio cuatro precios de tarea a cualquier
frecuencia de verificación [cálculo]. La falsificación pasa solo si los tres verificadores
están en colusión: con una proporción de colusión `q`, la probabilidad es `q³`. El fraude es
deficitario mientras el grupo coludido tenga menos del ~91% del peso de los verificadores
[cálculo].

**Debilidad.** La falsificación no verificada se paga y permanece en la red. Es una apuesta que
tiene desenlaces ganadores para el defraudador.

**Cálculo preliminar (22 de noviembre de 2026, un solo ordenador, no confirmado por otros
participantes).** La estimación «91%» se obtiene de la media de una sola falsificación. No
tiene en cuenta que el participante no puede perder más que la suma en espera: no hay depósitos
ni multas. Para un participante que se va y entrega falsificaciones en tandas antes de que
terminen las verificaciones, la enumeración exacta de estrategias en el modelo `exit-scam-a`
da un límite más bajo [cálculo]:

| Reglas | Abandonar con falsificaciones es rentable a partir de la proporción de colusión |
|---|---|
| Tareas pequeñas idénticas, 399 precios en espera, una tanda | 89,2% |
| Tareas pequeñas idénticas, 1200 precios en espera, una tanda | 90,8% |
| Tareas pequeñas idénticas, tres tandas, regla «no más de un tercio en trabajo» | 89,0% |
| Tareas de tamaño arbitrario, tres tandas, regla «no más de un tercio» | 87,5% |
| Tareas de tamaño arbitrario, dos tandas de hasta 100 tareas, sin la regla «no más de un tercio» | 80% |
| Sin colusión, tareas de tamaño arbitrario, dos tandas (92 millones de estrategias) | no es rentable |

Sin la regla «no más de un tercio», las recompensas no verificadas de la primera tanda aumentan
la suma en espera y el tamaño permitido de las tareas de la segunda, por eso esta regla es
obligatoria. El modelo está escrito al principio del archivo del núcleo
[exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) y reproduce las cifras del
ejemplo de la especificación («aproximadamente 78, 107 y 17»). Las tareas se describen en
[tasks/README.md](../../tasks/README.md), la primera ejecución en
[results/FIRST_RUN.md](../../results/FIRST_RUN.md). Estas cifras se convertirán en resultado del
proyecto tras la confirmación independiente por otros participantes.

### Variante B. La red paga solo por lo verificado (propuesta, pendiente de decisión)

La tarea se convierte en un billete de lotería. El sorteo elige una proporción `p` de las
tareas (por ejemplo, el 1%); solo ellas se verifican y **solo ellas se pagan, pero `1/p` veces
más caras**. En promedio, el participante honesto recibe lo mismo, y la falsificación no
elegida no aporta **nada**.

- Sin colusión, la falsificación aporta exactamente cero.
- Con colusión, el pago falso no es más frecuente que `q^k` por tarea verificada (k es el
  número de verificadores): 0,1% con q = 10% y k = 3 [cálculo]. Cada intento fallido quema
  toda la suma en espera.
- Agujeros encontrados: el novato en colusión recibe en promedio `q^k` precios por intento y
  no pierde nada; la «campaña de salida» con muchas falsificaciones de golpe. Se proponen
  arreglos: plazas de aprendiz con un presupuesto limitado, anulación de todas las ganancias no
  maduradas de una clave al descubrirse una falsificación, y un tope de tareas abiertas.
- Coste: el ingreso se vuelve irregular. Para un dispositivo débil, aproximadamente ±13% al
  mes [cálculo].

Ambos esquemas exigen que el resultado **coincida bit a bit** en distintos dispositivos. Camino
propuesto: aritmética entera (int8/int32) del modelo, donde el orden de la suma no afecta al
resultado. **La velocidad y la calidad del Qwen entero no están medidas**; un perfil int8
reproducible conocido era 5,2 veces más lento que el normal (Abierto).

Disputa barata: dividiendo el cálculo a la mitad hasta una sola operación, y después comprobando
la multiplicación de matrices con un vector aleatorio (algoritmo de Freivalds). Ahorro de unas
100 veces en el número de multiplicaciones en matrices grandes, 2,6 veces en LoRA, y sin
ganancia al generar un token cada vez [cálculo] (Candidato).

## 4. Peso y participantes nuevos (candidato)

- **Peso**: la suma de los precios de los resultados que han pasado la verificación en 30 días.
  No se puede comprar, transferir ni acumular. El número de cuentas no aporta nada: las
  probabilidades y los votos son proporcionales al peso.
- El **novato** primero hace recomprobaciones «de aprendiz» de tareas ajenas: su respuesta no
  decide nada y se paga solo si coincide con el resultado aceptado. Después recibe tareas que
  se verifican siempre, y luego cada vez menos.
- El peso se calcula por cada modelo por separado. En un modelo que pocos dispositivos pueden ejecutar, el círculo
  de verificadores es pequeño y más fácil de capturar (Abierto).

## 5. Encontrarse y recuperarse (candidato)

| Dónde | Qué sobrevive al apagado completo |
|---|---|
| Registro en la cadena de bloques pública | Reglas, cuentas, peso, huella del modelo, plan de entrenamiento, disputas, direcciones de los nodos que escribieron |
| Discos de los participantes y espejos públicos | Pesos del modelo, estado del entrenamiento, datos; cualquier copia se coteja con la huella del registro |
| Distribución del programa | Identificador de la red, dirección del registro, lista inicial de lugares de encuentro |

Tres maneras independientes de ser encontrado; basta con una cualquiera: registros firmados en
plataformas externas («lugares de encuentro»), redes abiertas de búsqueda de nodos (por
ejemplo, DHT de libp2p) y las direcciones de nodos guardadas en el registro. La ventana de verificación no
avanza mientras la red está parada; si no, se podría entregar una falsificación antes de la
parada.

Puntos débiles: la autenticidad de la primera instalación (el novato se entera de la dirección
del registro desde fuera); el bloqueo completo de todas las vías a la vez; la confianza en dos
de tres proveedores de punto de control tras una inactividad prolongada.

## 6. Peticiones y privacidad (candidato)

La petición se cifra para el dispositivo del ejecutor y viaja directamente o a través de un
retransmisor bajo seudónimo. En el registro solo hay huellas. Alrededor del 1% de las
peticiones las ven además tres verificadores.

**Advertencia honesta.** En un ordenador normal, el propietario del dispositivo con un programa
modificado puede leer la petición que este calcula. El cálculo totalmente homomórfico para tales
modelos es miles de veces más lento. Por eso hay dos modos: el normal (barato) y el protegido
(solo en hardware que demuestra que el propietario no mirará dentro; más caro, y se sostiene en
la confianza en el fabricante).

## 7. Entrenamiento y elección del plan (propuesta)

Un catálogo abierto de modelos y conjuntos de datos con licencias libres, fijados mediante
huellas. La red, según la regla, compone variantes de entrenamiento, da a cada variante una
prueba y reparte la potencia libre según los resultados y la votación por peso. Una versión
nueva del modelo sustituye a la anterior solo si ha aprobado mejor el examen, cuyas tareas las
elige la aleatoriedad después de fijar los pesos. La contribución de una sola tarea a la
actualización de los pesos está limitada; la parte «ligera» del paso (la suma de las
contribuciones) se recalcula siempre.

Un modelo que **se mejora a sí mismo de forma fiable e infinita** es una meta de investigación,
no una tecnología lista. Primera etapa realista: el ajuste fino automático y la selección
mediante examen.

## 8. Cambio de reglas (candidato)

Las reglas las cambia solo una versión nueva del programa, aceptada por 3/4 de **todo** el peso
tras una votación no inferior a 14 días y un plazo anunciado de 30 días. El freno común (más de
la mitad del peso) solo puede detener la versión nueva del modelo. Propuesta: un núcleo de
verificación inmutable que no se puede anular por votación (pendiente de decisión).

## 9. Resumen de ataques

De 60 maneras de fraude analizadas: 18 están cerradas, 6 son deficitarias, 19 están limitadas y
16 abiertas (para la variante A). Principales puntos abiertos:

1. **Mayoría por peso.** Un grupo con 3/4 del peso puede cambiar las reglas; en una red pequeña
   esa proporción se puede reunir con trabajo honesto en potencia alquilada. Por eso el arranque
   es cerrado, con créditos de aprendizaje.
2. **Fundamentos no construidos.** La coincidencia bit a bit y el recálculo de la disputa en el
   registro para el modelo completo no están construidos.
3. **Saboteador que no busca beneficio.** Puede estropear el entrenamiento dentro de la
   proporción de su trabajo; el examen no detecta las puertas traseras ocultas.
4. **Peticiones ajenas** en el modo normal y en las disputas.
5. **Disponibilidad de los datos.** La disputa «entregó o no entregó los datos grandes» no se
   puede dirimir con nada.
6. **Entrada en la red.** La cola para las plazas de aprendiz y la autenticidad de la primera
   instalación.

Los detalles y las tareas para los coautores están en [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
