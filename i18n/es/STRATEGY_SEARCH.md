<!-- translation of docs/STRATEGY_SEARCH.md, source sha256: 9c3fdac8710ac98433828b793ab6aad7fd31da5661c1fecb590bb7c63a2cdd26 -->

# Verificación «no por fuerza bruta»: qué aporta la matemática en lugar del recálculo completo

[English](../../docs/STRATEGY_SEARCH.en.md) · [中文](../zh/STRATEGY_SEARCH.md) · **Español** · [Français](../fr/STRATEGY_SEARCH.md) · [Deutsch](../de/STRATEGY_SEARCH.md) · [Italiano](../it/STRATEGY_SEARCH.md) · [Русский](../../docs/STRATEGY_SEARCH.md) · [Português](../pt/STRATEGY_SEARCH.md) · [العربية](../ar/STRATEGY_SEARCH.md)

Estado a 25 de noviembre de 2026.

Este documento es el resultado del quinto consejo de modelos. El propietario del proyecto preguntó literalmente:

> «¿Quizá tenga sentido elegir otra estrategia? Por ejemplo, ¿conectar alguna
> matemática? ¿Para no verificarlo todo sin distinción, sino predecir un intento de fraude y verificar solo
> en ese caso? ¿O hacer un análisis inteligente del funcionamiento de la red skynet y encontrar un comportamiento
> sospechoso? Pensad en esta dirección, qué más hay en la ciencia que pueda ayudar a no resolverlo por fuerza bruta».

El consejo analizó la teoría de juegos de inspección, la verificación por riesgo, la búsqueda de anomalías, las trampas, la verificación
por muestreo, los mecanismos sin verificación, la criptografía y la economía sin depósitos, y luego propuso una
estrategia y revisiones de las decisiones.

**Estado del documento.** Es un resultado de razonamiento y cálculo por fórmulas, no una medición.
No se hicieron para él experimentos, ejecuciones de la red ni instalaciones. Los participantes y los críticos ejecutaron solo
programas aritméticos cortos y pequeñas búsquedas exhaustivas en el procesador. Las cifras medidas se tomaron solo
de los [resultados del experimento D5](EXPERIMENT_D5.md) (resumen D5_RESULTS a 25 de noviembre de 2026) y están marcadas
[medido]; las cifras obtenidas por fórmulas a partir de parámetros nombrados explícitamente están marcadas [cálculo]. Los trabajos
de los científicos se nombran **de memoria**: no había red y no se cotejaron los textos de las fuentes primarias. **Las únicas
decisiones adoptadas son las decisiones D1–D25** en [ROADMAP](ROADMAP.md), sección 3. Todo lo demás
aquí es una estimación y recomendaciones del consejo. Donde los críticos discreparon, se dice directamente.

## 1. Resumen breve

1. **«Predecir el fraude y verificar solo a los sospechosos» con reglas abiertas no ahorra
   verificaciones.** Las reglas de verificación son iguales en todos los nodos y las conoce el defraudador (D4). Este presenta
   una falsificación solo donde el detector dice «seguro», y hasta el momento del fraude se comporta como
   un nodo honesto. Está demostrado con rigor: el detector eleva la probabilidad de verificación de una falsificación por encima de la
   verificación media del trabajo honesto en no más que la distancia entre sus distribuciones observables
   (sección 2). Por eso, la predicción, las anomalías, la confianza basada en el historial y los grafos solo pueden **añadir**
   verificaciones por encima de la cota inferior, pero no reducir la frecuencia por debajo de ella. En esto coinciden los seis
   trabajos y las tres críticas.
2. **Hay exactamente dos rasgos no falsificables:** el resultado del recálculo exacto después de que la respuesta
   ha quedado fijada de forma irrevocable, y la suma quemable en espera: las recompensas aún no pagadas de la clave,
   que se pierden al ser detectada. Todo el ahorro real proviene del segundo rasgo, no de la
   «inteligencia».
3. **La mejor estrategia encontrada para las respuestas del modelo:** el pagador verifica él mismo su respuesta en una
   pasada, y toma la decisión de «verificar o no» con **su propia moneda secreta** después de fijar
   la respuesta, con una probabilidad no inferior a `R/(R + H_lock)`. Aquí `R` es el precio de la tarea y `H_lock` la parte
   de las recompensas no maduradas del ejecutor que no madurará antes del final de la verificación. La respuesta de un novato
   con la cuenta vacía se verifica siempre. Entonces, con las condiciones de la sección 4, la falsificación no es rentable
   con ninguna proporción de colusión de los demás, incluida la colusión total. Esta estrategia cuenta con el apoyo de dos de los tres críticos;
   el crítico ChatGPT prefiere la verificación completa de cada respuesta (sección 6).
4. **El precio de la propia verificación es, además, de fracciones de porcentaje:** alrededor del 0,005–2% del trabajo según
   el calendario y la carga de la clave; en claves poco activas con limitación del daño, hasta el 6,7%
   [cálculo]. El coste principal se traslada al perfil exacto: este
   es 1,5–1,8 veces más lento que la generación normal de 8 bits con lote 1 y 2,5–2,8 veces con
   lote 8 [medido]. En conjunto, esto supone +50…+82% sobre la generación normal con lote 1 [cálculo]. La referencia del 5%
   choca con la velocidad del perfil exacto, no con la verificación.
5. **El daño no queda cubierto por la economía.** El saboteador no necesita beneficio: con la verificación por muestreo, parte
   de sus falsificaciones pasa (alrededor de la mitad con el calendario más barato, sección 4). Por eso,
   una respuesta no verificada debe llevar obligatoriamente la marca «no verificado», y «verificado» solo se pone tras
   una verificación completa antes de mostrarla. Para el paso de entrenamiento, el consejo no encontró una garantía nueva.
6. **El usuario sin equipo** no queda protegido por esta estrategia: si lo verifican
   nodos ajenos aleatorios, la fuga es `R·q^k` y, con colusión total, el precio completo (sección 5).
   Esto sigue siendo una cuestión abierta, D21.
7. **Lo que debe decidir el propietario:** si permitir el pago de lo no verificado según la regla de la moneda
   (D21, D11, D7); qué hacer con los fallos honestos gratuitos (D16), que son incompatibles
   con la verificación por muestreo; si adoptar la nueva decisión D26 sobre el «bloqueo» de la suma en espera y el límite
   de devolución al perjudicado; la regla de las disputas falsas (D23, cálculo M9) sigue siendo condición para la inclusión.
   Las preguntas se formulan en la sección 6.

**Notación.** `R`: precio de la tarea; `c`: coste del trabajo honesto; `c_f`: gastos
de la falsificación (el peor caso, casi cero); `H`: suma en espera de la clave del ejecutor;
`H_lock`: su parte que no madurará antes del resultado final de la verificación de una tarea dada;
`p`: probabilidad de verificación de la tarea; `q`: proporción de colusión entre los verificadores; `k`: número de verificadores
asignados; `n_w`: número de tareas de la clave por ventana de maduración; `ρ`: tiempo de verificación de la respuesta en una
pasada dividido por el tiempo de su generación (0,10–0,40 con lote 1, 0,26–0,64 con lote 8
[medido]); `γ`: ralentización del perfil exacto frente a llama.cpp Q8_0 (1,5–1,8 con lote 1, 2,5–2,8
con lote 8 [medido]); PPS: verificación por el propio pagador. `Δ₀` y `Δч`: diferencia esperada
de la ganancia de la falsificación frente a la inacción y frente al trabajo honesto; D1 y D25 exigen que ambas sean
no mayores que cero.

**Cómo leer.** Sección 2: por qué la predicción del fraude no funciona. Sección 3: tabla de todos los enfoques.
Sección 4: fórmulas que resistieron la crítica y errores encontrados. Sección 5: estrategia recomendada,
su precio y riesgo residual. Sección 6: preguntas-decisiones. Sección 7: cálculos y experimentos. Sección 8:
discrepancias no resueltas y referencias dudosas. Sección 9: quién hizo qué.

## 2. Por qué «predecir el fraude» no funciona con reglas abiertas

### 2.1. Cota a través de la variación total

