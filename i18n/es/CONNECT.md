<!-- translation of docs/CONNECT.md, source sha256: bd3f9740a67100d72b7a87b5073daf071ecf7c9648582be1586e382d46869750 -->

# Cómo participar

[English](../../docs/CONNECT.md) · [中文](../zh/CONNECT.md) · **Español** · [Français](../fr/CONNECT.md) · [Deutsch](../de/CONNECT.md) · [Italiano](../it/CONNECT.md) · [Русский](../ru/CONNECT.md) · [Português](../pt/CONNECT.md) · [العربية](../ar/CONNECT.md)

Puede ayudar a diseñar SkyNet con su ordenador o su teléfono. El agente de investigación es un
pequeño programa de código abierto: recibe cálculos de investigación firmados, los ejecuta en el
tiempo libre de su dispositivo y publica los resultados. No hace falta una cuenta en ningún sitio.
**En esta etapa no hay recompensas**: es ayuda voluntaria para la investigación, no la propia red
SkyNet.

## Instalación

| Su dispositivo | Qué hacer |
|---|---|
| **Windows 10/11** (64 bits) | Descargue `SkyNetAgentSetup-<version>-amd64.exe` de la [última versión](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) y ejecútelo. Windows muestra «Windows protegió su PC» porque el archivo no tiene firma de código: elija **Más información** y luego **Ejecutar de todas formas**. |
| **Linux** (x86_64 o ARM64) | Descargue `skynet-agent-linux-install-<version>.sh` de la [última versión](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) y ejecute `sh skynet-agent-linux-install-<version>.sh`. |
| **Android 7.0+** (64 bits) | Descargue `skynet-agent.apk` de la página de versiones, ábralo y permita la instalación desde este origen. La aplicación solo funciona mientras el teléfono se está cargando. |

macOS e iPhone no son compatibles.

El instalador le pregunta si quiere iniciar el agente ahora y al iniciar sesión. Después no hay nada
más que hacer: el agente se actualiza solo (únicamente a versiones firmadas por el proyecto), toma
tareas y publica resultados por su cuenta.

## Qué usa y qué no hace nunca

- Un núcleo del procesador con la prioridad más baja por defecto, para que sus propios programas no
  vayan más lentos. En un portátil no trabaja con batería a menos que usted lo permita.
- Nunca ejecuta código que venga de una tarea, nunca envía sus archivos y no necesita derechos de
  administrador. Cada resultado es un pequeño registro público firmado con la clave de su propio
  dispositivo.
- Para pausar o detener: la carpeta **SkyNet Agent** del menú Inicio en Windows,
  `skynet-agent pause` / `stop` en Linux, el botón **Detener** de la aplicación.
- Para eliminarlo: **SkyNet Agent → Desinstalar** en Windows, `skynet-agent uninstall --yes` en Linux,
  desinstale la aplicación en Android.

Detalles: [la guía del agente](AGENT.md).

## Ayude con ideas, no solo con computación

El principal problema abierto del proyecto es cómo comprobar los cálculos para que hacer trampas
nunca sea rentable, de forma barata y sin depósitos ni multas. Si usted, o su asistente de IA, tiene
una idea o ha encontrado un fallo, consulte el [tablero de tareas](BOARD.md), la
[hoja de ruta](ROADMAP.md) y las [preguntas abiertas](OPEN_QUESTIONS.md).
