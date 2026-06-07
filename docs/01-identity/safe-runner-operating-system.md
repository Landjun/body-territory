# 安全跑者操作系统(总系统)

> 一句话讲清:这个仓库不是知识堆,而是一个由八个子系统组成的"操作系统"——它让一个想长期走网络安全道路的人,用身体纪律、训练复盘、风险控制、费曼输出和 GitHub 工程化,把身体变成长期主义的底盘。

## 这篇解决什么问题

它是整个 body-territory 的"系统总览图":告诉访客(和未来的我)——这里的每个模块不是孤立的笔记目录,而是一个互相咬合的系统;以及这套系统每天、每周、长期是怎么转起来的。

## 八个子系统

| # | 子系统 | 解决的问题 | 入口 |
|---|---|---|---|
| 1 | **安全跑者身份系统** | 我为什么训练、训练服务什么 | [本模块](README.md)、[宣言](safe-runner-manifesto.md) |
| 2 | **身体底盘操作系统** | 把身体当系统来运维 | [身体作为安全系统](body-as-security-system.md) |
| 3 | **跑步安全决策系统** | 今天能不能跑、怎么跑、跑多少 | [docs/02](../02-running-safety/README.md) |
| 4 | **伤病复盘与负荷管理系统** | 为什么疼、怎么降级、怎么回归 | [docs/04](../04-injury-review/README.md)、[负荷管理](../../02-injury-free-running/concepts/load-management-10-percent.md) |
| 5 | **运动科学学习系统** | 解剖生理 / 无伤跑法 / ACE-CPT | [docs/06](../06-ace-cpt/README.md)、[01-body-systems](../../01-body-systems/README.md)、[02-injury-free-running](../../02-injury-free-running/README.md)、[03-ace-cpt](../../03-ace-cpt/README.md) |
| 6 | **费曼输出与录音讲解系统** | 把知识讲清、用上、留下来 | [docs/07](../07-feynman-output/README.md) |
| 7 | **长期训练日志与证据系统** | 把训练变成可追踪的证据链 | [docs/05](../05-training-log/README.md)、[logs/](../../logs/) |
| 8 | **GitHub 作品集展示系统** | 对外证明长期主义与工程化能力 | [PORTFOLIO](../PORTFOLIO.md)、[README](../../README.md) |

## 它们怎么咬合成一个闭环

```text
身份(为什么练)
   │
   ▼
学习系统(懂身体/懂跑法/懂科学)──┐
   │                              │ 原理支撑
   ▼                              ▼
决策系统(今天能不能跑)── 负荷管理 ── 力量重建(加固漏洞)
   │                              ▲
   ▼                              │ 找根因/降级/回归
训练 ──► 训练日志(记录证据) ──► 伤病复盘(出问题时)
   │                              
   ▼                              
费曼输出(把这一切讲清、留下) ──► GitHub 作品集(长期证据)
   │
   └──► 反哺身份:我确实在用工程化方式管理身体与学习
```

## 三个运行节奏

**每天**:跑前用[跑前 5 问](../02-running-safety/pre-run-checklist.md)+[疼痛分级](../02-running-safety/pain-scale.md)定[A-E 等级](../02-running-safety/training-level-a-e.md) → 训练(含快走/力量/康复)→ 记[训练日志](../05-training-log/daily-log-template.md) → 看次日反馈。

**每周**:[周身体报告](../../templates/weekly-body-report-template.md) → 跑一次 `python scripts/update_progress.py` 刷新看板 → 把一个知识点走完[费曼流程](../07-feynman-output/README.md)。

**长期**:周期化推进、ACE-CPT 学习、内容沉淀;GitHub 提交历史与两个徽章(进度、连续训练)成为长期主义的客观证据。

## 和网络安全纪律的关系

这八个子系统,几乎一一对应安全工程的工作流:身份=使命与红线,学习=威胁情报,决策=风险评估,复盘=事件响应,力量=基础设施加固,日志=审计留痕,输出=技术分享/报告,作品集=能力证明。**我在身体上跑通这套闭环,就是在为系统安全预演同一套纪律。**

## 常见误区

- 把模块当孤立目录读——它们是一个闭环,缺一环就漏;
- 只建系统不运行它——系统的价值在每天真实地用;
- 把"操作系统"当噱头——它必须真的能指导今天的训练决策。

## 今天可以怎么用

照"每天"节奏走一遍最小闭环:答 5 问 → 定等级 → 做(哪怕 5 分钟保底)→ 记一条日志。跑通一次,就理解了整个系统。

## 关联阅读

- [使用指南 HOW-TO-USE](../HOW-TO-USE.md) · [作品说明 PORTFOLIO](../PORTFOLIO.md) · [7 天启动](../00-start-here.md)
- [安全跑者宣言](safe-runner-manifesto.md) · [身体作为安全系统](body-as-security-system.md)
