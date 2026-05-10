# Interview Bible v0.5 PRD

# 双模式面试备考系统：全量地图 + 定点深挖

## 0. 版本结论

v0.5 的核心方向应该调整为：

> **输入 JD 或岗位方向，先生成完整知识地图；再允许用户选择“全量学习”或“特定知识点深挖”；最后形成可背诵、可测试、可打印、可复盘的面试训练包。**

也就是说，v0.5 不再只强调“面试就绪度诊断”，而是要同时支持两类人：

| 用户类型               | 核心需求      | 系统模式    |
| ------------------ | --------- | ------- |
| 小白 / 转岗 / 不知道学什么   | 需要完整知识点地图 | 全量知识点模式 |
| 有基础 / 临近面试 / 某些点薄弱 | 需要针对性补强   | 特定知识点模式 |

---

# 1. 产品定位

## 1.1 产品名称

**Interview Bible v0.5：Dual-Mode Interview Prep Engine**

中文名：

> **双模式面试备考引擎**

---

## 1.2 一句话定位

> **把 JD 或岗位方向转化为完整知识地图，并支持用户按“全量学习”或“定点深挖”两种方式生成面试背诵包、自测包和训练计划。**

---

## 1.3 最终目的

Interview Bible 的最终目的不是单纯生成八股文，而是帮助用户完成这条链路：

```text
知道要学什么
↓
知道哪些必须优先学
↓
每个知识点能搞清楚
↓
每个知识点能讲清楚
↓
每个知识点能被追问验证
↓
最终形成自己的面试表达包
```

---

# 2. v0.5 核心变化

## 2.1 从单一路径改成双模式

之前的路线偏向：

```text
JD → 差距诊断 → 针对性训练
```

v0.5 改成：

```text
JD / 岗位方向
↓
完整知识地图
↓
用户选择模式
├── 全量知识点模式
└── 特定知识点模式
↓
生成知识点卡 / 面试卡 / 自测题 / PDF
```

---

## 2.2 Readiness Engine 仍然保留

“面试就绪度”不是删掉，而是放到评估层。

它的作用是：

```text
判断每个知识点当前处于什么状态：
1. 没学过
2. 懂一点
3. 能讲
4. 能抗追问
5. 能结合项目讲
```

---

# 3. 用户场景

## 3.1 场景一：小白准备某类岗位

用户输入：

```text
我想准备 Go 后端开发岗位，但我是小白。
请给我完整知识点地图。
```

系统输出：

```text
Go 后端岗位完整知识地图
├── Go 语言基础
├── Go 并发
├── 数据结构与算法
├── 操作系统
├── 计算机网络
├── MySQL
├── Redis
├── 消息队列
├── 微服务
├── 分布式系统
├── 项目经验
└── 系统设计
```

并标注：

```text
P0：必须掌握
P1：高频掌握
P2：加分掌握
P3：暂缓
```

---

## 3.2 场景二：用户有具体 JD

用户输入：

```text
这是一个 Go 后端 JD，请帮我生成面试准备路线。
```

系统输出：

```text
JD 解构
↓
岗位能力模型
↓
完整知识点地图
↓
P0/P1/P2 优先级
↓
建议先生成哪些卡片
```

---

## 3.3 场景三：用户只想补某几个点

用户输入：

```text
我只想准备 MVCC、Redis 缓存一致性、Go context、GMP。
```

系统输出：

```text
只针对这 4 个知识点生成：
- 知识点卡
- 面试卡
- 高频追问
- 自测题
- 背诵 PDF
```

---

## 3.4 场景四：用户已经生成完整地图，现在选点深挖

用户先生成完整地图：

```text
Go 后端完整知识地图
```

然后选择：

```text
先生成 P0 里的 Go 并发、MySQL、Redis。
```

系统只处理被选中的知识点。

---

# 4. v0.5 核心模式

## 4.1 Mode A：全量知识点模式

### 目标

帮助小白或转岗用户建立完整备考地图。

### 输入

```text
岗位方向 / JD / 目标公司类型 / 用户基础
```

### 输出

```text
完整知识点地图
P0/P1/P2/P3 优先级
学习顺序
知识点依赖关系
建议第一批生成卡片的知识点
```

### 关键原则

全量模式不等于一次性生成所有完整卡片。

全量模式分三层输出：

| 层级       | 内容        | 是否完整生成  |
| -------- | --------- | ------- |
| 全量知识地图   | 所有知识点     | 是       |
| P0 知识点卡  | 最重要知识点    | 是       |
| P1/P2/P3 | 列表 + 简要说明 | 默认不完整生成 |

这样既满足小白要完整地图，又避免 context 爆炸。

