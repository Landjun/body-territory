#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_links.py — 检查仓库内所有 Markdown 的内部相对链接是否有断链。

用法：
    python scripts/check_links.py

行为：
- 扫描仓库下所有 .md（忽略 .git）；
- 对每个 Markdown 链接 [..](target)：
    * 跳过外部链接(http/https/mailto)与纯锚点(#...)；
    * 其余按相对路径解析，检查目标文件/目录是否存在；
- 打印所有断链并以非零退出码结束（便于 CI 失败）；无断链则退出 0。

仅依赖 Python 标准库。与 GitHub Actions 的 lychee 检查互补:
本脚本聚焦"仓库内相对链接",可在本地秒级自查,提交前先跑它。
"""

import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def iter_markdown_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            if name.lower().endswith(".md"):
                yield os.path.join(root, name)


def check_file(path):
    """返回该文件中的断链列表 [(link, resolved_path), ...]。"""
    broken = []
    base = os.path.dirname(path)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print("WARN: 无法读取 %s: %s" % (path, e), file=sys.stderr)
        return broken
    for m in LINK_RE.finditer(text):
        link = m.group(1).strip()
        if not link or link.startswith(SKIP_PREFIXES):
            continue
        target = link.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(resolved):
            broken.append((link, os.path.relpath(resolved, ROOT)))
    return broken


def main():
    total_files = 0
    total_broken = 0
    for md in sorted(iter_markdown_files()):
        broken = check_file(md)
        total_files += 1
        if broken:
            rel = os.path.relpath(md, ROOT).replace("\\", "/")
            for link, resolved in broken:
                total_broken += 1
                print("BROKEN  %s  ->  %s  (%s)" % (rel, link, resolved.replace("\\", "/")))
    if total_broken:
        print("\n%d broken link(s) in %d files." % (total_broken, total_files))
        return 1
    print("All internal links OK (%d markdown files)." % total_files)
    return 0


if __name__ == "__main__":
    sys.exit(main())
