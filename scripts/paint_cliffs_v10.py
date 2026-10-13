#!/usr/bin/env python3
"""Original pixel-authored faceted cliff plate for the existing V9 4x4 atlas.
CPU-only Pillow offline renderer, no third-party asset rights or gameplay changes.
"""
from pathlib import Path
import random
from PIL import Image, ImageDraw

W=64
SWATCHES=[
 ((73,89,94),(89,105,108),(120,130,127),(45,60,65)),
 ((79,91,100),(95,106,112),(128,139,135),(49,61,72)),
 ((68,88,91),(88,103,103),(115,130,121),(41,59,61)),
]

def make_cliff_atlas():
    atlas=Image.new('RGBA',(192,64))
    for variant in range(3):
        rng=random.Random(119407+variant*731)
        base, mid, bright, dark=SWATCHES[variant]
        img=Image.new('RGBA',(64,64),(*base,255));d=ImageDraw.Draw(img)
        # Large broad irregular stone faces cross 16px tile boundaries without a brick-grid.
        stones=[(-12,-12,28,20),(18,-11,50,15),(46,-8,76,18),(-11,14,22,48),
                (13,12,47,41),(40,16,78,46),(-8,43,29,79),(23,39,56,80),(51,44,75,77)]
        for j,(x0,y0,x1,y1) in enumerate(stones):
            jitter=lambda n:rng.randint(-n,n)
            x0+=jitter(4);x1+=jitter(3);y0+=jitter(4);y1+=jitter(3)
            l=x0+max(2,(x1-x0)//5);r=x1-max(2,(x1-x0)//6)
            poly=[(l,y0),(r,y0+jitter(3)),(x1,y0+6),(x1-jitter(4),y1-6),
                  (r,y1),(x0+5,y1-jitter(4)),(x0,y0+7)]
            col=[mid,base,(92,106,105)][(j+variant)%3]
            d.polygon(poly,fill=(*col,255))
            d.line(poly[:3],fill=(*bright,255),width=2)
            d.line([poly[3],poly[4],poly[5]],fill=(*dark,255),width=2)
            inner=[(l+2,y0+5),(r-2,y0+7),(r-4,y1-7),(l+4,y1-8)]
            if j%2==0: d.polygon(inner,fill=(112,124,121,255))
            elif j%3==0: d.polygon(inner,fill=(65,78,84,255))
            for i in range(3):
                x=rng.randint(max(0,x0),min(63,x1)) if x1>=0 and x0<=63 else 0
                y=rng.randint(max(0,y0),min(63,y1)) if y1>=0 and y0<=63 else 0
                d.line([(x,y),(x+jitter(4),y+1)],fill=(*bright,255))
        # Eroded thin crevices, with moss and tiny ochre quartz chips.
        for i in range(10):
            x=rng.randrange(3,61);y=rng.randrange(4,60)
            d.line([(x,y),(x+rng.choice([-3,3,5]),y+2),(x+rng.choice([-3,4]),y+5)],fill=(*dark,255))
        for i in range(9):
            x=rng.randrange(3,62);y=rng.randrange(4,61)
            shade=[(63,111,67),(89,139,80),(130,151,93)][i%3]
            d.line((x,y,x+rng.randrange(2,6),y),fill=(*shade,255))
            if i%3==0:d.point((x+1,y+1),fill=(46,92,59,255))
        for i in range(8):
            x=rng.randrange(2,62);y=rng.randrange(2,62)
            d.point((x,y),fill=(173,156,126,255))
        atlas.paste(img,(variant*64,0))
    return atlas

if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:raise SystemExit('usage: paint_cliffs_v10.py destination.png')
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    make_cliff_atlas().save(out,optimize=True)