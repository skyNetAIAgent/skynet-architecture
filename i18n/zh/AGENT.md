# SkyNet 研究代理程序

[English](../../agent/README.md) · **中文** · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

你可以让你的电脑承担一部分研究，从而帮助设计 SkyNet。研究代理程序是一个开源的小程序。它会查看这个仓库中的任务，完成一小部分计算并分享结果。你也可以在任务板上发布研究问题，或回答别人的问题。你不需要账号，也不需要人工智能助手。[任务板指南](BOARD.md)

**现阶段不提供任何奖励。** 没有积分，没有金钱，也没有对未来报酬的承诺。这是帮助设计 SkyNet 网络的志愿研究。

## 它做什么，以及它绝不做什么

| 它做 | 它绝不做 |
|---|---|
| 读取已签名的任务列表。每个任务指定一个内置计算，并提供其输入 | 运行来自任务或任务板帖子的代码 |
| 默认一次只运行一份工作，并使用较低的 CPU 优先级 | 默认在检测到电池供电时开始新的工作 |
| 用本设备的密钥为结果签名，并默认将其发送到公开中继和全节点 | 在自动结果中包含你的个人文件或硬件标识 |
| 在安装桌面更新之前检查项目签名 | 接受签名无效、文件哈希错误或版本编号更旧的下载更新 |
| 安装到你的用户账户下，并让你选择是否在登录时启动 | 普通桌面安装需要管理员权限 |

一个研究问题是：一个即将离开的参与者能否靠一批伪造结果获利。需要多少验证者参与？得到同一份计算的设备应得到完全相同的答案，因此它们的结果可以相互比较。[研究任务](../../tasks/README.md)

## 需要什么

- Windows x64（amd64）或 ARM64，或 Linux amd64、arm64 或 ARMv7。1.0.1 中的桌面代理程序是一个单独的 Go 程序。Releases 中的安装程序已包含可执行文件，可以直接运行。不支持 macOS。
- 对于实验性的 Android 应用，需要运行在 arm64-v8a 或 x86_64 上的 Android 7.0 或更高版本。
- 用于接收新任务和发布结果的网络连接。Releases 中的 Linux 安装程序可以离线安装。

## 安装

**Windows**

1. 从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 选择适合你电脑的 Windows 安装程序（`.exe`），amd64 或 arm64。
2. 将文件的 SHA-256 校验和与你信任的来源提供的校验和进行比较，然后运行安装程序。你可以选择立即启动代理程序，以及在登录时启动。安装程序会在开始菜单中添加快捷方式。[Windows 安装程序指南](../../installer/windows/README.md)

**Linux**

从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 下载 `skynet-agent-install.sh`，并以你的普通用户身份运行 `sh skynet-agent-install.sh`。该文件包含所有三种受支持的 Linux 架构的可执行文件。

你也可以使用下面的命令通过网络安装。它需要 `curl`、`jq`、`xxd`、`sha256sum` 以及支持 Ed25519 的 OpenSSL。

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

默认情况下，安装程序会保留你现有的登录启动设置。全新安装后，请自行使用 `skynet-agent run` 启动代理程序。要立即启动并在登录时启动，请运行 `sh skynet-agent-install.sh --autostart`。这会使用你的 systemd 用户服务。添加 `--linger` 可在开机后以及注销后继续运行，或使用 `--no-autostart` 关闭该服务。如果你的 shell 找不到该命令，请使用 `~/.local/bin/skynet-agent`。[Linux 安装程序指南](../../installer/linux/README.md)

**Android（实验性）**

从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 下载 `skynet-agent.apk`。打开该文件，并在 Android 询问时允许从浏览器或文件管理器安装。打开 **SkyNet Agent** 并点按 **Start**。默认情况下它只在充电时计算。**Start after reboot** 默认关闭。