Supongamos que la decisión de verificar la toma cualquier regla `π(x)` con un valor entre 0 y 1, donde `x` es
todo lo que la red o el pagador ven antes de la decisión: tiempo de respuesta, texto, estadísticas, historial de la clave,
grafo de vínculos. El trabajo honesto produce observaciones con distribución `P`; la falsificación, con distribución `F`.
Entonces

`E_F[π] − E_P[π] = Σ_x π(x)·(F(x) − P(x)) ≤ Σ_{x: F(x) > P(x)} (F(x) − P(x)) = TV(F, P)`.

La desigualdad es cierta porque `π ≤ 1` donde `F > P` y `π ≥ 0` donde `F < P`. La magnitud
`TV` es la distancia de variación total: hasta qué punto son distinguibles dos distribuciones. De aquí
(teorema T4 del trabajo claude2; la misma desigualdad en gpt1 y gpt2):

1. **La falsificación se verifica no más a menudo que el trabajo honesto en promedio, más `TV`.** Si una falsificación
   es difícil de distinguir por las observaciones (`TV ≈ 0`), el detector la verifica con la misma poca frecuencia que el trabajo honesto.
2. **Contra un adversario informado es aún peor.** Las reglas son abiertas (D4), por lo que el adversario calcula él mismo
   `π` y elige la observación con la que la verificación es menos probable. La probabilidad
   de detectar su mejor falsificación es igual al menor `π(x)` entre las observaciones que puede
   crear barato.
3. **Consecuencia para el ahorro.** Para que la falsificación sea deficitaria, debe verificarse con una probabilidad
   no inferior a `R/(R + H_lock)` (sección 4). Con `TV ≈ 0` habrá que mantener la misma frecuencia también para
   el trabajo honesto, es decir, no hay ahorro. Según la estimación de claude2, la ganancia de la «inteligencia» no supera
   el factor `R/(R − c*)`, donde `c*` es el precio de la falsificación indistinguible más barata; con un `c*` plausible
   `≈ 0,5R`, no es más de dos veces; pero `c*` lo elige el adversario y no está medido.
4. **El historial de la clave no dice nada sobre el momento del fraude.** Una clave que decide defraudar
   en la siguiente tarea tiene, hasta esa tarea, el mismo historial que una honesta (cociente
   de verosimilitud exactamente 1; teorema T5 de claude2, contraejemplo de gpt1). Por eso, las pruebas secuenciales
   (SPRT de Wald, CUSUM de Page), los algoritmos de bandidos y la «confianza» bayesiana solo se enteran de él
   después del fraude. Una pequeña búsqueda exhaustiva de claude1 mostró: si la frecuencia de verificación por confianza se reduce
   un 10% por debajo del umbral, aparece una estrategia rentable de «acumular confianza y defraudar»
   (+1,7R…+2,5R en 60 tareas); al reducirla a la mitad, +14,4R…+19,4R [cálculo]. El crítico Claude
   reprodujo estas cifras; el crítico DeepSeek, en el modelo más cercano, obtuvo otra magnitud (+0,085R),
   pero el mismo signo (sección 8).

### 2.2. Ejemplo con las mediciones de D5

La falsificación barata más natural es **el mismo Qwen ejecutado en llama.cpp Q8_0**. El perfil
exacto es 1,5–1,8 veces más lento que ella con lote 1 y 2,5–2,8 veces con lote 8 [medido], por lo que
la falsificación es notablemente más barata que el trabajo honesto. Además, es la respuesta del mismo modelo: el tiempo, el estilo
y la perplejidad bajo el modelo pequeño son los mismos que los de una respuesta honesta, y el ejecutor
puede añadir la latencia él mismo. Si la respuesta Q8_0 coincide con la respuesta exacta token a token, no es una falsificación:
según D2, importa el resultado. Si difiere en al menos un token, solo lo detectará el recálculo
exacto, porque los bits del perfil exacto coinciden en cualquier dispositivo probado [medido].

Salvedad del crítico ChatGPT: en D5 se midió la cercanía del perfil exacto al modelo oficial
(el mismo token en 90 de 90 posiciones, correlación de logits de 0,9996 [medido]), pero no se midió la cercanía de la falsificación Q8_0
al perfil exacto según rasgos baratos. Para la garantía esto no es importante: basta con que
nadie haya mostrado un rasgo que distinga cada falsificación disponible de una respuesta honesta.

### 2.3. Dónde siguen siendo útiles los detectores

Los detectores, las trampas y el análisis de la red son admisibles si **solo aumentan** la frecuencia de verificación:

- como cola de verificaciones voluntarias adicionales del pagador, que no cuentan
  para la garantía pero aumentan la detección real;
- contra saboteadores descuidados que no optimizan su comportamiento;
- para diagnosticar fallos de hardware y controladores; un participante puede llevar un CUSUM de sus
  autoverificaciones y detenerse antes de perder la suma en espera;
- con un flujo de errores no adaptativo, encuentran más errores por hora de verificación. Ejemplo de gpt1
  [cálculo]: con una proporción de falsificaciones del 2%, sensibilidad del 90% y 5% de falsas alarmas, se verifica el 8,57%
  de las tareas, se detecta el 90,2% de esta familia de falsificaciones y el precio es del 1,80% frente al 18,94% de la verificación uniforme.
  Pero la familia de falsificaciones que el detector no marca pasa en el 98% de los casos.

También hay un ataque inverso (claude2): las peticiones cuya respuesta honesta parece «anómala» obligan
a gastar verificaciones en los honestos. Si la verificación la paga quien la provocó, esto se limita solo;
si la paga la red, es una transferencia de carga.

## 3. Análisis de los enfoques

En la tabla, «garantiza» es lo que se sigue estrictamente con los supuestos indicados; «con `q`», el comportamiento
con una proporción de colusión de los verificadores; «cuenta vacía»: un novato con `H = 0` y muchas claves gratuitas;
«veredicto»: el resultado tras las tres críticas.

