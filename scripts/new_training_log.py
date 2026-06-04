#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_training_log.py — 用模板快速生成某一天的训练日志文件。

用法：
    python scripts/new_training_log.py
    python scripts/new_training_log.py --date 2026-06-04

行为：
- 读取 templates/training-log-template.md 作为内容来源；
- 在 logs/YYYY/YYYY-MM-DD-training-log.md 生成日志，并自动创建目录；
- 若目标文件已存在，则不覆盖（保护已有记录）；
- 自动把模板中的"日期："一行填上目标日期；
- 输出最终生成路径。

仅依赖 Python 标准库。
"""

import argparse
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "templates", "training-log-template.md")
LOGS_DIR = os.path.join(ROOT, "logs")


def parse_args(argv):
    parser = argparse.ArgumentParser(description="生成某一天的训练日志文件")
    parser.add_argument(
        "--date",
        help="日志日期，格式 YYYY-MM-DD，默认今天",
        default=None,
    )
    return parser.parse_args(argv)


def resolve_date(value):
    if value is None:
        return datetime.date.today()
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit("ERROR: 日期格式应为 YYYY-MM-DD，收到: %s" % value)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    day = resolve_date(args.date)
    date_str = day.strftime("%Y-%m-%d")

    if not os.path.isfile(TEMPLATE):
        print("ERROR: 找不到模板: %s" % TEMPLATE, file=sys.stderr)
        return 1

    with open(TEMPLATE, encoding="utf-8") as f:
        content = f.read()

    # 把模板里的"- 日期："补上目标日期（只替换第一处）
    if "- 日期：" in content:
        content = content.replace("- 日期：", "- 日期：%s" % date_str, 1)

    target_dir = os.path.join(LOGS_DIR, day.strftime("%Y"))
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "%s-training-log.md" % date_str)

    if os.path.exists(target):
        print("已存在，未覆盖: %s" % target)
        return 0

    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print("已生成训练日志: %s" % target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