---

## 4.2 Mode B：特定知识点模式

### 目标

针对用户指定的知识点进行深度准备。

### 输入

```text
知识点名称 / 知识点列表 / 从全量地图中选择的 topic_id
```

### 输出

每个知识点生成：

```text
知识点卡
面试卡
项目连接卡
压力追问
自测题
速记卡
```

### 适合用户

```text
有基础的人
临近面试的人
错题复盘的人
只想补短板的人
```

---

## 4.3 Mode C：混合模式

### 目标

先生成完整地图，再让用户选择重点。

### 流程

```text
生成全量知识地图
↓
用户选择 P0 / P1 / 指定知识点
↓
系统生成对应卡片
↓
用户自测
↓
回填薄弱项
↓
生成最终 PDF
```

这是推荐默认流程。

---

# 5. 核心流程

## 5.1 总流程

```text
1. 输入 JD / 岗位方向 / 指定知识点
   ↓
2. Router 判断模式
   ↓
3. 生成 Knowledge Map
   ↓
4. 用户选择生成范围
   ↓
5. 生成 Context Pack
   ↓
6. 分 topic 生成卡片
   ↓
7. 生成 Quiz Pack
   ↓
8. 生成 Readiness Report
   ↓
9. 导出 Markdown / PDF
```

---

## 5.2 全量模式流程

```text
岗位方向 / JD
↓
岗位能力模型
↓
完整知识点地图
↓
P0/P1/P2/P3 分级
↓
学习顺序
↓
第一批建议生成卡片
↓
生成 P0 核心卡片
↓
导出全量知识地图 PDF
```

---

## 5.3 特定知识点模式流程

```text
用户指定知识点
↓
识别知识点类型
↓
读取最小上下文
↓
生成知识点卡
↓
生成面试卡
↓
生成自测题
↓
生成速记版
↓
导出专项 PDF
```

---

# 6. v0.5 核心产物

## 6.1 Knowledge Map

文件：

```text
exports/knowledge-map.md
exports/knowledge-map.yaml
```

用途：

> 给用户一张完整备考地图。

示例结构：

```yaml
position: Go 后端开发工程师

subjects:
  - name: Go 语言
    priority: P0
    topics:
      - id: go_goroutine
        name: goroutine
        priority: P0
        reason: Go 后端高频基础
      - id: go_channel
        name: channel
        priority: P0
      - id: go_context
        name: context
        priority: P0
      - id: go_gmp
        name: GMP 调度模型
        priority: P1

  - name: 数据库
    priority: P0
    topics:
      - id: mysql_index
        name: MySQL 索引
        priority: P0
      - id: mysql_mvcc
        name: MVCC
        priority: P0
      - id: mysql_transaction
        name: 事务隔离级别
        priority: P0
```

---

## 6.2 Topic Card

文件：

```text
exports/cards/{topic_id}/knowledge-card.md
```

用途：

> 搞清楚一个知识点。

内容：

```text
What：它是什么
Why：为什么需要它
How：它如何工作
When：什么时候使用
Where：处在哪一层
Who：谁使用它
What if：用错会怎样
How know：如何验证理解
How much：成本、收益、权衡
Node Fingerprint
```

---

## 6.3 Interview Card

文件：

```text
exports/cards/{topic_id}/interview-card.md
```

用途：

> 讲清楚一个知识点。

内容：

```text
一句话定义
30 秒回答
2 分钟回答
必须讲到的关键词
常见追问
易混边界
工程取舍
项目连接
```

---

## 6.4 Quiz Card

文件：

```text
exports/cards/{topic_id}/quiz-card.md
```

用途：

> 验证是否真的掌握。

内容：

```text
闭卷回忆题
简答题
场景题
压力追问
自评分表
错题回填区
```

---

## 6.5 Readiness Report

文件：

```text
exports/readiness-report.md
```

用途：

> 判断当前准备状态。

评分模型：

| 层级      | 含义      |
| ------- | ------- |
| L1 知识理解 | 能不能解释清楚 |
| L2 面试表达 | 能不能说出来  |
| L3 项目证据 | 能不能结合经历 |
| L4 压力追问 | 能不能扛追问  |

评分：

| 分数 | 含义   |
| -: | ---- |
|  0 | 不会   |
|  1 | 知道一点 |
|  2 | 能正常讲 |
|  3 | 能抗追问 |

---

## 6.6 Print Pack

文件：

```text
exports/print/full-knowledge-map.pdf
exports/print/focused-topic-pack.pdf
exports/print/quiz-pack.pdf
exports/print/final-cram-pack.pdf
```

用途：

> 打印、背诵、考前复习。

