# Interview Bible v0.4 PRD：Context Optimization + State Persistence + Interview Pack

> 状态：开发中

---

# 0. 核心问题

1. **Context爆炸**：JD长、知识点多、项目多，一次性塞给AI质量会差
2. **状态丢失**：中断后不知道做到哪了，无法继续
3. **无法导出**：卡片散在对话里，没有结构化产物

# 1. 一句话定位

```
不做"生成一份很大的PDF"，
做"岗位面试材料编译器"。
Context Pack是编译中间层，
State是进度记录，
Topic Cards是编译单元，
Markdown/PDF是最终产物。
```

# 2. 架构：Map-Reduce + State Machine

```text
JD输入
  ↓ JD Intake（一次性）
  ↓ 生成 context_pack.yaml + state.yaml
  ↓
循环：for each topic in backlog:
  ↓ 读取 state.yaml → 找到断点
  ↓ 读取 context_pack.yaml（最小上下文）
  ↓ 生成 topic card → 写入 exports/cards/{topic_id}/
  ↓ 更新 state.yaml（标记完成）
  ↓
Reduce：脚本拼接
  ↓ exports/markdown/memorization_pack.md
  ↓ exports/pdf/memorization_pack.pdf（可选）
```

---

# 3. State Persistence（状态持久化）

## 核心文件：state.yaml

位置：`exports/{session}/state.yaml`

```yaml
session_id: go-backend-20260510
position: 云平台后端工程师
created: 2026-05-10
updated: 2026-05-10
status: in_progress  # in_progress / completed / paused

backlog:
  - id: go_goroutine
    name: Go并发模型
    priority: P0
    knowledge_card: done      # done / pending / skipped
    interview_card: done
    pressure_q: done

  - id: go_channel
    name: Channel深入
    priority: P0
    knowledge_card: done
    interview_card: pending
    pressure_q: pending

  - id: go_context
    name: Context
    priority: P0
    knowledge_card: pending
    interview_card: pending
    pressure_q: pending

current_focus: go_channel
next_action: 生成 interview_card

project_evidence_mapped: false
```

## 恢复逻辑

```text
用户说："继续" / "恢复" / "接着来"
  ↓
查找 exports/ 下最新的 state.yaml
  ↓
读取 current_focus + next_action
  ↓
告诉用户当前进度和下一步
  ↓
从断点继续
```

## Router新增关键词

```yaml
session_resume:
  keywords:
    - 继续
    - 恢复
    - 接着来
    - 上次做到哪了
    - 进度
    - 还差什么
    - 下一个
```

---

# 4. Context Pack（编译中间层）

核心文件：`exports/{session}/context_pack.yaml`

JD Intake阶段生成，后续所有任务只读这个压缩版，不再读原始JD。

```yaml
version: v0.4
position: Go 后端开发工程师

jd_digest:
  role_type: 后端工程师
  seniority: 中级
  core_stack: [Go, Gin, Docker, Kubernetes]
  hidden_requirements:
    - 云平台业务理解
    - 多云对接能力
    - API设计能力

subject_map:
  - subject: Go 语言
    priority: P0
    topics:
      - id: go_goroutine
        name: goroutine/channel
        priority: P0
      - id: go_context
        name: context
        priority: P0

  - subject: 容器化
    priority: P0
    topics:
      - id: docker_basics
        name: Docker基础
        priority: P0
      - id: k8s_core
        name: Kubernetes核心
        priority: P0

project_evidence_index:
  - id: project_1
    name: （待用户补充）
    tags: []
    evidence: []

generation_policy:
  max_topics_per_batch: 1
  include_raw_jd: false
  default_output_level:
    P0: full
    P1: standard
    P2: brief
```

---

# 5. 上下文压缩规则

文件：`context/context_rules.md`

1. 原始JD只进入JD Intake阶段
2. Topic Card生成阶段禁止重新注入完整JD
3. 每次只生成一个知识点
4. 项目经历按tag匹配后局部注入
5. Markdown/PDF通过脚本拼接
6. P2知识点默认只生成速记版

## Context Budget

文件：`context/context_budget.yaml`

```yaml
budget:
  jd_intake_max_chars: 20000
  topic_card_max_chars: 8000
  pressure_q_max_chars: 6000
  final_pack_max_chars: 50000

rules:
  forbid_raw_jd_in_topic_generation: true
  forbid_full_project_in_topic_generation: true
  max_topics_per_prompt: 1
```

---

# 6. 文件结构

```text
interview-bible/
├── context/
│   ├── context_rules.md
│   └── context_budget.yaml
├── exports/           ← 按session组织
│   └── {session}/
│       ├── state.yaml
│       ├── context_pack.yaml
│       ├── jd-analysis-card.md
│       ├── cards/
│       │   ├── go_goroutine/
│       │   │   ├── knowledge-card.md
│       │   │   ├── interview-card.md
│       │   │   └── pressure-q.md
│       │   └── go_context/
│       │       └── ...
│       ├── markdown/
│       │   ├── memorization_pack_full.md
│       │   ├── memorization_pack_cram.md
│       │   └── quiz_pack.md
│       └── pdf/
│           └── （未来生成）
├── scripts/
│   ├── build_context_pack.py
│   ├── build_markdown_pack.py
│   └── check_context_budget.py
└── ...
```

---

# 7. 最终产物分3层

1. **完整版** memorization_pack_full.md — P0+P1+P2附录+项目卡+自测题
2. **考前速记版** memorization_pack_cram.md — P0+高频追问+30秒回答+易混点
3. **自测版** quiz_pack.md — 闭卷回忆+场景题+压力追问+评分表

---

# 8. v0.4 最小实现范围

## 必做

1. ✅ State Persistence — state.yaml 读写 + 恢复逻辑
2. ✅ Context Pack — context_pack.yaml 生成 + 读取
3. ✅ Context Rules + Budget — 规则文件
4. ✅ Router新增 session_resume subtype
5. ✅ 测试覆盖

## 暂不做

- ❌ PDF生成（Markdown先跑通）
- ❌ 自动代码扫描
- ❌ Web UI

---

# 9. 成功标准

- [ ] JD Intake后自动生成 state.yaml + context_pack.yaml
- [ ] 每生成一张卡片，state.yaml自动更新
- [ ] 中断后说"继续"能从断点恢复
- [ ] 生成卡片时不读取完整JD，只读context_pack.yaml
- [ ] Markdown汇总包能从cards/目录脚本生成
- [ ] 16+个测试全部通过
