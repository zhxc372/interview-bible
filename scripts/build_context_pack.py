#!/usr/bin/env python3
"""
Build context_pack.yaml from JD analysis.

This script creates a context pack (compressed JD digest + subject map + backlog)
that subsequent topic card generation can use instead of the raw JD.

Usage:
    python3 scripts/build_context_pack.py --session <session_id> [--jd-file <path>]

If --jd-file is omitted, reads from stdin.
"""

from __future__ import annotations

import argparse
import os
import sys
import yaml
from datetime import datetime, timezone


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")


def build_context_pack(
    position: str,
    jd_digest: dict,
    subject_map: list,
    project_evidence_index: list | None = None,
    generation_policy: dict | None = None,
) -> dict:
    """Build a context_pack.yaml structure."""

    pack: dict = {
        "version": "v0.4",
        "position": position,
        "jd_digest": jd_digest,
        "subject_map": subject_map,
        "project_evidence_index": project_evidence_index or [],
        "generation_policy": generation_policy or {
            "max_topics_per_batch": 1,
            "include_raw_jd": False,
            "default_output_level": {
                "P0": "full",
                "P1": "standard",
                "P2": "brief",
            },
        },
    }
    return pack


def build_state(
    session_id: str,
    position: str,
    backlog: list,
) -> dict:
    """Build a state.yaml structure."""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Find first pending item
    current_focus = None
    next_action = "全部完成"
    for item in backlog:
        if item.get("knowledge_card") == "pending":
            current_focus = item["id"]
            next_action = f"生成知识点卡: {item['name']}"
            break

    state: dict = {
        "session_id": session_id,
        "position": position,
        "created": now,
        "updated": now,
        "status": "in_progress",
        "backlog": backlog,
        "current_focus": current_focus,
        "next_action": next_action,
        "project_evidence_mapped": False,
    }
    return state


def save_yaml(data: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def update_state_after_card(
    session_dir: str,
    topic_id: str,
    card_type: str,
) -> dict:
    """Update state.yaml after generating a card."""

    state_path = os.path.join(session_dir, "state.yaml")
    state = load_yaml(state_path)

    for item in state["backlog"]:
        if item["id"] == topic_id:
            item[card_type] = "done"
            break

    # Determine next action
    state["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    current_focus = None
    next_action = "全部完成"
    for item in state["backlog"]:
        if item.get("knowledge_card") == "pending":
            current_focus = item["id"]
            next_action = f"生成知识点卡: {item['name']}"
            break
        if item.get("knowledge_card") == "done" and item.get("interview_card") == "pending":
            current_focus = item["id"]
            next_action = f"生成面试卡: {item['name']}"
            break
        if item.get("interview_card") == "done" and item.get("pressure_q") == "pending":
            current_focus = item["id"]
            next_action = f"生成压力追问: {item['name']}"
            break

    state["current_focus"] = current_focus
    state["next_action"] = next_action

    if next_action == "全部完成":
        state["status"] = "completed"
    else:
        state["status"] = "in_progress"

    save_yaml(state, state_path)
    return state


def get_latest_session(exports_dir: str) -> str | None:
    """Find the latest session directory."""

    if not os.path.isdir(exports_dir):
        return None

    sessions = []
    for entry in os.listdir(exports_dir):
        session_path = os.path.join(exports_dir, entry)
        state_path = os.path.join(session_path, "state.yaml")
        if os.path.isdir(session_path) and os.path.exists(state_path):
            sessions.append((entry, os.path.getmtime(state_path)))

    if not sessions:
        return None

    sessions.sort(key=lambda x: x[1], reverse=True)
    return sessions[0][0]


def resume_state(exports_dir: str) -> dict | None:
    """Load state from latest session for resume."""

    session_id = get_latest_session(exports_dir)
    if not session_id:
        return None

    state_path = os.path.join(exports_dir, session_id, "state.yaml")
    if not os.path.exists(state_path):
        return None

    return load_yaml(state_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build context pack and state")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--position", default="", help="Position title")
    parser.add_argument("--resume", action="store_true", help="Resume latest session")
    args = parser.parse_args(argv)

    session_dir = os.path.join(EXPORTS_DIR, args.session)

    if args.resume:
        state = resume_state(EXPORTS_DIR)
        if state:
            print(f"📋 恢复会话: {state['session_id']}")
            print(f"   岗位: {state['position']}")
            print(f"   状态: {state['status']}")
            print(f"   当前进度: {state['current_focus']}")
            print(f"   下一步: {state['next_action']}")
            return 0
        else:
            print("❌ 没有找到可恢复的会话")
            return 1

    # Demo: create a sample context pack
    print(f"✅ 会话目录: {session_dir}")
    print(f"   使用 build_context_pack() 和 build_state() 生成文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
