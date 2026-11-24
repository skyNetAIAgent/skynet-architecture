<!-- translation of docs/VERIFICATION_SEARCH.md, source sha256: cdf54a57e7747ae1f862b5b29fa7a53eee7fca80d8bae17a0cbc60f022cec00b -->

# Búsqueda de una verificación que no dependa de la proporción de colusión

[English](../../docs/VERIFICATION_SEARCH.en.md) · [中文](../zh/VERIFICATION_SEARCH.md) · **Español** · [Français](../fr/VERIFICATION_SEARCH.md) · [Deutsch](../de/VERIFICATION_SEARCH.md) · [Italiano](../it/VERIFICATION_SEARCH.md) · [Русский](../../docs/VERIFICATION_SEARCH.md) · [Português](../pt/VERIFICATION_SEARCH.md) · [العربية](../ar/VERIFICATION_SEARCH.md)

Estado a 24 de noviembre de 2026.

Este documento es el resultado del consejo de modelos para la etapa 4 de la hoja de ruta («Búsqueda de una garantía que no dependa
de la proporción de colusión», [ROADMAP](ROADMAP.md), sección 4). El consejo buscaba una verificación que cada nodo
ejecute por sí mismo, de modo que el acuerdo o la colusión de otros verificadores no decida nada. Se buscaba para dos
tipos de trabajo: la respuesta del modelo Qwen a una petición del usuario y el paso de ajuste fino.

**Estado del documento.** Es un resultado de razonamiento y cálculo por fórmulas, no una medición.
No hubo para él experimentos con el modelo, ejecuciones de la red, sistemas de prueba ni model checking.
Los participantes y los críticos ejecutaron solo programas aritméticos cortos y pequeñas búsquedas exhaustivas
en el procesador; dos de esas búsquedas de los trabajos de ChatGPT fueron repetidas por dos críticos y los hashes de control
coincidieron. Las cifras con la marca [cálculo] se obtienen por las fórmulas a partir de parámetros nombrados explícitamente. Los parámetros
de los modelos y de las tarjetas gráficas los sustituyeron los propios participantes; ningún trabajo los cotejó con la configuración publicada
de Qwen3.5-4B ni de un modelo de unos 27 mil millones de parámetros. **Las únicas decisiones adoptadas son las decisiones D1–D25** en [ROADMAP](ROADMAP.md), sección 3. Todo lo demás aquí es
una estimación del consejo. Donde los críticos discreparon, figura «discutible».

**Cómo leer.** La sección 1 — qué se busca y en qué condiciones. La sección 2 — qué se demostró imposible
y qué afirmaciones de imposibilidad fueron refutadas. Las secciones 3 y 4 — el análisis de los mecanismos para la respuesta
del modelo y para el paso de entrenamiento, con el mejor candidato y sus limitaciones. La sección 5 — qué quedó
sin demostrar y qué experimentos y cálculos lo resolverán. La sección 6 — preguntas al propietario. La sección 7 — quién
participó.

**Resumen breve.**

1. **Respuesta del modelo.** La verificación que no depende de la proporción de colusión existe solo donde toda la
   respuesta la verifica el propio pagador, cuyo dinero está en juego. El mejor candidato es el «PPS»: el pagador en una sola
   pasada recalcula la petición y la respuesta lista en un perfil entero exacto, el pago procede
   solo de su prepago, y la disputa por la prueba de error la verifica cada nodo. El precio calculado es
   1,2–3,8% del tiempo de generación, pero solo con generación de una respuesta a la vez [cálculo]. El candidato
   no cubre al consumidor sin equipo y depende de una coincidencia de bits no medida.
2. **Paso de entrenamiento.** No se ha encontrado una verificación del propio paso dentro de alrededor del 20%, que no dependa de la proporción de colusión.
   Con esto coinciden los seis trabajos y las tres críticas.
3. **El único camino superviviente para el entrenamiento** cambia aquello por lo que se paga: la red paga
   por una mejora demostrada del modelo en un examen elegido después de fijar la actualización. Por la decisión D18 este camino
   se investiga como candidato a nueva unidad de pago, pero aún no se ha adoptado; hacen falta cálculos, un experimento y las correcciones
   halladas por los críticos.
4. **Lo deciden el experimento D5** (coincidencia de bits del Qwen3.5-4B entero en dos tarjetas gráficas y entre
   dos modos de cálculo, tiempo, calidad) **y los cálculos de los miniagentes** de la sección 5.3; con ellos se toma
   la decisión final sobre el pago del entrenamiento (D18).

Documentos de origen: las decisiones D1–D17 y la etapa 4 en [ROADMAP](ROADMAP.md); el modelo del adversario
y la formulación formal de D1 en [THREAT_MODEL](THREAT_MODEL.md), sección 1.5; las variantes A y B
en [CURRENT_DESIGN](CURRENT_DESIGN.md); [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); los requisitos obligatorios [REQUIREMENTS.md](../ru/REQUIREMENTS.md). Los participantes
también leyeron investigaciones previas del proyecto sobre aritmética exacta, sumcheck/GKR, Brakedown y el precio del testigo
para LoRA (los documentos `LORA_*` y `HONESTY_RESEARCH_GATE` del archivo de investigación; no forman parte de este
repositorio). Los participantes aún no tenían las decisiones D6–D17: se adoptaron ese mismo día.
Al consolidar, esas decisiones se aplicaron a las conclusiones de los trabajos; donde una decisión cambia el veredicto, se dice expresamente.

---

## 1. Planteamiento

### 1.1. Qué se busca

Se busca un procedimiento que el nodo ejecute por sí mismo con datos que la coalición no pueda falsificar:
la entrada de la tarea, el modelo fijado, las reglas fijadas y, posiblemente, una prueba
matemática. La decisión del nodo no debe apoyarse en firmas ni veredictos de otros nodos. Entonces
la proporción de verificadores coludidos `q`, incluida `q = 1`, no influye en la decisión.

Dos tipos de trabajo:

- **(a) respuesta del modelo** Qwen del orden de 4–27 mil millones de parámetros a una petición del usuario;
- **(b) paso de ajuste fino** (LoRA o completo) sobre una porción de datos dada.

### 1.2. Condiciones obligatorias

| Condición | Qué se deriva de ella para la verificación |
|---|---|
| **D1** | El beneficio esperado de cualquier declaración falsa no es mayor que cero ni frente a la inacción (`Δ₀ ≤ 0`) ni frente al trabajo honesto (`Δч ≤ 0`), para cualquier coalición, incluido un novato con la cuenta vacía y cualquier número de claves. Hacen falta **ambas** desigualdades ([THREAT_MODEL](THREAT_MODEL.md), sección 1.5). Una fuga positiva limitada como `R·q^k` en la variante B no sirve |
| **D2** | Solo se paga el resultado verificable. El tiempo de trabajo, la potencia declarada y el equipo encendido no sirven de base. El modo en que el ejecutor obtuvo el resultado correcto (caché, otra máquina) no importa |
| **D4** | La verificación es automática, sin votaciones; cada nodo la ejecuta por sí mismo según la huella fijada de las reglas |
| **D6** | El daño entra en D1: una respuesta falsa no debe entregarse al usuario como verificada, ni un paso falso debe entrar en el modelo. El resultado se usa solo tras una verificación que no dependa de la proporción de colusión, o se marca expresamente como no verificado |
| **D7** | Se exige una verificación que no dependa de la proporción de colusión. No se admite debilitar D1 a «mientras los coludidos sean menos de `q*`» |
| **D8** | Solo pueden disputar los verificadores asignados por sorteo a la tarea y el usuario respecto a su petición. Sin depósito. Los demás comunican una sospecha en el tablero sin derecho a detener el pago |
| **D15** | Un recálculo simple que se pueda copiar no se paga |
| **R5** | Ningún depósito, contribución ni multa. Solo se pueden perder las recompensas no maduradas («suma en espera» `H`) |
| **Referencias de precio** | Un recargo por la verificación de alrededor del 5% del trabajo para las peticiones y de alrededor del 20% para el entrenamiento. Son referencias, no requisitos confirmados |

Decisiones relacionadas: D9 (el plan de entrenamiento se deriva por regla del catálogo y de los resultados del examen,
los créditos se emiten una vez por contenido de la tarea), D10 (el intercambio se realiza con una sola entrada del registro),
D12 (las ventanas se cuentan en tiempo activo de la red), D14 (el precio de la disputa es el de la red de segundo
nivel más barata), D16 (un fallo de hardware honesto no se castiga), D17 (los pagos por peticiones en la variante B —
solo con cargo a los pagos de los usuarios).

El muestreo estadístico, la confianza en el enclave de hardware y el pequeño error criptográfico
según los requisitos son supuestos: se pueden proponer, pero hay que nombrarlos abiertamente.

### 1.3. Modelos y parámetros que usaron los trabajos

No había un manifiesto fijado de Qwen3.5-4B en los materiales. Cada trabajo tomó su propia configuración densa
convencional, por lo que «4B» significa números distintos en trabajos distintos. Si en Qwen3.5 hay capas híbridas de atención lineal, todas las proporciones de atención y las conclusiones sobre la coincidencia de modos de cálculo
cambian (sección 5).

