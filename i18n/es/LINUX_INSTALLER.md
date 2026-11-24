<!-- translation of installer/linux/README.md, source sha256: cabcf2237fcb61f3ccddb3e461306c5030f018a0db5353bfe00e7a5f55dd389f -->

# Instalador de Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · **Español** · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

El instalador sin conexión contiene ejecutables Go firmados para amd64, arm64 y ARMv7. Ejecútelo con el usuario de escritorio. Una instalación nueva usa el directorio de datos por usuario y coloca la orden en `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh
~/.local/bin/skynet-agent verify-install
~~~

Use `--home DIR` para un perfil personalizado. La instalación inicia el agente de inmediato y lo registra como servicio de usuario de systemd, de modo que vuelve a iniciarse tras un reinicio; también intenta mantenerlo en ejecución después de cerrar la sesión (linger). Use `--no-autostart` para solo instalar, o `--linger` para exigir linger. La eliminación del agente conserva la identidad y las colas. Añadir `--purge` elimina explícitamente sus datos guardados.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

El script de arranque en línea de `agent/install.sh` usa curl, jq, xxd, sha256sum y OpenSSL con compatibilidad con Ed25519. Obtenga el script de una versión de confianza. Autentica el manifiesto antes de ejecutar el binario específico de la arquitectura.

Para compilar el instalador sin conexión a partir de archivos firmados, ejecute lo siguiente desde la raíz del repositorio. El manifiesto y la firma deben estar en `agent/v2`. El generador verifica cada archivo antes de empaquetarlo.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
