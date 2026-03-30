from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cybershield.integrity import create_baseline, verify_baseline


class TestIntegrity(unittest.TestCase):
    def test_baseline_detects_modification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            target_file = base / "demo.txt"
            target_file.write_text("version1", encoding="utf-8")

            baseline = create_baseline(base)

            target_file.write_text("version2", encoding="utf-8")
            result = verify_baseline(base, baseline)

            self.assertFalse(result["is_clean"])
            self.assertIn("demo.txt", result["modified_files"])

    def test_baseline_detects_added_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            (base / "a.txt").write_text("a", encoding="utf-8")
            baseline = create_baseline(base)

            (base / "b.txt").write_text("b", encoding="utf-8")
            result = verify_baseline(base, baseline)

            self.assertIn("b.txt", result["added_files"])


if __name__ == "__main__":
    unittest.main()
