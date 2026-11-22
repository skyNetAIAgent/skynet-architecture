<!-- translation of docs/RESEARCH_AGENT.md, source sha256: 5b9c405c6752d25fab4db09f92c07df1d7daa6bf9dfd8b40de30d40adb0236a4 -->

# Programa agente: cómo ayudar al proyecto sin un asistente de IA

[English](../../docs/RESEARCH_AGENT.en.md) · [中文](../zh/RESEARCH_AGENT.md) · **Español** · [Français](../fr/RESEARCH_AGENT.md) · [Deutsch](../de/RESEARCH_AGENT.md) · [Italiano](../it/RESEARCH_AGENT.md) · [Русский](../../docs/RESEARCH_AGENT.md) · [Português](../pt/RESEARCH_AGENT.md) · [العربية](../ar/RESEARCH_AGENT.md)

Estado al 22 de noviembre de 2026. Versión del agente 0.2.0 (aún no publicada). Instrucciones para el participante:
[agent/README.md](../../agent/README.md) ([en ruso](../ru/AGENT.md)).

## Por qué

El repositorio está pensado para personas que tienen un asistente de IA: lee los documentos y ayuda
a diseñar. La mayoría de la gente no tiene ese asistente, pero sí un ordenador o un teléfono.
El programa agente les da una forma de participar: consulta periódicamente este repositorio,
toma tareas, las ejecuta en el dispositivo del participante y publica los resultados.

En esta etapa **no hay recompensas**: ni créditos, ni dinero, ni promesas de pagos futuros.
El objetivo es atraer al diseño de la arquitectura el mayor número posible de recursos de cálculo
y de verificadores independientes.

El agente es una **herramienta de investigación, no la red SkyNet**. Está hecho de forma más
sencilla y centralizada de lo que debe ser la red, y no cumple sus requisitos obligatorios.
Más abajo se dice claramente en cada punto.

## Cómo está hecho

| Parte | Dónde está | Qué hace |
|---|---|---|
| Lista de tareas | `tasks/index.json` y la firma `tasks/index.json.sig` | Nombra el cálculo incorporado, sus parámetros y el número de porciones independientes |
| Agente | `agent/skynet_agent/`, solo la biblioteca estándar de Python 3.9+ | Comprueba las firmas, elige una porción, calcula, publica, se actualiza |
| Descripción de la versión | `agent/release.json` y la firma | Enumera los archivos del agente con su tamaño y SHA-256 |
| Lanzador | `agent/launcher.py` | Arranca la versión actual, pasa a la nueva, vuelve atrás desde una versión rota |
| Resultados | Registros firmados con la clave del dispositivo, a través de relevos Nostr públicos y nodos completos ([tablero de tareas](BOARD.md)); si se desea, comentarios en la incidencia de GitHub | Registro legible por máquina con la huella del resultado |
| Resumen | `results/`, lo construye `tools/collect_results.py` | Compara los resultados de distintas personas y vuelve a comprobar los hallazgos |

Un ciclo de trabajo del agente:

1. Cada 30 minutos (con dispersión) descarga la descripción de la versión y la lista de tareas.
2. Comprueba la firma de cada uno con la clave de publicación incorporada en la copia instalada.
3. Si hay una versión con un número mayor, descarga sus archivos, comprueba cada uno con la huella,
   la coloca junto a la actual y se reinicia.
4. Elige una porción aleatoria de la tarea que todavía no ha calculado.
5. La calcula en un proceso aparte con la prioridad más baja y límite de tiempo.
6. Pone el resultado en la «bandeja de salida» y lo envía como un registro firmado con la clave de este
   dispositivo, de inmediato a varios relevos Nostr públicos y nodos completos. No hace falta cuenta.
   Un registro se considera entregado cuando lo confirmaron dos relevos o un nodo completo; en caso
   contrario, permanece en la «bandeja de salida» y el intento se repite: al minuto, después el doble
   de tiempo, pero no más de una hora. El reintento envía el mismo registro, de modo que el resultado
   no se cuenta dos veces. El método anterior, comentarios en la incidencia de GitHub en nombre del
   participante, se activa con el ajuste `submit_via github`. Tras trescientos resultados no enviados,
   el agente deja de tomar trabajo y lo comunica.

No hay planificador: cada agente elige la porción por sí mismo. La coincidencia de porciones entre
distintos participantes es intencionada: todas las tareas de cálculo son de números enteros, de modo
que en cualquier dispositivo se obtienen las mismas cifras. La coincidencia de huellas entre distintas
cuentas de GitHub se considera confirmación; la coincidencia entre distintas claves no, porque una
clave no cuesta nada y una persona puede crear cuantas claves quiera. Esas porciones las confirma
el recálculo.

