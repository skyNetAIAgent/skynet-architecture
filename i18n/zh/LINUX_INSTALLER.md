<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# Linux 安装程序

[English](../../installer/linux/README.md) · **中文** · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

在你自己的账户下，运行项目 Releases 页面上的单文件。

```sh
sh skynet-agent-install.sh
```

该文件包含已签名的代理程序版本。安装过程会离线校验它的 Ed25519 签名和文件哈希。如果 PATH 中有 Python 3.9 或更高版本，安装程序会使用该解释器。否则，它需要适用于 x86_64 或 aarch64 的固定版本 glibc CPython 构建。**目前这两个哈希都尚未确定。此构建需要系统 Python。**

在线安装程序使用相同的安装流程。在有经过校验的固定值时，它可以从 python-build-standalone 获取匹配的运行时，并在解压前检查 SHA-256。便携式解释器位于 `$XDG_DATA_HOME/skynet-agent/python/<sha256>` 下，通常是 `~/.local/share/skynet-agent/python/<sha256>`。`~/.local/bin` 中的命令和 systemd 用户服务会使用选定的可执行文件。

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## 启动与卸载

在终端中，在第一个提示处按 Enter，会立即启动服务，并在登录时启动。在第二个提示处按 Enter，则让它只在登录会话期间运行。没有终端时，安装程序会跳过这些提示。以下命令可以明确作出选择。

```sh
sh skynet-agent-install.sh --autostart           # Run now and at sign-in
sh skynet-agent-install.sh --autostart --linger  # Also run before login and after logout
sh skynet-agent-install.sh --no-autostart        # Install for manual use
```

该服务需要正在运行的 systemd 用户管理器。已签名的 0.2.2 服务写入程序支持带空格的路径。如果解释器或代理程序的路径包含双引号、反斜杠、美元符号、百分号或换行符，安装程序会要求手动启动。如果本地策略禁止驻留，安装程序会报告这一点，而服务仍会在登录会话期间运行。整个账户的驻留设置可以另行用 `loginctl disable-linger "$(id -un)"` 更改。手动安装后，用 `~/.local/bin/skynet-agent run` 开始工作。

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

卸载会关闭服务、请求停止，并等待代理程序的锁释放。你的设备密钥、发件箱、待发送的中继记录和设置会留在代理程序目录中，供重新安装时使用。如果要同时清除代理程序保存的数据，请使用 `uninstall --yes --purge`。驻留是整个账户的设置，卸载后仍会保留。

## 构建与校验

在仓库根目录下，在构建机器上使用 Python 3.9 或更高版本。

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

构建器使用 `agent/install.py` 中的公钥验证发布版本，并生成 `installer/linux/skynet-agent-install.sh`。要启用便携式 Python，请分别校验每个上游归档，并把它的 SHA-256 记录到 `python.lock`（每行一个字段）。仅对于空条目，CI 可以通过 `SKYNET_PYTHON_SHA256_X86_64` 或 `SKYNET_PYTHON_SHA256_AARCH64` 提供经过校验的摘要。这些是构建时的设置。构建器会校验并嵌入每个固定版本归档。要使用固定版本离线构建，请使用 `sh installer/linux/build.sh --runtime-dir /path/to/archives`。

Linux 安装程序工作流会在禁用网络的情况下，以非特权用户身份运行安装包。Ubuntu 24.04 会测试系统 Python。当 x86_64 摘要可用时，Debian 12 slim 会测试便携式解释器；摘要尚未确定时，则会检查安装是否被拒绝。安装成功后，会运行自检、报告版本，并测试两种卸载方式。该工作流会把脚本作为构建产物上传，以便手动分发。