| Enfoque | Esencia | Qué garantiza | Con `q` y con `q = 1` | Cuenta vacía, muchas claves | Precio | Veredicto tras la crítica |
|---|---|---|---|---|---|---|
| Juegos de inspección (Dresher, Maschler, la revisión de Avenhaus–von Stengel–Zamir; juegos de seguridad de Tambe y coautores, de memoria) | Verificación aleatoria anunciada de antemano con una frecuencia con la que el fraude no es rentable | `Δ₀ ≤ 0` con `p ≥ (R − c_f)/(R + H_lock)`, incluso para una tanda de falsificaciones antes de marcharse (con las condiciones de la sección 4) | Si verifica el pagador, no depende de `q`, incluido `q = 1`. Si son verificadores asignados, la detección es `p·(1 − q^k)`; con `q = 1`, cero | `H = 0` ⇒ `p = 1`; cada clave responde con su propia suma, Sybil no ayuda | `p·ρ`: centésimas a décimas de porcentaje en claves activas; verificación completa para el novato [cálculo] | **Base de la estrategia**, si la frecuencia la ejecuta quien tiene su dinero en juego |
| Verificación por riesgo: SPRT, CUSUM, bandidos, confianza bayesiana | Verificar más a menudo a novatos y sospechosos, menos a los antiguos | Detecta rápido a un defraudador ruidoso persistente; contra un estratega, nada | El veredicto por opiniones de los verificadores se rompe con la colusión; con `q = 1`, cero | Las claves nuevas son gratuitas; una clave «antigua» acumula confianza y defrauda al final | El ahorro del 40–70% (ds1) se refiere a un adversario ruidoso, no a SkyNet | **No se puede** reducir la frecuencia por debajo del umbral (contraejemplo de la sección 2.1); se pueden distribuir verificaciones adicionales |
| Anomalías, grafos, Sybil (tiempo, logits, entropía, perplejidad del modelo pequeño, marcas de agua, coherencia de repeticiones, grafos de colusión, SybilGuard/SybilLimit/SybilRank) | Buscar comportamiento y vínculos sospechosos | Contra un adversario informado, nada (cota de la sección 2.1) | Una falsificación coordinada parece un acuerdo honesto; con `q = 1` no hay protección | SybilRank requiere nodos iniciales de confianza y un número pequeño de vínculos «atacantes»; la coalición compra los vínculos con trabajo honesto | La perplejidad del modelo pequeño cuesta alrededor del 1,3–5% de **cada** respuesta según la estimación de claude1 (crítico ChatGPT: en los extremos de ds2, 1,875–9%) [cálculo], más caro que la verificación según la regla; la marca de agua solo certifica al muestreador | Solo **señal para verificaciones adicionales** y diagnóstico de fallos |
| Trampas, gold questions, modelo de Dawid–Skene | Tareas con respuesta conocida, indistinguibles de las reales | Solo si la trampa es indistinguible y la respuesta es secreta. En una red pública, el secreto solo puede guardarlo el pagador, y la trampa coincide con su verificación (T9 de claude2) | La colusión comparte las trampas al instante; Dawid–Skene supone errores independientes | Las claves de un solo uso estudian las trampas con pruebas; el tipo de tarea (D22) es visible para el ejecutor | Un patrón fresco de texto libre cuesta una generación completa, más caro que la verificación (`ρ < 1`); para el nivel `2⁻⁸⁰` con una proporción de trampas del 10% hacen falta 526–527 asignaciones [cálculo] | No es más barato que la verificación por el pagador; la forma admisible es repetir una petición del pagador ya verificada |
| Verificación por muestreo y lotería (parte de los tokens o capas tras la fijación; BOINC, TrueBit, opML, proof of sampling, de memoria) | Verificar una pequeña parte del cálculo; o pagar solo lo elegido por sorteo (lotería B) | Tokens: un defecto pasa con probabilidad `1 − s/N` (99,2% con 8 posiciones de 1000 [cálculo]). Lotería B con verificación de lo elegido por el pagador: `Δ₀ = −c_f` con cualquier `p` | La lotería con comité da al novato `R·q^k`: 0,001R / 0,027R / 0,125R / R con `q` = 0,1 / 0,3 / 0,5 / 1, `k = 3` [cálculo] | La lotería B con el pagador sirve para el novato; el muestreo de tokens, no | Estado de Qwen3.5-4B: 48 MiB + 64 KiB por posición; una muestra en la posición 500/1500/4000: 79/142/298 MiB [cálculo]; la lotería da ingresos irregulares y exige prepago de `R/p` | Los tokens y las capas son **peores** que la pasada completa tanto en tráfico como en garantía; la lotería B con el pagador es una variante admisible. Los sistemas externos se sostienen con depósito o con «uno honesto de N» |
| Peer prediction (Bayesian Truth Serum de Prelec, peer truth serum, DMI, de memoria) | Pagar por la coherencia de los informes sin verificación | La veracidad es un equilibrio solo sin colusión; hay equilibrios no informativos | Con `q > 0` el grupo se pone de acuerdo; con `q = 1` el mecanismo paga por cualquier cosa | Boletos gratuitos con cada clave | No hay verificación, pero se paga por no se sabe qué | **Inaplicables** al cálculo determinista; el pago por coincidencia es pago por copia, prohibido por D15 |
| Criptografía sin prueba completa, TEE, semilla | Compromisos y revelaciones selectivas, disputa por división en dos, sumcheck/GKR, atestación TEE, generación determinista | El muestreo sin codificación tiene la misma cota `1 − s/N`; la prueba completa sí cumple D19, pero según el presupuesto de la etapa 4 cuesta 16,8 veces más y es más caro para la respuesta; TEE es confianza en el fabricante | La disputa y el determinismo no dependen de `q`; en TEE, una clave extraída compromete todo el parque | Reducir la frecuencia según la atestación daría la frecuencia reducida a todas las claves del adversario | Compromiso sobre la respuesta: 2–4 KB en el registro (D24) | Hacen falta un compromiso sobre la respuesta, la moneda secreta y la disputa por división en dos; TEE solo para aumentar la verificación o la privacidad. La propuesta de ds1 de reducir la frecuencia según TEE fue rechazada por todos los críticos |
| Economía sin depósitos (pagos aplazados, reputación como capital, seguro, precio de la clave en trabajo) | Castigar con la pérdida de recompensas no maduradas y de ingresos futuros | La suma en espera es la única palanca compatible con R5. El ingreso futuro al marcharse es cero. El seguro indemniza a la víctima, pero no reduce la ganancia del defraudador | Funciona si la frecuencia la ejecuta el pagador | `H = 0` ⇒ verificación completa. La entrada mediante trabajo es un depósito oculto, inútil al marcharse; con una fuga por comité `R·q³` y `q = 0,3`, el precio de entrada `10R` se amortiza con unas 370 tentativas (ds1) [cálculo] | Aplazamiento del pago durante la ventana de maduración | `H_lock` es una parte obligatoria de la estrategia; el resto no sirve de base para la garantía |

## 4. Cotas inferiores y fórmulas que resistieron la crítica

### 4.1. Falsificación única: el umbral `R/(R + H_lock)`, no `R/H`

Una falsificación detectada no se paga y quema la suma en espera (no se puede descontar nada más
según R5). Entonces

`Δ₀ = (1 − p)·R − p·H_lock − c_f ≤ 0  ⇔  p ≥ (R − c_f)/(R + H_lock)`,

y con una falsificación casi gratuita, `p ≥ R/(R + H_lock)`. Frente al trabajo honesto,
`Δч = Δ₀ − (R − c) ≤ Δ₀`, por lo que la segunda condición de D25 se cumple sola. En un novato, `H_lock = 0`
y `p = 1`. Frecuencia mínima [cálculo, claude2]: 0,5 con `H_lock = R`; 0,25 con `3R`; 0,0909
con `10R`; 0,01 con `99R`; 0,000231 con `4320R`.

El trabajo claude1 propuso la regla `p = min(1, R/H)` y la llamó exacta. El crítico Claude mostró
mediante búsqueda exhaustiva que el umbral exacto es `R/(R + H)`: con él, la mayor ganancia de la falsificación es exactamente 0, y ya
con `0,99·R/(R + H)` es de +0,225R a +0,299R [cálculo]. La regla `R/H` contiene un margen. El crítico
DeepSeek señaló que este margen es útil para el daño: con `R/H`, el número esperado de falsificaciones hasta la detección
es finito (alrededor de `H/R + 1`); con `R/(R + H)`, infinito (sección 4.4). No está decidido qué fórmula tomar
en el núcleo (sección 8).

### 4.2. Condición: la suma no madura antes del resultado de la verificación

Solo se puede quemar lo que aún no se ha pagado en el momento de una disputa demostrada. Si una parte de `H` madura
antes, la regla se rompe. Contraejemplos [cálculo]:

- claude2: una clave con `H = 99R` que madura antes del resultado presenta `n` falsificaciones con `p = 1%`;
  ganancia de 0,99R con `n = 1`, 9,04R con 10, 36,6R con 100;
- crítico Claude: una clave con `H₀ = 100R` deja el trabajo honesto y presenta falsificaciones, mientras los pagadores
  verifican tarde; ganancia +0,99R, +9,1R, +49,7R, +74,4R con `n` = 1, 10, 100, 300. Con el «bloqueo»
  (se quema todo), las mismas estrategias dan de −0,01R a −0,75R.

Por eso, en el denominador de la frecuencia de la tarea `i` solo entra la parte de la suma que madurará
**después** del plazo máximo de disputa de `i`, y el plazo de verificación por el pagador `δ` debe ser mucho menor que
la ventana de maduración `W`; ambos plazos se cuentan en tiempo activo (D12). Este es el supuesto
de «verificación puntual»; para un teléfono que rara vez se conecta a la red, es el primero que se incumple.

### 4.3. Olas de falsificaciones antes de marcharse

La fórmula de la falsificación única cubre una tanda de falsificaciones antes de marcharse solo con la regla de que
**«la primera detección demostrada quema toda la suma no madurada de la clave, incluidas las recompensas de la misma ola»**.

- Sin esta regla (gpt1): 10 falsificaciones paralelas con `R = 1`, `B = 4R`, `d = 0,2`, cuando
  cada una que pasa se paga y la suma antigua se pierde una sola vez, dan
  `10·0,8 − 4·(1 − 0,8¹⁰) = +4,4295R`, aunque una sola falsificación da cero. Si la detección anula toda
  la ola, la misma estrategia da −2,49676R [cálculo; repetido por los críticos].
