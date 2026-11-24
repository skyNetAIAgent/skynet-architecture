<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# Windows 桌面安装程序

[English](../../installer/windows/README.md) · **中文** · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

为你的计算机选择 amd64 或 arm64 安装程序。通过可信渠道获取校验和，并用它验证其 SHA-256。安装程序会将已签名的原生发行版安装到当前用户的配置文件中。安装程序会立即启动代理程序，并在每次登录 Windows 时启动；这两项均可在“任务”页面上取消勾选。开始菜单快捷方式会调用常驻启动器。

卸载程序默认会保留设备身份、队列和发行历史。选择数据删除选项即可移除它们。迁移期间会保留此前已签名的 Python 桥接程序及其解释器，以便回滚。

## 构建与测试

在构建机上使用 Python 3.9+ 和 Inno Setup 6。将发行清单和分离签名暂存到 `agent/v2` 下，并将与之匹配的发行版二进制文件暂存到 `dist` 下。使用全新的构建目录。冒烟测试需要一个一次性的 Windows 账户。

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
