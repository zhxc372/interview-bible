# Interview Bible Project Constitution

> AI expands the search space. Human compresses the decision space.  
> Scripts verify the deterministic space. Skills preserve the reusable judgment space.

---

## 0. Mission

Interview Bible exists to help users convert real ability into interview-ready expression.

It does not create fake experience, inflate weak evidence, or replace human judgment.

**Core mission:**

> 帮用户把真实能力转化为可验证、可口述、可追问的面试表达。

**Final output:**

> 可打印、可验证、可口述的面试准备材料。

**This project does not pursue:**

- 万能化（resume beautifier, career planner, mock interview platform）
- 自动替人决策
- 无边界扩展
- 自我批准
- 用 AI 替代证据
- 用生成内容替代验证

---

## 1. Core Loop

The only valid workflow is:

```text
JD Intake
  ↓
JD 解构卡（岗位方向、知识点 Backlog、项目证据映射）
  ↓
知识点卡（搞清楚）
  ↓
面试卡（讲清楚）
  ↓
压力追问（验证清楚）
  ↓
漏洞回填（再搞清楚）
  ↓
Print Pack / PDF（只从完成 session 导出）
```

**No export may bypass the core loop.**

---

## 2. Evidence First

Evidence determines expression level.

- **Strong evidence** → may support strong claims.
- **Weak evidence** → must produce cautious claims.
- **Missing evidence** → must produce honest expression suggestions, never upgraded claims.

Forbidden:

- No evidence → generate deterministic conclusion
- Guess → package as fact
- Complete output by fabricating content
- Smooth expression to mask insufficient evidence

Standard:

```text
无证据 → 标记缺口
证据弱 → 降低结论强度
证据冲突 → 展示冲突
证据不足 → 停止最终判断
```

---

## 3. Human Decision Rights

AI may generate candidates, organize evidence, expose gaps, and propose improvements.

**Human must decide:**

- target role (JD 方向)
- evidence validity（证据是否真实）
- claim strength（表达强度是否可接受）
- final expression（最终措辞）
- whether to export or publish
- Roadmap 是否推进

**AI must not:**

- invent experience
- upgrade weak evidence into strong claims
- bypass router blockers
- generate project cards without evidence
- create PDF directly from vague input
- modify core rules without human review
- approve its own changes

---

## 4. Scope Boundary

This project is not:

- ❌ a resume beautifier
- ❌ a fake project packager
- ❌ a general exam trainer
- ❌ a full mock interview platform
- ❌ a long-term memory system
- ❌ a career planning agent
- ❌ a learning management system

Any function that does not serve the core mission must enter Backlog, not the main workflow.

---

## 5. PDF / Export Policy

PDF is not a generation entry point.

PDF may only be exported from a completed session that has:

- JD 解构完成
- 知识点卡完成
- 面试卡完成
- 压力追问完成
- evidence_gap_list 存在
- readiness check 通过

Directly requesting "generate a PDF" without a complete session must be blocked.

---

## 6. Change Governance

Any change to router rules, prompt rules, card templates, or core files must include:

- **reason**（为什么改）
- **affected workflow**（影响哪个流程）
- **before/after behavior**（改前改后行为）
- **eval case**（测试用例）
- **human review**（人类审查）

AI may propose rule modifications.

AI may not self-approve, self-merge, or modify this constitution without human review.

---

## 7. Skill Discipline

- Skill 只做一件事
- 每个 Skill 有清晰触发条件、边界、输入输出
- 禁止一个 Skill 同时承担过多职责
- 短入口，按需加载重材料
- 确定性任务交给脚本，AI 只做判断力任务

---

## 8. Failure Deposition

Every failure must produce at least one of:

- gotcha entry
- eval case
- rule patch
- checklist item
- script check
- documentation update

---

## Project Motto

> 搞清楚 → 讲清楚 → 验证清楚。  
> 证据决定表达上限。  
> 固定流程 + AI 扩展 + 人类裁决 + 证据约束 + 可验证导出。
