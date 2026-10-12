#!/usr/bin/env python3
"""CPU-only V5->V6 authored material variants from the original owner's sprites.
Run with Pillow installed. Never changes the World Server engine or collision.
"""
from pathlib import Path
from PIL import Image
import argparse
import hashlib
import json
import random
import shutil

TILE = 16
MATERIALS = {
    'grass': ('grass_sheet.png', 4), 'sand': ('sand.png', 1),
    'water': ('water_sheet.png', 4), 'cliff': ('cliff_sheet.png', 4),
    'path': ('path.png', 1), 'stone_path': ('stone_path.png', 1)
}
PALETTE = {
    'grass': [(64,146,62),(91,173,72),(126,190,76),(173,206,98)],
    'sand': [(204,178,111),(225,197,130),(241,218,158),(250,234,177)],
    'water': [(14,99,176),(25,121,205),(38,150,219),(120,199,238)],
    'cliff': [(62,72,72),(84,94,90),(117,126,119),(157,163,146)],
    'path': [(179,142,94),(204,170,116),(232,199,143),(244,220,167)],
    'stone_path': [(83,93,91),(112,118,111),(146,150,136),(183,182,155)]
}

def tone(r, g, b, kind):
    if kind == 'water': return max(0,int(r*.68)),max(0,int(g*.87)),max(0,int(b*.96))
    if kind == 'grass': return min(255,int(r*.89)),min(255,int(g*.99)),min(255,int(b*.76))
    if kind == 'cliff': return int(r*.87),int(g*.94),int(b*.82)
    return r,g,b