APK 有自己的版本号。应用版本 0.3.0 包含 Go 代理程序 1.0.0。应用会在其界面上或通过通知提供更新。在请求你在 Android 中确认安装之前，它会检查已签名的版本说明以及 APK 的大小和 SHA-256。[Android 指南](../../android/README.md)

你的设备密钥、设置和结果都存放在代理程序文件夹中。默认位置在 Windows 上是 `%LOCALAPPDATA%\SkyNetAgent`，在 Linux 上是 `~/.local/share/skynet-agent`（如果设置了 `$XDG_DATA_HOME`，则为 `$XDG_DATA_HOME/skynet-agent`）。Linux 安装程序还接受 `SKYNET_AGENT_HOME` 或 `--home DIR` 来指定其他文件夹。Android 将其配置保存在应用的私有存储中。

如果你已在受支持的桌面上运行 Python 代理程序并开启了自动更新，它会通过已签名的 **0.4.0** 桥接版本自行切换到 Go。它会保留你的设备密钥、进度和尚未发送的结果。旧的桥接版本及其解释器会被保留，以便回滚。

## 第一步

在 Linux 上，请使用下面的命令。在 Windows 上，请在代理程序文件夹中打开 PowerShell，并用 `.\skynet-agent.exe launch` 代替 `skynet-agent`。例如，`.\skynet-agent.exe launch status` 会通过常驻启动器显示你的状态。

```sh
skynet-agent verify-install       # check the installed release files and run a test calculation
skynet-agent selftest --online    # run the calculation and check signed documents online
skynet-agent net id               # show this device's public key, its name on the board
skynet-agent run                  # if it isn't running already, work until you press Ctrl+C
```

使用 `skynet-agent autostart status` 查看登录时启动是否已开启。要开启它，请使用 `skynet-agent autostart enable`。

### 发布结果

代理程序会把每个完成的结果保存在发件箱中。它使用代理程序文件夹中 `identity.key` 里的签名密钥，如果该文件不存在，会在首次使用时创建一把。默认情况下，它会把签名结果发送到公开 Nostr 中继和全节点。必须有一个节点或两个不同的中继确认收到，代理程序才会把结果移到 `sent`。否则它会留在发件箱中。每次重试都使用同一条具有相同 ID 的签名记录。

下面是使用内置测试计算的任务的部分结果。完整结果还会给出任务名称、耗时秒数、格式版本、代理程序版本编号，以及默认情况下的平台标签。包裹它的签名记录包含设备的公钥、时间戳、记录 ID 和签名。

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## 命令

| 桌面命令 | 作用 |
|---|---|
| `skynet-agent run` | 一直工作直到被停止。`--once` 最多尝试一个工作单元。`--no-submit` 在本次运行中把结果保留在本地。`--no-update` 跳过更新安装。`--verbose` 在日志中增加细节。 |
| `skynet-agent status` | 显示版本、代理程序文件夹、电源状态、工作计数、等待中的结果和最近的问题。 |
| `skynet-agent tasks` | 列出自动研究任务、哪些已就绪，以及本设备已完成多少个工作单元。 |
| `skynet-agent pause` / `resume` | 让活动中的工作单元完成并停止启动新的单元，或重新允许新的单元。 |
| `skynet-agent stop` | 让正在运行的代理程序退出。 |
| `skynet-agent outbox` | `list` 显示等待中的结果，`show NAME` 显示其中一条，`send` 尝试发布符合条件的结果，`drop NAME` 删除排队中的结果。 |
| `skynet-agent net` | 使用 `tasks` 或 `show` 浏览任务板。使用 `post-task`、`claim`、`report`、`accept` 或 `revise` 参与。`sync` 重试待发的任务板帖子并获取记录。`id` 显示你的公钥。[任务板指南](BOARD.md) |
| `skynet-agent config` | `show` 列出设置，`get KEY` 显示其中一项，`set KEY VALUE` 修改它。 |
| `skynet-agent update` | 检查是否有更新的已签名桌面版本，如果该版本适用于本设备则安装它。 |
| `skynet-agent selftest [--online]` | 用已知答案检查一项计算。添加 `--online` 可检查任务列表和项目较早版本说明上的签名。 |
| `skynet-agent verify-install` | 校验已安装的版本文件并运行测试计算。 |
| `skynet-agent version` | 显示代理程序版本、版本编号、Go 版本和平台。 |
| `skynet-agent autostart` | `status` 显示登录时启动是否已开启。`enable` 开启它，`disable` 关闭它。 |
| `skynet-agent uninstall --yes` | 移除 Linux 安装。添加 `--purge` 可一并删除已保存的数据。 |

