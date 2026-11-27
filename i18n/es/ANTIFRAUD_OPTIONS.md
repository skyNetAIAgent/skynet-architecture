<!-- translation of docs/ANTIFRAUD_OPTIONS.md, source sha256: 63c43d6864c5cccb6fa61953c9ba9594e26e3dba1a4c8241129e6f346bc08f20 -->

# Variantes de lucha contra el fraude: resultado de las auditorías y del consejo de modelos

[English](../../docs/ANTIFRAUD_OPTIONS.en.md) · [中文](../zh/ANTIFRAUD_OPTIONS.md) · **Español** · [Français](../fr/ANTIFRAUD_OPTIONS.md) · [Deutsch](../de/ANTIFRAUD_OPTIONS.md) · [Italiano](../it/ANTIFRAUD_OPTIONS.md) · [Русский](../../docs/ANTIFRAUD_OPTIONS.md) · [Português](../pt/ANTIFRAUD_OPTIONS.md) · [العربية](../ar/ANTIFRAUD_OPTIONS.md)

Estado a 27 de noviembre de 2026.

**Qué se ha hecho.** El propietario del proyecto reunió seis auditorías independientes de completitud y dos mapas
de mecanismos de protección contra el fraude y propuso tres ideas propias: incorporar la verificabilidad en el propio
modelo, tomar técnicas de los juegos y «cruzar» las vías indirectas de verificación con trabajo útil. El consejo
de modelos escribió once trabajos independientes y cuatro críticas cruzadas y reunió todo ello
en las variantes descritas abajo.

**Estado.** Este documento es un razonamiento y un cálculo. Las magnitudes medidas se toman solo del experimento D5
([EXPERIMENT_D5](EXPERIMENT_D5.md)) y están marcadas [medido]. Todo lo demás está marcado [cálculo] o
se denomina supuesto. Las únicas decisiones adoptadas siguen siendo D1–D25 ([ROADMAP](ROADMAP.md),
sección 3); todo lo que aquí se propone cambiar son propuestas del consejo, no decisiones. El consejo no realizó
nuevos experimentos, prototipos ni instalaciones. La literatura se cita de memoria de los modelos o
según los datos de las auditorías y no se cotejó con las fuentes primarias. Compendios anteriores:
[STRATEGY_SEARCH](STRATEGY_SEARCH.md) y [HIDDEN_DETECTOR](HIDDEN_DETECTOR.md).

**Notación.** `R` — precio de la tarea; `c` — coste del trabajo honesto en el perfil exacto
(entero); `c_f` — gastos del defraudador en la falsificación; `H_lock` — suma bloqueada
no madurada de la clave; `p` — probabilidad de verificación de la respuesta; `q` — proporción del peso de la coalición entre
los verificadores asignados; `ρ` — tiempo de verificación de una respuesta lista en una pasada, en fracciones del tiempo
de su generación exacta: 0,10–0,40 con lote 1 y 0,26–0,64 con lote 8 [medido]; `γ` — ralentización
del perfil exacto frente al Q8_0 normal: 1,52–1,78 con lote 1 y 2,47–2,79 con lote 8
[medido, solo RTX 2060].

## Resumen breve

1. **Caro no es verificar, sino calcular con exactitud.** La verificación de una respuesta cuesta el 10–40% de su
   generación [medido], pero el recargo principal es la ralentización del perfil exacto en 1,52–1,78 veces
   [medido]. La referencia «alrededor del 5%» es inalcanzable con los núcleos actuales en ninguna variante, por
   rara que sea la verificación [cálculo].
2. **La idea de «huellas y recálculo de un fragmento aleatorio» funciona, pero no como abaratamiento de la garantía.**
   Si se abren `s` fragmentos de `N`, una celda sustituida de forma dirigida pasa
   con probabilidad no menor que `1 − s/N`. La estimación «30 veces más barato y el fraude se sigue detectando»
   significa en realidad «30 veces menos detección». Las huellas son útiles en otro papel: una raíz corta
   del rastro permite resolver una disputa dividiendo por la mitad hasta un solo paso y da a un dispositivo débil
   una verificación parcial con una marca honesta.
3. **La idea de la «verificabilidad dentro del modelo» funciona en una sola forma:** reentrenar o reescribir
   los núcleos para que el perfil exacto se vuelva rápido. Esto reduce `γ` y no debilita la garantía.
   Las huellas las escribe un programa, no el modelo, y no hace falta reentrenar para ellas. Las sumas de control
   en las capas protegen al ejecutor honesto de fallos de hardware, pero no de la intención.
4. **De los juegos solo se traslada el orden de los movimientos:** «selló → fijación definitiva → elección
   secreta → apertura → recálculo». Con el cálculo están acoplados solo dos movimientos: el recálculo del fragmento abierto
   y la verificación del testigo de la tarea. Un juego aparte junto al trabajo útil no demuestra nada.
5. **Hay cuatro variantes y una capa adicional:** verificación completa de cada respuesta por el pagador;
   lotería por pedidos enteros; moneda secreta del pagador con suma bloqueada; tareas
   con resultado verificable; y decodificación especulativa exacta como posible forma de abaratar
   la primera y la tercera variantes.
6. **Recomendación.** El contrato principal es la verificación completa de cada respuesta por el pagador en el perfil
   exacto. Es el único que cumple las decisiones adoptadas sin modificarlas. Las tareas con resultado verificable —
   un tipo aparte de tareas y por ahora la única garantía estricta para el entrenamiento. La lotería — una tarifa
   para lotes. La moneda con suma bloqueada sigue siendo candidata hasta el cálculo M9 y las decisiones del propietario.
7. **Primer paso.** Un cálculo: M9 — disputas falsas sin depósito, todas las ramas de silencio y rechazo.
   Un experimento (con permiso del propietario): medir en el perfil v2 ya montado y en llama.cpp Q8_0
   la coincidencia de tokens con un prefijo común. Resuelve de golpe tres cuestiones (sección 5).