---

# 7. 优先级设计

## 7.1 P0/P1/P2/P3 定义

| 等级 | 含义         | 默认处理方式 |
| -- | ---------- | ------ |
| P0 | 岗位必备，高频必问  | 生成完整卡片 |
| P1 | 高频重要，经常追问  | 生成标准卡片 |
| P2 | 加分项，有时间再补  | 生成速记卡  |
| P3 | 暂缓项，当前阶段不学 | 只进入地图  |

---

## 7.2 全量模式下的生成策略

| 内容        | 是否生成  |
| --------- | ----- |
| 完整知识地图    | 生成    |
| P0 完整知识点卡 | 生成    |
| P0 面试卡    | 生成    |
| P0 自测题    | 生成    |
| P1 标准卡    | 可选    |
| P2 速记卡    | 可选    |
| P3        | 只列入地图 |

---

## 7.3 特定知识点模式下的生成策略

只要用户明确指定知识点，就默认完整生成：

```text
知识点卡
面试卡
项目卡
压力追问
自测题
速记卡
```

---

# 8. Context 设计

v0.5 必须继续控制上下文。

## 8.1 核心原则

```text
全量地图可以一次生成
完整卡片必须分 topic 生成
PDF 必须由脚本拼接
原始 JD 只进入 JD Intake
Topic 生成阶段使用 Context Pack
```

---

## 8.2 新增 Context Pack

文件：

```text
exports/context/context-pack.yaml
```

结构：

```yaml
version: v0.5

input_mode: full_map | focused_topics | mixed

position:
  title: Go 后端开发工程师
  level: junior | mid | senior
  source: jd | role_name | manual_topics

jd_digest:
  core_stack:
    - Go
    - MySQL
    - Redis
    - 微服务
  explicit_requirements:
    - 熟悉 Go 并发
    - 熟悉 MySQL 调优
  hidden_requirements:
    - 能处理线上问题
    - 能讲清楚服务治理
    - 能解释性能优化

selected_topics:
  - go_context
  - mysql_mvcc
  - redis_cache_consistency

generation_policy:
  mode: focused_topics
  max_topics_per_batch: 1
  include_raw_jd: false
  include_full_project: false
  default_depth:
    P0: full
    P1: standard
    P2: brief
    P3: map_only
```

---

# 9. Router 设计

## 9.1 新增 subtype

```yaml
full_knowledge_map:
  description: 生成完整岗位知识点地图
  keywords:
    - 完整知识点
    - 全部知识点
    - 全量知识地图
    - 小白
    - 从零准备
    - 岗位路线
    - 学习路线
    - 备考地图

focused_topic_pack:
  description: 针对指定知识点生成深度卡片
  keywords:
    - 指定知识点
    - 只准备
    - 重点准备
    - 深挖
    - 专项
    - 生成这个知识点
    - 针对这些知识点

mixed_interview_pack:
  description: 先生成地图，再选择重点生成面试包
  keywords:
    - 先给地图
    - 再选择
    - 按优先级生成
    - P0 优先
    - 先全量再重点
```

---

# 10. Prompt 设计

## 10.1 新增 Prompt 文件

```text
prompts/00-mode-router.prompt.md
prompts/01-full-knowledge-map.prompt.md
prompts/02-focused-topic-pack.prompt.md
prompts/03-context-pack.prompt.md
prompts/04-topic-card.prompt.md
prompts/05-interview-card.prompt.md
prompts/06-quiz-card.prompt.md
prompts/07-readiness-report.prompt.md
prompts/08-print-pack.prompt.md
```

---

## 10.2 Full Knowledge Map Prompt 目标

输入：

```text
岗位方向 / JD / 用户基础
```

输出：

```text
完整知识点地图
科目分类
P0/P1/P2/P3
学习顺序
依赖关系
建议第一批生成卡片的知识点
```

---

## 10.3 Focused Topic Pack Prompt 目标

输入：

```text
指定知识点列表
岗位方向
用户项目经历，可选
```

输出：

```text
每个知识点的：
- 知识点卡
- 面试卡
- 高频追问
- 自测题
- 速记卡
```

---

# 11. Template 设计

## 11.1 新增模板

```text
templates/knowledge-map.md
templates/knowledge-map.yaml
templates/context-pack.yaml
templates/topic-card.md
templates/interview-card.md
templates/quiz-card.md
templates/readiness-report.md
templates/print-pack.md
```

---

## 11.2 Knowledge Map 模板

