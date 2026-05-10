# Interview Bible Skill

## Purpose

Interview Bible is a lightweight interview-expression training skill based on Learning System v4.2.

It has two core abilities:

1. **知识点卡** — 搞清楚。通过 5W1H + Node Fingerprint 建立节点级理解。
2. **面试卡** — 讲清楚。把理解压缩成可口述、可追问、可验证的面试表达。

Plus: 项目表达卡 + 压力追问。

Core rules:

- 面试要证据。
- 项目要边界。
- 知识要取舍。
- 追问要暴露漏洞。
- 无证据不生成项目卡。
- 无 router pass 不执行 prompt。
- 搞清楚 → 讲清楚 → 被追问 → 暴露漏洞 → 再搞清楚（闭环）。

## When to use this skill

Use this skill when the user asks for any of the following:

- JD输入 / 岗位描述 / 招聘要求 → **JD解构卡**
- 继续 / 恢复 / 进度 / 下一个 → **会话恢复**
- 搞懂 / 搞清楚 / 梳理 / 分清 / 学明白一个知识点 → **知识点卡**
- 面试怎么讲 / 2分钟讲清 / 帮我准备回答 → **面试卡**
- 项目表达卡 / 项目复盘 → **项目卡**
- 压力追问 / 追问我 → **压力追问**
- 证据缺口检查 → **证据缺口清单**
- 诚实表达个人 Demo / 课程项目 / 开源贡献

## When not to use this skill

Do not use this skill for:

- full curriculum teaching
- general exam training
- unknown domain roadmap exploration
- resume beautification
- fake project packaging
- generating perfect memorization scripts
- automatic repository scanning during MVP
- long multi-role mock interview systems

## Mandatory workflow

1. Route first.
2. If blocked, return the blocker and ask for the next valid action.
3. If routed to jd intake, use `prompts/00-jd-intake.prompt.md`.
4. If routed to session resume, read `exports/` state.yaml to restore progress.
5. If routed to knowledge point card, use `prompts/01-knowledge-point-card.prompt.md`.
6. If routed to interview card, use `prompts/02-interview-card.prompt.md`.
7. If routed to project card, use `prompts/03-project-card.prompt.md`.
8. If routed to pressure question, use `prompts/04-pressure-q.prompt.md`.
9. Every output must include a validation action and a stop condition.
10. After generating a card, update `state.yaml` progress.

Suggested local router command:

```bash
./router/ls-router.sh "我想搞懂 MVCC"
```

## Card types

| 卡片 | 目标 | 输出 | 使用时机 |
|------|------|------|----------|
| JD解构卡 | 找方向 | 备考科目图谱 + 知识点Backlog + 项目证据映射 | 拿到JD后 |
| 知识点卡 | 搞清楚 | 5W1H + Node Fingerprint + 最小验证 | 学习、查漏 |
| 面试卡 | 讲清楚 | 30秒版 + 2分钟版 + Trade-off + 易混边界 + 压力追问 | 面试前训练 |
| 项目卡 | 讲清楚（项目） | 6字段 + 证据锚点 + 诚实表达建议 | 项目复盘 |
| 压力追问 | 验证清楚 | 3个追问 + 空泛点 + 缺失证据 | 卡片之后 |

## Closed loop

```text
JD输入（找方向）
    ↓
知识点卡（搞清楚）
    ↓ 提取
面试卡（讲清楚）
    ↓ 口述
压力追问（验证清楚）
    ↓ 发现漏洞
回填知识点卡（再搞清楚）
```

## Hard blockers

Block immediately when:

- the input mixes multiple goals
- the input asks to package or exaggerate a project without evidence
- the input requests automatic code scanning during MVP
- the input attempts to present a personal demo as production work
- the input asks for a full memorization script instead of answer direction

## Evidence policy

Strong evidence: code snippet, commit/PR/diff, logs, benchmark, screenshot, README, reproducible demo

Weak evidence: "I optimized it", "I participated in design", "The performance improved"

Missing evidence: strong claims without any anchor

If evidence is weak or missing, provide an honest expression suggestion rather than upgrading the claim.

## Project type labels

Every project card must start with one of these labels: 【商业生产】【个人实验】【开源贡献】【课程作业】【理论推演】

## Stop condition

Every skill response should end with:

```text
⛔ 本轮已停止。
下一步唯一动作：____
```
