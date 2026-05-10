#!/usr/bin/env python3
"""
Build Markdown packs from generated cards.

Reads all card files from exports/{session}/cards/ and assembles them into:
- memorization_pack_full.md
- memorization_pack_cram.md
- quiz_pack.md

Usage:
    python3 scripts/build_markdown_pack.py --session <session_id>
"""

from __future__ import annotations

import argparse
import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")


def read_card(cards_dir: str, topic_id: str, card_type: str) -> str | None:
    """Read a card file if it exists."""

    path = os.path.join(cards_dir, topic_id, f"{card_type}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def collect_cards(session_dir: str) -> list[dict]:
    """Collect all generated cards for a session."""

    cards_dir = os.path.join(session_dir, "cards")
    if not os.path.isdir(cards_dir):
        return []

    topics = []
    for topic_id in sorted(os.listdir(cards_dir)):
        topic_dir = os.path.join(cards_dir, topic_id)
        if not os.path.isdir(topic_dir):
            continue

        cards: dict = {"id": topic_id}
        for card_type in ("knowledge-card", "interview-card", "pressure-q"):
            content = read_card(cards_dir, topic_id, card_type)
            if content:
                cards[card_type] = content

        if len(cards) > 1:  # More than just 'id'
            topics.append(cards)

    return topics


def build_full_pack(topics: list[dict], position: str) -> str:
    """Build memorization_pack_full.md."""

    lines = [f"# 面试背诵手册：{position}\n"]
    lines.append(f"共 {len(topics)} 个知识点\n")

    # Table of contents
    lines.append("## 目录\n")
    for i, topic in enumerate(topics, 1):
        lines.append(f"{i}. {topic['id']}")
    lines.append("")

    for topic in topics:
        lines.append("---\n")
        if "knowledge-card" in topic:
            lines.append(topic["knowledge-card"])
            lines.append("")
        if "interview-card" in topic:
            lines.append(topic["interview-card"])
            lines.append("")
        if "pressure-q" in topic:
            lines.append(topic["pressure-q"])
            lines.append("")

    return "\n".join(lines)


def build_cram_pack(topics: list[dict], position: str) -> str:
    """Build memorization_pack_cram.md (P0 only, compressed)."""

    lines = [f"# 考前速记：{position}\n"]

    for topic in topics:
        if "interview-card" not in topic:
            continue

        lines.append(f"## {topic['id']}\n")
        card = topic["interview-card"]

        # Extract 30s version and trade-off
        in_30s = False
        in_tradeoff = False
        for line in card.split("\n"):
            if "30 秒版" in line or "30秒版" in line:
                in_30s = True
                in_tradeoff = False
                continue
            if "Trade-off" in line:
                in_tradeoff = True
                in_30s = False
                continue
            if line.startswith("## "):
                in_30s = False
                in_tradeoff = False
                continue
            if in_30s or in_tradeoff:
                lines.append(line)

        lines.append("")

    return "\n".join(lines)


def build_quiz_pack(topics: list[dict], position: str) -> str:
    """Build quiz_pack.md."""

    lines = [f"# 自测题：{position}\n"]

    q_num = 1
    for topic in topics:
        if "pressure-q" not in topic:
            continue

        card = topic["pressure-q"]
        lines.append(f"## {topic['id']}\n")

        # Extract questions
        for line in card.split("\n"):
            stripped = line.strip()
            if stripped and stripped[0].isdigit() and "." in stripped[:4]:
                lines.append(f"**Q{q_num}:** {stripped}")
                q_num += 1
            elif "回答方向" in stripped:
                lines.append(f"   {stripped}")
            elif "风险点" in stripped:
                lines.append(f"   {stripped}")

        lines.append("")
        lines.append("--- 闭卷回答后对照原卡 ---\n")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Markdown packs")
    parser.add_argument("--session", required=True, help="Session ID")
    args = parser.parse_args(argv)

    session_dir = os.path.join(EXPORTS_DIR, args.session)
    if not os.path.isdir(session_dir):
        print(f"❌ 会话不存在: {args.session}")
        return 1

    # Read position from state.yaml
    import yaml
    state_path = os.path.join(session_dir, "state.yaml")
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f)

    position = state.get("position", args.session)

    topics = collect_cards(session_dir)
    if not topics:
        print("❌ 没有找到已生成的卡片")
        return 1

    md_dir = os.path.join(session_dir, "markdown")
    os.makedirs(md_dir, exist_ok=True)

    # Full pack
    full = build_full_pack(topics, position)
    full_path = os.path.join(md_dir, "memorization_pack_full.md")
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(full)
    print(f"✅ 完整版: {full_path}")

    # Cram pack
    cram = build_cram_pack(topics, position)
    cram_path = os.path.join(md_dir, "memorization_pack_cram.md")
    with open(cram_path, "w", encoding="utf-8") as f:
        f.write(cram)
    print(f"✅ 速记版: {cram_path}")

    # Quiz pack
    quiz = build_quiz_pack(topics, position)
    quiz_path = os.path.join(md_dir, "quiz_pack.md")
    with open(quiz_path, "w", encoding="utf-8") as f:
        f.write(quiz)
    print(f"✅ 自测版: {quiz_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