- El crítico ChatGPT añadió un segundo ejemplo: con `H = R`, `p = 1/2`, dos falsificaciones con monedas
  independientes y un único descuento de la suma antigua, la ganancia es `R/4` [cálculo]. Por tanto, el protocolo debe
  vincular de forma atómica todas las obligaciones abiertas de la clave con todos sus ingresos no madurados.

Con esta regla, la demostración de claude2 (T2) es correcta: cada nueva falsificación multiplica el resultado esperado
por `(1 − p_j)·(1 + α_j/(H_lock + A)) ≤ 1`, donde `α_j` es el pago por lo no verificado y `A` lo
ya acumulado quemable. La inducción sobre el número de falsificaciones da `E[resultado] ≤ H_lock` para cualquier tanda
y cualquier secuencia adaptativa. Para una tanda homogénea, lo mismo se sigue de
`(1 + R/H)ⁿ ≥ 1 + nR/H`. La comprobación en una malla de fracciones exactas dio un exceso máximo de exactamente 0
[cálculo].

### 4.4. Verificación por comité: el factor `1 − q^k`

Si la detección debe registrarla al menos uno de los `k` verificadores asignados, y cada uno
pertenece a la coalición con probabilidad `q`, la probabilidad de detección cae a `p·(1 − q^k)` y el umbral
pasa a ser `p ≥ R/((R + H_lock)·(1 − q^k))`. Es inalcanzable cuando `1 − q^k < R/(R + H_lock)`
y siempre inalcanzable con `q = 1`. En la lotería B con comité, el novato recibe `R·q^k` por intento:
0,001R / 0,027R / 0,125R / R con `q` = 0,1 / 0,3 / 0,5 / 1 y `k = 3` [cálculo]. Esto coincide
con el modelo del adversario. La independencia de las elecciones también es un supuesto: al elegir `k` distintos de `N`
participantes, de los cuales `C` están coludidos, la probabilidad de colusión total es `C(C,k)/C(N,k)`;
con indisponibilidad general de los datos o entrega selectiva, puede llegar a `q` o a 1
(crítico ChatGPT, según el modelo del adversario). Conclusión de todos los trabajos: **la frecuencia debe ejecutarla quien
protege su decisión**: el pagador para su dinero, cada nodo para su propia contabilidad.

### 4.5. Daño: la proporción no detectada

El saboteador no necesita beneficio, por lo que el daño se evalúa por la proporción de sus falsificaciones que pasan sin ser detectadas.

- **El calendario más barato hace ilimitado el daño.** Con `p = R/(R + H)`, las falsificaciones no verificadas
  aumentan ellas mismas `H`, y la frecuencia cae. La probabilidad de sobrevivir a `n` falsificaciones desde el inicio
  `h = H/R` es `h/(h + n)`; el número esperado de falsificaciones hasta la detección es infinito (T8 de claude2).
  La estimación de claude1 «`e^{−m}`» subestima el paso: con `H₀ = 4320R` y 4320 falsificaciones, el paso exacto
  es 0,50 en lugar de 0,37 con frecuencia `m·R/H` y `m = 1`; 0,125 en lugar de 0,050 con `m = 3`;
  0,0078 en lugar de 0,0009 con `m = 7` [cálculo, crítico Claude].
- **Una falsificación selectiva** pasa con probabilidad `1 − p`: en una clave madura con
  `n_w = 4320`, alrededor del 99,977% (crítico ChatGPT) [cálculo].
- **La corrección basada en la parte verificada de la suma no resistió.** claude2 propuso calcular la frecuencia
  según `H_ver`, las recompensas solo por tareas verificadas; entonces, en una clave honesta `p ≈ 1/√n_w`
  (punto fijo `p²·n_w + p − 1 = 0`) y la proporción de falsificaciones del saboteador es aproximadamente `p`: 5,6% con
  `n_w = 300`, 1,8% con 3000, 0,58% con 30 000 [cálculo]. El crítico Claude mostró que `H_ver`
  se infla con las peticiones autopagadas de la coalición; el crítico ChatGPT, que un saboteador con una clave nueva
  tras una respuesta verificada con `p = 1/2` consigue que sea falsa aproximadamente la mitad de sus respuestas entregadas. Ningún trabajo encontró una frontera económica del daño que resista el autopago y las claves nuevas.

Conclusión: con cualquier `p < 1`, parte de las respuestas del saboteador es falsa. Para las peticiones, esto solo es admisible con
la marca «no verificado» (texto de D6); para el paso de entrenamiento, no.

### 4.6. Otras fórmulas que resistieron la crítica

- **Los fallos gratuitos son incompatibles con la verificación por muestreo** (claude1). Si un fallo honesto
  no quema la suma (D16), el defraudador detectado llama fallo a la falsificación, y
  `Δ₀ = (1 − p)·R − c_f > 0`. Con `b` fallos gratuitos por ventana, la fuga es del orden de `b·H` por ventana
  [cálculo].
- **Pagadores perezosos** (claude2). Si una proporción `λ` de los pagadores no verifica y el ejecutor
  no los distingue, hace falta `p·(1 − λ) ≥ R/(R + H_lock)`. Si los distingue, la falsificación contra ellos
  aporta hasta `R` sin riesgo. La disuasión es un bien común: el pagador que desactiva la verificación
  ahorra fracciones de porcentaje y no pierde nada. Este es el supuesto de que «los pagadores ejecutan en promedio
  la moneda del núcleo».
- **Precio e irregularidad de la lotería B** (claude2, T7, con corrección del crítico ChatGPT). El pago `R/p`
  con probabilidad `p` da un coeficiente de variación de los ingresos `√((1 − p)/(pT))` en `T` tareas.
  Para una dispersión dada `v` hace falta `p ≥ 1/(1 + T·v²)`; con `T = 6000`, `v = 10%`, `ρ = 0,21`,
  el precio mínimo de verificación es 0,3443% [cálculo]. Con verificación «por cada uno de 1000 nodos», el mismo precio
  se multiplica por el número de nodos, por lo que la lotería con verificación por todos los nodos no sirve para la emisión de créditos.
- **La colusión del pagador y el ejecutor** se reduce a transferir su propio dinero dentro de la coalición, mientras
  la petición pagada no cree emisión de créditos, peso ni derecho a indemnización con cargo a la caja común.

### 4.7. Errores en las fórmulas de los trabajos (breve)

| Trabajo | Error | Corrección |
|---|---|---|
| ds2 | El segundo umbral está escrito como `(c − c_f)/R` | Debe ser `(c − c_f)/(R + H)`; este umbral nunca es vinculante. Pasar a los miniagentes solo la versión corregida |
| ds1 | En el juego, la pérdida se toma como `L = H + V` sin tener en cuenta `c_f` ya gastado | Umbral `(R − c_f)/(R + H + V)`; con `H = 0`, `c_f = 0,1R`, 90%, no 100% |
| claude1 | Equilibrio del juego de inspección con `L = H + R` (doble conteo de `R`) | Punto de indiferencia `(R − c_f)/(R + H)`: con `H = R`, `c_f = 0`, 1/2, no 1/3 |
| claude1 | «La regla `R/H` es exacta»; daño `e^{−m}` | Umbral exacto `R/(R + H)`; el paso es mayor (sección 4.5) |
| claude1 | Generación especulativa «alrededor de `1 + ρ·s`» | No demostrado; según el crítico DeepSeek, doble conteo; con lote 8 resulta 1,65–2,79 |
| claude2 | T7: «`κ·CV²` no depende de `p`» | Hay un factor `1 − p`; umbral exacto `p ≥ 1/(1 + T·v²)` |
| claude2 | El precio agregado 0,2–1,2% se toma con `n_w = 3000` | Con `n_w = 300`, 0,56–2,24% (hasta 3,6% con lote 8); con `n_w = 30`, 1,7–6,7% [cálculo] |
| claude2 | Instantáneas de estado de 0,33 y 2,9 GiB por respuesta | Con caché de atención, 0,651 GiB (500/500, paso 64) y 12,38 GiB (2000/1000, paso 16) [cálculo, crítico ChatGPT] |
| claude2 | En S1, el pago de lo no verificado `α` con la regla según `H_ver` siempre es igual a `R` | No hay transición suave A/B en S1; no hace falta un faro común para la decisión de verificar |
| ds1, gpt1, gpt2 | Presupuestos de estrategias sin la ralentización del perfil exacto | El precio completo es 1,5–1,8 veces mayor ya con lote 1 (sección 5.2) |
| ds1 | «La verificación de `k` tokens no es más barata que la pasada completa» | En cómputo es más barata; pierde en tráfico de estado y en garantía |
| gpt2 | Certificado por cotas de logits: 6,25% | Las cotas requieren el estado verdadero de la última capa; la cabeza es alrededor del 15% de las multiplicaciones, el ahorro no supera su parte |
| ds2 | Proporción estable de fraude contra CUSUM `θ = d_h/(d_h + d_f)` | Es una aproximación por deriva media, no un teorema |
| ds1 | SPRT: 65 y 133 observaciones | Recálculo exacto del crítico ChatGPT: 132,73 y 76,70; prueba fija, 229 [cálculo]; no se refiere a un adversario estratégico |

