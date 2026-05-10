import os
import unittest

from router.router import decide, load_rules


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RULES = os.path.join(ROOT, "route_rules.yaml")


class TestInterviewBibleRouter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES)

    # --- Full Knowledge Map ---

    def test_full_knowledge_map_from_scratch(self):
        d = decide("我想从零准备Go后端面试，请生成完整知识点地图", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "full_knowledge_map")

    def test_full_knowledge_map_beginner(self):
        d = decide("我是初学者，帮我生成Go后端的备考地图", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "full_knowledge_map")

    def test_full_knowledge_map_fresh_grad(self):
        d = decide("我是应届生，帮我准备Go后端的完整知识点地图", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "full_knowledge_map")

    def test_full_knowledge_map_career_change(self):
        d = decide("我之前写Java的，现在转Go，帮我从零准备", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "full_knowledge_map")

    def test_full_knowledge_map_full_map(self):
        d = decide("给我全部知识点的完整地图", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "full_knowledge_map")

    # --- Focused Topic Pack ---

    def test_focused_topic_deep_dive(self):
        d = decide("我只想深挖MVCC和Redis缓存一致性", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "focused_topic_pack")

    def test_focused_topic_specific(self):
        d = decide("针对Go context这个知识点专项准备", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "focused_topic_pack")

    def test_focused_topic_sprint(self):
        d = decide("冲刺模式，重点准备P0知识点", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "focused_topic_pack")

    # --- JD Intake ---

    def test_jd_intake_routes_correctly(self):
        d = decide("这是一个Go后端岗位JD，帮我拆解面试准备科目", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "jd_intake")

    def test_jd_intake_job_description_keyword(self):
        d = decide("帮我分析这个岗位要求", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "jd_intake")

    def test_jd_intake_prepare_route_keyword(self):
        d = decide("根据这个招聘要求帮我准备面试准备路线", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "jd_intake")

    # --- Session Resume ---

    def test_session_resume_routes_correctly(self):
        d = decide("继续上次那个面试准备", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "session_resume")

    def test_session_resume_progress_keyword(self):
        d = decide("帮我看看进度", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "session_resume")

    def test_session_resume_next_keyword(self):
        d = decide("下一个知识点", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "session_resume")

    # --- Knowledge Point Card ---

    def test_knowledge_point_card_routes_correctly(self):
        d = decide("我想搞懂 MVCC 是怎么回事", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "knowledge_point_card")

    def test_knowledge_point_card_understand_keyword(self):
        d = decide("帮我梳理一下 Redis 的知识点", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "knowledge_point_card")

    def test_knowledge_point_card_cannot_explain(self):
        d = decide("MVCC 我讲不清楚，帮我搞清楚", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "knowledge_point_card")

    # --- Interview Card ---

    def test_interview_card_routes_correctly(self):
        d = decide("帮我准备 MVCC 的面试知识卡", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "interview_card")

    def test_interview_card_2min_keyword(self):
        d = decide("Redis 面试怎么讲", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "interview_card")

    # --- Project Card ---

    def test_project_card_routes_correctly(self):
        d = decide("我要整理一个个人实验项目卡，项目是本地幂等提交 Demo，我有代码片段、测试日志和 README", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "project_card")

    # --- Quiz Card ---

    def test_quiz_card_routes_correctly(self):
        d = decide("帮我生成MVCC的自测题", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["route"], "interview_bible")
        self.assertEqual(d["subtype"], "quiz_card")

    def test_quiz_card_test_me_keyword(self):
        d = decide("自测一下Go并发模型", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "quiz_card")

    # --- Pressure Question ---

    def test_pressure_question_routes_correctly(self):
        d = decide("帮我生成压力追问", self.rules).to_dict()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["subtype"], "pressure_question")

    # --- Other Routes ---

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
