# Interview Bible Skill

## Purpose

Interview Bible is a lightweight interview-expression training skill based on Learning System v4.2.

It turns a single knowledge topic or a single project experience into a concise, evidence-aware interview card that can survive pressure questions.

Core rules:

- Interview needs evidence.
- Knowledge needs trade-off.
- Project needs boundary.
- Pressure questions expose weakness.
- No evidence, no project card.
- No router pass, no prompt execution.

## When to use this skill

Use this skill when the user asks for any of the following:

- technical interview preparation
- interview knowledge card
- project expression card
- project retrospective for interview
- pressure questions
- technical answer refinement
- evidence gap check
- honest expression of a personal demo, course project, open-source contribution, or production project

Examples:

- “帮我准备 MVCC 的面试知识卡”
- “把这个项目整理成面试项目卡”
- “帮我生成 3 个压力追问”
- “我这个 Demo 怎么诚实地讲给面试官”
- “这个项目有什么证据缺口”

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
3. If routed to knowledge card, use `prompts/01-knowledge-card.prompt.md`.
4. If routed to project card, use `prompts/02-project-card.prompt.md`.
5. If the user asks for pressure questions on an existing card, use `prompts/03-pressure-q.prompt.md`.
6. Every output must include a validation action and a stop condition.

Suggested local router command:

```bash
./router/ls-router.sh "我要准备 MVCC 的面试知识卡"
```

## Hard blockers

Block immediately when:

- the input mixes multiple goals
- the input asks to package or exaggerate a project without evidence
- the input requests automatic code scanning during MVP
- the input attempts to present a personal demo as production work
- the input asks for a full memorization script instead of answer direction

## Evidence policy

Strong evidence:

- code snippet
- commit / PR / diff
- logs
- benchmark or test result
- screenshot
- README or design document
- reproducible demo

Weak evidence:

- “I optimized it”
- “I participated in design”
- “The performance improved”
- “The system was stable”

Missing evidence:

- strong claims without any anchor

If evidence is weak or missing, provide an honest expression suggestion rather than upgrading the claim.

## Project type labels

Every project card must start with one of these labels:

- 【商业生产】
- 【个人实验】
- 【开源贡献】
- 【课程作业】
- 【理论推演】

Never omit the label.

## Output discipline

Knowledge card:

- maximum 500 Chinese characters where possible
- 5 fields only
- no full textbook explanation
- no forced project hook
- 3 pressure questions only

Project card:

- 6 fields only
- must include project type
- must include “what I was responsible for / what I was not responsible for”
- must include evidence anchors
- must not fabricate production metrics

Pressure questions:

- exactly 3 questions
- target trade-off, failure mode, or evidence gap
- give answer direction only, not a complete standard answer

## Stop condition

Every skill response should end with:

```text
⛔ 本轮已停止。
下一步唯一动作：____
```
