#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_progress.py — 统计 docs/ 下各模块的任务完成情况，刷新 README 进度看板，
并刷新每个模块 README 顶部的进度小计。

用法：
    python scripts/update_progress.py            # 统计并刷新
    python scripts/update_progress.py --detail   # 额外按文件列出所有未完成项

实现要点：
- 只依赖 Python 标准库；
- 跨平台（Windows / Linux / macOS）；
- 以 UTF-8 读写，写回时统一使用 LF 行尾（与 .gitattributes 保持一致）；
- 找不到 README 的 <!-- PROGRESS:START --> / <!-- PROGRESS:END --> 标记时报错退出；
- 模块 README 若含 <!-- MODULE-PROGRESS:START/END --> 标记则刷新其小计，没有则跳过；
- 没有任何任务时不会崩溃，按 0% 处理；
- 不会破坏标记区域以外的任何内容。

任务与完成的识别规则（逐行判断，每个匹配行计为 1 个任务）：
- 任务行：
    * Markdown 复选框        - [ ] / - [x] / - [X]
    * 含关键字的行           TODO / 待补充 / 待学习 / 待费曼讲解 / 待整理 / 待转化
- 完成行（在任务行基础上判断）：
    * 勾选的复选框           - [x] / - [X]
    * 含完成标记的关键字行    ✅ / status: done / 状态：已完成 / 状态：done
"""

import argparse
import io
import os
import re
import sys

# Windows 控制台默认可能是 GBK，这里把标准输出切到 UTF-8，避免中文打印乱码/报错
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 仓库根目录 = 本脚本所在目录的上一级
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
README = os.path.join(ROOT, "README.md")

START_MARK = "<!-- PROGRESS:START -->"
END_MARK = "<!-- PROGRESS:END -->"
MOD_START = "<!-- MODULE-PROGRESS:START -->"
MOD_END = "<!-- MODULE-PROGRESS:END -->"

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
    """返回 (是否任务行, 是否已完成, 任务文本)。"""
    m = CHECKBOX_RE.match(line)
    if m:
        text = CHECKBOX_RE.sub("", line, count=1).strip()
        return True, m.group(1) in ("x", "X"), text or "(空任务)"
    # 标题行（如 "## 待补充"）本身不是任务，避免把小节标题计入
    if line.lstrip().startswith("#"):
        return False, False, ""
    if any(k in line for k in TASK_KEYWORDS):
        done = any(t in line for t in DONE_TOKENS)
        return True, done, line.strip()
    return False, False, ""


def scan_dir(path):
    """统计目录下所有 .md 的任务。返回 (total, done, details)。

    details = [(相对路径, [未完成任务文本, ...]), ...]
    """
    total = 0
    done = 0
    details = []
    if not os.path.isdir(path):
        return total, done, details
    for root, _dirs, files in os.walk(path):
        for name in sorted(files):
            if not name.lower().endswith(".md"):
                continue
            fp = os.path.join(root, name)
            unfinished = []
            try:
                with open(fp, encoding="utf-8") as f:
                    for line in f:
                        is_task, is_done, text = classify_line(line)
                        if is_task:
                            total += 1
                            if is_done:
                                done += 1
                            else:
                                unfinished.append(text)
            except OSError as e:
                print("WARN: 无法读取 %s: %s" % (fp, e), file=sys.stderr)
                continue
            if unfinished:
                details.append((os.path.relpath(fp, ROOT), unfinished))
    return total, done, details


def update_module_readme(dirpath, total, done):
    """刷新某模块 README 顶部 MODULE-PROGRESS 标记之间的小计行。"""
    readme = os.path.join(dirpath, "README.md")
    if not os.path.isfile(readme):
        return
    with open(readme, encoding="utf-8") as f:
        content = f.read()
    if MOD_START not in content or MOD_END not in content:
        return
    pct = round(100 * done / total) if total else 0
    line = "> 模块进度：%d / %d 项已完成（%d%%）。运行 `python scripts/update_progress.py` 刷新。" % (
        done,
        total,
        pct,
    )
    pre = content.split(MOD_START)[0]
    post = content.split(MOD_END, 1)[1]
    new_content = pre + MOD_START + "\n" + line + "\n" + MOD_END + post
    if new_content != content:
        with open(readme, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)


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


def main(argv=None):
    parser = argparse.ArgumentParser(description="统计学习进度并刷新看板")
    parser.add_argument(
        "--detail",
        action="store_true",
        help="按文件列出所有未完成任务项",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    stats = {}
    details_all = {}
    for dirname, _label in MODULES:
        total, done, details = scan_dir(os.path.join(DOCS, dirname))
        stats[dirname] = (total, done)
        details_all[dirname] = details
        update_module_readme(os.path.join(DOCS, dirname), total, done)

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

    if args.detail:
        print("\n未完成明细：")
        for dirname, label in MODULES:
            details = details_all[dirname]
            if not details:
                continue
            count = sum(len(items) for _f, items in details)
            print("\n[%s] 未完成 %d 项" % (label, count))
            for relpath, items in details:
                print("  %s" % relpath.replace("\\", "/"))
                for text in items:
                    print("    - %s" % text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
