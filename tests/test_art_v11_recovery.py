"""V11 checkpoint is recoverable, guarded, and not prematurely user-accepted."""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
class V11Recovery(unittest.TestCase):
    def test_asset_source_and_library_crosschat(self):
        x=json.loads((ROOT/'experiments/graphics-art-v11.json').read_text())
        self.assertIsNone(x['user_decision'])
        self.assertEqual(x['status'],'EXPERIMENTING')
        self.assertIsNone(x['measurement']['user_visibility_percent'])
        self.assertEqual(len(x['artifact']['playable_sha256']),64)
        for p in ('scripts/build_art_v11.py','scripts/apply_art_v11.py',
                  'scripts/art-v11.js','reference/v11/test_v11_art.py'):
            self.assertTrue((ROOT/p).is_file(),p)
        code=(ROOT/'scripts/art-v11.js').read_text()
        self.assertIn('DECAL_BUDGET = 90',code)
        self.assertNotIn('setInterval(',code)
        self.assertNotIn('requestAnimationFrame(',code)
        self.assertTrue(x['evidence']['map_sha_unchanged'])
        self.assertFalse(x['evidence']['production_changes'])
        self.assertIsNone(x['measurement']['independent_reference_similarity_percent'])
    def test_verdict_not_in_registry(self):
        state=json.loads((ROOT/'LIVE_STATUS.json').read_text())
        reg=json.loads((ROOT/'catalog/active_capabilities.json').read_text())
        self.assertEqual(state['checkpoint'],16)
        self.assertIn('graphics-art-v11',state['active_experiments'])
        self.assertTrue(any(x['id']=='graphics-art-v11' for x in reg['experimental_capabilities']))
        self.assertFalse(any(x['id']=='graphics-art-v11' for x in reg['implemented']))
        self.assertIsNone(state['owner_decision'])
if __name__=='__main__':unittest.main()
