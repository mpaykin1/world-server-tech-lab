#!/usr/bin/env python3
"""Deterministic V10 art on checkpoint14 original medieval game, not a replacement engine."""
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile, ZIP_DEFLATED
from tempfile import TemporaryDirectory
import hashlib, json, sys
from paint_cliffs_v10 import make_cliff_atlas

BASE_SHA = '63d0a624e7c982b7df2151b0de38b300a393437a21a5f65f78ef5b9935295ef7'
MAP_SHA = '183302c32964f5a43ca7fe7ab4d00c1a8d1d4fe861c8688fbe41c2c9369dec8e'
OLD_ATLAS_SHA = 'b874e392d20e6c798c60066c2ae93a165a62908caa1dfdbc275f0a29ace584c7'
ROOT = 'medieval_world_infinite_pack_v3'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def one(text, old, new):
    if text.count(old)!=1:raise ValueError('source mismatch for '+old[:45])
    return text.replace(old,new)

def apply(root,source_dir):
    root=Path(root); source_dir=Path(source_dir)
    if sha(root/'map.json')!=MAP_SHA:raise ValueError('Original world map differs')
    if json.loads((root/'map.json').read_text())['blockedTiles']!=['water','cliff']:
        raise ValueError('Original collision policy differs')
    atlas=root/'assets/tiles/cliff_macro_v10.png'
    if atlas.exists():raise ValueError('V10 already applied')
    make_cliff_atlas().save(atlas,optimize=True)
    copyfile(source_dir/'landscape-art-v10.js',root/'landscape-art-v10.js')
    demo=root/'demo.html';html=demo.read_text(encoding='utf-8')
    html=one(html,'"cliff_macro_v9": "assets/tiles/cliff_macro_v9.png"',
             '"cliff_macro_v9": "assets/tiles/cliff_macro_v9.png", "cliff_macro_v10": "assets/tiles/cliff_macro_v10.png"')
    html=one(html,'<script src="water-light-v9.js"></script>',
             '<script src="water-light-v9.js"></script><script src="landscape-art-v10.js"></script>')
    html=html.replace('Medieval World V9','Medieval World V10')
    demo.write_text(html,encoding='utf-8')
    test=root/'tools/test_animation_lab_v1.py'
    body=test.read_text();test.write_text(one(body,'== 5','== 6'))
    copyfile(source_dir.parent/'tests/test_scene_v10.py',root/'tools/test_scene_v10.py')
    evidence={'id':'GRAPHICS-DEMO-001-v10','owner_decision':None,'independent_reference_score':None,
              'real_iphone11_fps':None,'new_engine':False,'paid_api':False,
              'map_sha256':sha(root/'map.json'),'faceted_cliff_asset_sha256':sha(atlas),
              'art':['faceted stone atlas','mossy cliff crowns','grouped meadow flowers','animated shore sparkle']}
    (root/'GRAPHICS_DEMO_001_V10_EVIDENCE.json').write_text(json.dumps(evidence,indent=2)+'\n')
    return evidence

def rebuild(archive,out):
    archive=Path(archive);out=Path(out)
    if sha(archive)!=BASE_SHA:raise ValueError('Wrong pinned checkpoint14 V9 original ZIP')
    with TemporaryDirectory(prefix='world_v10_') as temp:
        temp=Path(temp)
        with ZipFile(archive) as z:
            names=z.namelist()
            if any(not n.startswith(ROOT+'/') or '..' in Path(n).parts for n in names):
                raise ValueError('Unexpected/unsafe archive structure')
            z.extractall(temp)
        root=temp/ROOT
        apply(root,Path(__file__).parent)
        out.parent.mkdir(parents=True,exist_ok=True)
        with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
            for path in sorted(root.rglob('*')):
                if path.is_file():z.write(path,path.relative_to(temp))
    return sha(out)

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: rebuild_v10_landscape.py V9_CHECKPOINT14.zip OUTPUT_V10.zip')
    print('V10_ZIP_SHA256',rebuild(sys.argv[1],sys.argv[2]))