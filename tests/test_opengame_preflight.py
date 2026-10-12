import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.opengame_medieval_preflight import inspect_archive


class PreflightTests(unittest.TestCase):
    def test_invalid_asset_animation_and_tile_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mock.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("world/manifest.json", json.dumps({
                    "map": "map.json", "tileset": {"atlasTiles": {"grass": {}}},
                    "characters": {"hero": {"file": "assets/missing.png"}},
                    "animatedObjects": {"water": {"frames": 1, "file": "assets/water.png"}}
                }))
                z.writestr("world/map.json", json.dumps({
                    "width": 2, "height": 1, "tiles": [["grass", "water"]], "infinite": True
                }))
            result = inspect_archive(path)
            self.assertFalse(result["diagnostic_pass"])
            self.assertEqual(len(result["asset_missing"]), 2)
            self.assertEqual(result["map_unknown_tile_keys"], ["water"])
            self.assertEqual(result["neighbor_transition_edges"], 1)
            self.assertEqual(result["invalid_animation_frame_counts"], ["water"])

    def test_absent_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("test.txt", "empty")
            with self.assertRaises(ValueError):
                inspect_archive(path)


if __name__ == "__main__":
    unittest.main()
