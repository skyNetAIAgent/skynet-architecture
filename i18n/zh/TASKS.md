<!-- translation of tasks/README.md, source sha256: f0685cfe87baef739cff7ff9121f8ab2fd0aed86866b5638fd79dcdd347c1916 -->

# 研究代理程序的任务

[English](../../tasks/README.md) · **中文** · [Español](../es/TASKS.md) · [Français](../fr/TASKS.md) · [Deutsch](../de/TASKS.md) · [Italiano](../it/TASKS.md) · [Русский](../ru/TASKS.md) · [Português](../pt/TASKS.md) · [العربية](../ar/TASKS.md)

本文件夹存放[研究代理程序](../../agent/README.md)领取的工作：

- [`index.json`](../../tasks/index.json)：当前任务列表；
- `index.json.sig`：它的签名（没有有效签名的列表会被代理程序忽略）；
- [`context/`](../../tasks/context)：AI 问题所引用的冻结文本。

结果以评论的形式出现在每个任务的跟踪 issue 中，并被汇总到
[`results/`](../../results)，由 `tools/collect_results.py` 完成。

## 什么是任务

任务是一份数据：内置于代理程序中的计算的名称（即“内核”）、它的参数，以及工作被拆分成的独立片段（“分片”）的数量。任务不能携带代码。一种新的计算类型需要代理程序的一个新的已签名版本。

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

没有调度器。每个代理程序随机挑选一个它尚未完成的分片。多个代理程序落到同一个分片是有意为之：所有计算内核都是精确的整数运算，因此在每台设备上，相同的工作得到相同的数字；当 `redundancy` 个不同的 GitHub 账号发布相同的哈希值时，一个分片才算得到确认。一个分片出现不同的哈希值就是冲突，由维护者重新计算来解决。

## 代理程序 0.1 中的内核

| 内核 | 它计算什么 | 来源 |
|---|---|---|
| `selftest@1` | 固定的整数工作量；每台设备都必须返回相同的摘要 | [selftest.py](../../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | 在一族策略上，提交伪造结果并离开的参与者的精确期望收益；报告胜过诚实离开的策略 | [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | 当只有经核查的任务才获得支付时，出现亏损月份或季度的精确概率 | [lottery_b.py](../../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | 可选：一个交给参与者运行的本地 AI 模型的问题 | [ai_answer.py](../../agent/skynet_agent/kernels/ai_answer.py) |

每个源文件都以它所实现的精确模型开头，这样任何人都能独立地重新计算出一个结果。

## 当前发布的任务及其原因

所有这些都涉及项目的主要开放问题：能否以低廉的代价让作弊变得无用（[OPEN_QUESTIONS, Q1](../../docs/OPEN_QUESTIONS.en.md)）。

| 任务 | 问题 |
|---|---|
| `selftest-1` | 流水线在你的设备上能正常工作吗？ |
| `exit-a-honest-check` | 在没有合谋的情况下，离开之前有没有任何办法靠伪造获利？设计给出的答案是没有 |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | 在任务都同样小的情况下：合谋验证者的份额达到多少时，带着伪造结果离开才有利可图？设计的估计约为 91% |
| `exit-a-uniform-cap-h399` | 同样的问题，但采用提议的限制“待处理金额中最多三分之一用于工作”，分三波进行 |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | 当任务可以有任意大小时，在有和没有该限制的情况下，同样的问题 |
| `lottery-b-table` | 如果只有经核查的任务才获得支付，一个小参与者出现亏损月份的频率有多高？ |
| `ask-variant-b-attack` | 针对本地 AI 模型：找到一种对“网络只为经核查的工作付费”的新攻击 |

这些是对设计文档中所写规则的计算。它们既不是对硬件的测量，也不是对网络的实验。测量类任务（例如，整数推理在不同显卡上是否会得到相同的比特）只有在项目维护者开放实验之后才会发布。

## 提议一个任务

打开一个标题为 `[Task] …` 的 issue，并说明：

1. 该计算要回答的问题，以及它属于哪个开放问题；
2. 精确的模型，以便能够独立地重新计算；
3. 哪个内核和参数能完成它，或者一个新内核必须计算什么；
4. 错误或伪造的结果会如何被发现。

维护者用 `tools/sign_tasks.py --check` 检查任务，将其加入 `index.json` 并对列表签名。只有发布密钥的持有者才能签名；参见
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md)。
