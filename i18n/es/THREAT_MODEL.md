<!-- translation of docs/THREAT_MODEL.md, source sha256: 96c64b91168c36392f3f705d1ce619df7c73340c08bffee57773d75508990fff -->

# Modelo del adversario y tabla de ataques

[English](../../docs/THREAT_MODEL.en.md) · [中文](../zh/THREAT_MODEL.md) · **Español** · [Français](../fr/THREAT_MODEL.md) · [Deutsch](../de/THREAT_MODEL.md) · [Italiano](../it/THREAT_MODEL.md) · [Русский](../../docs/THREAT_MODEL.md) · [Português](../pt/THREAT_MODEL.md) · [العربية](../ar/THREAT_MODEL.md)

Estado a 24 de noviembre de 2026.

Este documento es el resultado del consejo de modelos para la etapa 1 de la hoja de ruta («Planteamiento exacto»,
[ROADMAP](ROADMAP.md), sección 4). En él se reúnen el modelo del adversario, el cotejo del número de ataques,
el estado de cada uno de los 60 ataques de la especificación para las variantes A y B, los nuevos ataques hallados por el consejo
y las preguntas que solo puede resolver el propietario del proyecto.

**Estado del documento.** Es un resultado de razonamiento y cálculo por fórmulas, no una medición.
No hubo experimentos, ejecuciones de la red ni recálculos por programa para él. Las cifras con la marca
[cálculo] se obtienen por las fórmulas de los trabajos del consejo y fueron comprobadas a mano por los críticos; no se repitieron
en un segundo dispositivo. Solo se convierte en decisión adoptada lo que apruebe el propietario
del proyecto. Todo lo demás aquí es una estimación del consejo y, cuando hay desacuerdo con ella, se indica «discutible».

**Cómo leer.** La sección 1 define quién ataca y qué se considera ganancia. La sección 2 explica
la discrepancia entre 59 y 60. La sección 3 es la tabla principal: con ella cualquier participante puede nombrar
un ataque sin cerrar y comprobarlo con los documentos de origen. La sección 4 es un resumen breve y la sección 5,
las preguntas al propietario; la sección 6, quién participó.

Documentos de origen: las decisiones D1–D5 en [ROADMAP](ROADMAP.md), sección 3; las variantes A y B en
[CURRENT_DESIGN](CURRENT_DESIGN.md), sección 3; [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); la primera ejecución [FIRST_RUN](FIRST_RUN.md);
los requisitos obligatorios [REQUIREMENTS](REQUIREMENTS.md). La tabla de 60 ataques está tomada
de la especificación de la red sin coordinadores del 20 de noviembre de 2026 (en adelante SPEC); los números de fila
1.1–7.4 son los suyos.

---

## 1. Modelo del adversario

### 1.1. Símbolos y variantes

| Símbolo | Significado |
|---|---|
| `R`, `c` | Precio de la tarea y coste de la ejecución honesta, `c ≤ R` |
| `H` | Suma en espera: recompensas no maduradas de la clave de los últimos tres días. Solo se puede anular esa suma (no hay depósitos ni multas, requisito R5) |
| `p` | Proporción de verificación: en A `p = 4R/(R+H)`, pero no menos del 1%; en B es constante, por ejemplo el 1% |
| `B` | Anulación en A: `B = 4R/p − R`, no mayor que `H`; con `p > 1%` es `B = H`, si no `B = 399R` |
| `k` | Número de verificadores de la tarea, 3 (con rondas de sorteo, en promedio 3,5–4,5) |
| `q`, `q_eff` | Proporción de la coalición en todo el peso de los verificadores del modelo y entre quienes verifican realmente la tarea (sección 1.7) |
| `G` | Precio completo de la disputa en el registro |

**Variante A** (especificación actual): verificación por muestreo con anulación de `H`; la entrega no verificada
y no disputada se paga. **Variante B** (propuesta): solo se pagan las tareas elegidas por sorteo y confirmadas,
al precio `R/p`; lo no elegido no se paga a nadie; una falsificación detectada quema toda la `H` de la clave.
B está descrita a grandes rasgos, y el consejo analizó «B tal como está descrita»: en la descripción no hay
camino del novato, admisión de verificadores por `H`, tarifa de los verificadores ni fuente de `R/p` para las peticiones.

### 1.2. Quién ataca

Los perfiles están unificados en los seis trabajos. Las combinaciones son obligatorias: coalición con claves gratuitas,
arrendatario que se ha convertido en coalición, participante mucho tiempo honesto en colusión, usuario en colusión
con los verificadores, saboteador con claves gratuitas.

| Perfil | De qué dispone | Qué quiere |
|---|---|---|
| Solitario | Sus claves, su dispositivo, un programa modificado | Créditos sin trabajo o por encima del trabajo |
| Coalición con proporción `q` | Claves bajo gestión común; transmisión instantánea de resultados, pasos de cálculo, estados y peticiones; caja común | Dejar pasar una falsificación, cobrar verificaciones sin recálculo, ganar las votaciones |
| Dueño de muchas claves | Claves cuantas quiera casi gratis; el peso y la `H` de las claves nuevas son nulos | Colas, plazas de aprendiz, reparto de datos, asignaciones, billetes B |
| Arrendatario de potencia | Horas de GPU a precio de mercado, trabajo honesto y pagado por la red | Una parte del peso y luego colusión, un modelo raro o las reglas |
| Saboteador sin beneficio | Dispuesto a perder todas las recompensas no maduradas | El daño en sí: modelo, respuestas, puerta trasera, parada |
| Participante con la cuenta vacía | `H = 0`, sin peso | Cualquier pago sin trabajo |
| Mucho tiempo honesto y luego la marcha | Gran `H` y peso; elige el momento, el tamaño y el número de tandas | Más que `H` más el pago honesto de las últimas tareas |
| Usuario | Su petición, créditos, derecho de disputa, colusión con el ejecutor o con los verificadores | Una respuesta gratis, el reembolso de una respuesta correcta, datos ajenos |
| Operadores de retransmisores, puntos de encuentro, nodos de registro, puntos de acceso a la cadena de bloques, custodios de datos | Ven las direcciones y el tiempo, retrasan, no transmiten, muestran un entorno falso | Censura, aislamiento de un nodo, revelación de identidad, pago por los registros |
| Terceros | Faro de aleatoriedad, productor del bloque, proveedores de puntos de control, fabricante del modo protegido, distribuidor del programa | Desplazar el muestreo, colar una historia o un programa falsos |
| Dueño de dispositivos ajenos | Claves de trabajo robadas o infectadas | Confirmar falsificaciones arriesgando la `H` ajena |

### 1.3. Qué puede y qué no puede el adversario

**Puede:** crear claves cuantas quiera; ejecutar un programa modificado y leer todo en su propio
dispositivo, incluidas las peticiones privadas en modo normal; transmitir cualquier dato dentro de la coalición;
apagarse, elegir el momento de entrega, callar, dar datos a unos nodos y no a otros,
guardar una única copia; alquilar potencia; votar y comprar votos; ofrecer abiertamente
un soborno mediante un contrato inteligente (las confirmaciones están en el registro, el pago se puede ejecutar sin confianza);
como productor del bloque, no publicar el bloque y elegir uno de los dos valores de aleatoriedad;
controlar parte de los retransmisores y rodear un nodo; tener un beneficio externo o valorar el daño en sí.

**No puede** (son supuestos y hay que declararlos abiertamente): falsificar la firma de una clave ajena no robada,
encontrar una colisión de hash, abrir un compromiso de dos maneras, falsificar el sorteo secreto (VRF);
reescribir los bloques finales de una cadena de bloques pública: el registro no tiene clave de administrador y es
correcto (supuesto 1 de SPEC; el programa no está escrito); predecir o desplazar la aleatoriedad después
de fijar el paquete (supuesto 2; las fuentes no están elegidas; la mezcla protege de la predicción,
pero no de la elección por la última fuente, N13); obtener una coincidencia bit a bit sin calcular
(supuesto 3; no comprobado); cambiar el resultado del recálculo de un paso en el registro (supuesto 4; para el modelo completo
no está construido); cambiar el programa de un nodo ajeno (D4); anular créditos disponibles ajenos,
obtener un segundo pago por el mismo número, revocar un paquete entregado.

