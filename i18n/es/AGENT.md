# Agente de investigación de SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · **Español** · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Puede ayudar a diseñar SkyNet dejando que su ordenador haga parte de la investigación. El agente es un pequeño programa de código abierto. Consulta este repositorio en busca de tareas, realiza una parte de un cálculo y comparte el resultado. También puede publicar una pregunta de investigación o responder a la de otra persona en el tablero de tareas. No hace falta una cuenta ni un asistente de IA. [Guía del tablero de tareas](../../docs/BOARD.en.md)

**En esta etapa no hay recompensas.** No hay créditos, pagos ni promesas de pagos futuros. Es investigación voluntaria para ayudar a diseñar la red SkyNet.

## Qué hace y qué no hace nunca

| Hace | No hace nunca |
|---|---|
| Lee una lista de tareas firmada. Cada tarea indica un cálculo incorporado y aporta sus entradas | Ejecutar código de una tarea o de una publicación del tablero |
| Ejecuta una porción de trabajo a la vez por defecto, con prioridad de CPU baja | Iniciar una nueva porción de trabajo al detectar batería, por defecto |
| Firma los resultados con la clave de este dispositivo y, por defecto, los envía a relevos públicos y a un nodo completo | Incluir sus archivos personales o identificadores de hardware en un resultado automático |
| Comprueba la firma del proyecto antes de instalar una actualización de escritorio | Aceptar una actualización descargada con una firma no válida, un hash de archivo incorrecto o un número de versión anterior |
| Se instala en su cuenta de usuario y le deja elegir si arranca al iniciar sesión | Requerir derechos de administrador para una instalación de escritorio normal |

Una pregunta de investigación es si un participante que está a punto de abandonar puede beneficiarse de una tanda de resultados falsos. ¿Cuántos verificadores tendrían que ayudar? Distintos dispositivos a los que se da la misma parte de ese cálculo deberían obtener exactamente la misma respuesta, de modo que sus resultados puedan compararse. [Tareas de investigación](../../tasks/README.md)

## Requisitos

- Windows en x64 (amd64) o ARM64, o Linux en amd64, arm64 o ARMv7. El agente de escritorio de 1.0.1 es un único programa en Go. Los instaladores de Releases incluyen el ejecutable, listo para ejecutar. macOS no es compatible.
- Para la aplicación experimental de Android, Android 7.0 o posterior en arm64-v8a o x86_64.
- Una conexión a internet para recibir tareas nuevas y publicar resultados. El instalador de Linux de Releases puede instalar sin conexión.

## Instalación

**Windows**

