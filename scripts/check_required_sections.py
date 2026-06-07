#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_required_sections.py — 软性检查 docs 内容页是否包含必要小节(报告为主)。

用法：
    python scripts/check_required_sections.py            # 仅报告,退出 0
    python scripts/check_required_sections.py --strict   # 有缺失则退出 1(供 CI 选用)

检查规则(仅针对 docs/ 下的"内容页",自动跳过 README/索引/模板/示例)：
- 应包含"一句话讲清"或"一句话解释"(费曼核心);
- 若正文涉及 疼痛/伤/损伤/营养/康复/拉伤 等,应包含"免责声明"或"非医疗"字样。

设计原则:默认只报告、不报错,避免误伤(很多页天然不需要这些小节)。
仅依赖 Python 标准库。
"""

import argparse
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# 跳过这些文件名(索引/导航/模板类,不强制要求费曼小节)
SKIP_NAMES = {"README.md", "HOW-TO-USE.md", "PORTFOLIO.md", "00-start-here.md"}
SKIP_KEYWORDS_IN_NAME = ("template", "tracker", "dashboard")

ONELINER_TOKENS = ("一句话讲清", "一句话解释", "一句话定位", "本页目的", "大白话解释")
MEDICAL_TRIGGERS = ("疼痛", "损伤", "伤病", "拉伤", "康复", "营养")
DISCLAIMER_TOKENS = ("免责", "非医疗", "不构成医疗", "咨询医生", "咨询专业人士")


def content_pages():
    if not os.path.isdir(DOCS):
        return
    for root, _dirs, files in os.walk(DOCS):
        for name in files:
            if not name.lower().endswith(".md"):
                continue
            if name in SKIP_NAMES:
                continue
            low = name.lower()
            if any(k in low for k in SKIP_KEYWORDS_IN_NAME):
                continue
            yield os.path.join(root, name)


def main(argv=None):
    parser = argparse.ArgumentParser(description="检查 docs 内容页必要小节")
    parser.add_argument("--strict", action="store_true", help="有缺失则以非零码退出")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    missing_oneliner = []
    missing_disclaimer = []
    checked = 0

    for fp in sorted(content_pages()):
        try:
            with open(fp, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print("WARN: 无法读取 %s: %s" % (fp, e), file=sys.stderr)
            continue
        checked += 1
        rel = os.path.relpath(fp, ROOT).replace("\\", "/")
        if not any(t in text for t in ONELINER_TOKENS):
            missing_oneliner.append(rel)
        if any(t in text for t in MEDICAL_TRIGGERS) and not any(
            t in text for t in DISCLAIMER_TOKENS
        ):
            missing_disclaimer.append(rel)

    print("检查了 %d 个 docs 内容页。" % checked)
    if missing_oneliner:
        print("\n[提示] 缺少「一句话讲清/解释」的页面(%d):" % len(missing_oneliner))
        for r in missing_oneliner:
            print("  - " + r)
    if missing_disclaimer:
        print("\n[警告] 涉及伤病/营养但缺少免责声明的页面(%d):" % len(missing_disclaimer))
        for r in missing_disclaimer:
            print("  - " + r)
    if not missing_oneliner and not missing_disclaimer:
        print("全部通过:费曼小节与免责声明齐全。")

    if args.strict and (missing_oneliner or missing_disclaimer):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