| Trabajo | Respuesta del modelo (a) | Paso de entrenamiento (b) |
|---|---|---|
| claude1 | «4B»: 36 capas, anchura 2560, consultas de atención 4096, claves/valores 1024, MLP 9728, vocabulario 151 936, entrada y cabeza compartidas (4,022 mil millones de parámetros). «27B»: 64 capas, 5120, 6144, 1024, 20 480, 151 936, separadas (26,386 mil millones). Consultas de 500/500 y 2000/1000 tokens | LoRA de rango 16 en las matrices de las capas superiores, examen `n = 10⁴–10⁶` posiciones |
| claude2 | La misma «4B». Petición de 1000 tokens, respuesta de 500; trabajo de la petición 5,98·10¹² MAC [cálculo] | LoRA de rango 16/64 en las siete matrices, contexto 4096, porción de 64 o 7680 secuencias |
| gpt1 | «S»: 36 bloques, 2560, KV 640, MLP 11 008, 151 936. «Lg»: 48, 5120, 1024, 31 232. Entrada 128, salida 32 tokens | 8 micro-lotes de 512 tokens, LoRA de rango 8 en Q, V |
| gpt2 | «Pequeño»: 36, 3072, KV 768, MLP 8192, vocabulario 150 000. «Grande»: 60, 6144, 1024, 18 432. Entrada 128, salida 128 | Lo mismo que gpt1 |
| ds1 | Clase Qwen3-4B: 4·10⁹ parámetros, 36 capas, 2560, MLP 9728 | Perfil Qwen2.5-1.5B de investigaciones previas: 28 bloques, 1536, MLP 8960, LoRA de rango 8 en q/v, 512 tokens × 8 micro-lotes |
| ds2 | 36 capas, 2560, MLP 8960, 32/8 cabezas; contexto 2048, respuesta 200 | El mismo perfil 1.5B |

Equipo (ficha según la memoria, no cotejada): clase RTX 2060 — 336 GB/s de memoria, unos 103 TOPS
INT8, 6 GB; clase RTX 4090 — 1008 GB/s, unos 660 TOPS, 24 GB. Las proporciones de pico 0,8 para la memoria y 0,4
para el cálculo son escénicas. La única medición de velocidad es 73,8 tokens/s de Qwen3-4B Q4_K_M
en una RTX 2060 en el piloto ([PILOT_RESULTS](PILOT_RESULTS.md)). Es otro formato de pesos, y no
confirma ni refuta los modelos anteriores.

La formulación común de D1 para una sola declaración falsa, en la que coincidieron los trabajos: con precio de la tarea `R`,
coste de la ejecución honesta `c`, gastos de la falsificación `c_f` y probabilidad de su aceptación `ε`
hacen falta `Δ₀ = εR − c_f ≤ 0` y `Δч = εR − c_f − (R − c) ≤ 0` [cálculo].

---

## 2. Cotas inferiores: qué se demostró imposible

### 2.1. Cotas confirmadas por los críticos

Son afirmaciones sobre **clases** de verificaciones. Ninguna de ellas excluye todas las verificaciones concebibles;
nadie ha demostrado una cota inferior general de precio para todos los algoritmos.

1. **Indistinguibilidad.** Si el nodo acepta un resultado solo por mensajes de otros nodos, entonces, con la
   colusión de todos sus autores, existe un resultado falso que aceptará: la coalición enviará las mismas
   firmas y huellas que con un resultado honesto. Con `q = 1`, el nodo está protegido solo por lo que
   verificó él mismo. (claude1, lema 1; claude2, 3.1; gpt2, 9.4; ds2, 6.1. Todos los críticos coinciden.)
2. **Escala «cada nodo por sí mismo».** Si el cambio de un estado común (emisión de créditos, peso) debe
   estar protegido para cada uno de los `N` nodos completos, cada uno de ellos verifica cada resultado de ese tipo,
   y el precio total no es menor que `N·v`, donde `v` es el precio de una verificación. Para ajustarse al 5% o al 20%, con
   `N = 1000` hace falta `v/W ≤ 5·10⁻⁵` o `2·10⁻⁴` de trabajo [cálculo]. De aquí salen tres modos de obtener
   independencia de la colusión: decide el único participante cuyo dinero está en juego; la verificación se comprime
   (prueba breve o examen pequeño); el resultado no cambia en absoluto el estado común.
   (claude1, lema 2; claude2, 3.4; gpt1, §2; ds2, 6.1. Coinciden todos los críticos; el crítico ChatGPT
   corrigió la fórmula de ds2 a `1 + n·a` en lugar de `(1 + a)·n`.)
3. **Muestreo de celdas sin codificación.** Si el nodo lee en promedio `s` de `N` celdas sustituibles de forma
   independiente (capas, posiciones, secuencias), habrá una celda que verifica
   con probabilidad no mayor que `s/N`; su sustitución pasa con probabilidad no menor que `1 − s/N`.
   (claude2, 3.2; gpt2, 9.2; gpt1, 5.4; claude1, I2. El crítico Claude señaló una laguna de rigor para
   el verificador cuyas monedas dependen de la raíz de la traza; la conclusión no cambia por ello.)
4. **Verificación por muestreo y margen del ejecutor.** Para una declaración falsa `σ` con gastos `c_σ` y suma
   en espera `H`, D1 frente a la inacción exige `π(σ) ≥ (R − c_σ)/(R + H)`, donde `π` es la probabilidad
   de detección. Para una falsificación barata y una cuenta vacía hace falta `π ≈ 1`, es decir, verificación completa. Para
   una falsificación casi honesta hace falta una proporción de verificación no menor que `m/(1 + m)` con margen `m`. Para una clave
   con `H > 0` y verificación de un bloque de `L + 1` hace falta `H ≥ R·((L+1)/m_s − 1)`: 36R para 36 capas
   y 64R para 64 capas con un solo bloque verificado [cálculo]. La aleatoriedad fresca del nodo hace `π`
   independiente de la colusión, pero no la hace igual a uno. (claude1, lema 3; claude2, 3.11, obtenido
   de forma independiente. Coinciden todos los críticos. El crítico ChatGPT precisó: con verificación obligatoria del bloque de salida
   el umbral para un intento casi gratuito es 35R.)
5. **Verificaciones lineales fijas sobre el campo.** `t < n` verificaciones lineales
   fijadas de antemano tienen un núcleo común no nulo: un error de ese núcleo no lo ven. Un vector uniforme fresco,
   elegido después de la fijación, deja pasar un error fijo no nulo con probabilidad
   no mayor que `1/p`. Sobre enteros acotados la cota no es aplicable (véase 2.2, punto 3). (gpt1, 5.2;
   gpt2, 9.1; claude2, 3.5; ds2, 5.2; claude1, B4.)
6. **Error nulo equivale a determinismo.** Una verificación con cero aceptaciones falsas para cualesquiera monedas
   se convierte en determinista al fijar las monedas. (claude2, 3.6.)
7. **Aleatoriedad común con colusión total.** Con `q = 1`, una aleatoriedad común a todos los nodos solo es posible
   desde fuera de la red (faro externo o Fiat–Shamir); el intercambio de compromisos entre nodos de SkyNet
   no ayuda. Las monedas personales de nodos distintos dan decisiones distintas, y no se obtiene un cálculo único.
   (claude2, 3.8; gpt2, 6.1. El crítico ChatGPT añadió: el faro debe ser no desplazable, accesible
   y revelarse estrictamente después de la aceptación final del bloque; esto ya es el ataque 1.5 y N13
   en [THREAT_MODEL](THREAT_MODEL.md).)
8. **Repeticiones gratuitas.** Si el intento se puede repetir casi gratis (por ejemplo, la aleatoriedad
   se deriva del hash de la propia declaración), la probabilidad de éxito crece con el número de intentos. Para la elección de celdas
   no se puede usar Fiat–Shamir. (claude2, 3.3; ds2, 5.1.)
9. **El verificador que construye el resultado por sí mismo.** Si el nodo calcula él mismo todo el estado
   y lee la declaración solo para comparar, entonces, quitando la comparación, obtenemos un ejecutor honesto
   con el mismo trabajo. Por tanto, esa verificación cuesta no menos que el 100% del trabajo óptimo. Solo puede ser barata
   una verificación con una pista: una respuesta lista, una traza o una prueba.
   (gpt2, 9.5. Los críticos Claude y DeepSeek llamaron a esto la mejor formulación de la cota general.)
10. **Certificado del token ganador.** Para un estado oculto de posición general no se puede certificar
    al ganador sin obtener información sobre cada fila del vocabulario que pueda ganar. En el peor
    caso se verifica todo el vocabulario. (claude1, B6; gpt2, 9.3.)
11. **Entrada privada.** Un nodo ajeno sin la petición no puede verificar la respuesta si no hay
    una prueba de conocimiento cero. El crítico ChatGPT precisó la cota: un compromiso
    ocultador junto con esa prueba podría transmitir la propiedad necesaria, y el lema
    no lo excluye. (claude2, 3.7; ds2, 6.2; gpt1, §1.)

