# SkyNet 研究代理程序

[English](../../agent/README.md) · **中文** · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

帮助设计 SkyNet 并不一定需要人工智能助手。研究代理程序是一个开源的小程序。它会定期查看这个仓库，领取研究任务，在你的电脑空闲时进行计算，并发布结果。它还会给你一个[任务板](BOARD.md)，人们和他们的 AI 助手可以在上面发布研究任务并回答问题。任何地方都不需要账号。

**现阶段不提供任何奖励**：没有积分，没有金钱，也没有对未来报酬的承诺。这是对研究的自愿帮助。代理程序不是 SkyNet 网络，而是设计它的工具。

## 它做什么，以及它绝不做什么

| 它做 | 它绝不做 |
|---|---|
| 从仓库读取已签名的任务列表和已签名的版本说明 | 运行来自任务的代码。任务只是内置计算的名称加上数字 |
| 以最低的 CPU 优先级运行内置计算，默认一次一个 | 在电池供电时工作，除非你允许 |
| 把每个结果作为一条用本设备自己的密钥签名的记录，通过公开中继和全节点发布 | 发送你的文件、硬件标识或电脑上的任何其他内容 |
| 自动更新，但只更新到用项目发布密钥签名的版本 | 安装签名错误、文件哈希错误或编号更旧的更新 |
| 安装在你自己的用户配置文件中，并让你选择是否在登录时启动 | 需要管理员权限 |

首批任务是关于 SkyNet 支付规则的精确计算。例如：“一个准备离开网络的参与者，能否靠一批伪造结果获利？合谋验证者的份额达到多少时可以？”每台设备必须得到完全相同的数字，不同人的结果会相互比对。详见 [tasks/README.md](../../tasks/README.md)。

## 需要什么

- Windows x64 安装程序自带 Python。Linux 使用系统提供的 Python 3.9 或更高版本，或在 glibc x86_64 和 aarch64 上使用经过验证的便携运行时。目前 Linux 运行时的校验和仍未确定，所以这个版本需要使用系统的 Python。其他平台需要 Python 3.9 或更高版本。
- 用于接收任务和发布结果的网络连接。单文件 Linux 安装程序可以离线工作。

## 安装

**Windows x64**

1. 从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 下载 `SkyNetAgentSetup-<version>.exe` 并运行。安装程序会询问你是否立即启动代理程序，以及是否在 Windows 登录时启动。两个复选框默认都已勾选。关于校验和与 SmartScreen 的说明，请参见 [Windows 安装程序指南](../../installer/windows/README.md)。
2. 如果你已经装有 Python，也可以通过 PowerShell 安装。

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux**

从项目的 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 下载 `skynet-agent-install.sh`，然后运行 `sh skynet-agent-install.sh`。如果要从仓库直接安装，请运行：

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

在第一个提示处按回车，代理程序就会通过你的 systemd 用户服务立即运行，并在登录时启动。第二个提示会询问是否从开机起就运行，甚至在你登录之前。无人值守安装时，请使用 `--autostart`、`--autostart --linger` 或 `--no-autostart`。如果你的 shell 找不到 `skynet-agent`，请使用 `~/.local/bin/skynet-agent`。参见 [Linux 安装程序指南](../../installer/linux/README.md)。

**macOS**（终端）：

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android 应用（实验性）**：从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 页面下载 `skynet-agent.apk`，允许浏览器安装应用，然后打开该文件。应用只在设备充电时工作；结果以签名记录的形式发布，无需账号。尚未在真实设备上验证。源代码和说明：[android/README.md](../../android/README.md)。

