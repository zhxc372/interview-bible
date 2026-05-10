#!/usr/bin/env python3
"""
Build PDF v2：Markdown → HTML（带CSS美化）→ PDF

排版规则（设计层面固定，不靠LLM随机）：
- 标题：思源黑体（Noto Sans CJK SC）
- 正文：霞鹜文楷（LXGW WenKai）
- 行内代码：红底色块，等宽字体
- 代码块：灰底+pygments语法高亮
- 公式：预留KaTeX支持（weasyprint暂不支持JS，公式用code格式展示）
- blockquote分级：> ⚠️ 警告 / > 💡 提示 / > 📌 注意
- 列表：保持列表格式，不转成散文
- 表格：斑马纹+圆角
"""

from __future__ import annotations

import os
import sys
import argparse
import markdown
from weasyprint import HTML, CSS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")

# ===== 排版规则：CSS =====
BOOK_CSS = CSS(string="""
/* === 页面 === */
@page {
    size: A4;
    margin: 2.5cm 2cm 2.5cm 2cm;
    @bottom-center {
        content: counter(page);
        font-family: "Noto Sans CJK SC", sans-serif;
        font-size: 9pt;
        color: #999;
    }
}
@page :first { @bottom-center { content: none; } }

/* === 正文 === */
body {
    font-family: "LXGW WenKai", "霞鹜文楷", "Noto Serif CJK SC", serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #333;
    text-align: justify;
}

/* === 标题 === */
h1 {
    font-family: "Noto Sans CJK SC", "思源黑体", sans-serif;
    font-size: 22pt;
    font-weight: bold;
    color: #1a1a1a;
    margin-top: 0.3em;
    margin-bottom: 0.3em;
    page-break-before: auto;
    border-bottom: 2px solid #333;
    padding-bottom: 0.2em;
}
h1:first-of-type { page-break-before: auto; }

h2 {
    font-family: "Noto Sans CJK SC", "思源黑体", sans-serif;
    font-size: 15pt;
    font-weight: bold;
    color: #2c2c2c;
    margin-top: 0.8em;
    margin-bottom: 0.3em;
    border-left: 4px solid #555;
    padding-left: 0.5em;
}

h3 {
    font-family: "Noto Sans CJK SC", "思源黑体", sans-serif;
    font-size: 13pt;
    font-weight: bold;
    color: #444;
    margin-top: 0.6em;
    margin-bottom: 0.2em;
}

h4 {
    font-family: "Noto Sans CJK SC", "思源黑体", sans-serif;
    font-size: 12pt;
    font-weight: bold;
    color: #555;
    margin-top: 0.5em;
    margin-bottom: 0.2em;
}

/* 标题后不分页 */
h2, h3, h4, h5, h6 { page-break-after: avoid; }

/* === 段落 === */
p {
    margin: 0.5em 0;
    orphans: 3;
    widows: 3;
}

/* === 列表（保持列表格式！） === */
ul, ol {
    padding-left: 1.5em;
    margin: 0.5em 0;
}
li {
    margin: 0.3em 0;
    line-height: 1.7;
}
li > ul, li > ol {
    margin: 0.2em 0;
}

/* === 行内代码 === */
code {
    font-family: "Noto Sans Mono CJK SC", "Source Code Pro", "Courier New", monospace;
    font-size: 10pt;
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 3px;
    color: #c7254e;
    border: 1px solid #e0e0e0;
}

/* === 代码块 === */
pre {
    background: #282c34;
    border: 1px solid #3a3f47;
    border-radius: 6px;
    padding: 1em;
    overflow-x: auto;
    font-size: 9.5pt;
    line-height: 1.6;
    margin: 0.8em 0;
    page-break-inside: avoid;
}
pre code {
    background: none;
    padding: 0;
    border: none;
    color: #abb2bf;
}

/* === Pygments 语法高亮配色（One Dark风格） === */
.codehilite .hll { background-color: #3a3f47; }
.codehilite .c { color: #5c6370; font-style: italic; } /* Comment */
.codehilite .k { color: #c678dd; } /* Keyword */
.codehilite .n { color: #e06c75; } /* Name */
.codehilite .o { color: #56b6c2; } /* Operator */
.codehilite .p { color: #abb2bf; } /* Punctuation */
.codehilite .s { color: #98c379; } /* String */
.codehilite .s1 { color: #98c379; } /* String.Single */
.codehilite .s2 { color: #98c379; } /* String.Double */
.codehilite .nf { color: #61afef; } /* Name.Function */
.codehilite .nc { color: #e5c07b; } /* Name.Class */
.codehilite .nb { color: #e5c07b; } /* Name.Builtin */
.codehilite .nn { color: #e5c07b; } /* Name.Namespace */
.codehilite .kt { color: #e5c07b; } /* Keyword.Type */
.codehilite .mi { color: #d19a66; } /* Number.Integer */
.codehilite .mf { color: #d19a66; } /* Number.Float */
.codehilite .nd { color: #61afef; } /* Name.Decorator */
.codehilite .ne { color: #e06c75; } /* Name.Exception */
.codehilite .nt { color: #e06c75; } /* Name.Tag */
.codehilite .nv { color: #e06c75; } /* Name.Variable */
.codehilite .vc { color: #e06c75; } /* Name.Variable.Class */
.codehilite .vg { color: #e06c75; } /* Name.Variable.Global */
.codehilite .vi { color: #e06c75; } /* Name.Variable.Instance */

/* === Blockquote分级 === */
blockquote {
    margin: 0.8em 0;
    padding: 0.6em 1em;
    border-left: 4px solid #ddd;
    border-radius: 0 4px 4px 0;
    background: #fafafa;
    font-style: normal;
}
/* 提示 💡 */
blockquote {
    border-left-color: #4CAF50;
    background: #f1f8f1;
}
/* 注意 📌 或 ⚠️ 通过内容里的emoji区分，CSS统一绿色提示框 */

/* === 表格 === */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.8em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}
th {
    background: #f0f0f0;
    font-weight: bold;
    font-family: "Noto Sans CJK SC", "思源黑体", sans-serif;
}
tr:nth-child(even) { background: #fafafa; }

/* === 分隔线 === */
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 1em 0;
}
hr + * { page-break-before: avoid; }

/* === 加粗 === */
strong { color: #1a1a1a; }
""")


