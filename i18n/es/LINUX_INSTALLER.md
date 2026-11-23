<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# Instalador de Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · **Español** · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Ejecute el único archivo de la página Releases del proyecto con su propia cuenta.

```sh
sh skynet-agent-install.sh
```

El archivo contiene la versión firmada del agente. La instalación comprueba sin conexión su firma Ed25519 y las huellas de los archivos. Si Python 3.9 o posterior está en su PATH, la instalación usa ese intérprete. Si no, necesita una compilación fijada de CPython con glibc para x86_64 o aarch64. **Ahora mismo faltan las dos huellas. Esta compilación requiere el Python del sistema.**

El instalador en línea usa el mismo procedimiento de instalación. Con una fijación verificada, puede descargar el entorno de ejecución correspondiente de python-build-standalone y comprobar su SHA-256 antes de extraerlo. Los intérpretes portátiles se guardan en `$XDG_DATA_HOME/skynet-agent/python/<sha256>`, normalmente `~/.local/share/skynet-agent/python/<sha256>`. La orden de `~/.local/bin` y el servicio de usuario de systemd usan el ejecutable elegido.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## Iniciar y eliminar

En un terminal, si pulsa Intro en la primera pregunta, el servicio se inicia ahora y al iniciar sesión. Si pulsa Intro en la segunda, el servicio queda ligado a las sesiones de inicio de sesión. Sin terminal, la instalación omite las preguntas. Estas órdenes hacen la elección de forma explícita.

```sh
sh skynet-agent-install.sh --autostart           # Run now and at sign-in
sh skynet-agent-install.sh --autostart --linger  # Also run before login and after logout
sh skynet-agent-install.sh --no-autostart        # Install for manual use
```

El servicio necesita un gestor de usuario de systemd en ejecución. El componente firmado 0.2.2 que crea el servicio admite rutas con espacios. La instalación pide que se inicie a mano si la ruta de un intérprete o del agente contiene comillas dobles, una barra invertida, un signo de dólar, un signo de porcentaje o un salto de línea. Si la política local deniega la persistencia de sesión, la instalación lo indica y el servicio sigue funcionando durante las sesiones de inicio de sesión. La persistencia de sesión para toda la cuenta se puede cambiar aparte con `loginctl disable-linger "$(id -un)"`. Para una instalación manual, empiece a trabajar con `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

La eliminación desactiva el servicio, pide que se detenga y espera el bloqueo del agente. Su clave de identidad, la bandeja de salida, los registros de relevo pendientes y los ajustes se quedan en la carpeta del agente para volver a instalarlo. Para borrar también los datos guardados del agente, use `uninstall --yes --purge`. La persistencia de sesión es un ajuste de toda la cuenta y se mantiene después de eliminar el agente.

## Compilar y verificar

Desde la raíz del repositorio, use Python 3.9 o posterior en el equipo de compilación.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

El generador autentica la versión con la clave pública de `agent/install.py` y produce `installer/linux/skynet-agent-install.sh`. Para habilitar Python portátil, verifique cada archivo de origen por separado y anote su SHA-256 en `python.lock` (un campo por línea). Solo para una entrada nula, la integración continua puede aportar una huella verificada mediante `SKYNET_PYTHON_SHA256_X86_64` o `SKYNET_PYTHON_SHA256_AARCH64`. Son ajustes del momento de la compilación. El generador verifica e incorpora cada archivo fijado. Para compilar sin conexión con fijaciones, use `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

El flujo de trabajo del instalador de Linux ejecuta el paquete como un usuario sin privilegios y con la red desactivada. Ubuntu 24.04 prueba el Python del sistema. Debian 12 slim prueba el intérprete portátil cuando la huella x86_64 está disponible, y comprueba el rechazo cuando está pendiente. Las instalaciones correctas ejecutan la autocomprobación, informan de la versión y prueban los dos modos de eliminación. El flujo de trabajo sube el script como artefacto de compilación para distribuirlo a mano.
