<!-- translation of android/README.md, source sha256: dd56c64ec3931fa625cd383ec84dcdb5618d80f9faca47d3c9a52cd30294927e -->

# Android 版 SkyNet 研究代理程序（实验性）

[English](../../android/README.md) · **中文** · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

一个 Android 应用，内置与桌面版相同的[研究代理程序](../../agent/README.md)。它面向不想配置
Termux 的人：安装一个文件，按下开始。现阶段不提供任何奖励。

**状态：实验性。** 2026 年 11 月 22 日，该应用在一个 Android 14 模拟器（x86_64）上针对一个
用测试密钥签名的本地测试仓库进行了检查：它完成安装、启动、校验签名，无错误地计算出测试
任务的全部 7 个分片，在模拟器脱离充电器时等待，在后台持续工作，保存令牌并用它访问了真实
的 GitHub API，随后停止并再次启动且状态得以保留。一个仅 ARM 的构建（`arm64-v8a`）通过其
ARM 转译在同一模拟器上完成了相同的检查。其 Python 部分也在电脑上通过了测试。**它尚未在
真实手机上、在 Android 7–13 上、在长时间运行中、或针对手机厂商的电池优化进行验证。**
在 [Termux](../../agent/README.md#install) 中运行代理程序仍然是另一种方式。

## 面向参与者

1. 从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 页面下载
   `skynet-agent.apk`。
2. 打开该文件。Android 会询问你是否允许从浏览器或文件管理器安装应用。
3. 打开 "SkyNet Agent" 并按 **开始**。一条常驻通知会显示它正在运行。

需要了解的事项：

- 它仅在设备充电时工作，除非你勾选 "也在电池供电时工作"。充电器会在各份工作之间检查：
  已开始的一份工作（通常不到一分钟）即使你拔掉设备也会完成。
- 设备重启后它不会自行启动：请打开应用并再次按 **开始**。
- 在 Android 13 及更高版本上，如果你拒绝通知，应用仍会工作；此时 Android 只会把它显示在
  正在运行的应用列表中。
- 要发布结果，它需要一个 GitHub 令牌：在 GitHub 中打开 Settings → Developer settings →
  Personal access tokens，创建一个可以写入公开仓库 issue 的令牌，并将其粘贴到应用中。
  该令牌只保存在应用内部。没有令牌时，结果会在设备上等待（最多 300 个，之后应用停止
  计算）。
- 需要 Android 7.0 或更高版本、64 位设备、约 40 MB。
- 可选的 AI 模式在应用中不可用。
- 要移除它，卸载应用即可；设备上不会留下任何其他内容。

## 它与桌面代理程序有何不同

| | 桌面版 | Android 应用 |
|---|---|---|
| 代理程序代码 | `agent/skynet_agent` | 同一个包，已构建进 APK |
| 工作 | 独立的低优先级进程 | 一次一个分片，在应用的后台进程内进行 |
| 时间限制 | 工作进程被终止 | 看门狗结束后台进程；Android 会重启它，任务则留给更快的设备 |
| 代理程序更新 | 来自仓库的已签名版本 | 同一个已签名版本，由构建进 APK 的代码检查：签名、每个文件、签名列表之外没有任何文件、绝不低于此前已在此处工作的最高版本。新版本有三次机会访问仓库；否则应用回退到内置代码 |
| 应用本身 | 启动器和安装程序 | 只在有新 APK 时改变 |
| 发布 | GitHub CLI 登录 | 粘贴到应用中的令牌 |

如实说明的局限。该 APK 使用项目维护者持有的密钥签名；Android 只接受用同一密钥签名的应用更新。
发布密钥（用于代理程序代码和任务列表）和这个 APK 密钥是目标 SkyNet 网络不应存在的两个单点
信任。应用在运行时加载已签名的 Python 代码，这是 Google Play 规则不允许的，因此它以文件形式
分发。

## 自行构建

你需要在构建电脑上安装 JDK 17、Android SDK（platform 34、build-tools 34）、Gradle 8.7 和
Python 3.12。

```sh
cd android
gradle assembleRelease
```

结果是 `app/build/outputs/apk/release/app-release-unsigned.apk`。安装前用你自己的密钥签名
（先 `zipalign`，再 `apksigner sign`）。你自己签名的 APK 无法覆盖项目的 APK 安装，反过来也
一样。

请只从 `agent/skynet_agent/trust.py` 中列有发布密钥的提交构建应用：没有发布密钥的代理程序
不会接受任何任务。在这种情况下，发布构建会报错停止；`-PallowNoReleaseKey` 仍会构建这样的
APK，仅供测试使用。

应用的 Python 部分是 [`app/src/main/python/skynet_android.py`](../../android/app/src/main/python/skynet_android.py)。
它由 [`agent/tests/test_android_glue.py`](../../agent/tests/test_android_glue.py) 在电脑上测试。
Python 通过 [Chaquopy](https://chaquo.com/chaquopy/)（MIT 许可）嵌入。

## 许可

MIT，与代理程序相同：[agent/LICENSE](../../agent/LICENSE)。
