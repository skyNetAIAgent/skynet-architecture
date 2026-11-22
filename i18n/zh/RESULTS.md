<!-- translation of results/README.md, source sha256: 45df5513ecce206740e2354af46f84e5f3ecf7faccd93a990f4a851df0f249c9 -->

# 研究代理程序的结果

[English](../../results/README.md) · **中文** · [Español](../es/RESULTS.md) · [Français](../fr/RESULTS.md) · [Deutsch](../de/RESULTS.md) · [Italiano](../it/RESULTS.md) · [Русский](../ru/RESULTS.md) · [Português](../pt/RESULTS.md) · [العربية](../ar/RESULTS.md)

此文件夹由 `tools/collect_results.py` 从
[研究代理程序](../../agent/README.md) 的公开结果评论生成：

- `REPORT.md`：一份可读的摘要，包括已验证的发现和冲突；
- `summary.json`：按任务给出的相同内容，供程序使用；
- `coverage.json`：每个任务的每个单元有多少个相互一致的结果。代理程序读取它，以
  优先选择仍缺少结果的单元；它只是一个提示，不需要签名；
- `ai/`：参与者的本地 AI 模型给出的回答，机器生成且未经验证。

当任务所要求数量的不同 GitHub 账号发布了相同的结果哈希时，该单元即被确认。
退出骗局搜索中被报告的每一处“命中”，在列出之前都会由收集器精确地重新计算。任务的含义：
[tasks/README.md](TASKS.md)。

目前还没有从参与者那里收集到任何内容。整个任务列表在单台电脑上的首次运行——尚未被任何
其他人确认——在 [FIRST_RUN.md](FIRST_RUN.md) 中有描述。
