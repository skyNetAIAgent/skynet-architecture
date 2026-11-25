<!-- translation of docs/HIDDEN_DETECTOR.md, source sha256: a695d12d2972002373f749a618c390c3e937e344afd1e816d8c46319fe1127cb -->

# El detector oculto y cambiante: qué aporta el secreto de las reglas

[English](../../docs/HIDDEN_DETECTOR.en.md) · [中文](../zh/HIDDEN_DETECTOR.md) · **Español** · [Français](../fr/HIDDEN_DETECTOR.md) · [Deutsch](../de/HIDDEN_DETECTOR.md) · [Italiano](../it/HIDDEN_DETECTOR.md) · [Русский](../../docs/HIDDEN_DETECTOR.md) · [Português](../pt/HIDDEN_DETECTOR.md) · [العربية](../ar/HIDDEN_DETECTOR.md)

Estado a 25 de noviembre de 2026. Resultado del sexto consejo de modelos.

## 1. Pregunta y resumen breve

El propietario del proyecto preguntó literalmente:

> «Con reglas abiertas (D4), el defraudador conoce el detector y falsifica exactamente donde este
> está tranquilo. ¿Y si ocultamos el detector? Por ejemplo, que la red genere de forma aleatoria, en momentos
> aleatorios, nuevas reglas de verificación de la honestidad, y que los agentes verifiquen según ellas. Dada
> la arquitectura distribuida y abierta de la red skynet, las reglas de verificación no debe conocerlas nadie y
> deben cifrarse, y la clave del cifrado debe cambiar. Pensadlo con un consejo de modelos en esta dirección. Antes ya
> planteé la cuestión del uso de blockchain: ¿hay una variante de hacer un detector dinámico basado
> en blockchain? ¿Quizá existen otras tecnologías o algoritmos además de blockchain?»

**Estado del documento.** Es un razonamiento y un cálculo, no una medición. La red no estaba en marcha durante el consejo,
no se realizaron experimentos; los trabajos científicos se citan de memoria y no se cotejaron. Las mediciones se toman solo
de los resultados del experimento D5 a 25 de noviembre ([EXPERIMENT_D5](EXPERIMENT_D5.md), sección 7) y del compendio anterior
[STRATEGY_SEARCH](STRATEGY_SEARCH.md). Las únicas decisiones adoptadas del proyecto siguen siendo D1–D25
([ROADMAP](ROADMAP.md)); todo lo que abajo se llama «recomendación» el propietario debe aceptarlo o
rechazarlo explícitamente. Marcas: [medido] — medido en D5; [cálculo] — se sigue de una fórmula con los parámetros
nombrados; [suposición] — valor tomado para la estimación y no medido.

Notación que aparece abajo: `R` — pago de una tarea; `H_lock` — suma no madurada
del ejecutor, que se quema ante una falsificación demostrada; `c_f` — costes de la falsificación; `p` —
probabilidad de verificación completa de la tarea; `ρ` — tiempo de verificación de una respuesta lista en una pasada,
dividido por el tiempo de generación; `γ` — cuántas veces más lento es el perfil exacto de enteros que la generación
normal de llama.cpp Q8_0; `q` — proporción de colusión; `n_w` — número de tareas de la clave por ventana de maduración.

**Resumen breve.**

1. **Un detector oculto no aporta más que una verificación abierta con aleatoriedad secreta del mismo precio.**
   Si el defraudador conoce la ley por la que se eligen las reglas (y según D4 el código del agente es abierto, luego
   la conoce), la probabilidad de detectar cualquier falsificación suya con una regla oculta es igual a la
   probabilidad de detección con un programa abierto «tras fijar la respuesta, lanzar una moneda y aplicar
   la regla que salga». A esta conclusión llegaron de forma independiente los once trabajos, y los cuatro críticos lo
   confirmaron. Por tanto, el ocultamiento no permite bajar la frecuencia de verificación por debajo del umbral anterior
   `R/(R + H_lock)`.
2. **Una regla que vive más que una tarea es peor que una moneda fresca.** El defraudador aprende de sus
   resultados («pillado / no pillado»), prueba el detector con claves nuevas gratuitas y conoce la regla a través
   de cualquier cómplice al que se la dieron para aplicar. Incluso sin ninguna fuga, una regla común para la época
   es más peligrosa: en el ejemplo de ChatGPT, una ola de diez falsificaciones da `+8,1R` frente a `−2,38R` con
   monedas independientes [cálculo]. Por eso «cambiar las reglas en momentos aleatorios» es peor que cambiar
   la elección en cada tarea.
3. **Es útil exactamente una forma de ocultamiento:** el secreto de la elección aleatoria *antes* de que el ejecutor
   fije irrevocablemente la respuesta, y el secreto del *papel*: si verifica este pagador y quién
   está asignado como verificador. Las reglas, la familia de verificaciones y la ley de elección siguen abiertas. Esta
   forma ya está en la estrategia del consejo anterior («moneda secreta del pagador»).
4. **Qué tomar de la blockchain y de la criptografía.** La blockchain es un registro de fijaciones, orden, revelaciones y
   quema de sumas; secretos no hay ni puede haber en ella. Un faro umbral externo de aleatoriedad y
   el retraso VDF desde el bloque final son fuentes de aleatoriedad para las muestras comunes según D20 (auditoría
   del entrenamiento, examen, asignación de verificadores), mezcladas con hash. VRF y el compromiso sobre la sal antes de
   la fijación, allí donde el resultado de la moneda afecta al dinero ajeno. Un «detector dinámico en blockchain»
   en la forma correcta es un **generador abierto de reglas en el núcleo más aleatoriedad fresca después de la
   fijación**, y no reglas cifradas.
5. **Qué rechazar como fundamento de la garantía.** El almacenamiento umbral de reglas secretas por los participantes
   (se revela o se bloquea con la colusión; con `q = 1` no hay protección: violación de D7),
   los entornos de ejecución de confianza TEE (confianza en el fabricante; en las tarjetas del experimento D5 no los hay),
   el cifrado homomórfico FHE (según la estimación de los críticos, de 19 horas a 15 días de cálculo por
   respuesta), la computación multiparte MPC (cientos de megabytes o más de tráfico por token y de nuevo
   dependencia de `q`), la ofuscación indistinguible iO (poco práctica y aun así deja al defraudador
   un «ensayo» de su falsificación), el cifrado funcional y PIR (resuelven otros problemas). Las trampas, los umbrales
   secretos y la estadística solo son admisibles como señal para una verificación *adicional*.
6. **Se ha encontrado un error en tablas anteriores.** En STRATEGY_SEARCH 5.3 y en la mayoría de los trabajos de este
   consejo, la celda «pagador perezoso, el ejecutor lo distingue» × «novato» contiene 0. Lo correcto es
   **hasta `+R`**: la regla «al novato se le verifica siempre» la ejecuta el programa del pagador, y un pagador
   perezoso no la ejecuta. Peor aún, las claves nuevas permiten averiguar gratis qué
   pagador es perezoso. Solo protege de ello la no vinculabilidad de los pagadores entre peticiones,
   y aún hay que construirla.
7. **El consejo no propone nuevas decisiones sobre la garantía.** Se proponen una precisión de D4 («el núcleo acepta
   aleatoriedad futura, pero no un secreto de larga vida») y una precisión de D20 («las fuentes se mezclan con hash,
   no por elección; el faro es para las decisiones comunes, no para el dinero del pagador»). El precio de la verificación no
   cambia por el ocultamiento: el capítulo principal sigue siendo la ralentización del perfil exacto `γ`
   (+50…+82% frente a Q8_0 con lote 1 [medido γ, cálculo]), y no la verificación misma.

---

## 2. Por qué el secreto de las reglas no ayuda: afirmaciones y contraejemplos

### 2.1. Una regla oculta equivale a una regla abierta con moneda secreta

**Modelo.** El defensor elige una regla de verificación `r` de una distribución `D`. La regla `r` detecta
la falsificación `x` con probabilidad `π_r(x)`. El defraudador conoce la distribución `D` (según D4, el generador de reglas
forma parte del núcleo abierto), pero no conoce el `r` que salió, y elige la falsificación antes de que
salga `r`.

**Afirmación 1 (equivalencia).** La probabilidad de detectar la falsificación `x` es
`π̄(x) = E_{r~D}[π_r(x)]`, y el precio medio de la verificación es el precio medio de las reglas. El programa abierto
«tras la fijación irrevocable de la respuesta, tomar aleatoriedad fresca, elegir `r` según la ley `D`
y aplicarla» da para **cada** falsificación la misma probabilidad de detección y el mismo precio. Por tanto,
el ocultamiento de la implementación añade cero a la protección.

La demostración es un promedio sobre `r`: los resultados de los dos experimentos coinciden para cada valor de
la aleatoriedad. La realizaron de forma independiente gpt1, gpt2, ds1, ds2, claude1, claude2, mm1–mm5; los críticos
ChatGPT, DeepSeek, Claude y MiniMax lo confirmaron. Es el mismo resultado que la cota del consejo anterior
`E_F[π] − E_P[π] ≤ TV(F, P)` ([STRATEGY_SEARCH](STRATEGY_SEARCH.md), sección 2.1): la magnitud
`π̄` es una función normal de las observaciones con valores de 0 a 1, y el secreto no la cambia.

**Afirmación 2 (la información sobre el secreto solo perjudica al defensor).** Si el defraudador, antes de falsificar, recibe
cualquier señal `Z` sobre la regla que salió — por una disputa anterior, por una prueba, a través de una parte de la clave, por una fuga
del enclave —, su mejor resultado no empeora: `E_Z[min_x E[π_r(x) | Z]] ≤ min_x π̄(x)`. Siempre
puede ignorar la señal (claude1, claude2; confirmado por los críticos).

El crítico ChatGPT precisó el límite de esta afirmación: la desigualdad es no estricta. Si todas las reglas tienen
la misma falsificación «peor para el defensor», revelar la regla puede no cambiar nada. Por eso la frase
de claude1 «cualquier fuga empeora estrictamente» es incorrecta; lo correcto es «nunca mejora».

**En qué se diferencia de la aleatorización.** Varios trabajos (ds1, ds2, mm2) escribieron la consecuencia como
«un detector oculto equivale a verificar toda la respuesta con probabilidad `p`». Eso es impreciso. El equivalente
de un detector oculto es una *mezcla de las mismas reglas*. Una mezcla de verificaciones parciales a veces es más fuerte que una verificación
completa del mismo precio, pero la ganancia la da la aleatorización, no el secreto, y se conserva con un algoritmo
abierto:

