#!/usr/bin/env python3
"""
Build Print Pack：从cards目录生成完整Markdown包 + 目录

输入：
- session_id：会话目录名（如sample-go-backend）
- 或者手动指定主题列表

输出：
- exports/{session}/markdown/00-目录.md
- exports/{session}/markdown/01-编程语言.md
- ...
- exports/{session}/markdown/{session}-完整.md
"""

from __future__ import annotations

import os
import sys
import json
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
        return f"\n# {topic_id}（卡片待生成）\n\n请先生成知识点卡和面试卡。\n"


def build_toc(session: str, topic_list: list[tuple[str, str]]) -> str:
    """生成目录markdown"""
    lines = []
    lines.append(f"# {session} 面试备考手册\n")
    lines.append(f"> 生成时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
    lines.append("---\n\n## 目录\n")

    for idx, (topic_id, topic_name) in enumerate(topic_list, 1):
        lines.append(f"{idx}. {topic_name}")

    lines.append("\n---\n\n")
    return "\n".join(lines)


def build_full_markdown(session: str, topic_list: list[tuple[str, str]]) -> str:
    """生成完整markdown包（目录+所有章节）"""
    cards_dir = os.path.join(EXPORTS_DIR, session, "cards")
    if not os.path.exists(cards_dir):
        raise FileNotFoundError(f"会话目录不存在：{cards_dir}")

    lines = [build_toc(session, topic_list)]

    for topic_id, topic_name in topic_list:
        lines.append(f"\n---\n\n# {topic_name}\n\n")
        # 先加知识点卡
        knowledge_card = load_card(cards_dir, topic_id, "knowledge")
        if knowledge_card.strip():
            lines.append(f"## 1. 知识点卡（搞清楚）\n\n")
            lines.append(knowledge_card)
        # 再加面试卡
        interview_card = load_card(cards_dir, topic_id, "interview")
        if interview_card.strip():
            lines.append(f"## 2. 面试卡（讲清楚）\n\n")
            lines.append(interview_card)
        # 最后加自测题
        quiz_card = load_card(cards_dir, topic_id, "quiz")
        if quiz_card.strip():
            lines.append(f"## 3. 自测题（验证）\n\n")
            lines.append(quiz_card)

    return "\n".join(lines)


def build_chapter_markdown(topic_id: str, topic_name: str, cards_dir: str) -> str:
    """生成单个章节的markdown（用于单独PDF）"""
    lines = []
    lines.append(f"# {topic_name}\n")
    lines.append(f"> topic: {topic_id}\n")

    knowledge_card = load_card(cards_dir, topic_id, "knowledge")
    if knowledge_card.strip():
        lines.append(f"\n## 1. 知识点卡（搞清楚）\n\n")
        lines.append(knowledge_card)

    interview_card = load_card(cards_dir, topic_id, "interview")
    if interview_card.strip():
        lines.append(f"\n## 2. 面试卡（讲清楚）\n\n")
        lines.append(interview_card)

    quiz_card = load_card(cards_dir, topic_id, "quiz")
    if quiz_card.strip():
        lines.append(f"\n## 3. 自测题（验证）\n\n")
        lines.append(quiz_card)

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Print Pack")
    parser.add_argument("--session", required=True, help="会话目录名")
    args = parser.parse_args(argv)

    session_dir = os.path.join(EXPORTS_DIR, args.session)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)

    # 临时：默认Go后端主题列表
    default_topics = [
        ("go-concurrency", "Go并发（goroutine/channel）"),
        ("go-context", "Go context"),
        ("mysql-mvcc", "MVCC"),
        ("mysql-index", "MySQL索引"),
        ("redis-basics", "Redis基础"),
    ]

    markdown_dir = os.path.join(session_dir, "markdown")
    os.makedirs(markdown_dir, exist_ok=True)

    # 00-目录.md
    toc_path = os.path.join(markdown_dir, "00-目录.md")
    toc_content = build_toc(args.session, default_topics)
    with open(toc_path, "w", encoding="utf-8") as f:
        f.write(toc_content)
    print(f"✅ 目录已生成：{toc_path}")

    # 各章节
    cards_dir = os.path.join(session_dir, "cards")
    os.makedirs(cards_dir, exist_ok=True)

    for idx, (topic_id, topic_name) in enumerate(default_topics, 1):
        chapter_content = build_chapter_markdown(topic_id, topic_name, cards_dir)
        chapter_path = os.path.join(markdown_dir, f"{idx:02d}-{topic_id}.md")
        with open(chapter_path, "w", encoding="utf-8") as f:
            f.write(chapter_content)
        print(f"✅ 章节已生成：{chapter_path}")

    # 完整.md
    full_path = os.path.join(markdown_dir, f"{args.session}-完整.md")
    full_content = build_full_markdown(args.session, default_topics)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"✅ 完整包已生成：{full_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
