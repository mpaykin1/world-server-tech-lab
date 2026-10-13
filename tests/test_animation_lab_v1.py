import json,unittest,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AnimationTechSource(unittest.TestCase):
 def test_original_adapter_contract(self):
  a=(ROOT/'scripts/animation-lab-v1.js').read_text()
  self.assertIn('animation-tech-lab-v1',a)
  self.assertIn('drawKnight = function animatedKnight',a)
  self.assertIn('drawAtmosphere = function animatedAtmosphere',a)
  self.assertIn('maxParticles = 48',a)
  self.assertIn('prefers-reduced-motion: reduce',a)
  self.assertIn('riggedCapeAndArm(',a)
  for bad in ('new Worker','setInterval(','setTimeout(','requestAnimationFrame(','fetch('):
   self.assertNotIn(bad,a)
 def test_browser_evidence_and_provenance_not_fake_pass(self):
  e=json.loads((ROOT/'experiments/animation-tech-lab-v1.json').read_text())
  b=json.loads((ROOT/'evidence/animation-tech-lab-v1-browser.json').read_text())
  self.assertEqual(e['status'],'EXPERIMENTING')
  self.assertIsNone(e['user_decision'])
  self.assertIsNone(e['measurement']['physical_iphone_fps'])
  self.assertEqual(e['implementation']['production'],'NOT_INTEGRATED')
  self.assertEqual(e['implementation']['particle_cap'],48)
  self.assertEqual(len(e['upstream']),3)
  self.assertEqual(b['animated_v9']['1200x780']['loaded'],44)
  self.assertEqual(b['animated_v9']['390x844']['js_errors'],[])
  self.assertGreater(b['animated_v9']['1200x780']['median_draw_ms'],b['baseline_v9']['1200x780']['median_draw_ms'])
if __name__=='__main__':unittest.main()