**Android**：从 F-Droid 安装 [Termux](https://termux.dev) 应用，打开后运行：

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

在手机上，代理程序只在充电时工作。如果它无法判断手机是否在充电，它会等待并给出提示；这时请安装 Termux:API 应用并运行 `pkg install termux-api`，或者允许使用电池：`skynet-agent config set run_on_battery true`。

如果你想先看清楚再运行：下载 [`install.py`](../../agent/install.py)，读一读（它很短），然后运行 `python3 -I install.py`。

安装程序把代理程序放进一个文件夹（Windows 为 `%LOCALAPPDATA%\SkyNetAgent`，macOS 为 `~/Library/Application Support/SkyNetAgent`，Linux 和 Android 为 `~/.local/share/skynet-agent`），并创建 `skynet-agent` 命令。使用 `skynet-agent run` 手动启动它。

## 第一步

```sh
skynet-agent selftest --online    # 检查设备和签名
skynet-agent net id               # 本设备的公钥：它在网络上的名称
skynet-agent run                  # 一直工作，直到你按 Ctrl+C
skynet-agent autostart enable     # 可选：登录时自动启动
```

在 Windows 上，请从代理程序文件夹运行 `.\skynet-agent.cmd`。EXE 安装程序会在开始菜单的 **SkyNet Agent** 下添加状态、暂停、恢复和停止的快捷方式。代理程序会从已签名的版本更新自己的文件。要更新其自带的 Python，请运行更新的安装程序。

### 发布结果

代理程序启动时，会为本设备创建一把密钥（代理程序文件夹中的 `identity.key` 文件）。每条结果都是一条用该密钥签名的小记录。代理程序会立即把它发送到几个由不同所有者运营的公开 Nostr 中继和代理程序中列出的全节点；当两个中继或一个节点确认后，结果即视为已送达。否则它会留在发件箱中，稍后再次发送完全相同的记录，因此绝不会被计算两次。

记录是公开的，并带有本设备的公钥，因此同一台设备的结果可以相互关联。如果你更喜欢旧方式——在你自己的账号下、任务的 GitHub issue 中发表评论——请运行 `skynet-agent config set submit_via github`，并用 [GitHub CLI](https://cli.github.com) 登录（`gh auth login`），然后用 `skynet-agent github` 检查。

发布出的结果长这样，其中不包含其他任何内容：

```json
{"agent":"0.2.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## 命令

| 命令 | 作用 |
|---|---|
| `skynet-agent run` | 一直工作直到被停止。`--once` 完成一份工作后退出 |
| `skynet-agent status` | 版本、设置、计数、等待发布的结果、最近的问题 |
| `skynet-agent tasks` | 当前发布的任务以及本设备已完成的部分 |
| `skynet-agent pause` / `resume` | 不再领取新任务 / 重新领取 |
| `skynet-agent stop` | 让正在运行的代理程序退出 |
| `skynet-agent outbox` | 等待发布的结果（`list`、`show`、`send`、`link`、`approve`、`drop`） |
| `skynet-agent net ...` | 任务板：`tasks`、`show`、`post-task`、`claim`、`report`、`accept`、`revise`、`sync`、`id`；见[任务板指南](BOARD.md) |
| `skynet-agent config show` / `set 键 值` | 设置 |
| `skynet-agent update` | 立即安装最新的已签名版本 |
| `skynet-agent selftest [--online]` | 检查设备、已安装的文件和签名 |
| `skynet-agent autostart enable` / `disable` | 是否在登录时启动 |
| `skynet-agent uninstall --yes` | 关闭自启动并停止代理程序。Linux shell 安装还会一并删除它的程序文件 |

## 设置

| 设置 | 默认值 | 含义 |
|---|---|---|
| `workers` | 1 | 同时运行的任务数；每个大约占用一个 CPU 核心 |
| `run_on_battery` | false | 使用电池时也工作 |
| `poll_minutes` | 30 | 多久查看一次仓库 |
| `update` | auto | `auto` 安装已签名的更新，`notify` 只提示，`off` 忽略更新。维护者要求的暂停在任何模式下都有效 |
| `submit` | auto | `auto` 发布结果，`manual` 把结果留在发件箱 |
| `submit_via` | net | `net`：签名记录，无需账号；`github`：在你自己的 GitHub 账号下发表评论 |
| `max_task_minutes` | 120 | 一份工作最长可以持续多久 |
| `batch_minutes` | 60 | 使用 `submit_via github` 时：同一任务的结果合并发布，每隔这么多分钟最多发一条评论 |
| `max_submissions_per_day` | 48 | 使用 `submit_via github` 时：本设备每天最多发布的评论数 |
| `report_platform` | true | 在结果中加入类似 `windows-amd64-py3.12` 的粗略标签 |
| `ai.enabled` | false | 可选的 AI 模式，见下文 |

示例：`skynet-agent config set workers 4`。

## 可选：用你自己的本地 AI 模型回答研究问题

如果你在自己的电脑上运行开放模型（例如使用 Ollama、llama.cpp 服务器或 LM Studio），代理程序可以把任务列表中的研究问题交给它，并发布回答。此功能默认关闭，属于实验性质。

```sh
skynet-agent ai                               # 显示本地服务器和将使用的模型
skynet-agent config set ai.enabled true
```

- 代理程序不下载也不启动模型。除非你设置 `ai.allow_remote`，否则它只与你自己电脑上的服务器通信。
- 问题及其引用的文档来自已签名的任务列表；每份文档在交给模型之前都会与哈希值核对。
- 每个回答都会留在发件箱里等你查看：`skynet-agent outbox show 名称`，然后 `skynet-agent outbox approve 名称`。若要不经查看直接发布：`skynet-agent config set ai.review_before_submit false`。
- 回答会标明是机器生成且未经验证的。

## 安全，如实说明

- **更新和任务列表都有签名**（Ed25519）。只有当签名与已安装副本内置的发布密钥相符、版本编号高于当前版本、且每个文件都与其 SHA-256 一致时，代理程序才会接受。镜像或不良连接改变不了这一点。
- **任务是数据，不是程序。** 新的计算类型只能随已签名的版本到来，并且是 [`skynet_agent/kernels`](../../agent/skynet_agent/kernels) 中可读的 Python 源代码。
- **代理程序在 Python 的隔离模式下运行**，每份工作都在单独的低优先级进程中进行，并有时间限制。
- **如果新版本无法启动**，启动器会退回到上一个版本，并记住不再安装那个版本。
- **你的设备密钥**是代理程序文件夹中的一个普通文件。谁复制了它，就能以这台设备的名义签名；如果你想在重装后保留自己在任务板上的名字，请保留一份副本。
- **你必须信任什么。** 持有发布密钥的人可以把代码发到每一个已安装的代理程序上。在研究阶段，密钥由项目维护者持有。如果你不想自动更新，请运行 `skynet-agent config set update notify`，阅读变更后再手动更新。第一次安装信任与 GitHub 的 HTTPS 连接。目标 SkyNet 网络中根本不应有这样的密钥；本代理程序是研究工具，目前自身并不满足 SkyNet 的要求。细节和威胁表见 [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md)（俄文）。

## 隐私

代理程序从本仓库下载公开文件（和任何访问一样，GitHub 能看到你的 IP 地址），并把结果和任务板记录发送到代理程序中列出的中继和节点（它们也能看到你的 IP 地址）。一条结果包含任务名称、分片编号、计算出的数字、耗时，以及（除非你关闭 `report_platform`）一个粗略的平台标签。它是公开的，并用本设备的密钥签名。不会收集任何关于你的文件、网络或硬件的信息。

## 你的成本

默认情况下是一个繁忙 CPU 核心的电费，以最低优先级运行，因此不会拖慢其他程序。在手机上，除非你允许，否则不使用电池；请让手机保持充电。

## 卸载

如果使用 EXE 安装，请在开始菜单中选择 **SkyNet Agent → Uninstall**。卸载程序默认保留你的设备密钥和尚未发送的结果。勾选删除数据的复选框可以一并删除它们。如果使用命令行安装，请运行以下命令。

```sh
skynet-agent uninstall --yes
```

Linux shell 安装程序会保留设备密钥、设置和已保存的结果。要一并删除它们，请在卸载时使用 `skynet-agent uninstall --yes --purge`。对于其他命令行安装，请在命令执行结束后删除代理程序文件夹。

## 疑难解答

- **“no valid signature from a trusted release key”**：下载到的文件不是维护者签名的那个。代理程序会拒绝它，并继续使用已有的内容工作。如果连续多天出现，请查看仓库的 issue。
- **macOS 上出现 `CERTIFICATE_VERIFY_FAILED`**（使用 python.org 的 Python）：代理程序会自动改用系统的证书文件再试一次。如果错误仍然存在，请运行该 Python 附带的 `Install Certificates.command`。
- **来自 Microsoft Store 的 Python（Windows）** 使用 `AppData` 和注册表的私有副本。此时代理程序的文件夹是用户配置文件夹中的 `SkyNetAgent`，开机自启需要手动添加：`skynet-agent autostart enable` 会说明做法。尚未在真实设备上验证。
- **结果一直留在发件箱**：运行 `skynet-agent status`。使用 `submit_via net` 时，中继或节点无法访问（防火墙？）；使用 `submit_via github` 时，通常是缺少 `gh auth login`。
- **Android 在后台停止代理程序**：在 Termux 中运行 `termux-wake-lock`，并把 Termux 排除在电池优化之外。

## 目前已测试的范围

测试套件（[`tests/`](../../agent/tests)）覆盖签名、更新、回滚、任务、发布、签名记录、任务板、全节点以及端到端运行，每次改动都会在 Windows、Linux 和 macOS 上自动执行（见仓库的 Actions 页）。人工验证过的系统是 Windows 11。尚未在真实设备上验证：Android（Termux），以及 macOS、Linux 和 Android 上的自启动。如果在你的系统上有问题，请提交 issue。

## 许可

代理程序的代码采用 [MIT 许可](../../agent/LICENSE)。
