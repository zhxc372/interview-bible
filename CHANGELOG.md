# Interview Bible - 版本历史与路线图

> 最后更新：2026-05-10

---

## 版本路线图

| 版本 | 目标 | 状态 |
|------|------|------|
| v0.1 | MVP骨架：Router + 知识卡 + 项目卡 + 压力追问 | ✅ 完成 |
| v0.2 | 双卡结构：知识点卡(搞清楚) + 面试卡(讲清楚) | ✅ 完成 |
| v0.3 | JD Intake：输入JD，生成备考地图 | 🔨 进行中 |
| v0.4 | Card Queue：根据Backlog批量生成卡片队列 | 🔜 下一步 |
| v0.5 | Mock Interview：模拟面试状态机 | 🔜 |
| v0.6 | Export Pack：Markdown/HTML/PDF导出 | 🔜 |
| v0.7 | Evidence Binder：项目证据管理 | 🔜 |

---

## v0.1 - MVP骨架 (2026-05-10)

- Router路由器 + 5种拦截规则
- 面试知识卡 Prompt
- 项目表达卡 Prompt
- 压力追问 Prompt
- 8个单元测试

## v0.2 - 双卡结构 (2026-05-10)

核心变更：知识卡拆成两层
- **知识点卡**：搞清楚（5W1H 9问 + Node Fingerprint 9问 + 最小验证）
- **面试卡**：讲清楚（30秒版 + 2分钟版 + Trade-off + 易混边界 + 压力追问）
- 闭环：搞清楚 → 讲清楚 → 被追问 → 暴露漏洞 → 再搞清楚
- Router新增subtype: knowledge_point_card / interview_card
- 13个单元测试

## v0.3 - JD Intake (进行中)

新增JD入口，输出备考地图。
详见 `PRD-v0.3.md`。
