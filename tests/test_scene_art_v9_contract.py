"""V9 scene-art regression guards; no paid APIs or new engine."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from scripts.rebuild_v9_scene import rebuild, BASE_SHA256, MAP_SHA256, HOUSE_SHA256

ROOT=Path(__file__).resolve().parents[1]

class SceneV9Contract(unittest.TestCase):
    def test_pinned_sources_are_cryptographic_not_labels(self):
        for value in (BASE_SHA256, MAP_SHA256, HOUSE_SHA256):
            self.assertEqual(len(value),64)
            int(value,16)

    def test_wrong_baseline_fails_closed_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            src=Path(directory)/"not-the-baseline.zip"
            dst=Path(directory)/"out.zip"
            src.write_bytes(b"not a ZIP")
            with self.assertRaisesRegex(ValueError,"Wrong V9 animation baseline ZIP"):
                rebuild(src,dst)
            self.assertFalse(dst.exists())

    def test_shoreline_adapter_is_bounded_and_layer_preserving(self):
        js=(ROOT/"scripts/water-light-v9.js").read_text(encoding="utf-8")
        self.assertIn("const TILE_COUNT_BUDGET=900",js)
        self.assertIn("previousTerrain(camX,camY,bounds)",js)
        self.assertIn("drawTerrain=function v9WaterTerrain",js)
        self.assertIn("window.__graphicsDemoMetrics.animatedRipplesV9",js)
        for banned in ("requestAnimationFrame(", "setInterval(", "new Worker(", "fetch("):
            self.assertNotIn(banned,js)

if __name__=="__main__": unittest.main()
