from pathlib import Path
from PIL import Image
import hashlib,json,re
root=Path(__file__).resolve().parent.parent
report=json.loads((root/'GRAPHICS_DEMO_001_V7_EVIDENCE.json').read_text())
assert report['id']=='GRAPHICS-DEMO-001-v7'
assert report['world_tile_map_unchanged'] and report['collision_unchanged']
assert len(report['file_sha256'])==5
for path,digest in report['file_sha256'].items():
    p=root/path
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,path
for name,size in [('tree_round_v7.png',(144,44)),('tree_pine_v7.png',(120,46)),('rock_big_v7.png',(26,22))]:
    assert Image.open(root/'assets/objects'/name).size==size,name
for name in ('shoreline_shapes_v7.png','cliff_outcrops_v7.png'):
    assert Image.open(root/'assets/tiles'/name).size==(256,16),name
html=(root/'demo.html').read_text();js=(root/'graphics-enhancement.js').read_text()
for name in ('tree_round_v7.png','tree_pine_v7.png','rock_big_v7.png','shoreline_shapes_v7.png','cliff_outcrops_v7.png'):
    assert name in html
assert 'graphics-demo-001-sandbox-v7' in js
assert 'V7_EDGE_MASKS' in js and 'drawV7TerrainShapes(' in js
assert 'v7ShapesLoaded:Boolean(' in js
assert 'function drawVariedMaterial(' in js, 'v6 terrain materials must not be removed'
assert 'function drawAuthoredTerrainTransition(' in js, 'v5 edge atlas must remain'
assert js.count("load('assets/objects/bridge_h_extended.png')")==1
world=json.loads((root/'map.json').read_text())
embedded=json.loads(html.split('const TILE=16, mapData=',1)[1].split(', imagePaths=',1)[0])
assert world==embedded and world['blockedTiles']==['water','cliff']
assert len(js.splitlines())<=400,'World Server max-file rule'
print('graphics v7 PASS: 5 authored silhouette/shore/cliff assets, renderer, original map and collision retained')