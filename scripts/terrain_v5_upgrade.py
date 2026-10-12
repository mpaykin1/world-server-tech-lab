#!/usr/bin/env python3
"""GRAPHICS-DEMO-001: CPU-only real asset/tile upgrade of the original V4 pack.
Run: python scripts/terrain_v5_upgrade.py /path/to/medieval_world_infinite_pack_v3
Requires Pillow. Does not touch World Server runtime, call AI APIs or deploy.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

TILE = 16
EDITS = [(26,4,"grass","sand"),(15,5,"grass","sand"),(27,5,"grass","sand"),
         (28,6,"grass","sand"),(7,8,"path","grass"),(28,9,"grass","sand"),
         (6,11,"path","grass"),(9,11,"path","grass"),(11,11,"path","grass"),
         (13,11,"path","grass"),(28,11,"grass","sand"),(15,18,"grass","sand"),
         (1,19,"grass","sand"),(6,19,"grass","sand"),(7,19,"grass","sand"),
         (11,19,"grass","sand"),(12,19,"grass","sand"),(15,19,"grass","sand")]
ATLAS_SHA = "e330b1d476e7ac70923ae02399ac2ffb3dc7852c4abf4e4d5f761f1b6ac64bb4"

def hashed(x, y, seed=0):
    data = f"{x}:{y}:{seed}".encode()
    return int.from_bytes(hashlib.blake2s(data, digest_size=4).digest(), "little")

def atlas():
    sheet = Image.new("RGBA", (256, 48), (0,0,0,0))
    colors = [
        ["#4b9b99","#73afb1","#a5ccbc","#e4d7a3","#faf1cf"],
        ["#365939","#49783e","#6d994b","#9ab668","#b6c37d"],
        ["#313b3b","#4c5c57","#637a59","#a9bc77","#d1d0a2"]
    ]
    for row in range(3):
        for mask in range(1,16):
            for y in range(16):
                for x in range(16):
                    n = hashed(x,y,19 + row*13)
                    north = (mask&1) and y < 3+hashed(x,0,row)%3
                    east = (mask&2) and x >= 13-hashed(15,y,row)%3
                    south = (mask&4) and y >= 13-hashed(x,15,row)%3
                    west = (mask&8) and x < 3+hashed(0,y,row)%3
                    if not (north or east or south or west): continue
                    inward = min(x,y,15-x,15-y)
                    i = min(3,inward)
                    if row == 0:
                        ci = [3,2,1,0][i]
                        if n%13==0: ci=4
                        alpha=[225,205,174,124][i]
                    elif row == 1:
                        ci = [3,2,1,0][i]
                        if n%7==0: ci=4
                        alpha=[248,225,200,170][i]
                    else:
                        ci=[4,3,2,1][i]
                        if n%11==0: ci=0
                        alpha=[245,220,197,152][i]
                    color=tuple(bytes.fromhex(colors[row][ci][1:]))
                    sheet.putpixel((mask*16+x,row*16+y),(*color,alpha))
    return sheet

TRANSITIONS = """// Authored sprite atlas, 4-way neighbor masks, original map/engine preserved.
function transitionMask(tx,ty,predicate){
  return (predicate(tileAt(tx,ty-1))?1:0)|
         (predicate(tileAt(tx+1,ty))?2:0)|
         (predicate(tileAt(tx,ty+1))?4:0)|
         (predicate(tileAt(tx-1,ty))?8:0);
}
function drawAuthoredTerrainTransition(tx,ty,sx,sy,type){
  const atlas=imgs.terrain_transition_atlas;
  if(!atlas?.naturalWidth)return false;
  let row=-1,mask=0;
  if(type==='water'||type==='shallow'){
    row=0;mask=transitionMask(tx,ty,t=>t!=='water'&&t!=='shallow');
  }else if(type==='path'||type==='sand'||type==='stone_path'){
    row=1;mask=transitionMask(tx,ty,t=>t==='grass');
  }else if(type==='cliff'){
    row=2;mask=transitionMask(tx,ty,t=>t!=='cliff');
  }
  if(!mask||row<0)return false;
  ctx.drawImage(atlas,mask*TILE,row*TILE,TILE,TILE,sx,sy,TILE,TILE);
  return true;
}
"""

def upgrade(root):
    root=Path(root)
    map_path=root/"map.json"
    world=json.loads(map_path.read_text(encoding="utf-8"))
    assert (world["width"],world["height"])==(52,28), "unexpected source map"
    assert world["blockedTiles"]==["water","cliff"], "collision rules changed"
    for x,y,old,new in EDITS:
        assert world["tiles"][y][x]==old, "V4 baseline mismatch: "+str((x,y))
        world["tiles"][y][x]=new
    output=root/"assets/tiles/terrain_transitions_v5.png"
    atlas().save(output,optimize=True)
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    assert digest==ATLAS_SHA, "atlas generation drift: "+digest
    map_path.write_text(json.dumps(world,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    html_path=root/"demo.html"
    html=html_path.read_text(encoding="utf-8")
    a=html.index("const TILE=16, mapData=")+len("const TILE=16, mapData=")
    b=html.index(", imagePaths=",a)
    html=html[:a]+json.dumps(world,ensure_ascii=False)+html[b:]
    needle='"tiles_atlas": "assets/tiles/world_tileset.png",'
    assert html.count(needle)==1
    html=html.replace(needle,needle+' "terrain_transition_atlas": "assets/tiles/terrain_transitions_v5.png",')
    html=html.replace("Medieval World V4","Medieval World V5").replace("· <b>V4</b>","· <b>V5</b>")
    html_path.write_text(html,encoding="utf-8")
    js_path=root/"graphics-enhancement.js"
    js=js_path.read_text(encoding="utf-8")
    needle="function drawTerrain(camX,camY,bounds){"
    assert js.count(needle)==1
    js=js.replace(needle,TRANSITIONS+needle)
    target="    }else{tileDetail(tx,ty,sx,sy,type);shorelineBlend(tx,ty,sx,sy,type);pathBlend(tx,ty,sx,sy,type);transition(tx,ty,sx,sy,type);}"
    assert js.count(target)==1
    replacement="""    }else{
      tileDetail(tx,ty,sx,sy,type);
      const authored=drawAuthoredTerrainTransition(tx,ty,sx,sy,type);
      if(!authored){shorelineBlend(tx,ty,sx,sy,type);pathBlend(tx,ty,sx,sy,type);}
      transition(tx,ty,sx,sy,type);
    }"""
    js=js.replace(target,replacement)
    js=js.replace("graphics-demo-001-sandbox-v4","graphics-demo-001-sandbox-v5")
    js=js.replace("mineAccessCells:MINE_ACCESS.size",
                  "mineAccessCells:MINE_ACCESS.size,authoredTileTransitionsLoaded:Boolean(imgs.terrain_transition_atlas?.naturalWidth)")
    js_path.write_text(js,encoding="utf-8")
    test=root/"tools/test_graphics_v4.py"
    v4test=test.read_text(encoding="utf-8")
    v4test=v4test.replace('"graphics-demo-001-sandbox-v4"','"graphics-demo-001-sandbox-v5"')
    v4test=v4test.replace('"Medieval World V4"','"Medieval World V5"')
    v4test=v4test.replace("graphics v4 ok:","graphics v4 compatibility on v5 ok:")
    test.write_text(v4test,encoding="utf-8")
    report={"id":"GRAPHICS-DEMO-001-v5","source":"v4","modified_map_tiles":len(EDITS),
            "tile_changes":[list(row) for row in EDITS],"blocked_tile_mutations":0,
            "map_dimensions_unchanged":True,"new_authored_atlas":"assets/tiles/terrain_transitions_v5.png",
            "atlas_bytes_sha256":digest,"atlas_width":256,"atlas_height":48,"atlas_variants":45,
            "user_visibility_percent":None,"reference_similarity_percent":None,"user_decision":None}
    (root/"GRAPHICS_DEMO_001_V5_EVIDENCE.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"changed_tiles":len(EDITS),"atlas_sha256":digest,"visual_quality":"UNKNOWN"}))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("v4_extracted_root",help="Root folder of authorized V4 pack")
    args=parser.parse_args()
    upgrade(args.v4_extracted_root)