## La tarea son datos, no un programa

El agente nunca descarga ni ejecuta código de la tarea. La tarea nombra uno de los
cálculos incorporados en el agente (el «núcleo») y le pasa números. Cada núcleo comprueba
los parámetros y limita el volumen de trabajo. Un nuevo tipo de cálculo solo aparece con una
nueva versión firmada del agente, cuyo código fuente está en el repositorio y se lee con los ojos.

Núcleos de la versión 0.1:

| Núcleo | Qué calcula |
|---|---|
| `selftest` | Cálculo de control de números enteros: la huella debe coincidir en todos los dispositivos |
| `exit-scam-a` | La expectativa exacta de pago del participante que, antes de irse, entrega falsificaciones (variante A de [CURRENT_DESIGN](CURRENT_DESIGN.md)); recorre una familia de estrategias y comunica las que son más ventajosas que una salida honesta |
| `lottery-b` | La probabilidad exacta de un mes o trimestre con pérdidas si se paga solo por tareas verificadas (variante B) |
| `ai-answer` | A petición del participante: una pregunta para el modelo de IA local que ejecuta él mismo |

El modelo exacto de cada cálculo está escrito al principio del archivo fuente del núcleo, para que
cualquiera pueda recalcular el resultado de forma independiente. Las tareas y su significado:
[tasks/README.md](../../tasks/README.md).

**Límite con la regla del proyecto sobre los experimentos.** Las primeras tareas son cálculos
con las fórmulas de los documentos (análisis de coste y búsqueda de contraejemplos) y preguntas
a los modelos de lenguaje. No son mediciones en el hardware ni experimentos con la red. Las tareas
de medición (por ejemplo, si coinciden los bits de la salida de números enteros en distintas
tarjetas gráficas) solo se publican después de que el dueño del proyecto decida abrir los
experimentos.

## Modo de IA (opcional, experimental)

El participante que ejecuta en su equipo un modelo abierto (Ollama, el servidor de llama.cpp,
LM Studio y similares con una interfaz compatible con OpenAI) puede activar `ai.enabled`. Entonces
el agente pasa al modelo las preguntas de la lista firmada y publica las respuestas. Así, las
personas sin suscripción a una IA pero con tarjeta gráfica se convierten en participantes del
«consejo de modelos».

- El agente no descarga ni arranca el modelo y, por defecto, solo se dirige a un servidor
  del mismo ordenador.
- La pregunta y los documentos que cita vienen dados por la lista firmada. Cada documento
  se comprueba con la huella, de modo que no se puede dar al modelo otro texto.
- La respuesta espera por defecto en la «bandeja de salida» hasta que el participante la aprueba:
  el texto se publica en su nombre.
- La respuesta se marca como generada por máquina y no verificada por nadie. El número de
  respuestas por pregunta es limitado.

Solo se ha verificado con un servidor simulado en las pruebas automáticas. Con entornos reales
de ejecución de modelos, el modo todavía no se ha verificado.

## Aplicación para Android (experimental)

Para quien no quiere configurar Termux, hay una aplicación: un solo archivo APK y un botón «Start».
Código fuente e instrucciones: [android/README.md](ANDROID.md). En la aplicación está
integrado el mismo paquete `skynet_agent` y Python (mediante Chaquopy). Diferencias con el agente
de ordenador:

- Android no permite arrancar procesos Python aparte, de modo que la porción se calcula en el
  proceso en segundo plano de la propia aplicación, de una en una. Si la porción tarda más que
  el límite, el vigilante termina ese proceso, Android vuelve a arrancar el servicio y la tarea
  queda para los dispositivos más rápidos.
- La nueva versión del agente se toma del repositorio con la misma firma de la clave de
  publicación. La comprueba la copia integrada; si la nueva versión no arranca aquí o sus
  archivos han cambiado, la aplicación vuelve a la integrada.
- La propia aplicación (pantalla, servicio, vigilante) solo cambia con un APK nuevo. El APK está
  firmado con una clave aparte de los responsables del proyecto: es un segundo punto único de confianza que
  no debe existir en la red.
- Los resultados salen como registros firmados, igual que en el agente de ordenador. El token de
  GitHub solo hace falta si el participante eligió el método anterior de publicación.
- Solo trabaja mientras se carga, salvo que el participante permita otra cosa. No hay modo de IA.