## 5. Estrategia recomendada

### 5.1. Respuestas del modelo: «pagador-inspector con apuesta»

El núcleo procede de los trabajos claude1 y claude2; las correcciones, de gpt1 y las tres críticas.

1. **Perfil exacto.** Cada respuesta pagada se genera en el perfil exacto v2 (elección voraz
   o Gumbel-max canónico); el criptograma de la respuesta se registra en el registro en una sola entrada
   con acuse (D24).
2. **Moneda secreta del pagador.** Una vez fijada irrevocablemente la respuesta, el programa
   del pagador decide con su aleatoriedad secreta si la verifica en una sola pasada, con probabilidad
   `p_i = max(p_usu, R_i/(R_i + H_lock))`. `p_usu` lo elige el propio usuario; con
   `p_usu = 1` solo ve respuestas verificadas. Con `H_lock = 0` (novato), la verificación es siempre.
   Para esto no hace falta un faro común mientras el pago no dependa del resultado de la moneda; la decisión no espera
   a un bloque público.
3. **Bloqueo de la suma.** `H_lock` de la tarea `i` son las recompensas no maduradas de la clave que madurarán después
   del plazo máximo de disputa de `i`; el plazo de verificación `δ` es mucho menor que la ventana de maduración (sección 4.2).
4. **Quema.** Cualquier discrepancia demostrada quema **toda** la suma no madurada de la clave, incluidas
   las recompensas de la misma ola. Al perjudicado se le devuelve no más que su pago `R`; el resto
   se destruye. De lo contrario es posible el ataque de «autodisputa»: la coalición detecta con su clave-pagador
   una petición autopagada falsificada a propósito y se lleva sumas ajenas saltándose la ventana de maduración
   (crítico Claude).
5. **Marcas.** «Verificado» es solo la respuesta verificada por completo antes de mostrarse. Todo lo demás
   es por defecto «no verificado». La marca «verificado por muestreo» (claude1) fue rechazada por todos
   los críticos por inducir a error.
6. **Señales solo hacia arriba.** Las anomalías, la perplejidad, los grafos y las repeticiones de peticiones verificadas
   (trampas) solo activan verificaciones voluntarias adicionales. Está prohibido reducir la frecuencia por historial,
   reputación, anomalías, atestación o número de claves.
7. **Disputas**: solo mediante una prueba de discrepancia que cada nodo verifica por sí mismo (I8).
   La estrategia no se activa sin la regla de disputas falsas (D23, cálculo M9).
8. **Variante para claves con suma pequeña.** Donde la verificación frecuente es cara para el pagador, es admisible
   la lotería B: solo se paga la respuesta elegida por sorteo, y su pagador la verifica por completo (gpt1,
   claude2). En ella, el fallo honesto gratuito (D16) se mantiene sin cambios, pero los ingresos del ejecutor
   son irregulares y el pagador mantiene un prepago de `R/p`.

La estrategia exige cambiar D16 y D21 (sección 6). Todos los ceros de la garantía son condicionales: coincidencia de bits
en los dispositivos probados, no en cualesquiera; verificación puntual; vitalidad del registro y ausencia de
censura de la prueba; corrección del núcleo; ejecución honesta de la moneda por el programa del pagador;
regla de disputas falsas.

### 5.2. Precio

Parámetros: `p = R/(R + H)` con `H ≈ n_w·R` en régimen estable; `ρ` = 0,10 / 0,21 / 0,40 (lote 1);
`γ` = 1,5–1,8 (lote 1) y 2,5–2,8 (lote 8). Precio completo frente a Q8_0: `γ·(1 + p·ρ) − 1`.
Tabla del crítico Claude [cálculo]:

| `n_w` (tareas de la clave por ventana) | `p` estable | Verificación con `ρ` = 0,10 / 0,21 / 0,40 | Total frente a Q8_0, lote 1 | Total, lote 8 | Verificaciones en la primera ventana de una clave nueva |
|---|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5% … +82,3% | +152% … +186% | alrededor de 4,0 |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0% … +80,2% | +150% … +181% | alrededor de 6,3 |
| 4320 | 0,023% | 0,002% / 0,005% / 0,009% | +50,0% … +80,0% | +150% … +180% | alrededor de 9,0 |

Otros calendarios [cálculo]: con la frecuencia mínima por dinero `p ≈ t_task/t_lock ≈ 2,3·10⁻⁴`,
la verificación cuesta alrededor del 0,005% del trabajo (crítico DeepSeek); con la frecuencia con limitación del daño
`p ≈ 1/√n_w`, 0,18–0,72% con `n_w = 3000` y 0,56–2,2% con `n_w = 300`; con la lotería B y `p = 5%`,
0,5–2,0% con lote 1. Si a la regla monetaria se añade un suelo contra el daño según `H_ver`, la verificación
crece hasta 0,15–2,2% con `n_w` = 300–4320 y hasta 6,7% con `n_w = 30` (crítico Claude). La primera tarea
de un novato cuesta la verificación completa, 10–40% de su generación.
Para comparar: la verificación completa de cada respuesta (contrato principal de gpt1, gpt2, ds2) cuesta
`γ·(1 + ρ) − 1` = +65…+152% frente a Q8_0; con `γ = 1,65`, `ρ = 0,21`, +99,65% [cálculo].

No se han calculado: la escritura de 2–4 KB por cada respuesta en el registro, las disputas falsas (M9), la energía y la verificación
en dispositivos de los pagadores. **El cuello de botella de la referencia del 5% es la ralentización del perfil exacto, no la
verificación.** Pueden reducirlo núcleos rápidos con igualdad bit a bit y la decodificación especulativa exacta:
el borrador lo genera un Q8_0 rápido y el perfil exacto acepta el prefijo hasta la primera discrepancia.
Estimación de claude2 con una coincidencia del 99% de los tokens y bloque de 32: alrededor de 0,78 del tiempo del token exacto, es decir,
+28% sobre Q8_0 en lugar de +65%; con una coincidencia del 95%, 1,33 del tiempo del token exacto, peor que la generación directa
(crítico Claude) [cálculo; la coincidencia no está medida].

### 5.3. Riesgo residual

Ganancia esperada por falsificación; «daño» es la proporción de falsificaciones no detectadas del saboteador, todas
con la marca «no verificado». Resumen del crítico Claude y del crítico DeepSeek [cálculo].

| Caso | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Novato, `H = 0` |
|---|---|---|---|---|---|
| Dinero, el pagador verifica él mismo | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verificación siempre) |
| Respuesta falsa mostrada como «verificado» | 0 | 0 | 0 | 0 | 0 |
| Daño con `p = R/(R + H)`: no detectado tras `n_w` falsificaciones | alrededor del 50% | alrededor del 50% | alrededor del 50% | alrededor del 50% | 0 (los primeros se verifican) |
| Lo mismo con `p = 3R/(R + H)` | alrededor del 12,5% | igual | igual | igual | 0 |
| Pagador sin equipo encarga la verificación a una terna aleatoria | +0,001R | +0,027R | +0,125R | +R | igual |
| El pagador no verifica, el ejecutor lo distingue | hasta +R | hasta +R | hasta +R | hasta +R | 0 |
| Entrenamiento, hay un auditor honesto de frecuencia completa | ≤ 0 | ≤ 0 | ≤ 0 | — | `−c_f` |
| Entrenamiento, no hay auditor honesto | hasta +R | hasta +R | hasta +R | hasta +R | hasta +R |

