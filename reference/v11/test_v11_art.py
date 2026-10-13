"""V11 visual art restoration: source, deterministic assets, exact original gameplay."""
from pathlib import Path
from PIL import Image, ImageChops
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
MAP_SHA='183302c32964f5a43ca7fe7ab4d00c1a8d1d4fe861c8688fbe41c2c9369dec8e'
asset=json.loads((ROOT/'assets/art-v11/MANIFEST.json').read_text())['assets']
assert len(asset)==13
for name,meta in asset.items():
    p=ROOT/meta['path'];assert p.is_file(),name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'],name
    assert Image.open(p).size==tuple(meta['size']),name
    assert Image.open(p).getbbox(),name
for before,after in [('objects/house_3d.png','house.png'),
                     ('objects/mine_3d.png','mine.png'),
                     ('objects/tree_round_v8.png','tree_round_0.png'),
                     ('tiles/cliff_macro_v10.png','cliff.png'),
                     ('tiles/terrain_materials_v6.png','water_materials.png')]:
    x=Image.open(ROOT/'assets'/before).convert('RGBA')
    y=Image.open(ROOT/'assets/art-v11'/after).convert('RGBA')
    assert x.size==y.size
    assert ImageChops.difference(x.convert('RGB'),y.convert('RGB')).getbbox(),after
assert Image.open(ROOT/'assets/art-v11/decals.png').size==(128,16)
assert hashlib.sha256((ROOT/'map.json').read_bytes()).hexdigest()==MAP_SHA
map_data=json.loads((ROOT/'map.json').read_text())
assert map_data['blockedTiles']==['water','cliff']
source=(ROOT/'demo.html').read_text();js=(ROOT/'art-v11.js').read_text()
assert len(re.findall(r'<script src=',source))==8
assert source.index('src="animation-lab-v2.js"')<source.index('src="art-v11.js"')
assert source.count('art_v11_decals')==1
assert all('assets/art-v11/'+n in source for n in ['house.png','mine.png','decals.png','rock.png','tree_round_0.png','tree_pine_0.png','water_materials.png','cliff.png'])
assert len(js.splitlines())<=400
assert 'DECAL_BUDGET = 90' in js and 'finally { imgs[hit.type] = original; }' in js
for disallowed in ('requestAnimationFrame(', 'setInterval(', 'setTimeout(', 'new Worker(', 'fetch(', 'WebGL'):
    assert disallowed not in js,disallowed
assert json.loads(source.split('const TILE=16, mapData=',1)[1].split(', imagePaths=',1)[0])==map_data
print('ART_V11_COMPATIBILITY_PASS: 13 offline pixel assets, 0 extra timers, original collision/map preserved')