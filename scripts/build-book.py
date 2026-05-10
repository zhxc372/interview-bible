#!/usr/bin/env python3
"""
Build Print Pack（v2）：生成一本像书的Markdown手册

- 加前言、目录、学习顺序
- 按第一篇、第二篇分
- TOC带锚点链接
- 更像人写的，少点AI味
"""

from __future__ import annotations

import os
import sys
import argparse
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")


def load_card(cards_dir: str, topic_id: str, card_type: str = "knowledge") -> str:
    """加载指定类型的卡片内容"""
    card_path = os.path.join(cards_dir, topic_id, f"{card_type}-card.md")
    if os.path.exists(card_path):
        with open(card_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return None  # 缺卡返回None，由调用方决定是否报错


def build_toc(topic_list: list[tuple[str, str]]) -> str:
    """生成带锚点的目录"""
    lines = []
    lines.append("# 目录\n")

    # 第一篇：语言基础
    lines.append("## 第一篇：语言基础\n")
    for idx in range(2):  # 前两个
        topic_id, topic_name = topic_list[idx]
        lines.append(f"- [{topic_name}](#{topic_id})")

    # 第二篇：云原生
    lines.append("\n## 第二篇：云原生\n")
    for idx in range(2, len(topic_list)):
        topic_id, topic_name = topic_list[idx]
        lines.append(f"- [{topic_name}](#{topic_id})")

    return "\n".join(lines)


def build_full_book(session: str, topic_list: list[tuple[str, str]]) -> str:
    """生成完整的书"""
    cards_dir = os.path.join(EXPORTS_DIR, session, "cards")

    lines = []

    # 封面/前言
    lines.append(f"# {session} 面试备考手册（小白版）\n")
    lines.append(f"> 生成时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n")
    lines.append(">\n")
    lines.append("> 写给像我们一样的普通求职者：\n")
    lines.append("> 面试不用背答案，要的是理解和故事。\n")
    lines.append("> 这本手册不是给你背的，是帮你理明白的。\n")
    lines.append("---\n\n")

    # 目录
    lines.append(build_toc(topic_list))
    lines.append("\n---\n\n")

    # 正文——像连续的文章，不要每块都分页
    lines.append("## 第一篇：语言基础\n")
    for idx in range(2):
        topic_id, topic_name = topic_list[idx]
        lines.append(f"\n---\n\n")
        lines.append(f"### {topic_name}\n\n")
        knowledge_card = load_card(cards_dir, topic_id, "knowledge")
        lines.append(knowledge_card)
        interview_card = load_card(cards_dir, topic_id, "interview")
        lines.append(f"\n\n")
        lines.append(interview_card)

    lines.append(f"\n---\n\n## 第二篇：云原生\n")
    for idx in range(2, len(topic_list)):
        topic_id, topic_name = topic_list[idx]
        lines.append(f"\n---\n\n")
        lines.append(f"### {topic_name}\n\n")
        knowledge_card = load_card(cards_dir, topic_id, "knowledge")
        lines.append(knowledge_card)
        interview_card = load_card(cards_dir, topic_id, "interview")
        lines.append(f"\n\n")
        lines.append(interview_card)

    # 后记
    lines.append(f"\n---\n\n## 后记\n\n")
    lines.append("祝你面试顺利！别忘了带个真实的项目故事！\n\n")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Print Pack（v2 - 像书一样）")
    parser.add_argument("--session", required=True, help="会话目录名")
    args = parser.parse_args(argv)

    session_dir = os.path.join(EXPORTS_DIR, args.session)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)

    # 读取topic_backlog.yaml，不硬编码
    backlog_path = os.path.join(session_dir, "topic_backlog.yaml")
    if not os.path.exists(backlog_path):
        print(f"❌ topic_backlog.yaml 不存在：{backlog_path}")
        print("   请先运行 JD Intake 生成 topic_backlog.yaml")
        return 1

    import yaml
    with open(backlog_path, "r", encoding="utf-8") as f:
        backlog = yaml.safe_load(f) or {}

    topics_raw = backlog.get("topics", [])
    if not topics_raw:
        print("❌ topic_backlog.yaml 中 topics 为空")
        print("   请先运行 JD Intake 填充 topic 列表")
        return 1

    topics = [(t["id"], t["name"]) for t in topics_raw]

    markdown_dir = os.path.join(session_dir, "markdown")
    os.makedirs(markdown_dir, exist_ok=True)

    # 输出contract标准命名
    full_path = os.path.join(markdown_dir, "interview_handbook.md")
    full_content = build_full_book(args.session, topics)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"✅ 书已生成：{full_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
