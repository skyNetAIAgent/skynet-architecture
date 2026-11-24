<!-- translation of docs/STAGE4_KERNELS.md, source sha256: e81d4e27191f3ce009ea9b71602c58405e742a7229fc972d8c69ae520e675812 -->

# Etapa 4. Contrato byte a byte de los cálculos integrados

[English](../../docs/STAGE4_KERNELS.en.md) · [中文](../zh/STAGE4_KERNELS.md) · **Español** · [Français](../fr/STAGE4_KERNELS.md) · [Deutsch](../de/STAGE4_KERNELS.md) · [Italiano](../it/STAGE4_KERNELS.md) · [Русский](../../docs/STAGE4_KERNELS.md) · [Português](../pt/STAGE4_KERNELS.md) · [العربية](../ar/STAGE4_KERNELS.md)

Estado a 24 de noviembre de 2026. El documento define las reglas exactas de cuatro nuevos cálculos integrados del miniagente (desde la versión 1.2.0 del agente) para los cálculos M8, M10, M12 y M14 de [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), sección 5.3. La especificación y la implementación en Go las escribió ChatGPT; DeepSeek verificó de forma independiente la especificación con los trabajos de origen del consejo y a partir de ella sola escribió una segunda implementación en Python ([tools/reference_stage4.py](../../tools/reference_stage4.py)); los 73 resultados de las tareas coincidieron byte a byte; Claude revisó el código y el cotejo. Las referencias del tipo «claude1, §5.4» remiten a los trabajos del consejo de modelos reunidos en VERIFICATION_SEARCH. Es un cómputo exacto por fórmulas, no una medición: la coincidencia confirma la aritmética, pero no los supuestos de los modelos. Los cálculos M5, M7 y M18 quedan aplazados: en los trabajos faltan reglas para determinarlos de forma inequívoca (sección «Cálculos aplazados»).

| Cálculo de §5.3 | Kernel de la versión 1 | Qué se puede saber de una unit |
|---|---|---|
| M8 | `t4-scale` | Cuántos tokens de entrenamiento por nodo se requieren con un número dado de presentadores y cuántos presentadores admite el presupuesto |
| M10 | `exam-thresholds` | En qué intervalo racional se encuentra cada uno de los dos umbrales del examen |
| M12 | `merge-attribution` | Cómo cambia la suma de los abonos del participante al añadir copias exactas o con ruido |
| M14 | `verification-enumerations` | Qué casos superaron o fallaron de forma exhaustiva la comprobación de empaquetado, cadena o igualdad de campo |

La elección se deriva de la tabla del consejo en §5.3. Por D18, el pago por la mejora sigue siendo una hipótesis de investigación. Para reproducir los cuatro cálculos bastan los parámetros de entrada. [Resultado del consejo](VERIFICATION_SEARCH.md) · [Decisiones D18–D20](ROADMAP.md)

## Reglas generales de la versión 1

En la tarea firmable, el nombre del kernel y el entero `kernel_version: 1` se almacenan por separado. La entrada `params` es un objeto con todos los campos enumerados para el kernel. Los campos sobrantes y ausentes, la repetición de una clave JSON, los valores fuera de rango y los tipos incorrectos provocan un error. Un entero se escribe como literal entero JSON, sin punto decimal ni exponente. Se prohíben las cadenas y los valores lógicos en lugar de números. Los límites son inclusivos. Los ejes de la rejilla conservan el orden de entrada. El número de units es exactamente igual al tamaño de rejilla indicado para el kernel, de 1 a 1 000 000. El número de unit empieza en cero. En el producto cartesiano, el último eje cambia más rápido que todos los demás.

Para el cotejo se toma el objeto de resultado completo. En Python, los bytes canónicos son iguales a `json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode('ascii')`, sin salto de línea final. El hash del resultado es el SHA-256 de esos bytes, 64 dígitos hexadecimales en minúscula. El orden de los elementos de los arrays es significativo. Una fracción en una cadena se escribe en el sistema decimal como `p/q` con denominador positivo tras la reducción, incluidos `0/1` y los enteros con `/1`. No hay signos más ni ceros iniciales. Para M14 se define aparte el hash de los bytes *dentro* del resultado del empaquetado. [Codificador canónico del agente](../../agent-go/canon/canon.go)