### 2.2. Afirmaciones de imposibilidad que los críticos refutaron

1. **«La letra de D1 exige un error exactamente nulo»** (ds1, F1). Es cierto solo si el intento no
   cuesta nada. Si la aleatoriedad es externa e impredecible, y cada intento exige una nueva fijación
   y cuesta `c_min > 0`, entonces `Δ₀ ≤ εR − c_min ≤ 0` con `ε ≤ c_min/R` (claude1, lema 4; ds2, 5.1).
   El propio candidato de ds1 también se apoya en un hash con error mayor que cero. Lo refutaron los tres
   críticos. Salvedad del crítico ChatGPT: la cota inferior del precio del intento más barato para cualquier
   coalición el proyecto aún no la ha establecido, por lo que un error pequeño es compatible con D1 solo de forma condicional
   (pregunta 2 de la sección 6).
2. **«La verificación de una respuesta lista cuesta +100% del tiempo por definición»** (ds1, F2). Es falso para
   una respuesta lista: al verificar todas las posiciones en una sola pasada, los pesos se leen una vez, y no por cada
   token. Por número de operaciones la verificación es efectivamente igual a la generación, pero por tiempo, al generar
   una respuesta a la vez, puede ser decenas de veces más rápida. Además, ds1 comparaba
   perfiles de pesos no comparables. Lo refutaron los tres críticos.
3. **«La verificación lineal exacta exige no menos de `N` formas y `N²` operaciones»** (ds1, F3). Es falso
   por partida doble: los coeficientes frescos tras la fijación dan un paso con probabilidad de alrededor de `Q^(−s)`, y sobre
   enteros acotados basta una forma con empaquetado de bits `Σ y_i·B^i` con `B > 2U`
   (gpt1, 5.3; gpt2, 6.2); la matriz identidad lee las coordenadas en `O(N)`. Lo refutaron los tres
   críticos.
4. **«El tráfico mínimo de la verificación de una respuesta es igual al tamaño de la traza de cálculo»** (conclusión del lema 5.3
   de ds2). La verificación de una respuesta lista solo necesita los tokens de la respuesta, y el verificador de una prueba breve
   lee la prueba y las raíces, no los datos mismos. Lo refutaron los tres críticos.
5. **«Cualquier generación honesta está obligada a ejecutar tantas operaciones como la verificación en una sola
   pasada»** (claude1, §4.1 y B5). Es una cota superior del precio de la verificación, no una inferior (crítico
   Claude), y no se cumple si el ejecutor tiene una caché legítima del resultado listo
   (crítico ChatGPT).
6. **«La verificación exacta barata es imposible sin aleatoriedad secreta o criptografía»** (claude2, 3.5).
   Contraejemplo: la ecuación normal exacta de la regresión ridge sobre números racionales
   se verifica de forma determinista (crítico ChatGPT).

### 2.3. Cotas discutibles o condicionales

- **Tamaño del examen `n ≳ 2σ²·ln(1/ε)/δ²`** (claude2, 3.10). Los críticos Claude y DeepSeek la aplican
  como estimación de trabajo. El crítico ChatGPT mostró que de una sola varianza no se puede derivar el `n` necesario
  para cualquier distribución: hacen falta alternativas dadas y una unidad de muestreo independiente.
  **Discutible**: sirve como estimación en el modelo nombrado, no como teorema.
- **Barrera cuantitativa de la prueba completa** (claude2, 3.9): el presupuesto del 5% deja alrededor de 1–5,
  el del 20% alrededor de 6–18 operaciones en el campo por celda no lineal, mientras que las construcciones conocidas
  de redondeo cuestan decenas, y softmax, cientos [cálculo con costes supuestos]. Todos
  los críticos coinciden en que esto es una cota de las construcciones conocidas, no un teorema.

---

## 3. Respuesta del modelo (a)

### 3.1. Todos los mecanismos considerados

El «precio» se indica como recargo sobre el trabajo de la ejecución honesta; todas las cifras son [cálculo] según los parámetros
de los trabajos. El «veredicto» es el resultado tras las tres críticas y teniendo en cuenta D6–D17.

