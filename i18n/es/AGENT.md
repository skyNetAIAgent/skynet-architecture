# Agente de investigación de SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · **Español** · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Traducción de [agent/README.md](../../agent/README.md). Cómo funciona el mecanismo y cuáles son sus límites: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (en ruso).

No hace falta un asistente de IA para ayudar a diseñar SkyNet. El agente de investigación es un pequeño programa de código abierto. Consulta periódicamente este repositorio, toma tareas de investigación, las calcula en su ordenador en los ratos libres y publica los resultados.

**En esta etapa no hay recompensas**: ni créditos, ni dinero, ni promesas de pagos futuros. Es una ayuda voluntaria a la investigación. El agente no es la red SkyNet; es una herramienta para diseñarla.

## Qué hace y qué no hace nunca

| Hace | No hace nunca |
|---|---|
| Lee del repositorio la lista de tareas firmada y la descripción firmada de la versión | Ejecutar código que venga de una tarea. Una tarea es el nombre de un cálculo incorporado más unos números |
| Ejecuta cálculos incorporados con la prioridad de CPU más baja, de uno en uno por defecto | Trabajar con batería, salvo que usted lo permita |
| Publica cada resultado como comentario en GitHub con su propia cuenta | Enviar sus archivos, identificadores de hardware ni nada más de su ordenador |
| Se actualiza solo, pero únicamente a una versión firmada con la clave de publicación del proyecto | Instalar una actualización con firma incorrecta, huella de archivo incorrecta o número anterior |
| Guarda todo en una sola carpeta de su perfil | Necesitar derechos de administrador ni arrancar solo si usted no activa el inicio automático |

Las primeras tareas son cálculos exactos sobre las reglas de pago de SkyNet. Por ejemplo: «¿puede un participante que abandona la red ganar con una tanda de resultados falsos, y a partir de qué proporción de verificadores en colusión?». Todos los dispositivos deben obtener las mismas cifras, y los resultados de distintas personas se comparan. Véase [tasks/README.md](../../tasks/README.md).

## Requisitos

- Python 3.9 o posterior. Nada más: el agente usa solo la biblioteca estándar de Python.
- Una cuenta de GitHub para publicar resultados (gratuita). Sin ella también puede calcular y publicar a mano mediante un enlace.
- Unos pocos megabytes de disco y conexión a internet.

## Instalación

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux y macOS** (terminal):

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, la aplicación (experimental)**: descargue `skynet-agent.apk` de la página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases), permita a su navegador instalar aplicaciones y abra el archivo. La aplicación solo trabaja mientras el dispositivo se está cargando; los resultados se publican con un token de GitHub que usted pega en la aplicación. Aún no verificada en un dispositivo real. Código fuente y detalles: [android/README.md](../../android/README.md).

