# 训练日志

<!-- MODULE-PROGRESS:START -->
> 模块进度：0 / 19 项已完成（0%）。运行 `python scripts/update_progress.py` 刷新。
<!-- MODULE-PROGRESS:END -->

> 没有记录，训练就很难变成系统。
> 没有复盘，疼痛就只会重复出现。

## 这个模块为什么存在

- 训练日志不是为了打卡；
- 是为了形成反馈；
- 是为了防止重复受伤；
- 是为了让身体训练变成长期证据。

## 日志体系

| 文件 | 用途 |
|---|---|
| [每日训练日志模板](daily-log-template.md) | 单次训练记录 |
| [每周复盘模板](weekly-review-template.md) | 一周趋势与调整 |
| [每月复盘模板](monthly-review-template.md) | 一月总览与方向 |
| [训练看板](training-dashboard.md) | 当前状态与本周目标 |
| [身体信号库](body-signals.md) | 各类信号如何影响决策 |

## 生成日志

```bash
python scripts/new_training_log.py            # 今天
python scripts/new_training_log.py --date 2026-06-04
```

生成的日志保存在 `logs/YYYY/`。

## 待补充

- [ ] 累计第一周的真实日志
- [ ] 写出第一份真实周报
