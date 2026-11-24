<!-- translation of android/README.md, source sha256: f39e5a1b5b61d6be25ac07b2c69e9f4af5a9bca2ee2ff7cb9610398aebe13e0c -->

# Agente de investigación de SkyNet para Android (experimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · **Español** · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Una aplicación de Android que lleva los mismos [kernels de cálculo en Go](../../agent-go/README.md) que la
versión de escritorio. Instale un archivo y pulse Iniciar. De forma predeterminada, el agente firma
cada resultado en el dispositivo y lo publica sin cuenta ni token.
En esta etapa no se ofrecen recompensas.

**Experimental.** El shell 0.3.0 incluye el agente Go 1.0.0 (versión 7 del motor) en el APK. La
instalación sobre la 0.2.0, el ciclo de vida del servicio y el reinicio aún deben probarse en Android.

## Para participantes

1. Descargue `skynet-agent.apk` de la página
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Abra el archivo. Android le pide que permita instalar aplicaciones desde su navegador o gestor
   de archivos.
3. Abra «SkyNet Agent» y pulse **Iniciar**. Una notificación permanente muestra que está en
   funcionamiento.

- Solo funciona mientras el dispositivo se está cargando, salvo que marque «Trabajar también con
  batería». Desenchufar el dispositivo cancela la unidad actual y la deja disponible para una
  ejecución posterior.
- Una vez que pulse **Iniciar**, el agente también se inicia de nuevo tras reiniciar el dispositivo
  (**Iniciar tras reiniciar** está activada de forma predeterminada; desmárquela para desactivar esta
  opción). Pulsar **Detener** mantiene el agente detenido tras un reinicio.
- En Android 13 y posterior, si rechaza las notificaciones, la aplicación sigue funcionando;
  Android la muestra entonces solo en la lista de aplicaciones en ejecución.
- Si un perfil existente usa `submit_via=github`, sus resultados permanecen en cola. Esta versión
  admite la publicación mediante registros de red firmados.
- Android 7.0 o posterior en arm64-v8a o x86_64.
- El modo de IA opcional no está disponible en la aplicación.
- Para eliminarla, desinstale la aplicación; no queda nada más en el dispositivo.

## Actualizar la aplicación

Instale la 0.3.0 sobre la aplicación existente con la misma firma de paquete para conservar la
identidad de su dispositivo, los ajustes, el progreso y los resultados en cola. A partir de la 0.2.0, al abrir la pantalla se
comprueba si hay un APK nuevo. Android también programa una comprobación diaria cuando hay una red
disponible, incluso si el agente está detenido. Las restricciones de batería pueden retrasar esa
comprobación.

La aplicación comprueba el manifiesto firmado de la versión con la clave incorporada al APK. Para
una versión compatible más reciente, descarga el archivo de la versión en la caché privada y
comprueba su tamaño y su SHA-256. Pulse el botón de actualización o la notificación para
instalarla. En Android 8 y posterior, permita la instalación desde SkyNet Agent si se le pide,
vuelva a la aplicación y confirme en el instalador de Android. Con las notificaciones desactivadas,
use el botón de la pantalla principal.

## El agente y las actualizaciones

El servicio en primer plano inicia el ejecutable extraído en el directorio de bibliotecas nativas.
Ejecuta un trabajador de baja prioridad cada vez y mantiene un wake lock durante el cálculo. Un
trabajador que agota el tiempo de espera se detiene y el agente omite temporalmente esa tarea. Las
tareas nuevas llegan a través del índice de tareas firmado. El código ejecutable nuevo llega con una
actualización de la aplicación.

Android comprueba el certificado de firma del APK durante la instalación. La clave de publicación
separada autentica el índice de tareas y el manifiesto de descarga del APK. La aplicación comprueba
el tamaño, el SHA-256, el nombre del paquete y el código de versión del APK antes de abrir el
instalador.

## Compílela usted mismo

En Linux, instale Go 1.27.4 con las fuentes, Bash, GNU patch, coreutils, file y readelf (binutils).
Para compilar el APK también necesita JDK 17, Gradle 8.7 y Android SDK 34.

```sh
cd android
gradle assembleRelease
```

Gradle invoca `./build-go.sh`. Ejecute ese script directamente para compilar solo los dos
ejecutables `app/src/main/jniLibs/<abi>/libskynet.so`. Usa `GOOS=android`,
`CGO_ENABLED=0` y PIE para ambas ABI. La compilación para arm64 usa el Go estándar. Para la
compilación del emulador x86_64, el script habilita la vinculación interna en una copia temporal de
las herramientas de compilación del host de Go 1.27.4. Comprueba la arquitectura, el punto de
entrada y el intérprete `/system/bin/linker64` antes de instalar cualquiera de los dos archivos.

El APK de versión es `app/build/outputs/apk/release/app-release-unsigned.apk`. Use
`zipalign` y después `apksigner sign` con la misma clave que el APK anterior para las
actualizaciones in situ. Genere y firme `android/latest.json` a partir del APK firmado final con
`tools/make_apk_manifest.py`.

## Licencia

MIT, igual que el agente: [agent/LICENSE](../../agent/LICENSE).
