# Decision Rights

> 本文件定义 AI、人类、脚本在 Interview Bible 项目中的权力边界。

---

## AI May

- extract JD requirements（JD 解构）
- generate knowledge point candidates（知识点候选）
- draft cards（草拟卡片）
- expose weak evidence（暴露弱证据）
- ask pressure questions（压力追问）
- propose wording variants（措辞建议）
- generate print/export artifacts from completed sessions（从完成 session 生成导出）
- propose rule modifications（提出规则修改建议）
- generate test case candidates（生成测试用例候选）

## AI Must Not

- invent experience（编造经历）
- upgrade weak evidence into strong claims（升级弱证据为强主张）
- bypass router blockers（绕过路由拦截）
- generate project cards without evidence（无证据生成项目卡）
- create PDF directly from vague input（从模糊输入直接生成 PDF）
- modify core rules without human review（未经审查修改核心规则）
- approve its own changes（自我批准）
- modify this constitution without human review（未经审查修改宪法）
- delete or relax constraints（删除或放宽约束）
- hide uncertainty to appear complete（隐藏不确定性以显得完整）

## Human Must Decide

- whether the JD target is correct（JD 方向是否正确）
- whether evidence is real（证据是否真实）
- whether a claim is acceptable（主张是否可接受）
- which knowledge points are P0/P1/P2（优先级）
- whether a card is ready for export（卡片是否可导出）
- whether a roadmap item enters MVP（路线图是否进入主线）
- rule changes（核心规则变更）
- constitution changes（宪法变更）

## Scripts Should Decide

- whether session state is complete（session 是否完整）
- whether required files exist（必需文件是否存在）
- whether PDF export preconditions are met（PDF 导出前提是否满足）
- whether router tests pass（路由测试是否通过）
- whether pipeline E2E tests pass（端到端测试是否通过）
- format validation（格式校验）

## Skill Should Decide

- when to trigger（何时触发）
- what context to read（读取什么上下文）
- what format to output（输出什么格式）
- when to stop（何时停止）
- what must be delegated to human（什么必须交给人类）
- what must be delegated to scripts（什么必须交给脚本）
