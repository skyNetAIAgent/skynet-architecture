<!-- translation of installer/linux/README.md, source sha256: cabcf2237fcb61f3ccddb3e461306c5030f018a0db5353bfe00e7a5f55dd389f -->

# Linux 安装程序

[English](../../installer/linux/README.md) · **中文** · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

离线安装程序包含适用于 amd64、arm64 和 ARMv7 的已签名 Go 可执行文件。请以桌面用户身份运行它。全新安装会使用按用户划分的数据目录，并把命令放在 `~/.local/bin` 中。

~~~sh
sh skynet-agent-install.sh
~/.local/bin/skynet-agent verify-install
~~~

使用 `--home DIR` 可指定自定义配置目录。安装程序会立即启动代理程序，并将其注册为 systemd 用户服务，因此重启后它会再次启动；它还会尝试在注销后继续运行（linger）。使用 `--no-autostart` 可仅执行安装，或使用 `--linger` 要求启用 linger。卸载代理程序会保留身份和队列。加上 `--purge` 则会显式删除其保存的数据。

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

位于 `agent/install.sh` 的在线引导脚本使用 curl、jq、xxd、sha256sum 以及支持 Ed25519 的 OpenSSL。请从可信的发布版本获取该脚本。它会在执行特定架构的二进制文件之前验证清单。

要根据已签名的资产构建离线安装程序，请在仓库根目录下运行以下命令。清单和签名应放在 `agent/v2` 中。构建器会在打包每个资产之前对其进行校验。

~~~sh
sh installer/linux/build.sh --dir dist
~~~
