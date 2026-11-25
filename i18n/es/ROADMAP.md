<!-- translation of docs/ROADMAP.md, source sha256: ad345dc397f2cdc54e07879bb5286338d67fb1d45f5094c5f5e4bc4340588f70 -->

# Hoja de ruta: defensa contra el engaño

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · **Español** · [Français](../fr/ROADMAP.md) · [Deutsch](../de/ROADMAP.md) · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

Estado a 23 de noviembre de 2026 (actualizado tras la publicación de la versión v0.2.2). Es un **plan de trabajo, no una promesa de resultado**. La marca `[x]`
significa «hecho, y se puede comprobar en el repositorio o en los registros de la red»; `[ ]` significa
«no hecho». Las cifras con la marca [cálculo] se obtienen por fórmula, no se miden. La hoja de ruta se actualiza
con cada cambio de estado.

## 1. Objetivo y criterios de finalización

**Objetivo de la etapa actual del proyecto:** encontrar una forma de verificar la honestidad que cumpla
a la vez los requisitos obligatorios ([REQUIREMENTS](REQUIREMENTS.md)):

- no se puede engañar a la red: el engaño es inútil o deficitario, también para un novato con la cuenta vacía,
  con colusión y con muchas claves;
- ningún pago por adelantado: ni depósitos, ni aportaciones, ni multas;
- participar es rentable y la verificación de la honestidad es barata. Valores orientativos del recargo por verificación: alrededor del 5% del trabajo
  para las peticiones al modelo y alrededor del 20% para el entrenamiento (no confirmados).

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
| La red paga por un resultado verificable, no por el recurso | Aceptado (D2); la unidad del resultado y la condición de aceptación aún no están definidas | [CURRENT_DESIGN](CURRENT_DESIGN.md), sección 1 |
| Pago diferido en lugar de depósito: el participante responde solo con la suma en espera | Aceptado | CURRENT_DESIGN, sección 2 |
| Variante A: verificación por muestreo con anulación | Especificación actual | CURRENT_DESIGN, sección 3 |
| Variante B: la red paga solo por las tareas verificadas, `1/p` veces más caras | Candidato principal; la elección tras la comparación (D3) | CURRENT_DESIGN, sección 3 |
| Coincidencia del resultado bit a bit mediante aritmética entera | Medido en entradas cortas: el procesador, la RTX 2060 y la RTX 4070 Laptop dan los mismos bits para el Qwen3.5-4B con aritmética entera (24 de noviembre de 2026); el contexto largo, la velocidad y la calidad aún no están medidos | [EXPERIMENT_D5](EXPERIMENT_D5.md), sección 7 |
| Disputa dividiendo a la mitad con recálculo de un paso en el registro | Medido para una fila del modelo; no construido para el modelo completo | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Comprobación de la multiplicación de matrices con un vector aleatorio dentro de la disputa | Candidato, solo hay una estimación calculada | CURRENT_DESIGN, sección 3 |
| Núcleo de verificación inmutable que no se puede anular por votación | Aceptado (D4) | CURRENT_DESIGN, sección 8 |

**Lo que se sabe sobre la fuerza de la defensa.**

- Variante A, sin colusión: en la familia recorrida (dos tandas de falsificaciones, 92 millones de estrategias), el abandono
  con falsificaciones no aporta más que el abandono normal [cálculo].