| Mecanismo (trabajos) | Esencia | Garantía y supuestos | Datos del nodo | Colusión y contraejemplo | Precio [cálculo] | Veredicto |
|---|---|---|---|---|---|---|
| **Repetición completa por cada nodo**, pasada causal sobre la respuesta lista (los seis) | El nodo con la entrada calcula él mismo todas las posiciones y verifica cada token y la primera causa de parada | Error nulo con perfil exacto, entrada auténtica y núcleo en buen estado | Petición, respuesta, modelo, perfil, semilla | La colusión no ayuda: decide su propio recálculo | Alrededor del 100% de las operaciones para cada uno de los `N` nodos; un nodo ajeno no ve la petición privada | **Se sostiene** como referencia; no entra en el 5% con verificación por todos los nodos |
| **I1 / PPS** (claude1): verifica el pagador | El pagador en una sola pasada recalcula la petición y la respuesta en el perfil entero «INT-canónico»; el pago procede solo de su prepago; no hay emisión ni peso por la petición pagada | Error nulo con A1 (los mismos bits en equipo distinto **y** en la decodificación token a token y en la pasada de toda la secuencia en una misma tarjeta), A2 (el registro almacena), A3 (hash, cifrado), A4 (el pagador publica la prueba de error en plazo), A5 (los datos de la disputa están disponibles) | Petición, respuesta (`T·4` bytes), huellas del modelo y del perfil, semilla; pesos en memoria 4,02 GB para 4B W8, 12,8–25,6 GB para 27B | Decide el único participante cuyo dinero está en juego; la colusión «pagador + ejecutor» solo traslada sus propios créditos | 4B, 500/500, RTX 2060: 3,98·10¹² MAC, 0,19 s frente a 7,5 s de generación — alrededor del 2,5–2,6%; todos los escenarios 1,2–3,8% con generación de una respuesta a la vez; 8–22% con lote de 8; 21–48% con lote de 32. Sin GPU, alrededor de 8 s por 1000 tokens en el procesador — 100–300% | **Se sostiene con correcciones** (los tres críticos); correcciones en 3.2 |
| **I8 — disputa por las raíces de las capas** (claude1) | El ejecutor fija las huellas del flujo residual por capas. El pagador encuentra el primer bloque donde el recálculo diverge y publica su entrada; cada nodo recalcula un bloque. Sin prueba en la ventana, el pago va al ejecutor | No hay prueba falsa de error con A1; un rechazo falso del pagador es imposible | Entrada del bloque (10–20 MB con 1000 posiciones), pesos de una capa (101–388 MB) | Cada nodo decide la verificación por sí mismo. Contraejemplos: el ejecutor pone en el registro solo la huella del criptograma y no entrega la respuesta misma; el registro es igual con la respuesta entregada y con la retenida; la censura del bloque en la ventana depende de validadores externos | Alrededor de 1,0·10¹¹ MAC por nodo para 4B, 3,9·10¹¹ para 27B; con 1000 nodos, una disputa falsa supone del orden de 10–20 GB de tráfico de red (estimación del crítico Claude) | **Se sostiene con correcciones**: criptograma en el registro, límite de disputas falsas, puntualidad y censura como supuestos nombrados |
| **M1 — Freivalds del pagador con vector secreto** (ds2) | El pagador recalcula las operaciones elemento a elemento y verifica las multiplicaciones de matrices con productos escalares sobre su vector secreto fresco | Error no mayor que `N/p` en todas las igualdades, despreciable con `p ≈ 2⁶¹`; hacen falta verificación de rango y sumas brutas antes del redondeo | Traza de cálculo del ejecutor | Verifica el propio pagador. Contraejemplo al almacenamiento en caché del vector: conociendo el vector de una capa, el ejecutor controla la salida de esa capa en todas las peticiones futuras (crítico DeepSeek) — el vector debe ser fresco en cada petición | Se declara 2,7%; no se reproduce: softmax 0,79%, no 2,45%, y con un precio de la multiplicación en el campo de 10–100 MAC las proyecciones dan +1,6–15,8% (crítico DeepSeek). El tráfico es **discutible**: alrededor de 14 MB por token con int32 brutos y alrededor de 15 GB de traza de una petición de 1850 tokens (crítico Claude); 7,419 MB por token incluso en INT16 y 7,477 GB de prellenado (crítico ChatGPT); alrededor de 2,4 MB por token si el propio pagador recalcula las puntuaciones de atención (crítico DeepSeek) | **Se sostiene como verificación** para un pagador sin GPU pero con canal rápido; el precio declarado queda refutado |
| **I2 — capas por muestreo** con aleatoriedad fresca del nodo (claude1; ds1, 3.1; gpt2, §8) | El nodo verifica `m_s` capas aleatorias de `L` por las huellas | Paso de un error único con probabilidad `1 − m_s/(L+1)` | Entrada de la capa, pesos de la capa | Falsificación: respuesta con un modelo pequeño más una traza honesta del grande; se distorsiona una transición y luego una continuación coherente | Hash de la traza 0,38–4 GB; 1–8% en el ejecutor según la velocidad del hash | **Refutado** para la cuenta vacía (cota 2.1, punto 4); sirve solo para claves con `H ≥ 35–64R` |
| **PVYa** (claude2): el usuario verifica una muestra de celdas «bloque × token» con su aleatoriedad secreta | La celda se elige en proporción a su parte de las operaciones | Solo el beneficio monetario, no el daño | Celdas de la traza, camino en el árbol de huellas | Contraejemplo del crítico Claude: respuesta con un modelo pequeño y traza de prellenado honesta; la falsificación barata en tiempo se detecta con probabilidad de alrededor del 0,3–1%, `Δч ≈ +0,94c`. Crítico ChatGPT: en el modelo de costes iguales `Δ₀/c = +0,019`; también hace falta la vinculación de claves y valores de atención al prefijo | Para el usuario, de <0,001% a 2,7%, la variante estricta alrededor del 5,6%; para el ejecutor, el hash de una traza de unos 4 GB — 2–4 s de procesador, 30–50% del tiempo de la petición en RTX 2060 | **Refutado** (críticos Claude y ChatGPT). El crítico DeepSeek lo aceptaba separando las variantes estricta y relativa, pero la variante relativa no cumple la formulación bilateral de D1, y por D6 hace falta también una garantía frente al daño, que PVYa no ofrece |
| **I3 — Freivalds sobre la traza** por un nodo de la red (claude1; ds1, 2.2; gpt1; gpt2, 6.1) | Verificación de cada multiplicación con un vector aleatorio sobre la traza enviada | `≤ 1/p` por error; hacen falta salidas brutas antes del redondeo | Toda la traza | La colusión no ayuda si el vector es fresco | Traza de 4,4 GB por respuesta (4B), 15,2 GB (27B); para prellenado de 4096 posiciones, solo gate/up — 5,74 GB en INT16 frente a 0,755 GB en la estimación de ds1 (crítico ChatGPT) | **Refutado como verificación barata**: choca con el tráfico, no con la aritmética |
| **I4 — tablas de sumas parciales** (los seis) | El nodo construye de antemano tablas de salidas de una capa por grupos de entradas | Exacto con pesos canónicos | Tablas | — | Grupo 2: 859 GB por una matriz de 4B, alrededor de 476 TB todo el cuerpo; los planos de bits — no menos de 128 tamaños del modelo | **Refutado por el cálculo** (todos los críticos) |
| **I5 — certificado del token ganador** (claude1; ds1, 2.5; gpt1, 4.3; gpt2, 5.3) | Árbol de clústeres de filas de la cabeza con cotas superiores demostradas | Exacto para la elección voraz con cobertura completa del vocabulario y estado oculto verificado | Estado oculto de la última capa | Un estado oculto sustituido certifica otro token | Ahorra no más que la parte de la cabeza: 2,10% / 0,60% (gpt1), 6,04% / 1,76% (gpt2), hasta 9,67% (claude1); en el peor caso, todo el vocabulario | **Se sostiene como parte** de la verificación (elección voraz) |
| **Gumbel-max como muestreador canónico** (claude1; claude2, 5.5) | La elección con temperatura se reduce a `argmax(z/τ + g)` con ruido de PRF a partir de la semilla | La identidad es correcta | Semilla | La distribución difiere del top-p/top-k habitual: es un cambio de producto | Ruido fresco por cada token: alrededor de `V` valores de PRF y máximos de grupo, 75,97 millones de valores de PRF por 500 tokens | **Se sostiene** como modo de fijar la elección; el ahorro del certificado para el muestreo **no está justificado** (críticos DeepSeek y ChatGPT) |
| **Certificado de Gumbel «con margen»** (claude2, 5.5) | Se acepta el token casi ganador dentro de una tolerancia | — | — | Contraejemplo: con logits iguales y una diferencia de ruido menor que `2η` pasa un token incorrecto (crítico ChatGPT); cualquier tolerancia abre la sustitución (ds2, 6.4) | — | **Refutado** |
| **Certificado de intervalo con recálculo exacto en caso de ambigüedad** (gpt1, 4.4; gpt2, 5.4) | Aproximación de bajo rango de la matriz congelada y cota demostrada del resto; donde el intervalo admite redondeos distintos, el nodo recalcula de forma exacta | Error nulo con normas del resto calculadas de forma independiente y recálculo obligatorio | Sus propios factores y normas del resto | No se pueden tomar claves y valores del mensaje del ejecutor | Pasada rápida del 0,521% de las operaciones de la capa; para el 5%, la proporción de salidas ambiguas no es mayor que 4,479% en una capa caliente y 1,342% con preparación en frío (crítico ChatGPT). Crítico Claude: con pesos cercanos al rango completo, los intervalos casi con seguridad cubren muchas celdas, y el precio se acerca al 100% | **Se sostiene** matemáticamente; el **precio es discutible**, no demostrado |
| **Empaquetado de bits exacto** (gpt1, 5.3; gpt2, 6.2) | Una sola forma lineal `Σ y_i·B^i` sobre enteros | Exacto con `B > 2U` y rangos demostrados | Sumas brutas | Pequeña búsqueda exhaustiva: con `B = 8`, 9 aceptaciones correctas y 0 falsas; con `B = 4`, 20 falsas de 29 (repetida por dos críticos, los hashes coincidieron) | Casi sin ganancia: para W8A16 con anchura 3072, una palabra de 64 bits por salida | **Se sostiene** como primitiva exacta, no aporta abaratamiento |
| **Caché de prefijos verificados** (gpt2, 5.1) | El nodo reutiliza el estado que él mismo derivó | Exacto para la misma posición y versión | Su propia caché | Una raíz ajena puede vincular un estado incorrecto | Ganancia solo en las repeticiones; la misma caché está disponible para el ejecutor | **Se sostiene**, en general no abarata |
| **Pruebas breves sumcheck/GKR** para la respuesta (claude1, I6; claude2, 4.9 y 5.7) | El ejecutor prueba toda la pasada; cada nodo verifica la prueba | Garantía computacional; no se ha derivado una cota de error de extremo a extremo para el grafo de Qwen | Prueba, pesos para la evaluación en un punto aleatorio | La colusión no ayuda con un esquema completo y entradas verificadas | Referencia FlashProve 70–95× su propio perfil (denominador poco claro); estimación de claude2 — 6–20 veces más caro que el trabajo con contexto 2048; en la mejor lectura, alrededor de 16,8× (crítico ChatGPT) | **Se sostiene** como garantía condicional; **no entra** en el 5% |
| **Cambiar la tarea: pagar por un resultado verificable** (claude1, I7; claude2, 5.4; gpt1, 3.1; gpt2, 4) | Por ejemplo, un vector que satisface una fórmula SAT, código que pasa las pruebas, una solución con respuesta verificable | Exacto para su predicado | Tarea y resultado | El ejecutor puede enviar un resultado correcto que el modelo no produjo; por D2 esto es admisible | Verificación SAT — no más de `3m` lecturas | **Se sostiene para una clase estrecha**; la proporción de tales peticiones es desconocida; el diálogo libre no está cubierto |
| **P0 / M4 — la petición pagada no da emisión ni peso** (claude1, claude2, ds2) | El dinero solo pasa del pagador al ejecutor | La transferencia de sus propios créditos es neutra dentro de la coalición | — | Sin esta regla, la verificación por el pagador no protege la red (cota 2.1, punto 2) | 0 | **Se sostiene**; concuerda con D17 |
| **Verificador por lotes de un nodo dedicado, pago solo del prellenado** (ds1, 3.3–3.4) | Un solo nodo verifica el paquete; se paga el prellenado exacto | — | — | La firma del nodo dedicado es igual con una verificación real y con una simulada; el prellenado exacto con una respuesta inventada pasa | — | **Refutado** (crítico ChatGPT) |
| **Producto de las probabilidades de error de nodos distintos** (ds1, 3.2) | Cada nodo verifica con su propia aleatoriedad | — | — | Funciona solo con aceptación obligatoria por todos los nodos honestos; con `q = 1` no hay tales | — | **Refutado** |
| **Disputa abierta en la ventana** (los seis) | Cualquiera puede objetar antes de que expire la ventana | Hace falta un observador honesto con datos y tiempo | — | Si callan todos los que vieron los datos, el resultado falso pasa con probabilidad 1; el piloto lo mostró | Piloto: 93 transacciones y 5,8–6,3 millones de gas en una disputa de Cartesi | **Refutado** como verificación independiente de la colusión; además D8 limita el círculo de quienes disputan |
| **Delegación por un pagador débil** (claude1, 4.10) | El pagador encarga la verificación a su propio dispositivo o a un nodo elegido | La confianza en el elegido es un supuesto del pagador | — | Con elección aleatoria vuelve la dependencia de `q` | — | **Supuesto**, no solución |

### 3.2. Mejor candidato para la respuesta del modelo y correcciones de los críticos

