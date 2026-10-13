"""Source and artifact safety contract for optional animation V2."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TestAnimationV2(unittest.TestCase):
    def test_module_contract(self):
        source = (ROOT / "scripts/animation-lab-v2.js").read_text(encoding="utf-8")
        self.assertLessEqual(len(source.splitlines()), 400)
        for token in ("formerKnight = drawKnight", "formerTerrain = drawTerrain",
                      "formerObject = objectRender", "v2SmokeWisps",
                      "v2Shimmers", "v2Trees", "prefers-reduced-motion: reduce"):
            self.assertIn(token,source)
        for forbidden in ("requestAnimationFrame(", "setInterval(", "setTimeout(",
                          "new Worker(", "fetch("):
            self.assertNotIn(forbidden,source)
        self.assertIn("MAX_SHIMMERS = 28, MAX_SMOKE = 8, MAX_SWAY = 18",source)
    def test_library_is_not_a_hosted_game(self):
        import json
        data=json.loads((ROOT/"experiments/animation-tech-lab-v2.json").read_text())
        self.assertIsNone(data["user_decision"])
        self.assertEqual(data["status"],"EXPERIMENTING")
        self.assertFalse(data["production_integrated"])
        self.assertIsNone(data["measurement"]["user_visibility_percent"])

if __name__ == "__main__":
    unittest.main()
