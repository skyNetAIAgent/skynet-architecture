<!-- translation of installer/windows/README.md, source sha256: 2da95275cc3800c9e5962bb14e7d8acc894408a7819ddf9d7ce80194c3f1169e -->

# Установщик для Windows

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · **Русский** · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Выберите установщик amd64 или arm64 для своего компьютера. Проверьте его SHA-256 с помощью контрольной суммы, полученной по доверенному каналу. Программа установки устанавливает подписанный нативный выпуск в профиль текущего пользователя. Автозапуск при входе в систему и немедленный запуск необязательны. Ярлыки в меню «Пуск» вызывают постоянный запускатель.

Программа удаления по умолчанию сохраняет идентичность, очереди и историю выпусков. Чтобы удалить их, выберите параметр удаления данных. Во время миграции предыдущий подписанный мост Python и его интерпретатор сохраняются для отката.

## Сборка и тестирование

Используйте Python 3.9+ и Inno Setup 6 на сборочной машине. Разместите манифест выпуска и отсоединённую подпись в `agent/v2`, а соответствующие двоичные файлы выпуска — в `dist`. Используйте новую папку сборки. Для дымового теста нужна одноразовая учётная запись Windows.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
