# body-territory｜安全跑者的身体底盘知识库

> 用费曼学习法，把跑步安全、力量重建、伤病复盘、ACE-CPT 学习与长期训练记录，沉淀成一个可复用、可追踪、可长期进化的身体系统。

[![学习进度](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FLandjun%2Fbody-territory%2Fmain%2F.github%2Fprogress.json)](#学习进度看板)
[![link-check](https://github.com/Landjun/body-territory/actions/workflows/link-check.yml/badge.svg)](https://github.com/Landjun/body-territory/actions/workflows/link-check.yml)
[![progress-check](https://github.com/Landjun/body-territory/actions/workflows/progress-check.yml/badge.svg)](https://github.com/Landjun/body-territory/actions/workflows/progress-check.yml)

## 一句话定位

> 网络安全是我要成为谁，跑步是我用什么身体去成为那个人。

## 这个仓库是什么

这是安全跑者的身体底盘知识库。
它不是跑量炫耀，不是健身鸡血，也不是资料收藏夹。
它记录我如何把身体训练、疼痛反馈、力量重建、费曼学习和 GitHub 工作流，沉淀成一个长期可维护的个人系统。

## 为什么叫 body-territory

body 是身体。
territory 是领地、边界和可控范围。
训练不是征服身体，而是重新理解身体边界。
每个人的身体结构不同，真正的训练不是强行套用标准答案，而是理解自己的结构、负荷、恢复和边界，然后在安全范围内继续变强。

## 安全跑者

安全跑者不是跑得最快的人。
安全跑者是知道如何长期训练、及时降级、持续复盘、不让身体系统崩盘的人。

> 一个用身体的纪律映照安全的纪律的人。

## 它在我的人生系统里的位置

- **网络安全**：唯一一级人生主线，是圆心，是目的；
- **AI 安全 / Agent 安全**：能力突破方向；
- **Web 安全 / 漏洞复现 / 代码审计 / 区块链安全**：安全能力底座；
- **运营**：当前现金流与业务场景底座；
- **AI**：放大器与提效工具；
- **跑步 / 力量 / 睡眠 / 康复**：身体底盘（本仓库）；
- **费曼学习**：学习与输出方法；
- **GitHub 仓库**：长期证据库与作品集。

身体底盘不是抢主线时间，而是支撑主线：让我有更稳定的身体，去走更长的安全之路。

## 仓库地图

| 模块 | 解决的问题 | 最终产物 | 入口 |
|---|---|---|---|
| 身份定位 | 为什么训练、训练服务什么 | 安全跑者定义、身体底盘说明 | [docs/01-identity](docs/01-identity/README.md) |
| 跑步安全 | 今天能不能跑、怎么跑、跑多少 | 跑前 5 问、疼痛分级、A-E 训练等级 | [docs/02-running-safety](docs/02-running-safety/README.md) |
| 力量重建 | 如何重建臀腿核心踝小腿能力 | 5/20/30 分钟训练模板、动作库 | [docs/03-strength-rebuild](docs/03-strength-rebuild/README.md) |
| 伤病复盘 | 为什么疼、哪里出问题、如何调整 | 伤病日志、右脚踝/小腿复盘、回归跑步清单 | [docs/04-injury-review](docs/04-injury-review/README.md) |
| 训练日志 | 如何持续追踪身体状态 | 日志模板、周报、月报、训练看板 | [docs/05-training-log](docs/05-training-log/README.md) |
| ACE-CPT | 建立运动科学底层理解 | 学习地图、知识卡片、费曼讲稿 | [docs/06-ace-cpt](docs/06-ace-cpt/README.md) |
| 费曼输出 | 把学习转成讲解和作品 | 3 分钟讲稿、10 分钟讲稿、录音工作流 | [docs/07-feynman-output](docs/07-feynman-output/README.md) |
| 安全跑者品牌 | 把真实训练沉淀为长期内容 | 内容卡片、周记录、公众号素材 | [docs/08-safe-runner-brand](docs/08-safe-runner-brand/README.md) |
| 自动化 | 让知识库可维护 | 进度统计、日志生成、CI 检查 | [scripts/](scripts/README.md) |

> 新人请从这里开始:[7 天跑步基座启动计划](docs/00-start-here.md)。
> 资源导航见 [docs/09-resources](docs/09-resources/README.md)。

## 学习进度看板

> 由 `python scripts/update_progress.py` 自动统计 `docs/` 下各模块的任务完成情况并刷新下方表格。

<!-- PROGRESS:START -->
| 模块 | 已完成 | 总任务 | 进度 |
|---|---:|---:|---:|
| 身份定位 | 0 | 14 | 0% |
| 跑步安全 | 0 | 34 | 0% |
| 力量重建 | 0 | 33 | 0% |
| 伤病复盘 | 0 | 30 | 0% |
| 训练日志 | 0 | 19 | 0% |
| ACE-CPT | 0 | 36 | 0% |
| 费曼输出 | 0 | 16 | 0% |
| 安全跑者品牌 | 0 | 5 | 0% |
| 合计 | 0 | 187 | 0% |
<!-- PROGRESS:END -->

## 今日训练前自检

开始训练前，先回答 5 个问题：

1. 昨晚睡了几小时？
2. 今日能量 1-10 分是多少？
3. 腿 / 膝 / 踝 / 足 / 小腿有没有不适？疼痛 0-10 分是多少？
4. 上一次训练后有没有次日加重？
5. 今天可用训练时间是 10 / 20 / 30 / 60 分钟？

如果疼痛等级和训练计划冲突，以疼痛等级为准。详见 [跑前 5 问](docs/02-running-safety/pre-run-checklist.md)。

## 疼痛分级原则

| 疼痛等级 | 判断 | 今日策略 |
|---|---|---|
| 0-2 | 轻微不适或无痛 | 可轻量训练，不做速度训练 |
| 3-4 | 明显不适，有风险 | 不跑步，改快走 + 康复力量 + 拉伸 |
| 5+ | 高风险信号 | 停止跑跳，只做温和活动，必要时咨询专业人士 |
| 次日加重 | 恢复失败信号 | 降级训练，复盘诱因 |
| 步态改变 | 高风险信号 | 停止跑步，优先处理问题 |

完整版见 [疼痛分级](docs/02-running-safety/pain-scale.md)。

## 今日训练等级 A-E

| 等级 | 状态 | 今日策略 |
|---|---|---|
| A | 睡眠好、能量高、无痛 | 完整训练 |
| B | 普通状态、无明显疼痛 | 基础有氧 + 力量 |
| C | 疲劳但无明显疼痛 | 低强度维护 |
| D | 疼痛 3-4 或明显紧张 | 不跑步，康复力量和快走 |
| E | 极低状态或时间极少 | 5 分钟保底动作 |

完整版见 [A-E 训练等级](docs/02-running-safety/training-level-a-e.md)。

## 我的训练原则

- 安全第一；
- 疼痛优先级高于计划；
- 睡眠不足时降级；
- 能量低时降级；
- 不在疼痛状态下做速度训练；
- 快走算训练；
- 力量算训练；
- 康复算训练；
- 拉伸和恢复也算训练；
- 降级不是失败，是纪律；
- 安全完成就是胜利；
- 没有记录，训练就很难变成系统。

## 费曼学习法

我用费曼学习法把"学到的"变成"讲得清的":

```text
学习材料 → 直接讲 → 暴露卡点 → 补学 → 再讲 → 笔记 → 讲稿 → 训练应用 → GitHub 证据
```

完整方法与录音工作流见 [docs/07-feynman-output](docs/07-feynman-output/README.md)。

## 自动化

```bash
python scripts/update_progress.py        # 统计进度并刷新 README 看板
python scripts/new_training_log.py       # 用模板生成今天的训练日志
```

CI 会在每次推送时检查 Markdown 断链与进度看板是否最新。

## 作品集价值

这个仓库不是简历装饰。
它记录我如何把身体训练、费曼学习、自动化脚本和 GitHub 工作流结合起来，形成一个可以长期维护的个人系统。

它展示：

- 我能长期学习；
- 我能结构化复杂问题；
- 我能把经验变成方法论；
- 我能用 GitHub 管理个人知识库；
- 我能把跑步安全和系统安全连接起来；
- 我能把训练记录沉淀成长期证据。

## 免责声明

本仓库仅用于个人学习、训练记录和知识整理，不构成医疗建议、诊断建议或康复处方。若出现持续疼痛、疼痛加重、步态改变、明显肿胀、麻木、功能受限等情况，请及时咨询医生、康复师或其他合格专业人士。

## 许可

知识内容采用 [CC BY 4.0](LICENSE) 许可,欢迎在署名前提下自由引用与分享。
