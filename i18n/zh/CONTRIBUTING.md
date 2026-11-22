# 如何贡献

[English](../../CONTRIBUTING.md) · **中文** · [Español](../es/CONTRIBUTING.md) · [Français](../fr/CONTRIBUTING.md) · [Deutsch](../de/CONTRIBUTING.md) · [Italiano](../it/CONTRIBUTING.md) · [Русский](../ru/CONTRIBUTING.md) · [Português](../pt/CONTRIBUTING.md) · [العربية](../ar/CONTRIBUTING.md)

感谢你愿意帮忙。这里重要的是精确而不是篇幅：一个附有具体场景的漏洞，比十页泛泛而谈更有价值。

## 可以带来什么

- **对当前设计的攻击。** 一个场景：谁在行动、做了什么、得到什么、为什么网络没有发现。注明 [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md) 的章节。
- **对[开放问题](../../docs/OPEN_QUESTIONS.en.md)的解决方案。**
- **来源**：解决了部分问题的论文、协议或项目，注明版本、日期，以及它对我们的情况**没有**证明什么。
- **成本计算**或对现有计算的修正。
- **翻译修正**：基础文本译本中的不准确之处（通过勘误文件）。
- **给研究代理程序的任务**：能回答某个开放问题一部分的计算（见 [tasks/README.md](../../tasks/README.md)）。
- **算力**：如果你没有人工智能助手，也没有时间撰写，可以在电脑或手机上运行[研究代理程序](AGENT.md)。

## 如何提交

提交 issue，标题以标签开头：

| 标签 | 用途 |
|---|---|
| `[Attack]` | 欺骗或破坏网络的方法 |
| `[Q<N>]` | 针对开放问题 N 的提议 |
| `[Source]` | 有用的论文或项目 |
| `[Cost]` | 成本估计或数字修正 |
| `[Translation]` | 翻译不准确 |
| `[Task]` | 给研究代理程序的计算 |

正文中说明：

1. 保证什么，在什么假设下。
2. 机制。
3. 已知的攻击以及剩下的风险。
4. 成本，标注 [计算] 或 [实测]。
5. 六项[要求](REQUIREMENTS.md)中满足了哪些，没有满足哪些。

欢迎对工作文档（`docs/`）提交 pull request。改变某项的状态时，请说明原因。issue 和 pull request 可以用仓库中的任何一种语言撰写。

## 规则

- **基础不变。** 修改宣言、要求、README 或其指纹的 pull request 不会被接受。见 [CORE.md](../../CORE.md)。
- 计算不冒充测量，提议不冒充决定。
- 不要公开密钥、密码、个人数据或计算机地址。
- 礼貌、切题。批评想法，而不是批评人。

如果你与人工智能助手一起工作，请把 [AGENTS.md](AGENTS.md) 交给它。issue 的作者对其文本的准确性负责。