**Candidato.** Toda la respuesta la verifica el propio pagador. Si tiene una tarjeta gráfica en la que
cabe el modelo, es PPS (claude1). Si no hay tarjeta gráfica pero sí un canal rápido, es M1 (ds2)
con un vector secreto fresco por cada petición. En ambos casos, la petición pagada no da emisión de
créditos ni peso (P0; esto concuerda con D17), y la disputa la decide cada nodo según la prueba de error
(I8). Por qué la colusión no ayuda: la decisión la toma el único participante cuyo dinero está en juego;
tiene todos los datos — la petición, la respuesta y el modelo; la verificación es completa, no por muestreo.

**Correcciones sin las cuales el candidato no se sostiene.**

1. **Retención de la respuesta.** En el registro hay que poner el propio criptograma de la respuesta, y no solo su huella:
   alrededor de 2–4 KB por respuesta (crítico Claude). Esto concuerda con D10: el intercambio con una sola entrada del registro.
2. **Disputas falsas.** La coalición «pagador = ejecutor» puede crear cuantas peticiones pequeñas quiera
   y presentar por cada una una disputa que todos los nodos descargan y recalculan. D8 limita el flujo de disputas
   al número de peticiones, pero las peticiones autopagadas no quedan limitadas por ese tope. Ningún trabajo dio una solución
   (sección 5, tarea M9).
3. **Puntualidad y censura.** El pagador debe estar en la red y lograr publicar
   la prueba dentro de la ventana, y el registro debe aceptarla. La censura del bloque en la ventana depende de la honestidad
   de los validadores externos del registro. Es un supuesto sobre la colusión en otro conjunto, y hay que nombrarlo
   abiertamente. Para el teléfono del pagador se incumple con más frecuencia. La ventana según D12 se cuenta en tiempo activo
   de la red.
4. **Vinculación de los extremos.** La disputa sobre la primera capa exige la vinculación a la petición privada original; la disputa
   sobre la última, al criptograma pagado (crítico ChatGPT).
5. **Parada.** Hay que verificar la primera causa de parada. La condición «el último token es EOS o
   se alcanzó el límite» deja pasar una respuesta ampliada después de un EOS temprano (crítico ChatGPT).
6. **Aritmética del INT-canónico.** El producto de las probabilidades de atención por los valores en la especificación
   se acumula en int64. Si no se ejecuta en núcleos tensoriales, el precio del escenario largo
   2000/1000 sube del 3,8% a aproximadamente el 8% (estimación del crítico Claude); la salida es descomponer la probabilidad de 16 bits
   en dos mitades de 8 bits. El crítico ChatGPT encontró tres lagunas más: con una sola
   clave permitida, softmax da el valor 65 536, que no cabe en 16 bits; la suma de cuadrados
   en RMSNorm puede desbordar int64 (tres componentes de `2³¹−1` ya dan más que `INT64_MAX`); hacen falta
   anchuras explícitas, posiciones de RoPE y orden de redondeo. El principio mismo resiste estas correcciones.
7. **Entrega en flujo.** Por D6, el usuario no debe ver texto no verificado como verificado.
   Con entrega en flujo, cada prefijo mostrado debe estar verificado, y la frecuencia de esas verificaciones
   entra en el precio (gpt2, §1).

**Limitaciones del candidato.**

- El precio 1,2–3,8% es válido solo con generación de una respuesta a la vez. Al ejecutor le conviene
  unir peticiones en paquetes, y con un lote de 8–32 la comparación honesta da 8–48% [cálculo].
- El candidato no cubre al consumidor sin equipo. Para 27B el pagador necesita no menos de
  13 GB de memoria de vídeo. El consumidor principal según los requisitos es el participante sin equipo. Por D6 su
  respuesta solo puede entregarse con la marca «no verificado»; cómo pagar entonces al ejecutor
  sin infringir D1, ningún trabajo lo resolvió.
- Todo se apoya en el supuesto no medido A1: la coincidencia de bits en tarjetas gráficas distintas **y** entre
  la decodificación token a token y la pasada de toda la secuencia en una misma tarjeta. Si en Qwen3.5
  hay capas recurrentes de atención lineal, su forma paralela redondea de otro modo, y el precio
  de la verificación puede crecer aproximadamente el doble (claude1, 3.4, estimación con 10 µs por paso supuestos).
- La disputa revela la petición: la entrada del bloque reconstruye el texto casi de forma reversible. No hay disputa sin revelación.
- La energía no está medida: al chocar con el cálculo, la tarjeta gráfica consume más que al chocar con la memoria,
  por lo que la proporción por energía puede ser mayor que la proporción por tiempo.
- Los aceleradores (certificado de intervalo, certificado del ganador para la elección voraz, caché de prefijos propios)
  son admisibles solo por encima de la verificación completa, no en su lugar.

---

## 4. Paso de entrenamiento (b)

### 4.1. Todos los mecanismos considerados

La diferencia principal con la respuesta del modelo: el paso de entrenamiento no tiene un pagador cuyo dinero esté en juego. El pago
va por emisión de créditos, por lo que, según la cota 2.1, punto 2, la base debe verificarla cada nodo
completo. Por D15, además, ese recálculo simple no se paga.

