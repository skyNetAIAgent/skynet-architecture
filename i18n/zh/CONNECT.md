<!-- translation of docs/CONNECT.md, source sha256: 125af61335dde49176b5b023903489a40b1792ebe8e8eb04a960681206774db9 -->

# 如何加入

[English](../../docs/CONNECT.md) · **中文** · [Español](../es/CONNECT.md) · [Français](../fr/CONNECT.md) · [Deutsch](../de/CONNECT.md) · [Italiano](../it/CONNECT.md) · [Русский](../ru/CONNECT.md) · [Português](../pt/CONNECT.md) · [العربية](../ar/CONNECT.md)

你可以用你的电脑或手机帮助设计 SkyNet。研究代理程序是一个开源的小程序：它接收已签名的研究计算，在你设备的空闲时间里运行它们，并发布结果。任何地方都不需要账号。**现阶段不提供任何奖励**：这是为研究提供的志愿帮助，而不是 SkyNet 网络本身。

## 安装

| 你的设备 | 该怎么做 |
|---|---|
| **Windows 10/11**（64 位） | 从[最新发布版本](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest)下载 `SkyNetAgentSetup-<version>-amd64.exe` 并运行它。因为这个文件没有代码签名，Windows 会显示“Windows 已保护你的电脑”：请选择 **更多信息**，然后选择 **仍要运行**。 |
| **Linux**（x86_64 或 ARM64） | 从[最新发布版本](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest)下载 `skynet-agent-linux-install-<version>.sh`，然后运行 `sh skynet-agent-linux-install-<version>.sh`。 |
| **Android 7.0+**（64 位） | 从发布页面下载 `skynet-agent.apk`，打开它，并允许从此来源安装。这个应用只在手机充电时工作。 |

不支持 macOS 和 iPhone。

安装程序会立即启动代理程序，并将其设置为在重启后再次启动（在 Windows 上可以取消勾选这一项；在 Android 上按一次 **Start**）。之后就没有其他要做的事了：代理程序会自行更新（只更新到由项目签名的版本）、自行领取任务并发布结果。如果本地网络中有完整节点，它会自行找到它。

当前在线的代理程序列在 http://62.213.14.254:8790/agents：系统、处理器、内存、显卡、版本和已计算单位。不会显示 IP 地址或计算机名。

## 它使用什么，以及它绝不做什么

- 默认使用一个处理器核心，并采用最低优先级，因此你自己的程序不会被拖慢。在笔记本电脑上，除非你允许，否则它不会在使用电池供电时工作。
- 它绝不运行来自任务的代码，绝不发送你的文件，也不需要管理员权限。每个结果都是一条小的公开记录，用你设备自己的密钥签名。
- 暂停或停止：在 Windows 上是开始菜单中的 **SkyNet Agent** 文件夹，在 Linux 上是 `skynet-agent pause` / `stop`，在应用中是 **Stop** 按钮。
- 移除：在 Windows 上是 **SkyNet Agent → 卸载**，在 Linux 上是 `skynet-agent uninstall --yes`，在 Android 上卸载该应用。

详情：[代理程序指南](AGENT.md)。

## 提供想法上的帮助，而不只是计算

这个项目最主要的未解决问题是：如何以低成本、无需押金或罚款的方式检查计算，让作弊永远无利可图。如果你或你的 AI 助手有想法，或者发现了漏洞，请查看[任务板](BOARD.md)、[路线图](ROADMAP.md)和[待解决问题](OPEN_QUESTIONS.md)。
