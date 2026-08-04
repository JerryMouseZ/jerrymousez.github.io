#!/usr/bin/env python3
"""Render the latest Horizon Chinese Markdown report as static HTML."""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt


STYLE = """
:root{color-scheme:light dark}*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.72;background:#f5f7fb;color:#172033}main{max-width:920px;margin:32px auto;padding:38px 48px;background:#fff;border-radius:16px;box-shadow:0 8px 30px #1f29371a}a{color:#2563eb;text-decoration:none}a:hover{text-decoration:underline}h1,h2,h3{line-height:1.35;color:#0f172a}h1{border-bottom:1px solid #e5e7eb;padding-bottom:18px}h2{margin-top:42px}h3{margin-top:30px}blockquote{margin:20px 0;padding:12px 18px;border-left:4px solid #3b82f6;background:#eff6ff;color:#334155}code{padding:2px 6px;border-radius:5px;background:#eef2f7}hr{border:0;border-top:1px solid #e5e7eb;margin:36px 0}details{margin:14px 0;padding:10px 14px;border:1px solid #e5e7eb;border-radius:8px}nav{max-width:920px;margin:24px auto 0;padding:0 8px}nav a{font-weight:600}@media(max-width:720px){main{margin:12px;padding:24px 18px;border-radius:0}}@media(prefers-color-scheme:dark){body{background:#0b1120;color:#dbe4f0}main{background:#111827}h1,h2,h3{color:#f8fafc}blockquote{background:#172554;color:#dbeafe}code{background:#263244}details,h1,hr{border-color:#334155}}
""".strip()


def main() -> None:
    summaries_dir = Path(sys.argv[1])
    reports = sorted(summaries_dir.glob("horizon-*-zh.md"))
    if not reports:
        raise SystemExit(f"No Chinese report found in {summaries_dir}")

    report = reports[-1]
    date = report.stem.removeprefix("horizon-").removesuffix("-zh")
    title = f"Horizon 每日速递 - {date}"
    body = MarkdownIt("commonmark", {"html": True, "linkify": True}).render(
        report.read_text(encoding="utf-8")
    )
    page = (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(title)}</title><style>{STYLE}</style></head><body>"
        '<nav><a href="/">← 返回 JerryMouseZ 首页</a></nav>'
        f"<main>{body}</main></body></html>"
    )

    output_dir = Path("horizon")
    output_dir.mkdir(exist_ok=True)
    (output_dir / f"{date}.html").write_text(page, encoding="utf-8")
    (output_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"Rendered {report} to {output_dir}/{date}.html")


if __name__ == "__main__":
    main()
