# 使用指南｜如何使用这个知识库

> 这份指南面向两类读者：**我自己**（怎么日常维护这套系统）和**访客**（怎么读懂这个作品是怎么运转的）。
> 全程只需要 Git + Python（仅标准库，无第三方依赖）。

## 目录

- [1. 这个仓库是怎么运转的](#1-这个仓库是怎么运转的)
- [2. 环境准备](#2-环境准备)
- [3. 五分钟上手](#3-五分钟上手)
- [4. 日常工作流](#4-日常工作流)
- [5. 四个自动化脚本详解](#5-四个自动化脚本详解)
- [6. 进度系统是怎么算的](#6-进度系统是怎么算的)
- [7. 怎么写一篇笔记](#7-怎么写一篇笔记)
- [8. 训练日志与复盘](#8-训练日志与复盘)
- [9. 金句卡片](#9-金句卡片)
- [10. 提交与推送](#10-提交与推送)
- [11. GitHub 上的自动化](#11-github-上的自动化)
- [12. 常见问题](#12-常见问题)

---

## 1. 这个仓库是怎么运转的

一句话:**写 Markdown → 跑脚本统计进度 → 提交推送 → GitHub 自动检查并展示**。

```text
            ┌─────────────────────────────────────────────┐
            │  docs/  九大模块知识 + 待办（- [ ] 复选框）   │
            └───────────────┬─────────────────────────────┘
                            │ python scripts/update_progress.py
                            ▼
   README 进度看板 + 各模块小计 + .github/progress.json（徽章数据）
                            │ git commit / push
                            ▼
   GitHub Actions：断链检查 link-check + 进度校验 progress-check
```

知识在 `docs/`，模板在 `templates/`，自动化在 `scripts/`，训练日志在 `logs/`，CI 与协作模板在 `.github/`。

---

## 2. 环境准备

### 必需

- **Git**
- **Python 3.8+**（脚本只用标准库，不需要 `pip install` 任何东西）

检查：

```bash
git --version
python --version
```

> 本机说明：这台机器上 Python 是便携版,不在 PATH 里。本地跑脚本时用全路径
> `C:\Users\Administrator\python-embed\python.exe` 代替下文的 `python` 即可；
> GitHub Actions 上用的是云端 Python，不受影响。

### 克隆（访客 / 换机器时）

```bash
git clone https://github.com/Landjun/body-territory.git
cd body-territory
```

---

## 3. 五分钟上手

```bash
# 1) 生成今天的训练日志
python scripts/new_training_log.py

# 2) 打开 logs/2026/2026-06-04-training-log.md 填几项（睡眠/能量/疼痛/训练等级）

# 3) 学一个知识点：建一篇费曼笔记
python scripts/new_feynman_note.py --slug lactate-threshold --title "乳酸阈" --module 06-ace-cpt

# 4) 把笔记里能讲清楚的待办 - [ ] 改成 - [x]，然后刷新进度
python scripts/update_progress.py

# 5) 提交
git add .
git commit -m "docs: 今日训练与乳酸阈笔记"
git push
```

完成后 README 顶部的进度徽章、看板、各模块小计都会更新。

---

## 4. 日常工作流

### 每天（训练 + 学习）

1. `python scripts/new_training_log.py` 建当天日志，先做[跑前 5 问](02-running-safety/pre-run-checklist.md)；
2. 训练后回填日志的「主观感受」；第二天早上补「次日反馈」；
3. 学知识就 `new_feynman_note.py` 建笔记，边讲边补（见[第 7 节](#7-怎么写一篇笔记)）；
4. `python scripts/update_progress.py` 刷新进度；
5. 提交推送。

### 每周

- 用 [每周身体报告模板](../templates/weekly-body-report-template.md) 写周复盘；
- 更新 [训练看板](05-training-log/training-dashboard.md) 的勾选项；
- `update_progress.py` → 提交。

### 每月

- 用 [每月复盘模板](05-training-log/monthly-review-template.md) 做月度总览。

---

## 5. 四个自动化脚本详解

所有脚本都在 `scripts/`，只依赖 Python 标准库，跨平台。

### 5.1 `update_progress.py` — 进度统计

| 项 | 说明 |
|---|---|
| 作用 | 扫描 `docs/` 所有任务，刷新 README 看板、各模块 README 顶部小计、`.github/progress.json`（徽章数据） |
| 命令 | `python scripts/update_progress.py` |
| 明细 | `python scripts/update_progress.py --detail` 会按文件列出所有未完成项 |
| 产物 | 改写 README 的 `<!-- PROGRESS:START/END -->` 区域；各模块 `<!-- MODULE-PROGRESS:START/END -->` 区域；写出徽章 JSON |

`--detail` 输出示例：

```text
[身份定位] 未完成 18 项
  docs/01-identity/README.md
    - 写一段我自己的身份自述
```

### 5.2 `new_training_log.py` — 建训练日志

| 项 | 说明 |
|---|---|
| 作用 | 用 [训练日志模板](../templates/training-log-template.md) 在 `logs/YYYY/YYYY-MM-DD-training-log.md` 生成日志 |
| 命令 | `python scripts/new_training_log.py` 或 `--date 2026-06-04` |
| 特性 | 自动建年份目录、回填日期、**已存在不覆盖** |

### 5.3 `new_feynman_note.py` — 建费曼笔记

| 项 | 说明 |
|---|---|
| 作用 | 用 [费曼笔记模板](../templates/feynman-note-template.md) 建笔记，回填标题/模块/日期，并**自动在模块 README 里追加链接** |
| 命令 | `python scripts/new_feynman_note.py --slug <英文名> --title "<中文主题>" --module <模块目录>` |
| 参数 | `--slug` 必填（小写连字符，如 `lactate-threshold`）；`--title` 中文主题；`--module` 如 `06-ace-cpt` |
| 落点 | `docs/<module>/<slug>.md`；若 `--module` 不存在则落到 `feynman-notes/` |

示例：

```bash
python scripts/new_feynman_note.py --slug glute-medius --title "臀中肌的作用" --module 03-strength-rebuild
```

### 5.4 `gen_quote_cards.py` — 生成金句卡片

| 项 | 说明 |
|---|---|
| 作用 | 把金句批量渲染成 SVG 卡片到 `docs/08-safe-runner-brand/cards/` |
| 命令 | `python scripts/gen_quote_cards.py` |
| 改金句 | 编辑脚本顶部的 `QUOTES` 列表后重跑即可 |

---

## 6. 进度系统是怎么算的

`update_progress.py` 逐行扫描 `docs/` 下的 Markdown：

**算作"一个任务"的行：**

- 复选框：`- [ ]` / `- [x]` / `- [X]`
- 含关键字的行：`TODO`、`待补充`、`待学习`、`待费曼讲解`、`待整理`、`待转化`
- （标题行如 `## 待补充` **不计入**，避免虚高）

**算作"已完成"的行：**

- 勾选的复选框 `- [x]`
- 含 `✅` / `status: done` / `状态：已完成` / `状态：done` 的任务行

**想让某项变成"已完成"**：把对应的 `- [ ]` 改成 `- [x]`，再跑一次脚本。

进度展示在三处,全部自动同步：README 顶部**徽章**、README **看板表格**、每个模块 README 顶部的**小计行**。

---

## 7. 怎么写一篇笔记

这个仓库用**费曼学习法**：讲不清楚 = 没学会。推荐流程（适合"边看边讲"型）：

1. `new_feynman_note.py` 建笔记；
2. 对着[手表录音笔](07-feynman-output/watch-recorder-workflow.md)**先讲一遍**，讲不顺的地方就是卡点；
3. 把卡点记进笔记的「我卡住的地方」，回资料补学；
4. 再讲一遍，填「3 分钟讲稿」；
5. 能讲清楚后，把「完成标记」里的 `- [ ]` 勾成 `- [x]`。

**命名约定**：文件名英文小写连字符（`lactate-threshold.md`），正文中文。

**看一篇填好的样板**：[乳酸阈 · 费曼样板笔记](../examples/feynman-note-lactate-threshold.md) 演示了完整流程长什么样。

---

## 8. 训练日志与复盘

> 受伤/不适不知从哪查起?先走一遍 [疼痛诱因排查逻辑树](04-injury-review/cause-finding-decision-tree.md)。


- 单次训练 → [每日训练日志模板](05-training-log/daily-log-template.md) / `new_training_log.py`
- 一周 → [每周身体报告模板](../templates/weekly-body-report-template.md)
- 一月 → [每月复盘模板](05-training-log/monthly-review-template.md)
- 受伤/不适 → [伤病复盘模板](../templates/injury-review-template.md)，并对照[疼痛分级](02-running-safety/pain-scale.md)、[红旗信号](02-running-safety/red-flags.md)

> 所有训练/伤病内容均为个人记录，非医疗建议；出现红旗信号请咨询专业人士。

---

## 9. 金句卡片

```bash
python scripts/gen_quote_cards.py
```

生成的 SVG 在 [08-safe-runner-brand/cards/](08-safe-runner-brand/cards/)，可直接当社交平台/公众号配图。SVG 是纯文本，改字、改色、版本对比都方便。想增减金句，改 `scripts/gen_quote_cards.py` 里的 `QUOTES` 列表。

> 也可以什么都不做：推送后 GitHub Action 会在生成器变化时自动重生成并提交（见下一节）。

---

## 10. 提交与推送

提交信息用约定式格式：

| 前缀 | 用于 |
|---|---|
| `docs:` | 笔记、日志、文档内容 |
| `feat:` | 新脚本/新功能 |
| `ci:` | 工作流、协作模板 |
| `chore:` | 杂项维护 |

```bash
git add .
git commit -m "docs: add lactate-threshold feynman note"
git push
```

---

## 11. GitHub 上的自动化

- **link-check**（`.github/workflows/link-check.yml`）：每次 push / PR 用 lychee 检查 Markdown 断链。
- **progress-check**（`.github/workflows/progress-check.yml`）：跑 `update_progress.py` 并校验 README 看板是否最新——提醒我提交前别忘了刷新进度。
- **quote-cards**（`.github/workflows/quote-cards.yml`）：改了 `gen_quote_cards.py` 后自动重生成卡片并提交。
- **Issue 模板**：在 GitHub 上点 New issue，可选「训练日志 / 伤病复盘 / 费曼笔记」表单。
- **PR 模板**：开 PR 时自动带上更新类型清单。

---

## 12. 常见问题

**Q：脚本报错找不到 README 标记？**
A：README 里必须保留 `<!-- PROGRESS:START -->` 和 `<!-- PROGRESS:END -->` 两行，别删。

**Q：进度一直是 0%？**
A：所有任务初始都是 `- [ ]`。把能讲清楚/已完成的改成 `- [x]` 再跑脚本。

**Q：Windows 控制台打印中文是乱码？**
A：只是终端编码显示问题，写入的文件是 UTF-8，正常。脚本已把输出切到 UTF-8。

**Q：徽章不更新？**
A：徽章读 `.github/progress.json`，跑完 `update_progress.py` 要把它一起提交推送；shields.io 有几分钟缓存。

**Q：我能不能不用脚本，纯手写？**
A：可以。脚本只是省事；进度看板也可以手填，但建议用脚本保持一致。

---

> 回到 [仓库首页](../README.md) · 新手先看 [7 天启动计划](00-start-here.md)。
