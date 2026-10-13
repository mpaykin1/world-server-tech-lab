#!/usr/bin/env python3
"""Deterministic pixel-art upgrade for the original 92x74 user-owned V8 house sprite.

Requires Pillow. Accepts a verified extracted V8 original house; writes a V9 candidate.
No game engine, map, collision or third-party pixels are changed by this script.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import sys


def upgrade(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    if im.size != (92, 74):
        raise ValueError("pinned owner house canvas must remain 92x74")
    out = im.copy()
    d = ImageDraw.Draw(out)
    for row, y in enumerate((20, 24, 28)):
        for x in range(25 + (row % 2)*2, 61, 6):
            d.line((x,y,x+4,y),fill="#d97950",width=1)
            d.point((x+1,y+1),fill="#e7a06b")
            d.line((x+4,y+1,x+4,y+2),fill="#742c29",width=1)
    d.line((23,19,61,19),fill="#5c302a",width=1)
    d.line((62,20,75,35),fill="#c66940",width=2)
    d.line((65,23,76,36),fill="#783427",width=1)
    d.rectangle((18,9,22,17),fill="#a2a19b")
    d.line((17,9,23,9),fill="#504b48",width=2)
    d.point((20,13),fill="#e0c8ac")
    d.line((20,30,61,30),fill="#593a27",width=2)
    d.line((20,32,20,49),fill="#8e5b39",width=2)
    for x,y in ((21,36),(53,37),(21,43),(55,46)):
        d.line((x,y,x+4,y),fill="#c59d6a",width=1)
    for x,y in ((20,54),(28,57),(53,54),(64,57),(74,59)):
        d.line((x,y,x+4,y),fill="#797b76",width=1)
        d.point((x+1,y+1),fill="#ded2ae")
    d.rectangle((24,40,26,43),fill="#ffe09a")
    d.rectangle((29,40,31,43),fill="#ffd478")
    d.rectangle((24,45,26,46),fill="#e8a85b")
    d.rectangle((29,45,31,46),fill="#e9b96d")
    d.point((25,40),fill="#fff3c7")
    for x in (39,43,47):
        d.line((x,43,x,60),fill="#5c3527",width=1)
    d.line((37,37,47,37),fill="#b08858",width=1)
    d.rectangle((48,48,49,49),fill="#f4cb75")
    d.rectangle((37,61,52,62),fill="#77756b")
    d.line((38,62,51,62),fill="#c4b49a",width=1)
    d.line((53,35,55,35),fill="#40392d",width=1)
    d.rectangle((54,36,57,42),fill="#3b302b")
    d.rectangle((55,37,56,40),fill="#ffcc6a")
    d.point((55,37),fill="#fff3af")
    dst.parent.mkdir(parents=True,exist_ok=True)
    out.save(dst,optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: house_art_v9_upgrade.py V8_original_house.png V9_house.png")
    upgrade(Path(sys.argv[1]),Path(sys.argv[2]))
