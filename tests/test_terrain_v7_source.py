import ast, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class GraphicsV7SourceTests(unittest.TestCase):
    def test_authored_shape_upgrade_generator_is_parseable_and_bounded(self):
        s=(ROOT/'scripts/terrain_v7_upgrade.py').read_text()
        ast.parse(s)
        self.assertIn('def draw_foliage(',s)
        self.assertIn('def draw_rock(',s)
        self.assertIn('def overlay_atlas(',s)
        self.assertIn('V7_EDGE_MASKS',s)
        self.assertIn('drawV7TerrainShapes(',s)
        self.assertLessEqual(len(s.splitlines()),400)
    def test_actual_measured_but_no_fabricated_score(self):
        experiment=json.loads((ROOT/'experiments/graphics-terrain-v7.json').read_text())
        perf=json.loads((ROOT/'evidence/graphics-terrain-v7-performance.json').read_text())
        vis=json.loads((ROOT/'evidence/graphics-terrain-v7-reference.json').read_text())
        self.assertEqual(experiment['chromium_smoke']['v7_loaded'],42)
        self.assertEqual(experiment['chromium_smoke']['js_errors'],[])
        self.assertEqual(experiment['lane_policy']['actual_productive_minutes'],'NOT_MEASURED')
        self.assertIsNone(experiment['owner_decision'])
        self.assertIsNone(experiment['reference_similarity_percent'])
        self.assertIsNone(vis['reference_similarity_percent'])
        self.assertIsNone(perf['owner_pass_fail'])
        self.assertTrue(vis['source_map_hash_unchanged'])
        self.assertEqual(len(perf['runs']),4)
        self.assertTrue(experiment['output_zip_sha256'].isalnum())
if __name__=='__main__':unittest.main()