**Lo que la red no ve en principio:** a quién pertenecen las claves y si los participantes son independientes; si el
nodo ha dado los datos a otro; qué se ejecuta en un ordenador ajeno; en qué se diferencia el recálculo de una copia del estado
ajeno. Si los casos honesto y falso dan al nodo los mismos datos, ninguna regla los
distingue ([OPEN_QUESTIONS](OPEN_QUESTIONS.md)).

### 1.4. Ganancia del adversario y daño a la red

La ganancia se calcula para toda la coalición desde un mismo estado inicial, con los mismos derechos, tareas
y horizonte hasta el cálculo final, incluida la marcha. Se suman los créditos madurados, las devoluciones,
el valor del servicio recibido y de los nuevos derechos; se restan los costes reales (trabajo, energía, alquiler, gas,
pagos externos). Las transferencias dentro de la coalición se compensan, un crédito no se cuenta dos veces y la pérdida
de la víctima no es por sí misma ingreso de la coalición. Tipos de ganancia: créditos por una declaración falsa (falsificación, copia,
confirmación sin recálculo, fila ajena); costes ahorrados con el mismo pago; peso y plazas
en el sorteo; reembolso de una respuesta correcta o parte no pagada de los datos; ganancia por efecto: influencia en la
respuesta o el modelo, lectura de una petición ajena, control de las reglas, de la emisión, del catálogo, del plan, el daño en sí.

El daño a la red se calcula aparte, en sus propias unidades: se ha aceptado un resultado incorrecto; el resultado se ha usado
antes de la verificación; se han emitido créditos sin trabajo; un honesto ha perdido `H`; se han congelado los pagos o la entrada
de novatos; se han revelado datos privados; se han sustituido la historia, las reglas, el programa o la versión del modelo; la red
ha gastado trabajo en verificaciones y disputas impuestas. El daño sin ganancia no incumple D1, pero puede
incumplir otros requisitos; en la tabla esto es «n/a» con el nombre del requisito.

### 1.5. Formulación formal de D1

D1 (adoptado el 23 de noviembre de 2026): «el defraudador no obtiene lo que desea»; la ganancia esperada de una falsificación
no es mayor que cero en comparación con el trabajo honesto y con la inacción, para cualquier coalición, incluido un novato
con la cuenta vacía y cualquier número de claves; una fuga positiva limitada no satisface el criterio.

Sea `U(σ)` la utilidad esperada de la coalición con la estrategia `σ`. Para cada estrategia con una declaración
falsa hacen falta **ambas** desigualdades:

- `Δ₀ = E[U(σ) − U(inacción)] ≤ 0`: cada declaración falsa se sustituye por el rechazo de la tarea
  (la `H₀` ya ganada madura en ese caso);
- `Δh = E[U(σ) − U(trabajo honesto)] ≤ 0`: cada declaración falsa se sustituye por la ejecución honesta.

El requisito se aplica con cualquier `q` de 0 a 1, con `H = 0` y con cualquier número de claves. Para refutarlo
basta un estado admisible y una diferencia positiva. No se puede comparar con la mayor de las dos bases: con inacción 0, ganancia honesta 0,60
y declaración falsa 0,20, esa comparación da «no hay incumplimiento», aunque `Δ₀ = +0,20` [cálculo].

Un trabajo propuso dividir D1 en un nivel económico (solo créditos) y un nivel por efecto
(influencia en la respuesta y el modelo, lectura de la petición, daño). El consejo no lo adopta por sí mismo: la cuestión se remite
al propietario (sección 5, pregunta 1). En la tabla, la ganancia solo por efecto se marca «no (ef.)».

### 1.6. Principio general de la columna «datos para el rechazo»

Con la colusión del ejecutor con todos los verificadores asignados, el nodo solo ve datos acordados:
huellas del resultado y del paso, estados revelados con pruebas de inclusión. Todos ellos son compatibles
con la falsificación. Solo siguen siendo verificables de forma independiente la entrada y el modelo fijado, con los que el nodo
puede recalcular la tarea por sí mismo: alrededor del +100% del trabajo [cálculo]; ni A ni B lo exigen, y para
una petición privada un nodo ajeno tampoco tiene la entrada. Por eso en la tabla aparece a menudo «no, salvo recálculo
completo».

### 1.7. Proporción de colusión `q_eff`

Todos los umbrales del tipo «hasta el 91%» se refieren a la proporción de la coalición entre quienes verifican realmente la tarea.
`q_eff` es la proporción de la coalición entre los verificadores que (1) están admitidos a la tarea (según la regla 2.6 de SPEC,
en una tarea de un ejecutor veterano hace falta `H_v ≥ B`, hasta `399R`), (2) respondieron en el plazo de la ronda y (3) recibieron
los datos para verificar. Ejemplo [cálculo]: 3000 dispositivos domésticos honestos durante 8 horas y 100 honestos
las 24 horas frente a 800 arrendados las 24 horas. La proporción del adversario en todo el peso es del 42,1%
(19 200 de 45 600 horas-dispositivo al día); un dispositivo doméstico acumula alrededor de `144R < 399R`
y no está admitido a las tareas de ejecutores veteranos; entre los admitidos, `q_eff = 800/900 = 88,9%`,
`q_eff³ ≈ 0,70`. Salvedad de los críticos: esto afecta a las tareas con `B = 399R`. La condición (3) puede elevar
`q_eff` hasta uno con cualquier proporción global (N2). La fórmula `q^k` solo es válida para elecciones independientes;
en SPEC las rondas continúan hasta tres respuestas, y para una colusión parcial hace falta la distribución de los que respondieron.

### 1.8. Fórmulas básicas [cálculo]

- **A, una falsificación:** ganancia `R − 4R(1 − q³)`; deficitaria con `q < 0,9086`. **Novato A:**
  `p = 1`, `B = H = 3R`, ganancia `R(4q³ − 3)`.
- **A, marcha con falsificaciones** (recorrido de FIRST_RUN en un solo dispositivo, no confirmado): rentable desde
  `q = 0,875` (cualquier tamaño, tres tandas, regla «en curso no más de un tercio de `H`»; 1,00004·H₀ en
  0,875, 1,034·H₀ en 0,880), desde 0,890 (tareas idénticas), desde 0,800 sin la regla del tercio; sin colusión
  en 92 millones de estrategias no hay marcha rentable (la mejor, 0,980·H₀). Es un recorrido de familias, no una demostración.
- **B, una falsificación** es rentable con `q^k > pH/(R + pH)`; con `p = 1%`, `k = 3`: `q ≈ 0,928` para
  `H = 400R`, `0,659` para `40R`, cualquier `q > 0` para `H = 0`. El pago bruto medio por falsificación
  es `R·q^k` y no depende de `p`.
- **B, tanda de `N` falsificaciones:** `E = a^N·H₀ + N·a^(N−1)·q^k·R`, `a = 1 − p(1 − q^k)`. La primera
  falsificación es rentable con `H₀` por debajo de 2,8R / 14,3R / 52R / 105R / 269R para `q` = 0,3 / 0,5 / 0,7 /
  0,8 / 0,9. Con `H₀ = 0`, la mayor ganancia por clave es de alrededor de `q^k·R/(e·p·(1 − q^k))`: 0,037R / 1,0R /
  5,3R / 19R para `q` = 0,1 / 0,3 / 0,5 / 0,7. Una tanda sin recorrido es una estimación inferior.
- **Probabilidad de pago falso** por tarea sin disputa externa: en A `1 − p + p·s`, en B `p·s`
  (`s` es la probabilidad de colusión total en la elección); con `p = 0,01`, `s = 0,125`: 0,99125 y 0,00125,
  y el pago falso bruto con `R = 1`: 0,99125 y 0,125. No se pueden comparar las variantes solo por la frecuencia
  del pago falso.

---

## 2. Cotejo de «60 y 59»

En SPEC hay exactamente 60 filas (12 + 12 + 10 + 5 + 11 + 6 + 4): 18 cerrados, 6 deficitarios, 19 limitados,
16 abiertos y **uno que «no es ataque», la fila 1.9** (entregar un resultado correcto calculado en equipo ajeno
está permitido por la decisión D2); el resumen de CURRENT_DESIGN, sección 9, y el párrafo «En breve» de SPEC
sumaron solo cuatro categorías y perdieron la quinta; de ahí 59. Los seis trabajos y los tres críticos
llegaron a esto de forma independiente. La anotación correcta es: 60 = 18 + 6 + 19 + 16 + 1.