8. **Literalmente irrealizable:** proteger al consumidor sin equipo con colusión total de
   los verificadores; verificar el paso de entrenamiento con colusión total dentro de un recargo del 20%; encajar
   una respuesta verificada en el 5% con la `γ` medida. Las relajaciones mínimas se formulan
   como preguntas al propietario en la sección 7.

## 1. Qué encontraron las auditorías

Etiquetas de las auditorías: RU — `SkyNet_audit_completeness_RU`; SC — `skynet_completeness_audit`; GPT —
`gpt-SkyNet-audit`; DS — `deepseek-AUDIT_REPORT`; GEM — `gemini_report`; CR — `chat_responses`;
mapas — `mehanizmy-anti-obman` (MEH) y `mechanisms_map_report` (MAP). Donde los trabajos del consejo
leyeron de forma distinta quién llamó qué, se indica con la palabra «discutible».

### 1.1. Enfoques omitidos

| Enfoque | Quién de las auditorías lo nombró | Valoración del consejo |
|---|---|---|
| Huellas de activaciones, TOPLOC | SC, GPT, GEM, CR, DS (en una línea), MAP; MEH — discutible | No es base de pago; solo señal para una verificación exacta adicional (sección 2.4) |
| Esquemas optimistas, disputa con árbitro, división por la mitad | Las seis y ambos mapas | Capa de disputa necesaria; con colusión total no hay quién dispute, así que no sustituye la verificación del pagador |
| Pruebas estadísticas de sustitución del modelo | GPT, DS, GEM, CR, MAP; SC y RU — discutible | Solo señal para elevar la frecuencia de verificación; no entra en el núcleo |
| Aritmética de coma flotante reproducible, núcleos enteros tipo Ozaki | SC, GEM, DS, GPT, RU; CR los llama RepOps | La coma flotante no sustituye al perfil entero; la aceleración de núcleos es una hipótesis para el experimento |
| Sumas de control ABFT | SC, GEM, DS, GPT, RU | Autocontrol del nodo honesto frente a fallos; cubre solo multiplicaciones lineales |
| Verificación de Freivalds | SC, CR, GPT, GEM, mapas | Funciona para la parte lineal de la aritmética exacta con un vector secreto fresco tras la fijación |
| Disponibilidad de datos | SC, DS, GPT; GEM — en contra; RU y los mapas — discutible | Ingeniería de la disputa y del entrenamiento, no garantía de R4 |
| Diseño de mecanismos con verificación cara | GEM, DS, GPT, SC | Confirma el umbral `R/(R + H_lock)`; no aporta una palanca nueva |
| Atestación de hardware de GPU, TEE | Casi todas | Señal adicional y modo de privacidad; no se puede reducir por ella la frecuencia de verificación |
| Aval y seguro sin depósito del participante | SC, GEM, DS, GPT, RU | El candado ajeno es en esencia un depósito de un tercero, cuestión para R5; el fondo de seguro abre la autodisputa |
| Experiencia de Bittensor, Gensyn, Prime Intellect, Hyperbolic, Ritual, Atoma, Golem | Las seis y los mapas | Todas se sostienen en depósito, validadores de confianza, TEE o «uno honesto»; se trasladan técnicas sueltas |

Nombrados por una sola auditoría: las pruebas selectivas por capas como base (RU), la vinculación
del criptograma de la respuesta al compromiso mediante DLEQ (SC), el pool de cupones (SC; según uno de los trabajos,
también GEM y GPT).

### 1.2. Puntos débiles de las conclusiones anteriores

- El umbral `p ≥ R/(R + H_lock)` es correcto bajo tres condiciones que antes no se nombraban: el precio
  no es inferior al coste, la moneda realmente se lanza, la suma está disponible para quemarse
  (GPT, SC, GEM, RU).
- La conclusión «la referencia del 5% queda refutada» se refiere a una sola implementación de los núcleos (GEM, SC, DS).
- La barrera de las pruebas breves está calculada para una sola disposición (SC, GEM, DS, GPT).
- La coincidencia de bits se muestra en seis configuraciones, no «en cualquier hardware» (DS, GEM, SC, GPT).
  Las críticas precisaron: para una pasada larga sobre una respuesta lista, en tres.
- La afirmación «un pagador perezoso y un novato juntos dan cero» era un error: la ganancia llega hasta `+R`.
- El barrido de «92 millones de estrategias» no demuestra la completitud (RU).
- La literatura de los consejos anteriores se cita de memoria (RU, GEM, DS, GPT).

### 1.3. Contradicciones de requisitos y decisiones

- **D16 contra la verificación por muestreo.** Si un fallo honesto no se castiga, el defraudador declara
  la falsificación un fallo y recibe `(1 − p)·R − c_f` (DS, GEM, RU, SC).
- **D19.** La tercera condición — «el error multiplicado por `R` es menor que el precio del intento» — no es aplicable
  cuando el intento es gratuito (DS, RU; en el consejo, ChatGPT).
- **La emisión de créditos por entrenamiento con demanda nula**, la colusión total, el recargo del 20% y la verificación
  por cada nodo no se cumplen a la vez (DS, SC, GEM, GPT, CR, MEH).
- **El consumidor sin equipo y R4** (SC, GEM, RU, CR).
- **El D1 literal excluye cualquier muestreo** (RU, DS).
- **La disputa sin depósito y el fondo finito de disputas** (SC, GEM, GPT, RU).
- **«Primero la confianza plena, luego los experimentos»** se califica de círculo vicioso: `γ`, `ρ`, la calidad
  y la frecuencia de fallos solo se establecen midiendo (DS, GPT). Esta es la opinión de las auditorías y de un
  crítico; el consejo no ha infringido ni deroga la restricción vigente sobre experimentos.

### 1.4. Nuevos ataques

- **Pagador perezoso.** Si una proporción `λ` de pagadores no verifica, el umbral pasa a ser
  `R/((1 − λ)(R + H_lock))`; con la cuenta vacía es mayor que uno, y el defraudador que ha reconocido
  al pagador perezoso recibe hasta `+R` (SC) [cálculo].
