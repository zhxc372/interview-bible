# Interview Bible v0.4 PRD：Context Optimization + Interview Pack

> 状态：规划中，v0.3跑通完整流程后再启动

---

# 0. 核心问题

JD很长，知识点很多，模板很多，项目经历也很多。
如果一次性塞给AI，context会爆，质量会变差。

# 1. 一句话定位

```
不做"生成一份很大的PDF"，
做"岗位面试材料编译器"。
Context Pack是编译中间层，
Topic Cards是编译单元，
PDF是最终产物。
```

# 2. 架构设计：Map-Reduce

## Map：逐个知识点生成

```text
for each topic:
    读取 context_pack.yaml
    读取当前 topic
    读取当前模板
    生成 topic card
```

输出：
```text
exports/cards/
  go_goroutine/
    knowledge-card.md
    interview-card.md
  db_mvcc/
    knowledge-card.md
    interview-card.md
```

## Reduce：脚本汇总成PDF

```text
exports/cards/*
  ↓ 脚本拼接（不用AI）
exports/markdown/memorization_pack.md
  ↓
exports/pdf/memorization_pack.pdf
```

---

# 3. Context Pack（编译中间层）

核心文件：`exports/context/context_pack.yaml`

```yaml
version: v0.4
position: Go 后端开发工程师

jd_digest:
  role_type: 后端工程师
  seniority: 中级
  core_stack: [Go, MySQL, Redis, 微服务, Linux]
  hidden_requirements:
    - 能解释并发模型
    - 能做性能排查

subject_map:
  - subject: Go 语言
    priority: P0
    topics:
      - id: go_goroutine
        name: goroutine
        priority: P0

project_evidence_index:
  - id: exam_saas
    name: 在线考试系统
    tags: [Go, MySQL, Redis, 权限, 高并发]
    evidence:
      - 设计考试提交链路
      - Redis缓存策略

generation_policy:
  max_topics_per_batch: 1
  include_raw_jd: false
  default_output_level:
    P0: full
    P1: standard
    P2: brief
```

---

# 4. 上下文压缩规则

## 最小上下文原则

1. 原始JD只进入JD Intake阶段
2. Topic Card生成阶段禁止重新注入完整JD
3. 每次只生成一个知识点
4. 项目经历按tag匹配后局部注入
5. PDF通过脚本拼接，不通过大模型整包生成
6. P2知识点默认只生成速记版

## Context Budget

```yaml
budget:
  jd_intake_max_chars: 20000
  topic_card_max_chars: 8000
  quiz_card_max_chars: 6000
  final_pack_max_chars: 50000

rules:
  forbid_raw_jd_in_topic_generation: true
  forbid_full_project_in_topic_generation: true
  max_topics_per_prompt: 1
```

---

# 5. 优先级 = 学习优先级 × 生成深度 × Context分配

| 优先级 | 生成深度 | 是否进PDF主体 |
|--------|---------|-------------|
| P0 | 完整知识点卡 + 面试卡 + 自测题 + 追问 | 是 |
| P1 | 标准卡 + 简短自测 | 是 |
| P2 | 速记卡 + 附录 | 默认进附录 |

---

# 6. 最终产物分3层

1. **完整版** memorization_pack_full.pdf — P0+P1+P2附录+项目卡+自测题
2. **考前速记版** memorization_pack_cram.pdf — P0+高频追问+30秒回答+易混点
3. **自测版** quiz_pack.pdf — 闭卷回忆+场景题+压力追问+评分表

---

# 7. 新增文件结构

```text
context/
  context_rules.md
  context_budget.yaml

exports/
  context/
    context_pack.yaml
  cards/
  markdown/
  pdf/

scripts/
  build_context_pack.py
  build_topic_card.py
  build_markdown_pack.py
  build_pdf.py
  check_context_budget.py
```

---

# 8. v0.4 前置条件

- [ ] v0.3 跑通完整流程（JD → 知识点卡 → 面试卡 → 追问）
- [ ] 至少用2-3个不同JD验证JD解构质量
- [ ] 确认知识点Backlog拆分粒度合适
- [ ] 确认项目证据映射是否够用

**不满足前置条件不开v0.4。**