1. Elija el instalador de Windows (`.exe`) para su ordenador, amd64 o arm64, en [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Compare la suma de comprobación SHA-256 del archivo con la suma de comprobación de una fuente de confianza y, después, ejecute el instalador. Puede elegir iniciar el agente ahora y arrancarlo al iniciar sesión. La instalación añade accesos directos al menú Inicio. [Guía del instalador de Windows](../../installer/windows/README.md)

**Linux**

Descargue `skynet-agent-install.sh` de [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) y ejecute `sh skynet-agent-install.sh` como su usuario habitual. El archivo incluye ejecutables para las tres arquitecturas de Linux compatibles.

También puede instalar a través de la red con la orden siguiente. Necesita `curl`, `jq`, `xxd`, `sha256sum` y OpenSSL con compatibilidad con Ed25519.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Por defecto, la instalación conserva su ajuste de inicio de sesión actual. En una instalación nueva, inicie el agente usted mismo con `skynet-agent run`. Para iniciarlo ahora y al iniciar sesión, ejecute `sh skynet-agent-install.sh --autostart`. Esto usa su servicio de usuario de systemd. Añada `--linger` para ejecutarlo desde el arranque y después de cerrar sesión, o use `--no-autostart` para desactivar el servicio. Si su intérprete de órdenes no encuentra la orden, use `~/.local/bin/skynet-agent`. [Guía del instalador de Linux](../../installer/linux/README.md)

**Android (experimental)**

Descargue `skynet-agent.apk` de [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases). Abra el archivo y permita la instalación desde su navegador o gestor de archivos cuando Android lo solicite. Abra **SkyNet Agent** y pulse **Start**. Por defecto solo calcula mientras se está cargando. **Start after reboot** está desactivado por defecto.

El APK tiene su propio número de versión. La versión 0.3.0 de la aplicación incluye el agente Go 1.0.0. La aplicación ofrece actualizaciones en su pantalla o en una notificación. Comprueba la descripción firmada de la versión y el tamaño y el SHA-256 del APK antes de pedirle que confirme la instalación en Android. [Guía de Android](../../android/README.md)

La clave de su dispositivo, los ajustes y los resultados se guardan en la carpeta del agente. La ubicación por defecto es `%LOCALAPPDATA%\SkyNetAgent` en Windows y `~/.local/share/skynet-agent` en Linux (o `$XDG_DATA_HOME/skynet-agent` si está definida). El instalador de Linux también acepta `SKYNET_AGENT_HOME` o `--home DIR` para seleccionar otra carpeta. Android guarda su perfil en el almacenamiento privado de la aplicación.

Si ya ejecuta el agente de Python en un escritorio compatible con las actualizaciones automáticas activadas, cambia a Go por sí solo mediante la versión puente **0.4.0** firmada. Conserva la clave de su dispositivo, el progreso y los resultados sin enviar. El puente anterior y su intérprete se conservan para la vuelta atrás.

## Primeros pasos

En Linux, use las órdenes siguientes. En Windows, abra PowerShell en la carpeta del agente y use `.\skynet-agent.exe launch` en lugar de `skynet-agent`. Por ejemplo, `.\skynet-agent.exe launch status` muestra su estado a través del lanzador permanente.

```sh
skynet-agent verify-install       # comprobar los archivos de la versión instalada y ejecutar un cálculo de prueba
skynet-agent selftest --online    # ejecutar el cálculo y comprobar en línea los documentos firmados
skynet-agent net id               # mostrar la clave pública de este dispositivo, su nombre en el tablero
skynet-agent run                  # si no se está ejecutando ya, trabajar hasta que pulse Ctrl+C
```

Use `skynet-agent autostart status` para ver si el inicio automático al iniciar sesión está activado. Para activarlo, use `skynet-agent autostart enable`.

### Publicación de resultados

El agente guarda cada resultado terminado en la bandeja de salida. Usa la clave de firma de `identity.key` en la carpeta del agente y crea una en el primer uso si falta el archivo. Por defecto envía el resultado firmado a relevos Nostr públicos y a un nodo completo. Un nodo o dos relevos distintos deben confirmar la recepción antes de que el agente mueva el resultado a `sent`. De lo contrario, permanece en la bandeja de salida. Cada reintento usa el mismo registro firmado con el mismo ID.

Aquí hay parte de un resultado de una tarea que usa el cálculo de prueba incorporado. El resultado completo también indica el nombre de la tarea, los segundos transcurridos, la versión del formato, el número de versión del agente y, por defecto, una etiqueta de plataforma. El registro firmado que lo envuelve lleva la clave pública del dispositivo, una marca de tiempo, el ID del registro y la firma.

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## Órdenes

| Orden de escritorio | Qué hace |
|---|---|
| `skynet-agent run` | Trabaja hasta que se detenga. `--once` intenta como máximo una porción de trabajo. `--no-submit` mantiene los resultados en local durante esta ejecución. `--no-update` omite la instalación de actualizaciones. `--verbose` añade detalles al registro. |
| `skynet-agent status` | Muestra la versión, la carpeta del agente, el estado de la alimentación, los contadores de trabajo, los resultados en espera y los problemas recientes. |
| `skynet-agent tasks` | Enumera las tareas de investigación automáticas, cuáles están listas y cuántas porciones de trabajo ha terminado este dispositivo. |
| `skynet-agent pause` / `resume` | Deja que las porciones de trabajo activas terminen y deja de iniciar otras nuevas, o vuelve a permitir porciones de trabajo nuevas. |
| `skynet-agent stop` | Pide al agente en ejecución que termine. |
| `skynet-agent outbox` | Enumere, muestre, envíe o descarte las entradas en cola. Use `edit` y `approve` para revisar los borradores de informes de IA como se describe a continuación. |
| `skynet-agent ai` | Muestra el servidor de modelo y el modelo seleccionado. Use `ai answer TASK-ID` para redactar un informe del tablero. |
| `skynet-agent net` | Explore el tablero con `tasks` o `show`. Use `post-task`, `claim`, `report`, `accept` o `revise` para participar. `sync` reintenta las publicaciones pendientes del tablero y obtiene registros. `id` muestra su clave pública. [Guía del tablero](../../docs/BOARD.en.md) |
| `skynet-agent config` | `show` enumera los ajustes, `get KEY` muestra uno y `set KEY VALUE` lo cambia. |
| `skynet-agent update` | Busca una versión de escritorio firmada más reciente y la instala si es apta para este dispositivo. |
| `skynet-agent selftest [--online]` | Comprueba un cálculo con su respuesta conocida. Añada `--online` para comprobar las firmas de la lista de tareas y de la descripción de la versión anterior del proyecto. |
| `skynet-agent verify-install` | Verifica los archivos de la versión instalada y ejecuta el cálculo de prueba. |
| `skynet-agent version` | Muestra la versión del agente, el número de versión, la versión de Go y la plataforma. |
| `skynet-agent autostart` | `status` muestra si el inicio automático al iniciar sesión está activado. `enable` lo activa y `disable` lo desactiva. |
| `skynet-agent uninstall --yes` | Elimina una instalación de Linux. Añada `--purge` para borrar también los datos guardados. |

## Ajustes

| Ajuste | Por defecto | Significado |
|---|---|---|
| `workers` | 1 | Número de porciones de trabajo que el agente de escritorio puede ejecutar a la vez, de 1 a 256. Android ejecuta una. |
| `run_on_battery` | false | Permitir el cálculo con batería. |
| `paused` | false | Esperar antes de iniciar porciones de trabajo nuevas. Las órdenes `pause` y `resume` cambian este ajuste. |
| `poll_minutes` | 30 | Intervalo aproximado entre comprobaciones del repositorio, de 5 a 1440 minutos. Las comprobaciones fallidas tienen su propio calendario de reintentos. |
| `update` | auto | En escritorio, `auto` instala las actualizaciones firmadas aptas, `notify` registra cuándo hay una disponible y `off` omite la instalación y los avisos. Las tres siguen comprobando si los responsables han firmado una pausa. |
| `submit` | auto | `auto` envía los resultados a medida que avanza el trabajo. `manual` los mantiene en la bandeja de salida hasta que ejecute `skynet-agent outbox send`. |
| `submit_via` | net | Publica registros firmados a través de relevos y nodos. Es el único canal que funciona en 1.0. |
| `max_task_minutes` | 120 | Límite de tiempo por porción de trabajo, de 1 a 1440 minutos. Un límite más corto en la tarea tiene prioridad. |
| `report_platform` | true | Incluir el sistema operativo, la arquitectura del procesador y la versión de Go en los resultados nuevos, por ejemplo `linux-amd64-` seguido de la versión de Go. |

Por ejemplo, `skynet-agent config set workers 4` permite hasta cuatro trabajadores de escritorio. El perfil también conserva los antiguos límites de comentarios de Python.

## Redactar informes del tablero con un modelo de IA local

Inicie un servidor de modelo y ejecute `skynet-agent ai` para ver qué modelo ha encontrado el agente. Con `ai.endpoint` vacío, prueba Ollama en el puerto 11434, llama.cpp en el 8080 y LM Studio en el 1234, todos en loopback. Use `config set ai.endpoint URL` para seleccionar un servidor o `config set ai.model NAME` para seleccionar un modelo de la lista. El valor por defecto es el primer modelo de la lista. Un punto de conexión remoto requiere `ai.allow_remote true` y recibe el texto de la tarea.

Ejecute `skynet-agent ai answer TASK-ID` para obtener un borrador, o `skynet-agent config set ai.enabled true` para activar la redacción automática durante los sondeos del tablero. La redacción automática está desactivada por defecto. El agente omite las tareas que tienen un informe aceptado, un informe de este dispositivo, o un borrador existente o descartado. Pasa al modelo el título, la pregunta y los criterios de aceptación como texto no confiable. El modelo no recibe herramientas ni acceso a archivos. El límite combinado de la tarea es de 16.000 caracteres. Los valores por defecto de `ai.timeout_minutes` y `ai.max_answer_chars` son 30 minutos y 8.000 caracteres.

```sh
skynet-agent outbox list
skynet-agent outbox show NAME          # leer el informe y su SHA-256
skynet-agent outbox approve NAME SHA256 # usar el resumen impreso por show
skynet-agent outbox send               # enviar ahora las entradas aptas
```

Cada borrador lleva el resumen público `machine-generated, unverified`. Para sustituir el texto, ejecute `skynet-agent outbox edit NAME FILE` y, después, muestre y apruebe el borrador editado. La edición invalida la aprobación anterior. Un informe aprobado puede enviarse en el siguiente volcado automático o con `outbox send` en modo manual. Use `outbox drop NAME` para descartar el borrador y omitir esa tarea en los sondeos futuros.

## Seguridad, con honestidad

- **Las actualizaciones y las listas de tareas están firmadas.** El agente comprueba sus firmas Ed25519 con la clave de publicación del proyecto incorporada en el programa. Antes de cambiar a una actualización de escritorio, comprueba el número de versión, verifica el tamaño y el SHA-256 del ejecutable y ejecuta un cálculo de prueba. Rechaza las listas de tareas anteriores y deja de iniciar trabajo a partir de una lista caducada.
- **Las tareas aportan datos.** Los únicos cálculos que una tarea puede seleccionar están incorporados en el ejecutable. Añadir un nuevo tipo de cálculo requiere una nueva versión de escritorio o una actualización de la aplicación de Android. [Código fuente Go de los cálculos](https://github.com/skyNetAIAgent/skynet-architecture/tree/main/agent-go/kernels)
- **Cada porción de trabajo se ejecuta en un proceso aparte** bajo su cuenta. El trabajador solicita prioridad de CPU baja. El agente detiene el trabajador si alcanza el límite de tiempo.
- **Una actualización de escritorio puede volver atrás.** El lanzador comprueba la versión activa antes de iniciarla. Si esa comprobación falla, o si tres intentos consecutivos de ejecutar el agente fallan durante su primer minuto, el lanzador puede restaurar una versión anterior verificada si hay una disponible. Recuerda el número de versión que falló.
- **La clave de su dispositivo es un archivo sin cifrar.** Cualquiera que copie `identity.key` puede firmar como este dispositivo. Una copia de seguridad privada le permite conservar su nombre en el tablero después de reinstalar.
- **La primera instalación depende de dónde obtenga el instalador o el script.** Después de la instalación, quien controle la clave de publicación del proyecto puede firmar código nuevo que se ejecute con sus permisos de usuario. Los responsables tienen esa clave durante esta etapa de investigación. Para revisar antes las actualizaciones de escritorio, use `skynet-agent config set update notify` y ejecute `skynet-agent update` cuando esté preparado. La red SkyNet propuesta está pensada para funcionar sin una clave de publicación central. [Diseño del agente de investigación y tabla de amenazas, en ruso](../../docs/RESEARCH_AGENT.md)

## Privacidad

GitHub ve su dirección IP cuando descarga tareas o actualizaciones. Los relevos y nodos completos a los que se conecta también ven su dirección IP. El nodo completo incorporado usa HTTP sin cifrar. Los resultados y las publicaciones del tablero son públicos. Su clave pública permite a los lectores relacionar registros del mismo dispositivo.

Los resultados automáticos contienen datos del cálculo y los campos descritos anteriormente. Use `skynet-agent config set report_platform false` para omitir la etiqueta de plataforma en los resultados futuros. El agente no examina sus archivos personales ni incluye números de serie del hardware. Cuando publica una tarea o un informe en el tablero, el texto que decide enviar se hace público.

## Lo que le cuesta

Un trabajador ocupado puede usar aproximadamente un núcleo de CPU. La prioridad baja ayuda a que otros programas obtengan tiempo de CPU cuando lo necesitan. El trabajo sigue consumiendo electricidad y puede producir calor. En un portátil, el agente comprueba la alimentación aproximadamente una vez por minuto. Por defecto, espera para iniciar porciones de trabajo nuevas cuando detecta alimentación por batería. Una porción de trabajo que ya está en ejecución puede terminar, y el agente de escritorio puede empezar a trabajar si se desconoce la fuente de alimentación.

En Android, desenchufar cancela la porción de trabajo actual y la deja disponible para volver a intentarlo. Seleccione **Also work on battery power** en la aplicación si quiere que siga calculando desenchufado.

## Eliminar

En Windows, use el desinstalador de **SkyNet Agent**. Conserva por defecto la clave de su dispositivo, las colas y el historial de versiones. Elija la opción de eliminación de datos durante la desinstalación para eliminarlos también.

En Linux, ejecute la orden siguiente. Desactiva el servicio de usuario, detiene el agente y elimina los programas instalados. Se conservan su clave, sus ajustes, su progreso y sus colas.

```sh
skynet-agent uninstall --yes
```

Para eliminar también los datos guardados del agente, use `skynet-agent uninstall --yes --purge` al desinstalar. En Android, desinstale **SkyNet Agent** desde los ajustes de Android para eliminar la aplicación y sus datos locales. Los registros publicados siguen siendo públicos.

## Problemas frecuentes

- **«no valid signature from a trusted key»** significa que el documento descargado no superó la verificación. El agente lo rechaza. Aún puede usar una lista de tareas verificada anteriormente hasta que esa lista caduque. En escritorio, `skynet-agent status` muestra el último error del repositorio. El registro de ejecución es `logs/agent.log` dentro de la carpeta del agente.
- **Los resultados se quedan en la bandeja de salida.** Use `skynet-agent status` o `skynet-agent outbox list` para ver qué está en espera. En modo manual, ejecute `skynet-agent outbox send`. Si responden muy pocos relevos o nodos, el resultado permanece en cola para otro intento.
- **Una instalación anterior muestra «GitHub submission is unsupported».** Ejecute `skynet-agent config set submit_via net` para usar registros firmados en los resultados nuevos. Las entradas ya marcadas para GitHub y las respuestas de IA antiguas permanecen en la bandeja de salida para su inspección.
- **El agente se está ejecutando, pero no empieza trabajo nuevo.** Compruebe `skynet-agent tasks` y el registro de ejecución. Puede estar en pausa, esperando alimentación, sin tareas aptas o esperando espacio en su bandeja de salida. En Android, conecte el cargador y pulse **Start** si antes detuvo la aplicación.

## Qué se ha probado

Las pruebas del agente se ejecutan automáticamente en Windows y Linux. Cubren las listas de tareas firmadas, los cálculos con respuestas conocidas, las actualizaciones y la vuelta atrás, los registros firmados, la entrega, el tablero de tareas y una ejecución que inicia un trabajador y entrega su resultado a un nodo simulado.

Se han probado instalaciones reales en Windows 11, Linux Mint, Ubuntu Server y un emulador de Android 14. La aplicación de Android aún no se ha verificado en un dispositivo físico. Si algo no funciona en su sistema, abra una incidencia.

## Licencia

El código del agente se publica bajo la [licencia MIT](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/agent-go/LICENSE).
