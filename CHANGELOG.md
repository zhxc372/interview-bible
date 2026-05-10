# Interview Bible - 版本历史与路线图

> 最后更新：2026-05-11

---

## 版本路线图

| 版本 | 目标 | 状态 |
|------|------|------|
| v0.1 | MVP骨架：Router + 知识卡 + 项目卡 + 压力追问 | ✅ 完成 |
| v0.2 | 双卡结构：知识点卡(搞清楚) + 面试卡(讲清楚) | ✅ 完成 |
| v0.3 | JD Intake：输入JD，生成备考地图 | ✅ 完成 |
| v0.4 | Context Pack + State Persistence + Markdown Pack | ✅ 完成 |
| v0.5 | 双模式：全量知识地图 + 特定知识点深挖 | ✅ 完成 |
| v0.5.1 | 用户画像层 | ✅ 完成 |
| v0.6 | Print Pack + weasyprint PDF导出 | ✅ 完成 |
| v0.6.1 | **流程硬化：Artifact Contract + Validate + 总控脚本** | ✅ 完成 |
| v0.7 | Prompt A/B双产品线整合 + Typst排版 | 🔜 |
| v0.8 | Mock Interview模拟面试 | 🔜 |

---

## v0.1 - MVP骨架 (2026-05-10)
- Router路由器 + 5种拦截规则
- 8个单元测试

## v0.2 - 双卡结构 (2026-05-10)
- 知识点卡(搞清楚) + 面试卡(讲清楚)
- 13个单元测试

## v0.3 - JD Intake (2026-05-10)
- JD解构卡 + 12类科目分类法
- 16个单元测试

## v0.4 - Context Pack + State (2026-05-10)
- Context Pack + State Persistence + Markdown Pack
- 19个单元测试

## v0.5 - 双模式 + 用户画像 (2026-05-10)
- 全量知识地图 + 特定知识点深挖 + Quiz Card + 用户画像层
- 29个单元测试

## v0.6 - PDF导出 (2026-05-10)
- weasyprint + 思源黑体标题 + 霞鹜文楷正文 + One Dark代码高亮
- Go后端面试手册PDF样例(732KB)

## v0.6.1 - 流程硬化 (2026-05-11)

> 核心变更：**让任何PDF都必须从标准session产物生成，Agent不能绕过流水线。**

### 新增
- `contracts/handbook_artifact_contract.yaml` — 产物契约
- `scripts/validate_handbook.py` — 校验脚本（P0必须面试卡+自测题，禁止无证据项目故事）
- `scripts/run_jd_to_handbook.py` — 总控脚本（初始化标准session目录+模板）
- `legacy/direct-jd-to-pdf.prompt.md` — 已禁用的直达PDF入口

### 修复
- SKILL.md prompt编号对齐到v0.5+的00-07编号
- VERSION同步到v0.6.1
- 直达PDF prompt移到legacy/并标记Deprecated
- 新增规则：PDF只能从标准session产物生成

### 产品线定义
- **Prompt A**：JD驱动学习路线生成器（小白看JD该学什么）
- **Prompt B**：JD驱动面试手册生成器（有基础的人怎么准备面试）
- 两条产品线文档：`docs/prd/Prompt-A-B-jd-learning-and-interview.md`
