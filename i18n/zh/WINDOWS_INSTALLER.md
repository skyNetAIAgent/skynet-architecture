<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# Windows x64 安装程序

[English](../../installer/windows/README.md) · **中文** · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

从同一个项目发行版下载 EXE 和与之匹配的 `.exe.sha256` 文件。在 PowerShell 中打开下载文件夹，并核对校验和。[GitHub 发行版](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

打开核对过的 EXE。由于安装程序没有代码签名，SmartScreen 可能会显示 **Windows 已保护你的电脑**。选择 **更多信息**，确认文件名，然后选择 **仍要运行**。安装程序会为当前用户安装。取消勾选任意一个启动选项，就能改变代理程序何时运行。

代理程序会接受对其自身文件的已签名更新。较新的安装程序会更新随附的 Python。在现有副本上覆盖安装，可以保留设备身份和等待发布的结果。开始菜单中的卸载程序默认也会保留这些内容。它可选的数据删除选项包括发件箱和待处理的已签名记录。

## 构建与测试

请使用干净的代码检出，并让已签名文件采用 LF 换行符。在 x64 Windows 上，从仓库根目录使用全新的构建目录运行 PowerShell 7。构建过程会检查 PATH 中或通常安装位置是否有 Inno Setup 6.3.3 或更高版本。如果缺少编译器，它会使用 Chocolatey 安装 6.3.3。

```powershell
./installer/windows/build.ps1 -BuildDir build
```

`python.lock` 必须包含确切的 3.12 补丁版本号，以及官方 `python-<version>-embed-amd64.zip` 的 64 个字符的 SHA-256。如果要固定一个新版本，请按照 Python 发行页面链接的说明和 Sigstore 包验证该归档文件的真实性，然后记录它的 SHA-256。如果固定信息为空或无效，构建会在下载前停止。[Python 3.12.10 发行版](https://www.python.org/downloads/release/python-31210/)

构建会在解压前验证归档文件。嵌入式解释器只会暂存来自经过验证的发行清单中的文件。安装时，它会在执行候选程序之前再次检查该包，包括其中的文件列表。原装的 `python312._pth` 提供标准库。启动器和候选程序检查会把选定的发行目录添加到 `-I` 模式下的 `sys.path`。

在一个没有安装过 SkyNet 的一次性 Windows 用户配置上，运行冒烟测试。它会静默安装，检查登录注册，以及在没有系统 Python 位于 PATH 时检查命令行工具，然后卸载并检查保留的数据。

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

或者，运行 **Actions → Windows installer → 运行工作流**。冒烟测试通过后，下载 `SkyNetAgentSetup-x64` 构建产物。其中的 `SkyNetAgentSetup-<version>.exe` 和 `.exe.sha256` 是两个需要手动附加到对应 GitHub 发行版的资产。
