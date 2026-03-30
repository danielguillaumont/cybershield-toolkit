from __future__ import annotations

import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cybershield.password_audit import audit_password


class TestPasswordAudit(unittest.TestCase):
    def test_empty_password_is_very_weak(self) -> None:
        result = audit_password("")
        self.assertEqual(result["rating"], "Very Weak")
        self.assertEqual(result["score"], 0)

    def test_common_password_scores_low(self) -> None:
        result = audit_password("password123")
        self.assertLess(result["score"], 40)
        self.assertIn(result["rating"], {"Very Weak", "Weak"})

    def test_strong_password_scores_higher(self) -> None:
        result = audit_password("Ultra$SecurePass2026!")
        self.assertGreaterEqual(result["score"], 85)
        self.assertEqual(result["rating"], "Strong")


if __name__ == "__main__":
    unittest.main()
