#!/usr/bin/env python3
"""
Validate Repo：检查项目治理文件是否完整

用法：python3 scripts/validate_repo.py

校验规则：
1. PROJECT_CONSTITUTION.md 必须存在
2. DECISION_RIGHTS.md 必须存在
3. README.md 必须引用 PROJECT_CONSTITUTION.md
4. SKILL.md 必须引用 PROJECT_CONSTITUTION.md
5. evals/blocker-cases.yaml 必须存在
6. ROADMAP.md 必须存在且引用宪法
"""

from __future__ import annotations

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)


def check_file(path: str, errors: list, required: bool = True):
    if not os.path.exists(path):
        level = "❌ FAIL" if required else "⚠️  WARN"
        errors.append(f"{level}: 文件不存在 {path}")
        return False
    return True


def check_file_contains(filepath: str, keyword: str, errors: list, label: str = ""):
    if not os.path.exists(filepath):
        errors.append(f"❌ FAIL: 文件不存在 {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if keyword not in content:
        name = label or os.path.basename(filepath)
        errors.append(f"❌ FAIL: {name} 未引用 {keyword}")


def main() -> int:
    errors = []

    print("🔍 校验 Interview Bible 项目治理文件")
    print("-" * 40)

    # 1. 治理文件存在性
    gov_files = [
        "PROJECT_CONSTITUTION.md",
        "DECISION_RIGHTS.md",
        "ROADMAP.md",
        os.path.join("evals", "blocker-cases.yaml"),
    ]
    for f in gov_files:
        check_file(os.path.join(ROOT_DIR, f), errors)

    # 2. README.md 引用宪法
    check_file_contains(
        os.path.join(ROOT_DIR, "README.md"),
        "PROJECT_CONSTITUTION.md",
        errors,
        "README.md"
    )

    # 3. SKILL.md 引用宪法
    check_file_contains(
        os.path.join(ROOT_DIR, "SKILL.md"),
        "PROJECT_CONSTITUTION.md",
        errors,
        "SKILL.md"
    )

    # 4. ROADMAP.md 引用宪法
    check_file_contains(
        os.path.join(ROOT_DIR, "ROADMAP.md"),
        "PROJECT_CONSTITUTION.md",
        errors,
        "ROADMAP.md"
    )

    fails = [e for e in errors if e.startswith("❌")]
    warns = [e for e in errors if e.startswith("⚠️")]

    for e in errors:
        print(e)

    print("-" * 40)
    if fails:
        print(f"❌ 校验失败：{len(fails)} 个错误")
        return 1
    else:
        print(f"✅ 项目治理文件校验通过！{len(warns)} 个警告")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