## 设置

| 设置 | 默认值 | 含义 |
|---|---|---|
| `workers` | 1 | 桌面代理程序可同时运行的工作单元数，从 1 到 256。Android 只运行一个。 |
| `run_on_battery` | false | 允许在使用电池供电时进行计算。 |
| `paused` | false | 在启动新单元前等待。`pause` 和 `resume` 命令会修改此设置。 |
| `poll_minutes` | 30 | 大致多久检查一次仓库，从 5 到 1440 分钟。失败的检查有自己的重试安排。 |
| `update` | auto | 在桌面上，`auto` 安装符合条件的已签名更新，`notify` 在有可用更新时记录日志，`off` 跳过安装和提示。这三种模式都仍会检查维护者发布的已签名暂停通知。 |
| `submit` | auto | `auto` 随工作进展发送结果。`manual` 把结果留在发件箱中，直到你运行 `skynet-agent outbox send`。 |
| `submit_via` | net | 通过中继和节点发布签名记录。这是 1.0 中唯一可用的通道。 |
| `max_task_minutes` | 120 | 每个工作单元的时间限制，从 1 到 1440 分钟。任务中更短的限制优先。 |
| `report_platform` | true | 在新结果中包含操作系统、处理器架构和 Go 版本，例如 `linux-amd64-` 后接 Go 版本。 |

例如，`skynet-agent config set workers 4` 最多允许四个桌面工作单元。为兼容较旧的安装，`skynet-agent config show` 还会列出旧的评论限制和 AI 设置。这些设置对 Go 计算或网络发布没有影响。

## 可选：用你自己的本地 AI 模型回答研究问题

本地 AI 模式在 1.0 中不可用。你仍然可以自己撰写回答并发布到任务板上。

## 安全，如实说明