def md_to_pdf(md_path: str, pdf_path: str):
    """Markdown转PDF"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Markdown → HTML（带代码高亮）
    html_body = markdown.markdown(
        md_content,
        extensions=[
            "tables",
            "fenced_code",
            "toc",
            "codehilite",  # 代码高亮
        ],
        extension_configs={
            "codehilite": {
                "css_class": "codehilite",
                "guess_lang": True,
                "noclasses": False,
            },
        },
    )

    # 包裹成完整HTML
    html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
</head>
<body>
{html_body}
</body>
</html>"""

    # 生成PDF
    HTML(string=html_full).write_pdf(pdf_path, stylesheets=[BOOK_CSS])
    print(f"✅ PDF已生成：{pdf_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build PDF v2（weasyprint + 代码高亮）")
    parser.add_argument("--session", required=True, help="会话目录名")
    parser.add_argument("--input", help="指定输入md文件名")
    args = parser.parse_args(argv)

    session_dir = os.path.join(EXPORTS_DIR, args.session)
    markdown_dir = os.path.join(session_dir, "markdown")
    pdf_dir = os.path.join(session_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)

    # 找输入文件
    if args.input:
        md_path = os.path.join(markdown_dir, args.input)
    else:
        candidates = [f for f in os.listdir(markdown_dir) if f.endswith("面试手册.md")]
        if not candidates:
            candidates = [f for f in os.listdir(markdown_dir) if "完整" in f]
        if not candidates:
            print("❌ 找不到markdown文件")
            return 1
        md_path = os.path.join(markdown_dir, candidates[0])

    if not os.path.exists(md_path):
        print(f"❌ 文件不存在：{md_path}")
        return 1

    md_filename = os.path.basename(md_path)
    pdf_filename = md_filename.replace(".md", ".pdf")
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    md_to_pdf(md_path, pdf_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
