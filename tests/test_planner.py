import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.core.planner import _local_plan, summarize_plan


class TestPlanner(unittest.TestCase):
    def test_local_plan_has_steps(self):
        plan = _local_plan("write a file then run the tests")
        self.assertIn("steps", plan)
        self.assertTrue(len(plan["steps"]) >= 1)
        self.assertEqual(plan["source"], "local")

    def test_actions_classified(self):
        plan = _local_plan("run the build and then read the log")
        actions = [s["action"] for s in plan["steps"]]
        self.assertIn("shell", actions)

    def test_summarize(self):
        plan = _local_plan("list files")
        out = summarize_plan(plan)
        self.assertIn("Plan for", out)


if __name__ == "__main__":
    unittest.main()
