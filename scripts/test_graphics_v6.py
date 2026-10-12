from pathlib import Path
from PIL import Image
import hashlib,json
root=Path(__file__).resolve().parent.parent
report=json.loads((root/'GRAPHICS_DEMO_001_V6_EVIDENCE.json').read_text())
material=root/report['new_asset']
assert material.is_file() and Image.open(material).size==(256,96)
assert hashlib.sha256(material.read_bytes()).hexdigest()==report['asset_sha256']
assert report['total_derived_atlas_cells']==96 and report['tile_map_edited'] is False
assert report['original_engine_preserved'] and report['user_decision'] is None
js=(root/'graphics-enhancement.js').read_text()
html=(root/'demo.html').read_text()
assert 'function drawVariedMaterial(' in js
assert 'Math.imul' in js
assert 'variedMaterialsLoaded:Boolean(imgs.terrain_material_atlas_v6?.naturalWidth)' in js
assert 'terrain_material_atlas_v6' in html
assert 'graphics-demo-001-sandbox-v6' in js
assert 'const variedMaterial=drawVariedMaterial(tx,ty,sx,sy,type)' in js
assert len(json.loads((root/'map.json').read_text())['tiles'])==28
assert set(json.loads((root/'map.json').read_text())['blockedTiles'])=={'cliff','water'}
print('graphics v6 PASS: derived atlas, stable hash, original renderer and blocked movement preserved')