- **La moneda no se fuerza:** el programa del pagador se puede recompilar con `p = 0` (GEM, SC).
- **Reventa de la respuesta entre sesiones** («ataque de la mafia»): el intermediario toma el pedido, compra la respuesta
  a un ejecutor honesto y no paga. Funciona sin colusión de los verificadores; se cura con el orden
  «prepago bloqueado → respuesta → verificación en plazo → pago» (GEM; desarrollado en el consejo).
- **Venta de la suma no madurada** antes de marcharse (RU). Se cura con la prohibición de transferirla.
- **El autopago** aumenta la suma bloqueada y baja la frecuencia de verificación. La crítica mostró
  que esto no abre el dinero (el dinero propio del defraudador se quema al ser detectado),
  pero abarata el daño dirigido.
- **Inundación con claves gratuitas:** cada clave nueva exige verificación completa
  y carga al pagador; es una denegación de servicio, no un robo.
- **Sustitución de uno o dos tokens dentro de la ventana de huella de TOPLOC** (SC).

### 1.5. Qué es dudoso en las referencias y cifras de las auditorías

- **Aceleración de los núcleos según Ozaki hasta `γ` = 1,05–1,20.** Dudoso: los núcleos rápidos de D5 ya usan
  las mismas instrucciones de 8 bits, y con ellos se ha medido 1,52–1,78; 24 bloques de 32 son recursión, que
  la descomposición no acelera. No se puede poner esta cifra en los presupuestos junto a las medidas.
- **TOPLOC:** «258 bytes por 32 tokens», «10–100 veces más rápido», «sobrecarga del 1–3%». Dos trabajos
  lo confirman de memoria, tres — «no puedo verificarlo»; para SkyNet no se ha medido nada de esto.
- **No se pudo verificar:** las cifras de DeepProve y FlashProve, Verde (en las auditorías hay tres conjuntos distintos
  de recargos), las pérdidas de TEE en H100, el precio de DLEQ en gas, los estados e incidentes de Bittensor y otras
  redes, varios números de arXiv.
- **Atribuciones erróneas:** el algoritmo Krum se atribuye a autores equivocados (MEH); una auditoría tiene
  un error aritmético en el umbral (`c_f ≈ 0,3c`, `p ≥ 0,73`).
- Una misma cifra en dos auditorías no son dos mediciones independientes: ambas pueden estar repitiendo
  una sola fuente.

## 2. Las ideas del propietario llevadas a construcciones

### 2.1. Verificabilidad dentro del modelo y reentrenamiento

- **«El modelo se protege a sí mismo» no funciona.** Los pesos y el código están abiertos; el defraudador no está obligado a ejecutar
  el modelo. Esto lo confirmaron los once trabajos.
- **«El modelo escribe huellas»** es un programa de hashing alrededor de pesos inmutables.
  No hace falta reentrenar y no añade nada.
- **Las sumas de control en las capas (ABFT)** detectan un fallo aleatorio. Un adversario que sabe busca
  un error que conserve la suma. La recursión, las tablas y la división en la atención no están cubiertas por sumas.
  Las críticas consideraron exagerada la tesis de varios trabajos de que «ABFT elimina el conflicto de D16».
- **El reentrenamiento solo tiene sentido para reducir `γ`:** conseguir que el perfil exacto coincida
  con los núcleos rápidos de 8 bits («canon simplificado», propuesta de DeepSeek). Los bits siguen
  siendo bits, la garantía no cambia. Riesgo: el primer perfil de 8 bits en D5 ya fue rechazado por calidad
  [medido]; el coste del entrenamiento y la pérdida de calidad no se han medido, y las horas de GPU nombradas
  en los trabajos son supuestos.
- **El reentrenamiento «para la robustez al redondeo»**, para que el perfil rápido se verifique con tolerancia,
  vuelve al contrato con tolerancia (sección 2.4) y no da una cota demostrable.
- **Un modelo con menos estado** reduce el tráfico de verificación del fragmento, pero no aumenta la proporción
  de sustituciones detectables.

**Veredicto:** funciona una sola forma — la aceleración del perfil exacto. Se resuelve con un experimento.

### 2.2. Huellas y recálculo de un fragmento aleatorio

**Construcción.** El ejecutor, antes de elegir al verificador, sella con una sola raíz los tokens
y los estados intermedios. El verificador elige en secreto un fragmento, recibe la entrada sellada
del fragmento y lo recalcula en el perfil exacto. El fragmento se puede verificar sin recalcular todo
el principio de la respuesta: esto también lo confirma D5, donde la pasada por fragmentos da los mismos hashes de estado [medido].
La afirmación de varios trabajos de que «no se puede recalcular un fragmento sin el prefijo» fue rechazada por la crítica.

**Por qué no se evade la cota `1 − s/N`.** El defraudador calcula honestamente todo salvo una celda,
y continúa honestamente desde el valor sustituido. El rastro es coherente en todas partes salvo en una transición.
Si se abren `s` de `N` transiciones, habrá una transición que se verifica con probabilidad
no mayor que `s/N`. Las huellas hacen que la mentira sea localizable, pero no la multiplican. Solo puede
evadir la cota una verificación en la que cualquier mentira rompa una gran proporción de igualdades (pruebas breves),
y su precio es el mismo.

**Dos tipos de cortes** [cálculo según la configuración de D5]:

| Corte | Qué certifica | Qué hay que transmitir | Qué no detecta |
|---|---|---|---|
| Por capas: un bloque en toda la secuencia | Una transición del bloque desde la entrada presentada; el bloque es alrededor del 2,65% de la pasada, la cabeza de salida — alrededor del 15,1% | 0,78 / 4,9 / 14,6 MiB con 160 / 1000 / 3000 posiciones | Una sustitución reunida en otra capa: probabilidad 1 de 32–33 |
| Por posiciones: todas las capas en un segmento de 64 posiciones | Los tokens del segmento son iguales a la elección exacta con el estado sellado del límite izquierdo | 48 MiB de estado y 64 KiB por cada posición anterior: 58 / 110 / 236 MiB | Una posición sustituida fuera del segmento: pasa con probabilidad `1 − L/T`, por ejemplo 93,6% con 500 + 500 tokens |