| Mecanismo (trabajos) | Esencia | Garantía y supuestos | Datos del nodo | Colusión y contraejemplo | Precio [cálculo] | Veredicto |
|---|---|---|---|---|---|---|
| **T1 — repetición completa de la transición** por cada nodo (los seis) | El nodo repite el paso desde el padre aceptado y compara todo el estado siguiente, incluidos los pesos maestros, los momentos m, v del optimizador y el número de paso | Error nulo con perfil exacto y datos auténticos | Padre, porción de datos, reglas | Verificar solo los pesos es poco: los mismos pesos con v reiniciado cambian el paso siguiente (crítico ChatGPT) | +100% para cada nodo, en total `N × 100%`; por ejemplo, alrededor de 2,62·10¹⁵ MAC para recalcular una porción de 64 × 4096 de 4B | **Se sostiene** como referencia; no entra en el 20% |
| **T2 — capas, micro-lotes y pasos por muestreo** (claude1; ds1, 3.1) | El nodo verifica una parte aleatoria del paso | Paso de `1 − m_s/L` | Parte de la traza | Falsificación: entregar una actualización aleatoria o copiada; sustituir un gradiente de frontera | Con `N = 1000`, 36 capas y una capa verificada, alrededor de 28 trabajos por paso | **Refutado** (cota 2.1, punto 4) |
| **VYa-S** (claude2): el faro elige celdas «bloque × secuencia», cada nodo verifica su prueba comprimida | Probabilidad de pasar `(1 − f)^s` con proporción de falsificación `f` | Faro externo, hash, prueba de la celda; solo el beneficio monetario, no el daño | Pruebas de las celdas elegidas | Crítico Claude: copiar la traza de una secuencia a toda la porción — solo son incoherentes las celdas de vinculación (alrededor del 10,5% del peso); con `s = 30` `Δ₀ ≈ +0,036R`, con `s = 10` `Δ₀ ≈ +0,33R` y `Δч ≈ +0,26c`. Crítico ChatGPT: un gradiente nulo en la frontera del bloque hace que todas las celdas inferiores sean internamente correctas; en la fórmula se sustituyó la proporción de trabajo ahorrado en lugar de la proporción de igualdades incorrectas; incluso con igualdad, `Δ₀/c ≈ +0,096`. Crítico DeepSeek: solo se cumple `Δч ≤ 0`, y D1 exige también `Δ₀ ≤ 0` | Pruebas 0,66%, recuento repetido de entradas 0,39%, hash 3,7–10% con `s = 30`; fronteras de capas — 96,64 GB por tarea de 64 secuencias y 11,60 TB por tarea de 7680 | **Refutado en su forma actual** (los tres críticos). La reparación propuesta — una verificación aparte de la vinculación sobre secuencias aleatorias; no calculada |
| **T3 — prueba breve del paso** sumcheck/GKR con compromisos (claude1, T3; claude2, 4.9; ds1, 2.9; gpt1, 6.3; gpt2, 7.2) | El ejecutor prueba toda la transición, cada nodo verifica una sola prueba | Garantía computacional con esquema completo con vinculación de la entrada, redondeos, rangos y optimizador; no se ha derivado la cota de error de extremo a extremo | Prueba, raíces, una pasada por los pesos por paquete | La colusión no ayuda con un transcrito común | Referencia VeriLoRA alrededor de 137× (121,93 s de prueba por 0,89 s de entrenamiento, otro modelo de 3B); el presupuesto deja 11,43% — una brecha de alrededor de 1200×. Para el perfil 1.5B, una sola división exacta de softmax — 11 973 394 432 celdas del campo y 10 998 054 912 verificaciones de rango, 356,835 GiB antes de alinear; escritura de 3,067 TB a 100 GB/s — 30,67 s frente a 6,6 s del presupuesto con un paso de 60 s | **Se sostiene como dirección**; las disposiciones concretas quedan refutadas, el 20% no está demostrado. El crítico ChatGPT lo considera la rama de investigación más fuerte para un paso inalterado |
| **M1 para el entrenamiento** (ds2) | Vector secreto más recálculo de las operaciones elemento a elemento | Como en 3.1 | Traza | No hay vinculación de la traza a la porción asignada: un cálculo correcto sobre datos sustituidos pasa (crítico DeepSeek) | Se declara 1,5%; no se tienen en cuenta las operaciones inversas elemento a elemento (alrededor de ×2–2,5) ni el precio de la multiplicación en el campo. Tráfico de 16,08 GB por paso en INT16, 64,318 GB en INT64 — no menos de 514,5 s a 1 Gbit/s | **Refutado** para el entrenamiento por tráfico y vinculación |
| **Freivalds sobre la traza del paso** (ds1, 2.2; gpt2, 6.1) | Verificación de cada multiplicación del paso | `≤ p^(−t)` | Toda la traza | — | 64,3 GB por paso (1.5B); 123,92–410,44 GB para LoRA y 369,72–2073,34 GB para entrenamiento completo por paso (gpt2); no menos de 991 s a 1 Gbit/s | **Refutado** como verificación barata |
| **T5 — el paso como fórmula de actualización** (los seis) | Los nodos verifican los multiplicadores de la actualización, no la matriz nueva | Verifica solo la última suma | Multiplicadores | Contraejemplo: el gradiente enviado `G = 0` con el verdadero no nulo pasa la verificación de la fórmula | Alrededor de 10⁻⁶ del trabajo | **Refutado** como verificación del paso; el recálculo del optimizador y de la suma forma parte del núcleo |
| **Solo el delta de LoRA** (ds1, 3.5) | Verificar solo el adaptador | — | — | La salida de la parte congelada depende de la nueva entrada | — | **Refutado** |
| **T4 — pago por la mejora** medida por cada nodo en una muestra fresca (claude1) | La actualización se fija antes de la ronda; un faro externo elige `n` posiciones del examen; cada nodo calcula por sí mismo la diferencia truncada de pérdidas; se paga el exceso sobre el umbral de confianza | Pago de una actualización sin mejora con probabilidad `≤ ε = 2⁻⁴⁰` con faro externo, muestreo con reemplazo, perfil exacto y fijación antes del faro; el precio del intento debe ser no menor que `ε·κ·B/2` | Fondo del examen, todas las `K` actualizaciones de la ronda | No hay verificadores, calcula cada nodo. Contraejemplos: (1) el truncamiento de las diferencias paga una actualización dañina: +0,01 nat en el 99,5% de las posiciones y −20 en el 0,5% dan tras el truncamiento +0,005 frente a un verdadero −0,09 (crítico Claude); +0,1 en el 99% y −100 en el 1% dan +0,089 frente a un verdadero −0,901 (crítico ChatGPT); (2) el fondo público permite aprender directamente sobre él; (3) un duplicado con ruido, al fusionarse por suma, da una contribución positiva | Umbral con `B = 2`: 0,0745 nat con `n = 10⁴`, 0,0236 con `n = 10⁵` (Hoeffding). Para ajustarse al 20% hacen falta `D ≥ n(1 + K·a)/0,6` tokens de entrenamiento por nodo y ronda; con `K = N = 10⁴` son 1,85·10⁸ tokens, alrededor de 26 h. Caché de estados — 0,51 GB según la estimación de claude1 o 524,3 GB en int16 si las posiciones se toman de prefijos distintos de 1024 tokens (crítico ChatGPT) | **Se sostiene con correcciones** como nueva unidad de pago; no verifica el paso. Es discutible si es peligrosa la revelación selectiva de candidatos tras el faro: el crítico Claude dice que no con `ε = 2⁻⁴⁰`, el crítico ChatGPT que no se ha tenido en cuenta |
| **ODU** (claude2): pago por la mejora demostrada en un examen elegido por el faro después de la fijación | El presentador prueba el examen; cada nodo verifica la prueba en lugar de recalcular | Como T4, pero elimina el crecimiento del precio con el número de nodos; el entrenamiento puede llevarse en cualquier aritmética | Prueba del examen | Crítico Claude: el presentador calcula el examen gratis en su equipo y prueba solo a los candidatos ganadores, por lo que hace falta `ε ≲ 0,23%`, no 10%. Crítico ChatGPT: el mismo argumento, más la selección adaptativa sobre un examen común y que el pago por la cota de confianza no se suma telescópicamente (0,16 en lugar de 0,20 en el ejemplo). Crítico DeepSeek: `ε = 10%` pasa formalmente, pero solo a costa de todo el presupuesto del 20% | Prueba del examen alrededor de 2,4 h por candidato, en serie: con 100 candidatos la época no es más corta que 10 días (crítico Claude). La parte del examen es 0,655% de los tokens de entrenamiento, 0,327% si se prueba también al padre — alrededor de 858 tokens, menos que una secuencia de 4096 (crítico ChatGPT) | **Se sostiene con correcciones** como armazón; `ε` es **discutible** (2 de 3 críticos: hace falta mucho menos del 10%); la atribución no está resuelta |
| **Examen de ds1** (ds1, 2.8): 20–82 tokens, «error nulo» | Se paga la mejora en un examen pequeño | «Error nulo» solo por definición | — | Ruido de la media alrededor de 0,28 nat en 82 tokens con una mejora del paso de 10⁻⁴–10⁻³ (crítico DeepSeek) — se paga el ruido; la fuente de aleatoriedad no se nombra; el examen no ve los momentos sustituidos del optimizador | Se declara +1–3%; con el contexto completo de cada uno de los 20 tokens evaluados — 103,4% de la estimación matricial del paso (crítico ChatGPT) | **Refutado** |
| **Paso amortiguado de Gauss–Newton con certificado dual** (gpt1, 6.4) | Nuevo optimizador; el ejecutor da un vector corto, el nodo prueba cada bit del paso redondeado con `4λδ² > η²‖r‖²` | Error nulo para el nuevo paso con un modelo lineal dado | Forward exacto y dos pasadas de derivadas | Un empate en la frontera exacta de redondeo exige una solución exacta (crítico ChatGPT) | `3N/(2k+2)`: 8,82% con `k = 16` y `N = 1`, 75% con `k = 1`; con `N = 100` — cientos por ciento | **Se sostiene** como contrato modificado; el precio crece con `N`, la calidad es desconocida |
| **Característica exacta: regresión ridge, cabeza lineal** (claude1, T6; claude2, 4.1; gpt1, 3.2; gpt2, 4; ds1, 2.1; ds2, M2) | El nodo verifica la condición de óptimo `Xᵀ(Xw − y) + λw = 0` | Exacto con características auténticas | Características, etiquetas | Las características hay que verificarlas aparte; en M2 de ds2 falta el término `λw`, y un óptimo incorrecto pasa (crítico ChatGPT) | 44,4% con rango 8 y 12,1% con 32 respecto a la construcción de la matriz (gpt1); 0,390% en otra disposición (gpt2) | **Se sostiene para una tarea estrecha**; no es entrenamiento de Qwen, la proporción de ese trabajo es desconocida |
| **Varios primeros pasos LoRA distintos** (gpt2, 7.3) | Con adaptador nulo, las partes comunes se calculan una vez | Exacto | Caché común | No se traslada a los pasos siguientes | 16,70% para seis inicios permitidos frente a seis arranques en frío | **Se sostiene**, aplicabilidad estrecha |
| **Entrenamiento de orden cero** (claude2, 5.8); **campo pequeño en núcleos tensoriales** (claude2, 5.11); **caché del prefijo congelado y LoRA en los bloques superiores** (claude1; claude2, 5.9) | Reducciones de coste | — | — | El orden cero cambia el optimizador; el campo pequeño no da el error declarado sin cotas de rango | Caché del prefijo — alrededor de 20,97 TB por un millón de secuencias de 4096 | Ideas; **no demostradas** |
| **T7 — disputa abierta** (los seis) | — | Hace falta un observador | — | Para el entrenamiento no hay un observador interesado | — | **Refutado** |

### 4.2. Mejor candidato para el paso de entrenamiento y sus limitaciones

**No hay verificación del propio paso dentro del 20% que no dependa de la proporción de colusión.** Es un resultado
negativo general, confirmado desde distintos lados: la escala `N·v`, la traza de 64 GB–2 TB por paso,
las pruebas decenas o cientos de veces más caras que el trabajo, el presupuesto de operaciones elemento a elemento.

Con una **base de pago inalterada** quedan dos caminos: la repetición completa de la transición (referencia, +100%
por nodo) y, a largo plazo, una prueba obligatoria de todo el paso (T3). Para T3 hacen falta un grafo
concreto, una resistencia demostrada de la composición y una estimación completa; ahora no la hay.

Con un **cambio de la base de pago** (decisión del propietario, sección 6, pregunta 1) el mejor candidato es
la combinación de T4 y ODU con las correcciones de los críticos:

1. El examen lo elige un faro externo estrictamente después de la fijación de todas las actualizaciones y de la aceptación final
   del bloque.
2. El umbral se toma de una cota estadística con un `ε` criptográficamente pequeño (como en T4), y no del 10%.
3. El examen se verifica con una prueba (armazón de ODU), para que el precio no crezca con el número de nodos.
4. Las pérdidas se limitan con la propia aritmética (la probabilidad mínima del perfil) y no se truncan,
   pues de lo contrario se pagan actualizaciones dañinas.
5. La atribución de los duplicados hay que resolverla sin una cadena secuencial de pruebas. Ningún trabajo lo
   resolvió.