## M8. Escala de T4 con una actualización de cada participante

`t4-scale@1` calcula el número entero mínimo de tokens de entrenamiento propio por ronda con el que el examen añade no más del 20% del cómputo. Para un presupuesto de tokens dado, el kernel también halla el número límite de presentadores. En el modelo, cada nodo verifica las `K=N` actualizaciones. La base cuesta una pasada directa por posición, cada actualización de las capas superiores una fracción `a=L_a/L` de una pasada, y el entrenamiento de un token cuesta tres pasadas. Estas relaciones vienen dadas por la propuesta. claude1, §5.4 «Precio» y §7.5, punto 4 · critic_claude, §1.8 y §10.4, punto 3 · [VERIFICATION_SEARCH, §5.3, M8](VERIFICATION_SEARCH.md)

| Campo `params` | Valores admisibles |
|---|---|
| `N` | Eje de enteros de 1 a 1 000 000. Número de presentadores en la ronda |
| `n` | Eje de enteros de 1 a 1 000 000. Número de posiciones del examen |
| `a` | Eje de pares de enteros `[p,q]`, donde `1 ≤ p ≤ q ≤ 1 000 000`. Fracción de una pasada por actualización |
| `D_budget` | Eje de enteros de 1 a 1 000 000 000 000. Presupuesto de tokens de entrenamiento por nodo y ronda |
| `epsilon_bits` | Un entero de 1 a 256. Define `ε=1/2^epsilon_bits` para un examen fijo. Con `n` dado, el coste es el mismo para todos los `ε` |

Los cinco campos son obligatorios. Cada eje es un array de longitud 1…32, los valores son únicos teniendo en cuenta la reducción de fracciones, y se conserva el orden del array de entrada. El número de units es igual al producto de las longitudes de los ejes y no supera 1 000 000. La numeración empieza en cero sobre el producto cartesiano `N, n, a, D_budget` en el orden de bucles anidados; el presupuesto es el que cambia más rápido. Una unit produce un objeto.

Para el punto elegido, sea `D=D_budget` y reduzcamos `a=p/q`. Midamos el cómputo en unidades de `1/q` de una pasada directa por posición. Entonces el examen requiere `E=n(q+Np)`, el entrenamiento requiere `W=3Dq`, y la fracción de costes indirectos es `E/W`. La división por el volumen de entrenamiento propio se deriva de la formulación de «recargo» en §5.4. La condición del 20% equivale a `5E ≤ W`.

| Campo del resultado | Valor |
|---|---|
| `kernel` | Cadena `t4-scale@1` |
| `N`, `n`, `D_budget` | Enteros del punto de entrada |
| `a`, `epsilon` | Cadenas reducidas `p/q`; `epsilon` se escribe como `1/q`, donde `q = 2^epsilon_bits` es un entero decimal (por ejemplo, `"1/4"` con `epsilon_bits = 2`) |
| `D_min` | Entero `(5E + 3q − 1) // (3q)`, donde `//` es la división entera hacia abajo. Es el redondeo del umbral hacia arriba hasta un token entero |
| `fits` | Valor lógico `D_budget ≥ D_min`. La igualdad cuenta |
| `N_max` | `null` si `W < 5nq` e incluso la pasada base supera el presupuesto. En caso contrario, el entero `(W − 5nq) // (5np)`. Cero significa que solo cabe la base. El límite puede quedar fuera del eje de entrada `N` |
| `overhead` | `E/W` como cadena reducida `numerator/denominator` |

La cota inversa se deriva de la desigualdad lineal `5npN ≤ W − 5nq` con `p` positivo. Con los parámetros permitidos, `5E+3q−1 ≤ 5 000 005 000 002 999 999`, `W ≤ 3·10^18`. Los denominadores son positivos. Bastan enteros con signo de 64 bits y la reducción de fracciones mediante el MCD. En Go, para `overhead` se usa `big.Rat` y, para `2^epsilon_bits`, `big.Int`. Cada unit supone el análisis de no más de 128 elementos de ejes y un número constante de operaciones aritméticas.

