<!-- translation of android/README.md, source sha256: 3fd07398dc6f1c3ed1d7c21b1315b13e43cdbf629cf72aab3887e8ebbd602e2b -->

# Agente de investigación de SkyNet para Android (experimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · **Español** · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Una aplicación de Android que incluye el mismo [agente de investigación](../../agent/README.md) que la
versión de escritorio. Instale un archivo y pulse Iniciar. De forma predeterminada, el agente firma
cada resultado en el dispositivo y lo publica sin cuenta ni token.
En esta etapa no se ofrecen recompensas.

**Experimental.** El shell anterior se probó en un emulador de Android 14 el 22 de noviembre de
2026. Completó las siete unidades de prueba, esperó mientras se cargaba y conservó su estado entre
detenciones y arranques. El shell 0.2.0 incluye el agente 0.2.2. Sus flujos de instalación y
reinicio todavía deben probarse en Android.

## Para participantes

1. Descargue `skynet-agent.apk` de la página
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Abra el archivo. Android le pide que permita instalar aplicaciones desde su navegador o gestor
   de archivos.
3. Abra «SkyNet Agent» y pulse **Iniciar**. Una notificación permanente muestra que está en
   funcionamiento.

- Solo funciona mientras el dispositivo se está cargando, salvo que marque «Trabajar también con
  batería». El cargador se comprueba entre porciones de trabajo: una porción ya iniciada
  (normalmente de menos de un minuto) se termina aunque desconecte el dispositivo.
- Para reanudar tras reiniciar el dispositivo, active **Iniciar tras reiniciar**. Está desactivada
  de forma predeterminada. Pulsar **Detener** mantiene el agente detenido tras un reinicio.
- En Android 13 y posterior, si rechaza las notificaciones, la aplicación sigue funcionando;
  Android la muestra entonces solo en la lista de aplicaciones en ejecución.
- Los usuarios avanzados que seleccionen `submit_via=github` pueden introducir un token de GitHub
  en la pantalla principal.
- Android 7.0 o posterior, un dispositivo de 64 bits, unos 40 MB.
- El modo de IA opcional no está disponible en la aplicación.
- Para eliminarla, desinstale la aplicación; no queda nada más en el dispositivo.

## Actualizar la aplicación

Si tiene la versión 0.1.0, instale la 0.2.0 desde Releases sobre la aplicación existente para
conservar sus ajustes y los resultados en cola. A partir de la 0.2.0, al abrir la pantalla se
comprueba si hay un APK nuevo. Android también programa una comprobación diaria cuando hay una red
disponible, incluso si el agente está detenido. Las restricciones de batería pueden retrasar esa
comprobación.

La aplicación comprueba el manifiesto firmado de la versión con la clave incorporada al APK. Para
una versión compatible más reciente, descarga el archivo de la versión en la caché privada y
comprueba su tamaño y su SHA-256. Pulse el botón de actualización o la notificación para
instalarla. En Android 8 y posterior, permita la instalación desde SkyNet Agent si se le pide,
vuelva a la aplicación y confirme en el instalador de Android. Con las notificaciones desactivadas,
use el botón de la pantalla principal.

## En qué se diferencia del agente de escritorio

| | Escritorio | Aplicación de Android |
|---|---|---|
| Código del agente | `agent/skynet_agent` | el mismo paquete, incorporado al APK |
| Trabajo | procesos separados de baja prioridad | una unidad cada vez dentro del proceso en segundo plano de la aplicación |
| Límite de tiempo | se mata el proceso de trabajo | un vigilante termina el proceso en segundo plano; Android lo reinicia y la tarea se deja para dispositivos más rápidos |
| Actualizaciones del agente | versión firmada del repositorio | el APK comprueba los archivos firmados y el número de versión. Un agente nuevo dispone de tres arranques para superar una autocomprobación local y completar un paso del bucle |
| La propia aplicación | lanzador e instalador | un APK verificado instalado con su confirmación |
| Publicación | registros firmados de forma predeterminada | registros firmados de forma predeterminada |

Límites honestos. El APK está firmado con una clave en poder de los mantenedores del proyecto;
Android acepta una actualización de la aplicación solo si está firmada con la misma clave. La clave
de publicación (para el código del agente y las listas de tareas) y esta clave del APK son dos
puntos únicos de confianza que la red SkyNet objetivo no debe tener. La aplicación carga código
Python firmado en tiempo de ejecución, algo que las normas de Google Play no permiten, por lo que
se distribuye como archivo.

## Compílela usted mismo

Necesita JDK 17, el Android SDK (plataforma 34, build-tools 34), Gradle 8.7 y Python 3.12 en el
ordenador de compilación.

```sh
cd android
gradle assembleRelease
```

El resultado es `app/build/outputs/apk/release/app-release-unsigned.apk`. Fírmelo con su propia
clave (`zipalign` y después `apksigner sign`) antes de instalarlo. Un APK que firme usted mismo no
puede instalarse encima del del proyecto, y viceversa.

Compile la aplicación solo a partir de una confirmación en la que `agent/skynet_agent/trust.py`
contenga la clave de publicación: un agente sin clave de publicación no acepta tareas. La compilación
de versión se detiene con un error en ese caso; `-PallowNoReleaseKey` compila igualmente un APK así,
solo para pruebas.

El puente del agente y el verificador del APK tienen pruebas de Python independientes en el
ordenador.
[Pruebas del agente](../../agent/tests/test_android_glue.py) · [Pruebas de actualización del APK](../../agent/tests/test_apk_update.py)
Python se integra con [Chaquopy](https://chaquo.com/chaquopy/) (licencia MIT).

## Licencia

MIT, igual que el agente: [agent/LICENSE](../../agent/LICENSE).
