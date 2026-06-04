#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_feynman_note.py — 用费曼笔记模板一键创建一篇新笔记。

用法：
    python scripts/new_feynman_note.py --slug lactate-threshold --title "乳酸阈" --module 06-ace-cpt
    python scripts/new_feynman_note.py --slug glute-medius --title "臀中肌"   # 无 module 时落到 feynman-notes/

行为：
- 读取 templates/feynman-note-template.md；
- 文件名用英文 slug（小写连字符，符合本仓库命名约定）；
- --module 给定且 docs/<module> 存在时，笔记落到该模块目录；否则落到仓库根的 feynman-notes/；
- 自动回填模板里的 主题 / 所属模块 / 日期；
- 已存在则不覆盖；
- 输出生成路径。

仅依赖 Python 标准库。
"""

import argparse
import datetime
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "templates", "feynman-note-template.md")
DOCS = os.path.join(ROOT, "docs")

MODULE_NAMES = {
    "01-identity": "身份定位",
    "02-running-safety": "跑步安全",
    "03-strength-rebuild": "力量重建",
    "04-injury-review": "伤病复盘",
    "05-training-log": "训练日志",
    "06-ace-cpt": "ACE-CPT",
    "07-feynman-output": "费曼输出",
    "08-safe-runner-brand": "安全跑者品牌",
    "09-resources": "资源",
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

AUTO_START = "<!-- AUTO-NOTES:START -->"
AUTO_END = "<!-- AUTO-NOTES:END -->"


def link_in_module_readme(out_dir, slug, title):
    """在模块 README 的「自动收录笔记」区块追加新笔记链接（幂等）。"""
    readme = os.path.join(out_dir, "README.md")
    if not os.path.isfile(readme):
        return False
    with open(readme, encoding="utf-8") as f:
        content = f.read()
    if ("(%s.md)" % slug) in content:
        return False  # 已有链接，跳过
    bullet = "- [%s](%s.md)" % (title or slug, slug)
    if AUTO_START in content and AUTO_END in content:
        head, rest = content.split(AUTO_END, 1)
        new_content = head.rstrip() + "\n" + bullet + "\n" + AUTO_END + rest
    else:
        block = "\n%s\n## 自动收录笔记\n\n%s\n%s\n" % (AUTO_START, bullet, AUTO_END)
        new_content = content.rstrip() + "\n" + block
    with open(readme, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    return True


def parse_args(argv):
    p = argparse.ArgumentParser(description="用费曼模板创建一篇新笔记")
    p.add_argument("--slug", required=True, help="英文文件名，小写连字符，如 lactate-threshold")
    p.add_argument("--title", default="", help="笔记主题（中文），回填到模板")
    p.add_argument("--module", default="", help="docs 下的模块目录名，如 06-ace-cpt")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])

    slug = args.slug.strip().lower()
    if not SLUG_RE.match(slug):
        print("ERROR: slug 需为小写字母/数字+连字符，如 lactate-threshold，收到: %s" % args.slug,
              file=sys.stderr)
        return 1

    if not os.path.isfile(TEMPLATE):
        print("ERROR: 找不到模板: %s" % TEMPLATE, file=sys.stderr)
        return 1

    module = args.module.strip()
    if module and os.path.isdir(os.path.join(DOCS, module)):
        out_dir = os.path.join(DOCS, module)
        module_label = MODULE_NAMES.get(module, module)
    else:
        if module:
            print("提示: 未找到 docs/%s，改存到 feynman-notes/" % module)
        out_dir = os.path.join(ROOT, "feynman-notes")
        module_label = MODULE_NAMES.get(module, module)

    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "%s.md" % slug)
    if os.path.exists(target):
        print("已存在，未覆盖: %s" % os.path.relpath(target, ROOT).replace("\\", "/"))
        return 0

    with open(TEMPLATE, encoding="utf-8") as f:
        content = f.read()

    today = datetime.date.today().strftime("%Y-%m-%d")
    if args.title:
        content = content.replace("# 费曼学习笔记模板", "# %s" % args.title, 1)
        content = content.replace("- 主题：", "- 主题：%s" % args.title, 1)
    if module_label:
        content = content.replace("- 所属模块：", "- 所属模块：%s" % module_label, 1)
    content = content.replace("- 日期：", "- 日期：%s" % today, 1)

    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print("已创建费曼笔记: %s" % os.path.relpath(target, ROOT).replace("\\", "/"))
    if link_in_module_readme(out_dir, slug, args.title):
        print("已在模块 README 追加链接: %s" % os.path.relpath(os.path.join(out_dir, "README.md"), ROOT).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