- Variante A, colusión: los primeros puntos de la cuadrícula en los que el abandono con falsificaciones es rentable son la proporción de colusión 87,5%
  (tareas de tamaño arbitrario) y 89,0% (tareas idénticas) con la regla «como máximo un tercio en curso a la vez»,
  80% sin esa regla. El paso de la cuadrícula es 0,002–0,02; otras familias de estrategias no se han recorrido
  [cálculo, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, sin colusión: con la comparación exacta, la falsificación no se paga.
- Variante B, colusión: `q` es la proporción del peso de la coalición entre los verificadores de ese modelo. La falsificación
  se paga solo si la tarea es elegida y los `k` verificadores están en colusión. El pago medio
  por una falsificación presentada es `R·q^k` (`R` es el precio de la tarea) y no depende de `p` [cálculo].
  Con `q = 1` es el precio completo. A un novato con la cuenta vacía no hay nada que descontarle.
- El pago falso nulo con colusión total de los verificadores no está demostrado ni para la variante A ni para la
  variante B. Esa garantía la proporciona la verificación de cada resultado pagado con datos que cualquier nodo
  comprueba por sí mismo. El recálculo completo añade alrededor del 100% del trabajo. Mediciones del piloto: la demostración
  RISC Zero de una fila del modelo tardó 22 min 10 s en construirse; la ejecución de ocho filas en la zkVM fue
  aproximadamente 17 700 veces más lenta de lo normal, sin construir la demostración. Estas mediciones no dan
  un límite inferior general del precio.
- Irregularidad del ingreso en la variante B: con 6000 tareas al mes, verificación de 1 de cada 100 y un coste
  del 95% del precio, la probabilidad de un mes deficitario es del 33,10% [cálculo, FIRST_RUN].
- La primera ejecución de los cálculos (702 porciones) se hizo en un ordenador. Para el 23 de noviembre,
  un segundo dispositivo había recalculado las 702 porciones; todas coincidieron. Sus registros están firmados
  con la clave `46000d30…` y disponibles en el nodo completo. Ambos dispositivos pertenecen a los mantenedores,
  por lo que esto todavía no es una confirmación por un participante independiente.

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
8. La coincidencia bit a bit del modelo con aritmética entera solo está confirmada en entradas cortas de tres dispositivos; el contexto largo, la velocidad y la calidad no están medidos.
9. Un saboteador que no necesita beneficio y el envenenamiento de los datos de entrenamiento. La defensa económica
   no actúa sobre ellos.

## 3. Decisiones

Las decisiones D1–D5 se tomaron el 23 de noviembre de 2026 y las D6–D25, el 24 de noviembre de 2026 (por encargo del propietario;
las D18–D25, sobre las cuestiones de la etapa 4, con justificación en [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), sección 6).

| N.º | Pregunta | Decisión |
|---|---|---|
| D1 | Qué se acepta como garantía | **El defraudador no obtiene lo que desea.** No se pueden excluir los intentos de engaño, pero cualquier intento debe ser inútil para quien lo hace: la ganancia esperada de una falsificación no es mayor que cero en comparación con el trabajo honesto y con la inacción, para cualquier coalición, incluidos un novato con la cuenta vacía y cualquier número de claves. El objetivo es que el resultado falso no se pague en absoluto. No se exige una pérdida estricta en cada intento. Una fuga limitada pero positiva (por ejemplo, `R·q^k` para un novato en la variante B) **no satisface** el criterio y sigue siendo un agujero abierto |
| D2 | Base del pago | **Aceptado: solo se paga por un resultado verificable.** El equipo encendido, el tiempo de trabajo y la potencia declarada no son base del pago: una tarjeta gráfica se puede cargar también con algo ajeno |
| D3 | Variante A o B | **La decisión se toma tras la comparación con los mismos ataques y el mismo precio (etapa 2).** El candidato principal es la variante B |
| D4 | Núcleo de verificación inmutable | **Aceptado en forma reforzada.** La verificación se realiza automáticamente, sin participación humana y sin votaciones. Las reglas de verificación no se cambian por votación. Cada nodo ejecuta por sí mismo la verificación según la huella fijada de las reglas, de modo que la sustitución del algoritmo en un nodo o en un proveedor del programa no cambia la decisión de los demás. Abierto: cómo corregir un error en el propio núcleo (solo pasando a una red nueva) y cómo se asegura un participante de que su programa corresponde a la huella publicada (compilación reproducible). La clave de lanzamiento con la que ahora se firman los miniagentes es una herramienta de investigación; en la red objetivo no debe existir |
| D5 | Primer experimento con Qwen3.5-4B con aritmética entera | **Autorizado:** la tarjeta gráfica RTX 2060 en el Linux doméstico del mantenedor, su ordenador y, con consentimiento, los dispositivos de otros participantes mediante miniagentes. Se ejecuta después de la etapa 0 |
| D6 | ¿Entra el daño en D1? | **Sí** (decidido el 24 de noviembre de 2026 por encargo del propietario). «El defraudador no obtiene lo que desea» se refiere no solo a los créditos, sino también al resultado: una respuesta falsa no debe entregarse al usuario como verificada, ni un paso falso debe entrar en el modelo. Por eso el resultado se usa solo tras una verificación que no dependa de la proporción de colusión, o se marca explícitamente como no verificado |
| D7 | Verificación independiente de la proporción de colusión o debilitamiento de D1 | **Se requiere una verificación que no dependa de la proporción de colusión** (24 de noviembre de 2026). D1 no se debilita hasta «mientras los coludidos sean menos de q\*». La etapa 4 pasa a ser la principal |
| D8 | Disputa desde una cuenta vacía | **Solo pueden disputar los verificadores de esta tarea designados por sorteo y el usuario por su propia petición** (24 de noviembre de 2026). Sin depósito; el flujo de disputas está limitado por el número de verificaciones y de peticiones. Los demás comunican la sospecha en el tablero, sin derecho a detener el pago |
| D9 | Quién aprueba el plan de entrenamiento | **Ninguna persona: el plan se deriva con una regla fijada del catálogo abierto y de los resultados del examen** (24 de noviembre de 2026). Sin votaciones. Los créditos se emiten solo por tareas del plan, una vez por contenido de tarea |
| D10 | Fuga de una parte en el intercambio | **Se considera una violación de D1.** El intercambio de créditos y otros valores pasa solo por el registro, con una sola anotación para ambas partes, sin un tercero de confianza fuera del registro |
| D11 | Composición del núcleo inmutable | **La verificación, la regla «solo se paga lo verificado», la regla de emisión de créditos, la disputa y las reglas del registro.** Las tarifas, la comisión de red y el catálogo de modelos cambian solo dentro de los límites fijados en el núcleo |
| D12 | Tiempo para el peso y ventanas de verificación | **Tiempo activo de la red**, no el calendario: mientras la red está parada, el peso no envejece y la ventana de verificación no corre |
| D13 | Acceso a las tareas en la variante B | **Se introduce el camino del novato de la variante A:** el acceso a las tareas depende de la suma en espera de la clave. La elección definitiva entre A y B (D3) es tras la comparación |
| D14 | Coste de la disputa | **Para el presupuesto se toma una red de segundo nivel con el registro más barato.** La diferencia entre el coste de la disputa y la suma que se puede descontar al perdedor la paga la comisión de red de los consumidores, no la emisión de créditos |
| D15 | Verificaciones repetidas y de aprendiz | **El recálculo simple que se puede copiar no se paga.** La verificación se paga solo donde su resultado no se puede obtener copiando la respuesta de otro |
| D16 | Fallo de hardware honesto | **No se castiga como engaño:** la tarea no se paga, la suma en espera no se pierde; el número de tales fallos por clave está limitado |
| D17 | Fuente del pago por las peticiones en la variante B | **Solo de los pagos de los usuarios**, sin emisión de créditos |
| D18 | Pago del entrenamiento por una mejora demostrada | **Se investiga como candidato a una nueva unidad de pago del entrenamiento, pero no se ha aceptado.** No es una verificación del paso ni una demostración de ausencia de daño: el modelo se publica solo según la regla D9. La decisión de aceptarlo es tras los cálculos M7, M8, M10–M12 y el experimento O6 (fuera de D5, hace falta la autorización del propietario). La búsqueda de una verificación del propio paso continúa |
| D19 | Error criptográfico pequeño | **Se admite como supuesto explícito** con tres condiciones: aleatoriedad de un faro externo tras la fijación definitiva, la muestra no se deriva de los datos del ejecutor (sin Fiat–Shamir), está escrita la cota inferior del precio del intento y `ε·R` es menor que ella. El error no supera `2⁻⁸⁰` por intento. Esto no resuelve la verificación por muestreo habitual con fuga `q^k` |
| D20 | Faro externo | **No menos de dos fuentes públicas independientes**, el valor se toma en un momento designado de antemano tras la fijación definitiva, sin derecho a omitirlo. Las fuentes y el coste de influir en ellas se eligen en la etapa 2; la confianza en ellas se anota como supuesto. Hasta que se elija el esquema con muestreo no se incluyen |
| D21 | Quién verifica la respuesta del modelo | **La verificación de la respuesta independiente de la colusión es solo la del pagador, que verifica por sí mismo.** La red no paga una respuesta sin verificación. Un usuario sin equipo puede designar él mismo un verificador; es su supuesto, la red no le promete D1. La garantía para ese usuario sigue siendo una cuestión abierta |
| D22 | Cambios de producto en aras de una verificación barata | **Se permiten como tipos de tarea aparte del plan con un contrato explícito** (elección canónica del token, perfil con aritmética entera, tareas con desenlace verificable, optimizadores exactos), tras el experimento O5 y el cálculo M17. El muestreo habitual sigue con la marca «no verificado» |
| D23 | Disputas falsas del pagador | **Primero el cálculo M9.** La verificación por el pagador no se incluye hasta que se elija una regla que limite las disputas falsas sin depósito |
| D24 | Texto cifrado de la respuesta en el registro | **Sí:** se anota en una sola anotación junto con la aceptación, unos 2–4 KB por respuesta |
| D25 | La doble condición de D1 | **No cambia:** una falsificación que es peor que el trabajo honesto pero más rentable que la inacción también incumple D1 |

**Orden de trabajo.** Primero se termina la etapa 0 — los miniagentes y las aplicaciones para
smartphones, para que otras personas puedan incorporarse al trabajo. Después, las etapas 1–5 según
esta hoja de ruta.

## 4. Etapas y lista de comprobación

Primero se termina la etapa 0. Después, las etapas 1–4 avanzan a la vez: son cálculos y razonamientos.
La etapa 5 (experimento autorizado por la decisión D5) va después de la etapa 0. La etapa 6 reúne
los resultados.

### Etapa 0. Miniagentes y aplicaciones para smartphones (se ejecuta primero)

**Objetivo de la etapa.** En cada plataforma admitida, una persona recorre el camino «descargó →
instaló → ejecutó» y, a partir de ahí, el miniagente se actualiza sin intervención humana, toma
tareas y entrega el resultado. Sin cuenta, sin permisos de administrador, sin Python instalado de
antemano. Cada paso está comprobado en un dispositivo real, no solo con pruebas automáticas.

**Terminado cuando** para cada plataforma de la lista de abajo: una persona sin experiencia ha
recorrido el camino con una sola página de instrucciones; el agente de ese dispositivo obtuvo por
sí mismo una versión nueva, tomó por sí mismo una tarea de la lista nueva, su resultado apareció en
el nodo completo y coincidió con el resultado de otro dispositivo. Están anotados el sistema, la
arquitectura, las versiones de antes y de después y el identificador del registro en el nodo.

Plataformas: Windows, Linux, Android (decisión del 23 de noviembre de 2026). Para macOS e iOS los
miniagentes no se hacen ni se comprueban. El comando de instalación para Linux quizá funcione también
en macOS, pero esto no está soportado. La versión para Windows se publica sin firma de código:
al instalar, Windows muestra la advertencia de SmartScreen y hay que confirmarla manualmente;
la autenticidad del archivo se comprueba mediante el hash publicado y la firma del proyecto.

Ya hecho:

- [x] Repositorio público, base inmutable en nueve idiomas (etiqueta `core-v1`).
- [x] Programa agente para Windows y Linux: tareas y actualizaciones firmadas,
      comprobaciones automáticas en CI (versión 0.2.0). Instalación con un solo
      comando en la terminal; se necesita Python 3.9+.
- [x] Resultados y [tablero de tareas](BOARD.md) sin cuenta.
- [x] Primer nodo completo que guarda el historial de registros.
- [x] Primera tarea de investigación «Defensa contra los defraudadores» en el tablero, en nueve idiomas.
- [x] Aplicación Android de prueba 0.1.0 (comprobada solo en el emulador).

**Paso 1. Fiabilidad de la actualización (versión 0.2.1, sin tareas nuevas)**

- [x] La primera instalación comprueba la firma de la versión con la clave integrada en el propio
      instalador, **antes** de ejecutar el código descargado (antes, el agente descargado se
      comprobaba a sí mismo).
- [x] Cambio a una versión nueva con una sola operación atómica: primero se prepara y se comprueba
      el directorio nuevo, luego se cambia un único puntero; el conjunto funcional anterior se
      conserva.
- [x] El mayor número de versión aceptado se guarda fuera de los directorios de versiones y se
      comprueba también al reinstalar (protección contra el retroceso a una versión antigua).
- [x] La clave del dispositivo, la configuración, el progreso y los resultados no enviados se
      guardan fuera de los directorios de versiones y sobreviven a la actualización y a la
      reinstalación.
- [x] Sin red, el agente sigue trabajando con la última versión funcional y repite la conexión
      con un intervalo creciente.
- [x] Comprobación automática en CI: un archivo sustituido, una clave ajena, un número antiguo,
      un archivo de más, una descarga interrumpida y un Python incompatible se rechazan; la versión
      en funcionamiento se conserva.
- [x] **Comprobación en vivo en el servidor:** la instalación 0.2.0 pasó por sí misma a la 0.2.2 el 23 de noviembre
      de 2026; la clave del dispositivo y el progreso se conservaron. En el Linux doméstico, el agente se instaló
      de nuevo con el nuevo instalador (0.2.2); la próxima versión comprobará su autoactualización.
- [x] Comprobación en vivo de la autoactualización en Windows: la instalación del propietario pasó por sí misma
      de 0.2.2 → 0.3.0 → Go 1.0.1 (23 de noviembre de 2026).

**Paso 2. Android: aplicación sin token**

- [x] APK nuevo 0.2.0 con el agente 0.2.2 integrado: publicación mediante registros firmados, se quitan
      la pantalla del token y las indicaciones sobre el token.
- [x] Corregir el falso retroceso sin red: antes, tres arranques sin conexión marcaban una versión
      nueva y funcional como defectuosa. Ahora la versión se confirma con una autocomprobación local.
- [x] Una vez al día, la aplicación comprueba si hay versiones nuevas del APK, coteja el hash y la
      firma del proyecto y ofrece instalarla; la instalación la confirma una persona (así funciona
      Android fuera de la tienda).
- [x] Arranque tras el reinicio mediante un interruptor del usuario (comprobado en el emulador).
- [x] Comprobación de la actualización sobre el APK 0.1.0 en el emulador Android 14: los datos se conservan.
- [x] APK 0.4.1 (24 de noviembre de 2026): corregido el envío de resultados — Android prohibía el método
      de guardar la clave del dispositivo; en el emulador se calcularon y enviaron 4 de 4 sin token.
- [x] APK 0.4.2: el arranque tras el reinicio está activado por defecto (comprobado reiniciando el
      emulador). La antigua versión de prueba 0.1.0, que pedía token, está marcada como obsoleta.
- [ ] Comprobación de que la propia aplicación ofrece el APK nuevo (funcionará con la siguiente versión del APK).
- [ ] **Comprobación en vivo en un teléfono real** (hace falta un participante con teléfono):
      instalación, funcionamiento durante la carga, reinicio, ahorro de energía del fabricante.

**Paso 3. Windows: instalador de un solo archivo**

- [x] `SkyNetAgentSetup.exe` se compila en GitHub Actions, sin firma de código; dentro, Python
      incrustado de python.org, el agente y la versión firmada. Junto a él se publican su hash y
      la firma del proyecto. Instalación en el perfil del usuario, sin permisos de administrador,
      funciona sin red.
- [x] Accesos directos en el menú «Inicio»: estado del agente, pausa, continuación, detención,
      desinstalación.
- [x] Las casillas «ejecutar ahora» y «ejecutar al iniciar sesión» del instalador están activadas por
      defecto (desde la 1.3.3); la elección se conserva al actualizar.
- [x] Desinstalación mediante «Aplicaciones»; al desinstalar se puede conservar la clave del
      dispositivo.
- [x] Comprobación automática en CI en un Windows limpio sin Python: instalación, autocomprobación,
      desinstalación.
- [x] Comprobación en vivo en el ordenador de una persona: el propietario instaló el agente
      desde Releases (versión v0.2.2).

**Paso 4. Linux**

- [x] El instalador usa el Python 3.9+ del sistema y, si no lo hay, instala un Python portátil
      y comprueba su hash. También hay un instalador de un solo archivo sin red (versión v0.2.2).
- [x] Desde la 1.3.3, el instalador inicia el agente de inmediato, registra el servicio de usuario systemd
      (arranque tras el reinicio) e intenta activar el funcionamiento sin iniciar sesión (linger);
      `--no-autostart` — solo la instalación.
- [x] Desde la 1.3.4, el agente encuentra por sí mismo el nodo completo en su red local (consulta por UDP,
      respuesta solo a direcciones privadas). Hace falta donde el router no deja pasar desde dentro de la red
      a la dirección externa del nodo; antes esto se evitaba configurando la dirección a mano.
- [x] Comprobación en vivo de la búsqueda del nodo en la red local: el agente 1.3.4, sin configuración
      manual, encontró el nodo y apareció en la página de agentes (25 de noviembre de 2026).
- [x] Comprobación en CI: Debian 12 sin Python y Ubuntu 24.04 con Python; instalación en vivo en Linux Mint.
- [ ] Comprobación en vivo en un participante no vinculado a los mantenedores.

**Paso 5. Agente en Go en lugar de Python (decisión del propietario del 23 de noviembre de 2026)**

El agente se ha reescrito en Go: un único programa pequeño, no hace falta Python. El Python integrado y su
actualización ya no son necesarios, por lo que se ha suprimido el paso anterior «actualización del Python integrado».

- [x] Firmas, tareas, siete núcleos de cálculo, registros, Nostr, tablero, ciclo de trabajo, actualización
      por el segundo canal (`agent/v2/release.json`), lanzador, inicio automático: en Go, solo
      la biblioteca estándar (el código lo escribió ChatGPT, lo revisó DeepSeek).
- [x] Los resultados de Go coinciden con Python bit a bit en todas las porciones rápidas de referencia y en todas
      las pesadas comprobadas; el cotejo de las 1 199 porciones continúa.
- [x] Compilación reproducible: hashes idénticos de los programas al compilar en Windows y Linux.
- [x] El puente en Python 0.4.0 migra por sí mismo los agentes instalados a Go conservando la clave
      del dispositivo, el progreso y la cola. Transición en vivo: el servidor, el Linux doméstico y el Windows del propietario
      pasaron a Go 1.0.1 por sí mismos.
- [x] Instaladores en Go: Windows 4,7 MB, Linux en un solo archivo; aplicación Android 0.3.0 con
      motor Go, unos 8 MB en lugar de 40 (comprobado en el emulador Android 14).
- [x] Versiones en Go 1.1.0–1.3.4 (24 de noviembre de 2026): respuestas del modelo de IA local, cálculos
      de la etapa 4, página de agentes, inicio automático, búsqueda del nodo en la red local; los agentes
      instalados se actualizaron por sí mismos.
- [ ] Eliminar el puente y las copias en Python tras dos versiones verificadas en Go.

**Paso 6. Flujo de tareas**

- [x] Cuatro tareas de cálculo nuevas de la etapa 2 (campaña de salida de la variante B, plazas de
      aprendiz, lotería con proporción de verificación ajustada, certificado del token ganador):
      nuevos núcleos integrados del agente 0.3.0, 515 porciones en la lista de tareas n.º 2.
      La matemática se verificó de forma independiente con otro método en 111 puntos. El certificado
      sobre matrices aleatorias no aporta ahorro (alrededor del 0,8% de trabajo adicional), por lo
      que se dejaron 20 porciones como base para comparar con los pesos del modelo real.
- [x] Las tareas nuevas requieren el agente 0.3.0 o superior; el agente antiguo se salta la tarea
      incompatible y sigue trabajando (comprobado con una prueba).
- [ ] Cuando todas las tareas están calculadas, el agente espera y toma por sí mismo la lista
      siguiente.
- [ ] El recolector de resultados funciona según un horario en el nodo completo y publica un
      resumen.
- [ ] Confirmación independiente de las 702 porciones de la primera lista. Un segundo dispositivo
      (el servidor de los mantenedores) recalculó las 702 y todas coincidieron; todavía no hay un
      participante no vinculado a los mantenedores.

**Paso 7. Piloto con otras personas**

- [x] Página [«Cómo conectarse»](CONNECT.md) en nueve idiomas: un enlace por cada sistema.
- [x] Página de agentes en línea en el nodo completo: `http://62.213.14.254:8790/agents` — SO, procesador,
      RAM, tarjetas gráficas, versión, porciones; sin IP ni nombres de ordenadores. El agente informa de sí
      mismo cada 2 minutos; 5 minutos de silencio lo quitan de la lista (agente 1.3.0+).
- [ ] Un participante no vinculado a los mantenedores en cada plataforma; se cumplen los criterios
      de finalización de la etapa.
- [ ] Segundo y tercer nodos completos de propietarios distintos.

**Paso 8. Agentes de IA**

- [x] El agente recoge por sí mismo las tareas nuevas del tablero y las entrega al modelo local
      del participante; la respuesta se envía solo tras la aprobación de una persona. El texto de
      la tarea se considera no fiable (agente 1.1.0, desactivado por defecto).
- [ ] Instrucciones para el asistente de IA: cómo tomar una tarea del tablero, entregar un informe y comprobar el informe de otro.
- [ ] Informe para una tarea del tablero de un participante no vinculado a los mantenedores.

**Decisiones del propietario sobre la etapa 0** (23 de noviembre de 2026): macOS e iOS no se
hacen; la versión para Windows se publica sin firma de código.

### Etapa 1. Planteamiento exacto

- [x] Las decisiones D1 y D2 están tomadas y escritas (sección 3).
- [ ] Para una petición abierta y un paso de entrenamiento están escritos: la regla de aceptación, la aritmética,
      la base de la emisión de créditos, el momento de fijación del resultado respecto al sorteo y el momento en que
      el resultado se puede usar.
- [x] Modelo del adversario en un solo documento: [THREAT_MODEL](THREAT_MODEL.md), sección 1 (consejo de
      seis modelos y tres críticos, 24 de noviembre de 2026).
- [x] La tabla de ataques analizados está publicada en nueve idiomas con el estado de cada ataque para
      las variantes A y B: 60 ataques de la especificación y 32 nuevos. La discrepancia entre 59 y 60 está
      explicada: en el resumen se omitió la fila 1.9 («no es un ataque»).
- [x] Para cada ataque está escrito con qué datos verificables de forma independiente rechazará el nodo
      una declaración falsa en caso de colusión del ejecutor y de los verificadores. Resultado: ni la
      variante A ni la variante B cumplen D1 literalmente; la ganancia monetaria es posible en 24 filas
      de A y 25 filas de B [cálculo].
- [x] Decisiones sobre las doce cuestiones de la sección 5 de [THREAT_MODEL](THREAT_MODEL.md): D6–D17.

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

- [x] El consejo de modelos (seis trabajos y tres críticas) analizó todas las direcciones; el resultado y las tareas para los miniagentes están en [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), 24 de noviembre de 2026.
- [x] Los primeros cálculos exactos para los miniagentes: M8, M10, M12 y M14 de la sección 5.3 del compendio
      ([STAGE4_KERNELS](STAGE4_KERNELS.md)), agente 1.2.0, lista de tareas n.º 3. Los cálculos M5, M7 y M18
      quedan aplazados: en los trabajos faltan reglas para determinarlos de forma inequívoca.
- [ ] **Tareas con un criterio exacto y barato de corrección.** Ejemplo: para la regresión ridge, el nodo
      comprueba la condición de óptimo en una sola pasada por los datos. Pregunta: qué proporción del trabajo de la red
      cabe en tales tareas. Empezar por esta dirección: garantiza un pago falso nulo. *Resultado:* se sostiene para una clase estrecha de tareas, se desconoce la proporción de ese trabajo.
- [x] **Comprobación de cada multiplicación de matrices con un vector aleatorio** en lugar del recálculo. El vector
      se elige después de fijar el resultado; la probabilidad de dejar pasar un error no depende de la colusión.
      Es rentable para lotes grandes; al generar un token cada vez no hay ganancia. Las demás
      operaciones (redondeo, activaciones, caché, optimizador) hay que comprobarlas por separado. *Resultado:* refutado como verificación barata por el nodo de la red (choca con el tráfico); se sostiene como verificación del pagador con un canal rápido.
- [ ] **Comprobación de la respuesta final en una sola pasada del modelo** con un perfil exacto y la aleatoriedad
      fijada en la tarea. El número de operaciones es del mismo orden que el de la generación; no está establecido si cabe
      en el 5%. *Resultado:* el mejor candidato para la respuesta del modelo es la verificación por el pagador, 1,2–3,8% al generar una sola respuesta [cálculo]; espera el experimento D5 y la decisión D23.
- [x] **Tablas de sumas parciales exactas para capas inmutables:** el nodo deriva una vez las tablas
      a partir de los pesos y luego obtiene la salida de la capa con lecturas y sumas. Aplicable también a un solo token;
      se topa con el volumen de memoria. *Resultado:* refutado por cálculo.
- [x] **Certificado del token ganador** para un vocabulario grande: el ejecutor transmite la cobertura
      del vocabulario por grupos, el nodo comprueba las cotas superiores y desciende a los tokens sueltos solo
      donde la cota no separa al ganador. En el peor caso se comprueba todo el vocabulario. *Resultado:* se sostiene como parte de la verificación de la selección voraz.
- [x] **Paso de entrenamiento como fórmula exacta de actualización:** los nodos guardan y comprueban no la nueva matriz
      de pesos, sino los multiplicadores de actualización. Derivado solo para una capa lineal con SGD simple. *Resultado:* refutado como verificación del paso.
- [x] **Disputa abierta a cualquier participante durante la ventana.** Garantía condicional: hace falta al menos un
      observador que haya recibido los datos y haya tenido tiempo de objetar. Quién paga la observación con
      la cuenta vacía no está resuelto. Dejarlo como reserva. *Resultado:* refutado como verificación independiente de la colusión.
- [ ] **Pago por la mejora medida del modelo** en tareas elegidas después de fijar los pesos.
      Cambia la base del pago y exige una decisión aparte. Sirve para seleccionar versiones del modelo. *Resultado:* el único camino que sobrevive para el entrenamiento, con correcciones; se investiga según D18.
- [ ] **Demostraciones de cálculo para el entrenamiento (sumcheck, GKR)** para un paso determinado:
      presupuesto completo con rangos, redondeo y vinculación de la entrada a la tarea. *Resultado:* se sostiene como dirección; los desgloses concretos están refutados, el 20% no se ha demostrado.
- [x] **Límite inferior:** mostrar qué clases de verificaciones no pueden ser infalibles. Comienzo:
      un conjunto fijo de comprobaciones lineales en número menor que el tamaño del resultado siempre deja pasar
      algún error; quedan abiertas la aleatoriedad fresca y las entradas con estructura conocida. *Resultado:* las cotas que se mantienen están publicadas en [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), sección 2.
- [ ] Ideas de los participantes y de los asistentes de IA del tablero: cada una pasa el mismo análisis, incluido el caso
      `q = 1`.

Terminado cuando: para cada dirección están publicados una construcción con presupuesto, un contraejemplo o
un límite demostrado. Se considera encontrada la construcción que cumple todos los criterios de la sección 1.

### Etapa 5. Fundamentos que solo se establecen mediante experimentos (autorizado por D5)

- [x] Plan del experimento: perfil Qwen3.5-4B con aritmética entera, protocolos O1–O5 y criterios de refutación
      antes de la ejecución — [EXPERIMENT_D5](EXPERIMENT_D5.md), 24 de noviembre de 2026. La segunda tarjeta gráfica es
      una RTX 4070 Laptop en el ordenador del propietario.
- [x] Preparación (P0) y perfil v2: el modelo se cotejó con el original oficial; en el procesador, el perfil
      con aritmética entera elige el mismo token que el modelo oficial en 90 de 90 posiciones (correlación
      de logits 0,9996). El primer perfil v1 perdía precisión y se sustituyó.
- [x] Entradas cortas: el procesador, la RTX 2060 (Linux) y la RTX 4070 Laptop (Windows) dan los mismos
      bits — 242 millones de logits, 976 tokens y 37 mil hashes de estado por dispositivo; la generación
      token a token y el paso por una respuesta ya lista coinciden (O1 y O2, 24 de noviembre de 2026).
- [x] Otra arquitectura: la AMD Radeon RX 580 (OpenCL, Mesa) y NVIDIA mediante OpenCL dan los mismos
      bits que la versión CUDA y el procesador, con las mismas entradas cortas (25 de noviembre de 2026).
- [x] Contexto largo (512 + 64, 2048 + 256, 4096 + 64 tokens): la RTX 2060 (CUDA y OpenCL) y la RTX 4070 Laptop dan
      los mismos bits; la generación coincide con el paso por una respuesta ya lista (25 de noviembre de 2026).
      RX 580: la generación coincide, el paso por una respuesta larga lo interrumpe el controlador; hay que dividir
      el núcleo de atención.
- [ ] Proporción del tiempo de verificación de la respuesta respecto a la generación (O3).
- [ ] Su velocidad respecto al perfil normal en las mismas tarjetas.
- [ ] Su calidad respecto al perfil normal en el mismo conjunto de tareas.
- [ ] Planes de medición aparte (fuera de D5): energía de la verificación, entrenamiento con aritmética entera.
- [ ] Coste de la disputa en el registro para el modelo completo. Antes hacen falta la elección de la cadena de bloques, una máquina de referencia
      del modelo completo, la vinculación de la entrada, las longitudes y las rutas de cálculo.

Terminado cuando: cada cifra está medida, las condiciones de la medición están escritas y la medición la repitió un segundo
participante. La coincidencia de bits se refiere solo a las configuraciones probadas.

### Etapa 6. Síntesis y aceptación

- [x] Decisión D4 sobre el núcleo inmutable (sección 3).
- [ ] Composición del núcleo y forma en que un participante se asegura de que su programa corresponde a la huella publicada.
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
