# Direct Prompt B Demo

这是用Prompt B直接生成的PDF样例。

## 用途
- 展示面试手册的内容形态
- 作为回归对比基准

## 状态
⚠️ 这**不代表** repo E2E流程跑通。

## 已知问题
1. 未经过 context_pack / state / topic_backlog 流程
2. 项目故事无证据锚点（包含"我之前做过"的虚假表述）
3. PDF排版存在 bullet/table/code block 瑕疵
4. 部分技术表述过满（如"支撑千万级"、"快百倍"）
5. slice扩容策略同一张卡内版本不一致

## 改进方向
- 下一版必须走标准pipeline（run_jd_to_handbook.py）
- 禁止无证据的项目故事
- 技术表述加限定词
- 排版走Typst或优化weasyprint CSS
