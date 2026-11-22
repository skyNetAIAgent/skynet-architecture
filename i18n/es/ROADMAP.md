<!-- translation of docs/ROADMAP.md, source sha256: 4cd77f720933922c55c4d78c3e761ca614215cc0ed8610b0fb2ae2e3fbee22e2 -->

# Hoja de ruta: defensa contra el engaño

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · **Español** · [Français](../fr/ROADMAP.md) · [Deutsch](../de/ROADMAP.md) · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

Estado a 23 de noviembre de 2026. Es un **plan de trabajo, no una promesa de resultado**. La marca `[x]`
significa «hecho, y se puede comprobar en el repositorio o en los registros de la red»; `[ ]` significa
«no hecho». Las cifras con la marca [cálculo] se obtienen por fórmula, no se miden. La hoja de ruta se actualiza
con cada cambio de estado.

## 1. Objetivo y criterios de finalización

**Objetivo de la etapa actual del proyecto:** encontrar una forma de verificar la honestidad que cumpla
a la vez los requisitos obligatorios ([REQUIREMENTS](REQUIREMENTS.md)):

- no se puede engañar a la red: el engaño es inútil o deficitario, también para un novato con la cuenta vacía,
  con colusión y con muchas claves;
- ningún pago por adelantado: ni depósitos, ni aportaciones, ni multas;
- participar es rentable y la verificación de la honestidad es barata. Valores orientativos del trabajo adicional de verificación: alrededor del 5% del trabajo
  para las peticiones al modelo y alrededor del 20% para el entrenamiento (no confirmadas).

**El trabajo se considera terminado cuando existe todo lo siguiente:**

1. **Está escrito qué se garantiza exactamente** (decisión D1): para el resultado de la petición, el paso de
   entrenamiento, el pago y el historial; para la cuenta vacía, un número arbitrario de claves, el abandono y la colusión
   total de los verificadores de la tarea. El requisito admite «el engaño es inútil»; no es obligatorio demostrar
   una pérdida estricta en cada intento.
2. **Para cada ataque de la tabla de ataques está escrita la regla por la que el nodo rechaza una
   declaración falsa y a partir de qué datos lo hace.** Se indican por separado la probabilidad de aceptación
   falsa, el daño a la red y la ganancia neta de la coalición respecto a la inacción y respecto al trabajo honesto.
   Contraejemplo de la regla: casos honesto y falso en los que el nodo ve los mismos datos.
   El muestreo, la probabilidad pequeña de error y «existe un observador honesto» se anotan como supuestos.
3. **Está calculado el coste completo de la verificación** en relación con la misma tarea sin verificación: el trabajo
   del ejecutor y de los verificadores, la memoria, el tráfico, el almacenamiento, la escritura en el registro, las disputas, las repeticiones tras
   los fallos. Se deducen el ingreso neto de un participante con muchos recursos y electricidad cara,
   el recargo de un participante con equipo débil y el precio para un consumidor sin equipo. La escritura
   y la disputa están disponibles desde una cuenta a cero; solo se pueden perder recompensas no maduradas.
4. **Los cálculos son reproducibles:** se adjuntan la versión de las reglas y del núcleo, las entradas, los límites de la
   búsqueda, la salida y el hash; el cálculo se repite en un segundo dispositivo. La repetición confirma el cálculo, pero no la corrección
   del propio modelo: esta se justifica por separado.
5. **Está medido lo que no se puede establecer por razonamiento:** la coincidencia del resultado bit a bit en distintas
   tarjetas gráficas, la velocidad y la calidad del modelo con aritmética entera, el coste de la disputa. Los perfiles, las métricas y los umbrales
   se fijan antes de la medición.
6. **No se incumplen los demás requisitos:** la red funciona sin ningún nodo ni plataforma en particular,
   permite que sus nodos vuelvan a encontrarse tras una parada completa, se puede reconstruir qué justificó cada abono; al dividirse
   la red, el pago en disputa espera a la historia común y la repetición no se paga dos veces.