---

## 3. Tabla de ataques

### 3.1. Símbolos

**Estado:** cerr. — el nodo rechaza el ataque con los datos del registro bajo los supuestos indicados;
def. — el ataque es posible, pero deficitario en promedio hasta el límite indicado; lim. — es posible, pero el daño o la
ganancia están limitados por una regla; ab. — no hay solución; no es ataque.

**D1:** sí — la ganancia no es mayor que cero para cualquier coalición; **no** — hay una estrategia con
ganancia positiva al menos frente a una de las bases; cond. — se cumple solo bajo los supuestos indicados,
independientes de la proporción de colusión (supuestos 1–4 de SPEC, aún no construidos);
no (ef.) — no hay ganancia económica o no está establecida, pero se alcanza una ganancia por efecto
(sección 1.5); n/a — en el ataque no hay una declaración falsa con ánimo de ganancia, está afectado el requisito indicado;
? — la regla no está definida y el signo de la ganancia no está establecido.

**Datos** — con qué datos verificables de forma independiente rechazará el nodo una declaración falsa en caso de colusión
del ejecutor con todos los verificadores. «Discutible» — los trabajos o los críticos discrepan y la disputa no está resuelta.
Las referencias «N…» llevan a los nuevos ataques de la sección 3.9.

### 3.2. Ejecutor

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 1.1 | El novato con la cuenta vacía entrega una falsificación | def. hasta `q ≈ 0,909`: las primeras tareas se verifican siempre, ganancia `R(4q³−3)`. Discutible: el crítico ChatGPT considera la fila abierta, ya que las `3R` iniciales se pueden obtener copiando (2.2, N1) | **no** con `q ≥ 0,909`, y con cualquier `q > 0` mediante el pago de las reverificaciones de aprendiz | ab.: `R·q^k` por intento sin pérdidas, claves cuantas se quieran | **no** con cualquier `q > 0` | No, salvo recálculo completo por la entrada abierta; para una petición, solo el usuario | Verificar los primeros resultados pagados de un modo que cada nodo ejecute por sí mismo; hasta entonces, solo trabajo no remunerado. En B, admisión por `H` (N16) |
| 1.2 | Un participante veterano falsifica parte de las tareas | def. hasta `q ≈ 0,909`; el 99% de las falsificaciones no se verifican y quedan en la red | **no** con `q` alto | def. con `q^k R < p(1−q^k)H`: 0,928 con `H = 400R`, 0,659 con `40R`, cualquier `q` con `H = 0` o desde una clave vacía (N16) | **no** | No, salvo recálculo completo | Verificación del resultado pagado que no dependa de la proporción de colusión (etapa 4). En B, `p` y admisión en función de `H` |
| 1.3 | Mucho tiempo honesto, luego un gran engaño y la marcha | def. solo en las familias recorridas por debajo de 0,875 / 0,890 / 0,800 (sección 1.8) | **no** con `q ≥ 0,875`; por debajo, no demostrado | ab.: la campaña de salida no está calculada; con `H` pequeña es rentable con cualquier `q > 0` | **no** | No, salvo recálculo | Demostración para todas las estrategias en A; cálculo de la campaña de salida de B, incluida `H₀ = 0` (etapa 2) |
| 1.4 | Entrega una falsificación y desaparece al ver el muestreo | cerr.: el paquete no se revoca; la desaparición tras el muestreo es un resultado incorrecto | cond. | igual | cond. | Fila del paquete y ausencia de revelación en plazo | Un fallo de comunicación honesto es indistinguible (coste para los honestos); para una petición privada, disponibilidad de la entrada |
| 1.5 | Conoce o elige de antemano el muestreo | ab. hoy: cerrado solo bajo el supuesto 2, y las fuentes no están elegidas (así lo evaluaron los trabajos de ChatGPT; los críticos Claude y ChatGPT coinciden) | cond.; **no** con la elección por la última fuente (N13) | igual | igual | Valores públicos del faro y del bloque; la colusión del umbral del faro o la retención del bloque no se ven por ellos | Elegir las fuentes; ronda del faro estrictamente después de la aceptación final del bloque; anotar la confianza en terceros como supuesto |
| 1.6 | Doble pago o tarea ajena | lim.: el número es único, pero el registro solo rechaza una fila con una tarea ajena por objeción; si el ejecutor está apagado toda la ventana, la fila madura. Lo confirmaron los tres críticos | **no**: pago de `R` a una clave ajena | igual | **no** | La asignación es computable si la lista de admitidos al sorteo está en el registro | El registro comprueba por sí mismo la asignación al aceptar la fila (barato) |
| 1.7 | Se asigna tareas a sí mismo, inventa trabajo | ab.: al ejecutor lo elige el sorteo (esa parte está cerrada), pero no se ha adoptado la regla de aprobación del plan de entrenamiento (ROADMAP, «Lo que no está resuelto», punto 5); la repetición de contenido da varios pagos (N22). Crítico DeepSeek: «cerrado para un plan fijo, abierto para el plan» | **no** | igual | **no** | El nodo comprueba que la tarea está en el plan; el derecho a la emisión y la no repetición, no | Regla del plan en el núcleo inmutable; emisión solo por un lugar permitido del plan; abono único por contenido |
| 1.8 | Toma las tareas ventajosas y abandona el resto | lim.: lo abandonado pasa a otro | sí con costes iguales; discutible si una ganancia pequeña por selección con costes desiguales incumple D1 | lim.; la selección tras el sorteo es imposible | igual | Asignación y plazo en el registro | Coste igual de las tareas; la cuota disminuye tras las abandonadas |
| 1.9 | Resultado calculado en equipo ajeno | no es ataque (D2) | n/a | no es ataque | n/a | — | Distinguirlo de la entrega repetida del mismo resultado (N1, N22) |
| 1.10 | Alarga la disputa o calla | lim.: el silencio es derrota; con `H` pequeña, la diferencia de gastos de la disputa la paga la red | n/a; discutible con una disputa cara (N3) | lim.; `H` suele estar cerca de cero | igual | Temporizadores de los pasos en el registro | Plazos de los pasos; presupuesto del precio de la disputa |
| 1.11 | Falsificaciones antes de la parada de la red | cerr.: la ventana no avanza mientras la red está parada; el umbral no está elegido | cond. | igual | cond. | Tiempo de la ventana por paquetes con una proporción de peso no inferior al umbral | Elegir el umbral (3.10); guardar las filas durante la parada (N7) |
| 1.12 | Oculta la falsificación y no entrega los datos | ab. para datos grandes: el registro no ve «lo dio o no lo dio»; para el entrenamiento hace falta el estado del paso anterior | **no** | ab.; no pagado, pero ya usado | **no** | Para datos pequeños, publicación en la cadena de bloques; para grandes, no | Disponibilidad de los datos antes del sorteo; «sin datos en plazo, incorrecto» también para el estado de entrenamiento (N2, M3) |

