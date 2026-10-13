"""Pack-only acceptance; Lab CI verifies its recovery source without local game assets."""
from pathlib import Path
_PACK = Path(__file__).resolve().parents[1]
if not (_PACK / "demo.html").is_file():
    import unittest
    class _UnpackedGameOnly(unittest.TestCase):
        def test_original_game_is_not_duplicated_in_lab(self):
            self.assertTrue((_PACK / "scripts/rebuild_v10_landscape.py").is_file())
else:
    """Regression contract for isolated V10 artistic terrain: preservation and honest evidence."""
    from pathlib import Path
    import hashlib,json,re
    from PIL import Image,ImageChops
    r=Path(__file__).resolve().parents[1];s=(r/'demo.html').read_text()
    asset=r/'assets/tiles/cliff_macro_v10.png'
    a=Image.open(asset).convert('RGBA');assert a.size==(192,64)
    prev=Image.open(r/'assets/tiles/cliff_macro_v9.png').convert('RGBA')
    assert ImageChops.difference(a.convert("RGB"),prev.convert("RGB")).getbbox()
    assert s.count('"cliff_macro_v10": "assets/tiles/cliff_macro_v10.png"')==1
    assert s.count('src="landscape-art-v10.js"')==1
    assert s.index('src="animation-lab-v1.js"')<s.index('src="landscape-art-v10.js"')
    assert len(re.findall(r'<script src=',s))==6
    assert len((r/'landscape-art-v10.js').read_text().splitlines())<=400
    assert len((r/'graphics-enhancement.js').read_text().splitlines())<=400
    assert 'water' in (r/'landscape-art-v10.js').read_text()
    assert 'originalCliff(tx,ty,sx,sy,type)' in (r/'landscape-art-v10.js').read_text()
    assert 'TILE_BUDGET=900' in (r/'landscape-art-v10.js').read_text()
    assert hashlib.sha256((r/'map.json').read_bytes()).hexdigest()=='183302c32964f5a43ca7fe7ab4d00c1a8d1d4fe861c8688fbe41c2c9369dec8e'
    assert json.loads((r/'map.json').read_text())['blockedTiles']==['water','cliff']
    for forbidden in ('requestAnimationFrame(', 'setInterval(', 'new Worker(', 'fetch(', 'WebGLRenderingContext'):
     assert forbidden not in (r/'landscape-art-v10.js').read_text(),forbidden
    assert json.loads((r/'GRAPHICS_DEMO_001_V10_EVIDENCE.json').read_text())['owner_decision'] is None
    print('V10 ORIGINAL_GAME_ART_PRESERVATION_PASS')