Para `n=3, N=4, a=1/2`, el examen cuesta 9 pasadas; con 15 tokens de entrenamiento ocupa exactamente una quinta parte. Con 14 tokens, el límite baja a tres presentadores. Con `epsilon_bits=2` se obtienen los siguientes bytes canónicos.

```json
{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}
```

Como referencia de §5.4, con `n=100000, N=10000, a=4/36` el mínimo exacto es igual a 185 351 852 tokens. El precio físico depende de la reutilización de prefijos, el volumen de la caché, la cabeza de salida, la normalización, el tráfico y el precio real del entrenamiento de las capas superiores. La fórmula abarca solo el cómputo de pasadas descrito en §5.4. Para estimar el umbral estadístico al cambiar `ε` sirve M10. La tarea propuesta fija `ε=2^-80` conforme a la referencia numérica D19. critic_gpt, sección sobre claude1, «Precio oculto de T4» · [ROADMAP, D18–D19](ROADMAP.md)

## M10. Umbral del examen T4 — `exam-thresholds@1`

M10 determina cuán grande debe ser la mejora media observada en el examen para que supere el umbral estadístico. Para un único candidato fijado de antemano se toman `n` posiciones independientes con reemplazo. La diferencia de pérdidas en cada posición se recorta a `[−B/2, B/2]`. La `V` de entrada es la varianza muestral de las diferencias recortadas con divisor `n−1` (el cuadrado de la desviación estándar). Las cotas en nats por posición se toman del paso 6 de la descripción de T4. claude1, §5.4 · crítico Claude, §1.8

| Método | Umbral exacto `t` |
|---|---|
| Hoeffding | `B·√(ln(1/ε)/(2n))` |
| Bernstein empírico | `√(2V·ln(2/ε)/n) + 7B·ln(2/ε)/(3(n−1))` |

**Parámetros y units.** Son obligatorios cinco campos. Los campos `n`, `epsilon_bits`, `B`, `variance` son ejes de longitud 1 a 32, cada uno en el orden del array de entrada. Los valores de un eje son distintos; las fracciones se comparan tras la reducción.

| Campo | Valores admisibles |
|---|---|
| `n` | Número de posiciones, entero de 2 a 1 000 000 |
| `epsilon_bits` | Entero `k` de 1 a 128, `ε = 2⁻ᵏ` por comparación |
| `B` | Anchura del intervalo de recorte, entero de 1 a 64 |
| `variance` | Fracción `[p,q]`, enteros `0 ≤ p ≤ 10⁶` y `1 ≤ q ≤ 10⁶`. En todos los puntos de la rejilla, `V=p/q ≤ B²·floor(n/2)·ceil(n/2)/(n(n−1))` |
| `digits` | Un entero `d` de 1 a 9. La anchura absoluta garantizada de cada intervalo es menor que `10⁻ᵈ` |

El máximo de la varianza se alcanza en los extremos del rango, ya que la varianza es convexa respecto a cada observación. Con `j` valores en un extremo, su numerador es proporcional a `j(n−j)`, lo que da la cota indicada. El número de units es igual al producto de las longitudes de los cuatro ejes y no supera 1 000 000. La numeración coincide con `itertools.product(n, epsilon_bits, B, variance)`, empezando en cero.

**Algoritmo de reproducción byte a byte.** Para ambos métodos, escribir `t = √(A·ln 2) + C·ln 2`. En Hoeffding, `A=B²k/(2n), C=0`. En Bernstein, `A=2V(k+1)/n, C=7B(k+1)/(3(n−1))`. Todas las divisiones aquí son racionales.

