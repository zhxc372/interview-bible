# Interview Bible - 版本历史与路线图

> 最后更新：2026-05-10

---

## 版本路线图

| 版本 | 目标 | 状态 |
|------|------|------|
| v0.1 | MVP骨架：Router + 知识卡 + 项目卡 + 压力追问 | ✅ 完成 |
| v0.2 | 双卡结构：知识点卡(搞清楚) + 面试卡(讲清楚) | ✅ 完成 |
| v0.3 | JD Intake：输入JD，生成备考地图 | ✅ 完成 |
| v0.4 | Context Pack + State Persistence + Markdown Pack | ✅ 完成 |
| v0.5 | 双模式：全量知识地图 + 特定知识点深挖 | ✅ 完成 |
| v0.6 | PDF导出 + Print Pack | 🔜 |
| v0.7 | Mock Interview：模拟面试状态机 | 🔜 |
| v0.8 | Evidence Binder：项目证据管理 | 🔜 |

---

## v0.1 - MVP骨架 (2026-05-10)

- Router路由器 + 5种拦截规则
- 面试知识卡 Prompt
- 项目表达卡 Prompt
- 压力追问 Prompt
- 8个单元测试

## v0.2 - 双卡结构 (2026-05-10)

- 知识点卡(搞清楚) + 面试卡(讲清楚)
- 闭环：搞清楚 → 讲清楚 → 被追问 → 暴露漏洞 → 再搞清楚
- 13个单元测试

## v0.3 - JD Intake (2026-05-10)

- JD解构卡 + 12类科目分类法 + 知识点Backlog
- 16个单元测试

## v0.4 - Context Optimization + State Persistence (2026-05-10)

- Context Pack（编译中间层）
- State Persistence（state.yaml断点恢复）
- Markdown Pack生成器 + Context Budget检查器
- 19个单元测试

## v0.5 - 双模式面试备考系统 (2026-05-10)

- **全量知识地图模式**：小白/转岗/从零开始 → 生成完整岗位知识地图
- **特定知识点深挖模式**：有基础/冲刺/补短板 → 指定知识点生成完整训练包
- **Quiz Card**：自测题 + 评分表 + 错题回填
- Prompt重新编号（8个prompt：00-07）
- Router新增3个subtype：full_knowledge_map / focused_topic_pack / quiz_card
- P0/P1/P2/P3四级优先级
- 示例JD文件 + 示例知识点文件
- 27个单元测试全部通过