### 3.3. Verificador

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 2.1 | Confirma sin recalcular | Discutible. cerr. para un verificador fuera de la coalición (cuatro trabajos, los críticos Claude y DeepSeek); ab. según la evaluación de los trabajos de ChatGPT y del crítico ChatGPT: dentro de la coalición, los mismos datos son compatibles con la ausencia de recálculo | sí para uno no vinculado; dentro de la coalición, 2.2 | igual | igual | Su propio estado en un punto aleatorio y la prueba de inclusión; el origen del cálculo no es verificable | No publicar estados intermedios por la disponibilidad (N11) |
| 2.2 | Pago de la verificación de su grupo sin recálculo | lim.: alrededor del 0,3% del ingreso con el 10% del peso [cálculo: 0,01·3·0,1] | **no** con cualquier `q > 0`: ahorro del recálculo (cinco trabajos, los tres críticos) | lim., si la verificación en B se paga como en A (tarifa no definida) | **no** con el mismo pago | No: el recálculo y la copia dan los mismos datos | No pagar por la repetición; el arreglo «pagar con la recompensa de la tarea verificada» no anula la ganancia (sección 4.5) |
| 2.3 | Colusión del ejecutor con todos los verificadores | def. hasta `q_eff ≈ 0,909` (marcha: 0,875) | **no** | def. por la fórmula de la sección 1.8 | **no** | No, salvo recálculo completo; petición privada, solo el usuario | Verificación que no dependa de la proporción de colusión (etapa 4), o un debilitamiento explícito de D1 (pregunta 2) |
| 2.4 | Soborno o presión tras el muestreo | ab.: el verificador de una petición se revela al ejecutor; soborno mediante contrato (N4); con M1, el sobornado no arriesga. La rebaja la confirmaron los tres críticos | **no** | igual; con `H = 0` el soborno es más barato | **no** | No | Petición a los verificadores sin contacto con el ejecutor; consecuencias de la no revelación (M1) |
| 2.5 | Un grupo responde primero y ocupa las plazas | cerr.: se cuentan todas las respuestas en plazo; el plazo no está elegido | cond. | igual | cond. | Tiempo de las respuestas en el registro | Plazo de la ronda no más corto que el ciclo diario; tener en cuenta el crecimiento de `q_eff` |
| 2.6 | Un registro con peso y sin `H` confirma falsificaciones | cerr.: admisión solo con `H_v ≥ B`; efecto secundario, crecimiento de `q_eff` (N5) | sí | ab.: no hay regla de admisión en B | **no**: la coalición recibe `R/p` sin riesgo | `H` del verificador en el registro (en A) | Una medida propia de responsabilidad del verificador en B |
| 2.7 | Acusa falsamente a un ejecutor honesto | cerr. bajo el supuesto 4 (no construido) | cond. | igual | cond. | Recálculo del paso en el registro | Máquina de referencia del modelo completo; devolución por tiempo de espera: 2.8, 4.2 |
| 2.8 | Acusa a un ejecutor apagado | lim.: para una petición privada no hay defensor, se quema la `H` del honesto | **no** para la combinación «usuario + verificadores» (devolución de una respuesta correcta recibida); n/a para el daño puro | igual | igual | Para el entrenamiento protegerá cualquiera con la entrada abierta; para una petición privada no hay datos | Copia de la petición disponible para el defensor sin revelarla |
| 2.9 | Flujo de disputas falsas | lim. por el precio de la `H` del atacante | n/a (verificación barata) | lim.; en B la `H` suele ser 0 | n/a | Resultado de la disputa en el registro | Resolver la contradicción N23 |
| 2.10 | Interceptación del hallazgo ajeno | ab.: el orden no está elaborado | **no**: parte de lo anulado para el interceptador | ab.; la prima en B no está definida | ? | Objeción oculta `hash(hallazgo ‖ clave)` con marca del bloque | Entrega oculta con revelación y vinculación a la clave (barato); certifica la prioridad de la fijación, no el momento de la apertura |
| 2.11 | Denuncia su propia falsificación por una parte de la anulación | cerr. para la tarea elegida; una autodenuncia separada es deficitaria | sí | la prima en B no está definida | ? | El registro no paga al hallador antes de terminar la verificación asignada | Regla de la prima para B |
| 2.12 | Rechaza verificaciones | lim.: el sorteo pasa a la ronda siguiente | n/a; discutible: con `G > B`, al disconforme le conviene callar (N3), depende del presupuesto `G` | igual | igual | — | Presupuesto `G`; consecuencias de la ausencia sin depósitos |

### 3.4. Conjunto de registros, peso y votaciones

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 3.1 | Miles de cuentas | cerr. para el peso y los votos; lim. en conjunto: los pagos de aprendiz, el reparto y las asignaciones crecen con el número de claves (críticos Claude y DeepSeek). Crítico ChatGPT: el número de intentos pagados depende de las plazas asignadas, no de los registros | **no** | ab.: cada clave con asignación es un billete con esperanza `R·q^k` | **no** | No hay datos que vinculen las claves | Entrada sin pagos hasta la verificación independiente; en B, admisión por `H` (N16) |
| 3.2 | Infla el peso con falsificaciones o peticiones a sí mismo | def. hasta el umbral; las falsificaciones no verificadas que pasan la ventana reciben peso | **no** en el límite | ab.: con `H = 0`, una falsificación elegida da peso casi gratis | **no** | No, salvo recálculo | Peso solo por lo verificado de forma independiente; conciliar «pasó la ventana» (SPEC) y «pasó la verificación» (CURRENT_DESIGN) |
| 3.3 | Alquila potencia y acumula peso honestamente | ab. en una red pequeña: para ¾ del peso, mes y medio con el triple de trabajo que el resto, para el 91%, diez veces más [cálculo SPEC] | n/a (el alquiler está permitido por D2); lleva a 2.3 y 3.7 | igual | n/a | No: el trabajo es honesto | Verificación que no dependa de la proporción de peso; núcleo inmutable (D4) |
| 3.4 | Tareas grandes que solo él verificará | cerr. por la regla de tamaño pequeño igual; la captura de tareas pequeñas de un modelo raro es la fila 3.5 | sí | igual | sí | Tamaño de la tarea: regla del núcleo | — |
| 3.5 | Captura de las verificaciones de un modelo raro | ab.: `q_eff ≈ 1` es alcanzable | **no** | igual | **no** | No | No pagar por un modelo sin un umbral de verificadores independientes en otro equipo |
| 3.6 | Registros vacíos en las plazas de aprendiz | ab.: cola de novatos honestos; pago del aprendiz por una copia (2.2) | **no** mediante la copia; n/a para la cola | ab.; el presupuesto de plazas se lo lleva quien tiene más claves | **no** | No | No pagar la reverificación de aprendiz; plazo de liberación de la plaza (N28) |
| 3.7 | ¾ del peso cambian las reglas a su favor | Discutible. Críticos Claude y DeepSeek: ab. — D4 protege el núcleo de verificación, pero no la emisión, la tarifa, la tasa, el freno y el catálogo. Crítico ChatGPT: lim. — D4 tiene prioridad sobre la SPEC antigua, el beneficio exige un cambio concreto | **no** (captura de la emisión), discutible | igual | igual | Huella del núcleo: el nodo rechaza una versión que cambia el núcleo | Enumerar la composición del núcleo (pregunta 5) |
| 3.8 | Bloquea decisiones (½, el modelo; ¼, las reglas) | lim.: reversible, pero el error no se corrige | n/a (supervivencia) | igual | n/a | — | — |
| 3.9 | Compra votos | lim.: hacen falta ¾ de todo el peso; el soborno lo ejecuta un contrato | como 3.7: **no**, si la mayoría cambia la emisión; discutible | igual | igual | No | Como 3.7 |
| 3.10 | Deja de entregar paquetes para congelar la ventana | ab.: con un umbral alto, congelación de los pagos; con uno bajo, la coalición mantiene la ventana con sus paquetes y las falsificaciones maduran (N14) | **no** (rama del umbral bajo) | igual; la falsificación elegida recibe `R/p` | **no** | Tiempo y proporciones de peso de los paquetes | Umbral con demostración de ambos límites; distinguir el peso activo de la red y la composición de los verificadores |

### 3.5. Usuario

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 4.1 | No paga la respuesta, gasta los créditos dos veces | lim. por una parte de la respuesta; el doble gasto está cerrado | **no**: la parte no pagada es una fuga positiva (pregunta 3) | igual | **no** | Fijación de los créditos; el registro no ve la transmisión de la parte | Un intercambio honesto sin parte de confianza es imposible en general: reducir la parte o aceptarlo como supuesto |
| 4.2 | Disputa una respuesta correcta por el reembolso | ab. por dos vías: la disputa se cierra si los verificadores del sorteo coinciden (N17); devolución por tiempo de espera con el ejecutor apagado. Los tres críticos consideraron exagerada la evaluación «cerrado» de tres trabajos | **no** | igual | **no** | Recálculo en el registro, solo si la disputa ha llegado a él | Derecho a llevar la disputa hasta el recálculo; regla del tiempo de espera; defensor con datos |
| 4.3 | El usuario y el ejecutor emiten créditos con peticiones | cerr.: las peticiones no emiten créditos | sí | cerr., si `R/p` se paga solo con los pagos de los usuarios; la fuente no está anotada | cond. | Regla de emisión | Anotar la fuente de `R/p` en B (pregunta 12) |
| 4.4 | Inunda la red de peticiones | lim. por la cartera | n/a | igual | n/a | — | — |
| 4.5 | Copia el modelo y presta servicio fuera de la red | ab. en la cuenta de SPEC (forma parte de 16) | n/a: riesgo para la demanda | igual | n/a | — | — |