Además, el ejecutor debe almacenar 0,13–2,38 GiB de puntos de control por respuesta durante la ventana de
disputa [cálculo]. En el registro solo puede ir la raíz de 32 bytes: el estado en sí es 3–5 órdenes de magnitud
mayor que el registro de D24.

**Falsificación «borrador con perfil rápido + pasada exacta».** La encontró la crítica Claude. El defraudador
genera la respuesta en Q8_0, luego hace una pasada exacta sobre los tokens listos e imprime el rastro.
En ese rastro son coherentes todas las transiciones de todos los bloques; solo no coinciden las posiciones en las que el token
del borrador difiere de la elección exacta.

- El precio de la falsificación es `c·(1/γ + ρ)`, el ahorro frente al trabajo honesto es `1 − 1/γ − ρ`: 18,4% con
  `γ = 1,65`, `ρ = 0,21`; la falsificación es rentable cuando `ρ < 1 − 1/γ` (0,34 / 0,39 / 0,44 con `γ` =
  1,52 / 1,65 / 1,78) [cálculo].
- El corte por capas no la detecta (salvo la probabilidad 1 de 32–33 en la cabeza de salida).
- El corte por posiciones de longitud 64 la detecta con probabilidad 97% si los tokens de Q8_0 y del perfil exacto
  coinciden en el 95% de las posiciones; 49% con coincidencia del 99%; 29% con 99,5%; 6,5% con 99,9% [cálculo].
  La proporción de coincidencia no se ha medido.
- La verificación completa la detecta siempre. El agujero solo afecta a los esquemas en los que el corte **sustituye**
  la pasada completa.

Consecuencia: el corte certifica «el ejecutor pagó al menos la pasada exacta», no «la respuesta
fue generada por el perfil exacto». Aquí las críticas discreparon: DeepSeek considera que el corte
por posiciones detecta la sustitución de toda la respuesta por Q8_0 con probabilidad 1; MiniMax — que esa probabilidad
no se ha medido; Claude aportó el cálculo anterior. Lo decide la medición de la coincidencia de tokens.

La crítica de MiniMax añadió: la falsificación gratuita «cortar la respuesta antes» no crea celdas falsas
en absoluto. La longitud de la respuesta y la causa de la parada deben entrar en el objeto de la verificación.

**Qué da aun así la raíz del rastro:**

- **Disputa por división en dos.** Dos partes con rastros distintos convergen en un número logarítmico de movimientos
  a un solo paso, que cada nodo recalcula por sí mismo. La crítica precisó: los 15–23 movimientos declarados bastan solo
  hasta la celda, dentro del bloque hacen falta unas 27 divisiones más; la regla
  «el silencio es derrota» exige el cálculo M9.
- **Dispositivo débil.** El pagador sin tarjeta gráfica puede verificar un segmento por cada
  respuesta. Esto da la marca «verificado parcialmente», no «verificado». El precio para él es el tráfico
  de 52–300 MiB por respuesta y el tiempo de procesador; en el teléfono no se ha medido.
- **Inmutabilidad del historial del ejecutor** y disputa por una petición privada con revelación de una celda.

**Veredicto:** la construcción es posible y útil para la disputa y el dispositivo débil, pero no abarata la garantía D1
y D25. Para que la sustitución puntual sea menos rentable que la inacción, con 32 bloques hay que
abrir 2 / 4 / 7 / 10 bloques con un margen del 5 / 10 / 20 / 30% [cálculo], y contra el daño (D6)
tampoco ayuda.

### 2.3. Técnicas de los juegos

| Técnica | Dónde el movimiento está acoplado al cálculo | Dónde no lo está |
|---|---|---|
| «Sellé — abrí» | El fragmento abierto debe coincidir con el recálculo desde la entrada sellada | El sellado en sí no demuestra nada: se puede sellar también una mentira coherente |
| «Uno corta — otro elige» | La elección se hace tras la fijación con la moneda secreta del verificador | El que corta estropea una parte de `N`; no hay ahorro frente a la verificación completa |
| Moneda común de dos partes | No hace falta cuando está en juego el dinero de un solo pagador: basta su moneda secreta | Quien se revela el último frustra el resultado desfavorable; con colusión total, la coalición conoce todas las aportaciones |
| Cartas sin crupier (mental poker) | — | Para elegir el número del fragmento es redundante: lo mismo hace una sola función aleatoria verificable |
| «Cada uno vigila al rival» | El pagador verifica su respuesta — en esto se basan todas las variantes de la sección 3 | El ejecutor no puede castigar a un pagador deshonesto sin depósito (cálculo M9) |
| Cartas marcadas, comprador secreto | — | El secreto de la trampa en una red abierta solo lo guarda el pagador, por eso la trampa coincide con su verificación y es más cara que ella |

Una fuente pública común de aleatoriedad solo hace falta allí donde se verifica el dinero ajeno; entonces
rige D20 (no menos de dos fuentes independientes).

**Veredicto:** de los juegos se toma el orden de los movimientos y el principio principal «verifica quien tiene su dinero en juego».
El juego no convierte el muestreo en verificación completa.

### 2.4. Ejecutor rápido y juez exacto

**Contrato con tolerancia.** El ejecutor calcula en Q8_0 rápido, el pagador hace la pasada exacta
y acepta la respuesta si en cada posición la puntuación del token elegido queda por detrás de la máxima
en no más de `m`. Ventaja frente al «certificado con margen» rechazado antes: el veredicto
se calcula con números enteros y es igual en cualquier dispositivo. Pero la crítica encontró cuatro defectos.

- **La tolerancia legaliza respuestas ajenas.** Cualquier borrador más una pasada exacta muestra
  al ejecutor todas las puntuaciones; corrige las posiciones fuera de la tolerancia y obtiene una respuesta admisible. El productor más
  barato de tal respuesta es el modelo-borrador más barato, no el Q8_0 del mismo modelo.
