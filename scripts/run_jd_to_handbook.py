#!/usr/bin/env python3
"""
Run JD to Handbook：总控脚本

JD → 标准session目录 → 校验 → Markdown Pack → PDF
Agent不能绕过这个脚本直接生成PDF。

用法：
  python3 scripts/run_jd_to_handbook.py --jd examples/jds/go-backend-cloud.md --session go-demo --mode interview
"""

from __future__ import annotations

import os
import sys
import argparse
import shutil
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")


def init_session(session: str, jd_path: str, mode: str) -> str:
    """初始化session目录结构"""
    session_dir = os.path.join(EXPORTS_DIR, session)
    os.makedirs(session_dir, exist_ok=True)
    os.makedirs(os.path.join(session_dir, "cards"), exist_ok=True)
    os.makedirs(os.path.join(session_dir, "markdown"), exist_ok=True)
    os.makedirs(os.path.join(session_dir, "pdf"), exist_ok=True)

    # 复制JD到raw_jd.md
    raw_jd = os.path.join(session_dir, "raw_jd.md")
    if not os.path.exists(raw_jd):
        shutil.copy2(jd_path, raw_jd)
        print(f"✅ raw_jd.md 已复制")
    else:
        print(f"ℹ️  raw_jd.md 已存在")

    return session_dir


def init_context_pack(session_dir: str, mode: str):
    """初始化context_pack.yaml模板"""
    cp_path = os.path.join(session_dir, "context_pack.yaml")
    if os.path.exists(cp_path):
        print(f"ℹ️  context_pack.yaml 已存在")
        return

    content = f"""# Context Pack - 自动生成
# 原始JD只在Intake阶段使用，后续任务只读本文件

created: {datetime.now(timezone.utc).isoformat()}
mode: {mode}

# 以下字段由JD Intake阶段填充
position: ""
tech_stack: []
experience: ""
priorities:
  P0: []
  P1: []
  P2: []
  P3: []
"""
    with open(cp_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ context_pack.yaml 已初始化")


def init_topic_backlog(session_dir: str):
    """初始化topic_backlog.yaml模板"""
    tb_path = os.path.join(session_dir, "topic_backlog.yaml")
    if os.path.exists(tb_path):
        print(f"ℹ️  topic_backlog.yaml 已存在")
        return

    content = """# Topic Backlog - 由JD分析阶段填充
# 每个topic包含：id, name, priority, source, status

topics: []
# 示例：
# - id: go-goroutine
#   name: goroutine/channel/CSP并发模型
#   priority: P0
#   source: JD显式
#   status: pending
"""
    with open(tb_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ topic_backlog.yaml 已初始化")


def init_state(session_dir: str, mode: str):
    """初始化state.yaml"""
    state_path = os.path.join(session_dir, "state.yaml")
    if os.path.exists(state_path):
        print(f"ℹ️  state.yaml 已存在")
        return

    content = f"""# Session State

session: {os.path.basename(session_dir)}
mode: {mode}
created: {datetime.now(timezone.utc).isoformat()}
current_step: init
completed_steps:
  - init
pending_steps:
  - jd_intake
  - context_pack_build
  - topic_backlog_build
  - card_generation
  - markdown_pack
  - validation
  - pdf_generation
"""
    with open(state_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ state.yaml 已初始化")


def init_source_trace(session_dir: str):
    """初始化source_trace.md"""
    trace_path = os.path.join(session_dir, "source_trace.md")
    if os.path.exists(trace_path):
        print(f"ℹ️  source_trace.md 已存在")
        return

    content = """# Source Trace - 来源追踪

> 每个考点必须记录来源（JD显式/JD隐含/面经高频/项目相关/加分项）
> 格式：| 考点 | 来源 | 说明 |

| 考点 | 来源 | 说明 |
|------|------|------|
"""
    with open(trace_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ source_trace.md 已初始化")


def run_validation(session: str) -> bool:
    """运行校验"""
    from validate_handbook import validate_session
    errors = validate_session(session)
    fails = [e for e in errors if e.startswith("❌")]
    return len(fails) == 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run JD to Handbook Pipeline")
    parser.add_argument("--jd", required=True, help="JD文件路径")
    parser.add_argument("--session", required=True, help="session目录名")
    parser.add_argument("--mode", default="interview", choices=["interview", "learning"],
                        help="模式：interview=面试手册 / learning=学习路线")
    parser.add_argument("--skip-validation", action="store_true", help="跳过校验（开发用）")
    args = parser.parse_args(argv)

    if not os.path.exists(args.jd):
        print(f"❌ JD文件不存在：{args.jd}")
        return 1

    print(f"🚀 启动 Pipeline: {args.session} ({args.mode}模式)")
    print("=" * 50)

    # Step 1: 初始化session
    session_dir = init_session(args.session, args.jd, args.mode)

    # Step 2: 初始化模板文件
    init_context_pack(session_dir, args.mode)
    init_topic_backlog(session_dir)
    init_state(session_dir, args.mode)
    init_source_trace(session_dir)

    print("=" * 50)
    print(f"""
📁 Session目录已创建：{session_dir}

下一步（需要Agent执行）：
1. JD Intake → 分析JD，填充 context_pack.yaml + topic_backlog.yaml + source_trace.md
2. Card Generation → 按topic_backlog逐个生成卡片
3. Markdown Pack → python3 scripts/build_markdown_pack.py --session {args.session}
4. Validate → python3 scripts/validate_handbook.py --session {args.session}
5. PDF → python3 scripts/build-pdf-v2.py --session {args.session}

⚠️ 禁止跳步！每步必须完成才能进入下一步。
""")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