1. Tomar `S=10^(d+1)`, `l=693147180559945309/10¹⁸`, `h=693147180559945310/10¹⁸`.
2. La cota inferior es igual a `(floor(√(S²Al)) + floor(SCl))/S`. La cota superior es igual a `(ceil(√(S²Ah)) + ceil(SCh))/S`. Ambos sumandos se redondean **por separado**.
3. Para una fracción no negativa `x=p/q`, calcular `r=isqrt(p//q)`. Esto es `floor(√x)`. Para la cota superior, sumar uno a `r` exactamente cuando `r²q < p`. Los `floor` y `ceil` habituales también se ejecutan con división entera. Todas las fracciones obtenidas se reducen.

**Certificado de precisión.** De la serie para `2·atanh(1/3)=ln 2` tomamos `T=2·Σ 1/(j·3ʲ)` sobre los `j=1,3,…,39` impares. El resto es positivo y está acotado por el primer término omitido multiplicado por `1/(1−1/9)`. Mediante comparación entera obtenemos `l < T < ln 2 ≤ T + 9/(4·41·3⁴¹) < h`. La monotonía de ambos sumandos y el redondeo dirigido garantizan que el umbral verdadero quede incluido. En el rango dado, `A ≤ 264192` y `C ≤ 19264`. Como `√h+√l > 1`, sustituir `l` por `h` cambia el umbral sin redondear en menos de `(515+19264)·10⁻¹⁸`. El redondeo amplía el intervalo en menos de `4/S`. La suma es menor que `10⁻ᵈ` incluso con `d=9`. Por unit bastan cuatro raíces cuadradas enteras y un número constante de operaciones sobre enteros y fracciones de un tamaño de varios cientos de bits, independientemente de `n`.

**Respuesta.** Los campos `n`, `epsilon_bits`, `B` y `digits` son coordenadas enteras y precisión. `variance` es una cadena con la fracción reducida. `hoeffding` y `bernstein` son arrays de dos de esas cadenas, primero la cota inferior. Para `n=2, k=1, B=2, V=0, d=1`, el kernel produce los siguientes bytes canónicos.

```json
{"B":2,"bernstein":["323/50","647/100"],"digits":1,"epsilon_bits":1,"hoeffding":["83/100","21/25"],"kernel":"exam-thresholds@1","n":2,"variance":"0/1"}
```

Para un umbral límite dado `τ`, el tamaño mínimo del examen **en la rejilla** queda establecido cuando en el punto elegido la cota superior es `≤ τ` y en todos los `n` menores, con los mismos parámetros, la cota inferior es `> τ`. Si el intervalo cruza el objetivo, puede hacer falta mayor precisión. Los números caracterizan la comparación unilateral de la media truncada con la fijación antes del faro externo. La corrección por la selección entre varios candidatos, la calidad fuera del examen, la elección de `τ` y la magnitud del efecto real requieren datos o reglas aparte. El pago por la mejora sigue siendo una variante de investigación según D18. [ROADMAP, D18–D20](ROADMAP.md) · crítico GPT, estimación de T4

## M12. Cómo cambia el abono al propietario de los duplicados al fusionar por suma

En el trabajo para M12 se indican pérdidas lineal-cuadráticas con gradiente y hessiano conocidos, tres reglas de atribución, duplicados exactos y duplicados con ruido. Elegimos la variante `merge = sum` analizada explícitamente en §5.4. El crítico aporta un caso en el que incluso añadir repetidamente el mismo paso mejora la función de pérdidas. El kernel `merge-attribution@1` comprueba esto con coeficientes de entrada explícitos. claude1, §5.4, pasos 6–7 y punto 2 «Atribución y duplicados», §7.5, punto 7 · critic_gpt, tabla sobre claude1, fila T4

