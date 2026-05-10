#!/usr/bin/env python3
"""
Check context budget compliance.

Verifies that generated content stays within budget and that
topic generation doesn't include the raw JD.

Usage:
    python3 scripts/check_context_budget.py [--session <session_id>]
"""

from __future__ import annotations

import argparse
import os
import sys
import yaml


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")
BUDGET_PATH = os.path.join(ROOT_DIR, "context", "context_budget.yaml")


def load_budget() -> dict:
    if os.path.exists(BUDGET_PATH):
        with open(BUDGET_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def check_card_length(cards_dir: str, budget: dict) -> list[str]:
    """Check all card files against budget."""

    errors = []
    max_chars = budget.get("budget", {}).get("topic_card_max_chars", 8000)

    if not os.path.isdir(cards_dir):
        return errors

    for topic_id in os.listdir(cards_dir):
        topic_dir = os.path.join(cards_dir, topic_id)
        if not os.path.isdir(topic_dir):
            continue
        for fname in os.listdir(topic_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(topic_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content) > max_chars:
                errors.append(
                    f"⚠️ {topic_id}/{fname}: {len(content)} chars > budget {max_chars}"
                )

    return errors


def check_no_raw_jd(session_dir: str, budget: dict) -> list[str]:
    """Verify that topic cards don't contain raw JD text."""

    errors = []
    rules = budget.get("rules", {})

    if not rules.get("forbid_raw_jd_in_topic_generation", True):
        return errors

    # Check if raw JD file exists in session
    jd_path = os.path.join(session_dir, "raw_jd.md")
    if not os.path.exists(jd_path):
        return errors  # No raw JD to check against

    with open(jd_path, "r", encoding="utf-8") as f:
        raw_jd = f.read()

    # Take first 200 chars of JD as fingerprint
    jd_fingerprint = raw_jd.strip()[:200]

    cards_dir = os.path.join(session_dir, "cards")
    if not os.path.isdir(cards_dir):
        return errors

    for topic_id in os.listdir(cards_dir):
        topic_dir = os.path.join(cards_dir, topic_id)
        if not os.path.isdir(topic_dir):
            continue
        for fname in os.listdir(topic_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(topic_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            if jd_fingerprint[:100] in content:
                errors.append(
                    f"⚠️ {topic_id}/{fname}: 包含原始JD内容（违反context_rules）"
                )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check context budget")
    parser.add_argument("--session", help="Session ID to check")
    args = parser.parse_args(argv)

    budget = load_budget()
    all_errors = []

    if args.session:
        session_dir = os.path.join(EXPORTS_DIR, args.session)
        if not os.path.isdir(session_dir):
            print(f"❌ 会话不存在: {args.session}")
            return 1
        sessions = [(args.session, session_dir)]
    else:
        # Check all sessions
        sessions = []
        if os.path.isdir(EXPORTS_DIR):
            for entry in os.listdir(EXPORTS_DIR):
                session_dir = os.path.join(EXPORTS_DIR, entry)
                if os.path.isdir(session_dir):
                    sessions.append((entry, session_dir))

    if not sessions:
        print("⚠️ 没有找到任何会话")
        return 0

    for session_id, session_dir in sessions:
        cards_dir = os.path.join(session_dir, "cards")
        errors = check_card_length(cards_dir, budget)
        errors += check_no_raw_jd(session_dir, budget)
        all_errors.extend(errors)

    if all_errors:
        print("❌ Budget 检查失败:\n")
        for e in all_errors:
            print(f"  {e}")
        return 1

    print("✅ Budget 检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