**Android**: instale la aplicación [Termux](https://termux.dev) desde F-Droid, ábrala y ejecute:

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

En un teléfono el agente solo trabaja mientras el teléfono se está cargando. Si no puede saber si se está cargando, espera y lo indica; en ese caso instale la aplicación Termux:API junto con `pkg install termux-api`, o permita el uso de la batería: `skynet-agent config set run_on_battery true`.

Si prefiere leer antes de ejecutar: descargue [`install.py`](../../agent/install.py), léalo (es corto) y ejecute `python3 -I install.py`.

El instalador coloca el agente en una carpeta (`%LOCALAPPDATA%\SkyNetAgent` en Windows, `~/Library/Application Support/SkyNetAgent` en macOS, `~/.local/share/skynet-agent` en Linux y Android) y crea la orden `skynet-agent`. No arranca nada.

## Primeros pasos

```sh
skynet-agent selftest --online    # comprobar el dispositivo y las firmas
skynet-agent github               # ver con qué cuenta de GitHub se publicarán los resultados
skynet-agent run                  # trabajar hasta que pulse Ctrl+C
skynet-agent autostart enable     # opcional: arrancar al iniciar sesión
```

En Windows la orden es el archivo `skynet-agent.cmd` de la carpeta del agente; el instalador muestra la línea exacta.

### Publicación de resultados

Los resultados son comentarios en la incidencia de seguimiento de la tarea en este repositorio, publicados desde su propia cuenta de GitHub. La forma más sencilla de iniciar sesión es la herramienta de línea de órdenes de GitHub:

1. Instale [GitHub CLI](https://cli.github.com) (`winget install GitHub.cli`, `brew install gh`, `pkg install gh` en Termux o el gestor de paquetes de su Linux).
2. Ejecute `gh auth login` y siga las instrucciones en el navegador.
3. Ejecute `skynet-agent github`. Muestra el nombre de la cuenta.

El agente pide el acceso a `gh` cuando lo necesita y no guarda contraseñas ni tokens. Alternativas: poner un token en la variable de entorno `SKYNET_GITHUB_TOKEN`, o publicar a mano: `skynet-agent outbox link` muestra enlaces que abren una página de GitHub ya rellenada donde solo hay que pulsar un botón.

Para que las incidencias sigan siendo legibles, los resultados de una tarea se publican juntos: como mucho un comentario por hora, con varios resultados cada uno.

Un resultado publicado tiene este aspecto y no contiene nada más:

```json
{"agent":"0.1.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## Órdenes

| Orden | Qué hace |
|---|---|
| `skynet-agent run` | Trabaja hasta que se detenga. `--once` hace una porción de trabajo y termina |
| `skynet-agent status` | Versión, ajustes, contadores, resultados en espera, último problema |
| `skynet-agent tasks` | Las tareas publicadas ahora y lo que ha hecho este dispositivo |
| `skynet-agent pause` / `resume` | Dejar de tomar tareas nuevas / volver a tomarlas |
| `skynet-agent stop` | Pedir al agente en ejecución que termine |
| `skynet-agent outbox` | Resultados pendientes de publicar (`list`, `show`, `send`, `link`, `approve`, `drop`) |
| `skynet-agent config show` / `set CLAVE VALOR` | Ajustes |
| `skynet-agent update` | Instalar ahora la versión firmada más reciente |
| `skynet-agent selftest [--online]` | Comprobar el dispositivo, los archivos instalados y las firmas |
| `skynet-agent autostart enable` / `disable` | Arrancar al iniciar sesión, o no |
| `skynet-agent uninstall --yes` | Desactivar el inicio automático y detenerse; después borre la carpeta del agente |

## Ajustes

| Ajuste | Por defecto | Significado |
|---|---|---|
| `workers` | 1 | Tareas simultáneas; cada una usa aproximadamente un núcleo de CPU |
| `run_on_battery` | false | Trabajar con batería |
| `poll_minutes` | 30 | Cada cuánto se consulta el repositorio |
| `update` | auto | `auto` instala actualizaciones firmadas, `notify` solo avisa, `off` las ignora. Una pausa pedida por los responsables se aplica en cualquier modo |
| `submit` | auto | `auto` publica los resultados, `manual` los deja en la bandeja de salida |
| `max_task_minutes` | 120 | Lo máximo que puede durar una porción de trabajo |
| `batch_minutes` | 60 | Los resultados de una tarea se publican juntos, como mucho un comentario cada tantos minutos |
| `max_submissions_per_day` | 48 | Máximo de comentarios publicados al día desde este dispositivo |
| `report_platform` | true | Añadir a los resultados una etiqueta aproximada como `windows-amd64-py3.12` |
| `ai.enabled` | false | Modo de IA opcional, véase abajo |

Ejemplo: `skynet-agent config set workers 4`.

## Opcional: responder preguntas de investigación con su propio modelo local de IA

Si ejecuta un modelo abierto en su ordenador (por ejemplo con Ollama, el servidor de llama.cpp o LM Studio), el agente puede pasarle preguntas de investigación de la lista de tareas y publicar las respuestas. Está desactivado por defecto y es experimental.

```sh
skynet-agent ai                               # muestra el servidor local y el modelo que usaría
skynet-agent config set ai.enabled true
```

- El agente no descarga ni arranca ningún modelo. Solo habla con un servidor de su propio ordenador, salvo que active `ai.allow_remote`.
- La pregunta y los documentos que cita vienen de la lista de tareas firmada; cada documento se comprueba con su huella antes de que el modelo lo vea.
- Cada respuesta espera en la bandeja de salida hasta que usted la mire: `skynet-agent outbox show NOMBRE` y después `skynet-agent outbox approve NOMBRE`. Para publicar sin revisión: `skynet-agent config set ai.review_before_submit false`.
- Las respuestas se publican como generadas por máquina y sin verificar.

## Seguridad, con honestidad

- **Las actualizaciones y las listas de tareas están firmadas** (Ed25519). El agente solo las acepta si la firma corresponde a una clave de publicación incorporada en la copia instalada, el número de versión es mayor que el actual y cada archivo coincide con su SHA-256. Un espejo o una mala conexión no cambian esto.
- **Las tareas son datos, no programas.** Los nuevos tipos de cálculo llegan solo dentro de una versión firmada, como código Python legible en [`skynet_agent/kernels`](../../agent/skynet_agent/kernels).
- **El agente se ejecuta en el modo aislado de Python**, y cada porción de trabajo va en un proceso aparte de baja prioridad con límite de tiempo.
- **Si una versión nueva no arranca**, el lanzador vuelve a la anterior y recuerda no instalar esa versión otra vez.
- **En qué hay que confiar.** Quien tenga la clave de publicación puede enviar código a todos los agentes instalados. En esta etapa de investigación la clave la tienen los responsables del proyecto. Si no quiere actualizaciones automáticas, ejecute `skynet-agent config set update notify` y actualice a mano tras leer los cambios. La primera instalación confía en la conexión HTTPS con GitHub. La red SkyNet objetivo no debe tener una clave así; este agente es una herramienta de investigación y todavía no cumple los requisitos de SkyNet. Detalles y tabla de amenazas: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (en ruso).

## Privacidad

El agente solo contacta con GitHub: descarga archivos públicos de este repositorio (GitHub ve su dirección IP, como en cualquier visita) y, si ha iniciado sesión, publica resultados con su cuenta. Un resultado contiene el nombre de la tarea, el número de porción, las cifras calculadas, cuánto tardó y, salvo que desactive `report_platform`, una etiqueta aproximada de plataforma. No se recoge nada sobre sus archivos, su red ni su hardware.

## Lo que le cuesta

La electricidad de un núcleo de CPU ocupado por defecto, con la prioridad más baja, de modo que los demás programas no se ralentizan. En un teléfono no se usa la batería salvo que usted lo permita; manténgalo enchufado.

## Desinstalar

```sh
skynet-agent uninstall --yes
```

Después borre la carpeta del agente. No se cambió nada más en su ordenador.

## Problemas frecuentes

- **«no valid signature from a trusted release key»**: el archivo descargado no es el que firmaron los responsables. El agente lo rechaza y sigue trabajando con lo que tiene. Si se repite durante días, mire las incidencias del repositorio.
- **`CERTIFICATE_VERIFY_FAILED` en macOS** con Python de python.org: el agente prueba entonces por sí mismo con el archivo de certificados del sistema. Si el error continúa, ejecute el `Install Certificates.command` que viene con ese Python.
- **Python de Microsoft Store (Windows)** trabaja con una copia privada de `AppData` y del registro. Con él la carpeta del agente es `SkyNetAgent` dentro de su carpeta de perfil, y el inicio automático hay que añadirlo a mano: `skynet-agent autostart enable` explica cómo. Aún no verificado en un dispositivo real.
- **Los resultados se quedan en la bandeja de salida**: ejecute `skynet-agent github`; normalmente falta `gh auth login`.
- **Android detiene el agente en segundo plano**: ejecute `termux-wake-lock` en Termux y excluya Termux de la optimización de batería.

## Qué se ha probado

El conjunto de pruebas ([`tests/`](../../agent/tests)) cubre firmas, actualizaciones, vuelta atrás, tareas, publicación y un recorrido completo, y se ejecuta automáticamente en Windows, Linux y macOS con cada cambio (pestaña Actions del repositorio). A mano se ha verificado en Windows 11. Aún no se ha verificado en un dispositivo real: Android (Termux) y el inicio automático en macOS, Linux y Android. Si algo no funciona en su sistema, abra una incidencia.

## Licencia

El código del agente se publica bajo la [licencia MIT](../../agent/LICENSE).