| Campo `params` | Significado y límites inclusivos |
|---|---|
| `scale` | Denominador común `s`, entero 1…10 000 |
| `g` | Vector de numeradores del gradiente en el punto base. Su longitud define la dimensión `d`, 1…8 |
| `hessian` | Matriz simétrica de numeradores del hessiano, array de `d` filas de `d` componentes |
| `updates` | Array de `b=1…8` vectores de numeradores originales de longitud `d`, en el orden de presentación. Se permiten vectores iguales |
| `owner` | Índice entero de la propuesta original del participante comprobado, de 0 a `b−1`. Las demás propuestas originales pertenecen a otros participantes |
| `copies` | Eje de 1…8 enteros distintos 1…8. La `c` elegida define el número de propuestas añadidas del mismo participante |
| `noise` | Eje de 1…32 vectores de numeradores de longitud `d` distintos por pares. El vector nulo da un duplicado exacto |
| `threshold` | Numerador entero 0…10 000 para la deducción `t=threshold/s` de la valoración de cada propuesta |

Cada componente de `g`, `hessian`, `updates` y `noise` es un entero de −10 000 a 10 000. Para obtener el valor matemático de cada componente, dividirla por `s` **una sola vez**, también para la matriz. La versión admite coeficientes racionales con denominador común en el rango indicado. La simetría es obligatoria; el signo de la curvatura es arbitrario. Los ejes de entrada `copies, noise` forman la rejilla. Para la unit `u`, tomar los índices `divmod(u,len(noise))` respectivamente. Tras las `b` propuestas originales, añadir `c` vectores, cada uno igual a `updates[owner] + noise[j]` en numeradores. Los vectores originales se conservan. Los conjuntos de propuestas antes y después de la adición se consideran por separado.

**Cálculo.** Sea `U` el conjunto de índices de propuestas de un mismo lote, y `x(S)` la suma de sus vectores de actualización **matemáticos** sobre el subconjunto `S`. La ganancia en pérdidas se define como la reducción respecto a una base común,

```text
v(S) = −gᵀx(S) − x(S)ᵀ H x(S)/2,     v(∅) = 0.
```

Para cada índice `i`, calcular tres valoraciones **con signo**. `separate[i]=v({i})`. Regla de exclusión de uno, `loo[i]=v(U)−v(U без i)`. La valoración `shapley[i]` es igual al incremento medio `v(S∪{i})−v(S)` sobre todas las permutaciones de índices, donde `S` consta de los predecesores de `i`. Esta regla se aplica a la función completa de reducción de pérdidas. Para calcular sin un recorrido factorial, sea `q_i=v({i})`, `h_ij=−x_iᵀ H x_j`. La simetría da `v(S)=Σ q_i + Σ_{i<j} h_ij` sobre los participantes `S`. Al excluir a un participante desaparecen todos sus términos por pares. En una permutación uniforme, cada uno de los demás participantes le precede exactamente en la mitad de los casos. Por tanto

```text
loo[i]     = q_i + Σ_{j≠i} h_ij
shapley[i] = q_i + (Σ_{j≠i} h_ij)/2
v(U)       = Σ shapley[i].
```

Después, por separado para cada regla, la valoración `z` se convierte en un abono `max(0,z−t)` en unidades de mejora (el coeficiente de pago κ se toma como uno). Primero se abona por cada propuesta y luego se suman los abonos del propietario. `gain` es el abono al propietario por su propuesta original y todas las añadidas tras la adición menos el abono por su única propuesta antes de la adición. Un signo positivo significa una ganancia de las presentaciones adicionales en este ejemplo.

**Formato de la respuesta.** Claves `kernel` (cadena `merge-attribution@1`), `owner`, `scale`, `copies` (el entero elegido del eje), `noise` (el vector elegido de enteros numeradores), `baseline`, `with_copies` y `gain`. Cada uno de los objetos `baseline` y `with_copies` contiene `value` — la fracción `v(U)` — y los campos `separate`, `loo`, `shapley` — arrays de fracciones en el orden de los índices de propuestas. El objeto `gain` contiene una fracción bajo cada uno de los tres nombres de regla. Todas las fracciones de salida son cadenas canónicas.

