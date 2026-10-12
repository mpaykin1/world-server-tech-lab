import ast
import hashlib
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = "e330b1d476e7ac70923ae02399ac2ffb3dc7852c4abf4e4d5f761f1b6ac64bb4"

class TerrainUpgradeContract(unittest.TestCase):
    def test_real_authored_atlas_and_reproducible_code(self):
        path = ROOT / "artifacts/terrain_transitions_v5.png"
        raw = path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), SHA)
        self.assertTrue(raw.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(struct.unpack(">II", raw[16:24]), (256,48))
        code = (ROOT / "scripts/terrain_v5_upgrade.py").read_text()
        module = ast.parse(code)
        edits = next(ast.literal_eval(node.value) for node in module.body
                     if isinstance(node, ast.Assign)
                     and any(isinstance(t,ast.Name) and t.id=="EDITS" for t in node.targets))
        self.assertEqual(len(edits), 18)
        self.assertTrue(all(a not in ("cliff","water") and b not in ("cliff","water")
                            for x,y,a,b in edits))
        self.assertIn("function drawAuthoredTerrainTransition(", code)
        self.assertIn("atlas().save(output,optimize=True)", code)

    def test_no_unmeasured_visual_success(self):
        exp = json.loads((ROOT/"experiments/graphics-terrain-v5.json").read_text())
        result = json.loads((ROOT/"evidence/graphics-terrain-v5-browser.json").read_text())
        self.assertIsNone(exp["user_decision"])
        self.assertIsNone(exp["measurement"]["user_visibility_percent"])
        self.assertIsNone(result["reference_similarity_percent"])
        self.assertTrue(result["v5"]["authoredTileTransitionsLoaded"])
        self.assertEqual(result["v5"]["js_errors"], [])
        self.assertEqual(result["invariants"]["blocked_tile_mutations"], 0)
        self.assertEqual(result["invariants"]["visible_map_cells_edited"], 18)
        self.assertEqual(exp["measurement"]["atlas_sha256"], SHA)

if __name__=="__main__":
    unittest.main()
