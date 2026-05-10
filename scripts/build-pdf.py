#!/usr/bin/env python3
"""
Build PDF：从markdown目录生成PDF

前提：
- 安装 pandoc：brew install pandoc / apt install pandoc
- 安装 pypdf：pip install pypdf
- （可选）安装 texlive-full 支持完整LaTeX（用于中文）

输出：
- 00-目录.pdf
- 01-章节1.pdf
- ...
- {session}-完整.pdf
"""

from __future__ import annotations

import os
import sys
import argparse
import subprocess
from pathlib import Path
from pypdf import PdfWriter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")


def check_pandoc():
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        print("⚠️ 未安装 pandoc，将跳过PDF生成")
        print("   安装命令：")
        print("   - macOS: brew install pandoc")
        print("   - Ubuntu: apt install pandoc")
        return False


def markdown_to_pdf(md_path: str, pdf_path: str):
    """单份Markdown转PDF"""
    cmd = [
        "pandoc",
        "-s", md_path,
        "-o", pdf_path,
        "--toc", "--toc-depth=2",
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=2cm",
        "-V", "mainfont=Noto Sans CJK SC",
        "-V", "monofont=Noto Sans Mono CJK SC",
        "-V", "CJKmainfont=Noto Sans CJK SC",
        "-V", "CJKmonofont=Noto Sans Mono CJK SC",
    ]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ pandoc失败：{e}")
        print(f"   stdout: {e.stdout.decode('utf-8', errors='ignore')}")
        print(f"   stderr: {e.stderr.decode('utf-8', errors='ignore')}")
        return False


def merge_pdfs(pdf_list: list[str], output_path: str):
    """合并多个PDF"""
    merger = PdfWriter()
    for pdf in pdf_list:
        if os.path.exists(pdf):
            merger.append(pdf)
    merger.write(output_path)
    merger.close()
    print(f"✅ 合并完成：{output_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build PDF")
    parser.add_argument("--session", required=True, help="会话目录名")
    args = parser.parse_args(argv)

    session_dir = os.path.join(EXPORTS_DIR, args.session)
    markdown_dir = os.path.join(session_dir, "markdown")
    pdf_dir = os.path.join(session_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)

    if not os.path.exists(markdown_dir):
        print(f"⚠️ markdown目录不存在：{markdown_dir}")
        return 1

    if not check_pandoc():
        print("\nℹ️ 跳过PDF生成，但已完成Markdown包")
        return 0

    # 生成单页PDF
    pdf_list = []
    md_files = sorted(os.listdir(markdown_dir))
    for md_file in md_files:
        if not md_file.endswith(".md"):
            continue
        md_path = os.path.join(markdown_dir, md_file)
        pdf_file = md_file.replace(".md", ".pdf")
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"🔄 生成PDF：{md_file} → {pdf_file}")
        if markdown_to_pdf(md_path, pdf_path):
            pdf_list.append(pdf_path)

    # 合并完整PDF
    if pdf_list:
        full_pdf = os.path.join(pdf_dir, f"{args.session}-完整.pdf")
        merge_pdfs(pdf_list, full_pdf)
    else:
        print("⚠️ 未生成任何PDF")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