- **La libertad de elección es un canal de daño.** En las posiciones con una diferencia menor que `m`, el token lo elige
  el ejecutor, incluida la parada temprana. Ejemplo: las puntuaciones de «continuar» y «detenerse» son
  100 y 99; con `m = 1`, una respuesta cortada pasa la verificación completa. Tal texto recibiría
  la marca «verificado con tolerancia» — en esencia es una violación de D6. Una marca parecida ya la rechazó el
  consejo anterior.
- **El ejecutor honesto se ve obligado a verificarse a sí mismo**, si no pierde la suma por un solo valor atípico,
  incluso en una entrada elegida por el pagador. Entonces el precio es `1 + ρ·γ`: +15…+71% con lote 1,
  y con lote 8 no hay ganancia frente a la generación exacta [cálculo].
- **El precio declarado «+0,01…+2,3%» no resistió:** para abrir fragmentos, el ejecutor necesita
  los hashes de estado del perfil exacto, es decir, una pasada exacta por cada generación [cálculo].

Incluso con un ejecutor rápido, la pasada exacta completa del juez cuesta en la RTX 2060 no menos del 31,9%
del tiempo de la generación normal [cálculo], así que este contrato no encaja cada respuesta en el 5%.

**Decodificación especulativa exacta** — el mismo contrato con `m = 0`. El borrador se obtiene como
sea, solo se paga la respuesta bit a bit igual a la exacta. El contrato y la garantía no cambian,
D6 no se ve afectado. El precio depende de la proporción de coincidencia de tokens y de la longitud de las series coincidentes; la cota inferior
es `1 + ρ·γ`. No se ha medido; con una coincidencia por debajo de aproximadamente el 95% resulta peor que la generación exacta directa.

**TOPLOC y huellas con tolerancia en coma flotante.** La huella certifica que
las activaciones son coherentes con el texto, no de dónde salió el texto. Falsificación: texto de cualquier modelo,
luego una pasada del modelo declarado sobre este texto — las huellas son auténticas. El veredicto con tolerancia
depende del hardware: dos nodos honestos pueden discrepar, por eso no se puede quemar la suma por él, y D4 se viola
literalmente. Para que la tarifa con tolerancia sea barata, el verificador necesita
una referencia que no tiene hasta que él mismo ha calculado la pasada exacta.

**Veredicto:** el contrato con tolerancia y las huellas con tolerancia no entran en la lista de variantes:
cambian el producto y ponen una marca a un texto elegido por el ejecutor. Solo son admisibles como señal
para una verificación exacta adicional. La decodificación especulativa exacta es candidata a
abaratar, se resuelve con una medición.

## 3. Variantes integrales

El precio es el recargo computacional completo respecto a la generación normal Q8_0 sin verificación
[cálculo según las mediciones de D5]. No incluye el registro, las disputas, el almacenamiento, el tráfico ni la energía: no
se han medido. La ganancia es la esperada, por una falsificación presentada. El extremo inferior «+67%» une la `ρ`
de la tarjeta RTX 4070 Laptop con la `γ` de la tarjeta RTX 2060; en una sola RTX 2060 el intervalo empieza en +84%.

| № | Variante | Precio con lote 1 | Dinero del defraudador con `q` = 0,1 / 0,3 / 0,5 / 1 | Novato con la cuenta vacía | Saboteador sin beneficio | Principal riesgo residual |
|---|---|---|---|---|---|---|
| V1 | Verificación completa de cada respuesta por el pagador | +67…+149% (en una sola RTX 2060 +84…+149%) | `−c_f` con todos los `q` | `−c_f` | No hay marca falsa de «verificado»; puede arruinar la entrega | Pagador perezoso; rechazos falsos del pagador (M9) |
| V2 | Lotería por pedidos enteros | +53…+82% y reserva del comprador `R/p` | `−c_f` con todos los `q` | 0 | La proporción `1 − p` de respuestas no se verifica y nada la contiene | Ingreso irregular; la reserva es una cuestión para R5 |
| V3 | Moneda secreta del pagador y suma bloqueada | +50…+82%; la verificación en sí 0,005–3,6% | No más que cero con todos los `q`, si el pagador lanza la moneda a tiempo | `−c_f` (verificación siempre) | Pasa la proporción `1 − p`: hasta el 99,98% | Pagador perezoso reconocido — hasta `+R`; un fallo honesto quema la suma |
| V4 | Tareas con resultado verificable | `(N − 1)·v/w`, no medido | `−c_f` con todos los `q` | 0 | Un testigo incorrecto no pasa | No es una respuesta del modelo ni un paso de entrenamiento |
| V5 | Capa adicional: decodificación especulativa exacta sobre V1 o V3 | No medido; cota inferior +15…+71% | Como en la variante portadora | Igual | Igual | La coincidencia de tokens no se ha medido |

**El pagador sin equipo** no tiene garantía en ninguna variante. Si encarga la verificación
a un trío de nodos asignados, el pago falso esperado es `R·q³`: 0,001`R` / 0,027`R` / 0,125`R`
/ `R` con `q` = 0,1 / 0,3 / 0,5 / 1 [cálculo]. Esto ya está escrito en D21.

### V1. Verificación completa de cada respuesta por el pagador

**Pasos.** El pedido fija el modelo, el perfil, la semilla, los límites de longitud y la condición de aceptación.
El ejecutor calcula la respuesta en el perfil exacto y fija con un solo registro el criptograma y la raíz
del rastro. El pagador, antes de mostrarla, recalcula toda la respuesta en una pasada, incluida la longitud y la causa de la
parada. Una discrepancia significa impago; la suma en espera no se quema. La marca «verificado»
solo se pone tras la pasada.

**Garantía y supuestos.** Una respuesta falsa no se paga ni recibe la marca con cualquier proporción
de colusión, para el novato y para cualquier número de claves. Supuestos: los bits coinciden en el dispositivo
del pagador (mostrado en seis ejecutores [medido], en teléfonos no); el núcleo de verificación
es correcto; el pagador verifica de verdad.