Las filas «el pagador verifica él mismo» no dependen de `q`. Este es el resultado principal del consejo:
la verificación que no depende de la proporción de colusión es barata para el pagador si verifica por muestreo,
y la suma quemable del ejecutor está bloqueada hasta el final de la verificación.

### 5.4. Novato

Una clave con la cuenta vacía se verifica siempre, por lo que la falsificación en ella da `−c_f`. A medida que se acumula
la suma bloqueada, la frecuencia cae: con la regla `R/(R + H)`, en la primera ventana hay alrededor de 4,0 / 6,3 / 9,0 verificaciones
completas con `n_w` = 30 / 300 / 4320 (crítico Claude); con la regla `R/H`, 5,0 / 7,3 / 10,0
(claude1) [cálculo]. El precio de la primera ventana con `n_w = 30` es 1,7 / 3,5 / 6,6% con `ρ` = 0,10 / 0,21 / 0,40
(claude1) [cálculo]. El «precio de entrada» es trabajo útil verificado por completo, no una cuota de entrada.
La otra cara es la carga: una coalición de claves nuevas obliga a los pagadores a verificar cada
respuesta suya. Esto afecta al precio (R6), pero no a D1; hay que calcular la magnitud (sección 7).

### 5.5. Usuario sin equipo

La estrategia no lo protege. Si encarga la verificación a una terna aleatoria de nodos ajenos, la fuga esperada
es `R·q³`: 0,001R / 0,027R / 0,125R / R con `q` = 0,1 / 0,3 / 0,5 / 1 [cálculo]. Si la
encarga a su propio dispositivo o a un nodo conocido, es un supuesto suyo según D21; con la colusión del ayudante
y el ejecutor, una certificación falsa es posible con probabilidad 1. El crítico Claude propone comprobar
experimentalmente cuánto cuesta la verificación en una pasada en el procesador de un portátil y de un teléfono: con una frecuencia
de alrededor de una verificación por ventana de clave, una verificación lenta y poco frecuente puede resultar aceptable.
La garantía para ese usuario sigue siendo una cuestión abierta, D21.

### 5.6. Entrenamiento

Para el paso de entrenamiento, el consejo no encontró una garantía nueva. El paso no tiene un pagador cuyo dinero esté en juego,
por lo que la verificación por muestreo debe ejecutarla cada nodo que necesite la garantía, y el precio
se multiplica por el número de tales nodos. Variantes:

- **Repetición completa del paso** desde el padre aceptado: alrededor del 100% del trabajo del paso por cada nodo verificador.
  Ejemplo del crítico ChatGPT: si la inferencia es el 80% del trabajo base, `ρ = 0,21` y cada paso
  se repite una vez, resulta `0,8·0,21 + 0,2·1 = 36,8%` por encima del trabajo base [cálculo]; con `N`
  nodos que verifican por sí mismos, el segundo término se multiplica por `N`.
- **Verificación por muestreo del paso por todos los nodos completos** (claude2, S2): solo para el dinero, con una ventana
  de 3 días, 0,23% / 2,3% / 23% del trabajo de la red con 10 / 100 / 1000 nodos verificadores; con una limitación
  del daño del 10%, 10 veces más caro [cálculo; la columna de daño no se deduce con rigor]. Requiere entrenamiento exacto con aritmética entera,
  que no está construido ni medido.
- **Auditoría «uno honesto de N»** (claude1, S2): es un supuesto que la etapa 4 ya rechazó para
  el entrenamiento; sin auditoría pagada, el equilibrio es «no hay auditores».
- **Pago por una mejora demostrada (D18)**: no es verificación del paso; el cálculo M12 ya mostró que un
  duplicado exacto de la solicitud aumenta la asignación del propietario según las tres reglas de atribución (cálculo
  de miniagentes, resumen D5_RESULTS).

La agregación robusta de contribuciones (Krum, mediana, media truncada, de memoria) limita el daño
de la parte no detectada, pero no protege de saboteadores coordinados con una parte notable del peso y no cumple
D1. Un paso no verificado no debe entrar en la versión publicada del modelo (D6).

## 6. Decisiones que hay que cambiar o adoptar

Las formulaciones siguientes son **recomendaciones del consejo**, no decisiones adoptadas. Cada pregunta debe aceptarse
o rechazarse explícitamente. Los requisitos inmutables R1–R6 no cambian al editar una línea de la hoja de ruta
(recordatorio de gpt1).

**Pregunta 1 (D21, y también D11 y D2). ¿Permitir que el pagador pague con su prepago una respuesta
que su programa, según la regla del núcleo, no verificó?** Ahora D21 dice: «La red no paga una respuesta sin
verificación», y D11: «solo se paga lo verificado».
*Recomendación (crítico Claude, según los trabajos claude1 y claude2):* sí. Segunda frase propuesta para D21:
«El pagador paga con su prepago la respuesta que verificó o dejó pasar según la regla D7
con su moneda secreta; la respuesta omitida lleva la marca «no verificado». No hay emisión de créditos ni peso
por la petición pagada». Al mismo tiempo hay que precisar D11 (y, según la observación del crítico DeepSeek,
D2); de lo contrario, las enmiendas se contradicen.
*Donde discreparon:* el crítico DeepSeek: no cambiar D21 por ahora (la estrategia ya está bloqueada por D23)
y usar la lotería B (`α = 0`, pago de `R/p` al elegido), compatible con las D2, D11 y D21 actuales.
El crítico ChatGPT: dejar como contrato principal la verificación completa de cada respuesta por el pagador,
e introducir el pago de los elegidos de un lote mediante un contrato aparte; sin verificación propia no hay pago de la red.

**Pregunta 2 (D7). ¿Cómo escribir qué verificación es admisible para el pago?**
*Recomendación (crítico Claude):* «La verificación que no depende de la proporción de colusión es obligatoria para la marca
«verificado», para la emisión de créditos y para el peso. El pago de la petición con fondos del pagador se admite
tras la verificación por el pagador o tras omitir la verificación según la regla del núcleo: moneda secreta
del pagador, lanzada después de fijar la respuesta, probabilidad no inferior a `R_i/(R_i + H_lock)`.
Está prohibido reducir esta probabilidad por historial, reputación, anomalías, atestación o número de claves;
aumentarla está permitido. La verificación por verificadores asignados no sirve de base para el pago. D1
no se debilita a `q < q*`». Aparte hay que elegir `R/(R + H_lock)` (umbral exacto) o `R/H`
(con margen, número finito de falsificaciones del saboteador hasta la detección).
*Donde discreparon:* los críticos DeepSeek y ChatGPT proponen no cambiar el texto de D7 y añadir el ámbito
de aplicación: la garantía para la parte que ejecuta ella misma la verificación no depende de `q`; la parte
que delegó la verificación solo está protegida si la proporción de colusión de los asignados es inferior a `q*`, y esto se le
muestra (crítico DeepSeek). El crítico ChatGPT añade: la calificación, el quórum, la expiración del plazo
y el supuesto `q_eff < q*` no dan derecho a un estatus independiente.

**Pregunta 3 (D6). ¿Precisar las marcas del resultado?**
*Recomendación (común a los críticos, formulación según ds1):* «Una respuesta falsa no se entrega como
«verificado». Hay dos marcas: «verificado», verificación completa antes de mostrarse por un método que no depende de la proporción
de colusión (para una petición, por el pagador en persona o mediante una prueba aceptada por el núcleo); «no verificado»,
por defecto, se pone automáticamente y solo tal verificación puede retirarla. La entrega en flujo se hace
en bloques verificados o con esta marca. Un paso de entrenamiento no verificado no entra en la versión publicada
del modelo». El crítico ChatGPT precisa: un paso no verificado y sus descendientes solo pueden estar
en una rama de investigación aislada sin pago por la transición.
*Donde discreparon:* en esencia no discreparon; claude1 propuso una tercera marca, «verificado por muestreo»,
que rechazaron los tres críticos.

