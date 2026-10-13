import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("blob47",ROOT/"scripts/autotiler_47_index.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class V8LabAcceptance(unittest.TestCase):
    def test_exact_offline_mask_contract(self):
        m=mod.legal_masks()
        self.assertEqual(len(m),47)
        self.assertEqual(len(set(m)),47)
        self.assertEqual(len({mod.to_autotiler(v) for v in m}),47)
        self.assertEqual(mod.to_autotiler(1),1)
        self.assertEqual(mod.to_autotiler(2),4)
        self.assertEqual(mod.to_autotiler(16|1|2),7)
        with self.assertRaises(ValueError):
            mod.to_autotiler(16)

    def test_scope_and_owner_verdict_not_forged(self):
        e=json.loads((ROOT/"experiments/graphics-terrain-v8.json").read_text())
        p=json.loads((ROOT/"evidence/clean-review-v8.json").read_text())
        self.assertEqual(e["status"],"EXPERIMENTING")
        self.assertIsNone(e["user_decision"])
        self.assertIsNone(e["validation"]["user_visibility_percent"])
        self.assertEqual(e["lane_policy"]["GRAPHICS"],50)
        self.assertEqual(e["lane_policy"]["CLEAN_SERVER"],50)
        self.assertEqual(e["lane_policy"]["new_automations"],0)
        self.assertFalse(e["clean_server"]["world_server_master_updated"])
        self.assertEqual(p["status"],"BLOCK_NOT_PASS")
