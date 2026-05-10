#!/usr/bin/env python3
"""
Validate Handbook：生成PDF前必须通过的校验

用法：python3 scripts/validate_handbook.py --session <session_name>

校验规则：
1. session目录必须存在
2. 必须有raw_jd.md
3. 必须有context_pack.yaml
4. 必须有topic_backlog.yaml
5. P0 topic必须有interview-card.md和quiz-card.md
6. 禁止出现无证据的项目故事
7. 必须有source_trace.md
8. Markdown中不能有孤立bullet/编号
"""

from __future__ import annotations

import os
import sys
import re
import json
import argparse
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")
CONTRACT_PATH = os.path.join(ROOT_DIR, "contracts", "handbook_artifact_contract.yaml")


def load_contract() -> dict:
    """加载产物契约"""
    if os.path.exists(CONTRACT_PATH):
        with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def check_file(path: str, errors: list, required: bool = True):
    """检查文件是否存在"""
    if not os.path.exists(path):
        level = "❌ FAIL" if required else "⚠️  WARN"
        errors.append(f"{level}: 文件不存在 {path}")
        return False
    return True


def check_no_fake_project_stories(dir_path: str, errors: list):
    """检查是否有无证据的项目故事"""
    forbidden_patterns = [
        r"我之前做过",
        r"我之前负责",
        r"我主导了",
        r"优化到\d+[%.]",
        r"提升了\d+[%.]",
    ]
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            for pattern in forbidden_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    # 检查是否有project_evidence.md
                    evidence_path = os.path.join(os.path.dirname(filepath), "project_evidence.md")
                    if not os.path.exists(evidence_path):
                        errors.append(
                            f"❌ FAIL: {filepath} 包含无证据的项目故事: {matches}。"
                            f"请添加project_evidence.md或改用'理论推演'表达。"
                        )


def check_orphan_bullets(dir_path: str, errors: list):
    """检查Markdown中是否有孤立bullet"""
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
            for i, line in enumerate(lines):
                # 连续3行以上只有bullet符号没有内容
                if re.match(r"^\s*[-*]\s*$", line):
                    count = 0
                    for j in range(i, min(i + 3, len(lines))):
                        if re.match(r"^\s*[-*]\s*$", lines[j]):
                            count += 1
                    if count >= 3:
                        errors.append(f"⚠️  WARN: {filepath}:{i+1} 有孤立bullet（连续空列表项）")


def validate_session(session: str) -> list[str]:
    """校验session产物"""
    errors = []
    session_dir = os.path.join(EXPORTS_DIR, session)

    if not os.path.exists(session_dir):
        errors.append(f"❌ FAIL: session目录不存在 {session_dir}")
        return errors

    contract = load_contract()
    session_required = contract.get("session_required_files", [
        "raw_jd.md", "jd_analysis.md", "context_pack.yaml",
        "topic_backlog.yaml", "state.yaml", "source_trace.md"
    ])

    # 1. 检查session级必需文件
    for f in session_required:
        check_file(os.path.join(session_dir, f), errors, required=True)

    # 2. 检查topic级必需文件
    cards_dir = os.path.join(session_dir, "cards")
    if os.path.exists(cards_dir):
        # 从topic_backlog.yaml读取优先级
        backlog_path = os.path.join(session_dir, "topic_backlog.yaml")
        if os.path.exists(backlog_path):
            with open(backlog_path, "r", encoding="utf-8") as f:
                backlog = yaml.safe_load(f) or {}
            topics = backlog.get("topics", [])
            for topic in topics:
                topic_id = topic.get("id", "")
                priority = topic.get("priority", "P2")
                topic_dir = os.path.join(cards_dir, topic_id)

                if priority in ("P0", "P1"):
                    topic_required = contract.get("topic_required_files", {}).get(priority, [])
                    for f in topic_required:
                        check_file(os.path.join(topic_dir, f), errors, required=True)

    # 3. 检查无证据项目故事
    check_no_fake_project_stories(session_dir, errors)

    # 4. 检查孤立bullet
    check_orphan_bullets(session_dir, errors)

    # 5. 检查source_trace.md
    trace_path = os.path.join(session_dir, "source_trace.md")
    if os.path.exists(trace_path):
        with open(trace_path, "r", encoding="utf-8") as f:
            trace = f.read()
        if not trace.strip():
            errors.append(f"⚠️  WARN: source_trace.md 是空的")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Handbook Session")
    parser.add_argument("--session", required=True, help="会话目录名")
    args = parser.parse_args(argv)

    print(f"🔍 校验 session: {args.session}")
    print("-" * 40)

    errors = validate_session(args.session)

    fails = [e for e in errors if e.startswith("❌")]
    warns = [e for e in errors if e.startswith("⚠️")]

    for e in errors:
        print(e)

    print("-" * 40)
    if fails:
        print(f"❌ 校验失败：{len(fails)} 个错误，{len(warns)} 个警告")
        print("   请修复所有错误后再生成PDF。")
        return 1
    else:
        print(f"✅ 校验通过！{len(warns)} 个警告")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
