#!/usr/bin/env python3
"""
Interview Bible MVP Router.

This script is intentionally small and deterministic.
It does not generate interview content. It only decides whether an input can
enter a prompt and which prompt should be loaded.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

DEFAULT_RULES_PATH = os.path.join(os.path.dirname(__file__), "route_rules.yaml")


@dataclass
class RouteDecision:
    status: str
    route: str | None = None
    subtype: str | None = None
    reason: str = ""
    message: str = ""
    next_action: str = ""
    matched_routes: List[str] | None = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "status": self.status,
            "route": self.route,
            "subtype": self.subtype,
            "reason": self.reason,
            "message": self.message,
            "next_action": self.next_action,
        }
        if self.matched_routes:
            data["matched_routes"] = self.matched_routes
        return {k: v for k, v in data.items() if v not in (None, "", [])}


def _simple_yaml_load(text: str) -> Dict[str, Any]:
    """A tiny YAML subset loader for this repository's route_rules.yaml.

    Supported shape:
    key:
      child:
        keywords:
          - item
    list_key:
      - item
    scalar_key: value
    """
    result: Dict[str, Any] = {}
    current_top: str | None = None
    current_child: str | None = None
    current_list_key: str | None = None

    lines = text.splitlines()
    for raw in lines:
        if not raw.strip() or raw.strip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        if indent == 0 and line.endswith(":"):
            current_top = line[:-1]
            result[current_top] = {}
            current_child = None
            current_list_key = None
            continue

        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value.lower() == "false":
                parsed: Any = False
            elif value.lower() == "true":
                parsed = True
            else:
                parsed = value.strip('"\'')
            result[key.strip()] = parsed
            current_top = None
            current_child = None
            current_list_key = None
            continue

        if current_top is None:
            continue

        if indent == 2 and line.endswith(":"):
            key = line[:-1]
            container = result[current_top]
            if isinstance(container, dict):
                # If next items are list entries, this can become a list later.
                container[key] = {}
            current_child = key
            current_list_key = None
            continue

        if indent == 2 and line.startswith("-"):
            # top-level list under current_top
            if not isinstance(result.get(current_top), list):
                result[current_top] = []
            result[current_top].append(line[1:].strip())
            continue

        if indent == 2 and ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value.lower() == "false":
                parsed = False
            elif value.lower() == "true":
                parsed = True
            else:
                parsed = value.strip('"\'')
            result[current_top][key.strip()] = parsed
            continue

        if indent == 4 and current_child and line.endswith(":"):
            current_list_key = line[:-1]
            result[current_top][current_child][current_list_key] = []
            continue

        if indent == 4 and current_child and ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            result[current_top][current_child][key.strip()] = value.strip('"\'')
            continue

        if indent == 6 and current_child and current_list_key and line.startswith("-"):
            result[current_top][current_child][current_list_key].append(line[1:].strip())
            continue

        if indent == 4 and current_child is None and line.startswith("-"):
            if not isinstance(result.get(current_top), list):
                result[current_top] = []
            result[current_top].append(line[1:].strip())
            continue

    return result


def load_rules(path: str = DEFAULT_RULES_PATH) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        if isinstance(loaded, dict):
            return loaded
    except Exception:
        pass

    return _simple_yaml_load(text)


def normalize(text: str) -> str:
    return text.strip()


def contains_any(text: str, keywords: List[str]) -> bool:
    lower = text.lower()
    return any(str(kw).lower() in lower for kw in keywords)


def matched_keys(text: str, keywords: List[str]) -> List[str]:
    lower = text.lower()
    return [str(kw) for kw in keywords if str(kw).lower() in lower]


def match_routes(text: str, rules: Dict[str, Any]) -> List[str]:
    routes = rules.get("routes", {}) or {}
    matched: List[str] = []
    for route_name, route_cfg in routes.items():
        kws = route_cfg.get("keywords", []) if isinstance(route_cfg, dict) else []
        if contains_any(text, kws):
            matched.append(route_name)
    return matched


def match_subtype(text: str, rules: Dict[str, Any]) -> str | None:
    subtypes = rules.get("subtypes", {}) or {}
    # Priority matters: explicit pressure request > knowledge point > interview card > project card.
    for subtype in ("pressure_question", "knowledge_point_card", "interview_card", "project_card"):
        cfg = subtypes.get(subtype, {})
        kws = cfg.get("keywords", []) if isinstance(cfg, dict) else []
        if contains_any(text, kws):
            return subtype
    return None


def prompt_path_for(subtype: str | None) -> str:
    mapping = {
        "knowledge_point_card": "prompts/01-knowledge-point-card.prompt.md",
        "interview_card": "prompts/02-interview-card.prompt.md",
        "project_card": "prompts/03-project-card.prompt.md",
        "pressure_question": "prompts/04-pressure-q.prompt.md",
        "evidence_gap": "返回证据缺口清单，不加载生成 Prompt",
    }
    return mapping.get(subtype or "", "请人工确认后再加载 Prompt")


def decide(text: str, rules: Dict[str, Any] | None = None) -> RouteDecision:
    rules = rules or load_rules()
    text = normalize(text)

    if not text:
        return RouteDecision(
            status="blocked",
            reason="empty_input",
            message="⛔ 输入为空。请说明你要做：面试表达、教材学习、陌生领域探索，还是代码证据提取。",
            next_action="补充一个明确任务。",
        )

    matched = match_routes(text, rules)

    if not matched:
        return RouteDecision(
            status="blocked",
            reason="unclear_goal",
            message="⛔ 当前目标不清楚。请说明你要做：面试表达、教材学习、陌生领域探索，还是代码证据提取。",
            next_action=str(rules.get("fallback_action", "manual_confirm")),
        )

    if len(matched) > 1:
        return RouteDecision(
            status="blocked",
            reason="mixed_goals",
            message="⛔ 当前输入包含多个目标。本轮只能选择一个：面试表达 / 教材学习 / 陌生领域探索 / 代码证据提取。",
            next_action="重新输入一个单一目标。",
            matched_routes=matched,
        )

    route = matched[0]

    if route == "coding_agent" and not bool(rules.get("coding_agent_enabled_in_mvp", False)):
        return RouteDecision(
            status="blocked",
            route=route,
            subtype="evidence_extract",
            reason="coding_agent_disabled_in_mvp",
            message="⛔ MVP 阶段暂不启用自动代码扫描。请手动提供代码片段、日志、commit、PR、压测结果、截图或 Demo 说明。",
            next_action="手动提供至少一个证据锚点。",
        )

    risky_words = rules.get("risky_claims", []) or []
    evidence_words = rules.get("evidence_words", []) or []
    has_risky = contains_any(text, risky_words)
    has_evidence = contains_any(text, evidence_words)

    if route == "interview_bible" and has_risky and not has_evidence:
        return RouteDecision(
            status="blocked",
            route=route,
            subtype="evidence_gap",
            reason="missing_evidence",
            message="⛔ 当前描述包含强成果表述，但缺少证据锚点。请提供代码、日志、commit、PR、压测、截图或 Demo。否则只能生成【练习表达卡】或【证据缺口清单】。",
            next_action="补充证据，或降级为【个人实验】练习表达卡 / 证据缺口清单。",
        )

    subtype = match_subtype(text, rules)

    if route == "interview_bible" and subtype is None:
        return RouteDecision(
            status="blocked",
            route=route,
            reason="subtype_unclear",
            message="⛔ 已识别为 Interview Bible，但未确定是知识卡、项目卡还是压力追问。",
            next_action="请选择：knowledge_card / project_card / pressure_question。",
        )

    return RouteDecision(
        status="ok",
        route=route,
        subtype=subtype,
        reason="matched_single_route",
        message=f"✅ 路由成功：{route}" + (f" / {subtype}" if subtype else ""),
        next_action=f"加载 {prompt_path_for(subtype)}",
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Interview Bible MVP router")
    parser.add_argument("text", nargs="*", help="User input text to route")
    parser.add_argument("--rules", default=DEFAULT_RULES_PATH, help="Path to route_rules.yaml")
    args = parser.parse_args(argv)

    text = " ".join(args.text).strip()
    rules = load_rules(args.rules)
    decision = decide(text, rules)
    print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2))
    return 0 if decision.status == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