Un resultado honesto también es un resultado: si para alguna clase de tareas la verificación barata es imposible,
esto se muestra con una demostración que nombra la clase de tareas y los datos del verificador,
no con la ausencia de ideas.

## 2. Dónde estamos ahora

| Qué | Estado | Dónde está escrito |
|---|---|---|
| Por las firmas y las respuestas cortas no se puede establecer qué dispositivo trabajó ni durante cuánto tiempo: un intermediario, una caché y una tarjeta inactiva dan los mismos datos | Establecido por razonamiento | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), «Qué se ha descartado» |
| La red paga por un resultado verificable, no por el recurso | Base del proyecto; la unidad del resultado y la condición de aceptación esperan fijarse (D2) | [CURRENT_DESIGN](CURRENT_DESIGN.md), sección 1 |
| Pago diferido en lugar de depósito: el participante responde solo con la suma en espera | Aceptado | CURRENT_DESIGN, sección 2 |
| Variante A: verificación por muestreo con anulación de las recompensas pendientes si se detecta fraude | Especificación actual | CURRENT_DESIGN, sección 3 |
| Variante B: la red paga solo por las tareas verificadas, `1/p` veces más caras | Propuesta (D3) | CURRENT_DESIGN, sección 3 |
| Coincidencia del resultado bit a bit mediante aritmética entera | Candidato, no medido | OPEN_QUESTIONS, Q2 |
| Disputa dividiendo a la mitad con recálculo de un paso en el registro | Medido para una fila del modelo; no construido para el modelo completo | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Comprobación de la multiplicación de matrices con un vector aleatorio dentro de la disputa | Candidato, solo hay una estimación calculada | CURRENT_DESIGN, sección 3 |
| Núcleo de verificación inmutable que no se puede anular por votación | Propuesta (D4) | CURRENT_DESIGN, sección 8 |

**Lo que se sabe sobre la fuerza de la defensa.**

- Variante A, sin colusión: en la familia recorrida (dos tandas de falsificaciones, 92 millones de estrategias), el abandono
  con falsificaciones no aporta más que el abandono normal [cálculo].
