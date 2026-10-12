#!/usr/bin/env python3
"""OpenGame Debug Skill-inspired static preflight, no dependencies or runtime mutation."""
import argparse
import collections
import hashlib
import json
import zipfile
from pathlib import Path


def inspect_archive(path):
    source = Path(path)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    with zipfile.ZipFile(source) as z:
        names = set(z.namelist())
        manifests = [p for p in names if p.endswith("/manifest.json")]
        if len(manifests) != 1:
            raise ValueError("expected one rooted manifest.json")
        root = manifests[0][:-len("manifest.json")]
        manifest = json.loads(z.read(root + "manifest.json"))
        world = json.loads(z.read(root + manifest["map"]))
        refs = set()

        def collect(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k == "file" and isinstance(v, str):
                        refs.add(v)
                    else:
                        collect(v)
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, str) and v.lower().endswith((".png", ".jpg", ".webp")):
                        refs.add(v)
                    else:
                        collect(v)

        collect(manifest)
        missing = sorted(f for f in refs if root + f not in names)
        tiles = world["tiles"]
        width, height = world["width"], world["height"]
        if len(tiles) != height or any(len(row) != width for row in tiles):
            raise ValueError("map dimensions invalid")
        counts = collections.Counter(t for row in tiles for t in row)
        unknown = sorted(set(counts) - set(manifest["tileset"]["atlasTiles"]))
        edges = collections.Counter()
        for y in range(height):
            for x in range(width):
                for xx, yy in ((x + 1, y), (x, y + 1)):
                    if xx < width and yy < height and tiles[y][x] != tiles[yy][xx]:
                        edges[tuple(sorted((tiles[y][x], tiles[yy][xx])))] += 1
        animations = manifest.get("animatedObjects") or {}
        bad = sorted(k for k, v in animations.items() if int(v.get("frames", 0)) < 2)
        return {
            "schema_version": 1, "source_sha256": digest, "source_file": source.name,
            "policy": "READ_ONLY_ENGINE_UNCHANGED",
            "opengame_inspiration": "Debug Skill proactive asset-key/animation checks",
            "asset_references": len(refs), "asset_missing": missing,
            "map_width": width, "map_height": height, "map_tiles": width * height,
            "map_unique_tile_types": len(counts), "map_unknown_tile_keys": unknown,
            "tile_counts": dict(sorted(counts.items())),
            "distinct_neighbor_transition_types": len(edges),
            "neighbor_transition_edges": sum(edges.values()),
            "direct_water_cliff_edges": edges.get(("cliff", "water"), 0),
            "opposite_border_mismatch_rows": sum(row[0] != row[-1] for row in tiles),
            "opposite_border_mismatch_columns": sum(a != b for a, b in zip(tiles[0], tiles[-1])),
            "infinite_claimed_in_manifest": world.get("infinite") is True,
            "animated_objects": len(animations), "invalid_animation_frame_counts": bad,
            "diagnostic_pass": not (missing or unknown or bad),
            "visual_similarity_percent": None, "user_visibility_percent": None,
            "notes": "These are structural diagnostics, not user-visible graphical quality or a user PASS/FAIL."
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = inspect_archive(args.zip_file)
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    print(output, end="")
    if not result["diagnostic_pass"]:
        raise SystemExit(1)
