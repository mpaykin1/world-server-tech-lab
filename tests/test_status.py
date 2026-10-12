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
            (root / "LIVE_STATUS.json").write_text(
                (ROOT / "LIVE_STATUS.json").read_text())
            (root / "checkpoints/history.jsonl").write_text("")
            self.assertTrue(validate(root, self.now))

    def test_paused_checkpoint_does_not_expire(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "checkpoints").mkdir()
            (root / "experiments").mkdir()
            status = json.loads((ROOT / "LIVE_STATUS.json").read_text())
            status["phase"] = "PAUSED"
            (root / "LIVE_STATUS.json").write_text(json.dumps(status))
            (root / "checkpoints/history.jsonl").write_text(
                (ROOT / "checkpoints/history.jsonl").read_text())
            for name in status["active_experiments"]:
                source = ROOT / "experiments" / (name + ".json")
                (root / "experiments" / (name + ".json")).write_text(source.read_text())
            self.assertNotIn("ACTIVE_CHECKPOINT_STALE: older than 14 days",
                             validate(root, self.now + dt.timedelta(days=20)))
            status["phase"] = "EXPERIMENTING"
            (root / "LIVE_STATUS.json").write_text(json.dumps(status))
            self.assertIn("ACTIVE_CHECKPOINT_STALE: older than 14 days",
                          validate(root, self.now + dt.timedelta(days=20)))


if __name__ == "__main__":
    unittest.main()