### 3.6. Registro, programa y comunicación

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 5.1 | Reescribe la historia o las cuentas | cerr. bajo el supuesto 1 | cond. | igual | cond. | Bloques finales a través de puntos independientes | Verificación formal del programa del registro |
| 5.2 | El nodo de registro no deja pasar o falsea registros | lim. para la censura (su propio registro cuesta monedas de la cadena de bloques, inaccesible para una cuenta vacía); ab. para una fila con precio o destinatario incorrectos sin objeción (críticos DeepSeek y ChatGPT) | **no** | igual | **no** | El precio y el destinatario son verificables, pero hoy solo por objeción | Verificación de la fila al aceptarla; devolución de registros sin emisión (N12) |
| 5.3 | Programa falso para el novato | ab.: la dirección y la referencia vienen de la misma fuente | n/a (autenticidad) | igual | n/a | No antes de la primera instalación | Fuentes independientes de la dirección y de la huella; compilación reproducible |
| 5.4 | Actualización maliciosa | lim.: D4 permite rechazar una huella ajena del núcleo; no hay compilación reproducible del programa del nodo, por lo que el «cerrado» de SPEC no se sostiene; para el resto del programa, ab. | n/a | igual | n/a | Huella en el registro sin vínculo verificable con el código fuente | Compilación reproducible; la coincidencia con el texto aprobado no demuestra su seguridad |
| 5.5 | Pago de un almacenamiento o una entrega inexistentes a sí mismo | cerr.: por el almacenamiento no se emite nada | sí | igual | sí | Regla de emisión | — |
| 5.6 | Cobra el pago y no entrega los datos | lim. por una parte | **no**: fuga de una parte en el lado del receptor sin recibo (pregunta 3) | igual | **no** | Huella de la parte; el recibo confirma el pago, no la entrega | Como 4.1 |
| 5.7 | Bloquea todas las vías de encuentro | ab. si se bloquean todas las vías | n/a (distribución) | igual | n/a | — | — |
| 5.8 | Rodea el nodo de un estado falso | lim. por la confianza en dos de los tres proveedores; con su colusión, ab. (N29) | cond. | igual | cond. | Bloque final a través de puntos independientes | Cliente ligero con verificación del consenso |
| 5.9 | Divide la red por dos pagos | cerr.: un solo registro | sí | igual | sí | Número de la tarea en un solo registro | División de reglas: N15 |
| 5.10 | Roba una clave de trabajo | lim.: la clave no gasta los créditos de la cartera | Discutible: n/a (daño a la víctima) o **no**: las claves robadas confirman falsificaciones a costa de la `H` ajena (N9, apoyado por el crítico Claude) | igual | igual | La firma no muestra al operador | Revocación de la clave; almacenamiento por hardware |
| 5.11 | Agota el reparto gratuito | ab.: no se ha comprobado si alcanza para los novatos | n/a (denegación de servicio); discutible si el beneficio se define «para el primero que llega» | igual | igual | Un propietario nuevo es indistinguible de una clave nueva del anterior | Reparto solo por tareas ya asignadas |

### 3.7. Modelo y entrenamiento

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 6.1 | Un saboteador entrega contribuciones incorrectas | lim.: alrededor de `x/3` de las contribuciones con una proporción de trabajo `x` [cálculo SPEC]; con colusión total, no demostrado; la contribución actúa de inmediato (N21) | n/a por créditos; no (ef.) | ab.: la falsificación no elegida es gratuita, el límite `x/3` no actúa (críticos Claude y ChatGPT) | **no** | No, salvo recálculo | Promover solo contribuciones verificadas (coste: retraso y memoria) |
| 6.2 | Comportamiento oculto | ab.: el examen detecta el empeoramiento, no la puerta trasera | no (ef.) | igual | no (ef.) | No; la puerta trasera es posible incluso con un paso correcto | Tarea de investigación |
| 6.3 | Conjunto de datos malicioso o licencia ajena | ab.: un cálculo correcto sobre datos maliciosos no se corrige | n/a; no (ef.) | igual | igual | No: el hash y la inscripción son iguales en el titular de los derechos y en un tercero | Limitar el catálogo a fuentes verificables |
| 6.4 | Ajuste al examen | lim.: las tareas se eligen tras la fijación | no (ef.) dentro de lo no medible | igual | igual | Momento de elección de las tareas | — |
| 6.5 | Falsificación de los resultados del examen | def. hasta el umbral 2.3; el examen se verifica siempre, sin lotería | **no** con `q` alto | como en A; la fórmula `R·q^k` no es aplicable al examen (sección 4.5) | **no** | El examen es pequeño y abierto: cada nodo puede recalcularlo por sí mismo | Recálculo del examen por cada nodo (lo recomendó el crítico DeepSeek; crítico ChatGPT: el coste y la obligatoriedad no están establecidos) |
| 6.6 | Captura de la votación sobre el plan | lim.: propiedad del esquema | n/a; **no** en combinación con 1.7 | igual | igual | No | Véase 1.7 |

### 3.8. Confidencialidad

| N.º | En breve | A | D1 en A | B | D1 en B | Datos para el rechazo en caso de colusión | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|---|
| 7.1 | El dueño del dispositivo lee las peticiones | ab. en modo normal | n/a; no (ef.): privacidad incumplida | igual | igual | No | Modo protegido a costa de confiar en el fabricante (N25) |
| 7.2 | Recogida masiva de peticiones ajenas | lim. por la proporción de asignaciones y plazas de verificación | n/a; no (ef.) | igual | igual | — | — |
| 7.3 | Vinculación de las peticiones del usuario | ab.: el seudónimo y las direcciones en el retransmisor | n/a | igual | n/a | — | Pago no vinculable |
| 7.4 | Lectura de la petición mediante la verificación o la disputa | ab.: alrededor del 1% de las peticiones las ven otros tres dispositivos; una disputa falsa publica un fragmento | n/a; no (ef.) | igual; la proporción `p` no limita la revelación: la disputa la abre el usuario | igual | — | Disputa sin revelación (prueba de conocimiento cero del paso) |

### 3.9. Nuevos ataques hallados por el consejo

Los duplicados de distintos trabajos están unificados. «Trabajos»: cuántos de los seis trabajos de la ronda 1 destacaron el ataque;
«Críticas»: la conclusión de la ronda 2. Los números N1… son propios de este documento y no coinciden con los números
locales de los trabajos. No hay nuevos ataques refutados; donde la justificación está refutada, se dice.

