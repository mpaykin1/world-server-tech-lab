#!/usr/bin/env python3
"""Idempotent insertion of V11 offline hand-shaded owned game assets."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'demo.html'
EXT=ROOT/'graphics-enhancement.js'
REWRITES={
 'assets/objects/house_3d.png':'assets/art-v11/house.png',
 'assets/objects/mine_3d.png':'assets/art-v11/mine.png',
 'assets/objects/rock_big_v7.png':'assets/art-v11/rock.png',
 'assets/objects/tree_round_v8.png':'assets/art-v11/tree_round_0.png',
 'assets/objects/tree_pine_v8.png':'assets/art-v11/tree_pine_0.png',
 'assets/tiles/cliff_macro_v10.png':'assets/art-v11/cliff.png',
 'assets/tiles/terrain_materials_v6.png':'assets/art-v11/water_materials.png',
}

def apply():
 src=DOC.read_text();assert 'art-v11.js' not in src
 for old,new in REWRITES.items():
  assert src.count(old)==1,old
  assert (ROOT/new).is_file(),new
  src=src.replace(old,new)
 mark='"obj_tree_round": "assets/art-v11/tree_round_0.png",'
 assert src.count(mark)==1
 extras=''.join(f' "v11_{sp}_{i}": "assets/art-v11/{sp}_{i}.png",'
     for sp in ('tree_round','tree_pine') for i in (0,1,2))
 src=src.replace(mark,mark+extras+' \"art_v11_decals\": \"assets/art-v11/decals.png\",')
 needle='<script src="animation-lab-v2.js"></script>'
 assert src.count(needle)==1
 src=src.replace(needle,needle+'<script src="art-v11.js"></script>')
 src=src.replace('Medieval World · V9','Medieval World · V11')
 # This is ONLY label text; no change to game state or collision map.
 assert src.count('<script src="art-v11.js"></script>')==1
 DOC.write_text(src)
 old=EXT.read_text();needle="load('assets/objects/bridge_h_extended.png')"
 assert old.count(needle)==1
 EXT.write_text(old.replace(needle,"load('assets/art-v11/bridge.png')"))
 print('ART_V11_APPLIED',hashlib.sha256(DOC.read_bytes()).hexdigest())

if __name__=='__main__':apply()