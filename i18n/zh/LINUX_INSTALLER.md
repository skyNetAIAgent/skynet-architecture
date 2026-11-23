<!-- translation of installer/linux/README.md, source sha256: 7ece3bc522f30a5f0b62b4a6580a177b3d4725e5b1eaa5513e255f0772f27156 -->

# Linux 安装程序

[English](../../installer/linux/README.md) · **中文** · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

离线安装程序包含适用于 amd64、arm64 和 ARMv7 的已签名 Go 可执行文件。请以桌面用户身份运行它。全新安装会使用按用户划分的数据目录，并把命令放在 `~/.local/bin` 中。

~~~sh
sh skynet-agent-install.sh --no-autostart
~/.local/bin/skynet-agent verify-install
~~~

使用 `--home DIR` 可指定自定义配置目录。默认情况下，安装程序会保留登录时启动。使用 `--autostart` 可立即启动 systemd 用户服务，并在登录时启动；或者加上 `--linger`，让它在登录会话之外继续运行。卸载代理程序会保留身份和队列。加上 `--purge` 则会显式删除其保存的数据。

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

位于 `agent/install.sh` 的在线引导脚本使用 curl、jq、xxd、sha256sum 以及支持 Ed25519 的 OpenSSL。请从可信的发布版本获取该脚本。它会在执行特定架构的二进制文件之前验证清单。

要根据已签名的资产构建离线安装程序，请在仓库根目录下运行以下命令。清单和签名应放在 `agent/v2` 中。构建器会在打包每个资产之前对其进行校验。

~~~sh
sh installer/linux/build.sh --dir dist
~~~