- Variante A, colusión: los primeros puntos de la cuadrícula en los que el abandono con falsificaciones es rentable son la proporción de colusión 87,5%
  (tareas de tamaño arbitrario) y 89,0% (tareas idénticas) con la regla «como máximo un tercio en curso a la vez»,
  80% sin esa regla. El paso de la cuadrícula es 0,002–0,02; otras familias de estrategias no se han recorrido
  [cálculo, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, sin colusión: con la comparación exacta, la falsificación no se paga.
- Variante B, colusión: `q` es la fracción del peso total de los verificadores de ese modelo que corresponde a la coalición. La falsificación
  se paga solo si la tarea es elegida y los `k` verificadores están en colusión. El pago medio
  por una falsificación presentada es `R·q^k` (`R` es el precio de la tarea) y no depende de `p` [cálculo].
  Con `q = 1` es el precio completo. A un novato con la cuenta vacía no hay nada que descontarle.
- No se ha demostrado para ninguna de las dos variantes que, si todos los verificadores se confabulan, no se pague por ningún resultado falso. Esa garantía se obtiene al verificar cada resultado pagado con datos que cualquier nodo puede comprobar por sí mismo. El recálculo completo añade alrededor del 100% del trabajo. Mediciones del piloto: la demostración
  RISC Zero de una fila del modelo tardó 22 min 10 s en construirse; la ejecución de ocho filas en la zkVM fue
  aproximadamente 17 700 veces más lenta de lo normal, sin construir la demostración. Estas mediciones no dan
  un límite inferior general del precio.
- Irregularidad del ingreso en la variante B: con 6000 tareas al mes, verificación de 1 de cada 100 y un coste
  del 95% del precio, la probabilidad de un mes deficitario es del 33,10% [cálculo, FIRST_RUN].
- La primera ejecución de los cálculos (702 porciones) se hizo en un ordenador. Un segundo dispositivo recalculó,
  hasta el 22 de noviembre, 40 porciones; todas coincidieron. Sus registros están firmados con la clave `46000d30…` y disponibles
  en el nodo completo. Las 662 porciones restantes no están confirmadas de forma independiente.

**Lo que no está resuelto.**

1. Novato con la cuenta vacía en colusión (variante B): ganancia media de `R·q^k` por intento, sin pérdidas.
2. «Mucho tiempo honesto, luego un gran engaño y se marcha»: la pérdida está limitada por la suma en espera, la ganancia
   crece con el número de falsificaciones. Los arreglos para la variante B están propuestos, no calculados.
3. El flujo de basura desde claves gratuitas. La clave no cuesta nada; el pago mediante trabajo del procesador pone
   a los dispositivos débiles en peor situación.
4. Resultado usado antes de la verificación. La respuesta ya ha sido leída por el usuario, el paso ya ha entrado
   en el entrenamiento; la limitación de los pagos no lo corrige. En la variante B esto se aplica también a las tareas
   no elegidas.
5. Tareas de entrenamiento pagadas mediante la emisión de créditos: quién las aprueba y con qué regla.
   Una tarea bien ejecutada pero autoasignada no debe otorgar créditos.
6. Modelo raro: el círculo de verificadores es pequeño y su `q` puede estar cerca de uno.
7. Disponibilidad de los datos y disputa por una petición privada sin revelar la petición.
8. La coincidencia bit a bit y la velocidad del modelo con aritmética entera no están medidas.
9. Un saboteador que no necesita beneficio y el envenenamiento de los datos de entrenamiento. La defensa económica
   no actúa sobre ellos.

## 3. Decisiones que esperan aprobación

Mientras la decisión no esté tomada, los puntos del plan que dependen de ella siguen siendo propuestas.

| N.º | Pregunta | Qué depende de esta decisión |
|---|---|---|
| D1 | Qué se acepta como garantía. ¿Basta con «el engaño no aporta nada, lo gastado se pierde, el trabajo honesto es más rentable»? ¿Se admite una fuga limitada con colusión, o el pago falso debe quedar excluido también con colusión total de los verificadores? | Criterios de finalización, etapas 3 y 4 |
| D2 | Fijar el pago por un resultado verificable en lugar de por la potencia y el tiempo; definir la unidad del resultado y la condición de aceptación | Etapas 2–6 |
| D3 | Variante A, variante B o ninguna. Se decide tras la comparación con los mismos ataques y el mismo precio (etapa 2) | Etapas 3 y 6 |
| D4 | El núcleo de verificación inmutable y qué contiene | Etapa 6 |
| D5 | El primer experimento: Qwen3.5-4B con aritmética entera en dos tarjetas gráficas distintas (si los resultados coinciden bit a bit, a qué velocidad funciona y qué calidad ofrece) | Etapa 5 |

## 4. Etapas y lista de comprobación

Las etapas 1–4 avanzan a la vez: son cálculos y razonamientos. La búsqueda de algoritmos nuevos (etapa 4)
no espera a las demás. La etapa 5 exige la decisión D5. La etapa 6 reúne los resultados.

### Etapa 0. Herramientas de colaboración

- [x] Repositorio público, base inmutable en nueve idiomas (etiqueta `core-v1`).
- [x] Programa agente para Windows, Linux y macOS: tareas y actualizaciones firmadas,
      comprobaciones automáticas en los tres sistemas (versión 0.2.0).
- [x] Resultados y [tablero de tareas](BOARD.md) sin cuenta.
- [x] Primer nodo completo que guarda el historial de registros.
- [x] Primera tarea de investigación «Defensa contra los defraudadores» en el tablero, en nueve idiomas.
- [ ] Informe para una tarea del tablero de un participante no vinculado a los mantenedores, que indique quién lo obtuvo
      y cómo. Ahora todos los registros de la red están hechos por dispositivos de los mantenedores. Claves
      distintas no demuestran propietarios distintos.
- [ ] Confirmación independiente de las 702 porciones de la primera lista de tareas (ahora 40).
- [ ] Actualización del agente de una versión publicada a la siguiente, observada en una
      instalación real (ahora solo se ha comprobado con pruebas).
- [ ] Aplicación Android: comprobación en un teléfono real, publicación de resultados sin token.
- [ ] Instalación sin Python preinstalado: un solo archivo para Windows, macOS y Linux.
- [ ] Instrucciones para el asistente de IA: cómo tomar una tarea del tablero, entregar un informe y comprobar el informe de otro.
- [ ] Ciclo automático para los asistentes de IA: el agente recoge por sí mismo las tareas nuevas del tablero y las entrega
      al modelo local del participante. Ahora esto se hace con comandos manuales.
- [ ] Segundo y tercer nodos completos de propietarios distintos.
- [ ] Corregir la línea obsoleta en BOARD («el agente 0.2.0 aún no está publicado»).

### Etapa 1. Planteamiento exacto

- [ ] Las decisiones D1 y D2 están tomadas y escritas.
- [ ] Para una petición abierta y un paso de entrenamiento están escritos: la regla de aceptación, la aritmética,
      la base de la emisión de créditos, el momento de fijación del resultado respecto al sorteo y el momento en que
      el resultado se puede usar.
- [ ] Modelo del adversario en un solo documento: colusión, muchas claves, abandono, alquiler de potencia; qué
      se considera ganancia del defraudador y qué se considera daño a la red.
- [ ] La tabla de ataques analizados está publicada en el repositorio en nueve idiomas con el estado de cada
      ataque para las variantes A y B. Antes de publicar, comprobar las filas: en el resumen de CURRENT_DESIGN la suma
      de las categorías 18 + 6 + 19 + 16 = 59 frente a los 60 declarados.
- [ ] Para cada ataque está escrito con qué datos verificables de forma independiente rechazará el nodo una
      declaración falsa en caso de colusión del ejecutor y de los verificadores.

Terminado cuando: cualquier participante puede nombrar a partir de la tabla un ataque que sigue sin mitigarse y comprobar que es así.

### Etapa 2. Economía: cálculos que realizan los miniagentes

Cada tarea es un modelo exacto con una cuadrícula finita de entradas; las probabilidades y las sumas se calculan con
fracciones exactas y el hash de cada porción se coteja entre dispositivos.

- [x] Variante A, abandono con falsificaciones: primera ejecución.
- [x] Variante B, irregularidad del ingreso con proporción de verificación constante: primera ejecución.
- [ ] Confirmación independiente de ambos cálculos (véase la etapa 0).
- [ ] **Campaña de salida en la variante B.** Entradas: la suma en espera `H₀`, el precio `R`, la proporción de verificación
      `p`, la colusión `q` y `k`, el tope de tareas simultáneas `C`, el número de tandas `T`. Una falsificación
      descubierta anula todo el saldo pendiente, incluidas las ganancias de la tanda. Hallar el mayor pago esperado
      por encima de `H₀`, también con `H₀ = 0`, `q = 0` y `q = 1`.
- [ ] **Plazas de aprendiz.** Por época se reparten `S` plazas entre `n` claves honestas y `m` claves
      de la coalición. Hallar la fuga esperada en `E` épocas y la proporción de plazas que reciben los novatos
      honestos al crecer `m`.
- [ ] **Lotería con una proporción de verificación ajustada.** Para `N` tareas al mes, tomar el menor `p`
      con el que se paguen en promedio no menos de 60 tareas. Hallar la probabilidad de un mes
      deficitario y de un trimestre deficitario, la probabilidad de un mes sin ningún pago y el número de recálculos para la red.
- [ ] **Certificado del token ganador** (véase la etapa 4): número de operaciones de verificación respecto
      al recálculo completo de la capa de salida en un conjunto dado de entradas.
- [ ] Fórmula del coste completo de la verificación para los tres tipos de participantes; tras la etapa 5 se sustituyen
      en ella las mediciones.
- [ ] Comparación de las variantes A y B con los mismos ataques y el mismo precio, y luego la decisión D3.
      Resultado posible: ambas variantes siguen siendo de investigación.

Terminado cuando: para cada variante existe una tabla «proporción de colusión → mayor ganancia esperada
del defraudador», recalculada en no menos de dos dispositivos independientes.

### Etapa 3. Cerrar los agujeros conocidos

- [ ] **Novato con la cuenta vacía.** Candidato: las primeras tareas del novato son tales que cualquier nodo
      las comprueba exactamente por sí mismo, y solo después se acumulan la recompensa y el peso. Opción de reserva:
      presupuesto común de pagos de aprendiz por época; limita la fuga, pero no la hace cero,
      y la colusión puede ocupar todas las plazas.
- [ ] **«Mucho tiempo honesto, luego un gran engaño».** Candidato: un tope sobre la suma de todas las obligaciones
      abiertas de la clave, contando las mayores ganancias posibles. Es el límite de una tanda,
      no una fuga nula.
- [ ] **Basura de claves gratuitas.** Candidato: el nodo acepta datos solo con números de tarea permitidos,
      limita el tamaño, la cola y el trabajo por época. El canal se puede llenar de todos modos;
      no se ha obtenido un lugar garantizado para el novato honesto con un número arbitrario de claves.
- [ ] **Resultado usado antes de la verificación.** Candidato: comprobar el bloque de respuesta antes de entregarlo;
      mantener el paso de entrenamiento en una rama aparte y promover solo al descendiente verificado. Coste:
      retraso y memoria.
- [ ] Tareas de entrenamiento: regla de aprobación sin un participante con derechos especiales.
- [ ] Modelo raro: umbral derivado de la distribución del peso por debajo del cual la red no paga por el
      modelo.
- [ ] Verificador perezoso y reenvío de un resultado conocido: compromisos ocultantes
      con revelación, abono único según el contenido.
- [ ] Fallo del equipo de un participante honesto: regla que no da ganancia al defraudador.
- [ ] Disponibilidad de los datos y disputa por una petición privada sin revelación.
- [ ] Ventana de disputa al pararse la red, protección frente a una historia obsoleta, división de la red.

Terminado cuando: para cada punto están publicados una construcción con supuestos, un ataque contra ella y el coste,
o un contraejemplo, o el estado «abierto» con su razón.

### Etapa 4. Búsqueda de una garantía independiente de la proporción de colusión

Se busca una verificación que cada nodo realice por sí mismo, de modo que el acuerdo de los verificadores no
decida nada. Las direcciones no están aprobadas. Para cada una hay que indicar las operaciones verificadas, los datos,
la probabilidad de error y el coste de una petición o un paso completos; después, llevarla a una construcción o cerrarla
con un contraejemplo.

- [ ] **Tareas con un criterio exacto de corrección que cuesta poco comprobar.** Ejemplo: para la regresión ridge, el nodo
      comprueba la condición de óptimo en una sola pasada por los datos. Pregunta: qué proporción del trabajo de la red
      cabe en tales tareas. Empezar por esta dirección: garantiza que no se pague por ningún resultado falso.
- [ ] **Comprobación de cada multiplicación de matrices con un vector aleatorio** en lugar del recálculo. El vector
      se elige después de fijar el resultado; la probabilidad de dejar pasar un error no depende de la colusión.
      Es rentable para lotes grandes; al generar un token cada vez no hay ganancia. Las demás
      operaciones (redondeo, activaciones, caché, optimizador) hay que comprobarlas por separado.
- [ ] **Comprobación de la respuesta final en una sola pasada del modelo** con un perfil exacto y la aleatoriedad
      fijada en la tarea. El número de operaciones es del mismo orden que el de la generación; no está establecido si cabe
      en el 5%.
- [ ] **Tablas de sumas parciales exactas para capas inmutables:** el nodo deriva una vez las tablas
      a partir de los pesos y luego obtiene la salida de la capa con lecturas y sumas. Aplicable también a un solo token;
      se topa con el volumen de memoria.
- [ ] **Certificado del token ganador** para un vocabulario grande: el ejecutor transmite la cobertura
      del vocabulario por grupos, el nodo comprueba las cotas superiores y desciende a los tokens sueltos solo
      donde la cota no separa al ganador. En el peor caso se comprueba todo el vocabulario.
- [ ] **Paso de entrenamiento como fórmula exacta de actualización:** los nodos guardan y comprueban no la nueva matriz
      de pesos, sino los multiplicadores de actualización. Derivado solo para una capa lineal con SGD simple.
- [ ] **Disputa abierta a cualquier participante durante la ventana.** Garantía condicional: hace falta al menos un
      observador que haya recibido los datos y haya tenido tiempo de objetar. Quién paga la observación con
      la cuenta vacía no está resuelto. Dejarlo como reserva.
- [ ] **Pago por la mejora medida del modelo** en tareas elegidas después de fijar los pesos.
      Cambia la base del pago y exige una decisión aparte. Sirve para seleccionar versiones del modelo.
- [ ] **Demostraciones de cálculo para el entrenamiento (sumcheck, GKR)** para un paso determinado:
      presupuesto completo con rangos, redondeo y vinculación de la entrada a la tarea.
- [ ] **Límite inferior:** mostrar qué clases de verificaciones no pueden ser infalibles. Comienzo:
      un conjunto fijo de comprobaciones lineales en número menor que el tamaño del resultado siempre deja pasar
      algún error; quedan abiertas la aleatoriedad fresca y las entradas con estructura conocida.
- [ ] Ideas de los participantes y de los asistentes de IA del tablero: cada una pasa el mismo análisis, incluido el caso
      `q = 1`.

Terminado cuando: para cada dirección están publicados una construcción con presupuesto, un contraejemplo o
un límite demostrado. Se considera encontrada la construcción que cumple todos los criterios de la sección 1.

### Etapa 5. Cuestiones que solo se pueden resolver mediante experimentos (exige D5)

- [ ] Qwen3.5-4B con aritmética entera en dos tarjetas gráficas distintas: si coinciden los bits.
- [ ] Su velocidad respecto al perfil normal en las mismas tarjetas.
- [ ] Su calidad respecto al perfil normal en el mismo conjunto de tareas.
- [ ] Planes de medición aparte (fuera de D5): energía de la verificación, entrenamiento con aritmética entera.
- [ ] Coste de la disputa en el registro para el modelo completo. Antes hacen falta la elección de la cadena de bloques, una máquina de referencia
      del modelo completo, la vinculación de la entrada, las longitudes y las rutas de cálculo.

Terminado cuando: cada cifra está medida, las condiciones de la medición están escritas y la medición la repitió un segundo
participante. La coincidencia de bits se refiere solo a las configuraciones probadas.

### Etapa 6. Síntesis y aceptación

- [ ] Decisión D4 sobre el núcleo inmutable, antes de la comprobación final frente a la captura de la mayoría.
- [ ] Actualizar CURRENT_DESIGN y la tabla de ataques según los resultados de las etapas 1–5.
- [ ] Una declaración rastreada sobre papel desde la autorización de la tarea hasta el uso del resultado,
      incluidos el rechazo, la repetición y la división de la red.
- [ ] Revisión abierta de la construcción final: consejo de modelos y tarea en el tablero.
- [ ] Para cada requisito están publicados una demostración, una medición, un contraejemplo o el estado
      «abierto». Comprobación según los seis criterios de la sección 1.

## 5. Cómo avanza el trabajo

1. Un punto de la lista de comprobación se convierte en una tarea: de cálculo (los miniagentes realizan el cálculo, el resultado
   se coteja por coincidencia) o de investigación (se publica en el tablero).
2. Los participantes y sus asistentes de IA entregan informes. Un informe se acepta solo si se puede
   comprobar: mediante recálculo, contraejemplo o referencia a una fuente. El número de claves que están de acuerdo
   no demuestra nada; la decisión del autor de la tarea en el tablero no confirma el cálculo.
3. Según el resultado de la comprobación, la tarea se cierra, se precisa o da lugar a tareas nuevas.
4. El cambio de estado se introduce en esta hoja de ruta y en CURRENT_DESIGN con una sola edición, con fecha.

## 6. Lo que esta hoja de ruta no promete

- Que exista una solución en las condiciones dadas. Es objeto de búsqueda.
- Plazos. El proyecto no tiene ejecutores remunerados; la velocidad depende de los participantes.
- Recompensas por participar en el diseño.