**Aritmética y límites.** El denominador común de las valoraciones intermedias es `2s³`. Si `G, A, z_i` son los numeradores enteros de entrada del gradiente, el hessiano y el paso, el numerador `q_i` es igual a `−2s Gᵀz_i−z_iᵀAz_i`. A la mitad del término por pares le corresponde el numerador entero `−z_iᵀAz_j`. El numerador de la deducción es `2s²·threshold`. Tras añadir hasta 16 propuestas, también se cumple `|z_ij| ≤ 20 000`. De aquí, `|z_iᵀAz_j| ≤ 8²·20 000²·10 000 = 2,56·10¹⁴`, y la parte lineal en módulo no supera `3,2·10¹³`. Incluso la suma de 16 valoraciones LOO completas y deducciones es menor que `1,3·10¹⁷` en módulo. Todas las multiplicaciones y sumas parciales caben en 64 bits con signo. La implementación reduce las fracciones mediante `big.Rat`. Tiempo `O(k d²+k²d)` con `k ≤ 16`, sin tabla de subconjuntos. La memoria está limitada por los vectores de entrada, la matriz, tres valoraciones por propuesta y el resultado.

**Comprobación manual.** Con `v(x)=3x−x²/2`, una sola propuesta `x=1` y umbral nulo, la valoración original es igual a `5/2` según todas las reglas. Tras el duplicado exacto, `v(2)=4`. Las reglas dan por cada propuesta `5/2` por separado, `3/2` con la exclusión y `2/1` según Shapley. La ganancia total del propietario es, respectivamente, `5/2`, `1/2`, `3/2`. Solo este ejemplo basta para refutar la ausencia de ganancia para cada una de las tres reglas en toda la familia de tales modelos con umbral nulo.

**Ámbito de la conclusión.** El conjunto de participantes de comparación está fijado. El ruido viene dado por un vector explícito y el umbral por la entrada. La aceptación, la reselección de la composición tras la deducción del umbral, los costes de presentación, el entrenamiento de parámetros, los efectos externos y el examen empírico quedan fuera de este modelo. La ganancia numérica se refiere a la suma de abonos según la regla elegida. La comprobación completa de D1 exige comparar la utilidad de la coalición también con el trabajo honesto y con la inacción. [THREAT_MODEL, §§1.4–1.5](THREAT_MODEL.md) · [ROADMAP, D18 y D25](ROADMAP.md)

## M14. Comprobación de fórmulas por enumeración finita

El kernel `verification-enumerations@1` repite tres pequeños experimentos. Permite comprobar si el empaquetado conserva la distinción entre los vectores permitidos y cuántos errores dejan pasar dos tipos de comprobación por muestreo. Los datos de origen, el orden de la enumeración y los hashes de referencia se publican en GPT2, §6.2 y «Código de control para la primera repetición». La cadena se define en la tabla «Qué entregar a los miniagentes»; la condición de omisión en el campo, en §6.1. Trabajo de GPT2 · [Resumen, §5.3](VERIFICATION_SEARCH.md)

El único parámetro `cases` es un array de 1–4 cadenas distintas de la tabla siguiente. `units = len(cases)`. Numeración desde cero; la unit `u` calcula todo el experimento `cases[u]`. La clave `case` del resultado contiene esa misma cadena, y `kernel` es igual a `"verification-enumerations@1"`. El formato de los demás campos depende del experimento.

| `case` | Campos del resultado además de `case` y `kernel` | Valores de control |
|---|---|---|
| `packing-8` | Enteros `total`, `true_accepts`, `false_accepts`, cadena `verdict_sha256` | 441, 9, 0, `a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c` |
| `packing-4` | Los mismos campos | 441, 9, 20, `fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9` |
| `chain-8-2` | Enteros `total`, `caught`, `missed` | 224, 56, 168 |
| `field-5` | Enteros `total`, `caught`, `missed` | 25, 20, 5 |

