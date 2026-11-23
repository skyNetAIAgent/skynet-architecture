<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# Instalador de Windows x64

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · **Español** · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Descargue el EXE y el archivo `.exe.sha256` correspondiente de la misma versión del
proyecto. En PowerShell, abra la carpeta de descargas y compare la suma de comprobación.
[Versiones de GitHub](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

Abra el EXE verificado. SmartScreen puede mostrar **Windows protegió su PC** porque el
instalador no tiene firma de código. Elija **Más información**, confirme el nombre del
archivo y elija **Ejecutar de todas formas**. La instalación se hace para el usuario
actual. Desmarque cualquiera de las casillas de inicio automático para cambiar cuándo se
ejecuta el agente.

El agente acepta actualizaciones firmadas de sus propios archivos. Un instalador más
reciente actualiza el Python incluido. Instale encima de la copia existente para conservar
la identidad del dispositivo y los resultados en espera. El desinstalador del menú Inicio
también los conserva de forma predeterminada. Su casilla opcional de eliminación de datos
incluye la bandeja de salida y los registros firmados pendientes.

## Compilar y probar

Use una copia de trabajo limpia con finales de línea LF para los archivos firmados. Desde
la raíz del repositorio en Windows x64, ejecute PowerShell 7 con un directorio de
compilación nuevo. La compilación comprueba si Inno Setup 6.3.3 o posterior está en PATH
o en su ubicación habitual. Si falta el compilador, usa Chocolatey para instalar 6.3.3.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

`python.lock` debe contener la versión de parche 3.12 exacta y el SHA-256 de 64 dígitos
de su `python-<version>-embed-amd64.zip` oficial. Para fijar una versión nueva, autentique
el archivo con las instrucciones y el paquete Sigstore enlazados desde la página de la
versión de Python y anote después su SHA-256. Si la versión fijada está vacía o no es
válida, la compilación se detiene antes de la descarga. [Versión de Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

La compilación verifica el archivo antes de extraerlo. El intérprete incorporado solo
prepara archivos del manifiesto de la versión autenticada. En el momento de la instalación
vuelve a comprobar el paquete, incluida su lista de archivos, antes de ejecutar el
candidato. El archivo `python312._pth` sin modificar proporciona la biblioteca estándar. El
lanzador y la comprobación del candidato añaden el directorio de la versión seleccionada
a `sys.path` con `-I`.

En un perfil de Windows desechable sin ninguna instalación de SkyNet, ejecute la prueba de
humo. La prueba instala en silencio, comprueba el registro de inicio de sesión y la CLI sin
Python del sistema en PATH; después desinstala y comprueba los datos conservados.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

Como alternativa, ejecute **Actions → Windows installer → Ejecutar flujo de trabajo (Run workflow)**.
Cuando la prueba de humo pase, descargue el artefacto `SkyNetAgentSetup-x64`.
Su `SkyNetAgentSetup-<version>.exe` y su `.exe.sha256` son los dos archivos que hay que
adjuntar a mano a la versión correspondiente de GitHub.
