<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# Instalador de escritorio de Windows

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · **Español** · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Elija el instalador amd64 o arm64 para su computadora. Verifique su SHA-256 con una suma
de comprobación obtenida por un canal de confianza. El instalador instala la versión
nativa firmada en el perfil del usuario actual. El instalador inicia el agente de
inmediato y en cada inicio de sesión de Windows; ambas opciones se pueden desmarcar en
la página de tareas. Los accesos directos del menú Inicio invocan el lanzador permanente.

El desinstalador conserva la identidad, las colas y el historial de versiones de forma
predeterminada. Seleccione la opción de eliminación de datos para eliminarlos. Durante la
migración se conservan el puente de Python firmado anterior y su intérprete para la
reversión.

## Compilar y probar

Use Python 3.9+ e Inno Setup 6 en la máquina de compilación. Coloque el manifiesto de la
versión y la firma separada en `agent/v2` y los binarios de la versión correspondientes en
`dist`. Use un directorio de compilación nuevo. La prueba de humo necesita una cuenta de
Windows desechable.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