```md
# {{position}} 面试知识地图

## 1. 岗位画像

{{role_profile}}

## 2. 科目总览

| 科目 | 优先级 | 说明 |
|---|---|---|
| {{subject}} | {{priority}} | {{reason}} |

## 3. 全量知识点地图

### {{subject_name}}

| 知识点 | 优先级 | 依赖 | 面试频率 | 建议动作 |
|---|---|---|---|---|
| {{topic}} | {{priority}} | {{dependency}} | {{frequency}} | {{action}} |

## 4. 小白学习顺序

{{learning_order}}

## 5. 第一批建议生成卡片

{{first_batch_topics}}
```

---

# 12. 输出设计

## 12.1 全量模式输出

```text
exports/
  knowledge-map.md
  knowledge-map.yaml
  context/context-pack.yaml
  cards/
    p0/
  print/
    full-knowledge-map.pdf
    p0-memory-pack.pdf
    p0-quiz-pack.pdf
```

---

## 12.2 特定知识点模式输出

```text
exports/
  selected-topics.md
  context/context-pack.yaml
  cards/
    go_context/
    mysql_mvcc/
    redis_cache_consistency/
  print/
    focused-topic-pack.pdf
    focused-quiz-pack.pdf
```

---

## 12.3 混合模式输出

```text
exports/
  knowledge-map.md
  selected-topics.md
  readiness-report.md
  training-plan.md
  print/
    final-cram-pack.pdf
    final-quiz-pack.pdf
```

---

# 13. 脚本设计

## 13.1 新增脚本

```text
scripts/
  build_knowledge_map.py
  build_context_pack.py
  build_topic_cards.py
  build_print_pack.py
  build_pdf.py
  check_context_budget.py
```

---

## 13.2 `build_knowledge_map.py`

职责：

```text
读取 JD / 岗位方向
生成 knowledge-map.yaml
生成 knowledge-map.md
```

---

## 13.3 `build_context_pack.py`

职责：

```text
根据模式生成 context-pack.yaml
控制输入范围
控制 selected_topics
控制生成深度
```

---

## 13.4 `build_topic_cards.py`

职责：

```text
按 topic_id 分批生成卡片
每次只处理一个 topic
输出到 exports/cards/{topic_id}
```

---

## 13.5 `build_print_pack.py`

职责：

```text
拼接 Markdown
生成完整地图包
生成专项知识点包
生成自测包
生成考前速记包
```

---

## 13.6 `build_pdf.py`

职责：

```text
Markdown 转 PDF
支持中文字体
输出到 exports/print/
```

---

# 14. MVP 边界

## 14.1 v0.5 必须做

```text
支持全量知识点地图
支持指定知识点深挖
支持 P0/P1/P2/P3 优先级
支持 Context Pack
支持分 topic 生成
支持 Markdown 导出
支持 PDF 导出
支持自测题
支持 Readiness Report
```

---

## 14.2 v0.5 暂不做

```text
Web UI
数据库
长期记忆
自动爬 JD
自动扫描代码仓库
自动投简历
虚假项目包装
完整语音模拟面试
Anki 导出
多用户系统
```

---

# 15. 验收标准

## 15.1 全量知识点模式验收

输入：

```text
我想从零准备 Go 后端面试，请生成完整知识点地图。
```

系统应输出：

```text
knowledge-map.md
knowledge-map.yaml
```

并包含：

```text
科目分类
完整知识点
P0/P1/P2/P3
学习顺序
第一批建议生成卡片
```

---

## 15.2 特定知识点模式验收

输入：

```text
请只针对 MVCC、Redis 缓存一致性、Go context 生成面试卡和自测题。
```

系统应输出：

```text
exports/cards/mysql_mvcc/
exports/cards/redis_cache_consistency/
exports/cards/go_context/
```

每个目录包含：

```text
knowledge-card.md
interview-card.md
quiz-card.md
memory-card.md
```

---

## 15.3 Context 验收

必须满足：

```text
Topic Card 生成阶段不读取完整 JD
每次只生成一个 topic
PDF 由脚本拼接
P3 不生成完整卡片
selected_topics 明确记录在 context-pack.yaml
```

---

## 15.4 PDF 验收

必须生成：

```text
full-knowledge-map.pdf
focused-topic-pack.pdf
quiz-pack.pdf
```

要求：

```text
中文正常显示
标题层级清楚
可以打印
每个知识点分页
自测题有答题区
```

---

# 16. 测试设计

## 16.1 Router 测试

```text
test_route_full_knowledge_map
test_route_focused_topic_pack
test_route_mixed_interview_pack
```

---

## 16.2 Knowledge Map 测试

```text
test_generate_knowledge_map_yaml
test_knowledge_map_has_subjects
test_knowledge_map_has_priorities
test_knowledge_map_has_learning_order
```

