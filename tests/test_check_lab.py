import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_lab import check_experiment, validate  # noqa: E402


class LabContractTests(unittest.TestCase):
    def setUp(self):
        import json
        self.record = json.loads((ROOT / "experiments/TEMPLATE.json").read_text(encoding="utf-8"))

    def test_structure(self):
        self.assertEqual(validate(), [])

    def test_no_decision_before_user(self):
        record = copy.deepcopy(self.record)
        record["status"] = "USER_PASS"
        self.assertTrue(check_experiment(record))

    def test_success_requires_user_evidence(self):
        record = copy.deepcopy(self.record)
        record["status"] = "USER_PASS"
        record["user_decision"] = "PASS"
        self.assertTrue(check_experiment(record))
        record["user_decision_source"] = "user message id"
        self.assertFalse(check_experiment(record))

    def test_visibility_gate(self):
        record = copy.deepcopy(self.record)
        record["status"] = "READY_FOR_USER"
        record["measurement"]["user_visibility_percent"] = 85
        self.assertTrue(check_experiment(record))
        record["measurement"]["user_visibility_percent"] = 86
        record["measurement"]["visibility_evidence"] = "evidence/score.json"
        record["measurement"]["reproducible_test_command"] = "python test.py"
        self.assertFalse(check_experiment(record))

    def test_analysis_requires_verdict(self):
        record = copy.deepcopy(self.record)
        record["analysis_commit"] = "sha"
        self.assertTrue(check_experiment(record))


if __name__ == "__main__":
    unittest.main()
