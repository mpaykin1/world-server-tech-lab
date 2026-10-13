#!/usr/bin/env python3
"""Rebuild the original medieval game's V9 scene from the pinned playable animation ZIP.

No new engine, network calls, runtime dependencies, concurrent jobs or production edits.
Input belongs to owner's Library; download the pinned original manually once per recovery.
"""
import hashlib
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from scripts.house_art_v9_upgrade import upgrade as upgrade_house
    from scripts.house_runtime_patch_v9 import patch as patch_house_runtime
except ImportError:
    from house_art_v9_upgrade import upgrade as upgrade_house
    from house_runtime_patch_v9 import patch as patch_house_runtime

BASE_SHA256 = "58d72dc5e044862fd708d0e7becef0b21c3de11997300e3b1d6d6946b80446eb"
MAP_SHA256 = "183302c32964f5a43ca7fe7ab4d00c1a8d1d4fe861c8688fbe41c2c9369dec8e"
HOUSE_SHA256 = "b874e392d20e6c798c60066c2ae93a165a62908caa1dfdbc275f0a29ace584c7"
ROOT_NAME = "medieval_world_infinite_pack_v3"
SCRIPT_NAME = 'water-light-v9.js'
SCRIPT_TAG = '<script src="animation-lab-v1.js"></script>'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rebuild(baseline_zip, output_zip):
    baseline_zip, output_zip = Path(baseline_zip), Path(output_zip)
    if digest(baseline_zip) != BASE_SHA256:
        raise ValueError("Wrong V9 animation baseline ZIP; refusing an unpinned game")
    with tempfile.TemporaryDirectory(prefix="worldserver_v9_") as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(baseline_zip) as z:
            names = z.namelist()
            if any(not p.startswith(ROOT_NAME + "/") or ".." in Path(p).parts for p in names):
                raise ValueError("Unsafe or unexpected ZIP member")
            z.extractall(tmp)
        root = tmp / ROOT_NAME
        if digest(root / "map.json") != MAP_SHA256:
            raise ValueError("Original world/map integrity mismatch")
        house = root / "assets/objects/house_3d.png"
        upgrade_house(house, house)
        if digest(house) != HOUSE_SHA256:
            raise ValueError("V9 house reference sprite mismatch")
        patch_house_runtime(root / "graphics-enhancement.js")
        source = Path(__file__).with_name(SCRIPT_NAME)
        shutil.copyfile(source, root / SCRIPT_NAME)
        html = root / "demo.html"
        raw = html.read_text(encoding="utf-8")
        if raw.count(SCRIPT_TAG) != 1 or SCRIPT_NAME in raw:
            raise ValueError("Unexpected animation scripts or duplicate V9 adapter")
        html.write_text(raw.replace(SCRIPT_TAG, SCRIPT_TAG + '<script src="' + SCRIPT_NAME + '"></script>'), encoding="utf-8")
        animation_test = root / 'tools/test_animation_lab_v1.py'
        if animation_test.exists():
            test = animation_test.read_text(encoding="utf-8")
            assert test.count('== 4') == 1, "Unexpected animation test baseline"
            animation_test.write_text(test.replace('== 4', '== 5'))
        if len((root / "graphics-enhancement.js").read_text().splitlines()) > 400:
            raise ValueError("World Server renderer architecture limit")
        output_zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in sorted(root.rglob("*")):
                if f.is_file():
                    member = zipfile.ZipInfo(str(f.relative_to(tmp)), date_time=(2026, 10, 13, 0, 0, 0))
                    member.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(member, f.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    return digest(output_zip)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit('usage: rebuild_v9_scene.py PINNED_ANIMATION_BASE.zip OUTPUT.zip')
    print("ZIP_SHA256", rebuild(sys.argv[1], sys.argv[2]))