**Limitaciones.**

- No es una verificación del paso. El examen no ve los momentos del optimizador, no certifica el origen de la
  actualización y no excluye el entrenamiento sobre el propio examen.
- Por D6, un paso falso no debe entrar en el modelo. La mejora en el examen no demuestra la ausencia de daño
  en peticiones raras ni de puertas traseras (Q4 en [OPEN_QUESTIONS](OPEN_QUESTIONS.md)). El candidato limita
  el beneficio monetario, pero no el daño.
- No se sabe si la mejora honesta de una actualización supera el umbral: el ruido de la diferencia de pérdidas `σ`
  no está medido. Si no lo supera, los participantes honestos no reciben pago, y se infringe R6.
- Los dispositivos débiles con una actualización pequeña no superan el umbral; «toda la potencia libre aprende»
  se cumple solo como «aprende», no como «recibe pago».
- Relación con D9: el plan de entrenamiento ya se deriva de los resultados del examen. Esto convierte el examen en parte del
  núcleo, pero no resuelve la cuestión de si se puede pagar por la mejora en lugar del paso.

---

## 5. Qué no está demostrado y con qué comprobarlo

### 5.1. Qué no está demostrado

1. La coincidencia de bits del perfil entero en tarjetas gráficas distintas y entre la decodificación token a token
   y la pasada de toda la secuencia en una misma tarjeta (A1, pregunta Q2). De ello dependen PPS, M1,
   el certificado de intervalo y cualquier repetición exacta.
2. El tiempo de verificación de una respuesta lista respecto a la generación en tarjetas reales con lotes de 1, 8, 32;
   la energía; el comportamiento de las capas híbridas de atención lineal.
3. La calidad y la velocidad del perfil entero de Qwen3.5-4B respecto al habitual.
4. El precio del certificado de intervalo y del certificado del ganador con pesos reales.
5. La disponibilidad de los datos de la disputa, el límite de disputas falsas sin depósitos, la puntualidad y la censura del registro.
6. Para el pago por la mejora: la magnitud de la mejora honesta frente al umbral, la regla de atribución sin
   beneficio de los duplicados, la cota de pérdidas sin truncamiento, el precio de la prueba del examen.
7. Para la prueba breve del paso: la estimación completa de un paso y la cota de error de extremo a extremo.
8. La configuración exacta de Qwen3.5-4B y del modelo de unos 27B: todas las cifras de los trabajos se sustituyeron a mano.

### 5.2. Experimentos mínimos

La decisión D5 autoriza el primer experimento: el Qwen3.5-4B entero en una RTX 2060 del Linux doméstico
del acompañante, en su computadora y, con su consentimiento, en dispositivos de otros participantes mediante
miniagentes, después de la etapa 0. Los perfiles, las métricas y los umbrales se fijan antes de la medición. La coincidencia de bits
se refiere solo a las configuraciones probadas.

| Nº | Experimento | Qué se mide | Refuta al candidato si |
|---|---|---|---|
| O1 (D5) | Qwen3.5-4B entero en dos tarjetas gráficas distintas | Hashes de logits y tokens en un mismo conjunto de peticiones; el primer token no coincidente, EOS, empates, contexto largo, peticiones con logits cercanos | Un solo bit difiere con la misma especificación |
| O2 (D5) | Pasada de toda la secuencia frente a decodificación token a token en una misma tarjeta | La misma comparación de bits; aparte para las capas híbridas, si las hay | Un solo bit difiere |
| O3 (D5) | Velocidad: verificación de una respuesta lista frente a generación | Tiempo con lotes 1, 8, 32 y combinaciones entrada/salida 128/32, 128/128, 500/500, 2000/1000; implementación del producto de atención en 16 y 8 bits; memoria, tráfico | La proporción de la verificación con lote 1 es mayor que 5% |
| O4 (D5) | Velocidad del perfil entero frente al habitual en las mismas tarjetas | Tokens por segundo, memoria | La ralentización hace el servicio no rentable (fijar el umbral antes del experimento) |
| O5 (D5) | Calidad del perfil entero frente al habitual | El mismo conjunto de tareas | La pérdida de calidad es mayor que el umbral fijado de antemano |
| O6 (fuera de D5, hace falta autorización aparte) | Ruido de la mejora de un solo adaptador LoRA | Distribución de la diferencia de pérdidas base/adaptador de rango 16 tras un día de entrenamiento, `σ` y `δ/σ` | La mejora honesta es típicamente menor que el umbral con un tamaño de examen admisible |
| O7 (fuera de D5; la ejecución de sistemas de prueba está prohibida ahora por una restricción de investigación) | Precio de la prueba de un bloque forward de 4096 tokens | Coeficiente `P` | `P` es mayor que alrededor de 300 — entonces ODU y VYa-S no se ajustan (estimación de claude2) |
| O8 (fuera de D5) | Relación entre el precio de la multiplicación en el campo y el MAC tensorial en RTX 2060 y RTX 4090 | Coeficiente `R_f` | Decide todas las estimaciones de Freivalds y GKR |
| O9 (fuera de D5) | Energía de la verificación | Julios por verificación y por generación | La proporción por energía es mayor que la referencia |

### 5.3. Cálculos exactos que se pueden encargar a miniagentes

Son cálculos deterministas sin mediciones. Para cada tarea se fijan la versión del procedimiento,
los bytes de entrada o el generador con los límites de la búsqueda exhaustiva, los enteros o fracciones exactos, la serialización de la respuesta
y el SHA-256; el resultado se repite en un segundo dispositivo. La coincidencia confirma el cálculo, pero no
la semántica ni la desigualdad económica.

| Nº | Tarea | Parámetros | Qué resuelve |
|---|---|---|---|
| M1 | Inventario del grafo según el manifiesto fijado de Qwen3.5-4B y del modelo de unos 27B (el `config.json` publicado con hash) | Formas y tipos de todas las operaciones de relleno de contexto, generación, verificación de la respuesta y paso de entrenamiento; MAC, bytes de las sumas brutas, tiempo de vida de los búferes; capas híbridas; LoRA y entrenamiento completo | Precisa los numeradores y denominadores de todas las estimaciones |
| M2 | Tabla de la proporción de verificación `ρ(B)` según el modelo de «techo» | `L, d`, anchuras de atención y MLP, vocabulario, `P, T`, lote `B ∈ {1, 8, 32}`, ancho de banda de memoria, TOPS, proporciones de pico | Predicción para el experimento O3 |
| M3 | Cotas de desbordamiento del INT-canónico | Todos los acumuladores según la especificación, incluido el producto de atención hasta `T ≤ 32 768`, la suma de cuadrados de RMSNorm, el tamaño de la probabilidad en softmax; variante con dos mitades de 8 bits | Encuentra una entrada con desbordamiento o demuestra su ausencia |
| M4 | Tráfico exacto de M1 | int32 brutos y traza de la petición sobre la rejilla (entrada, salida, modelo); con y sin recálculo de las puntuaciones de atención por el pagador | Elimina la discrepancia de los críticos sobre el tráfico de M1 |
| M5 | Ola de falsificaciones para esquemas por muestreo con `H > 0` | `π = m_s/(L+1)`, `H₀` inicial, `R`, techo de tareas abiertas; búsqueda exhaustiva del tamaño y del número de olas | La `H*` mínima con la que una falsificación antes de la marcha no es rentable |
| M6 | VYa-S: búsqueda exhaustiva de estrategias de copia y entradas degeneradas | Proporción `f`, número de celdas `s`, pesos de las celdas, número de verificaciones de vinculación `s'`; antes y después de la reparación | La mayor `Δ₀`; si la reparación se sostiene |
| M7 | Economía de la prueba por muestreo y de la revelación en ODU y T4 | `e/R`, `P`, margen `m`, número de claves y candidatos | La mayor `ε` admisible |
| M8 | Escala de T4 | `D(N)` con `K = N`, `n`, `a`, `ε` | El límite del número de presentadores para el 20% |
| M9 | Precio de una disputa falsa de I8 | Tráfico y cálculos de la red en función de `N`, `P + T`, paso de las huellas `k` | Si hace falta un límite de disputas falsas y cuál |
| M10 | Tablas del umbral `t(n, ε, V̂)` | Hoeffding y Bernstein empírico con el término `B`; rejilla `n, ε, B` | El examen mínimo |
| M11 | Truncamiento de pérdidas | La mayor proporción pagadera de actualizaciones dañinas con `B, n, ε`; la cota de pérdidas del INT-canónico en función de la probabilidad mínima | La elección de `B` sin pagar el daño |
| M12 | Atribución en un modelo de fusión de juguete | Pérdidas lineal-cuadráticas, gradientes conocidos; reglas «por separado», «dejar uno», Shapley; duplicados y duplicados con ruido; fracciones exactas | Si hay una regla sin beneficio de los duplicados |
| M13 | Pistas y gadgets de la prueba breve | Número de valores con redondeo, división y tablas por token y capa; celdas, accesos a tablas y compromisos por una operación de redondeo y softmax | La barrera 2.3 y la estimación de T3 |
| M14 | Pequeñas búsquedas exhaustivas para comprobar fórmulas | Empaquetado de bits con `B = 8` y `B = 4` (repetición de hashes); cadena de 8 transiciones con elección 2: 224 pares, 56 atrapados, 168 omitidos; campo F₅ y error (1, −1): 5 omisiones de 25 | Comprobación de la implementación de los modelos probabilísticos |
| M15 | Certificado del ganador en matrices estructuradas sintéticas | Filas agrupadas, brecha de logits dada, empates, escala común | Ahorro con distintas distribuciones; con pesos reales — después de O1 |
| M16 | Certificado de intervalo en prefijos fijos | Proporción de salidas ambiguas `u`, número de recálculos completos, precio de la preparación por número de peticiones | Si la aceleración se ajusta al 5% (una vez disponibles los pesos) |
| M17 | Paso de Gauss–Newton en un bloque pequeño | Matriz racional explícita `J`, identidad `⟨Jx, z⟩ = ⟨x, Jᵀz⟩`, longitudes de los enteros, número de refinamientos, empates | El precio del nuevo contrato |
| M18 | Cálculo de pagos y recuperación | Búsqueda exhaustiva finita: un número de tarea, dos padres, bifurcación, pérdida de la entrada, colusión de todos los asignados, cuenta vacía | No más de un pago por resultado; nada se aplica antes de la aceptación |

