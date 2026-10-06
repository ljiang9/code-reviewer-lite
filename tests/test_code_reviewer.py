import unittest

from code_reviewer import review

GOOD = """
def add(a, b):
    return a + b

result = add(1, 2)
"""

BAD = """
import os
eval(user_input)
os.system("rm -rf /")
# TODO: 以后处理
def q(x):
    return x
"""


class TestReviewer(unittest.TestCase):
    def test_good_no_issues(self):
        self.assertEqual(review(GOOD), [])

    def test_eval_flagged(self):
        issues = review(BAD)
        self.assertTrue(any(i["message"].startswith("使用了裸 eval") for i in issues))

    def test_os_system_flagged(self):
        issues = review(BAD)
        self.assertTrue(any("os.system" in i["message"] for i in issues))

    def test_todo_flagged(self):
        issues = review(BAD)
        self.assertTrue(any("TODO" in i["message"] for i in issues))

    def test_levels(self):
        issues = review(BAD)
        levels = {i["level"] for i in issues}
        self.assertIn("high", levels)

    def test_line_numbers(self):
        issues = review(BAD)
        self.assertTrue(all("line" in i for i in issues))


if __name__ == "__main__":
    unittest.main()
