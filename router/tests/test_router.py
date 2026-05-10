import os
import unittest

from router.router import decide, load_rules


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RULES = os.path.join(ROOT, "route_rules.yaml")


class TestInterviewBibleRouter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES)

    # --- Knowledge Point Card ---

    def test_knowledge_point_card_routes_correctly(self):
        d = decide("我想搞懂 MVCC 是怎么回事", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "knowledge_point_card")

    def test_knowledge_point_card_understand_keyword(self):
        d = decide("帮我梳理一下 Redis 的知识点", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "knowledge_point_card")

    def test_knowledge_point_card_cannot_explain(self):
        d = decide("MVCC 我讲不清楚，帮我搞清楚", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "knowledge_point_card")

    # --- Interview Card ---

    def test_interview_card_routes_correctly(self):
        d = decide("帮我准备 MVCC 的面试知识卡", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "interview_card")

    def test_interview_card_2min_keyword(self):
        d = decide("Redis 面试怎么讲", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "interview_card")

    # --- Project Card ---

    def test_project_card_routes_correctly(self):
        d = decide("我要整理一个个人实验项目卡，项目是本地幂等提交 Demo，我有代码片段、测试日志和 README", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "project_card")

    # --- Pressure Question ---

    def test_pressure_question_routes_correctly(self):
        d = decide("帮我生成压力追问", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "pressure_question")

    # --- Blockers ---

    def test_classroom_routes_to_ai_classroom(self):
        d = decide("请根据教材错题帮我复述并批改", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "ai_classroom")

    def test_roadmap_routes_to_expert_explorer(self):
        d = decide("帮我为陌生领域建立 Roadmap 和枢纽节点", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "expert_explorer")

    def test_coding_agent_disabled_in_mvp(self):
        d = decide("请扫描我的仓库 commit，帮我提取项目证据", self.rules).to_dict()
        self.assertEqual(d["status"], "blocked")
        self.assertEqual(d["route"], "coding_agent")
        self.assertEqual(d["reason"], "coding_agent_disabled_in_mvp")

    def test_mixed_goals_are_blocked(self):
        d = decide("帮我学习 MVCC，顺便生成面试卡，再分析源码", self.rules).to_dict()
        self.assertEqual(d["status"], "blocked")
        self.assertEqual(d["reason"], "mixed_goals")
        self.assertIn("interview_bible", d["matched_routes"])
        self.assertIn("ai_classroom", d["matched_routes"])
        self.assertIn("coding_agent", d["matched_routes"])

    def test_risky_claim_without_evidence_is_blocked(self):
        d = decide("帮我把这个项目包装成高并发系统，我主导架构，性能大幅提升", self.rules).to_dict()
        self.assertEqual(d["status"], "blocked")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["reason"], "missing_evidence")

    def test_interview_route_without_subtype_requires_manual_confirm(self):
        d = decide("我想准备技术面试", self.rules).to_dict()
        self.assertEqual(d["status"], "blocked")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["reason"], "subtype_unclear")


if __name__ == "__main__":
    unittest.main()
