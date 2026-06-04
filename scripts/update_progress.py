#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_progress.py — 统计 docs/ 下各模块的任务完成情况，并刷新 README.md 中的进度看板。

用法：
    python scripts/update_progress.py

实现要点：
- 只依赖 Python 标准库；
- 跨平台（Windows / Linux / macOS）；
- 以 UTF-8 读写，写回时统一使用 LF 行尾（与 .gitattributes 保持一致）；
- 找不到 README 的 <!-- PROGRESS:START --> / <!-- PROGRESS:END --> 标记时报错退出；
- 没有任何任务时不会崩溃，按 0% 处理；
- 不会破坏 README 标记区域以外的任何内容。

任务与完成的识别规则（逐行判断，每个匹配行计为 1 个任务）：
- 任务行：
    * Markdown 复选框        - [ ] / - [x] / - [X]
    * 含关键字的行           TODO / 待补充 / 待学习 / 待费曼讲解 / 待整理 / 待转化
- 完成行（在任务行基础上判断）：
    * 勾选的复选框           - [x] / - [X]
    * 含完成标记的关键字行    ✅ / status: done / 状态：已完成 / 状态：done
"""

import os
import re
import sys

# 仓库根目录 = 本脚本所在目录的上一级
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
README = os.path.join(ROOT, "README.md")

START_MARK = "<!-- PROGRESS:START -->"
END_MARK = "<!-- PROGRESS:END -->"

# 进度看板里展示的 8 个一级模块：目录名 -> 显示名（顺序即表格顺序）
MODULES = [
    ("01-identity", "身份定位"),
    ("02-running-safety", "跑步安全"),
    ("03-strength-rebuild", "力量重建"),
    ("04-injury-review", "伤病复盘"),
    ("05-training-log", "训练日志"),
    ("06-ace-cpt", "ACE-CPT"),
    ("07-feynman-output", "费曼输出"),
    ("08-safe-runner-brand", "安全跑者品牌"),
]

CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]")
TASK_KEYWORDS = ("TODO", "待补充", "待学习", "待费曼讲解", "待整理", "待转化")
DONE_TOKENS = ("✅", "status: done", "状态：已完成", "状态：done")


def classify_line(line):
    """返回 (是否任务行, 是否已完成)。"""
    m = CHECKBOX_RE.match(line)
    if m:
        return True, m.group(1) in ("x", "X")
    if any(k in line for k in TASK_KEYWORDS):
        done = any(t in line for t in DONE_TOKENS)
        return True, done
    return False, False


def count_dir(path):
    """统计某模块目录下所有 .md 文件的任务总数与完成数。"""
    total = 0
    done = 0
    if not os.path.isdir(path):
        return total, done
    for root, _dirs, files in os.walk(path):
        for name in files:
            if not name.lower().endswith(".md"):
                continue
            fp = os.path.join(root, name)
            try:
                with open(fp, encoding="utf-8") as f:
                    for line in f:
                        is_task, is_done = classify_line(line)
                        if is_task:
                            total += 1
                            if is_done:
                                done += 1
            except OSError as e:
                print("WARN: 无法读取 %s: %s" % (fp, e), file=sys.stderr)
    return total, done


def build_table(stats):
    """根据统计结果生成 Markdown 表格字符串。"""
    rows = ["| 模块 | 已完成 | 总任务 | 进度 |", "|---|---:|---:|---:|"]
    grand_total = 0
    grand_done = 0
    for dirname, label in MODULES:
        total, done = stats[dirname]
        grand_total += total
        grand_done += done
        pct = round(100 * done / total) if total else 0
        rows.append("| %s | %d | %d | %d%% |" % (label, done, total, pct))
    gpct = round(100 * grand_done / grand_total) if grand_total else 0
    rows.append("| 合计 | %d | %d | %d%% |" % (grand_done, grand_total, gpct))
    return "\n".join(rows), grand_total, grand_done, gpct


def main():
    stats = {}
    for dirname, _label in MODULES:
        stats[dirname] = count_dir(os.path.join(DOCS, dirname))

    table, total, done, pct = build_table(stats)

    if not os.path.isfile(README):
        print("ERROR: 找不到 README.md: %s" % README, file=sys.stderr)
        return 1

    with open(README, encoding="utf-8") as f:
        content = f.read()

    if START_MARK not in content or END_MARK not in content:
        print(
            "ERROR: README.md 中缺少进度标记 %s / %s" % (START_MARK, END_MARK),
            file=sys.stderr,
        )
        return 1

    pre = content.split(START_MARK)[0]
    post = content.split(END_MARK, 1)[1]
    new_content = pre + START_MARK + "\n" + table + "\n" + END_MARK + post

    if new_content != content:
        with open(README, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)

    print("Updated README progress table.")
    print("Total tasks: %d" % total)
    print("Done tasks: %d" % done)
    print("Progress: %d%%" % pct)
    return 0


if __name__ == "__main__":
    sys.exit(main())
