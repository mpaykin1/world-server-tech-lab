import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RecoveryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"catalog/active_capabilities.json").read_text())
        cls.s=json.loads((ROOT/"LIVE_STATUS.json").read_text())
        cls.v8=json.loads((ROOT/"experiments/graphics-terrain-v8.json").read_text())
        cls.v9=json.loads((ROOT/"experiments/graphics-art-v9.json").read_text())
    def test_manifest_bound_to_real_v8(self):
        b=self.r["verified_baseline"]
        self.assertEqual(b["sha256"],self.v8["artifacts"]["sha256"])
        self.assertEqual(b["library_path"],self.v8["artifacts"]["library_path"])
        self.assertEqual(b["library_file_id"],self.v8["artifacts"]["library_file_id"])
        self.assertRegex(b["sha256"],r"^[a-f0-9]{64}$")
        self.assertIn("v8(1).zip",b["library_path"])
        self.assertTrue((ROOT/"scripts/autotiler_47_index.py").is_file())
    def test_every_lab_capability_traversable(self):
        ids=set()
        for c in self.r["implemented"]:
            self.assertNotIn(c["id"],ids)
            ids.add(c["id"])
            self.assertEqual(c["state"],"LAB_VERIFIED")
            self.assertEqual(c["production_status"],"NOT_INTEGRATED")
            for name in ("source","asset","test"):
                link=c[name]
                self.assertIn(link["location"],("github","library_zip"))
                path=link["path"]
                self.assertNotIn("..",Path(path).parts)
                if link["location"]=="github":
                    self.assertTrue((ROOT/path).is_file())
                else:
                    self.assertTrue(path.startswith(self.r["verified_baseline"]["root_directory"]))
            self.assertTrue((ROOT/c["evidence"]).is_file())
            self.assertTrue(c["next"])
        self.assertGreaterEqual(len(ids),5)
    def test_planned_not_falsely_reported_as_implemented(self):
        self.assertEqual(self.v9["status"],"NOT_TESTED")
        self.assertEqual(self.v9["implementation_status"],"NOT_IMPLEMENTED")
        self.assertIsNone(self.v9["user_decision"])
        self.assertIsNone(self.r["owner_decision"])
        self.assertEqual(self.r["production_status"],"NOT_INTEGRATED")
        self.assertTrue(all(x["state"]=="NOT_IMPLEMENTED" for x in self.r["planned_v9"]))
        self.assertEqual(self.s["lane_policy"]["new_scheduled_jobs"],0)
        self.assertEqual((self.s["lane_policy"]["GRAPHICS"],self.s["lane_policy"]["CLEAN_SERVER"]),(50,50))
    def test_recovery_and_entrypoint_references(self):
        for path in ("README.md","AGENTS.md","docs/RECOVERY_ANY_CHAT_RU.md"):
            s=(ROOT/path).read_text()
            self.assertIn("catalog/active_capabilities.json",s)
            self.assertIn("V9_EXECUTION_BRIEF_RU.md",s)
        self.assertIn("AI_START_HERE.md",(ROOT/"docs/RECOVERY_ANY_CHAT_RU.md").read_text())
        self.assertIn("docs/V9_EXECUTION_BRIEF_RU.md",self.s["links"]["v9_execution_brief"])
        self.assertIn("docs/RECOVERY_ANY_CHAT_RU.md",self.s["links"]["any_chat_recovery"])
if __name__=="__main__":
    unittest.main()
