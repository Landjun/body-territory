#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_quote_cards.py — 根据金句列表批量生成安全跑者金句卡片（SVG）。

用法：
    python scripts/gen_quote_cards.py

说明：
- 输出到 docs/08-safe-runner-brand/cards/card-01.svg ... ；
- SVG 是纯文本，零依赖，GitHub 直接渲染，改文字即改图；
- 想增减金句，直接改下面的 QUOTES 列表再运行即可。

仅依赖 Python 标准库。
"""

import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "08-safe-runner-brand", "cards")

# (金句正文, 署名)。正文会按中文字宽自动折行。
QUOTES = [
    ("网络安全是我要成为谁，跑步是我用什么身体去成为那个人。", "—— 安全跑者"),
    ("一个用身体的纪律映照安全的纪律的人。", "—— 安全跑者"),
    ("降级不是失败，是纪律。", "—— 安全跑者"),
    ("力量重建不是跑步的附属品，而是安全跑步的地基。", "—— 安全跑者"),
    ("不受伤地持续，才是真正长期主义。", "—— 安全跑者"),
    ("没有记录，训练就很难变成系统。", "—— 安全跑者"),
]

WIDTH = 1200
HEIGHT = 630
MARGIN = 90
MAX_CHARS_PER_LINE = 16  # 主句每行最多中文字符数
FONT = '"PingFang SC","Microsoft YaHei","Noto Sans SC","Hiragino Sans GB",sans-serif'


def wrap(text, max_chars):
    """按字符数折行，尽量在标点后断开。"""
    lines = []
    cur = ""
    for ch in text:
        cur += ch
        if len(cur) >= max_chars and ch in "，。；！？、":
            lines.append(cur)
            cur = ""
        elif len(cur) >= max_chars + 3:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines


def xml_escape(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render(quote, attribution):
    lines = wrap(quote, MAX_CHARS_PER_LINE)
    # 主句整体垂直居中
    line_h = 86
    block_h = len(lines) * line_h
    start_y = (HEIGHT - block_h) // 2 + 60
    parts = []
    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" role="img" aria-label="安全跑者金句卡片">'
        % (WIDTH, HEIGHT, WIDTH, HEIGHT)
    )
    parts.append(
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0f172a"/>'
        '<stop offset="1" stop-color="#1e293b"/></linearGradient>'
        '<style>.zh{font-family:%s;}</style></defs>' % FONT
    )
    parts.append('<rect width="%d" height="%d" fill="url(#bg)"/>' % (WIDTH, HEIGHT))
    parts.append('<rect x="0" y="0" width="14" height="%d" fill="#38bdf8"/>' % HEIGHT)
    parts.append(
        '<text x="%d" y="110" class="zh" fill="#38bdf8" font-size="26" '
        'font-weight="700" letter-spacing="6">BODY TERRITORY · 安全跑者</text>'
        % MARGIN
    )
    for i, line in enumerate(lines):
        y = start_y + i * line_h
        parts.append(
            '<text x="%d" y="%d" class="zh" fill="#f8fafc" font-size="54" '
            'font-weight="800">%s</text>' % (MARGIN, y, xml_escape(line))
        )
    parts.append(
        '<text x="%d" y="%d" class="zh" fill="#cbd5e1" font-size="30" '
        'font-weight="600">%s</text>'
        % (MARGIN, start_y + block_h + 24, xml_escape(attribution))
    )
    parts.append(
        '<text x="%d" y="566" class="zh" fill="#64748b" font-size="22">'
        'github.com/Landjun/body-territory</text>' % MARGIN
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    written = []
    for i, (quote, attribution) in enumerate(QUOTES, start=1):
        svg = render(quote, attribution)
        path = os.path.join(OUT_DIR, "card-%02d.svg" % i)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        written.append(os.path.relpath(path, ROOT).replace("\\", "/"))
    print("已生成 %d 张金句卡片：" % len(written))
    for w in written:
        print("  " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
