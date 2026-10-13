"""Cheap CI contract for V10 original-game art. Full browser proof lives in Library."""
import hashlib, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class LandscapeV10Test(unittest.TestCase):
    def test_art_adapter_stays_bounded(self):
        js=(ROOT/'scripts/landscape-art-v10.js').read_text()
        self.assertIn('TILE_BUDGET=900',js)
        self.assertIn('PREVIOUS(camX,camY,bounds)',js)
        self.assertIn('originalCliff(tx,ty,sx,sy,type)',js)
        self.assertIn("window.__graphicsDemoMetrics.landscapeV10",js)
        self.assertLessEqual(len(js.splitlines()),400)
        for banned in ('setInterval(', 'setTimeout(', 'requestAnimationFrame(', 'fetch(', 'new Worker('):
            self.assertNotIn(banned,js)

    def test_rebuild_fail_closed_and_pin(self):
        py=(ROOT/'scripts/rebuild_v10_landscape.py').read_text()
        self.assertIn('63d0a624e7c982b7df2151b0de38b300a393437a21a5f65f78ef5b9935295ef7',py)
        self.assertIn('Wrong pinned checkpoint14 V9 original ZIP',py)
        self.assertIn('Unexpected/unsafe archive structure',py)
        self.assertIn('Original world map differs',py)
        self.assertIn("['blockedTiles']",py)
        self.assertNotIn('world_master_write',py)

    def test_pixel_art_generator_reproducible_source(self):
        py=(ROOT/'scripts/paint_cliffs_v10.py').read_text()
        self.assertIn('random.Random(119407+variant*731)',py)
        self.assertIn('(192,64)',py)
        self.assertIn('ImageDraw',py)
        self.assertNotIn('requests.',py)

    def test_checkpoint_does_not_infer_verdict(self):
        import json
        status=json.loads((ROOT/'LIVE_STATUS.json').read_text())
        self.assertIsNone(status['owner_decision'])
        self.assertEqual(status['lane_policy']['GRAPHICS'],50)
        self.assertEqual(status['lane_policy']['CLEAN_SERVER'],50)
        self.assertEqual(status['lane_policy']['new_scheduled_jobs'],0)
        self.assertIsNone(json.loads((ROOT/'experiments/graphics-landscape-v10.json').read_text())['user_decision'])

if __name__=='__main__':unittest.main()