def variant(frame, kind, variation):
    """Precompute material details once; runtime uses drawImage, not pixel loops."""
    rng = random.Random(1985 + variation*529 +
                        ["grass","sand","water","cliff","path","stone_path"].index(kind)*271)
    out = Image.new('RGBA', (16,16))
    pixels = frame.convert('RGBA').load()
    for y in range(16):
        for x in range(16):
            r,g,b,a = pixels[x,y]
            r,g,b = tone(r,g,b,kind)
            spot = (x*29+y*13+variation*71)%17
            if spot < 3 and rng.random() < .3:
                pr,pg,pb = PALETTE[kind][rng.randrange(4)]
                r,g,b = (2*r+pr)//3,(2*g+pg)//3,(2*b+pb)//3
            out.putpixel((x,y),(r,g,b,a))
    draw = out.load()
    for _ in range(4 if kind in ('water','grass') else 3):
        x,y = rng.randrange(1,14),rng.randrange(1,14)
        c = PALETTE[kind][rng.randrange(4)]
        points = [(0,0),(1,0),(0,1)] if rng.random()<.6 else [(0,0),(1,0)]
        for dx,dy in points:
            r,g,b,a = draw[x+dx,y+dy]
            if kind=='water' and (x+y+variation)%3==0:
                c = PALETTE['water'][3]
            draw[x+dx,y+dy] = ((r+c[0])//2,(g+c[1])//2,(b+c[2])//2,a)
    return out

def make_atlas(root):
    atlas = Image.new('RGBA',(16*16,16*len(MATERIALS)),(0,0,0,0))
    for row,(kind,(filename,frames)) in enumerate(MATERIALS.items()):
        source = list((root/'assets').rglob(filename))
        if len(source)!=1: raise ValueError('source asset missing/ambiguous: '+filename)
        raw = Image.open(source[0]).convert('RGBA')
        if raw.size!=(16*frames,16): raise ValueError('unexpected source size: '+str(raw.size))
        for var in range(4):
            for f in range(4):
                sprite = raw.crop(((f%frames)*16,0,(f%frames+1)*16,16))
                atlas.paste(variant(sprite,kind,var),((var*4+f)*16,row*16))
    return atlas

PATCH_JS = """
// V6 authored offline variants, stable deterministic cell animation, no runtime noise allocations.
const V6_MATERIAL_ROWS=Object.freeze({grass:0,sand:1,water:2,cliff:3,path:4,stone_path:5});
function drawVariedMaterial(tx,ty,sx,sy,type){
  const img=imgs.terrain_material_atlas_v6;
  const row=V6_MATERIAL_ROWS[type];
  if(!img?.naturalWidth||row===undefined)return false;
  let n=(Math.imul(tx,73856093)^Math.imul(ty,19349663))|0;
  n^=n>>>16;n=Math.imul(n,0x7feb352d);n^=n>>>15;
  const variant=n&3;
  const frames=frameMeta.tile[type]||1;
  const frame=frames>1?(frameIndex(frames,4)+(variant&3))%frames:0;
  ctx.drawImage(img,(variant*4+frame)*TILE,row*TILE,TILE,TILE,sx,sy,TILE,TILE);
  return true;
}
"""

def upgrade(root):
    root=Path(root)
    asset=root/'assets/tiles/terrain_materials_v6.png'
    make_atlas(root).save(asset,optimize=True)
    jsfile=root/'graphics-enhancement.js'
    js=jsfile.read_text(encoding='utf-8')
    assert 'terrain_material_atlas_v6' not in js
    start='function drawTerrain(camX,camY,bounds){'
    assert js.count(start)==1
    js=js.replace(start,PATCH_JS+start)
    needle="    sprite('tile_'+type,sx,sy,frameIndex(frameMeta.tile[type]||1,4));"
    assert js.count(needle)==1
    js=js.replace(needle,"    const variedMaterial=drawVariedMaterial(tx,ty,sx,sy,type);\n    if(!variedMaterial)sprite('tile_'+type,sx,sy,frameIndex(frameMeta.tile[type]||1,4));")
    needle='      tileDetail(tx,ty,sx,sy,type);'
    assert js.count(needle)==1
    js=js.replace(needle,'      if(!variedMaterial)tileDetail(tx,ty,sx,sy,type);')
    js=js.replace('graphics-demo-001-sandbox-v5','graphics-demo-001-sandbox-v6')
    js=js.replace('authoredTileTransitionsLoaded:Boolean(imgs.terrain_transition_atlas?.naturalWidth)',
                  'authoredTileTransitionsLoaded:Boolean(imgs.terrain_transition_atlas?.naturalWidth),variedMaterialsLoaded:Boolean(imgs.terrain_material_atlas_v6?.naturalWidth)')
    jsfile.write_text(js,encoding='utf-8')
    htmlfile=root/'demo.html'
    html=htmlfile.read_text(encoding='utf-8')
    needle='"terrain_transition_atlas": "assets/tiles/terrain_transitions_v5.png",'
    assert html.count(needle)==1
    html=html.replace(needle,needle+' "terrain_material_atlas_v6": "assets/tiles/terrain_materials_v6.png",')
    html=html.replace('Medieval World V5','Medieval World V6').replace('· <b>V5</b>','· <b>V6</b>')
    htmlfile.write_text(html,encoding='utf-8')
    for name in ('test_graphics_v5.py','test_graphics_v4.py'):
        check=root/'tools'/name
        old=check.read_text(encoding='utf-8')
        old=old.replace('graphics-demo-001-sandbox-v5','graphics-demo-001-sandbox-v6')
        old=old.replace('Medieval World V5','Medieval World V6')
        check.write_text(old,encoding='utf-8')
    shutil.copy2(Path(__file__).resolve().parent/'test_graphics_v6.py',root/'tools/test_graphics_v6.py')
    report={
      'id':'GRAPHICS-DEMO-001-v6','source':'v5',
      'new_asset':str(asset.relative_to(root)),
      'asset_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),
      'source_tiles_used':list(MATERIALS),'derived_variants_per_material':16,
      'total_derived_atlas_cells':16*len(MATERIALS),
      'tile_map_edited':False,'original_engine_preserved':True,
      'user_visibility_percent':None,'user_decision':None
    }
    (root/'GRAPHICS_DEMO_001_V6_EVIDENCE.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('extracted_v5_root')
    args=p.parse_args()
    print(json.dumps(upgrade(Path(args.extracted_v5_root)),indent=2))
