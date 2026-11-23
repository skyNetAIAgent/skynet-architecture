<!-- translation of installer/linux/README.md, source sha256: 7ece3bc522f30a5f0b62b4a6580a177b3d4725e5b1eaa5513e255f0772f27156 -->

# Установщик для Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · **Русский** · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Автономный установщик содержит подписанные исполняемые файлы Go для amd64, arm64 и ARMv7. Запустите его от имени пользователя рабочего стола. При новой установке используется каталог данных пользователя, а команда размещается в `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh --no-autostart
~/.local/bin/skynet-agent verify-install
~~~

Используйте `--home DIR` для пользовательского профиля. По умолчанию установка сохраняет автозапуск при входе в систему. Используйте `--autostart`, чтобы запустить пользовательскую службу systemd сейчас и при входе в систему, или добавьте `--linger`, чтобы она работала вне сеансов входа. При удалении агента сохраняются идентичность и очереди. Добавление `--purge` явно удаляет его сохранённые данные.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

Онлайн-загрузчик `agent/install.sh` использует curl, jq, xxd, sha256sum и OpenSSL с поддержкой Ed25519. Получите скрипт из доверенного выпуска. Он проверяет подлинность манифеста перед запуском двоичного файла для конкретной архитектуры.

Чтобы собрать автономный установщик из подписанных ресурсов, выполните следующее из корня репозитория. Манифест и подпись должны находиться в `agent/v2`. Сборщик проверяет каждый ресурс перед упаковкой.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
