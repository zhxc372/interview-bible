# Interview Bible MVP Skill

一个基于 Learning System v4.2 的轻量面试表达训练 Skill。

它不是简历优化器，不是八股题库，不是模拟面试平台。它只做一件事：

> 把一个知识点或一个项目经历，整理成有边界、有证据、能被追问的面试卡片。

## 目录结构

```text
interview-bible-skill/
├── SKILL.md
├── README.md
├── router/
│   ├── ls-router.sh
│   ├── router.py
│   ├── route_rules.yaml
│   └── tests/
│       └── test_router.py
├── prompts/
│   ├── 01-knowledge-card.prompt.md
│   ├── 02-project-card.prompt.md
│   └── 03-pressure-q.prompt.md
├── templates/
│   ├── knowledge-card.md
│   └── project-card.md
├── examples/
│   ├── example-mvcc.md
│   ├── example-personal-demo.md
│   ├── blocked-missing-evidence.json
│   └── blocked-mixed-goals.json
└── docs/
    └── router-impl-notes.md
```

## 快速使用

```bash
cd interview-bible-skill
chmod +x router/ls-router.sh
./router/ls-router.sh "我要准备 MVCC 的面试知识卡"
```

示例输出：

```json
{
  "status": "ok",
  "route": "interview_bible",
  "subtype": "knowledge_card",
  "reason": "matched_single_route",
  "message": "✅ 路由成功：interview_bible / knowledge_card",
  "next_action": "加载 prompts/01-knowledge-card.prompt.md"
}
```

## 跑测试

```bash
python3 -m unittest router.tests.test_router
```

## MVP 范围

当前只做：

- Router 路由与拦截
- 面试知识卡 Prompt
- 项目表达卡 Prompt
- 压力追问 Prompt
- 两个模板
- 两个示例

当前不做：

- UI
- 数据库
- 长期记忆
- 完整模拟面试
- 简历优化器
- 八股题库生成器
- 自动代码仓库扫描
- 三工具串联

## 核心铁律

```text
面试要证据。
项目要边界。
知识要取舍。
追问要暴露漏洞。
无证据不生成项目卡。
```