Estado al 22 de noviembre de 2026: la aplicación se compila y su parte en Python pasa las pruebas
en el ordenador (`agent/tests/test_android_glue.py`). La compilación de prueba con una clave de
prueba ha pasado en el emulador de Android 14 (x86_64) con un repositorio local de prueba:
instalación, comprobación de firmas, cálculo de las 7 porciones de prueba sin errores, espera sin
carga, trabajo en segundo plano, guardado del token y su uso con la API real de GitHub, parada y
nuevo arranque con el estado guardado.
En un teléfono real la aplicación todavía no se ha ejecutado, y la compilación para ARM
(`arm64-v8a`) no se ha verificado. No se distribuye a través de Google Play: sus normas prohíben
las aplicaciones que cargan código ejecutable.

## En qué confía el agente

| Qué | Confianza |
|---|---|
| Firma Ed25519 con la clave de publicación | Sí. Sin ella no se acepta ni la versión ni la lista de tareas |
| Canal (HTTPS, espejo, el propio GitHub, relevos Nostr, nodos completos) | No para la integridad: cambiar un archivo rompe la firma o la huella, sustituir un registro rompe su firma |
| Contenido de la tarea | No: los parámetros se comprueban, el volumen de trabajo está limitado, no hay código en la tarea |
| Respuesta del modelo local | No: es texto y se publica como no verificado |
| Primera instalación | Sí, al canal HTTPS hasta GitHub. Lo instalado se puede comprobar con la orden `selftest --online` |

**Límite honesto.** Quien tiene la clave de publicación puede entregar el programa a todos los
agentes instalados. Ahora mismo la clave la tienen los responsables del proyecto. Es un punto único de
confianza que no debe existir en la red SkyNet: en el proyecto objetivo el programa solo se
actualiza a una versión cuya huella ha sido aceptada por votación de los participantes en el
registro común, y la firma con la clave de alguien no basta
([CURRENT_DESIGN, sección 8](CURRENT_DESIGN.md)). El participante que no quiere confiar en la
clave pone `update` en `notify` y se actualiza a mano después de leer los cambios.

## Tabla de amenazas

| Amenaza | Con qué se cubre | Qué queda |
|---|---|---|
| Compromiso del repositorio o de la cuenta con permiso de escritura: sustitución del agente | La versión solo se acepta con la firma de una clave que no está en el repositorio | Cubierto mientras no se robe la clave |
| Sustitución de un archivo por el camino o en el espejo | La firma de la descripción de la versión y el SHA-256 de cada archivo | Cubierto |
| Vuelta atrás a una versión antigua vulnerable | El número de versión debe ser mayor que el actual | Cubierto para los agentes instalados. Una instalación nueva toma lo que hay en el repositorio |
| Tarea dañina | La tarea no lleva código; el núcleo comprueba los parámetros y limita el volumen de trabajo y de memoria; hay un límite de tiempo | Limitado: una tarea firmada puede ocupar el procesador hasta el límite de tiempo |
| Repetición de una lista de tareas firmada antigua | El número de la lista no debe ser menor que el ya visto; la lista puede tener una fecha de caducidad | Limitado: una instalación nueva puede recibir una lista antigua y calcular en vano tareas cerradas |
| Versión rota | El lanzador devuelve la versión anterior tras tres caídas rápidas o si los archivos de la nueva versión han desaparecido, y recuerda el número inservible. Las peticiones repetidas de reinicio las cumple con una pausa creciente | Cubierto para las caídas al arrancar. Un error silencioso en el cálculo lo detecta la comparación de resultados |
| Robo de la clave de publicación | La clave está fuera del repositorio; en Windows está cifrada para la cuenta del dueño | **Abierto.** El ladrón puede publicar una versión dañina. El cambio de clave se hace con una versión nueva firmada con la clave antigua, y al ladrón también le resulta accesible |
| Pérdida de la clave de publicación | Copia de seguridad en poder del dueño | Sin la clave no se puede actualizar a los agentes instalados: los participantes tendrán que instalar el agente de nuevo |
| Falsificación de un resultado | El cálculo de números enteros se compara entre distintas cuentas de GitHub; todas las claves juntas, el recopilador las cuenta como un solo voto; los hallazgos se recalculan al recopilar | Limitado: una persona con dos cuentas se «confirmará» a sí misma. No hay recompensas, así que no hay beneficio en ello, pero es posible un atacante. Los responsables recalculan de forma selectiva |
| Flujo de basura de cuentas ajenas y claves gratuitas | El recopilador solo acepta registros con la firma correcta, la huella correcta y una tarea conocida; el nodo limita el tamaño, la frecuencia y el volumen total | **Abierto para las claves**: una clave no cuesta nada, por eso se puede enviar basura sin fin. Es parte de la principal pregunta abierta del proyecto |
| Fuga de la clave del dispositivo | La clave está en la carpeta del agente y no se envía a ningún sitio | Quien copie el archivo `identity.key` podrá firmar en nombre del dispositivo. La firma en Python puro no es de tiempo constante |
| Fuga del token de GitHub (método anterior) | El agente no guarda el token, lo toma de `gh` o de la variable y no lo envía a ningún sitio salvo a GitHub por HTTPS, sin redirecciones | El token con permiso de escritura en repositorios públicos sigue siendo responsabilidad del participante |
| Código ajeno junto al agente (un módulo plantado en la carpeta actual) | Modo aislado de Python (`-I`) | Cubierto. Contra un programa con los permisos del mismo usuario en el mismo ordenador no hay protección |
| Consumo de recursos del participante | Un proceso por defecto, la prioridad más baja, pausa con batería, límite de tiempo, órdenes `pause` y `stop` | La electricidad la gasta el propio participante, de forma gratuita |
| Parada de todos los agentes por los responsables | La marca firmada `halt` en la descripción de la versión; actúa incluso con las actualizaciones desactivadas | Es una palanca intencionada: solo parar, sin arrancar nada |