**Pregunta 4 (D16). ¿Qué hacer con un fallo de hardware honesto?** Ahora el fallo no se castiga y la suma
en espera no se quema. Con la verificación por muestreo y el pago de lo no verificado, esto es una fuga directa
(sección 4.6).
*Recomendación (críticos Claude y DeepSeek, según claude1):* «Con verificación completa o lotería B, un fallo honesto
no se castiga (regla anterior). Con verificación por muestreo y pago de lo no verificado, cualquier
discrepancia demostrada quema el `H_lock` de la clave independientemente de la causa, ya que por una salida errónea idéntica
no se puede establecer la causa. La pérdida esperada del honesto (alrededor de `P_f·R` por tarea, donde
`P_f` es la probabilidad de un fallo silencioso) la compensa un recargo incondicional con cargo a la recaudación de la red. La regla
se activa solo tras medir `P_f`».
*Donde discreparon:* el crítico ChatGPT: mantener la protección frente al fallo honesto: el fallo deja el resultado sin
pago, las recompensas anteriores se conservan, el número de fallos por clave es limitado y la fiabilidad del cálculo
no debe depender del descuento de recompensas anteriores. Señala además que el recargo con cargo a la recaudación ajena
por cada tarea aumenta el pago también a la falsificación y cambia el umbral. El crítico Claude añade: quemar
una ventana de ingresos por una inestabilidad no medida golpea a los nodos débiles (R6); el recargo compensa la media,
no el riesgo de ruina. La disputa se resuelve eligiendo la estructura de pago (la lotería B conserva D16; el pago
de lo no verificado, no) y midiendo `P_f`.

**Pregunta 5 (D8). ¿Cómo organizar el plazo y los derechos de disputa?**
*Recomendación (crítico Claude):* «El pagador presenta la prueba de discrepancia a más tardar en el plazo `δ`
de tiempo activo tras recibir la respuesta; la disputa se resuelve solo con una prueba que cada
nodo verifica por sí mismo». *Adición (crítico ChatGPT):* el ejecutor tiene derecho a exigir el cálculo
de su pedido fijado en caso de rechazo injustificado o silencio del comprador; ambas partes
disputan con la cuenta vacía y sin depósito; un duplicado no lanza una nueva verificación cara; hasta la decisión
la suma disputada permanece en espera. Aquí hay una bifurcación abierta: si se paga al vencer el plazo
sin objeción, la ausencia del pagador paga la falsificación; si se rechaza por silencio, un pagador deshonesto
obtiene gratis una respuesta correcta.
*Donde discreparon:* claude2 y el crítico DeepSeek proponen, tras M9, permitir la disputa a cualquier nodo sobre
una tarea elegida por el faro, con una cuota de disputas falsas; el crítico Claude lo considera vacío para una petición privada
(un nodo ajeno no tiene la petición) y útil solo para el entrenamiento.

**Pregunta 6 (D23). ¿Mantener el bloqueo hasta el cálculo M9?**
*Recomendación (los tres críticos):* mantenerlo. Complementar (crítico Claude): «M9 se calcula para la regla
D7: las disputas son raras en equilibrio, pero la coalición «pagador = ejecutor» puede presentarlas sin límite
por peticiones autopagadas; la suma quemada se destruye y al perjudicado se le devuelve
no más que su pago». El crítico ChatGPT propone escribir el criterio para levantar el bloqueo: cotas superiores
de bytes, cómputo, mensajes y plazos por caso, límite de casos abiertos simultáneamente,
fuente de cobertura de la carga, comprobación de formato y unicidad antes del recálculo caro, resistencia
a peticiones autopagadas, a la colusión de ambas partes, al rechazo falso del comprador, a la partición de la red
y a la indisponibilidad de los datos.

**Pregunta 7 (nueva D26). ¿Adoptar la decisión sobre el bloqueo de la suma en espera y el límite de devolución?**
*Recomendación (crítico Claude, con las correcciones de la sección 4):* «El `H_lock` de la tarea `i` son las recompensas no maduradas
de la clave que madurarán después del plazo máximo de disputa de `i`; el plazo de verificación por el pagador
es mucho menor que la ventana de maduración. Una discrepancia demostrada quema toda la suma no madurada de la clave, incluidas
las recompensas de tareas entregadas después de la disputada y en la misma ola. Al pagador perjudicado se le devuelve
no más que su pago por la respuesta disputada; el resto se destruye; la primera disputa no toma sumas
debidas a otros pagadores». Sin esta regla, la estrategia de las secciones 5.1–5.3 no se sostiene
(contraejemplos +4,4295R y hasta +74,4R en las secciones 4.2–4.3).
*Donde discreparon:* el crítico ChatGPT no discute el bloqueo en esta forma, ya que no apoya el pago
de lo no verificado; pero él mismo exige vincular de forma atómica las obligaciones abiertas con todos los ingresos no madurados.

**Pregunta 8 (D1). ¿Hay que cambiar D1?**
*Recomendación (los tres críticos):* no debilitar el texto. Las variantes «D1 con una proporción de colusión menor que `q*`»
y «fuga no mayor que `ε` del volumen de negocio» (claude1, ds1, ds2, gpt1) fueron rechazadas: con `q = 1` entregan
a la coalición toda la producción no verificada, contradicen D19 y el inmutable R4, y el «volumen de negocio» se infla
con autotratos. El crítico Claude propone una nota: para la respuesta del modelo, D1 se garantiza respecto
al pagador que ejecuta la verificación del núcleo; la verificación por muestreo con su moneda secreta cumple
D1 como esperanza y se registra con el supuesto de un adversario racional (según R4, el muestreo estadístico es
un supuesto); para un consumidor que no verifica, la red no promete D1. El crítico DeepSeek: una nota de que
la garantía D1 se refiere a cada resultado con la marca «verificado» y a cada emisión de créditos.

## 7. Qué calcular con miniagentes y qué comprobar experimentalmente

### 7.1. Cálculos exactos (fracciones, hash de control, repetición en un segundo dispositivo)

1. Búsqueda exhaustiva completa de la regla D7 con maduración de la suma, olas, varias claves, precios distintos
   en la ola y verificaciones retroactivas. Referencias: `κ = 1` → 0; `κ = 0,9` con `H₀ = 0` → +1,734R
   (reproducido por el crítico Claude, no reproducido por el crítico DeepSeek; la búsqueda exhaustiva debe decidirlo);
   `0,99·R/(R + H)` → +0,225R; contraejemplo de maduración +0,99R / +9,08R / +49,7R / +74,4R.
2. Fórmula de la ola de gpt1: +4,4295R con descuento separado y −2,49676R con la quema de toda la ola.
3. Ataque de «autodisputa»: con qué proporción de devolución al perjudicado la ganancia se vuelve positiva.
4. Fuga de fallos gratuitos (`b` por ventana) y recargo `P_f·R` con dispersión de las pérdidas del honesto.
5. Daño con los calendarios `H_lock`, `H_old`, `H_ver`, `m·R/(R + H)` con autopago y claves nuevas;
   referencias 0,50 / 0,125 / 0,0078 con `n_w = 4320`.
6. Pagadores perezosos: la proporción `λ` y la distinguibilidad con las que desaparece la disuasión.
7. Carga de una coalición de claves nuevas sobre los pagadores con `p = 1` para los novatos.
8. M9 (disputas falsas) para la regla D7: condición de D23.
9. Precio agregado `γ·(1 + p·ρ)` en una malla de `γ`, `ρ` medidos y de la distribución de `n_w`.
10. Probabilidad de colusión total en la elección sin reemplazo (`C(C,k)/C(N,k)`) y en las rondas de sorteo.
11. Tamaños de las instantáneas de estado según la configuración fijada del modelo (M1): disputa sobre el precio de los tokens
    y las instantáneas por muestreo.
12. Umbral corregido de ds2 y script de control de gpt2 (SHA-256 empieza por `58aec3b0`
    y termina en `cd07ba`; coincidió en los críticos Claude y DeepSeek).
