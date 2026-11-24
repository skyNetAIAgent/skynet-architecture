<!-- translation of android/README.md, source sha256: f39e5a1b5b61d6be25ac07b2c69e9f4af5a9bca2ee2ff7cb9610398aebe13e0c -->

# Android 版 SkyNet 研究代理程序（实验性）

[English](../../android/README.md) · **中文** · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

一个 Android 应用，内置与桌面版相同的 [Go 计算内核](../../agent-go/README.md)。安装一个文件，按下开始。
默认情况下，代理程序会在设备上对每个结果进行签名，并在没有账户或令牌的情况下发布它。
现阶段不提供任何奖励。

**实验性。** 外壳 0.3.0 在 APK 中包含 Go 代理程序 1.0.0（引擎发布 7）。在 0.2.0 之上安装、
服务生命周期和重启仍需要在 Android 上进行测试。

## 面向参与者

1. 从 [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) 页面下载
   `skynet-agent.apk`。
2. 打开该文件。Android 会询问你是否允许从浏览器或文件管理器安装应用。
3. 打开 "SkyNet Agent" 并按 **开始**。一条常驻通知会显示它正在运行。

- 它仅在设备充电时工作，除非你勾选 "也在电池供电时工作"。拔掉电源会取消当前的工作单元，
  并让它可供稍后运行。
- 按下一次 **开始** 后，代理程序也会在设备重启后再次启动（**重启后启动** 默认开启；取消勾选即可关闭此功能）。按下 **停止** 会使代理程序
  在重启后保持停止状态。
- 在 Android 13 及更高版本上，如果你拒绝通知，应用仍会工作；此时 Android 只会把它显示在
  正在运行的应用列表中。
- 如果现有配置文件使用 `submit_via=github`，其结果会保持排队。此版本支持通过已签名的网络
  记录进行发布。
- 需要 Android 7.0 或更高版本，arm64-v8a 或 x86_64。
- 可选的 AI 模式在应用中不可用。
- 要移除它，卸载应用即可；设备上不会留下任何其他内容。

## 更新应用

在现有应用之上安装具有相同包签名的 0.3.0，以保留你的设备身份、设置、进度和排队中的结果。
从 0.2.0 起，打开界面会检查是否有新的 APK。只要有可用网络，Android 还会安排每日检查，
即使代理程序已停止。电池限制可能会延迟该检查。

应用使用随 APK 捆绑的密钥验证已签名的发布清单。对于更新的兼容版本，它会将发布资源下载到私有
缓存，并检查其大小和 SHA-256。点按更新按钮或通知以安装它。在 Android 8 及更高版本上，如果
出现提示，请允许从 SkyNet Agent 安装，返回应用并在 Android 安装程序中确认。在通知已禁用的
情况下，请使用主界面上的按钮。

## 代理程序与更新

前台服务会启动原生库目录中解压出的可执行文件。它一次运行一个低优先级工作进程，并在计算期间
持有唤醒锁。超时的工作进程会被停止，代理程序会暂时跳过该任务。新任务通过已签名的任务索引
到达。新的可执行代码随应用更新到达。

Android 在安装期间会检查 APK 签名证书。单独的发布密钥用于认证任务索引和 APK 下载清单。
应用在打开安装程序之前会检查 APK 的大小、SHA-256、包名和版本代码。

## 自行构建

在 Linux 上，安装带源码的 Go 1.27.4、Bash、GNU patch、coreutils、file 和 readelf（binutils）。
构建 APK 还需要 JDK 17、Gradle 8.7 和 Android SDK 34。

```sh
cd android
gradle assembleRelease
```

Gradle 会调用 `./build-go.sh`。直接运行该脚本即可只构建两个
`app/src/main/jniLibs/<abi>/libskynet.so` 可执行文件。它对两个 ABI 都使用 `GOOS=android`、
`CGO_ENABLED=0` 和 PIE。arm64 构建使用原版 Go。对于 x86_64 模拟器构建，该脚本会在
Go 1.27.4 主机构建工具的临时副本中启用内部链接。在安装任一文件之前，它会验证架构、入口点和
`/system/bin/linker64` 解释器。

发布 APK 为 `app/build/outputs/apk/release/app-release-unsigned.apk`。要覆盖安装，请先使用
`zipalign`，再用与上一个 APK 相同的密钥执行 `apksigner sign`。使用 `tools/make_apk_manifest.py`
从最终签名的 APK 生成并签名 `android/latest.json`。

## 许可

MIT，与代理程序相同：[agent/LICENSE](../../agent/LICENSE)。
