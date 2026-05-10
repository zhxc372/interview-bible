# Interview Bible Roadmap

> 当前冻结版本：v0.6.2
> 当前阶段：Pipeline MVP 已完成
> 核心定位：JD 驱动的面试手册生成流水线
>
> ⚠️ 路线图受 PROJECT_CONSTITUTION.md 约束。所有新功能必须通过宪法准入检查。
> 不服务核心使命的功能进入 parking-lot，不进主线。

---

## 项目长期目标

做一个 **JD驱动的技术面试准备系统**，解决两个核心场景：

| 场景 | 问题 | 产品线 |
|------|------|--------|
| 我想做这个岗位 | 看到JD后不知道该学什么 | Prompt A：学习路线 |
| 我要面试这个岗位 | 拿到JD后不知道怎么准备 | Prompt B：面试手册 |

---

## 版本路线

```
v0.6.2  冻结流水线                    ✅ 完成
v0.7    Human Decision Gates           🔜
v0.8    Evidence Ledger                🔜
v0.9    Review Mode + 真实JD打样       🔜
v0.10   渲染器泛化 + Prompt A/B        🔜
v0.11   CLI + Typst排版引擎            🔜
v1.0    稳定发布                       🔜
```

---

## v0.7：Human Decision Gates

### 目标
在关键节点增加明确的人类审批闸门。

### 任务
1. JD approval gate（JD确认后再继续）
2. Evidence approval gate（证据确认后再生成卡片）
3. Claim strength gate（表达强度确认）
4. Export approval gate（导出前确认）
5. Session readiness check（session完整性校验强化）

### 验收标准
- [ ] 每个gate有明确的blocker行为
- [ ] 无gate pass不能进入下一阶段
- [ ] blocker消息清晰告知人类需要做什么

---

## v0.8：Evidence Ledger

### 目标
跨卡片追踪证据锚点，防止AI自动升级项目经历。

### 任务
1. evidence_id + evidence_type + claim_supported + claim_strength
2. missing_evidence 自动警告
3. Claim Strength Level 分级（L0无证据→L4生产主导）
4. 没有 evidence 不允许输出 L3/L4 表达

### 验收标准
- [ ] 每个claim关联到evidence_id
- [ ] 无evidence的claim被自动降级
- [ ] evidence_gap_list 自动生成

---

## v0.9：Review Mode + 真实JD打样

### 目标
让 AI review 已有卡片而非无限生成新内容；用真实JD测试输出质量。

### 任务
1. Review Mode：空泛短语检测、假自信检测、过度主张检测、缺失trade-off检测
2. 收集5类JD样例（Go后端/Java后端/前端/测开/AI工程）
3. 每类JD跑一次完整流程
4. 渲染器泛化：按topic.category自动分篇

### 验收标准
- [ ] Review Mode可检测至少4类问题
- [ ] 至少5个真实JD样例跑通
- [ ] 每个样例有完整Markdown和PDF

---

## v0.7：真实JD打样与渲染器泛化

### 目标
用真实JD测试输出质量，渲染器改为通用。

### 任务
1. 收集5类JD样例（Go后端/Java后端/前端/测开/AI工程）
2. 每类JD跑一次完整流程，输出Markdown + PDF
3. 渲染器泛化：按topic.category自动分篇，不硬编码
4. 每个样例输出quality_report.md

### 验收标准
- [ ] 至少5个真实JD样例跑通
- [ ] 每个样例有完整Markdown和PDF
- [ ] 渲染器不再硬编码具体技术栈
- [ ] 每个样例有quality_report.md
- [ ] PDF版式无孤立bullet/表格挤压/章节断裂

---

## v0.8：Prompt A/B 双入口产品化

### 目标
两个入口正式产品化，Router能区分学习路线和面试手册。

### 验收标准
- [ ] Router区分学习路线模式和面试手册模式
- [ ] 两种模式有独立artifact contract
- [ ] 两种模式有独立markdown/pdf输出
- [ ] 同一个JD可选择生成学习路线或面试手册

---

## v0.9：交互体验与自动化

### 任务
1. CLI统一入口（init/build/validate/pdf）
2. 配置文件（interview-bible.config.yaml）
3. 更稳定的PDF引擎（评估Typst）

### 多平台适配

| 平台 | 适配方式 | 优先级 |
|------|---------|--------
| OpenClaw | ✅ 已适配（SKILL.md + Router） | 当前 |
| 任意LLM（ChatGPT/Claude/Gemini） | 复制Prompt B直接使用 | v0.8 |
| OpenCode | 转换skill格式 | v0.9 |
| Cursor/Claude Code | 写入.cursorrules/CLAUDE.md | v0.9 |

---

## v1.0：稳定产品版本

### 必须具备
1. 双入口（学习路线 / 面试手册）
2. 真实JD样例库
3. 稳定artifact contract + validator
4. 稳定PDF输出
5. 清晰README + 使用文档
6. 可复现demo
7. CI测试 + Release包

---

## 新功能准入检查

| 问题 | 要求 |
|---|---|
| 是否服务核心使命？ | 必须是 |
| 是否有重复使用价值？ | 必须是 |
| 是否有明确输入输出？ | 必须是 |
| 是否有验收标准？ | 必须是 |
| 是否可以被测试？ | 最好是 |
| 是否会扩大 AI 自由度？ | 必须评估 |
| 是否会削弱人类决策权？ | 禁止 |
| 是否会让项目变成万能平台？ | 禁止 |

任何不能通过检查的新功能，进入 `parking-lot.md`，不得进入主线 Roadmap。

---

## Parking Lot（暂不纳入主线）

1. 完整模拟面试平台
2. 简历优化器
3. 长期记忆系统
4. 自动扫描代码仓库生成项目经历
5. 自动生成大型八股题库
6. AI 自动修改 Skill 规则并自我合并
7. UI / 数据库 / SaaS 化

---

## 不做什么

1. 不做在线SaaS
2. 不做用户系统
3. 不做大而全题库
4. 不做爬虫自动抓JD
5. 不做简历造假辅助
6. 不做无证据项目经历生成
7. 不做所有语言所有岗位全覆盖
8. 不追求一次生成完美手册
9. 不让导出流程绕过核心 session
10. 不让AI自动修改并合并核心规则

当前重点：**固定流程 + AI 扩展 + 人类裁决 + 证据约束 + 可验证导出**
