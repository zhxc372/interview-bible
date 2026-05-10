# Interview Bible MVP

> 基于 Learning System v4.2 | [GitHub](https://github.com/zhxc372/interview-bible) | [Releases](https://github.com/zhxc372/interview-bible/releases)

一个面试表达训练工具包。

它不是简历优化器，不是八股题库，不是模拟面试平台。它只做一件事：

> **搞清楚 → 讲清楚 → 验证清楚**

---

## 核心模型

Interview Bible 把面试准备拆成两层：

| 卡片 | 目标 | 输出 | 使用时机 |
|------|------|------|----------|
| **知识点卡** | 搞清楚 | 5W1H(9问) + Node Fingerprint(9问) + 最小验证 | 学习、查漏 |
| **面试卡** | 讲清楚 | 30秒版 + 2分钟版 + Trade-off + 易混边界 + 压力追问 | 面试前训练 |
| **项目卡** | 讲清楚（项目） | 6字段 + 证据锚点 + 诚实表达建议 | 项目复盘 |
| **压力追问** | 验证清楚 | 3个追问 + 空泛点 + 缺失证据 | 卡片之后 |

闭环：

```text
知识点卡（搞清楚）
    ↓ 提取
面试卡（讲清楚）
    ↓ 口述
压力追问（验证清楚）
    ↓ 发现漏洞
回填知识点卡（再搞清楚）
```

---

## 目录结构

```text
interview-bible/
├── SKILL.md                    # OpenClaw Skill 入口
├── README.md
├── VERSION
├── PRD.md                      # 产品需求文档
├── router/
│   ├── router.py               # 路由器（Python）
│   ├── route_rules.yaml        # 路由规则（关键词词库）
│   ├── ls-router.sh            # Shell 入口
│   └── tests/
│       └── test_router.py      # 13 个单元测试
├── prompts/
│   ├── 01-knowledge-point-card.prompt.md   # 知识点卡 Prompt
│   ├── 02-interview-card.prompt.md         # 面试卡 Prompt
│   ├── 03-project-card.prompt.md           # 项目表达卡 Prompt
│   └── 04-pressure-q.prompt.md             # 压力追问 Prompt
├── templates/
│   ├── knowledge-point-card.md  # 知识点卡模板
│   ├── interview-card.md        # 面试卡模板
│   └── project-card.md          # 项目卡模板
├── examples/
│   ├── example-mvcc.md
│   ├── example-personal-demo.md
│   ├── blocked-missing-evidence.json
│   └── blocked-mixed-goals.json
└── docs/
    └── router-impl-notes.md
```

---

## 快速使用

```bash
cd interview-bible
chmod +x router/ls-router.sh

# 搞清楚：生成知识点卡
./router/ls-router.sh "我想搞懂 MVCC"

# 讲清楚：生成面试卡
./router/ls-router.sh "帮我准备 MVCC 的面试知识卡"

# 项目卡
./router/ls-router.sh "我要整理一个个人实验项目卡，有代码和测试日志"

# 压力追问
./router/ls-router.sh "帮我生成压力追问"
```

示例输出（知识点卡）：

```json
{
  "status": "ok",
  "route": "interview_bible",
  "subtype": "knowledge_point_card",
  "reason": "matched_single_route",
  "message": "✅ 路由成功：interview_bible / knowledge_point_card",
  "next_action": "加载 prompts/01-knowledge-point-card.prompt.md"
}
```

---

## 跑测试

```bash
python3 -m unittest router.tests.test_router
```

当前 13 个测试全部通过。

---

## Router 拦截规则

Router 先拦截再生成，5 种拦截场景：

| 拦截原因 | 说明 |
|----------|------|
| `empty_input` | 空输入 |
| `unclear_goal` | 没命中任何路由 |
| `mixed_goals` | 同时命中多个路由 |
| `missing_evidence` | 强成果表述 + 无证据锚点 |
| `coding_agent_disabled_in_mvp` | 请求自动代码扫描 |
| `subtype_unclear` | 命中 interview_bible 但不知道要哪种卡 |

---

## 核心铁律

```text
面试要证据。
项目要边界。
知识要取舍。
追问要暴露漏洞。
无证据不生成项目卡。
搞清楚再讲清楚。
```

---

## MVP 范围

✅ 做：
- Router 路由与拦截
- 知识点卡（搞清楚）
- 面试卡（讲清楚）
- 项目表达卡
- 压力追问
- 3 个模板 + 2 个示例

❌ 不做：
- UI / 数据库 / 长期记忆
- 完整模拟面试
- 简历优化器 / 八股题库生成器
- 自动代码仓库扫描
- Anki 闪卡导出（未来考虑）

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.1 | 2026-05-10 | MVP 初始版本：Router + 知识卡 + 项目卡 + 压力追问 |
| v0.2 | 2026-05-10 | 双卡结构：知识点卡(搞清楚) + 面试卡(讲清楚)，13个测试 |
