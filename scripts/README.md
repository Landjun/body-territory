# scripts｜自动化脚本

让这个知识库可以长期、低成本地维护。仅依赖 Python 标准库，跨平台可用。

## 脚本一览

| 脚本 | 作用 |
|---|---|
| `update_progress.py` | 扫描 `docs/` 各模块的任务（复选框 / 待补充等关键字），统计完成度，刷新 README 看板、各模块 README 顶部小计，并写出 `.github/progress.json`（README 顶部 shields 徽章读取它）。`--detail` 可按文件列出未完成项 |
| `new_training_log.py` | 用 `templates/training-log-template.md` 在 `logs/YYYY/YYYY-MM-DD-training-log.md` 生成当天训练日志，自动建目录、不覆盖已有文件 |
| `new_feynman_note.py` | 用 `templates/feynman-note-template.md` 创建一篇费曼笔记，回填主题/模块/日期，落到 `docs/<module>/<slug>.md` |
| `gen_quote_cards.py` | 根据金句列表批量生成安全跑者金句卡片 SVG 到 `docs/08-safe-runner-brand/cards/` |
| `check_links.py` | 扫描全仓库 Markdown 的内部相对链接，列出断链并以非零码退出（提交前本地自查，与 CI 的 lychee 互补） |
| `check_required_sections.py` | 软性检查 `docs/` 内容页是否含「一句话讲清/本页目的」与（涉伤病/营养时）免责声明；默认只报告，`--strict` 才报错 |

## 日常工作流

```bash
# 1. 开始训练前，生成今天的训练日志
python scripts/new_training_log.py

# 也可以补记某一天
python scripts/new_training_log.py --date 2026-06-04

# 2. 学习 / 复盘 / 勾掉待办后，刷新进度看板
python scripts/update_progress.py

# 3. 提交前自查链接与小节
python scripts/check_links.py
python scripts/check_required_sections.py

# 4. 提交
git add .
git commit -m "docs: update training log and progress"
git push
```

## 进度统计规则

`update_progress.py` 逐行判断：

- **任务行**：Markdown 复选框 `- [ ]` / `- [x]` / `- [X]`，或包含关键字 `TODO`、`待补充`、`待学习`、`待费曼讲解`、`待整理`、`待转化` 的行。
- **完成行**：勾选的复选框 `- [x]`，或包含 `✅`、`status: done`、`状态：已完成`、`状态：done` 的任务行。

> 想让某个任务计入"已完成"，把对应的 `- [ ]` 改成 `- [x]` 即可。