- **Contraejemplo de gpt1.** El resultado tiene tres partes verificables de forma independiente y del mismo precio, y por la estructura
  de la tarea cualquier falsificación admisible estropea al menos dos. Verificar una parte aleatoria por un tercio
  del precio completo detecta no menos de 2/3 de las falsificaciones; el recálculo completo con probabilidad 1/3 detecta solo 1/3.
- **Variante de gpt2.** Tres pruebas a la mitad del precio del recálculo completo, cada una detecta dos clases de error
  de tres: la mezcla detecta 2/3, el recálculo completo de la mitad de las tareas, 1/2. Si se añade una cuarta clase
  que no detecta ninguna prueba, la garantía de la mezcla cae a 0.

Para Qwen no está demostrada tal cobertura de clases de error: una sola posición incorrecta de la respuesta ya es una
falsificación, y para ella cualquier verificación parcial detecta no más que su propia proporción. Por eso la ganancia
práctica de la mezcla es ahora nula (críticos Claude y ChatGPT). La afirmación de mm2 «la mezcla siempre es más cara
que el tipo decisorio» es falsa en general; además, en su fórmula sobra un factor (los números 0,2111 / 0,22
/ 0,2333 están calculados con la fórmula correcta, pero está escrita la incorrecta: críticos Claude y DeepSeek).

**Dónde el secreto no se reduce a una moneda.** Es una marca privada del defensor, ligada a la respuesta correcta:
el patrón de referencia de una trampa, que solo conoce el pagador (gpt1, gpt2). No se puede sustituir por un bit aleatorio.
Pero, como se muestra en la sección 3, cuesta no menos de una generación y por eso no abarata la verificación.

**Frente a una regla «fija», la oculta es ciertamente mejor.** claude1 pone un ejemplo: si la regla abierta siempre mira
las posiciones 1–8, una falsificación en la posición 9 no se detecta nunca. Pero la misma ganancia la da una regla abierta
«elegir 8 posiciones uniformemente después de la fijación» (mm3, teorema 2: una posición fresca detecta `e/N` falsificaciones,
donde `e` es el número de posiciones estropeadas de `N`, independientemente de si el defraudador conoce la regla).
El crítico MiniMax lo llamó el principal error de la ronda: muchos trabajos compararon el detector oculto con una regla
abierta fija y atribuyeron al secreto una ganancia que pertenece a la aleatoriedad.

### 2.2. El aprendizaje del defraudador por los resultados y las pruebas con claves nuevas

Un secreto que se usa más de una vez se aprende. Para ello el adversario no necesita conocer la regla
entera: basta con encontrar un lugar seguro.

- **Dos posiciones de diez (claude1).** La regla oculta verifica 2 posiciones de 10; la detección de una falsificación
  de una sola posición es 1/5. Después de que una disputa revele una posición verificable, la detección cae a 1/9;
  tras revelarse la segunda, a 0. Si la regla se revela con la primera disputa, el número esperado de falsificaciones detectadas
  de cada 100 es `1 − 0,8¹⁰⁰ = 0,9999999998`, es decir, prácticamente una, mientras que una moneda fresca habría detectado
  de media 20 [cálculo, confirmado por los críticos]. El crítico ChatGPT señaló que esto es cierto para un orden concreto
  de pruebas y una revelación completa en la primera detección; en el caso general, una disputa revela al menos
  la posición verificada, pero no necesariamente todo el conjunto.
- **Ocho posiciones de mil (ds2).** Con un subconjunto oculto fijo de 8 posiciones de 1000, la primera falsificación
  de una sola posición pasa con probabilidad 0,992, igual que con una muestra pública fresca de la misma proporción.
  La diferencia es que, con un subconjunto oculto fijo, la posición que pasó sigue siendo segura para siempre. La cifra
  de ds2 «≈ 2718 intentos para reconstruir todo el conjunto» está calculada con un modelo incorrecto (con reemplazo);
  sin reemplazo hacen falta unos 890 intentos y, sobre todo, al adversario le basta una posición segura (críticos Claude,
  DeepSeek y ChatGPT).
- **Regla de época y clave madura (claude2).** Una regla determinista por época de 100 tareas,
  `p = 1%`, `H_lock = 99R`: el defraudador que ha encontrado mediante pruebas una zona segura recibe alrededor de
  `0,99·100R − 0,01·99R = 98,01R` por época frente a `≤ 0` con moneda fresca [cálculo, confirmado].
- **Bit común de época (gpt2).** `R = 1`, bloqueado `9R`, diez falsificaciones de una misma ola, la primera falsificación demostrada
  anula la ola y los `9R`, frecuencia de verificación de una petición individual 1/10. Si un solo bit oculto
  de la época decide «verificar todo» o «saltar todo», la ganancia de la ola es `0,9·10R − 0,1·9R = +8,1R`:
  violación de D1 **antes de cualquier fuga**. Con diez monedas independientes y los mismos costes,
  `(0,9¹⁰·10 − (1 − 0,9¹⁰)·9)R = −2,3751096381R` [cálculo, repetido por todos los críticos].
  Análogamente en el crítico ChatGPT: con `R = 1`, `H = 4`, `p = 0,2` y diez falsificaciones, una moneda común
  para toda la ola da `+7,2R` incluso anulando toda la ola.

**Claves Sybil.** Las claves nuevas son gratuitas. Una clave con la cuenta vacía no pierde nada al ser detectada, por lo que
las pruebas del detector con ella casi no cuestan nada. La protección se sostiene solo donde al novato
se le verifica realmente siempre (`p = 1`). El crítico ChatGPT advirtió que de la gratuidad de las claves no
se sigue que la adaptación sea instantánea: cada resultado informativo requiere una tarea pagada y
tiempo, y con retroalimentación ruidosa, varios intentos. La conclusión no cambia: un secreto
que dura mucho tarde o temprano se aprende, y una moneda fresca no enseña nada, porque el siguiente
lanzamiento es independiente de los anteriores.

**Conclusión.** La elección debe hacerse de nuevo para cada tarea, no según un calendario. Precisamente por eso
«la red genera nuevas reglas en momentos aleatorios» es peor que «una moneda fresca en cada tarea»,
que se regenera sola y gratis (ds1).

### 2.3. La regla se filtra a través de quienes la aplican

«Una regla que nadie conoce pero que todos ejecutan» es imposible en una red abierta. El nodo que
aplica la regla la conoce en el momento de aplicarla: el código y las claves están en la memoria de la máquina, y el propietario
de la máquina, según el modelo de adversario, puede leerlos ([THREAT_MODEL](THREAT_MODEL.md), sección 1.3).
claude1 formuló la lista completa de portadores del secreto:

1. la regla aún no existe: se derivará de aleatoriedad futura (faro, VDF);
2. la regla se ejecuta en hardware que el propietario no puede abrir (TEE): entonces la confianza
   se traslada al fabricante, y R4 lo llama suposición;
3. la regla está cifrada de modo que puede ejecutarse sin conocerla (iO, FHE, MPC): véase la sección 3;
4. la regla la conoce un comité de participantes: entonces la colusión la revela o la bloquea.

El crítico ChatGPT completó la lista: la MPC sobre partes y el cálculo de un esquema abierto sobre un
parámetro cifrado permiten al operador no ver el resultado en absoluto. Esto no cambia la conclusión, porque
tales esquemas vuelven a apoyarse en una proporción de participantes honestos o en el titular de la clave.

**Una clave umbral protege el almacenamiento, pero no la aplicación** (claude2, el argumento más fuerte del consejo contra
una regla secreta en un comité). Aunque la clave esté dividida de forma fiable, la regla de época descifrada
la ejecuta un nodo concreto. Con `m` aplicaciones independientes, la probabilidad de que al menos un
nodo aplicador sea de la coalición es `1 − (1 − q)^m`: para 10 aplicaciones es 0,65 / 0,97 / 0,999 con
`q` = 0,1 / 0,3 / 0,5. La probabilidad de que la regla de época *no* sea conocida por la coalición en 100 aplicaciones con
`q = 0,1` es `0,9¹⁰⁰ ≈ 2,7·10⁻⁵` [cálculo, confirmado].

**Ocultar algo al verificador carece de sentido** (claude2, corolario 4.2). Un verificador coludido puede
no verificar nada y decir «limpio»; al honesto no hay nada que ocultarle. El único al que hay que ocultar la decisión
es al ejecutor antes de la fijación de la respuesta. claude2 añadió el teorema 4: si el verificador no
debe saber qué posiciones verifica, tiene que «tocar» todas las posiciones y la economía del muestreo desaparece.
El crítico ChatGPT señaló que esta conclusión es válida en un modelo especial (un servidor,
sin preprocesamiento) y que con otros modelos de acceso a memoria puede cambiar;
el crítico Claude, que el teorema refuta una variante que nadie defendía.

**Un secreto oculto no da un veredicto verificable.** mm2 observó que la afirmación «existe una regla secreta
que aceptó el resultado» siempre es cierta para la regla «aceptar todo». Los críticos Claude y
ChatGPT precisaron: una prueba de conocimiento cero puede certificar una afirmación sustancial «la regla se derivó de un compromiso
registrado antes de la fijación, y aceptó el resultado». Pero tal prueba requiere una relación abierta en el núcleo, es decir, nos devuelve
al generador abierto, y su precio para Qwen no está calculado.

### 2.4. Clave umbral con una proporción de colusión q

Supongamos que la clave está dividida entre `n` titulares y que para descifrarla hacen falta `t` partes. Entonces la coalición conoce
el secreto antes de tiempo si tiene `t` o más puestos, y puede detener el funcionamiento si tiene `n − t + 1`
o más puestos. Si los puestos se eligen de forma independiente y cada uno pertenece a la coalición con probabilidad `q`,
se trata de colas binomiales. Tabla del crítico Claude, cotejada por los críticos ChatGPT y DeepSeek;
en cada celda, «revelación / parada» [cálculo]:

