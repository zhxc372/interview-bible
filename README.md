# Interview Bible

> 岗位面试材料编译器 | [GitHub](https://github.com/zhxc372/interview-bible) | [Releases](https://github.com/zhxc372/interview-bible/releases)

**两条产品线：**

| 产品线 | 解决的问题 | 受众 |
|--------|-----------|------|
| **学习路线**（Prompt A） | 看到JD后该学什么 | 小白/转岗/零基础 |
| **面试手册**（Prompt B） | 拿到JD后怎么准备面试 | 有基础/有面试机会 |

当前聚焦：**面试手册（Prompt B）**

---

## 项目宪法

本项目受 [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md) 最高约束。

核心使命：**帮用户把真实能力转化为可验证、可口述、可追问的面试表达。**

所有工作流必须遵守 [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md) 和 [DECISION_RIGHTS.md](DECISION_RIGHTS.md)。
任何违反宪法的行为（无证据生成项目卡、绕过流水线直接生成PDF、包装个人demo为生产项目）都会被blocker拦截。

---

## 核心闭环

```text
JD输入
  → Router路由
  → JD Intake（分析JD，生成考点地图）
  → Context Pack（压缩JD，后续不用原始JD）
  → Topic Backlog（P0/P1/P2/P3优先级）
  → 逐Topic生成卡片
  → Validate（校验产物完整性）
  → Markdown Pack（拼接完整手册）
  → PDF（可打印）
```

**硬约束：PDF只能从标准session产物生成，Agent不能绕过流水线。**

---

## 卡片类型

| 卡片 | 目标 | 什么时候用 |
|------|------|-----------|
| 面试卡 | 讲清楚 | 每个P0/P1考点 |
| 知识点卡 | 搞清楚 | 面试卡生成前的理解铺垫 |
| 自测卡 | 验证 | 检查掌握程度 |
| 项目卡 | 项目表达 | 有真实项目时 |

---

## 目录结构

```text
interview-bible/
├── SKILL.md                    # OpenClaw Skill入口
├── VERSION                     # 当前版本
├── CHANGELOG.md                # 版本历史
├── contracts/
│   └── handbook_artifact_contract.yaml  # 产物契约
├── router/
│   ├── router.py               # 路由器
│   ├── route_rules.yaml        # 路由规则
│   └── tests/test_router.py    # Router测试（29个）
├── scripts/
│   ├── tests/test_pipeline.py   # Pipeline E2E测试（7个）
├── prompts/                    # 8个Prompt（00-07）
│   ├── 00-mode-router.prompt.md
│   ├── 01-full-knowledge-map.prompt.md
│   ├── 02-focused-topic-pack.prompt.md
│   ├── 03-knowledge-point-card.prompt.md
│   ├── 04-interview-card.prompt.md
│   ├── 05-project-card.prompt.md
│   ├── 06-pressure-q.prompt.md
│   └── 07-quiz-card.prompt.md
├── scripts/
│   ├── run_jd_to_handbook.py   # 总控脚本
│   ├── validate_handbook.py    # 产物校验
│   ├── build-book.py           # Markdown书籍生成
│   ├── build-pdf-v2.py         # weasyprint PDF生成
│   ├── build_context_pack.py
│   ├── build_markdown_pack.py
│   └── check_context_budget.py
├── templates/                  # 输出模板
├── legacy/                     # 已废弃的文件
├── examples/
│   ├── reference/              # 参考样例
│   ├── sample-go-backend-jd.md
│   └── sample-focused-topics.md
├── docs/prd/                   # PRD文档
│   ├── PRD-v0.6.md
│   ├── Prompt-A-B-jd-learning-and-interview.md
│   └── PRODUCT-DEFINITION.md
└── exports/                    # 运行时输出（git-ignored）
```

---

## 快速使用

> ⚠️ **本流程不是一键自动化。** Agent 负责生成内容（JD分析、卡片生成），scripts 负责初始化、校验、拼接、导出。build_context_pack.py 当前由 Agent 在 session 中填充，不是脚本自动生成。

```bash
# 1. 初始化session（创建目录结构）
python3 scripts/run_jd_to_handbook.py --jd examples/sample-go-backend-jd.md --session my-interview --mode interview

# 2. Agent执行JD Intake → 手动填充context_pack.yaml + topic_backlog.yaml
#    （当前阶段：Agent生成内容，人工确认后写入）

# 3. Agent逐个生成卡片到 cards/ 目录

# 4. 校验产物（Level 3: 自动校验脚本）
python3 scripts/validate_handbook.py --session my-interview

# 5. 生成Markdown（Level 3: 自动拼接脚本）
python3 scripts/build-book.py --session my-interview

# 6. 生成PDF（只能从通过validate的标准session生成）
python3 scripts/build-pdf-v2.py --session my-interview
```

---

## 跑测试

```bash
# Router测试
python3 -m unittest router.tests.test_router -v

# Pipeline E2E测试
python3 scripts/tests/test_pipeline.py -v

# 总计：36个测试（29 Router + 7 Pipeline）
```

---

## 核心铁律

```text
1. 面试要证据。无证据不生成项目卡。
2. PDF只能从标准session产物生成，build-pdf-v2默认强制校验。
3. Agent不能绕过流水线——工程上不可绕过（测试保证）。
4. 项目故事不能编。没有真实项目就用"理论推演"。
5. 搞清楚 → 讲清楚 → 验证清楚。
```

**以上铁律来源于 [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md)。宪法是最高约束，任何prompt/route/export不能违反。**

---

## v0.6.x 冻结范围

v0.6.x 只做 **Skill + CLI Artifact Compiler**：

- ✅ Router、Prompt、Template
- ✅ Artifact Contract、Validate
- ✅ Markdown/PDF Export

不做：
- ❌ Web UI
- ❌ 账户系统
- ❌ 在线模拟面试
- ❌ 简历优化平台
- ❌ 题库平台

---

## 支持等级

| 能力 | 等级 | 说明 |
|------|------|------|
| Router关键词路由 | Level 4 | 有单元测试（29个） |
| Pipeline E2E | Level 4 | 有端到端测试（7个） |
| 项目卡证据闸门 | Level 4 | Router硬拦截+测试 |
| PDF导出 | Level 3 | 有脚本，需手动跑 |
| Markdown书籍生成 | Level 3 | 有脚本，需手动跑 |
| JD Intake | Level 2 | Agent生成+人工确认 |
| Context Pack | Level 2 | Agent填充，非自动 |
| 卡片生成 | Level 1 | Agent对话式，无自动化 |

**等级定义：**
- Level 0: 文档建议
- Level 1: 可手动复制使用
- Level 2: 有入口文件/适配文件
- Level 3: 有自动校验脚本
- Level 4: 有真实端到端测试
- Level 5: 有release包+安装命令+回归测试

---

## 版本历史

| 版本 | 说明 |
|------|------|
| v0.1 | MVP骨架：Router + 知识卡 + 项目卡 |
| v0.2 | 双卡结构：知识点卡 + 面试卡 |
| v0.3 | JD Intake：输入JD生成备考地图 |
| v0.4 | Context Pack + State Persistence |
| v0.5 | 双模式 + Quiz Card + 用户画像 |
| v0.5.1 | 用户画像层（应届/初级/转岗/自定义） |
| v0.6 | weasyprint PDF导出 + 书籍排版 |
| **v0.6.1** | **流程硬化：Artifact Contract + Validate + 总控脚本** |
| **v0.6.2** | **工程硬化：PDF强制校验 + backlog驱动 + E2E测试（36个）** |
