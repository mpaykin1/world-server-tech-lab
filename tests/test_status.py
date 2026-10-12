import copy
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from scripts.check_status import validate

ROOT = Path(__file__).resolve().parents[1]

class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime.now(dt.timezone.utc)

    def test_current_checkpoint(self):
        self.assertEqual(validate(now=self.now), [])

    def test_break_missing_history(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "checkpoints").mkdir()
            (root / "LIVE_STATUS.json").write_text((ROOT / "LIVE_STATUS.json").read_text())
            (root / "checkpoints/history.jsonl").write_text("")
            self.assertTrue(validate(root, self.now))

    def test_stale_checkpoint_fails_closed(self):
        future = dt.datetime(2026, 11, 10, tzinfo=dt.timezone.utc)
        self.assertIn("ACTIVE_CHECKPOINT_STALE: older than 14 days", validate(now=future))

if __name__ == "__main__":
    unittest.main()