**Precio.** `γ·(1 + ρ) − 1`: +67…+149% con lote 1; +211…+358% con lote 8 (en una sola RTX 2060
+251…+358%). Ejemplo `γ = 1,65`, `ρ = 0,21`: +99,65%. Al pagador la verificación le cuesta el 15–71%
del tiempo de su propia generación normal [cálculo].

**Qué cambiar en las decisiones.** Nada; hacen falta precisiones de D6 (dos marcas, no hay intermedias),
D16 (con verificación completa una discrepancia solo conlleva impago) y D22 (sección 4).

**No medido.** La calidad del perfil exacto (experimento O5); `γ` en otras tarjetas; el tiempo y la memoria
en portátil y teléfono; el precio de la disputa; el comportamiento ante rechazos falsos del pagador.

### V2. Lotería por pedidos enteros

**Pasos.** El comprador reserva el premio de antemano. Todos los resultados del lote se fijan antes del sorteo.
El sorteo elige la proporción `p` de pedidos; los elegidos el pagador los verifica por completo y paga `R/p`;
los demás no se pagan y se marcan «no verificado».

**Garantía y supuestos.** El pago falso es imposible incluso con la cuenta vacía y sin quema de
sumas; no hace falta cambiar D16. Supuestos: sorteo según D20; la reserva del comprador no se considera depósito.

**Precio.** `γ·(1 + p·ρ) − 1`: +53…+82% con lote 1; ejemplo `p = 0,05`, `γ = 1,65`, `ρ = 0,21`:
+66,73%. Pero por cada resultado **verificado** recae `1/p` veces más trabajo.

**Puntos débiles.** El ingreso es irregular: con `p = 0,1`, un novato honesto con probabilidad 34,87% no recibirá
nada por los primeros diez pedidos; con 6000 tareas al mes, `p = 0,01` y un coste del 95% del precio
la probabilidad de un mes deficitario es 33,10% [cálculo]. Las respuestas no verificadas no están contenidas por nada: el saboteador
con claves gratuitas suministra basura gratis.

**Qué cambiar.** Responder si la reserva `R/p` son «fondos por adelantado» según R5; elegir las fuentes
de aleatoriedad según D20.

**No medido.** La probabilidad exacta de ruina en el recorrido, el tamaño de la reserva, la demanda de tal tarifa.

### V3. Moneda secreta del pagador y suma bloqueada

Esta es la estrategia del consejo 5 ([STRATEGY_SEARCH](STRATEGY_SEARCH.md)) con correcciones.

**Pasos.** La respuesta se fija en el perfil exacto. Tras la fijación, el programa del pagador lanza
su moneda secreta y verifica la respuesta por completo con probabilidad no menor que `R/(R + H_lock)`;
con el novato — siempre. Una discrepancia demostrada quema con una sola acción toda la suma no madurada
de la clave, incluidas las recompensas de la misma ola; al perjudicado se le devuelve no más que `R`. La suma no madurada
no se puede transferir, vender ni pignorar. Una respuesta omitida por la moneda se paga
y se marca «no verificado».

**Garantía y supuestos.** El resultado esperado de cualquier serie de falsificaciones no supera la suma bloqueada
con cualquier proporción de colusión: ejemplo de control — una ola de diez falsificaciones da +4,4295`R` sin
quema y −2,49676`R` con ella [cálculo, reproducido por los críticos]. Supuestos: el pagador
lanza de verdad la moneda y verifica a tiempo; el registro está disponible; la suma realmente
se pierde.

**Precio.** +50…+82% con lote 1; la verificación en sí en claves maduras — 0,005–3,6% del trabajo. La primera
ventana del novato cuesta 1,3–5,3% del trabajo de la ventana en unidades de generación exacta [cálculo].

**Puntos débiles.** El agujero del pagador perezoso no lo cierra ninguna reparación: con la cuenta vacía
y `λ > 0` el umbral es inalcanzable. Con el D16 vigente, el defraudador declara la falsificación un fallo y recibe
`(1 − p)·R − c_f`. El saboteador pasa con probabilidad `1 − p`. Un añadido barato es el límite inferior
de frecuencia (por ejemplo, `p ≥ 1/11` cuesta 0,9–3,6% del trabajo), pero aun así pasa el 90,9% de las falsificaciones del saboteador
[cálculo].

**Qué cambiar.** D2, D11 y D21 (pago de la respuesta omitida por la moneda); D7; anulación de D16 para
una discrepancia publicada; nueva decisión sobre la suma bloqueada; respuesta a si la quema es una penalización según R5;
cálculo M9.

**No medido.** La frecuencia de fallos silenciosos de hardware — de ella depende cuántos participantes honestos
perderán la suma; la proporción de pagadores que realmente ejecutan la verificación.

### V4. Tareas con resultado verificable

**Pasos.** El plan (D9) autoriza de antemano una tarea cuyo resultado va acompañado de un testigo
verificable por máquina: pruebas, demostración formal, solución de un problema con certificado
de optimalidad. La solicitud se sella antes de revelar el testigo, para que este no se pueda
interceptar. Cada nodo verifica el testigo por sí mismo; el pago — una vez por el contenido de la tarea.

**Garantía.** Un testigo incorrecto no pasa con colusión total, cuenta vacía y cualquier número de
claves.

**Precio.** Si `N − 1` nodos verifican con `v` a un coste de generación `w`, el recargo
`(N − 1)·v/w`. Con `N = 1000` encaja en el 20% solo si `v/w ≤ 2·10⁻⁴`; con `v/w = 10⁻³`
ya es el 99,9% [cálculo]. La relación `v/w` se toma de las auditorías y no se ha medido.

**Puntos débiles.** Es otro producto: no una respuesta libre del modelo ni un paso de gradiente. La tarea
se puede resolver sin modelo y sin tarjeta gráfica. No se presenta una regla que genere tareas difíciles útiles.
La verificación del testigo es copiable, por eso no se paga según D15: la idea de que «el teléfono
gana verificando certificados» la contradice.

