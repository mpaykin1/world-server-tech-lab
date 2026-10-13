#!/usr/bin/env python3
"""Author additional pixel-art shading/geometry atop OWNED original game PNGs.
Deterministic CPU-only; no model/API, browser runtime or collision change.
Never overwrite original sprites: outputs live under assets/art-v11/.
"""
from PIL import Image, ImageDraw
from pathlib import Path
import random, json, hashlib

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'assets'
OUT = BASE / 'art-v11'
OUT.mkdir(parents=True, exist_ok=True)
SEED = 110021

def orig(rel):
    return Image.open(BASE / rel).convert('RGBA')

def save(img, name):
    target=OUT / name
    img.save(target, optimize=True)
    return {"path":str(target.relative_to(ROOT)),"size":list(img.size),"sha256":hashlib.sha256(target.read_bytes()).hexdigest()}

def rect(d,box,c): d.rectangle(box,fill=c)

def house():
    im=orig('objects/house_3d.png'); d=ImageDraw.Draw(im); r=random.Random(SEED)
    # Shingle rows clipped to the authored, non-transparent original roof silhouette.
    pix=im.load()
    mask=set()
    for y in range(7,39):
        for x in range(2,85):
            cr,cg,cb,a=pix[x,y]
            if a>190 and cr>70 and cr>cg*1.12 and cr>cb*1.17: mask.add((x,y))
    # Precise hand-indexed highlights and dark mortar never leak beyond roof polygons.
    for y in range(12,35,4):
        start=5 if (y//4)%2 else 1
        for x in range(start,84,9):
            for k in range(7):
                xx=x+k
                if (xx,y) in mask:
                    pix[xx,y]=(190+r.randrange(16),79+r.randrange(16),57+r.randrange(9),255)
                if (xx,y+1) in mask and k in (1,2,3):
                    pix[xx,y+1]=(238,129,77,255)
            for yy in range(y+1,y+4):
                if (x,yy) in mask: pix[x,yy]=(113,51,47,255)
    # Sunlit ridge and overlapped roof faces, cobbled foundation and wood grain.
    for x in range(9,67):
        if (x,11) in mask: pix[x,11]=(241,172,100,255)
    for x in range(13,68,11):
        if r.random()<.8: rect(d,(x,18,x+2,18),'#74413a')
    for y in (59,65,70):
        for x in range(6+(y%3)*4,78,12):
            if im.getpixel((x,y))[3]>0:
                d.line((x,y,x+8,y),fill='#b8b4a1',width=1)
                if x%3:rect(d,(x,y+2,x+1,y+2),'#5f6664')
    # Door arch keystone and reflective stained-glass panes.
    for x,y in ((47,35),(52,32),(58,35)):
        rect(d,(x,y,x+2,y+1),'#d8b78d')
    d.line((17,45,28,45),fill='#f9dfa0',width=1)
    rect(d,(20,50,20,53),'#fff4bb');rect(d,(24,50,24,53),'#8ed7d8')
    rect(d,(47,51,47,61),'#e0b26c');rect(d,(52,55,53,55),'#ffdc74')
    # Wooden exterior joists and climbing ivy follow right wall, NOT the tile collision.
    d.line((76,39,76,65),fill='#7b5b4b',width=2)
    for y in (45,50,57):
        rect(d,(80,y,82,y+1),'#3e7547')
        rect(d,(78,y+2,80,y+2),'#94b763')
    return im

def mine():
    im=orig('objects/mine_3d.png');d=ImageDraw.Draw(im);r=random.Random(SEED+5)
    # Pixel-authored limestone arch replacing the old uniform wooden slab.
    rocks=[[(7,16),(17,10),(23,18),(19,26),(7,28)],[(18,6),(28,4),(34,16),(26,21),(17,15)],
          [(33,4),(46,4),(48,15),(34,14)],[(48,7),(59,8),(63,21),(50,17)],
          [(61,16),(71,21),(71,36),(63,35)],[(4,30),(12,27),(14,39),(6,42)],
          [(6,41),(14,40),(16,52),(5,55)],[(61,38),(73,34),(74,52),(62,55)]]
    for i,poly in enumerate(rocks):
        d.polygon(poly,fill=['#677878','#87928b','#67746e','#56666a'][i%4])
        d.line(poly+[poly[0]],fill='#3a454a',width=1)
        x,y=poly[0];d.line((x+1,y+1,x+4,y+1),fill='#c3c4ad',width=1)
    # Keep original central dark opening, but give it thick beams with end grain.
    d.polygon([(20,21),(57,21),(55,30),(22,30)],fill='#493c32')
    rect(d,(21,22,57,26),'#75543b');d.line((22,22,56,22),fill='#cc9860',width=1)
    rect(d,(20,26,23,59),'#4b3529');rect(d,(57,26,60,59),'#4b3529')
    for x in (21,58):
        for y in range(28,56,7):rect(d,(x,y,x+1,y+1),'#c28d4e')
    for x,y in [(6,23),(10,38),(63,10),(64,43),(52,6),(17,10)]:
        rect(d,(x,y,x+2,y),'#b1b9a2')
    # Existing lanterns remain and now glow against the new stone masonry.
    for x in (1,72):
        rect(d,(x,35,x+2,39),'#ffbd54');rect(d,(x+1,36,x+1,37),'#fff1a6')
    return im

def bridge():
    im=orig('objects/bridge_h_extended.png');d=ImageDraw.Draw(im);r=random.Random(SEED+8)
    # Discrete plank grain, edge brackets and cast-iron rivets over the SAME deck.
    for x in range(11,86,7):
        d.line((x,12,x,32),fill='#533725',width=1)
        d.line((x+1,13,x+1,27),fill='#d7a16c',width=1)
        d.line((x+3,15,x+4,21),fill='#81502e',width=1)
        rect(d,(x+3,29,x+4,29),'#f0b777')
    for y in (10,15):
        d.line((5,y,91,y),fill='#442b22',width=2)
        d.line((6,y-1,90,y-1),fill='#c88e56',width=1)
    for x in (5,24,43,62,81,91):
        rect(d,(x,8,x+3,14),'#4b3025')
        rect(d,(x+1,9,x+1,9),'#f1c17f')
    return im

def foliage(name,palette_shift):
    original=orig('objects/'+name+'_v8.png')
    out=original.copy(); pixels=out.load()
    width=original.width//4
    for f in range(4):
        r=random.Random(SEED+palette_shift*311+f*13)
        for y in range(out.height-11):
            for x in range(f*width,(f+1)*width):
                rr,gg,bb,aa=pixels[x,y]
                if aa<240 or not(gg>rr*1.1 and gg>bb*.98): continue
                tone=(r.random()-.5)*20+palette_shift*11
                # Respect original shadow/highlight, create locally coherent leaf volumes.
                if (x//3+y//4+palette_shift)%5 in (0,1): tone-=20
                if (x//4-y//3+f)%7==0: tone+=20
                nr=max(15,min(235,int(rr+tone*.38)))
                ng=max(30,min(250,int(gg+tone)))
                nb=max(12,min(205,int(bb+tone*.25)))
                pixels[x,y]=(nr,ng,nb,aa)
        d=ImageDraw.Draw(out)
        for k in range(36 if name=='tree_round' else 22):
            xx=f*width+r.randrange(4,width-4);yy=r.randrange(5,out.height-14)
            rr,gg,bb,aa=original.getpixel((xx,yy))
            if aa<250 or gg<=rr*1.13:continue
            tint=['#bfe385','#8ec75d','#41734e','#224d3e'][r.randrange(4)]
            d.rectangle((xx,yy,xx+(k%2),yy),fill=tint)
    return out

def rocks():
    im=orig('objects/rock_big_v7.png');d=ImageDraw.Draw(im);pix=im.load();r=random.Random(SEED+22)
    for i in range(36):
        x=r.randrange(3,23);y=r.randrange(4,19)
        rr,gg,bb,a=pix[x,y]
        if a>200 and abs(rr-gg)<35:
            c=['#a3ada9','#485862','#b6bba9','#748b87'][i%4]
            d.line((x,y,x+(i%3),y),fill=c)
    d.line((7,6,10,4,16,5),fill='#c3c9b9',width=1)
    return im

def cliff():
    im=orig('tiles/cliff_macro_v10.png');d=ImageDraw.Draw(im);r=random.Random(SEED+35)
    w,h=im.size
    for macro in range(3):
        ox=macro*64
        for k in range(110):
            x=ox+r.randrange(2,62);y=r.randrange(3,61)
            rr,gg,bb,a=im.getpixel((x,y));
            if a<200 or gg>rr*1.35:continue
            if k%11==0:
                d.line((x,y,x+3,y-1,x+5,y+1),fill='#344548',width=1)
            elif k%7==0:
                d.line((x,y,x+4,y),fill='#a0ada4',width=1)
            elif k%5==0:
                d.line((x,y,x,y+3),fill='#3f5658',width=1)
            else:
                d.rectangle((x,y,x+1,y),fill=['#677b75','#88938a','#586c69','#abb2a3'][k%4])
        # Keep grassy crown near the top but dapple it with stepped stones.
        for k in range(12):
            x=ox+r.randrange(0,61);y=r.randrange(1,7)
            d.rectangle((x,y,x+2,y),fill=['#4a8541','#afd67d','#365f3b'][k%3])
    return im

def water():
    im=orig('tiles/terrain_materials_v6.png');d=ImageDraw.Draw(im)
    # Water is third atlas row (y32–47); all 4 variations keep their 4-frame timing.
    r=random.Random(SEED+40)
    for x0 in range(0,im.width,16):
        for y0 in (32,):
            y=y0+r.choice((3,6,10,13));x=x0+r.randrange(2,9)
            d.line((x,y,x+4,y),fill='#a3dcd6',width=1)
            if r.random()>.35:d.line((x+1,y+1,x+3,y+1),fill='#338aa9',width=1)
    return im

def decals():
    # Eight deliberately authored 16px decals, packed into a tiny alpha atlas.
    im=Image.new('RGBA',(8*16,16),(0,0,0,0));d=ImageDraw.Draw(im)
    def pixel(k,x,y,c,dx=1,dy=1):d.rectangle((16*k+x,y,16*k+x+dx-1,y+dy-1),fill=c)
    # 0 grass flower carpet with contact shadows and colored petals.
    for x,y in ((3,5),(10,12),(12,3)):
        pixel(0,x,y+1,'#2e6739',2,2);pixel(0,x-1,y,'#fff5c8',3,1)
        pixel(0,x,y-1,'#fefdf0');pixel(0,x,y+1,'#dba846')
    # 1 fern group growing beyond stone shadows.
    for k in range(3):
        x=2+k*5;pixel(1,x+1,13-k,'#254d30',2,2)
        for yy in range(5+k,12+k):
            pixel(1,x+1,yy,'#315f35')
            if yy%2:pixel(1,x-1,yy,'#7fae53',2,1);pixel(1,x+2,yy,'#91bb64',2,1)
    # 2 stone ruins chipped highlights/shadowed mortar.
    for x,y,w in ((2,4,6),(8,10,5),(4,14,8)):
        pixel(2,x,y+1,'#324447',w,2);pixel(2,x,y,'#a0aa9b',w,1)
        pixel(2,x,y+2,'#516666',w-2,1)
    # 3 shallow shore blue lines and foamy break.
    for x,y,w in ((2,4,7),(8,11,6),(5,14,8)):
        pixel(3,x,y,'#b1f0ef',w,1);pixel(3,x+1,y+1,'#4a9ca8',max(1,w-2),1)
    # 4 sand shells and reed stems.
    for x,y in ((3,6),(11,12)):
        pixel(4,x,y,'#ffe9b2',3,1);pixel(4,x+1,y-1,'#f9eaca',1,1)
        pixel(4,x,y+1,'#aa8359',2,1)
    pixel(4,8,5,'#2f6d56',1,6);pixel(4,7,7,'#adc566',1,3)
    # 5 twisted moss on cliff margins.
    for x,y in ((2,2),(9,10),(12,4)):
        pixel(5,x,y,'#28463a',4,3);pixel(5,x,y,'#729a50',4,1)
        pixel(5,x+1,y-1,'#b5d680',2,1)
    # 6 forest mushroom and leaf humus: original art, no imported engine.
    for x,y in ((5,5),(11,12)):
        pixel(6,x,y+2,'#e6d6aa',2,3)
        pixel(6,x-1,y,'#bb7051',4,2);pixel(6,x,y,'#edb080',1,1)
    for x,y in ((3,13),(8,3),(14,8)):
        pixel(6,x,y,'#385a3f',2,1)
    # 7 river stones in shadow, narrow alpha silhouette, no physics.
    for x,y in ((3,5),(10,11)):
        pixel(7,x,y+2,'#203d4f',6,1)
        pixel(7,x+1,y,'#677f89',4,2);pixel(7,x+2,y,'#c0c6b8',2,1)
    return im

def main():
    assets={}
    for name,im in [('house.png',house()),('mine.png',mine()),('bridge.png',bridge()),
                    ('rock.png',rocks()),('cliff.png',cliff()),('water_materials.png',water()),('decals.png',decals())]:
        assets[name]=save(im,name)
    for species in ('tree_round','tree_pine'):
        for v in range(3):
            n=f'{species}_{v}.png';assets[n]=save(foliage(species,v),n)
    p=OUT/'MANIFEST.json';p.write_text(json.dumps({'schema_version':1,'source':'original Game assets, copyright preserved','seed':SEED,'assets':assets,'owner_verdict':None},indent=2)+'\n')
    print('V11_ASSETS_READY',len(assets))

if __name__=='__main__':main()