## Qué dice el agente sobre sí mismo

Solo el contenido del registro publicado: el nombre de la tarea, el número de porción, las cifras
del resultado, el tiempo de cálculo y, salvo que se desactive, una etiqueta aproximada de
plataforma como `linux-amd64-py3.12`. Las peticiones van a GitHub (tareas y versiones) y a los
relevos y nodos de `trust.py` (registros). Los registros son públicos y están firmados con la
clave permanente del dispositivo, de modo que los resultados de un mismo dispositivo se pueden
relacionar entre sí, y el receptor ve la dirección de red del remitente. No se recogen datos sobre
los archivos, la red ni el hardware del participante.

## Procedimiento para los responsables

La clave de publicación se crea una sola vez y se guarda fuera del repositorio:

```
python tools/keytool.py generate
```

La copia de seguridad del secreto la hace el dueño a mano, con la orden
`python tools/keytool.py backup`, y la guarda fuera del ordenador. El secreto no se debe mostrar
a los asistentes ni pegar en chats y archivos.

Nueva versión del agente:

```
python tools/make_release.py --seq <siguiente número> --version <x.y.z>
```

después, subida de los archivos modificados de `agent/` al repositorio. Nueva lista de tareas:

```
python tools/sign_tasks.py
```

después, subida de `tasks/index.json` y `tasks/index.json.sig`. Recopilación de resultados de ambas
fuentes (registros firmados y comentarios de GitHub; `--net-only` o `--github-only` dejan una sola):

```
python tools/collect_results.py
```

Para detener el trabajo de todos los agentes hasta corregir un error: publicar una descripción de
versión con `--halt-through <número>` y el motivo.

## Qué no hay aquí y por qué hay que decirlo con honestidad

- **No es una red distribuida.** Las tareas y las versiones las reparte un único repositorio
  y las firma una única clave. Los resultados y las tareas del tablero ya van por varias
  plataformas independientes. Los requisitos R1–R4 de los [requisitos obligatorios](../ru/REQUIREMENTS.md)
  no se aplican al agente y no los cumple.
- **No hay protección frente a múltiples claves y cuentas.** Para la etapa gratuita esto es
  aceptable; los resultados importantes los confirma el recálculo.
- **Android no está verificado en un dispositivo real**; el inicio automático en macOS, Linux y
  Android solo está verificado al nivel de los archivos que se crean. Dos casos están contemplados
  por la documentación y tampoco están verificados en dispositivos reales: Python de Microsoft
  Store en Windows (ve una copia privada de `AppData` y del registro, de modo que la carpeta del
  agente está en el perfil y el inicio automático se añade a mano) y Python de python.org en macOS
  sin los certificados instalados (el agente repite la petición con el archivo de certificados del
  sistema).
- **Las primeras tareas son ligeras.** Toda la primera tanda (702 porciones) ocupó en un ordenador
  de sobremesa 15,5 horas de tiempo de procesador con 16 procesos simultáneos de prioridad más baja,
  es decir, alrededor de una hora de reloj [medido en un solo PC, 22 de noviembre de 2026].
  El mecanismo está listo para aceptar tareas pesadas. Qué ha resultado:
  [results/FIRST_RUN.md](../../results/FIRST_RUN.md).

## Qué viene después

1. Tareas de medición en distintos dispositivos: la principal incógnita del proyecto es la
   coincidencia del resultado bit a bit en distintas tarjetas gráficas. Son experimentos y esperan
   la decisión del dueño.
2. Hecho en la versión 0.2.0: resultados y [tablero de tareas](BOARD.md) sin cuenta.
3. Abandonar la clave única: varias firmas independientes y, después, la aceptación de versiones
   según las reglas de la propia red.
4. Gestión del modelo local: descargar un modelo abierto con comprobación de la huella, para que
   el modo de IA se active con una sola orden.
