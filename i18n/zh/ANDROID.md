<!-- translation of android/README.md, source sha256: 3fd07398dc6f1c3ed1d7c21b1315b13e43cdbf629cf72aab3887e8ebbd602e2b -->

# Android 版 SkyNet 研究代理程序（实验性）

[English](../../android/README.md) · **中文** · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

一个 Android 应用，内置与桌面版相同的[研究代理程序](../../agent/README.md)。安装一个文件，按下开始。
默认情况下，代理程序会在设备上对每个结果进行签名，并在没有账户或令牌的情况下发布它。
现阶段不提供任何奖励。

**实验性。** 上一版外壳于 2026 年 11 月 22 日在一个 Android 14 模拟器上进行了测试。它完成了
全部 7 个测试分片，等待充电，并在停止和启动后保留了状态。外壳 0.2.0 包含代理程序 0.2.2。
其安装和重启流程仍需要在 Android 上进行测试。

## 面向参与者

1. 从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 页面下载
   `skynet-agent.apk`。
2. 打开该文件。Android 会询问你是否允许从浏览器或文件管理器安装应用。
3. 打开 "SkyNet Agent" 并按 **开始**。一条常驻通知会显示它正在运行。

- 它仅在设备充电时工作，除非你勾选 "也在电池供电时工作"。充电器会在各份工作之间检查：
  已开始的一份工作（通常不到一分钟）即使你拔掉设备也会完成。
- 要在设备重启后恢复运行，请启用 **重启后启动**。该选项默认关闭。按下 **停止** 会使代理程序
  在重启后保持停止状态。
- 在 Android 13 及更高版本上，如果你拒绝通知，应用仍会工作；此时 Android 只会把它显示在
  正在运行的应用列表中。
- 选择 `submit_via=github` 的高级用户可以在主界面上输入 GitHub 令牌。
- 需要 Android 7.0 或更高版本、64 位设备、约 40 MB。
- 可选的 AI 模式在应用中不可用。
- 要移除它，卸载应用即可；设备上不会留下任何其他内容。

## 更新应用

如果你使用的是 0.1.0 版，请在现有应用之上安装 Releases 中的 0.2.0，以保留你的设置和排队中的
结果。从 0.2.0 起，打开界面会检查是否有新的 APK。只要有可用网络，Android 还会安排每日检查，
即使代理程序已停止。电池限制可能会延迟该检查。

应用使用随 APK 捆绑的密钥验证已签名的发布清单。对于更新的兼容版本，它会将发布资源下载到私有
缓存，并检查其大小和 SHA-256。点按更新按钮或通知以安装它。在 Android 8 及更高版本上，如果
出现提示，请允许从 SkyNet Agent 安装，返回应用并在 Android 安装程序中确认。在通知已禁用的
情况下，请使用主界面上的按钮。

## 它与桌面代理程序有何不同

| | 桌面版 | Android 应用 |
|---|---|---|
| 代理程序代码 | `agent/skynet_agent` | 同一个包，已构建进 APK |
| 工作 | 独立的低优先级进程 | 一次一个分片，在应用的后台进程内进行 |
| 时间限制 | 工作进程被终止 | 看门狗结束后台进程；Android 会重启它，任务则留给更快的设备 |
| 代理程序更新 | 来自仓库的已签名版本 | APK 会验证已签名的文件和发布编号。新的代理程序有三次启动机会来通过本地自检并完成一个循环步骤 |
| 应用本身 | 启动器和安装程序 | 一个经你确认后安装的已验证 APK |
| 发布 | 默认发布已签名的记录 | 默认发布已签名的记录 |

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

代理程序桥接层和 APK 验证器有各自的桌面 Python 测试。
[代理程序测试](../../agent/tests/test_android_glue.py) · [APK 更新测试](../../agent/tests/test_apk_update.py)
Python 通过 [Chaquopy](https://chaquo.com/chaquopy/)（MIT 许可）嵌入。

## 许可

MIT，与代理程序相同：[agent/LICENSE](../../agent/LICENSE)。
