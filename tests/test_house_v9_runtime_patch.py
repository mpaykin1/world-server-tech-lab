"""Deterministic negative tests of the V9 original renderer patch."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.house_runtime_patch_v9 import patch, OLD, NEW

class RuntimePatchTests(unittest.TestCase):
    def test_exact_original_patch_and_fail_closed_second_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'graphics-enhancement.js'
            path.write_text("const keep = 1;\n"*5 + OLD)
            patch(path)
            self.assertIn(NEW, path.read_text())
            first = path.read_bytes()
            with self.assertRaises(ValueError):
                patch(path)
            self.assertEqual(path.read_bytes(), first)

    def test_missing_or_duplicate_callsite_never_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'graphics-enhancement.js'
            for source in ('nothing', OLD + '\n' + OLD):
                path.write_text(source)
                with self.assertRaises(ValueError):
                    patch(path)
                self.assertEqual(path.read_text(), source)

    def test_pinned_binary_asset_and_browser_metrics_are_not_user_verdict(self):
        root = Path(__file__).resolve().parents[1]
        sprite = root / 'assets/graphics-v9/house_3d.png'
        self.assertEqual(hashlib.sha256(sprite.read_bytes()).hexdigest(),
                         'b874e392d20e6c798c60066c2ae93a165a62908caa1dfdbc275f0a29ace584c7')
        evidence = json.loads((root/'experiments/graphics-art-v9-browser.json').read_text())
        self.assertTrue(all(not run['js_errors'] and run['loaded'] == run['total'] == 44 for run in evidence['runs']))
        self.assertIsNone(evidence['visibility_score'])
        self.assertIsNone(evidence['real_iphone11'])

if __name__ == '__main__':
    unittest.main()
