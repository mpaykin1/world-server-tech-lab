#!/usr/bin/env python3
"""Minimal offline 47-blob mask contract used by the user-owned V8 full ZIP.

Full V7->V8 Python asset upgrade is preserved inside the SHA-verified V8 ZIP at
tools/upgrade_to_v8.py. This small module needs no Pillow or network and makes
the Autotiler bit ordering/validity reusable by any other World Server consumer.
The upstream Autotiler/Pixleorama applications were NOT installed.
"""
from itertools import product

RUNTIME={"N":1,"E":2,"S":4,"W":8,"NE":16,"SE":32,"SW":64,"NW":128}
AUTOTILER={"N":1,"NE":2,"E":4,"SE":8,"S":16,"SW":32,"W":64,"NW":128}
ADJACENT=(("NE","N","E"),("SE","E","S"),("SW","S","W"),("NW","W","N"))

def legal_masks():
    return tuple(mask for mask in range(256) if all(
        not(mask&RUNTIME[corner]) or (
            mask&RUNTIME[first] and mask&RUNTIME[second])
        for corner,first,second in ADJACENT))

def to_autotiler(runtime_mask):
    if runtime_mask not in legal_masks():
        raise ValueError("noncanonical eight-neighbor blob mask")
    return sum(AUTOTILER[k] for k,bit in RUNTIME.items() if runtime_mask&bit)

def atlas_index(runtime_mask):
    return legal_masks().index(runtime_mask)

if __name__=="__main__":
    assert len(legal_masks())==47
    assert len({to_autotiler(m) for m in legal_masks()})==47
    print("47_BLOB_MASKS_PASS")