**Qué cambiar.** Complementar D9 y D15; D18 sigue siendo investigación.

**No medido.** Qué proporción del trabajo de la red encaja en esta clase.

### V5. Capa adicional: decodificación especulativa exacta

El borrador se obtiene por cualquier vía rápida; el ejecutor lo coteja él mismo con una pasada exacta
y corrige las discrepancias; solo se paga la respuesta bit a bit exacta. La garantía es la misma que
la de la variante portadora V1 o V3; las decisiones, salvo la precisión de D22, no cambian. La ganancia es posible
solo si los tokens de los perfiles rápido y exacto coinciden a menudo y en series largas. Nada
de esto se ha medido.

## 4. Recomendación del consejo y primer paso

**Recomendación (compendio).** El contrato principal es **V1**. Es el único que cumple D1, D6, D7 y D25 para
la respuesta sin nuevos supuestos sobre la frecuencia, la suma bloqueada y la quema, y no requiere modificar las decisiones
adoptadas. Los once trabajos dan para él la misma fórmula de precio. **V4** — un tipo aparte de
tareas del plan. **V2** — una tarifa para lotes acordados. **V3** — candidata: incluirla solo
tras el cálculo M9 y decisiones explícitas del propietario. **V5** y la aceleración de los núcleos exactos son vías
para reducir el precio, no contratos separados.

**Precisiones de las decisiones para V1** (propuestas, no decisiones):

- D6: hay dos marcas — «verificado» tras una verificación completa bit a bit antes de mostrarse y «no verificado».
- D16: con la verificación de cada respuesta por el pagador, una discrepancia solo conlleva impago.
- D19: si el intento es gratuito, el supuesto de D19 no se aplica.
- D22: el borrador se puede obtener de cualquier forma; solo se paga la respuesta bit a bit
  igual a la exacta. La longitud de la respuesta y la causa de la parada entran en el objeto de la verificación.
- D12 no cambiar: sustituir el tiempo activo por la altura de bloques de la cadena externa permite que las sumas no maduradas
  maduren mientras la red no está disponible.
- Nueva decisión sobre el precio: en qué perfil se cuenta el volumen de cálculo. Con un precio de 1,10 respecto al
  coste del perfil normal, el trabajo honesto en el perfil exacto es deficitario en un 42–68%
  del coste [cálculo]; esta premisa en sí no está aprobada en el proyecto.

**Un cálculo.** M9: disputas falsas sin depósito para un pedido de un solo uso — silencio de cada
parte, autodisputa, autopedido con disputa falsa, límites de bytes y de cálculo por caso, fuente
de los fondos. Sin él no se activa ninguna variante (D23).

**Un experimento** (hace falta permiso del propietario; ampliación de O3 y O4 ya realizados). Sobre el perfil
v2 ya montado y llama.cpp Q8_0 con un prefijo común, medir la proporción de coincidencia de tokens, la distribución
del retraso de la puntuación del token elegido y las longitudes de las series de coincidencia. Resuelve tres cuestiones:
si V5 se amortiza; si el contrato con tolerancia es viable; si el corte por posiciones detecta la falsificación
«borrador + pasada exacta», es decir, si el pagador sin tarjeta gráfica tiene alguna protección.
Primero conviene comprobar si en los registros de D5 se conservaron las puntuaciones completas de ambos perfiles.

**Dónde discreparon las críticas y los trabajos.**

1. **Qué contrato es el principal.** Los críticos Claude y ChatGPT — V1. El crítico DeepSeek — V3 con reparaciones,
   y V1 como tarifa cara y modo de novato. El crítico MiniMax — V1 como tarifa básica y moneda
   para claves maduras, pero la red solo paga lo verificado.
2. **Si pagar la respuesta omitida por la moneda.** A favor — la mayoría de los trabajos; en contra — los dos trabajos
   de ChatGPT y uno de MiniMax. Si no se paga, el ejecutor honesto recibe `p·R`
   por tarea, y eso es una lotería sin multiplicador `1/p`. No hay tercera opción; es una elección del propietario.
3. **Qué experimento es el primero.** Los críticos Claude y ChatGPT — la coincidencia de tokens de los dos perfiles.
   Los críticos DeepSeek y MiniMax — un microbenchmark de núcleos de 8 bits tipo Ozaki con cotejo bit a bit:
   muestra si la referencia del 5% es alcanzable en general. El compendio lo pone en segundo lugar.
4. **La `γ` alcanzable.** 1,05–1,20, 1,1–1,3 o «no bajará». No medido.
5. **Si son depósito según R5** la quema de la suma no madurada, la reserva de disputa, la reserva de la lotería,
   el largo plazo de maduración y el aval.
6. **Si limitar la suma bloqueada por arriba.** Un techo de 10`R` limita el número esperado de
   falsificaciones, pero hace la verificación de las claves maduras unas 400 veces más cara [cálculo de un
   crítico, no recalculado].
7. **La tercera marca.** El crítico MiniMax propone «verificado parcialmente»; el crítico Claude — solo
   dos marcas.

## 5. Entrenamiento: qué hay y qué no hay

**Qué no hay.** Ningún trabajo da una garantía para el paso de entrenamiento. El entrenamiento no tiene pagador:
la base de la emisión de créditos debe verificarla cada nodo completo. El entrenamiento entero
no está construido ni medido; las mediciones de D5 se refieren solo a la pasada directa y no se trasladan a la pasada
inversa ni al optimizador.

**Qué hay.**

- **Repetición completa del paso por cada nodo** — estricta, pero cuesta `N` pasos adicionales: con diez
  nodos, alrededor del 1000% [cálculo].
- **Cortes del paso:** el nodo verifica una celda de aproximadamente cada cuatro mil. Precio 0,24% / 2,4% /
  24% con 10 / 100 / 1000 nodos [cálculo], pero con colusión total la detección es cero.
- **Pago del resultado verificable** (V4): garantía estricta para una afirmación estrecha. Se verifica
  el testigo de la tarea, no el paso de gradiente; las formulaciones de los trabajos «el entrenamiento está resuelto» y «el daño está excluido»
  fueron consideradas exageradas por la crítica.