| N.º | Ataque | Trabajos | Críticas | A · D1 | B · D1 | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|---|
| N1 | **Un cálculo, muchos pagos.** Una clave de la coalición recalcula una vez una tarea ajena (incluso honesta) y reparte el paso a todas sus claves que hayan salido verificadoras o aprendices para esa tarea. Generaliza 2.2: no hace falta colusión con el ejecutor | 1 | Lo confirmaron los tres; la ventaja crece con el número de plazas pagadas asignadas, no con el de claves | ab. · **no** | ab. · **no** | No hay datos. Ningún pago debe depender de la repetición de un trabajo ya hecho |
| N2 | **Inanición de datos de los verificadores honestos.** El verificador toma la petición del ejecutor y se revela; el ejecutor de la coalición entrega la petición solo a los suyos; el honesto «no la recibió» no responde y no pierde nada; las rondas siguen hasta reunir tres respuestas de la coalición | 1 (parcialmente también 3) | Correcto con la salvedad: hacen falta alrededor de `3/(λ·q)` rondas diarias — unos 15 días con `q = 5%`, `λ ≈ 4`, unos 75 días con `q = 1%` [cálculo], y el ataque se nota en el registro. El mecanismo de «publicación de una copia cifrada» está nombrado en SPEC, pero no definido. Para el entrenamiento, solo con una única copia de la entrada | ab. · **no** para peticiones | ab. · **no** | El registro no ve la transmisión. Disponibilidad de las entradas antes del sorteo; para una petición privada no hay solución; véase M3 |
| N3 | **Disputa más cara que la apuesta.** El juego de la disputa en el piloto: 93 transacciones, 5,8–6,3 millones de gas: unos 18 $ con 1 gwei y 3000 $ por ETH, unos 360 $ con 20 gwei [cálculo; los precios son supuestos]. La repetición de la fila: 14,1 millones de gas, otro prototipo, no se pueden sumar | 1 (de forma próxima también 3) | Correcto como dilema, las cifras son condicionales: o la parte derecha asume `G − B` y el honesto disconforme calla; o la red compensa `G` (así se lee 1.10 de SPEC) y el saboteador obliga a la red a pagar `G` por cada falsificación detectada | ab. · **no** | ab. · **no** | Presupuesto `G` para la cadena elegida; las tareas en las que un error exige disputa, solo con `H ≥ G` |
| N4 | **Soborno «P+ε»:** el contrato paga ε al verificador por confirmar y promete devolver `H_v` si lo detectan. Variante de 2.4 | 1 | Crítico DeepSeek: sustancial; crítico ChatGPT: la ejecutabilidad y el equilibrio no están demostrados | ab. · **no** | ab. · **no** | Verificación donde el acuerdo no decide nada; véase M1 |
| N5 | **Crecimiento de `q_eff` por la admisión `H_v ≥ B`:** el 42,1% del peso global da el 88,9% entre los admitidos (sección 1.7) | 2 | Confirmado; solo para tareas con `B = 399R` | lim. · **no** con captura | ab. (2.6) | Calcular los límites por `q_eff`; calcular el compromiso entre el tamaño de la anulación y la amplitud de la ronda |
| N6 | **El peso desaparece tras 30 días naturales de parada:** la ventana se detiene, el peso se cuenta «por 30 días»; el primer grupo que vuelve recibe todo el peso | 1 | Correcto según la letra de SPEC, pero condicional: no se dice si es tiempo natural o activo; con peso nulo de todos, el sorteo no está definido | ab. · **no** | ab. · **no** | Contar el peso por el tiempo activo de la red (barato) y definir el abono inicial |
| N7 | **Las filas de los paquetes viven unos 18 días, la ventana puede durar más:** tras la parada queda una raíz sin filas y no hay con qué disputar | 3 | Lo confirmaron todos | ab. · ? | ab. · ? | Guardar las filas y las bases de las transiciones durante todo el plazo de verificación y disputa; sin datos, el asiento en disputa espera |
| N8 | **Un modelo propio en el catálogo da `q = 1`:** un modelo que solo descarga el equipo de la coalición | 1 | Crítico ChatGPT: es la combinación de 1.7, 3.5 y 6.6; que una proporción pequeña de peso lleve un modelo al catálogo no está demostrado | ab. · **no** | ab. · **no** | No pagar por un modelo sin una ronda mínima de verificadores en otro equipo |
| N9 | **Dispositivos ajenos como peso gratuito de verificadores:** las claves de trabajo robadas confirman falsificaciones y se quema la `H` de las víctimas. Ampliación de 5.10 | 1 | Confirmado; el aumento de `q` va por el peso de las claves capturadas, no por el número de dispositivos | ab. · **no** | ab. · **no** | Almacenamiento de la clave por hardware; contabilizar el compromiso en la `q` admisible |
| N10 | **La entrega instantánea de falsificaciones aumenta el flujo de asignaciones** (B) | 1 | Condicional: el crecimiento de 10 a 100 veces no se deduce de las reglas de SPEC | lim. · sí | ab. · **no** | Ritmo de asignaciones solo por trabajo verificado |
| N11 | **Disponibilidad frente a 2.1:** publicar estados intermedios por N2 permite confirmar sin recálculo | 1 | Limitación del cambio propuesto, no un ataque autónomo | — | — | Publicar solo las entradas; los intermedios, en la disputa |
| N12 | **Pago por el asiento en el registro por encima de los costes:** devolución de asientos basura o cartel de nodos de registro | 2 | La regla de devolución no está definida en SPEC; el ingreso normal de un intermediario no incumple D1 | ab. · cond. | ab. · cond. | Devolver solo los asientos con resultados aceptados y no por encima de la comisión real |
| N13 | **Elección por la última fuente de aleatoriedad:** si la ronda del faro se conoce antes del bloque decisivo, su productor elige entre dos valores; en A `p → p²`, ganancia de unos +0,96R por falsificación [cálculo]. Crítico Claude: con un calendario de productores conocido de antemano, la coalición entrega paquetes para sus bloques | 4 | Lo confirmaron todos; las cifras solo con un orden incorrecto de las fuentes | ab. · **no** con orden incorrecto | igual | Ronda del faro estrictamente después de la aceptación final del bloque |
| N14 | **La ventana avanza sin mayoría:** una coalición del 40% con la desconexión de la mitad de los honestos llega al 40/70 = 57% entre los activos [cálculo]. Variante de 3.10 | 2 | Confirmado como variante de 3.10 | def. · **no** para fugas de tipo B | ab. · **no** | Véase 3.10 |
| N15 | **División de reglas:** las sumas no maduradas maduran en dos ramas | 1 | Condicional: la duplicación de una obligación no está demostrada | ab. · ? | ab. · ? | Contrato aparte con separación de saldos |
| N16 | **En B la contención está vinculada a la clave, pero el acceso a las tareas no:** las falsificaciones desde una clave vacía aparte dan `R·q^k` sin pérdidas. Raíz común de 1.1-B, 1.2-B, 1.3-B, 3.1-B | 2 + crítico Claude | Dos trabajos justificaron el agujero con que un participante normal de B tiene `H = 0` en el 23,5–54,7% de las ventanas; este argumento está refutado (sección 4.5). La forma correcta la dio el crítico Claude | — | ab. · **no** | Admisión a los billetes con `H` no menor que el pago esperado por falsificación; entonces B pierde la proporción de verificación baja constante (pregunta 8) |
| N17 | **La disputa del usuario la resuelve el muestreo, no la aritmética:** la disputa se cierra si los verificadores del sorteo coinciden con el ejecutor | 1 | Lo confirmaron los críticos Claude y DeepSeek; crítico ChatGPT: correcto, pero 4.2 trata de la pretensión contraria | ab. · **no** | ab. · **no** | Derecho a llevar la disputa hasta el recálculo en el registro |
| N18 | **Falsificaciones → peso → `q`.** Ampliación de 3.2 | 1 | Confirmado; la conclusión económica exige contabilizar los pagos futuros | lim. · **no** en el límite | ab. · **no** | Peso solo por lo verificado de forma independiente |
| N19 | **La basura de claves gratuitas antes de la asignación** sobrecarga los nodos y las colas | 4 | Confirmado; la plaza del novato honesto no está garantizada en ninguna variante. La evaluación «la basura cuesta a la red 3–4,5 de trabajo con costes casi nulos del atacante en A» fue refutada por el crítico Claude | ab. · n/a | ab. · **no** en combinación con billetes gratuitos | Rechazar los mensajes sin asignación antes del procesamiento caro; el camino desde la cuenta vacía es obligatorio |
| N20 | **Divergencia impuesta de las aritméticas** del ejecutor y del árbitro | 2 | Confirmado; la divergencia por sí misma no demuestra ganancia | ab. · ? | ab. · ? | Semántica única y ejecutable de las operaciones y verificación de las implementaciones contra la referencia |
| N21 | **Uso del resultado antes de la verificación:** la respuesta se lee, el paso se toma como paso siguiente y permanece en el linaje del modelo | 5 (+1 en 6.1) | Lo confirmaron todos; el daño es posible incluso con `q = 0`; `1 − p` es la proporción de no elegidos, no de no aplicados | ab. · no (ef.) | ab. · no (ef.) | Verificar el bloque antes de entregarlo; promover solo el descendiente verificado (coste: retraso y memoria) |
| N22 | **Un mismo derecho de emisión con números distintos** (pruebas idénticas, repetición de un paso tras un reinicio) | 3 | Confirmado; dos pedidos legítimos pueden tener la misma salida | ab. · **no** | ab. · **no** | Abono único por el derecho canónico al lugar del plan |
| N23 | **Contradicción de las reglas de disputa desde la cuenta vacía** (ROADMAP lo exige, SPEC no) | 1 | Lo confirmaron los críticos DeepSeek y ChatGPT | ab. · n/a | ab. · n/a | Decisión del propietario (pregunta 4) |
| N24 | **Apropiación de la tarea de un ejecutor apagado:** desarrollo de 1.6 | 2 | Confirmado | véase 1.6 | véase 1.6 | Verificación de la asignación al aceptar la fila |
| N25 | **Colusión con el fabricante del modo protegido** | 1 | Correcto dentro de 7.1 | ab. · n/a | ab. · n/a | Anotar el supuesto de confianza en el fabricante |
| N26 | **Recibos falsos de transmisión de datos** | 1 | No hay ingreso externo: la coalición se paga a sí misma | ab. · n/a | ab. · n/a | No hay indicio de entrega de datos grandes |
| N27 | **No entrega selectiva por el retransmisor** | 1 | Confirmado para la disponibilidad | lim. · n/a | lim. · n/a | Varios retransmisores, rutas de reserva |
| N28 | **El «aprendiz eterno»** ocupa una plaza y no termina la reverificación (respecto a 3.6) | 1 | Confirmado | ab. · n/a | ab. · n/a | Plazo y liberación automática de la plaza |
| N29 | **Colusión de dos de los tres proveedores del punto de control** (respecto a 5.8) | 1 | Confirmado; «más proveedores» no resuelve la colusión de la mayoría requerida | lim. · cond. | lim. · cond. | Cliente ligero con verificación del consenso |
| N30 | **Al usuario se le entrega un bloque distinto del fijado** | 1 | Confirmado | ab. · ? | ab. · ? | Vincular el bloque entregado al compromiso y verificarlo antes de usarlo |
| N31 | **Un error común en el propio núcleo** acepta una transición incorrecta en todos los nodos | 1 | Confirmado; distinto de N20 | ab. · ? | ab. · ? | Especificación independiente de la transición; según D4, la corrección solo es posible pasando a una red nueva |
| N32 | **Reconocimiento de una petición privada corta por su huella pública** | 2 | Confirmado condicionalmente: hash determinista y un conjunto pequeño de textos | ab. · no (ef.) | igual | Compromisos ocultantes con aleatoriedad fresca |

