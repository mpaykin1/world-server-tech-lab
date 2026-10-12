import ast
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class V6EvidenceTests(unittest.TestCase):
    def test_generator_is_valid_python_without_executing_user_assets(self):
        source=(ROOT/'scripts/terrain_v6_upgrade.py').read_text()
        ast.parse(source)
        self.assertIn("make_atlas(root).save(asset,optimize=True)",source)
        self.assertIn("const variant=n&3",source)
        self.assertIn("'original_engine_preserved':True",source)

    def test_real_pack_browser_evidence_is_not_user_pass(self):
        exp=json.loads((ROOT/'experiments/graphics-terrain-v6.json').read_text())
        evidence=json.loads((ROOT/'evidence/graphics-terrain-v6.json').read_text())
        self.assertIsNone(exp['user_decision'])
        self.assertIsNone(exp['measurement']['user_visibility_percent'])
        self.assertIsNone(evidence['target_similarity_percent'])
        self.assertEqual(evidence['chromium_v6']['loaded'],40)
        self.assertEqual(evidence['chromium_v6']['js_errors'],[])
        self.assertEqual(evidence['atlas_sha256'],
          '933f33c465ca18359a1b62198e9762a1be4c17e6b717f876908d214758b3ff69')
        self.assertEqual(evidence['v6_zip_sha256'],
          'dd011f5b7d0a84c33785c67af2f1e2527efea229188bb69e7fb0696050f944df')
        self.assertLess(evidence['benchmark']['v6_desktop_mean_render_ms'],
                        evidence['benchmark']['v5_desktop_mean_render_ms'])
        self.assertTrue(exp['integration']['world_server_runtime_changed'] is False)

if __name__=='__main__':
    unittest.main()