---

## 16.3 Context Pack 测试

```text
test_context_pack_has_mode
test_context_pack_has_selected_topics
test_max_topics_per_batch_is_one
test_raw_jd_not_in_topic_generation
```

---

## 16.4 Card Generation 测试

```text
test_generate_topic_card
test_generate_interview_card
test_generate_quiz_card
test_generate_memory_card
```

---

## 16.5 PDF 测试

```text
test_build_markdown_pack
test_build_pdf_output_exists
test_pdf_supports_chinese_font
```

---

# 17. 推荐默认交互

## 17.1 用户输入 JD 后，系统默认输出

```text
我已经根据 JD 生成了完整知识点地图。

你可以选择：

1. 小白模式：按 P0 → P1 → P2 生成完整学习包
2. 冲刺模式：只生成 P0 高频面试包
3. 专项模式：选择几个知识点深挖
4. 测试模式：直接生成自测题，看你哪里不会
```

---

## 17.2 小白模式默认策略

```text
先生成完整地图
再生成 P0 卡片
P1 只生成简版
P2 进入附录
P3 暂缓
```

---

## 17.3 冲刺模式默认策略

```text
只生成 P0
每个 P0 包含：
- 30 秒回答
- 2 分钟回答
- 高频追问
- 易混点
- 自测题
```

---

## 17.4 专项模式默认策略

```text
用户指定什么，就生成什么
不自动扩展太多
最多补充必要前置知识
```

---

# 18. 给代码 Agent 的实现 Prompt

```text
请基于当前 interview-bible 仓库，重新设计并实现 v0.5：Dual-Mode Interview Prep Engine。

v0.5 的核心目标：
支持两种面试准备方式：
1. 全量知识点模式：适合小白或转岗用户，先生成完整岗位知识地图。
2. 特定知识点模式：适合有基础或临近面试用户，只针对指定知识点生成深度卡片、自测题和打印包。

必须实现：

1. 新增 docs/prd-v0.5.md
   - 写清楚 v0.5 是双模式系统
   - 包含 full_knowledge_map 和 focused_topic_pack 两种模式
   - 说明全量模式不是一次性生成所有完整卡片，而是先生成完整地图，再按优先级生成

2. 新增 prompts/
   - 01-full-knowledge-map.prompt.md
   - 02-focused-topic-pack.prompt.md
   - 03-context-pack.prompt.md
   - 04-topic-card.prompt.md
   - 05-interview-card.prompt.md
   - 06-quiz-card.prompt.md
   - 07-readiness-report.prompt.md

3. 新增 templates/
   - knowledge-map.md
   - knowledge-map.yaml
   - context-pack.yaml
   - topic-card.md
   - interview-card.md
   - quiz-card.md
   - readiness-report.md
   - print-pack.md

4. 新增 context/context_budget.yaml
   - max_topics_per_batch: 1
   - forbid_raw_jd_in_topic_generation: true
   - P0: full
   - P1: standard
   - P2: brief
   - P3: map_only

5. 更新 router/route_rules.yaml
   - 新增 full_knowledge_map
   - 新增 focused_topic_pack
   - 新增 mixed_interview_pack

6. 新增 scripts/
   - build_knowledge_map.py
   - build_context_pack.py
   - build_topic_cards.py
   - build_print_pack.py
   - build_pdf.py
   - check_context_budget.py

7. 新增 examples/
   - sample-go-backend-jd.md
   - sample-focused-topics.md

8. 新增 tests/
   - 测试 full_knowledge_map 路由
   - 测试 focused_topic_pack 路由
   - 测试 knowledge-map.yaml 生成
   - 测试 context-pack.yaml 包含 selected_topics
   - 测试 max_topics_per_batch 等于 1
   - 测试 P3 不生成完整卡片

设计约束：
- 不做 Web UI
- 不做数据库
- 不做自动爬虫
- 不生成虚假项目经历
- 不一次性生成全部完整八股
- 完整地图可以全量生成
- 完整卡片必须分 topic 生成
- PDF 必须由 Markdown 拼接生成
- 保持当前 Router + Prompt + Template 架构
- 优先保证能跑通、能测试、能打印
```

---

# 19. 最终版 v0.5 一句话

> **v0.5 要做成“双模式面试备考系统”：小白可以先拿完整知识地图，有基础的人可以选择特定知识点深挖；系统最终输出可背诵、可自测、可打印、可复盘的岗位定制面试包。**

这版比单纯 “JD → PDF” 稳。
也比单纯 “Readiness Engine” 更适合小白。
它的核心是：

```text
先给地图
再选重点
分批生成
自测验证
最后打印
```