**Hallados solo por los críticos** (no comprobados por los demás participantes):

| N.º | Ataque | Quién | A · D1 | B · D1 | Qué hace falta para cerrarlo |
|---|---|---|---|---|---|
| M1 | **Renuncia gratuita a la revelación.** Los verificadores de la coalición entregan un «confirmo» oculto y lo revelan solo si todas las respuestas entregadas son suyas; si no, callan y no pierden nada. El soborno de un verificador ajeno pasa a no tener riesgo: en lugar del riesgo de `399R`, cero [cálculo]. Condición: si las respuestas ocultas se ven antes de la revelación no está definido en SPEC | crítico Claude | ab. · **no** | ab. · **no** | Consecuencias de la no revelación sin depósitos (pérdida del pago y del peso de la ronda) o ocultación del número y la autoría de las respuestas; el coste para los honestos apagados no está calculado |
| M3 | **Carga mediante el mecanismo de disponibilidad.** Si a «no lo recibí» se responde con la publicación obligatoria de una copia, el verificador de la coalición siempre declara «no lo recibí»; con `q = 10%`, `λ ≈ 4` esto es alrededor del 34% de las tareas elegidas [cálculo] | crítico Claude | ab. · n/a | igual | La declaración de no entrega debe costar al declarante no menos que la publicación provocada (de su `H`) |
| M4 | **Fallo y engaño bajo una misma regla de anulación:** la causa de una misma salida errónea no se puede verificar | crítico ChatGPT | ? | ? | No se presenta una regla justa para ambas partes (pregunta 11) |

(M2 del crítico Claude es N16.)

---

## 4. Conclusión

### 4.1. Cuántos ataques incumplen D1

Recuento por la tabla de las secciones 3.2–3.8 [cálculo por la tabla]. Las filas marcadas «discutible» están incluidas
y se nombran aparte.

| | Variante A | Variante B |
|---|---|---|
| Ganancia económica («**no**»), de 60 filas | 24 (y otras 2 condicionales: 1.5 con un orden incorrecto de las fuentes, 6.6 en combinación con 1.7): 1.1, 1.2, 1.3, 1.6, 1.7, 1.12, 2.2, 2.3, 2.4, 2.8, 2.10, 3.1, 3.2, 3.5, 3.6, 3.7*, 3.9*, 3.10, 4.1, 4.2, 5.2, 5.6, 5.10*, 6.5 | 25: las mismas sin 2.10 (en B «?»), más 2.6 y 6.1 (y las mismas 2 condicionales) |
| Solo ganancia por efecto («no (ef.)») | 7: 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.4 | 6: las mismas sin 6.1 |
| Nuevos ataques con «**no**» económico (N1–N32, M1) | 14 | 16 |

Con asterisco se marcan las filas discutibles (3.7, 3.9, 5.10). Sin ellas quedan 21 en A y 22 en B.
El número de filas no se puede sumar como número de modos independientes de engaño: un mismo esquema se describe a menudo
en varias filas. La conclusión principal no depende del recuento: **D1 en su forma literal no lo cumple
ni la variante A ni la variante B**, y con esto coinciden los seis trabajos y los tres críticos.

**Comparación de A y B.** B tal como está descrita es peor que A con `H` vacías y bajas cuando `0 < q < 0,909`:
una clave vacía recibe `R·q^k` por intento sin pérdidas (N16). Con `q = 0`, B es mejor: una falsificación no elegida
no aporta nada, ni siquiera con la marcha. Con `q ≥ 0,909` pierden ambas. Si se traslada a B
el camino del novato de A (verificación completa de las primeras tareas), la diferencia en claves vacías desaparece
(`q^k R − (1 − q^k)·3R`, como en A [cálculo]), pero B pierde la proporción de verificación baja constante.
Esto es una entrada para la decisión D3 en la etapa 2, no la decisión misma.

### 4.2. Críticos para el lanzamiento de la red con créditos reales

Resumen de las evaluaciones de los trabajos y de los críticos. El inicio cerrado con créditos de aprendizaje no bloquea estos puntos,
salvo la privacidad, la recuperación (N6, N7) y los puntos sin los cuales el piloto no comprueba lo que
debe comprobar (N2, N3).

1. **Colusión por `q_eff`:** 1.1, 1.2, 1.3, 2.3, 3.2, 3.5, 6.5 y N5. En ambas variantes la aceptación
   se apoya en el acuerdo de una muestra de participantes.
2. **Pago de la repetición:** 2.2, 3.6, N1. Incumple D1 con cualquier `q > 0`; no se ha encontrado un arreglo barato.
3. **Claves vacías en B:** N16, 1.1-B, 3.1-B.
4. **Derecho de emisión y destinatario:** 1.7, 1.6, 5.2, N22, y también 3.7 para la emisión fuera del núcleo.
5. **Disponibilidad de los datos:** 1.12, N2, N7.
6. **Disputas:** 4.2 y N17; el precio de la disputa N3, la relacionada con ella 2.12; la contradicción N23; M1.
7. **Uso antes de la verificación:** N21, 6.1, N30 (si el propietario incluye el efecto en D1).
8. **Recuperación:** N6 (peso tras la parada) y N7 (filas de los paquetes).
9. **Entrada y programa:** 5.3, 5.4, N19.
10. **Privacidad:** 7.1, 7.4, N32: incumplen una condición obligatoria con independencia del dinero.

### 4.3. Raíz común

En ambas variantes la aceptación normal del resultado se apoya en el acuerdo de una muestra aleatoria de participantes,
es decir, en firmas que con colusión no demuestran nada. Por eso el límite de la defensa siempre
se expresa mediante la proporción de colusión `q_eff`, y `q_eff` se puede elevar con el alquiler de potencia, la captura de un modelo
raro, la regla de admisión por `H` (N5), la inanición de datos (N2), claves robadas (N9) o
una larga parada (N6). Los datos verificables de forma independiente con colusión total son solo la entrada y el modelo,
con los que el nodo puede recalcular la tarea por sí mismo; ni A ni B lo exigen, y para una petición privada
el nodo tampoco tiene la entrada. D1 solo es alcanzable con una verificación que no dependa de la proporción de colusión
(etapa 4 [ROADMAP](ROADMAP.md)), o con un debilitamiento explícito de D1 hasta «con `q < q*`» por decisión del propietario.

### 4.4. Arreglos baratos confirmados por los críticos

