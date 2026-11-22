<!-- translation of CORE.md, source sha256: bf365ef474bbcbb38228177243cd54e909c8bf626180103b058e7126414cf4b4 -->

# SkyNet 的不可变基础

[English](../../CORE.md) · **中文** · [Español](../es/CORE.md) · [Français](../fr/CORE.md) · [Deutsch](../de/CORE.md) · [Italiano](../it/CORE.md) · [Русский](../ru/CORE.md) · [Português](../pt/CORE.md) · [العربية](../ar/CORE.md)

**什么属于基础（第 1 版，2026 年 11 月 22 日）：** README、宣言和强制性要求，以本仓库的每一种语言：

- `README.md`、`MANIFESTO.md`、`REQUIREMENTS.md`（英文）；
- `i18n/<lang>/README.md`、`i18n/<lang>/MANIFESTO.md`、`i18n/<lang>/REQUIREMENTS.md`
  用于 `ru zh es fr de it pt ar`。

标准版本是俄文版（`i18n/ru/`）。当译文出现分歧时，以它为准。

**基础是如何固定的：**

1. **指纹。** 每个基础文件的 SHA-256 指纹都列在 [CORE_HASHES.txt](../../CORE_HASHES.txt) 中。任何人都可以检查副本：`sha256sum -c CORE_HASHES.txt`（Linux/macOS），或与 `Get-FileHash`（Windows）比较。
2. **标签 `core-v1`。** 包含第 1 版基础的提交用标签 `core-v1` 标记。
3. **自动检查。** 每次 pull request 和 push 都会运行一项检查：如果任何基础文件或 `CORE_HASHES.txt` 与第 1 版不一致，检查就会失败。
4. **许可。** 基础文本采用 CC BY-ND 4.0 许可：可以原样复制和分享，但不得分发修改过的版本。
5. **未来的网络软件。** 基础的指纹应写入网络账本的不可变核心，软件必须拒绝在与之相抵触的规则下运行。这是对未来软件的要求；该软件尚不存在。
6. **副本。** 每个 fork、clone 和存档都保留原始文本及其指纹，因此任何地方的变化都可以通过比对被发现。

**诚实的界限。** 从技术上，没有人能禁止 GitHub 组织的所有者更改仓库设置，任何人都可以 fork 文本并编辑自己的副本。可以保证的则是另一回事：对基础的任何改动都是**可见的**，因为它会破坏已发布的指纹，而基础不同的项目就不是 SkyNet。错别字和翻译错误记录在 [ERRATA.md](ERRATA.md) 中，而不改动基础文件。