13. Cadenas exactas de SPRT y CUSUM en mallas finitas, incluido el cambio de comportamiento tras un buen historial.
14. Tablas de trampas `(1 − g·θ·d)^m` para los niveles `10⁻³`, `10⁻⁹`, `2⁻⁸⁰`.

### 7.2. Solo experimentalmente

El experimento D5 permite trabajar con Qwen3.5-4B con aritmética entera en el alcance O1–O5 de su protocolo. **Todo lo demás requiere una autorización aparte del propietario.**

1. Dentro de D5: núcleos rápidos con igualdad bit a bit (O3, O4), el único camino para acercarse al 5%;
   proporción de verificación en dispositivos de los pagadores y con lotes 1, 8, 32; O5: calidad en 320 tareas.
2. Fuera de D5: decodificación especulativa exacta: distribución de la longitud del prefijo coincidente entre Q8_0
   y el perfil exacto en respuestas largas.
3. Fuera de D5: frecuencia de discrepancias silenciosas `P_f` en trabajo prolongado en dispositivos voluntarios, antes de
   cualquier cambio de D16.
4. Fuera de D5: tiempo y memoria de la verificación en una pasada en el procesador de un portátil y de un teléfono.
5. Coincidencia de bits en entradas límite (desbordamiento, empates, final temprano de la respuesta) y en controladores
   nuevos; en la RX 580, una pasada larga sobre una respuesta lista fue interrumpida por el controlador [medido].
6. Fuera de D5: O9 (energía), O6 (ruido de la mejora de LoRA), O7 (precio de la prueba de bloque), entrenamiento
   con aritmética entera: condición previa de cualquier esquema de verificación del paso.
7. Fuera de D5, opcional: hasta qué punto las falsificaciones baratas son distinguibles por rasgos. Esto no da garantía
   con ningún resultado, solo precisa el techo de la sección 2.1.

## 8. Discrepancias no resueltas y referencias dudosas

### 8.1. Discrepancias

1. **¿Cumple la verificación por muestreo del pagador el D1 literal?** claude1, claude2 y los críticos
   Claude y DeepSeek: sí para el dinero, no para el daño. ds1 y ds2: hace falta verificación completa (los críticos
   consideran que no advirtieron la verificación por el pagador con frecuencia según la suma bloqueada). gpt1, gpt2
   y el crítico ChatGPT: verificación completa de cada respuesta, y el pago de los elegidos solo mediante un contrato
   aparte para lotes. La decisión de si basta la ganancia esperada en la primera frase de R4 corresponde
   al propietario.
2. **`R/(R + H_lock)` o `R/H`.** Lo primero es exacto para el dinero; lo segundo da margen y un número esperado finito
   de falsificaciones hasta la detección; la diferencia de precio es de alrededor de dos veces con una suma pequeña.
3. **¿Pagar lo no verificado** (`α = R` o un G(α) suave en claude2) **o solo lo elegido**
   (`α = 0`, lotería B)? Depende de la enmienda de D2, D11, D21 y de la irregularidad no medida de los ingresos.
4. **Faro o moneda secreta.** claude2: faro común (D20); claude1 y los críticos Claude y DeepSeek:
   moneda secreta del pagador, el faro solo hace falta con `α < R` y para disputas de terceros nodos. Crítico
   ChatGPT: la moneda secreta sirve para la verificación personal, pero no puede disponer de un premio común;
   al elegir el conveniente de dos resultados independientes del faro, la detección cae de `p` a `p²`.
5. **D16**: sección 6, pregunta 4.
6. **Frontera del daño**: ningún esquema resistió el autopago y las claves nuevas.
7. **Entrenamiento**: auditoría «uno de N» (claude1), verificación por cada nodo completo con retroceso de la rama
   (claude2), D18 o repetición completa (ds1, ds2, gpt1, gpt2); ningún esquema cumple D7 con
   `q = 1`.
8. **Magnitudes de la búsqueda exhaustiva de claude1** (+1,73R con `κ = 0,9`): reproducidas por el crítico Claude,
   no reproducidas por el crítico DeepSeek (+0,085R en el modelo más cercano); el signo es el mismo en ambos.
9. **Decodificación especulativa:** 1,15–1,38 (claude1) frente a alrededor de 0,78 del tiempo del token exacto
   (claude2); ambas no medidas.
10. **Trampas:** ds2 calcula el número necesario de trampas; claude1 y claude2 demuestran que
    en una red pública la trampa coincide con la verificación por el pagador. Las conclusiones son compatibles.

### 8.2. Referencias bibliográficas señaladas por los críticos como dudosas

Todas las referencias se dan de memoria, sin cotejar los textos.

- SybilGuard y SybilRank bajo el «Yu y coautores» común (ds1): según la memoria de los críticos, SybilGuard y SybilLimit son
  de Yu y coautores (2006, 2008); SybilRank, de Cao y coautores (2012); el año de SybilRank en sí fue señalado
  por el crítico Claude como incierto.
- «Proof of Sampling (2024)» y «Verde (Gensyn, 2025)» (claude1, claude2): los propios trabajos escriben
  «no estoy seguro»; el funcionamiento del mecanismo no está confirmado.
- Peer Truth Serum como trabajo de Witkowski y Parkes (2012) (ds2): el crítico Claude lo considera
  dudoso (según su memoria, ellos tienen una «BTS robusta», y el nombre pertenece a Radanovic
  y Faltings); el crítico DeepSeek lo considera correcto. Discrepancia.
- DMI como trabajo de Kong y Schönbeck (2019) (ds1, ds2): dudoso según la memoria de los críticos Claude
  y ChatGPT (DMI es un trabajo de Kong de alrededor de 2020); el crítico DeepSeek considera correcta la atribución.
- «Ataques de autopredicción contra BTS en Radanovic y Faltings» (ds1): dudoso.
- «Gao, Wright y Leighton-Brown (2016)» sobre la superioridad de la verificación por muestreo frente a peer prediction
  (claude2): el año no está confirmado (crítico DeepSeek); la incondicionalidad de la conclusión es dudosa (crítico ChatGPT).
- Kreps y Wilson (1982) como base de «la reputación solo funciona con un horizonte largo» (claude1):
  dudoso (crítico ChatGPT).
- DetectGPT como justificación del umbral de perplejidad del modelo pequeño (ds1): incorrecto, estudia otra
  propiedad (crítico ChatGPT).
- La fórmula general de paso `(1 − f)^s` como propiedad de BOINC, TrueBit y opML (ds1, ds2): no se sigue de sus
  protocolos.
- Las referencias de ds1 y ds2 a «0,3–0,7% / 0,33–0,66% de los tokens del examen» y «alrededor de 2,4 horas por candidato»
  no se encontraron en los documentos de entrada.

## 9. Quién hizo qué

El consejo de modelos trabajó con los materiales del proyecto, sin acceso a la red y sin experimentos.

- **Seis trabajos independientes:** dos trabajos de ChatGPT (gpt1, gpt2), dos de DeepSeek (ds1, ds2)
  y dos de Claude (claude1, claude2). Cada uno analizó siete direcciones del encargo, añadió
  las suyas, las cotejó con las decisiones D1, D6 y D7 y propuso estrategias con precio y riesgo residual.
  Los programas aritméticos cortos y las pequeñas búsquedas exhaustivas los ejecutaron claude1 (búsqueda de estrategias
  contra la regla de frecuencia), claude2 (malla de fracciones exactas), gpt1 y gpt2 (gpt2 adjuntó un script de control
  con hash).
- **Tres críticas:** una de ChatGPT, una de DeepSeek y una de Claude. Cada crítico leyó los seis trabajos,
  buscó errores y contraejemplos y recalculó las cifras clave. Los críticos Claude y DeepSeek repitieron
  el script de control de gpt2 y el hash coincidió; el crítico Claude repitió la búsqueda exhaustiva de claude1; el crítico DeepSeek
  no reprodujo sus magnitudes.
- **Consolidación:** este documento lo compuso Claude a partir de los trabajos y las críticas. No se añadieron
  estimaciones ni cifras nuevas más allá de los trabajos, las críticas y las mediciones de D5; donde los críticos discreparon, se indica.