| Arreglo | Cierra | Salvedad |
|---|---|---|
| El registro comprueba por sí mismo la asignación, el precio y el destinatario de la fila al aceptarla, y no por objeción | 1.6, 5.2, N24 | La lista de admitidos al sorteo debe estar en el registro |
| Abono único según el derecho canónico al lugar del plan y la huella del contenido | N22, parte de 1.7 | Dos pedidos legítimos pueden dar la misma salida; el agujero principal de 1.7, la regla del plan, sigue abierto |
| Entrega oculta de la objeción con revelación y vinculación a la clave | 2.10 | Certifica la prioridad de la fijación, no el momento de la apertura |
| Contar el peso y la ventana por el tiempo activo de la red, no por el calendario | N6 | Hace falta una regla de abono inicial tras la parada |
| Ronda del faro estrictamente después de la aceptación final del bloque | 1.5 (parte), N13 | Las fuentes aún no están elegidas |
| Cada nodo recalcula el examen antes de aceptar la versión | 6.5 | Recomendado por un crítico; el coste y la obligatoriedad aún no están establecidos |
| Corregir el resumen de CURRENT_DESIGN: 60 = 18 + 6 + 19 + 16 + 1 | Cotejo 59/60 | — |

### 4.5. Conclusiones refutadas

Los críticos consideraron erróneas estas afirmaciones de los trabajos de la ronda 1; no se han trasladado a la tabla.

| Afirmación | Dónde | Por qué es incorrecta |
|---|---|---|
| Umbral de rentabilidad de la falsificación en B `q^k > H/(H+R)` | un trabajo de DeepSeek | Se ha perdido el factor `p`. Lo correcto es `q^k > pH/(R+pH)`. Con `p = 1%`, `H = 400R`, `q = 0,95`: ganancia `0,857R`, pérdida esperada `0,01·0,143·400R = 0,572R`, resultado +0,285R por falsificación, mientras que con la fórmula incorrecta da pérdida [cálculo]. El error sobreestima la protección casi hasta el máximo (0,999 en lugar de 0,93) |
| El umbral del 90,9% del novato A «es válido bajo el supuesto de que las 3R se han acumulado por colusión» | el mismo trabajo | El umbral no depende de cómo se hayan obtenido las `3R` |
| La falsificación del examen en B da `R·q^k` | ambos trabajos de DeepSeek | El examen se verifica siempre, sin lotería; la fórmula de la lotería no es aplicable |
| El arreglo 2.2 «pagar a los verificadores con la recompensa de la tarea verificada» anula la ganancia | un trabajo de Claude | El que copia sigue ahorrándose el recálculo; frente a la inacción la ganancia también es positiva; el arreglo no afecta a la copia en una tarea honesta ajena (N1). Solo elimina la emisión de créditos por una verificación vacía |
| «En un participante normal de B, `H = 0` en el 23,5–54,7% de las ventanas, y en ese tiempo la falsificación no entraña ningún riesgo» | ambos trabajos de Claude | Las cifras `0,99^60 ≈ 54,7%`, `0,99^144 ≈ 23,5%`, `0,99^432 ≈ 1,3%` son correctas, pero es la proporción de ventanas a posteriori. La `H` se quema en el momento de la detección, incluidas las ganancias llegadas después de la entrega. La conclusión sobre el agujero es correcta por otra razón: por la clave vacía (N16) |
| D1 se comprueba comparando con la mayor de las dos bases | un trabajo de Claude | Omite el caso con ganancia positiva frente a la inacción (ejemplo en la sección 1.5) |
| «La basura cuesta a la red 3–4,5 de trabajo con costes casi nulos del atacante» (variante A) | un trabajo de Claude | En A la clave recibe tareas solo con `H ≥ 3R`, y cada resultado basura quema esas `3R`; no hay amplificación múltiple. La amplificación solo existe en B sin admisión por `H` |
| Estados corregidos en la tabla: 2.6-B «cerrado» (trabajos de DeepSeek y Claude); 1.7 «cerrado / sí», 1.6 y 4.2 «cerrados / sí», 4.1 y 5.6 «D1 sí», 2.2 «no incumple D1» (trabajos de DeepSeek, en parte Claude); 3.4 «no», 2.7 «abierto / no», 5.11 «no» (trabajos de ChatGPT) | distintos | Las justificaciones están en las filas correspondientes de la tabla: no hay regla de admisión en B; la regla del plan está abierta; la verificación de la asignación y la disputa del usuario dan ganancia; D1 prohíbe una fuga limitada; la ganancia en 3.4 y 2.7 está tomada de filas vecinas; en SPEC no hay un beneficio personal |
| 1.3: ganancia 1,034·H₀ en el punto 0,875 | un trabajo de Claude | 1,034·H₀ corresponde al punto 0,880; en 0,875 es 1,00004·H₀ |

Siguen siendo discutibles (no refutadas) las evaluaciones 2.1 «abierto» en ambos trabajos de ChatGPT y 3.7
«limitado»: los críticos discreparon (filas 2.1 y 3.7 de la tabla).

---

## 5. Preguntas al propietario

Decisiones sin las cuales no se puede cerrar la etapa 1. El consejo no las adopta.

1. **¿Entra el efecto en D1?** Un trabajo propuso distinguir D1 económico (solo créditos)
   y D1 por efecto (influencia en la respuesta y el modelo, lectura de la petición, el daño en sí). Las palabras «el defraudador
   no obtiene lo que desea» en su sentido literal incluyen el efecto; entonces el uso del resultado
   antes de la verificación (N21) incumple D1 en ambas variantes con cualquier `q`, y solo se puede cerrar
   verificando antes de la entrega y de la promoción (coste: retraso y memoria).
2. **¿Exigir una verificación que no dependa de la proporción de colusión, o debilitar D1 hasta «con `q < q*`»?**
   Sin una de las dos cosas, D1 es inalcanzable ni en A ni en B.
3. **¿Fuga de una parte en el intercambio** (4.1, 5.6): un intercambio honesto sin parte de confianza en general
   es imposible. ¿Reconocerla como supuesto explícito o considerarla un incumplimiento de D1?
4. **¿Disputa desde la cuenta vacía** (N23): ROADMAP la exige, SPEC no. ¿Con qué limitar entonces el flujo
   de disputas falsas sin depósitos?
5. **¿Composición del núcleo inmutable** (3.7): ¿entran en él la regla de emisión, la tarifa, la tasa de red,
   el freno y el catálogo, o solo la verificación?
6. **¿Regla de aprobación del plan de entrenamiento** (1.7, ROADMAP «Lo que no está resuelto», punto 5): quién y cómo
   autoriza que una tarea emita créditos.
7. **¿Tiempo para el peso y la ventana** (N6): tiempo natural o tiempo activo de la red.
8. **¿Admisión a las tareas en B** (N16): introducir o no en B la dependencia del acceso respecto de `H`, sabiendo que entonces
   B pierde la proporción de verificación baja constante. Esto es una entrada para D3.
9. **¿Precio de la disputa** (N3): qué cadena considerar para el presupuesto `G` y quién asume la diferencia `G − B`:
   la parte derecha o la red.
10. **¿Pagar la verificación repetida y las reverificaciones de aprendiz** (2.2, N1), si la copia no se puede
    distinguir del recálculo?
11. **Fallo honesto del equipo:** ¿anular por él igual que por un engaño?
12. **Fuente del pago `R/p` en B para las peticiones** (4.3): solo de los pagos de los usuarios o con emisión.

---

## 6. Quién hizo qué

El consejo de modelos trabajó con los materiales del proyecto, sin acceso a la red y sin experimentos.

- **Ronda 1, seis trabajos independientes:** dos trabajos de ChatGPT, dos de DeepSeek, dos de
  Claude. Cada uno elaboró un modelo del adversario, el cotejo de las 60 filas, los estados para las variantes A y B,
  los datos para el rechazo y nuevos ataques.
- **Ronda 2, tres críticas:** una de ChatGPT, una de DeepSeek y una de Claude. Cada crítico leyó los seis
  trabajos, cotejó las afirmaciones con los documentos de origen, recalculó las fórmulas a mano e indicó
  las discrepancias y los errores.
- **Síntesis:** este documento lo elaboró Claude a partir de los trabajos y las críticas. Donde los críticos discreparon,
  en la tabla figura «discutible»; no se añadieron evaluaciones nuevas propias en la síntesis.
