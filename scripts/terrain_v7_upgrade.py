#!/usr/bin/env python3
"""Upgrade an extracted, owned Medieval World V6 in-place with authored-shaped V7 sprites.
Usage: python terrain_v7_upgrade.py /path/to/medieval_world_infinite_pack_v3
CPU/Pillow only. No new runtime, map movement or engine replacements.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import argparse, hashlib, json, random

T = 16

def draw_foliage(d, frame, pine=False):
    rng = random.Random(9138 + frame * 17 + (99 if pine else 0))
    fw, fh = (30, 46) if pine else (36, 44)
    img = Image.new('RGBA', (fw, fh)); d = ImageDraw.Draw(img)
    bark = '#4c3021'; light_bark = '#a47748'
    d.polygon([(fw//2-4,fh-15),(fw//2+2,fh-15),(fw//2+4,fh-1),(fw//2-5,fh-1)], fill=bark)
    d.polygon([(fw//2-1,fh-14),(fw//2+1,fh-14),(fw//2+2,fh-1),(fw//2,fh-1)],fill=light_bark)
    mask=Image.new('L',(fw,fh));m=ImageDraw.Draw(mask)
    if pine:
        for cy,r,w in [(5,4,7),(12,7,11),(22,9,14),(31,8,14)]:
            m.polygon([(fw//2,cy-r),(fw//2-w,cy+r+2),(fw//2+w,cy+r+2)],fill=255)
        m.polygon([(fw//2,0),(fw//2-4,9),(fw//2+5,9)],fill=255)
    else:
        for cx,cy,rx,ry in [(11,14,10,12),(25,15,9,13),(18,9,12,9),
                            (17,21,16,10),(7,23,6,7),(29,22,6,8)]:
            m.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255)
    edge=mask.filter(__import__('PIL.ImageFilter',fromlist=['MaxFilter']).MaxFilter(3))
    img.paste((30,55,38,255),(0,0,fw,fh),edge)
    interior=Image.new('RGBA',(fw,fh),(37,98,56,255) if pine else (52,120,59,255))
    idraw=ImageDraw.Draw(interior)
    colors=['#1e5544','#226b48','#358148','#4a9c4d','#6ab64d','#8bcc56','#b9df70'] if pine else ['#285f43','#337842','#489346','#60ae47','#79c658','#a1d562','#d0e37e']
    for yy in range(fh):
        for xx in range(fw):
            if mask.getpixel((xx,yy))==0: continue
            # Shade lower and right canopy; brighter crowns face upper-left.
            depth=(xx/fw*.25)+(yy/fh*.43)
            k=2 if depth>.38 else 3 if depth>.21 else 4
            if rng.random()<.12:k+=1
            if rng.random()<.13:k-=1
            idraw.point((xx,yy),fill=colors[max(0,min(len(colors)-1,k))])
    img.paste(interior,(0,0),mask)
    dr=ImageDraw.Draw(img)
    for _ in range(44 if pine else 62):
        x=rng.randrange(fw);y=rng.randrange(2,fh-12)
        if mask.getpixel((x,y))==0:continue
        color='#a7d75d' if (x+y+frame)%3 else '#d3e67e'
        dr.rectangle((x,y,x+rng.choice([0,1,1]),y),fill=color)
    for xx in range(4,fw-2,7):
        yy=rng.choice([11,16,20,24])
        if mask.getpixel((xx,yy)):
            dr.point((xx,yy+1),fill='#1b5038')
    return img

def draw_rock():
    im=Image.new('RGBA',(26,22));d=ImageDraw.Draw(im)
    d.polygon([(1,17),(4,9),(9,5),(12,2),(19,3),(24,9),(25,17),(20,21),(6,21)],fill='#293b43')
    d.polygon([(3,16),(5,10),(12,4),(19,4),(23,9),(22,17),(18,20),(6,20)],fill='#687b80')
    d.polygon([(5,10),(12,4),(18,4),(14,11),(9,13),(4,17)],fill='#b6beb4')
    d.polygon([(14,11),(18,4),(23,9),(22,16),(18,20),(13,16)],fill='#51646c')
    d.polygon([(6,13),(9,10),(13,11),(12,17),(6,19),(4,16)],fill='#899c9f')
    d.line([(11,11),(13,13),(10,15),(11,17)],fill='#394b50',width=1)
    d.line([(18,6),(17,11),(19,14)],fill='#344c51',width=1)
    for x,y in [(6,10),(8,7),(12,5),(17,7),(21,11),(6,17)]:d.point((x,y),fill='#d5d5c2')
    return im

def overlay_atlas(kind):
    im=Image.new('RGBA',(256,16))
    for mask in range(1,16):
        d=ImageDraw.Draw(im)
        ox=mask*16
        def mark(a,b,step):
            seed=(mask*173+a*17+b*29+step*31)%9
            if kind=='shore':
                fill=('#dec891' if seed%3 else '#f0dcad')
                foam=('#e0f5ed' if seed%2 else '#9adeef')
            else:
                fill=('#768a80' if seed%3 else '#5c7372')
                foam=('#a6bb97' if seed%2 else '#c9c1a1')
            return fill,foam,2+seed%4
        for side,bit in [('top',1),('right',2),('bottom',4),('left',8)]:
            if not(mask&bit): continue
            for pos in range(16):
                fill,foam,length=mark(ox,pos,bit)
                if side=='top':x,y=ox+pos,0
                elif side=='bottom':x,y=ox+pos,15
                elif side=='left':x,y=ox,pos
                else:x,y=ox+15,pos
                for j in range(length):
                    px=x+(j if side=='left' else -j if side=='right' else 0)
                    py=y+(j if side=='top' else -j if side=='bottom' else 0)
                    im.putpixel((px,py),tuple(bytes.fromhex(fill[1:]))+(243,))
                q=length
                px=x+(q if side=='left' else -q if side=='right' else 0)
                py=y+(q if side=='top' else -q if side=='bottom' else 0)
                if 0<=px<256 and 0<=py<16 and (pos+mask)%3 != 0:
                    im.putpixel((px,py),tuple(bytes.fromhex(foam[1:]))+(172,))
    return im

def save_sheets(root):
    outputs={}
    for kind,fw,fh in [('tree_round',36,44),('tree_pine',30,46)]:
        sheet=Image.new('RGBA',(fw*4,fh))
        for frame in range(4):sheet.paste(draw_foliage(None,frame,pine=kind=='tree_pine'),(frame*fw,0))
        name=f'assets/objects/{kind}_v7.png'
        sheet.save(root/name,optimize=True);outputs[name]=sha(root/name)
    for name,img in [('assets/objects/rock_big_v7.png',draw_rock()),
                     ('assets/tiles/shoreline_shapes_v7.png',overlay_atlas('shore')),
                     ('assets/tiles/cliff_outcrops_v7.png',overlay_atlas('cliff'))]:
        img.save(root/name,optimize=True);outputs[name]=sha(root/name)
    return outputs

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

OVERLAYS="""
// Static memoized neighbor masks from original 52x28 map; render only edge tiles.
// A repeat/wrapped world reuses the same cache. Collision and world state untouched.
const V7_EDGE_MASKS=(()=>{
  const water=[],cliff=[];
  for(let y=0;y<mapData.height;y++)for(let x=0;x<mapData.width;x++){
    water.push(transitionMask(x,y,t=>t!=='water'&&t!=='shallow'));
    cliff.push(transitionMask(x,y,t=>t==='cliff'));
  }
  return {water,cliff};
})();
function drawV7TerrainShapes(tx,ty,sx,sy,type){
  const i=mod(ty,mapData.height)*mapData.width+mod(tx,mapData.width);
  let img,mask;
  if(type==='water'||type==='shallow'){
    img=imgs.shoreline_shapes_v7;mask=V7_EDGE_MASKS.water[i];
  }else if(type!=='cliff'){
    img=imgs.cliff_outcrops_v7;mask=V7_EDGE_MASKS.cliff[i];
  }
  if(mask&&img?.naturalWidth)ctx.drawImage(img,mask*TILE,0,TILE,TILE,sx,sy,TILE,TILE);
}
"""

def upgrade(root):
    root=Path(root)
    report=json.loads((root/'GRAPHICS_DEMO_001_V6_EVIDENCE.json').read_text())
    assert report['id']=='GRAPHICS-DEMO-001-v6'
    manifest=save_sheets(root)
    html_path=root/'demo.html';html=html_path.read_text()
    swaps={'assets/objects/tree_round_sheet.png':'assets/objects/tree_round_v7.png',
           'assets/objects/tree_pine_sheet.png':'assets/objects/tree_pine_v7.png',
           'assets/objects/rock_big.png':'assets/objects/rock_big_v7.png'}
    for old,new in swaps.items():
        assert html.count('"'+old+'"')==1,old
        html=html.replace('"'+old+'"','"'+new+'"')
    anchor='"terrain_material_atlas_v6": "assets/tiles/terrain_materials_v6.png",'
    assert html.count(anchor)==1
    extra=' "shoreline_shapes_v7": "assets/tiles/shoreline_shapes_v7.png", "cliff_outcrops_v7": "assets/tiles/cliff_outcrops_v7.png",'
    html=html.replace(anchor,anchor+extra).replace('· <b>V6</b>','· <b>V7</b>').replace('<title>Medieval World V6','<title>Medieval World V7')
    html_path.write_text(html)
    js_path=root/'graphics-enhancement.js';js=js_path.read_text()
    anchor='function drawTerrain(camX,camY,bounds){'
    assert js.count(anchor)==1
    js=js.replace(anchor,OVERLAYS+anchor)
    needle='      transition(tx,ty,sx,sy,type);'
    assert js.count(needle)==1
    js=js.replace(needle,needle+'\n      drawV7TerrainShapes(tx,ty,sx,sy,type);')
    js=js.replace('graphics-demo-001-sandbox-v6','graphics-demo-001-sandbox-v7')
    js=js.replace('variedMaterialsLoaded:Boolean(imgs.terrain_material_atlas_v6?.naturalWidth)',
                 'variedMaterialsLoaded:Boolean(imgs.terrain_material_atlas_v6?.naturalWidth),v7ShapesLoaded:Boolean(imgs.shoreline_shapes_v7?.naturalWidth&&imgs.cliff_outcrops_v7?.naturalWidth&&imgs.obj_tree_round?.naturalWidth)')
    js_path.write_text(js)
    evidence={'id':'GRAPHICS-DEMO-001-v7','source':'v6',
      'changed_sprite_silhouettes':['tree_round','tree_pine','rock_big'],
      'terrain_shape_atlases':['shoreline_shapes_v7','cliff_outcrops_v7'],
      'file_sha256':manifest,'world_tile_map_unchanged':True,'collision_unchanged':True,
      'original_engine_preserved':True,'reference_similarity_score':None,
      'iphone11_proof':None,'user_decision':None}
    (root/'GRAPHICS_DEMO_001_V7_EVIDENCE.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('v6_root')
    upgrade(ap.parse_args().v6_root)