---

## 6. Decisiones que exige esta etapa

El consejo no toma decisiones. Abajo están las preguntas con la recomendación del consejo. El propietario encargó decidirlas
al acompañante; las decisiones D18–D25 se adoptaron el 24 de noviembre de 2026 y están registradas en [ROADMAP](ROADMAP.md),
sección 3. Cada decisión se indica después de la pregunta.

1. **¿Cambiar la base de pago del entrenamiento por «pago por la mejora demostrada»?** Por D2
   se paga un resultado verificable; la mejora en un examen formalmente lo es, pero es un objeto distinto
   del paso ejecutado. Tres trabajos (claude1, claude2, ds1) lo consideran el candidato principal,
   tres (gpt1, gpt2, ds2) — otro contrato, no una verificación del paso. *Recomendación del consejo:* permitir
   investigar este camino como candidato a nueva unidad de pago del entrenamiento, sin llamarlo verificación del paso.
   Decidir definitivamente tras los cálculos M7, M8, M10–M12 y el experimento O6. Condiciones: faro externo tras
   la fijación, `ε` criptográficamente pequeño, pérdidas sin truncamiento, prueba del examen, regla de
   atribución sin beneficio de los duplicados. Por D6, dejar registrado que la mejora no demuestra la ausencia de daño.
   **Decidido — D18:** el camino se investiga como candidato a nueva unidad de pago del entrenamiento, pero no se adopta ni
   se llama verificación del paso. La decisión de adopción — tras M7, M8, M10–M12 y el experimento O6 (está fuera de D5
   y exige autorización del propietario). El modelo
   se publica solo según la regla D9. La búsqueda de la verificación del propio paso (T3) continúa.
2. **¿Es admisible un error criptográfico pequeño?** Los requisitos lo llaman supuesto. Los trabajos
   claude1, claude2, ds2 y los críticos Claude y DeepSeek consideran que un error `2⁻⁴⁰…2⁻¹²⁸` es compatible
   con D1 como expectativa, si la aleatoriedad es externa e impredecible y cada intento cuesta
   más que `ε·R`. Los trabajos gpt1, gpt2 y el crítico ChatGPT: un solo error pequeño no basta para D1, hace falta
   una cota inferior demostrada del precio del intento más barato. ds1 considera que hace falta exactamente cero.
   *Recomendación del consejo:* aceptar el error pequeño como supuesto nombrado abiertamente bajo tres condiciones —
   faro externo estrictamente tras la aceptación final del bloque, prohibición de Fiat–Shamir para el muestreo,
   cota inferior registrada del precio del intento. Sin esta decisión no son posibles ni el pago por la mejora
   ni las pruebas breves.
   **Decidido — D19:** se admite un error pequeño como supuesto explícito bajo estas tres condiciones,
   no mayor que `2⁻⁸⁰` por intento y con `ε·R` menor que la cota inferior registrada del precio del intento. La
   verificación por muestreo habitual con error `q^k` no queda autorizada por esto.
3. **¿Qué faro externo y cuya confianza es admisible?** Sin una fuente externa de aleatoriedad común, con
   `q = 1` no funciona ningún esquema con muestreo tras la fijación (cota 2.1, punto 7). Las fuentes aún
   no están elegidas (ataque 1.5 y N13). *Recomendación del consejo:* elegir varias fuentes independientes
   y registrar la confianza en ellas como supuesto.
   **Decidido — D20:** no menos de dos fuentes públicas independientes, el valor se toma en un momento fijado de antemano
   tras la fijación final, sin derecho a omitirlo. Las fuentes concretas
   y el precio de influir en ellas — en la etapa 2. Hasta que se elija el esquema, no se incluyen esquemas con muestreo.
4. **¿Aceptar que para la respuesta del modelo la única verificación independiente de la colusión es la del pagador
   que verifica por sí mismo?** *Recomendación del consejo:* sí. Para el consumidor sin equipo la respuesta
   se entrega con la marca «no verificado» (D6 lo permite), y la delegación de la verificación es un supuesto suyo.
   Decidir aparte cómo pagar al ejecutor por esa respuesta sin infringir D1: no hay solución.
   **Decidido — D21:** sí. La red no paga una respuesta sin verificación. El usuario sin equipo puede
   nombrar él mismo un verificador; es un supuesto suyo, y la red no le promete D1.
   La garantía de D1 para ese usuario sigue siendo una cuestión abierta.
5. **¿Permitir cambios del producto en aras de una verificación exacta barata?** Aquí entran la elección canónica
   del token mediante Gumbel-max (cambia la distribución respecto al muestreo habitual top-p/top-k),
   el perfil entero exacto (puede empeorar la calidad), las tareas con resultado verificable (fórmulas,
   pruebas) y los nuevos optimizadores con certificado exacto (Gauss–Newton, regresión ridge).
   *Recomendación del consejo:* permitirlos como tipos de tarea aparte del plan con un contrato explícito, tras
   los experimentos O5 y el cálculo M17.
   **Decidido — D22:** permitirlos como tipos de tarea aparte del plan con un contrato explícito, tras O5 y M17.
   El muestreo habitual sigue disponible con la marca «no verificado».
6. **¿Cómo limitar las disputas falsas del pagador sin depósitos?** D8 limita las disputas al número de
   peticiones, pero una coalición que se paga las peticiones a sí misma elude ese límite. *Recomendación
   del consejo:* calcular el precio de una disputa falsa (M9) antes de decidir; el consejo no encontró una regla que no
   exija depósito.
   **Decidido — D23:** primero el cálculo M9. PPS no se incluye hasta que se elija para él una regla
   que limite las disputas falsas sin depósito.
7. **¿Guardar el criptograma de la respuesta en el registro?** Sin esto, el ejecutor puede retener la respuesta.
   *Recomendación del consejo:* sí, alrededor de 2–4 KB por respuesta; esto concuerda con D10.
   **Decidido — D24:** sí, el criptograma se registra en el registro en una sola entrada junto con la aceptación.
8. **¿Hace falta la formulación bilateral de D1 también para la falsificación parcial?** El trabajo claude2 preguntaba
   si es admisible una falsificación que es peor que el trabajo honesto pero mejor que la inacción. La formulación formal
   de D1 en [THREAT_MODEL](THREAT_MODEL.md), sección 1.5, ya exige ambas desigualdades. *Recomendación
   del consejo:* no cambiarla; por eso VYa-S y PVYa en la variante relativa quedan rechazados.
   **Decidido — D25:** no cambiarla.

---

## 7. Quién hizo qué

El consejo de modelos trabajó con los materiales del proyecto, sin acceso a la red y sin experimentos.

- **Ronda 1, seis trabajos independientes:** dos trabajos de ChatGPT (gpt1, gpt2), dos de DeepSeek
  (ds1, ds2), dos de Claude (claude1, claude2). Cada uno analizó las direcciones de la etapa 4
  de la hoja de ruta, propuso sus propios mecanismos y calculó su precio. Los programas aritméticos cortos
  los ejecutaron claude1, claude2, gpt1 y gpt2; gpt1 y gpt2 adjuntaron pequeñas búsquedas exhaustivas
  con hashes de control.
- **Ronda 2, tres críticas:** una de ChatGPT, una de DeepSeek y una de Claude. Cada crítico leyó los seis
  trabajos, buscó contraejemplos y recalculó las cifras clave. Los críticos ChatGPT y DeepSeek repitieron las pequeñas
  búsquedas exhaustivas de gpt1 y gpt2 en el procesador; los hashes coincidieron.
- **Consolidación:** este documento lo compuso Claude a partir de los trabajos y las críticas. Donde los críticos discreparon, figura
  «discutible». Al consolidar se aplicaron a las conclusiones las decisiones D6–D17, que los participantes no tenían; no se añadieron
  estimaciones ni cifras nuevas más allá de los trabajos y las críticas.
