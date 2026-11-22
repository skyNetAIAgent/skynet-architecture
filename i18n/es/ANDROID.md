<!-- translation of android/README.md, source sha256: dd56c64ec3931fa625cd383ec84dcdb5618d80f9faca47d3c9a52cd30294927e -->

# Agente de investigación de SkyNet para Android (experimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · **Español** · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Una aplicación de Android que incluye el mismo [agente de investigación](../../agent/README.md) que la
versión de escritorio. Es para quienes no quieren configurar Termux: instale un archivo y pulse
Iniciar. En esta etapa no se ofrecen recompensas.

**Estado: experimental.** El 22 de noviembre de 2026 la aplicación se comprobó en un emulador de
Android 14 (x86_64) contra un repositorio de prueba local firmado con una clave de prueba: se
instaló, arrancó, comprobó las firmas, calculó sin errores las 7 unidades de las tareas de prueba,
esperó mientras el emulador estaba desconectado del cargador, siguió trabajando en segundo plano,
guardó un token y llegó con él a la API real de GitHub, y se detuvo y volvió a arrancar conservando
su estado. Una compilación solo para ARM (`arm64-v8a`) hizo lo mismo en ese emulador mediante su
traducción de ARM. Su parte de Python también supera las pruebas en un ordenador. **Aún no se ha
verificado en un teléfono real**, ni en Android 7–13, ni en ejecuciones largas, ni frente a los
ahorradores de batería de los fabricantes de teléfonos. Ejecutar el agente en
[Termux](../../agent/README.md#install) sigue siendo la otra forma.

## Para participantes

1. Descargue `skynet-agent.apk` de la página
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Abra el archivo. Android le pide que permita instalar aplicaciones desde su navegador o gestor
   de archivos.
3. Abra «SkyNet Agent» y pulse **Iniciar**. Una notificación permanente muestra que está en
   funcionamiento.

Qué debe saber:

- Solo funciona mientras el dispositivo se está cargando, salvo que marque «Trabajar también con
  batería». El cargador se comprueba entre porciones de trabajo: una porción ya iniciada
  (normalmente de menos de un minuto) se termina aunque desconecte el dispositivo.
- No se inicia por sí sola tras reiniciarse el dispositivo: abra la aplicación y pulse Iniciar de
  nuevo.
- En Android 13 y posterior, si rechaza las notificaciones, la aplicación sigue funcionando;
  Android la muestra entonces solo en la lista de aplicaciones en ejecución.
- Para publicar resultados necesita un token de GitHub: en GitHub abra Configuración →
  Configuración de desarrollador → Tokens de acceso personal, cree un token que pueda escribir
  incidencias de repositorios públicos y péguelo en la aplicación. El token se guarda solo dentro
  de la aplicación. Sin token, los resultados esperan en el dispositivo (hasta 300; después, la
  aplicación deja de calcular).
- Android 7.0 o posterior, un dispositivo de 64 bits, unos 40 MB.
- El modo de IA opcional no está disponible en la aplicación.
- Para eliminarla, desinstale la aplicación; no queda nada más en el dispositivo.

## En qué se diferencia del agente de escritorio

| | Escritorio | Aplicación de Android |
|---|---|---|
| Código del agente | `agent/skynet_agent` | el mismo paquete, incorporado al APK |
| Trabajo | procesos separados de baja prioridad | una unidad cada vez dentro del proceso en segundo plano de la aplicación |
| Límite de tiempo | se mata el proceso de trabajo | un vigilante termina el proceso en segundo plano; Android lo reinicia y la tarea se deja para dispositivos más rápidos |
| Actualizaciones del agente | versión firmada del repositorio | la misma versión firmada, comprobada por el código incorporado al APK: la firma, cada archivo, ningún archivo fuera de la lista firmada, nunca por debajo de la versión más alta que ya funcionó aquí. Una versión nueva tiene tres intentos de llegar al repositorio; si no, la aplicación vuelve al código incorporado |
| La propia aplicación | lanzador e instalador | cambia solo con un APK nuevo |
| Publicación | inicio de sesión con GitHub CLI | un token pegado en la aplicación |

Límites honestos. El APK está firmado con una clave en poder de los mantenedores del proyecto; Android acepta
una actualización de la aplicación solo si está firmada con la misma clave. La clave de publicación
(para el código del agente y las listas de tareas) y esta clave del APK son dos puntos únicos de
confianza que la red SkyNet objetivo no debe tener. La aplicación carga código Python firmado en
tiempo de ejecución, algo que las normas de Google Play no permiten, por lo que se distribuye como
archivo.

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

La parte de Python de la aplicación es
[`app/src/main/python/skynet_android.py`](../../android/app/src/main/python/skynet_android.py). Se prueba en un
ordenador con [`agent/tests/test_android_glue.py`](../../agent/tests/test_android_glue.py). Python se
integra con [Chaquopy](https://chaquo.com/chaquopy/) (licencia MIT).

## Licencia

MIT, igual que el agente: [agent/LICENSE](../../agent/LICENSE).