| `n`, `t` | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` |
|---|---|---|---|---|
| 5, 3 | 0,856% / 0,856% | 16,3% / 16,3% | 50% / 50% | 1 / 1 |
| 7, 5 | 0,0177% / 2,57% | 2,88% / 35,3% | 22,7% / 77,3% | 1 / 1 |
| 16, 11 | 2,7·10⁻⁸ / 0,33% | 0,157% / 34,0% | 10,5% / 89,5% | 1 / 1 |
| 30, 16 | 3,66·10⁻⁹ / 3,56·10⁻⁸ | 0,637% / 1,69% | 42,8% / 57,2% | 1 / 1 |
| 64, 43 | 4,75·10⁻²⁸ / 1,20·10⁻⁷ | 9,43·10⁻¹⁰ / 26,2% | 0,41% / 99,6% | 1 / 1 |
| 100, 51 | 6,3·10⁻²⁵ / 5,8·10⁻²⁴ | 9,0·10⁻⁶ / 2,2·10⁻⁵ | 46,0% / 54,0% | 1 / 1 |
| 100, 67 | 9,6·10⁻⁴³ / 7,0·10⁻¹¹ | 2,7·10⁻¹⁴ / 22,1% | 0,044% / ≈1 | 1 / 1 |

Qué se sigue de ella:

1. **Ninguna fila da protección con `q = 1`.** D7 exige una verificación independiente de la proporción de
   colusión, por lo que el secreto en un comité no cumple D7 con ningún umbral.
2. **Un umbral alto guarda bien el secreto, pero se bloquea con facilidad.** Fila 16/11: con `q = 0,3`
   la revelación es del 0,157%, pero con probabilidad del 34% la coalición detiene la emisión simplemente no enviando
   sus partes.
3. **Las épocas se acumulan.** Con una probabilidad de revelación del 0,856% por época (3 de 5, `q = 0,1`), en
   30 épocas independientes al menos una revelación ocurrirá con probabilidad del 22,7% (gpt1) [cálculo].
4. **La tabla es optimista.** La elección independiente de puestos es una suposición. Falla si los titulares
   se seleccionan por peso, y el peso puede acumularse con peticiones verificadas autopagadas; si en un modelo poco frecuente
   la proporción de colusión es mayor que la media; si hay soborno después de la asignación; si los puestos tienen propietarios comunes.
   En [THREAT_MODEL](THREAT_MODEL.md) (sección 1.7) ya hay un ejemplo: el 42,1% del peso total da
   `q_eff = 88,9%` entre los admitidos a la tarea (lo señaló el crítico MiniMax).
5. **Errores en los trabajos.** claude1 registró la condición «`q < min(t/n, 1 − t/n) ≤ 1/2`» como teorema; esto
   no es un teorema: con `t = n` el secreto se mantiene mientras haya al menos un honesto en el comité, y el bloqueo
   puede tener una salida de reserva segura (crítico Claude). mm4 confundió los umbrales de revelación y de bloqueo;
   mm2 creía erróneamente que el descifrado umbral requiere a todos los titulares; ds1 registró de forma contradictoria
   «se reconstruye con `t + 1` partes». La afirmación de mm3 «con `q ≥ t` la coalición falsifica
   la regla» es cierta solo donde el veredicto es una firma umbral sin contenido verificable; si
   se descifra un criptograma fijado de antemano, la coalición conoce la regla, pero no puede sustituirla.

**Cómo leer los requisitos R2/R3.** ds1, mm1, mm3 y mm4 escribieron que el requisito de recuperación tras una
parada total «prohíbe por principio» los secretos comunes. Los críticos Claude y ChatGPT lo consideran excesivo:
las partes de los titulares pueden sobrevivir a la parada en sus discos; R2/R3 prohíben depender de la dirección
de un coordinador vivo, no del regreso de una parte de los participantes. La frontera exacta (claude2):
un secreto sin el cual no puede verificarse el fundamento de una decisión **pasada** es incompatible con la verificabilidad
tras el reinicio. Por tanto, cualquier regla secreta debe revelarse no más tarde del pago, y su secreto
no vive más que el secreto de la moneda. La conclusión sobre la inutilidad de las reglas secretas es la misma; el fundamento de ds1, mm1 y
mm3 estaba exagerado.

### 2.5. El principio de Kerckhoffs, los juegos de seguridad, los bancos y CAPTCHA

**Kerckhoffs.** El principio de Kerckhoffs (de memoria) admite un algoritmo abierto con clave cerrada.
En este juego, la «clave» cerrada debe ser la realización impredecible antes de la fijación de la llamada
de verificación, y no el algoritmo. Cambiar una clave de larga vida es útil tras un compromiso, pero no borra
lo que el defraudador ya ha aprendido sobre la función que esa clave descifraba (crítico ChatGPT).

**Juegos de seguridad.** El defensor con presupuesto limitado aleatoriza: es la clásica teoría de los juegos
de Stackelberg y de inspección (de memoria). Pero allí la distribución del defensor suele considerarse
conocida por el atacante, y todo el beneficio viene de la aleatoriedad, no del secreto de la distribución. El crítico
DeepSeek corrigió a mm3: el desconocimiento por el defraudador de la distribución no puede elevar su ganancia por encima de la mejor
respuesta a la distribución verdadera, y según D4 está obligado a conocer esa distribución de todos modos. Para la mezcla
de distintas pruebas, gpt1 escribió un problema de programación lineal: maximizar la menor probabilidad de detección
entre las falsificaciones `min_f Σ w_j D(j,f)` con el presupuesto `Σ w_j c_j ≤ B`.

**«Blanco móvil».** La idea de moving target defense (de memoria) es valiosa cuando el observador
necesita tiempo para adaptarse a una nueva configuración. En SkyNet el mejor «blanco móvil» es
una nueva configuración en cada tarea, es decir, una moneda fresca (mm4, mm5).

**Por qué el ocultamiento funciona en un banco y en CAPTCHA, pero no en SkyNet.** Los trabajos y los críticos coincidieron en
las siguientes diferencias (claude2, ds2, mm3, mm5, crítico ChatGPT):

| | Antifraude bancario, CAPTCHA | SkyNet |
|---|---|---|
| Quién posee el modelo de verificación | Una organización en su propio servidor | No hay centro; el código del agente es abierto (D4) |
| Retroalimentación al atacante | A menudo no atribuible y con retraso | El resultado se ve de inmediato y está ligado a la tarea |
| Coste del intento | Abrir una cuenta, documentos, limitación de repeticiones | La clave es gratuita (Sybil) |
| Sanciones | No monetarias: bloqueo, juicio, información externa | Solo la quema de la suma no madurada (R5) |
| Objetivo de la protección | Reducir las pérdidas en promedio | La ganancia esperada de cualquier coalición no es mayor que cero (D1) |
| Verificabilidad de la decisión | No se exige a terceros | Cada nodo verifica el fundamento por sí mismo |

El banco tiene marcas privadas de los resultados, un coste de apertura de cuenta y limitación de repeticiones; CAPTCHA tiene
un verificador externo. Son información adicional y costes para el atacante. No aparecen en SkyNet por cambiar
un archivo cifrado de reglas. ds2 y mm5 nombraron la esencia con precisión: donde el ocultamiento funciona, el secreto es
en la práctica de un solo uso, es decir, es la misma moneda.

**La premisa principal de la pregunta en SkyNet es en parte falsa** (mm3). La verificación principal del proyecto es la comparación
bit a bit con el recálculo exacto. No tiene «lugares donde el detector está tranquilo»: la respuesta honesta coincide
en todas partes, la falsificación diverge donde ha sido falsificada. Las «zonas silenciosas» solo existen en los detectores
estadísticos y en las verificaciones parciales. Los detectores estadísticos contra la falsificación principal (generación normal
Q8_0 en lugar del perfil exacto) son casi inútiles, y para las verificaciones parciales ayuda una elección fresca
después de la fijación.

---

## 3. Análisis de las tecnologías

Los precios de abajo son [cálculo] según parámetros nombrados explícitamente y [suposición] sobre la velocidad de la criptografía estimada de memoria;
ninguna de estas tecnologías se ha medido en el proyecto. Mediciones de base: `ρ = 0,10–0,40` con lote 1
y `0,26–0,64` con lote 8; `γ = 1,5–1,8` con lote 1 y `2,5–2,8` con lote 8 [medido, O3 y O4].
Modelo D5: 32 bloques, tamaño oculto 2560, MLP 9216, 24 bloques Gated DeltaNet con estado
`32×128×128`, vocabulario 248 320, alrededor de 4,2·10⁹ multiplicaciones-sumas por token.

| Tecnología | Qué aporta | Qué no aporta | Precio [cálculo / suposición] | Veredicto |
|---|---|---|---|---|
| **Registro blockchain** | Orden, fijación final de la respuesta (D24, 2–4 KB de criptograma), compromisos, revelaciones, cálculo único, quema | Confidencialidad: todo el mundo ve lo que hay en el bloque. Aleatoriedad no sesgable: el productor del bloque puede retener un bloque inconveniente (H13) | Disputa piloto: 93 transacciones, 5,8–6,3 millones de gas; con 1 gwei y 3000 $/ETH, 17,4–18,9 $; con 20 gwei, 348–378 $ (crítico ChatGPT según THREAT_MODEL, H3) | **Adoptar como registro** |
| **Contrato inteligente como detector** | Cálculo automático sobre un fundamento ya verificado | Ni almacenamiento de secretos ni cálculo del modelo | Recálculo de un token dentro del contrato: `4,2·10⁹ × 3 gas ≈ 1,26·10¹⁰ gas` ≈ 37 800 $ por token con 1 gwei y 3000 $/ETH (ds1, confirmado). Crítico Claude: son unos 420 bloques de 30 millones de gas (límite de memoria). Crítico ChatGPT: una operación MUL simple cuesta, de memoria, 5 gas, así que esto es un escenario y no una cota inferior estricta | **Rechazar como detector** |
| **Faro umbral externo** (clase drand, de memoria) | Aleatoriedad pública que nadie conoce de antemano, si es honesto el umbral de su comité | Secreto: la ronda se publica para todos. Una coalición dentro del comité del faro conoce la ronda antes o puede no emitirla | Cientos de bytes por ronda y por lote, y la espera de una ronda (de memoria, 30 s en la cadena principal y unos 3 s en una rápida) | **Adoptar como una de las dos fuentes de D20** para las muestras comunes |
| **VDF desde el bloque final** | Retraso con el que el productor del bloque no llega a preparar un bloque conveniente | Entropía independiente: un VDF del mismo bloque no es una segunda fuente independiente (crítico ChatGPT) | Trabajo secuencial del computador; la verificación es rápida | **Adoptar como complemento del faro**, y registrar la suposición sobre la superioridad del hardware rápido |
| **Cifrado timelock mediante el faro** | Revelación aplazada de patrones de referencia comunes y de tareas del examen | Secreto más allá de la ronda; hereda el umbral del faro | Como el del faro | **Solo para la revelación aplazada de datos comunes**; no revelar así datos privados |
| **Rompecabezas con bloqueo temporal** (Rivest–Shamir–Wagner, de memoria) | Retraso de la revelación | El creador conoce la respuesta de inmediato; la moneda es más simple | Trabajo secuencial | **Rechazar** |
| **VRF** | Un valor unívoco y verificable para una clave y una entrada registradas de antemano | Secreto frente al titular de la clave: calcula el valor cuando quiere. Verificar la prueba VRF revela el valor (error de mm4). No demuestra el hecho del recálculo | Una llamada y cientos de bytes por respuesta | **Adoptar**: para la asignación de verificadores (contra el soborno posterior a la asignación) y como moneda del pagador allí donde el resultado afecta al pago ajeno; la clave se registra por pedido antes de la fijación |
| **Commit–reveal** | Vinculación de la sal a un solo pedido antes de la fijación de la respuesta | Protección frente al «último que revela», que puede callar | gpt2: 448 bytes por esquema | **Adoptar de forma limitada**: compromiso antes de la fijación, sin derecho a elegir el resultado |
| **Criptografía umbral** (Shamir, DKG, descifrado umbral) | Almacenar la clave sin un único titular | Independencia de `q` (sección 2.4); protección al aplicar la regla (sección 2.3) | DKG con `n = 7`, `t = 5`: `7·6·32 + 7·5·48 = 3024` bytes de carga útil (gpt2); firma umbral BLS: 288 bytes; sin replicación ni quejas | **Rechazar para reglas secretas**; el faro umbral interno de los participantes solo como una de las fuentes, no como la única |
| **TEE** (SGX, SEV, TDX, GPU protegidas) | Ejecutar código oculto al propietario de la máquina, con confianza en el fabricante | Independencia del fabricante y de su cadena de atestación; en el parque de D5 (RTX 2060, RTX 4070 Laptop, RX 580) no hay GPU protegidas | Escenario del crítico ChatGPT: la verificación protegida dura 1,2 veces más que la abierta; `p = 0,1`: alrededor del 3,20% del tiempo de generación con carga de pesos; el modelo en CPU: unos 50–100 ms por token frente a 15–50 ms en GPU (crítico Claude) [suposición]. Crítico MiniMax: el propietario puede usar el enclave como oráculo; el secreto se sostiene limitando el número de peticiones | **Solo como modo de privacidad a elección del usuario**, no como fundamento de la garantía |
| **FHE** | Cálculo sobre datos cifrados y, mediante un esquema universal, sobre un programa cifrado | Verificación de la corrección del cálculo; el resultado lo abre el titular de la clave (de nuevo `q`). El esquema aproximado CKKS no reproduce los bits del perfil v2 | 1,4·10⁷–2,6·10⁷ bootstrap por token; con 10⁴–10⁵ bootstrap por segundo [suposición]: 140–2600 s por token, de 19 horas a 15 días por una respuesta de 500 tokens; factor frente a la verificación abierta `Φ ≈ 3·10³…2·10⁵` (claude2; críticos Claude, ChatGPT, MiniMax). Recargo `p·ρ·Φ` con `n_w = 300`: de 2,1 a 139 generaciones por respuesta | **Rechazar para la verificación**; estudiar solo para privacidad |
| **MPC** | Cálculo sin reunir el secreto en un solo lugar | Independencia de `q`: la protección se apoya en una mayoría honesta o en «al menos un honesto» con derecho a arruinar el trabajo; con `q = 1` no hay protección | Para ocultar la *elección* de la verificación hay que procesarlo todo: `1/p` = 31 / 303 / 4329 veces más caro que la moneda con `n_w` = 30 / 300 / 4320 (crítico Claude). Ocultar la *petición*: crítico Claude, desde 151 MB por token como cota inferior hasta 0,15–1 GB, 10–67 minutos por respuesta a 1 Gbit/s; crítico ChatGPT, 448 MB por posición, 224 GB por 500 posiciones; crítico MiniMax, hasta 180 TB por respuesta (las estimaciones difieren en órdenes de magnitud, véase la sección 7) | **Rechazar para la verificación** |
| **iO** (ofuscación indistinguible) | En teoría, ejecutar un programa sin revelar su estructura | No hay implementación práctica para el modelo; incluso una iO ideal deja al defraudador un «ensayo» de su falsificación a través del detector | No se evalúa | **Rechazar** |
| **Ofuscación de funciones puntuales** | Verificar «si coincide con el patrón» sin revelar el patrón | Protección con un espacio pequeño de respuestas: fuerza bruta; es la misma trampa | Hash | Solo como parte de la trampa |
| **Cifrado funcional** | Que el titular de una clave funcional obtenga el valor de la función | Ocultar la función al titular de la clave (hace falta un esquema aparte); hace falta un emisor de claves | No se evalúa | **Rechazar** para esta tarea |
| **PIR, ORAM** | Ocultar al servidor el índice de lectura | Ocultar la regla; prueba del origen de los datos | Crítico ChatGPT: en PIR de dos servidores con 10 000 registros de 32 bytes, una consulta de unos 320 KB por servidor y la no colusión de los servidores | **Rechazar** para esta tarea |
| **Trampas** (petición con respuesta conocida de antemano) | Información nueva: un patrón correlacionado con la verdad | Abaratamiento. Una trampa de la misma fuerza que la moneda cuesta el trabajo del ejecutor (≈ una generación, pagada y que nadie necesita) y el patrón (una generación, si es fresco). La coalición reconoce la repetición de una petición antigua | Relación entre el precio de la trampa y el de la moneda `≥ 1/((1 − σ)ρ)`, donde `σ` es la probabilidad de reconocer la trampa: con `ρ = 0,21`, 5,3 / 6,8 / 9,5 / ∞ veces con `σ = q` = 0,1 / 0,3 / 0,5 / 1; con `ρ = 0,40`, 2,8 / 3,6 / 5,0 / ∞ (claude2). gpt2: trampas de un solo uso en el 1% de las tareas con dos generaciones añaden un 2,02% | **Solo «señal hacia arriba»**, sin reducir la frecuencia y sin la marca «verificado» |
| **Pruebas estadísticas y umbrales secretos** | Diagnóstico de fallos masivos y errores de implementación | Reducir la frecuencia: cota `TV`; el umbral se aprende con pruebas | Poco | **Solo «señal hacia arriba»** |
| **Verificador oculto, pagadores no vinculables** | Contra el soborno posterior a la asignación (asignación por VRF) y contra la distinción de pagadores perezosos (claves de pagador de un solo uso, claude1) | Independencia de `q` al verificar un comité. Para el pago no vinculable hace falta un emisor u otro mecanismo sin derechos especiales: no está construido | Kilobytes y segundos (claude1), no evaluado por completo | **Adoptar la asignación por VRF; estudiar a los pagadores no vinculables** |
| **Prueba ZK del cálculo** | El único camino hacia un veredicto verificable públicamente sobre un testigo cerrado | No trata del secreto de las reglas; el precio para Qwen no está calculado. Experiencia del piloto: la ejecución en zkVM es 17 700 veces más lenta incluso sin construir la prueba | No se evalúa | **Estudiar** por separado |
| **«Moving target defense»** | El valor de cambiar la configuración mientras el observador no se ha adaptado | En SkyNet el mejor cambio es en cada tarea, es decir, una moneda fresca | Cero por encima de la moneda | Reducir a la moneda fresca |
| **Antifraude bancario, CAPTCHA** | Funcionan gracias a un servidor cerrado, al coste del intento, a sanciones no monetarias y a llamadas de un solo uso | Nada de esto aparece en SkyNet por cambiar el archivo de reglas (sección 2.5) | — | No trasladar |

**Hallazgo aparte de claude1 (no sobre el secreto): la verificación de Freivalds.** Verificar la multiplicación de una matriz
por un vector con una proyección aleatoria puede ser más barato que la propia multiplicación: una relación de unas 1740 por token y
bloque [cálculo, confirmado por el crítico Claude]. Pero el crítico ChatGPT señaló que esto no acelera
la respuesta: hay que transmitir las activaciones intermedias, tener en cuenta las no linealidades, los redondeos del perfil v2
y la frescura del vector en cada petición. La conclusión de claude1 «el tráfico de activaciones lo hace peor que una pasada
completa» es correcta. No se puede declarar todo Qwen verificado por una sola multiplicación.

---

## 4. Estrategia recomendada

### 4.1. Pasos

Es la estrategia del consejo anterior («pagador-inspector»), precisada por los trabajos y los críticos de este
consejo. Ningún paso requiere reglas secretas. Los pasos 3, 4 y 9 dependen de decisiones aún no adoptadas
(sección 5).

1. **Núcleo abierto.** El generador de la instancia de verificación, la familia de verificaciones admisibles y la ley de elección son
   la parte abierta del núcleo con una huella fijada (D4). «Nuevas reglas en momentos aleatorios» son
   nuevos valores de aleatoriedad, no nuevos algoritmos.
2. **Fijación.** El ejecutor calcula en el perfil exacto v2 y, con un solo registro con acuse de recibo, deposita en el registro
   el criptograma de la respuesta (D24). Hasta ese momento no se hace ninguna elección de verificación.
3. **Moneda secreta del pagador.** Tras la fijación irrevocable, el programa del pagador toma aleatoriedad fresca
   y decide si verificar la respuesta con probabilidad
   `p = max(p_usu, (R − c_f)/(R + H_lock))`; con `c_f ≈ 0` es `R/(R + H_lock)`; con `H_lock = 0`
   (novato), siempre. Para el dinero del propio pagador no hace falta faro.
4. **Moneda verificable allí donde de ella depende dinero ajeno.** Si del resultado de la moneda depende un pago
   ajeno (lotería con premio común, disputas de nodos terceros), la moneda debe ser verificable:
   VRF de una clave registrada por pedido antes de la fijación, o un compromiso sobre la sal publicado
   antes de la fijación (gpt2, claude2). Un compromiso hecho después de la fijación carece de sentido: el pagador
   elige el resultado viendo ya la respuesta (error de mm5 en la propuesta D28).
5. **Bloqueo de la suma.** `H_lock` es solo la suma que madura después del plazo de disputa; el plazo de verificación `δ`
   es mucho menor que la ventana de maduración `W` (en tiempo activo, D12). La primera falsificación demostrada
   quema de forma atómica toda la suma no madurada de la clave, incluidas las recompensas de la misma ola; al perjudicado
   se le devuelve no más de su pago (candidato D26). Sin atomicidad, las fórmulas no aguantan una ola:
   10 falsificaciones paralelas con `R = 1`, `H = 4`, `p = 0,2` dan `+4,4295R` en lugar de `−2,49676R`
   [cálculo].
6. **Marcas.** «Verificado» solo para una respuesta verificada por completo antes de mostrarse; todo lo demás es
   «no verificado» por defecto. Un paso de entrenamiento no verificado no entra en el modelo publicado (D6).
7. **Muestras comunes según D20.** La auditoría del entrenamiento, el examen, la lotería con premio común y la asignación de
   verificadores toman la aleatoriedad de no menos de dos fuentes independientes (el faro umbral externo
   y el VDF desde el bloque final), mezcladas con hash; la ronda se asigna antes de la fijación y llega después
   de ella. Los nodos asignados conocen la elección mediante VRF.
8. **Señales solo hacia arriba.** Las trampas, las anomalías y las pruebas estadísticas pueden asignar
   una verificación adicional, pero no reducen la frecuencia ni dan la marca «verificado».
9. **No vinculabilidad del pagador** (elemento de investigación). Claves de pagador de un solo uso y
   un retransmisor, para que el ejecutor no pueda distinguir a un pagador que verifica de uno perezoso (claude1).
   Mientras el mecanismo no esté construido, en la tabla de riesgo figura la fila «los perezosos son distinguibles: hasta `+R`, incluso
   para el novato».
10. **Lo que no hay en el fundamento.** Reglas secretas, claves de verificación de red, comités umbral
    de custodios, TEE, FHE, MPC, iO.

### 4.2. El papel de la blockchain y del faro: el «detector dinámico en blockchain» en su forma correcta

La pregunta del propietario sobre un detector dinámico en blockchain recibe esta respuesta. La blockchain hace bien
lo que se requiere de un detector, *excepto* el secreto:

- **fija la respuesta antes de la elección de la verificación**: sin esto, ninguna aleatoriedad ayuda;
- **guarda compromisos** sobre rondas futuras y sales, para que nadie pueda elegir un resultado conveniente;
- **hace reproducible la elección**: cualquier nodo, tras la ronda, calcula por sí mismo qué se eligió
  y verifica el fundamento de la decisión incluso después de una parada total de la red;
- **ejecuta la quema y el cálculo único**.

La «dinamicidad» no la da el cifrado de las reglas, sino que la instancia de verificación se deriva cada vez de
una aleatoriedad que aún no existía en el momento de fijar la respuesta. Para una respuesta privada, esa
aleatoriedad es la moneda del pagador; para las decisiones comunes, el faro según D20. Los trabajos lo expresaron así:
«un generador abierto de reglas en el núcleo más una instancia de regla derivada del faro, cuya ronda
se asigna antes de la fijación» (claude1); «las reglas son abiertas, el secreto está solo en la elección: quién, cuándo y qué
regla aplicar» (mm4); «impredecible, no secreto» (mm3).

Dos errores que hay que evitar:

- **El faro en la decisión monetaria del pagador** (mm3, mm4). El sorteo público dice *qué* verificar,
  pero verifica el mismo pagador; un pagador perezoso no verificará ni con sorteo público, y no hay sanción
  por no verificar sin depósito (R5). El sorteo público aquí solo añade la suposición de honestidad
  del faro y el retraso de la ronda (críticos Claude, DeepSeek; mm2 y claude2 dicen lo mismo). mm3 y mm4
  no están de acuerdo (sección 7).
- **Modo de reserva «según el último valor disponible»** (mm3). Si el faro no está disponible y las verificaciones
  de la época van según un valor ya conocido, el defraudador sabe de antemano qué no se verificará. Esto viola directamente
  D20. Si la ronda no está disponible, la operación en disputa espera o la verificación es obligatoria.

Otra precisión: «elegir el bit conveniente de dos independientes» reduce la probabilidad de verificación obligatoria
de `p` a `p²` (crítico ChatGPT), mientras que *mezclar* dos fuentes con un hash unívoco es exactamente lo que
exige D20. La adición propuesta por mm5 a D19, «la moneda secreta y el faro no se mezclan», confunde estas dos
acciones y contradiría D20 (crítico Claude).

### 4.3. Precio

El secreto de las reglas no cambia el precio: no toca ni `ρ` ni `γ`.

| `n_w` | `p = R/(R + H_lock)` | Verificación `p·ρ` con `ρ` = 0,10 / 0,21 / 0,40 | Total frente a Q8_0, lote 1 | Lote 8 |
|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5…+82,3% | +152…+186% |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0…+80,2% | +150…+181% |
| 4320 | 0,023% | 0,0023% / 0,0049% / 0,0093% | +50,0…+80,0% | +150…+180% |

La tabla es [cálculo] según la fórmula `γ(1 + pρ) − 1` y los `ρ`, `γ` medidos (crítico MiniMax, cotejado
por los críticos DeepSeek y Claude). El crítico ChatGPT recuerda que los puntos extremos del rango de `γ` y de `ρ`
proceden de tarjetas distintas y no se midieron en pareja; es una envolvente, no una medición.

- **Novato.** La primera respuesta es una verificación completa, el 10–40% de su generación. Con un trabajo honesto estrictamente
  secuencial y un crecimiento de `H_lock` de `R` por tarea, el número esperado de verificaciones completas en las primeras
  30 tareas es `1 + 1/2 + … + 1/30 ≈ 3,995`; esto es el 1,33% / 2,80% / 5,33% del trabajo de la ventana con
  `ρ` = 0,10 / 0,21 / 0,40 (mm1, crítico ChatGPT) [cálculo]. Con un arranque paralelo desde una cuenta vacía,
  cada petición cuesta una verificación completa.
- **Referencia del 5%.** Como recargo por la verificación es alcanzable: `p·ρ ≤ 0,05` exige `p` no mayor que 50% /
  23,81% / 12,5%, es decir, `H_lock/R ≥ ρ/0,05 − 1` = 1 / 3,2 / 7 (gpt1, gpt2) [cálculo]. Como «5% por encima
  de la generación normal», no: el perfil exacto por sí solo cuesta +50…+80% [medido γ]. El único camino al 5% son
  núcleos más rápidos e idénticos bit a bit.
- **Añadidos de la estrategia.** 32–64 bytes de compromiso o cientos de bytes de VRF por respuesta allí donde hace falta
  que la moneda sea verificable; el faro: cientos de bytes por ronda y por lote, y el retraso de una ronda solo para
  las muestras comunes (crítico Claude) [cálculo].
- **Quién paga** (mm4, crítico MiniMax). El recargo del perfil exacto `γ − 1` lo soporta el ejecutor en cada
  respuesta pagada; la verificación `p·ρ`, el pagador con su prepago. Trasladar la verificación al
  pagador elimina el papel de «verificador al que se paga por verificar» de
  [CURRENT_DESIGN](CURRENT_DESIGN.md), sección 1. Entonces, o el precio `R` sube un 50–80%, o el margen
  del ejecutor tiende a cero. Es una cuestión aparte del propietario (sección 5).
- **Lotería B** (solo se pagan las respuestas elegidas y verificadas por completo; variante de gpt1, gpt2
  y del crítico ChatGPT). Con una proporción de selección del 5%, las verificaciones cuestan de media el 0,5 / 1,05 / 2% del tiempo de generación
  exacta, pero el 95% de las respuestas quedan sin verificar y sin pagar; la varianza de un pago individual es
  `19R²`; la probabilidad de no recibir ningún pago en 20 peticiones independientes es `0,95²⁰ ≈ 35,85%`, y en 30,
  21,46% [cálculo].
- **Entrenamiento.** Una repetición completa de un paso cuesta alrededor del 100% del paso por cada nodo verificador; la referencia del 20%
  no la demuestra ninguna solución. Con `N = 1000` nodos receptores, incluso con costes adicionales nulos, para una verificación
  queda no más de 0,0002 del trabajo del paso (crítico ChatGPT) [cálculo].

### 4.4. Riesgo residual

Ganancia esperada de una falsificación frente a la inacción; «daño» es la proporción de falsificaciones no detectadas
del saboteador, todas con la marca «no verificado». La tabla se compone de las tablas de los críticos Claude, DeepSeek,
ChatGPT y MiniMax y de STRATEGY_SEARCH 5.3; **están resaltadas las celdas corregidas por este consejo**. El detector oculto
no mejora ninguna fila [cálculo].

| Caso | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Novato, `H = 0` |
|---|---|---|---|---|---|
| Dinero, el pagador verifica él mismo; el registro está vivo, D26 y D23 resueltos | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verificación siempre) |
| Lo mismo, pero la coalición `q = 1` incluye a los productores de bloques y censura la disputa | — | — | — | hasta `+R` | hasta `+R` |
| Respuesta falsa con la marca «verificado» | 0 | 0 | 0 | 0 | 0 |
| Daño con `p = R/(R + H)`: pasa toda la serie de `n_w` falsificaciones | ≈ 50% | ≈ 50% | ≈ 50% | ≈ 50% | 0 con un pagador honesto |
| Daño con `p = 3R/(R + H)` | ≈ 12,5% | igual | igual | igual | 0 |
| Pagadores perezosos de proporción `λ`, el ejecutor no los distingue | ≤ 0 con `p(1 − λ) ≥ R/(R + H)` | igual | igual | igual | **`+λR`** |
| Pagadores perezosos distinguibles (con pruebas desde claves nuevas, gratis) | hasta `+R` | hasta `+R` | hasta `+R` | hasta `+R` | **hasta `+R`** |
| Pagador sin equipo encargó la verificación a un trío aleatorio | +0,001R | +0,027R | +0,125R | +R | igual |
| Muestra común según D20, al menos una fuente honesta | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 con una fuente externa honesta; si no, hasta `+R` | igual |
| Solo el faro interno de participantes 64/43 | ≤ 0 salvo 4,8·10⁻²⁸ | salvo 9,4·10⁻¹⁰ | salvo 0,41% | hasta `+R` | igual |
| Para comparación: regla de época secreta en un comité | se filtra en 10 aplicaciones con probabilidad 0,65; después, alrededor de `(1 − p)·E·R` por época | 0,97 | 0,999 | hasta `+R` por falsificación | las pruebas son gratis: hasta `+R` |
| Entrenamiento sin un nodo que se autoverifique | hasta `+R` | hasta `+R` | hasta `+R` | hasta `+R` | hasta `+R` |

Cómo leer la tabla:

- **La fila «≤ 0 con cualquier `q`»** es cierta solo con las condiciones nombradas: `q` es la proporción de colusión entre
  verificadores ajenos; si esa misma coalición controla la producción de bloques o el faro, puede
  retrasar o censurar la prueba (lo dijeron directamente gpt1 y gpt2). También hacen falta `δ ≪ W`,
  la quema atómica (D26), la resolución del conflicto con D16 y la regla de disputas falsas (D23, cálculo M9).
- **La ejecución de la verificación importa no menos que la frecuencia.** Ejemplo del crítico ChatGPT: `R = 1`, `H = 3`,
  `p = 1/4`, `c_f = 0` dan una esperanza exactamente nula; si el pagador ejecuta solo el 90% de las verificaciones asignadas,
  la probabilidad de detección es 0,225 y la ganancia `+0,1R` [cálculo]. Si la primera falsificación puede
  explicarse como un fallo según el D16 actual y conservar `H`, la esperanza `(1 − p)R − c_f` es positiva.
- **«≈ 50%»** es la probabilidad de que pase *toda la serie* de `n_w = H/R` falsificaciones con `H` creciendo
  tras cada omisión (`h/(h + n)` con `n = h`). Una falsificación deliberada de una clave madura
  pasa con probabilidad `1 − p`: con `H = 4320R` es alrededor del 99,977% (crítico ChatGPT según ds2).
- **Las filas «perezosos»** están corregidas: el valor anterior 0 para el novato es incorrecto (sección 1, punto 6).
  Escenario: una clave fresca presenta una falsificación al pagador `X`; si `X` verifica, solo se pierde `c_f`,
  no hay nada que quemar; si `X` es perezoso, la clave recibe `R` y el conocimiento de que «`X` es perezoso»; después, las claves maduras
  de la coalición presentan falsificaciones solo a los perezosos (crítico Claude). El crítico ChatGPT añadió que incluso con
  una indistinguibilidad total la condición `p(1 − λ) ≥ 1` para el novato es imposible de cumplir con `λ > 0`, y que
  las claves no vinculables cierran solo un canal de distinción: el texto, el tiempo, el tamaño de la petición y el pago asociado
  permanecen.

### 4.5. Novato

Un novato con la cuenta vacía (`H_lock = 0`) frente a un pagador honesto se verifica siempre y pierde
`c_f`. El ocultamiento de las reglas no añade nada aquí. Dos salvedades de este consejo: frente a un pagador perezoso
el novato recibe hasta `+R` (sección 4.4), y las claves nuevas gratuitas pueden elevar la proporción de peticiones
verificadas por completo: si la proporción de trabajo en los primeros pedidos de claves vacías es `f`, y en
el resto `p = 0,1`, el recargo es `ρ[f + 0,1(1 − f)]`, y la condición del 5% con `ρ = 0,21` da `f ≤ 0,1534`
(crítico ChatGPT) [cálculo]. Ninguna solución del consejo soporta aún a la vez el flujo de claves nuevas y el autopago.

### 4.6. Pagador perezoso

La estrategia se apoya en que el pagador lanza realmente la moneda y verifica. Un pagador perezoso al que el ejecutor
puede distinguir da hasta `+R` a cualquier clave. Medios en orden decreciente de fuerza: (a) el programa del pagador
ejecuta por defecto la regla del núcleo, y desactivar la verificación quita a la respuesta la marca «verificado»;
(b) claves de pagador no vinculables (claude1): hace falta un mecanismo de pago sin un emisor con derechos
especiales; la firma ciega necesita un emisor, Privacy Pass (de memoria) es un esquema
con emisor de servidor; un emisor umbral vuelve a introducir `q` (crítico Claude); (c) el sorteo público del faro
*no* corrige al pagador perezoso (sección 4.2). No está resuelto cómo combinar la no vinculabilidad con la regla de disputas
falsas sin depósito (D23).

### 4.7. Usuario sin equipo

Un usuario que no puede recalcular la respuesta por sí mismo no está protegido por esta estrategia. Si encarga
la verificación a un trío aleatorio, la coalición recibe `q³R`: +0,001R / +0,027R / +0,125R / +R; con un solo
ayudante, `qR`, y con un cómplice elegido a propósito, hasta `+R` con cualquier proporción media (crítico
ChatGPT) [cálculo]. D1 prohíbe directamente una fuga positiva limitada, así que esto es un agujero abierto
de D21. Un detector oculto no lo cierra: claude1 mostró un contraejemplo con «canarios secretos»:
un verificador coludido pasa honestamente todas las tareas de control ajenas y miente solo en sus propias
falsificaciones, que reconoce por la clave del ejecutor o por la libertad de elección (la falsificación no tiene que ser
determinista; la respuesta exacta sí es determinista). La variante honesta es vender dos niveles de servicio
con la diferencia claramente escrita: «verificado por mí» y «verificado por los asignados, fuga `R·q^k`» (mm1).

### 4.8. Daño

El saboteador no necesita ganancia. Con cualquier frecuencia `p < 1`, parte de sus falsificaciones pasa. La única
protección es la marca «no verificado» por defecto y «verificado» solo tras una verificación completa antes de mostrarse.
Un detector oculto no cambia la fila de daño (todos los trabajos). mm1 encontró el único lugar donde una *elección
fresca* cambia sustancialmente el panorama de daño: con una verificación parcial (sobre todo del paso de entrenamiento), frente
a una prueba fija abierta el defraudador, con una sola pasada exacta, encuentra las celdas no verificables y
falsifica solo esas; la detección es 0; una elección fresca de la prueba después de la fijación da una detección `s` (la proporción de la parte
verificada) para una desviación y `1 − (1 − s)^m` para `m` desviaciones. Los críticos DeepSeek y
Claude precisaron: es aleatoriedad fresca, no secreto de reglas; el motivo de tal falsificación es el daño, no el
dinero (frente al trabajo honesto, una falsificación exacta gana alrededor de cero); y la conclusión se apoya en
una suposición no establecida: que las celdas del paso de entrenamiento pueden falsificarse de forma independiente.

---

## 5. Decisiones

Las formulaciones de abajo son **recomendaciones**, no decisiones adoptadas. Los requisitos inmutables R1–R6 no cambian
al editar líneas de la hoja de ruta. Según D4, tras el lanzamiento con una huella fijada, cambiar el conjunto
de transiciones admisibles exige pasar a una nueva red; cambiar la clave no otorga ese derecho
(crítico ChatGPT).

### 5.1. D4: complementar, sin cambiar el sentido

Texto actual de D4: la verificación es automática, sin votaciones; cada nodo ejecuta por sí mismo la verificación según
la huella fijada de las reglas. El consejo está unánimemente en contra de debilitar D4 en aras de reglas
secretas: una regla secreta exige aceptar el veredicto de los titulares de la clave, del enclave o de un grupo, que el nodo
no puede verificar por sí mismo. El crítico ChatGPT mostró cómo sería tal debilitamiento: «el nodo acepta
el veredicto del programa actual elegido por los titulares de la clave de la época», «el nodo acepta el informe de un programa medido
por la cadena de confianza del fabricante» o «el nodo acepta un bit emitido por el grupo».

**Adición propuesta** (unión de las variantes de los críticos Claude y ChatGPT, claude1, claude2, gpt1,
y de la propuesta D27 de mm5):

> «El núcleo puede aceptar como entrada aleatoriedad desconocida para el ejecutor hasta la fijación final
> del resultado: (a) la moneda secreta de la parte cuya propia decisión se protege, lanzada después de la
> fijación; (b) los valores de las fuentes D20 en rondas asignadas antes de la fijación y que llegan después de ella.
> El generador de la instancia de verificación, la familia de verificaciones admisibles y la ley de elección son la parte abierta del núcleo
> con una huella fijada; las nuevas reglas en momentos aleatorios son nuevos valores de aleatoriedad, y
> no nuevos algoritmos. La instancia implementada que afecta a derechos ajenos se publica no más tarde del pago
> y la recalcula cada nodo. La marca local del pagador por sí sola no crea una
> prueba de red sobre el trabajo. El fundamento de una decisión común no contiene reglas secretas
> ni claves de verificación de larga vida, comités umbral, atestaciones TEE ni veredictos cerrados; solo son admisibles
> como verificaciones adicionales que aumentan la frecuencia».

**Qué no cambia:** la inmutabilidad del núcleo, la ausencia de votaciones, la verificación autónoma por cada
nodo. **Qué rompe:** nada; la adición cierra la dirección de los «detectores secretos» como fundamento de la garantía. La posibilidad de una prueba
verificable públicamente de la relación fijada (ZK) sigue abierta y no requiere modificar D4
(crítico ChatGPT).

### 5.2. D20: precisar

Texto actual de D20: no menos de dos fuentes públicas independientes, el valor en un momento asignado de antemano
después de la fijación final, sin derecho a omitir.

**Precisión propuesta** (crítico Claude con añadidos del crítico ChatGPT):

> «No menos de dos fuentes públicas independientes; sus valores se combinan con una función hash unívoca
> con etiqueta de dominio e identificador de la partida, y no eligiendo uno de los valores. La ronda
> de cada fuente se asigna antes de la fijación final y llega después de la aceptación final
> del bloque con la fijación. Se prohíben la omisión, el sorteo repetido, la sustitución de una fuente o el paso a un valor conocido
> anteriormente; si la ronda no está disponible, la operación en disputa espera, y la nueva petición no recibe
> billete para esa ronda. El faro se usa para muestras que afectan a derechos ajenos (entrenamiento, examen,
> lotería con premio común, asignación de verificadores); para la verificación privada por el pagador de su dinero no
> se requiere. El faro umbral interno de participantes puede ser una de las fuentes solo
> con una suposición registrada sobre la proporción de colusión de sus titulares, y no puede ser la única. Un VDF del
> mismo bloque no se considera una fuente independiente. La confianza en las fuentes es una suposición según R4».

**Qué excluye:** el modo de reserva «último valor disponible» (mm3), la modificación de mm5 a D19
(«no mezclar las fuentes»), el faro en la decisión monetaria del pagador (mm3, mm4). **Riesgo abierto:**
si «esperar la ronda» significa un retraso infinito, es un riesgo R1/R6 no cerrado (crítico ChatGPT);
el crítico MiniMax propone, en lugar de esperar, considerar la verificación obligatoria.

### 5.3. Qué no cambia

- **D1**: no cambiar ni debilitar hasta «mientras `q` sea pequeño»; una fuga positiva limitada
  sigue siendo una violación (todos los trabajos y críticos).
- **D7**: una regla secreta no lo cumple con ningún umbral (sección 2.4).
- **D19**: no cambiar; la adición de mm5 es errónea (sección 4.2).
- **D6**: el ocultamiento no cambia la fila de daño; las marcas se precisan según la cuestión 3 del compendio anterior.

### 5.4. Relación con las ocho cuestiones del compendio anterior

Las ocho cuestiones de [STRATEGY_SEARCH](STRATEGY_SEARCH.md), sección 6, siguen abiertas. Este consejo
añadió a ellas:

| Cuestión del compendio anterior | Qué añadió el sexto consejo |
|---|---|
| 1. D21, D11, D2: ¿pagar o no la respuesta omitida por la moneda? | No hay argumentos nuevos. Se corrigió la celda «pagador perezoso × novato» (hasta `+R`): si se permite pagar lo omitido, hace falta protección contra la distinción de los perezosos. El crítico ChatGPT sigue a favor de la verificación completa como contrato principal y de la lotería B como algo aparte |
| 2. D7: qué verificación es admisible para el pago | Se confirma que ni el ocultamiento, ni la atestación, ni el comité pueden reducir la frecuencia inferior; aumentarla sí es posible. Se añade: importa la proporción de verificaciones *ejecutadas*, no solo la frecuencia (ejemplo `+0,1R`) |
| 3. D6: marcas | La trampa, la estadística y el detector oculto no dan la marca «verificado» |
| 4. D16: fallo honesto | Si la primera falsificación puede declararse un fallo y conservar `H`, la moneda no disuade: `(1 − p)R − c_f > 0`. La decisión sobre D16 hace falta antes de activar cualquier pago de lo omitido |
| 5. D8: plazo y derechos de disputa | La condición `δ ≪ W` y la vitalidad del registro entran en la fila «≤ 0» (sección 4.4) |
| 6. D23: bloqueo hasta M9 | Ninguno de los once trabajos calculó M9; el bloqueo se mantiene. La no vinculabilidad de los pagadores añade a M9 una nueva cuestión |
| 7. Nuevo D26: bloqueo de la suma | Se confirma la necesidad de una quema atómica de la ola; el bit común de época es un nuevo contraejemplo (`+8,1R`) |
| 8. D1: ¿cambiarlo? | No cambiar |

### 5.5. Nuevas cuestiones-decisión de este consejo

**Cuestión A (D4).** ¿Aceptar la adición a D4 de la sección 5.1? *Recomendación de los críticos Claude, ChatGPT
y DeepSeek:* sí; el sentido de D4 no cambia. *Dónde discreparon:* el crítico ChatGPT propone una redacción más detallada
que habla explícitamente de la verificación «mediante una prueba públicamente verificable de la afirmación
fijada»; el crítico DeepSeek considera suficiente una breve nota sobre la aleatoriedad después de la fijación;
el crítico MiniMax (como mm2 y mm5) cree que no hay que cambiar D4 en absoluto, porque la regla de verificación
ya es abierta.

**Cuestión B (D20).** ¿Aceptar la precisión de D20 de la sección 5.2? *Recomendación:* sí. *Dónde discreparon:*
qué hacer si la ronda no está disponible: esperar (críticos Claude y ChatGPT) o considerar la verificación
obligatoria (críticos DeepSeek y MiniMax). La espera puede convertirse en un retraso infinito; la verificación
obligatoria cambia el precio y, en la lotería, la composición de los ganadores.

**Cuestión C (faro o moneda en la decisión monetaria).** ¿Registrar que para la verificación privada
por el pagador de su dinero no se usa el faro? *Recomendación* de los críticos Claude y DeepSeek, así como de
claude1, gpt1, gpt2, ds1, ds2, mm1, mm2: sí. *En contra:* mm3, mm4, mm5 (sorteo público en lugar de moneda),
claude2 (VRF del pagador más faro para los asuntos comunes). El crítico DeepSeek propone comparar primero
ambos esquemas con un miniagente en ataques iguales (sección 6).

**Cuestión D (pagadores no vinculables).** ¿Incluir en el programa de investigación un mecanismo por el cual
el ejecutor no pueda vincular las peticiones de un mismo pagador? *Recomendación* del crítico Claude: sí, como
investigación; antes de construirlo, la tabla de riesgo contiene la fila «los perezosos son distinguibles: hasta `+R`».
*Abierto:* el pago sin un emisor con derechos especiales, la compatibilidad con D23, la distinción por texto y
tiempo.

**Cuestión E (peso).** ¿Registrar en la especificación del peso ([CURRENT_DESIGN](CURRENT_DESIGN.md), sección 4),
que el peso por el que se seleccionan titulares o verificadores no crece con peticiones autopagadas?
*Recomendación* del crítico Claude: sí. claude2 proponía una selección «por el peso del trabajo verificado» sin tal salvedad.

**Cuestión F (quién paga el perfil exacto).** ¿Cómo distribuir el recargo `γ − 1` si desaparece el papel del verificador
remunerado? *La plantearon* mm4 y el crítico MiniMax; no se ha propuesto solución.

**Cuestión G (nuevas decisiones de mm5).** ¿Aceptar D27 («secreto de la elección, no secreto de la verificación») y D28
(«moneda con revelación aplazada»)? *Recomendación de los críticos:* D27 entra por su sentido en la adición a D4
(sección 5.1); D28 duplica el compromiso de la moneda de gpt2 y claude1 y solo tiene sentido si
el compromiso se publica *antes* de la fijación de la respuesta.

---

## 6. Qué calcular con miniagentes y qué comprobar con experimentos

### 6.1. Miniagentes (fracciones exactas, hash de control, repetición en un segundo dispositivo)

Lista común de los cuatro críticos. Para cada cálculo, conservar la descripción de las reglas, las entradas, las fracciones exactas,
el peor historial, la versión y el hash de control (crítico ChatGPT).

1. **Regla de época frente a moneda fresca.** Ola, `H_lock`, quema de toda la suma, secuencia adaptativa.
   Referencias: `+8,1R` / `−2,3751096381R` (gpt2), `98,01R` (claude2),
   1/5 → 1/9 → 0 (claude1), `+4,4295R` / `−2,49676R` / `+7,2R` (consejo anterior y crítico ChatGPT).
2. **Pruebas de pagadores perezosos con claves nuevas.** Esperanza de una prueba, tiempo hasta reconocer
   al pagador, ganancia de las claves maduras; con pagadores vinculables y no vinculables. Expectativa
   del crítico Claude: con vinculabilidad, la disuasión contra los perezosos es nula.
3. **Moneda secreta frente a sorteo público del faro** en ataques iguales (crítico DeepSeek). Expectativa:
   resultados monetarios iguales y mayor precio en el sorteo público.
4. **Programa lineal de la mezcla de pruebas** (gpt1, gpt2): referencia «tres clases → 2/3 frente a 1/2»,
   añadir una clase no cubierta → 0; minimax sobre la matriz «prueba × falsificación».
5. **Colas del umbral:** binomiales, sin reemplazo, por peso con autopago, con soborno después de la
   asignación. Referencia «3 de 5»: `107/12500`, `4077/25000`, `1/2`, `1`; SHA-256 de control
   de las cuatro filas de gpt1, repetido por el crítico ChatGPT:
   `fd83fbdd42baa56d982eba3be90888cf3ec5a6261b5daa53d42fdc42b99c8323`.
6. **Trampas:** `1/((1 − σ)ρ)` en una malla de `ρ` y `σ`; reconocimiento de la repetición; amortización de un banco de patrones
   frente al recálculo; comprobación de la afirmación de mm2 sobre el precio casi nulo de repetir una petición ya verificada.
7. **Desviaciones en la VRF y el compromiso del pagador:** negarse a revelar, varias claves, corte tras
   la revelación, lotería con premio común.
8. **Mezcla de fuentes D20:** sesgo con una sola fuente honesta, con retención de un bloque, con
   la ronda no disponible; prohibición del «último valor».
9. **Falsificación «quirúrgica» de mm1** frente a una prueba fija abierta y a una prueba fresca: detección 0 frente a `s`;
   umbral `p·s ≥ (R − c)/(R + H_lock)`.
10. **Recuento de operaciones no lineales por token** según la configuración fijada de D5 para las estimaciones de FHE y MPC
    (ahora 1,4·10⁷–2,6·10⁷ de forma aproximada); estimaciones de DKG, commit–reveal y VRF en bytes y mensajes.
11. **Lote 8 en el pagador** (mm3): `ρ` se midió respecto a la generación por lotes, y el recálculo de una sola
    respuesta por el pagador no se abarata así.
12. **Corrección de tablas:** mm1 (`k = 10`, `H_lock = 10R`), mm5 (`p·ρ`), la celda «perezoso × novato»
    en STRATEGY_SEARCH 5.3.
13. **M9**: el precio de la disputa para la regla D7 y la condición para levantar el bloqueo de D23; autodisputa, límite de devolución,
    flujo de claves nuevas.

### 6.2. Experimentos

**Para la conclusión sobre el detector oculto no hace falta experimento:** son teoremas, una medición no los refuta (claude1,
claude2, ds2, críticos Claude y DeepSeek). Tampoco hacen falta experimentos con FHE, MPC y TEE: su mejor resultado
no cambia los teoremas.

**Dentro de D5 (permitido):** O5, la calidad en 320 tareas; O3 y O4 con núcleos más rápidos e idénticos bit a bit,
el único camino a la referencia del 5%.

**Fuera de D5, solo con permiso expreso del propietario:**

- el tiempo de una pasada de verificación en la CPU de un portátil y en un teléfono, arranque en frío y en caliente, energía;
- hasta qué punto los metadatos de la petición (tiempo, tamaño, texto) permiten al ejecutor distinguir a un pagador
  que verifica; de esto depende el precio de las claves no vinculables;
- la frecuencia de discrepancias de hardware silenciosas `P_f`, antes de cualquier modificación de D16;
- la proporción de coincidencia de tokens entre Q8_0 y el perfil exacto (para estimar la falsificación barata y para la decodificación
  especulativa exacta);
- la latencia y el coste de una ronda de un faro real, el comportamiento con una fuente silenciosa;
- para las trampas, si se reconoce la verificación y cuánto cuestan los patrones;
- la repetición exacta del paso de entrenamiento como condición previa de cualquier verificación del mismo.

---

## 7. Discrepancias no resueltas por el consejo y referencias dudosas

### 7.1. Discrepancias

1. **Pago de la respuesta omitida por la moneda frente a la verificación completa de cada respuesta pagada.** claude1,
   claude2, ds1, ds2 y mm1–mm5 se apoyan en pagar lo omitido bajo el riesgo de quema de la suma
   no madurada; gpt1, gpt2 y el crítico ChatGPT, en la verificación completa como contrato principal y la lotería B como
   algo aparte. Heredado del consejo anterior; decisión del propietario sobre D21, D11, D7.
2. **Faro o moneda en la decisión monetaria del pagador**: sección 5.5, cuestión C. mm3 y mm4 creen que
   el sorteo público elimina la suposición de un pagador honesto; los críticos Claude y DeepSeek lo consideran
   un error (un pagador perezoso no verificará ni con sorteo público). No está calculado.
3. **`R/(R + H_lock)` o `R/H`.** La primera es exacta para el dinero; la segunda da margen y un número esperado finito
   de falsificaciones hasta la detección con `H` fijo, pero cuesta alrededor del doble con `H` pequeño.
   El crítico ChatGPT mostró que, con `H` creciendo tras cada omisión, en ambas reglas el número medio de omisiones
   hasta la primera detección es infinito. El consejo no aportó argumentos nuevos.
4. **La trampa como ganancia autónoma.** mm2 (el patrón secreto es la única ganancia real)
   y ds1 (ahorro del patrón en caché) frente a claude2, mm4, mm5, gpt1 y los críticos Claude y DeepSeek.
   El crítico ChatGPT adoptó una posición intermedia: un patrón ya conocido por el pagador honesto puede
   reducir el precio marginal, y para trampas frescas indistinguibles `σ` puede ser 0 incluso con `q = 1`
   entre ejecutores ajenos. El cálculo no se ha hecho.
5. **La mezcla de tipos de verificación como medio de ahorro.** gpt1, gpt2, claude2: posible con una cobertura demostrada
   de las clases de error; mm2: nunca. Para Qwen la cobertura no está demostrada.
6. **El faro umbral interno de los participantes.** mm3: el mejor primitivo; mm5: solo externo; claude1,
   claude2 y el crítico Claude: admisible solo como una de las fuentes.
7. **Hasta qué punto R2/R3 prohíben los secretos comunes.** ds1, mm1, mm3: por principio; claude2, críticos Claude
   y ChatGPT: solo los secretos necesarios para verificar decisiones pasadas.
8. **Precio de MPC.** Las estimaciones difieren en órdenes de magnitud: ds1, 2,4–14 MB por token (los críticos creen que es el
   precio del rastro de verificación, no de MPC); crítico Claude, 0,15–1 GB por token; crítico ChatGPT, 448 MB por
   posición; crítico MiniMax, hasta 180 TB por respuesta (considera todas las multiplicaciones en red, mientras que el crítico ChatGPT
   observa que multiplicar un peso abierto por una activación dividida en muchos protocolos se hace
   localmente). La conclusión «MPC está fuera de presupuesto y depende de `q`» no cambia por ello.
9. **Factores de FHE:** ds1 `10³–10⁶`, claude2 `3·10³–2·10⁵`; el crítico ChatGPT cree que multiplicar la
   estimación por bootstrap por `ρ` de una pasada completa es incorrecto, y hace falta una estimación de la misma pasada bajo
   el esquema concreto. Las conclusiones no dependen de ello.
10. **Prueba oculta con verificación parcial** (mm1): «detector secreto» o moneda fresca,
    una discrepancia de palabras; la aplicabilidad al paso de entrenamiento depende de una independencia no medida de las celdas.
11. **D16.** Quemar `H_lock` por cualquier discrepancia demostrada, con indemnización a los honestos con cargo a una tasa de red
    (línea de claude1 y de los críticos Claude y DeepSeek), frente a conservar las recompensas anteriores en un fallo honesto
    (gpt1, gpt2, crítico ChatGPT). Hace falta medir `P_f`.
12. **Entrenamiento.** Ninguna solución cumple D7 con `q = 1` dentro del 20%.
13. **Clase principal de falsificaciones:** la «quirúrgica» cara (mm1) o la Q8_0 barata (mm3, mm4). No medido.

### 7.2. Errores encontrados en las cifras de los trabajos

Para que las cifras erróneas no pasen a otros documentos:

| Trabajo | Afirmación | Correcto [cálculo de los críticos] |
|---|---|---|
| mm1 | Con `H_lock = 10R`, frecuencia 0,0909 y precio de verificación 0,005–0,009% | `0,0909·ρ` = 0,91–3,64% |
| mm1 | Fuga de «diez» con `q = 0,1`: `1·10⁻⁵R` | `10⁻¹⁰R` |
| mm1 | Umbral del 25% con `H_lock = R` | 29,29% con los propios parámetros de mm1 |
| mm5 | `p·ρ` = 0,021–0,042% con `p = 0,1` | 2,1–4,0% (la propia tabla de mm5 es correcta) |
| mm5 | «FHE es determinista, el observador construye un diccionario» | Los esquemas FHE seguros son probabilísticos |
| mm5 | «La VRF es impredecible para el titular» | El titular calcula la VRF cuando quiere |
| mm5 | La repetición completa del paso de entrenamiento ≈ 36,8% | 36,8% es un ejemplo de carga mixta; la repetición del paso ≈ 100% |
| mm2 | «El 5% es alcanzable con `p ≤ 0,33%`» | Con `ρ = 0,21` es admisible `p ≤ 23,8%` |
| mm4 | «La VRF no revela la elección» | Verificar la prueba VRF revela el valor |
| ds2 | `N·H_s ≈ 2718` intentos | Alrededor de 890 sin reemplazo; basta una posición segura |
| ds1 | La trampa cuesta `φ·ρ`, el patrón en caché ahorra | La trampa cuesta no menos que una generación del ejecutor; primero hay que obtener la caché |
| ds1, ds2 | Las trampas añaden una detección `φ` con cualquier `q` | No más de `φ(1 − q)` al repetir; con `q = 1`, 0 |
| claude1, claude2, mm3, mm4, STRATEGY_SEARCH | Pagador perezoso × novato = 0 | Hasta `+R` |
| claude2 | Fórmula del ejemplo de época `(1 − p)(E − 1)R` | `(1 − p)·E·R − p·H_lock = 98,01R`; la coincidencia es casual |

### 7.3. Referencias dudosas (estimaciones de los críticos de memoria, sin cotejo)

| Trabajo | Afirmación | Valoración |
|---|---|---|
| mm5 | «RandAILight» como faro | Dudoso; los críticos no conocen el nombre |
| mm5 | «La iO es teóricamente posible, Barak y coautores ~2001» | Confundido: Barak y coautores, 2001, es la imposibilidad de la ofuscación de «caja negra»; los candidatos de iO son Garg y coautores, 2013 |
| mm1 | «Hoja de ruta de la iO de Barak y coautores, 2019» | Dudoso |
| mm2 | Apéndice F: «Ben-Or y coautores», «Allingham, Melvin, Temple 1992», «Dwork ~1999», «Hashcash: Homstein», «Awasthi», «Randcast Bader ~2020» | Dudoso en casi todos los puntos; no trasladar al compendio |
| mm3 | «Cui, Wang y otros, Skoglid y otros» sobre moving target defense | Dudoso |
| ds1 | «Canetti 1997: funciones puntuales en el modelo de oráculo aleatorio» | Dudoso (de memoria, una suposición de tipo DDH) |
| ds1 | «Bishop–Jain–Kowalczyk 2018» | Dudoso en el año (de memoria, 2015) |
| ds1, ds2 | «drand ~30 s» | En parte: de memoria, distintas cadenas tienen 30 s y 3 s |
| ds2 | «MPC 5,98·10¹² MAC (claude2)» | La referencia es imprecisa |
| claude1 | «SGX.Fail, clave maestra de Secret Network, 2022» | Dudoso en los detalles (el autor mismo lo señaló) |
| claude1 | Privacy Pass como ejemplo de emisión sin una parte especial | De memoria, es un esquema con emisor de servidor |
| claude2 | La cota inferior de PIR: Beimel, Ishai, Malkin | Dudoso: sus trabajos son sobre PIR con preprocesamiento; la cota clásica, de memoria, es de Chor y coautores |
| claude2 | Lowd–Meek, Tramèr: `d` consultas binarias bastan para cualquier clasificador | Dudoso en general |

Las demás referencias de los trabajos (Shamir, Feldman, Pedersen, Gennaro–Jarecki–Krawczyk–Rabin, Micali–Rabin–Vadhan,
Boneh y coautores sobre VDF, Rivest–Shamir–Wagner, Aumann–Lindell, Asharov–Orlandi, los juegos de inspección,
Barak y coautores sobre la imposibilidad de la «caja negra») a los críticos les parecen correctamente atribuidas en cuanto a la dirección;
las fuentes primarias no se cotejaron.

---

## 8. Quién hizo qué

El consejo trabajó con los materiales del proyecto, sin acceso a la red y sin experimentos.

- **Once trabajos independientes:** ChatGPT, dos (gpt1, gpt2); DeepSeek, dos (ds1, ds2);
  Claude, dos (claude1, claude2); MiniMax, cinco (mm1 centrado en la economía, mm2 en la protección contra
  el engaño, mm3 en la distribucionalidad y la recuperación, mm4 en los contraejemplos, mm5 en las soluciones no estándar). Cada trabajo analizó seis direcciones del encargo: quién guarda la clave, cómo verificar
  según una regla desconocida, qué puede ser un detector secreto, la teoría, el precio y la compatibilidad
  con las decisiones.
- **Cuatro críticas:** una de ChatGPT, DeepSeek, Claude y MiniMax (la crítica de MiniMax está redactada
  como propuesta con crítica). Cada crítico leyó los once trabajos, buscó errores y
  contraejemplos y recalculó las cifras clave. El crítico DeepSeek comprobó la aritmética con programas locales sobre fracciones
  exactas; el crítico Claude, con cálculos cortos en Python; el crítico ChatGPT
  reprodujo el hash de control de la tabla de gpt1.
- **Compendio:** este documento lo compuso Claude a partir de los trabajos y las críticas. No se añadieron estimaciones ni cifras nuevas más allá de los trabajos,
  las críticas, los resultados de D5 y STRATEGY_SEARCH; donde los críticos discreparon, se indica.