- **Pago por una mejora demostrada en el examen** (D18) sigue siendo investigación: el examen
  certifica la nota en un conjunto dado, pero no la ausencia de una puerta trasera en los pesos.

**Límite.** Con 1000 nodos y un recargo del 20%, toda la verificación independiente de un nodo debe costar
no más de 0,0002 del trabajo del paso [cálculo]. Una prueba breve del paso, según todos los presupuestos del proyecto,
es órdenes de magnitud más cara.

**Recomendación del consejo.** Emitir créditos solo por resultados que cada nodo verifica
por sí mismo; no incluir en la versión del modelo un paso no verificado (esto ya es D6).

## 6. Qué es literalmente irrealizable: preguntas al propietario

El consejo no propone cambiar los textos R1–R6. Las propuestas de dos trabajos de modificar R4 y R6 fueron rechazadas por la crítica:
son la base inmutable. La imposibilidad general de conciliar R4 y R6 para todos los algoritmos concebibles
no está demostrada; abajo está lo que es irrealizable con las construcciones encontradas.

| № | Qué es irrealizable | Relajación mínima | Recomendación del consejo |
|---|---|---|---|
| 1 | Proteger al consumidor sin equipo con colusión total de los verificadores: los casos honesto y falso le dan mensajes idénticos | La garantía se promete solo a la parte que verifica por sí misma; a los demás la respuesta se les muestra con la marca «no verificado», y la magnitud del riesgo `R·q³` se nombra directamente | Aceptar: esto ya está escrito en D21, solo hay que trasladarlo a la descripción para el usuario |
| 2 | Verificar el paso de entrenamiento con colusión total dentro del 20% | (a) pagar por el resultado verificable, no por el paso; (b) admitir «al menos un nodo completo honesto»; (c) retirar la referencia del 20% para una red pequeña | (a): la única vía con garantía estricta; con ello, parte de la potencia libre queda sin entrenamiento pagado |
| 3 | Encajar la respuesta verificada en el 5% con la `γ` medida = 1,52–1,78 | Considerar la referencia del 5% un objetivo de ingeniería, publicar el precio real y llevar la reducción de `γ` como tarea aparte | Aceptar; el 5% es una referencia de la hoja de ruta, no el texto de R6 |
| 4 | Contener con la economía a un saboteador que no necesita beneficio, con `p < 1` | Solo las marcas y la prohibición de usar lo no verificado (D6) | Ya adoptado; no hay medidas nuevas |
| 5 | Disputa sin depósito con un fondo finito de disputas | Decidir si el prepago bloqueado del comprador se considera depósito según R5 | Decidir tras el cálculo M9 |
| 6 | Tener plena confianza en la decisión antes de cualquier medición | Permitir una lista limitada de mediciones de las que depende la elección | Decisión del propietario; el consejo nombra dos mediciones de la sección 4 y el experimento O5 |

Preguntas adicionales: si pagar la respuesta omitida por la moneda (sección 4, punto 2);
en qué perfil se cuenta el precio de la tarea; si admitir el aval de un tercero.

## 7. Qué calcular con miniagentes y qué comprobar con experimentos

**Cálculos** (fracciones exactas, hash de control, repetición en un segundo dispositivo; no son experimentos sobre el protocolo):

1. M9 por todas las ramas de un pedido de un solo uso.
2. Ganancia de la falsificación «borrador + pasada exacta» bajo cortes en una malla de `γ`, `ρ`, proporción de coincidencia,
   longitud del segmento y de la respuesta, margen.
3. Moneda con límite inferior de frecuencia y proporción de pagadores perezosos, incluida la cuenta vacía.
4. Falsificación mixta «todo honesto salvo una columna» y falsificación por corte de la respuesta.
5. Lotería: probabilidad exacta de ruina en el recorrido y tamaño de la reserva del comprador.
6. Tamaños exactos de la entrada de la celda y del paso de disputa según el desglose del perfil v2 (cotejar 48 MiB y 64 KiB).
7. Inundación con claves nuevas: carga sobre el pagador y deducción de la cuota de claves nuevas.
8. Enumeración de los conjuntos falsos mínimos de celdas en un modelo pequeño.
9. Conciliación de `ρ` y `γ` en una misma tarjeta y con longitudes iguales; precio por un resultado verificado.

**Experimentos.** O5 está autorizado por la decisión D5. Los demás están fuera de D5 y requieren permiso del propietario:

1. Coincidencia de tokens y retraso de las puntuaciones de Q8_0 frente a v2 — primer experimento.
2. O5 — calidad del perfil v2 en 320 tareas.
3. Microbenchmark de núcleos de 8 bits con cotejo bit a bit — comprobación de la estimación de Ozaki.
4. `γ` y `ρ` por pares en una misma tarjeta, incluida la RTX 4070 Laptop.
5. Tiempo y memoria de la pasada y del segmento en el procesador de un portátil y en un teléfono.
6. Precio de la impresión del rastro, cobertura de ABFT y frecuencia de fallos silenciosos.
7. Experimentos de entrenamiento O6 y O7 — aparte, tras la decisión sobre D18.

## 8. Quién hizo qué

- **ChatGPT:** dos trabajos independientes y una crítica de todos los trabajos.
- **DeepSeek:** dos trabajos independientes y una crítica con recálculo de las cifras con aritmética exacta.
- **Claude:** dos trabajos independientes, una crítica y este compendio.
- **MiniMax:** cinco trabajos independientes y una crítica.
- **Gemini** no participó en el consejo: no había clave en el hub de modelos; su auditoría estaba entre
  los datos de entrada.
- **Las auditorías externas y los mapas de mecanismos** son datos de entrada reunidos por el propietario; el consejo
  no los cotejó con las fuentes primarias.

Limitaciones del compendio: el crítico ChatGPT analizó diez trabajos de once; el crítico Claude leyó
uno de los trabajos no del todo; los cálculos de los críticos se hicieron cada uno en un ordenador y esperan
la repetición por miniagentes.