**Empaquetado de bits.** Tomar la base `B` de la etiqueta del experimento. Recorrer `(x,y,c,d)` lexicográficamente en orden creciente, con `x,y ∈ {−1,0,1}` y `c,d ∈ {−3,…,3}`. El bucle interior cambia `d`. El resultado verdadero es `(s,t)=(2x−y,−x−y)`. El criterio de aceptación es la divisibilidad de `(c−s)+B(d−t)` por `B²` sobre enteros. Si `(c,d)=(s,t)`, la aceptación incrementa `true_accepts`; en los demás casos de aceptación, incrementa `false_accepts`. Escribir en el orden del recorrido exactamente 441 bytes, cada uno con valor 1 en caso de aceptación y 0 en caso de rechazo. `verdict_sha256` es el SHA-256 de esos bytes crudos en forma de 64 dígitos hexadecimales en minúscula. El hash habitual del resultado de la unit se calcula aparte de todo el JSON canónico. Para la comprobación manual con `B=4`, `x=−1`, `y=1`, la respuesta verdadera `(−3,0)` y la propuesta `(1,−1)` dan una diferencia 0.

**Cadena.** Para cada defecto único `h=0,…,7`, recorrer todos los pares no ordenados sin reemplazo como `0 ≤ i < j < 8`. Incrementar `total` en 1 por cada tripleta, y `caught` si `h=i` o `h=j`. El número de omisiones es `missed=total−caught`. Para cada `h` hay 28 pares, de los cuales exactamente 7 contienen `h`.

**Campo.** Recorrer los vectores `(x,y)∈{0,…,4}²`, incluido el nulo. El error `(1,−1)` se omite exactamente cuando `(x−y) mod 5 = 0`. `total` cuenta todos los vectores, `missed` cuenta las omisiones y `caught=total−missed`. Los cinco pares diagonales dan cinco omisiones.

La unit más larga comprueba 441 combinaciones y almacena 441 bytes de veredictos para un solo SHA-256. Los contadores no superan 441, el módulo de la expresión de empaquetado no supera 46 y el mayor módulo de división es 64. Bastan enteros con signo de 32 bits. Los resultados se refieren a los rangos indicados, a un único error fijo y a la enumeración completa de variantes equiprobables. La generalización a un protocolo real exigiría justificar la distribución de las llamadas y la independencia de las comprobaciones.

## Cálculos aplazados


| Cálculo | Qué está ya definido | Qué datos permitirán obtener un resultado inequívoco |
|---|---|---|
| M5. Oleadas de falsificaciones | Para una sola falsificación barata con costes nulos, `π=m_s/(L+1)` y `H*=R(1/π−1)`. Por ejemplo, con `L=36, m_s=2`, el umbral es igual a 17,5R | Para la oleada hay que fijar la distribución conjunta de las comprobaciones y la transición del saldo con varios descubrimientos simultáneos, incluido el momento del cargo y la disponibilidad de las recompensas de la oleada anterior. Con `π=1/2`, la muestra común para dos errores iguales omite ambos con probabilidad 1/2; las muestras independientes, con probabilidad 1/4. La analogía propuesta con `exit-scam-a` requiere además precisar si se conserva su probabilidad separada de asignación de la comprobación. (claude1, §1.3, §4.2 y §7.5, punto 3) (THREAT_MODEL, §1.8) |
| M7. Economía de la revelación | Para un pago fijo R y el pago de la prueba solo en la rama exitosa, se conoce el ingreso de un intento `p(R−Pe)−c_view−c_commit` | Para el límite general ε hacen falta el precio del intento descartado, la regla de pago con varios éxitos y la ley conjunta de los resultados de los candidatos en un examen común. El número de claves por sí solo no determina estas magnitudes. ODU con prueba obligatoria de cada intento da otro presupuesto, y en T4 el pago depende además de la magnitud de la mejora. (claude2, §5.3) (critic_claude, §2.4) (critic_gpt, análisis de ODU) |
| M18. Pagos y recuperación | Están definidos la atomicidad de la aceptación, el carácter único de la amortización del derecho en la historia canónica y la lista de escenarios | Para contar las rutas hace falta una tabla de transiciones al cambiar de rama, un criterio de finalidad, las reglas de recuperación cuando los datos desaparecen y vuelven, y un límite finito del número de presentaciones repetidas. Autómatas distintos pueden satisfacer los mismos invariantes y dar números de pagos distintos según historias intermedias. (gpt1, §1 y §7) (critic_gpt, «Completitud, recuperación y precio») |