- **更新和任务列表都有签名。** 代理程序会用程序中内置的项目发布密钥检查它们的 Ed25519 签名。在切换到桌面更新之前，它会检查版本编号、校验可执行文件的大小和 SHA-256，并运行一次测试计算。它会拒绝较旧的任务列表，并停止从已过期的列表启动工作。
- **任务是数据。** 任务只能选择可执行文件中内置的计算。添加新的计算类型需要新的桌面版本或 Android 应用更新。[计算的 Go 源代码](https://github.com/skyNetAIAgent/skynet-architecture/tree/main/agent-go/kernels)
- **每个工作单元都在单独的进程中运行**，并使用你的账户。工作进程会请求较低的 CPU 优先级。如果达到时间限制，代理程序会停止该工作进程。
- **桌面更新可以回滚。** 启动器在启动活动版本之前会检查它。如果检查失败，或者连续三次启动代理程序的尝试都在第一分钟内崩溃，启动器可以在有可用版本的情况下恢复一个经过校验的先前版本。它会记住失败的版本编号。
- **你的设备密钥是一个未加密的文件。** 任何复制了 `identity.key` 的人都能以这台设备的名义签名。保留一份私密备份，可以让你在重装后仍保留任务板上的名字。
- **首次安装取决于你从哪里获取安装程序或脚本。** 安装之后，谁掌握了项目的发布密钥，谁就能签署会以你的用户权限运行的新代码。在研究阶段，该密钥由项目维护者持有。如果你想先审阅桌面更新，请使用 `skynet-agent config set update notify`，并在准备好时运行 `skynet-agent update`。拟议的 SkyNet 网络旨在无需中央发布密钥即可运行。[研究代理程序设计及威胁表（俄文）](../../docs/RESEARCH_AGENT.md)

## 隐私

当你下载任务或更新时，GitHub 能看到你的 IP 地址。你联系的中继和全节点也能看到你的 IP 地址。内置的全节点使用未加密的 HTTP。结果和任务板帖子都是公开的。它们的公钥让读者可以把同一台设备的记录关联起来。

自动结果包含计算数据以及上文所述的字段。使用 `skynet-agent config set report_platform false` 可从以后的结果中省略平台标签。代理程序不会扫描你的个人文件，也不会包含硬件序列号。当你发布任务板任务或报告时，你选择提交的文本会变为公开。

## 你的成本

一个繁忙的工作进程大约会占用一个 CPU 核心。低优先级有助于其他程序在需要时获得 CPU 时间。这项工作仍然会消耗电力，并可能产生热量。在笔记本电脑上，代理程序大约每分钟检查一次电源。默认情况下，当它检测到电池供电时，会等待而不启动新的工作单元。已经在运行的工作单元可以完成，而且如果无法确定电源来源，桌面代理程序可以开始工作。

在 Android 上，拔掉电源会取消当前的工作单元，并让它可供重试。如果你希望它在拔掉电源后继续计算，请在应用中选择 **Also work on battery power**。

## 卸载

在 Windows 上，请使用 **SkyNet Agent** 卸载程序。默认情况下，它会保留你的设备密钥、队列和版本历史。在卸载时选择删除数据选项可一并删除它们。

在 Linux 上，请运行以下命令。它会关闭用户服务、停止代理程序并删除已安装的程序。你的密钥、设置、进度和队列会被保留。

```sh
skynet-agent uninstall --yes
```

要一并删除已保存的代理程序数据，请在卸载时使用 `skynet-agent uninstall --yes --purge`。在 Android 上，请通过 Android 设置卸载 **SkyNet Agent**，以删除该应用及其本地数据。已发布的记录仍然公开。

## 疑难解答

- **“no valid signature from a trusted key”** 表示下载的文档未通过校验。代理程序会拒绝它。它仍然可以使用先前已验证的任务列表，直到该列表过期。在桌面上，`skynet-agent status` 会显示最近的仓库错误。运行日志是代理程序文件夹中的 `logs/agent.log`。
- **结果一直留在发件箱。** 使用 `skynet-agent status` 或 `skynet-agent outbox list` 查看有哪些结果在等待。在手动模式下，请运行 `skynet-agent outbox send`。如果应答的中继或节点太少，结果会继续排队等待另一次尝试。
- **较旧的安装显示“GitHub submission is unsupported”。** 运行 `skynet-agent config set submit_via net`，让新结果使用签名记录。已标记为 GitHub 的条目和旧的 AI 回答会留在发件箱中以便检查。
- **代理程序正在运行，但没有开始新的工作。** 检查 `skynet-agent tasks` 和运行日志。它可能已暂停、在等待电源、没有符合条件的任务，或在等待发件箱有空间。在 Android 上，如果你之前停止了应用，请连接充电器并点按 **Start**。

## 目前已测试的范围

代理程序测试会在 Windows 和 Linux 上自动运行。它们覆盖已签名的任务列表、带已知答案的计算、更新和回滚、签名记录、投递、任务板，以及一次启动工作进程并将其结果投递到模拟节点的运行。

已在 Windows 11、Linux Mint、Ubuntu Server 和 Android 14 模拟器上尝试过实际安装。Android 应用尚未在真实设备上验证。如果在你的系统上有东西无法正常工作，请提交 issue。

## 许可

代理程序的代码采用 [MIT 许可](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/agent-go/LICENSE)。
