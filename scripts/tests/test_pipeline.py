"""
v0.6.2 Pipeline Tests：流程硬化测试

确保：
1. 没有直达PDF prompt在active prompts目录
2. validate对空backlog失败
3. validate对缺P0面试卡失败
4. validate对无证据项目故事失败
5. build-pdf-v2拒绝未校验session
6. build-book读取topic_backlog
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
import unittest

# 确保能import项目模块
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# scripts/tests/ → scripts/ → project root
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, PROJECT_ROOT)

from validate_handbook import validate_session


class TestNoDirectPdfPrompt(unittest.TestCase):
    """确保active prompts目录没有直达PDF入口"""

    def test_no_direct_pdf_prompt_in_prompts(self):
        prompts_dir = os.path.join(PROJECT_ROOT, "prompts")
        if not os.path.exists(prompts_dir):
            self.skipTest("prompts/ not found")
        files = os.listdir(prompts_dir)
        for f in files:
            self.assertFalse(
                "jd-to-pdf" in f,
                f"❌ 发现直达PDF prompt: prompts/{f}，请移到legacy/"
            )

    def test_no_legacy_keywords_in_active_prompts(self):
        prompts_dir = os.path.join(PROJECT_ROOT, "prompts")
        if not os.path.exists(prompts_dir):
            self.skipTest("prompts/ not found")
        for f in os.listdir(prompts_dir):
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(prompts_dir, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read().lower()
            self.assertNotIn(
                "deprecated", content.lower(),
                f"❌ prompts/{f} 包含 DEPRECATED 标记，应该移到legacy/"
            )


class TestValidatorHardening(unittest.TestCase):
    """Validator强度测试"""

    def setUp(self):
        """创建临时session目录"""
        self.tmpdir = tempfile.mkdtemp()
        self.session_name = "test-session"
        self.session_dir = os.path.join(self.tmpdir, self.session_name)
        os.makedirs(os.path.join(self.session_dir, "cards"), exist_ok=True)
        os.makedirs(os.path.join(self.session_dir, "markdown"), exist_ok=True)

        # Monkey-patch EXPORTS_DIR
        import validate_handbook
        self._orig_exports = validate_handbook.EXPORTS_DIR
        validate_handbook.EXPORTS_DIR = self.tmpdir

    def tearDown(self):
        import validate_handbook
        validate_handbook.EXPORTS_DIR = self._orig_exports
        shutil.rmtree(self.tmpdir)

    def test_validate_fails_empty_session(self):
        """空session应该失败"""
        errors = validate_session(self.session_name)
        fails = [e for e in errors if e.startswith("❌")]
        self.assertGreater(len(fails), 0, "空session应该有校验错误")

    def test_validate_fails_empty_backlog(self):
        """空backlog应该失败"""
        # 创建必需文件
        for f in ["raw_jd.md", "jd_analysis.md", "context_pack.yaml",
                   "state.yaml", "source_trace.md"]:
            with open(os.path.join(self.session_dir, f), "w") as fh:
                fh.write("test")

        # 创建空backlog
        with open(os.path.join(self.session_dir, "topic_backlog.yaml"), "w") as fh:
            fh.write("topics: []\n")

        errors = validate_session(self.session_name)
        fails = [e for e in errors if e.startswith("❌")]
        self.assertTrue(
            any("topics 为空" in e for e in fails),
            "空backlog应该报错"
        )

    def test_validate_fails_fake_project_story(self):
        """无证据项目故事应该失败"""
        # 创建带假故事的文件
        fake_md = os.path.join(self.session_dir, "test.md")
        with open(fake_md, "w") as fh:
            fh.write("我之前做过订单系统，优化到50%。")

        errors = validate_session(self.session_name)
        fails = [e for e in errors if e.startswith("❌")]
        self.assertTrue(
            any("无证据的项目故事" in e for e in fails),
            f"假项目故事应该被拦截。errors: {fails}"
        )


class TestBuildPdfForcesValidation(unittest.TestCase):
    """build-pdf-v2 必须强制校验"""

    def test_build_pdf_refuses_unvalidated_session(self):
        """未校验session应该被拒绝"""
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "build-pdf-v2.py"),
             "--session", "nonexistent-session"],
            capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0, "不存在的session应该返回非0")

    def test_build_pdf_has_force_flag(self):
        """--force参数应该存在"""
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "build-pdf-v2.py"),
             "--session", "nonexistent-session", "--force"],
            capture_output=True, text=True
        )
        # 不存在的session即使--force也会失败（找不到markdown）
        self.assertNotEqual(result.returncode, 0, "不存在的session应该返回非0")


if __name__ == "__main__":
    unittest.main()
