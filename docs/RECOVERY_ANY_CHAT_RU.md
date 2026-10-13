# Any-chat Tech Lab recovery

This is a durable source-of-truth workflow, not an assertion that new code gets auto-loaded into every chat or World Server production. It works in a NEW chat with access to the owner's GitHub and same user's ChatGPT Library.

## Read order
1. https://github.com/mpaykin1/World_server/blob/master/AI_START_HERE.md — section 9 links to Tech Lab.
2. https://github.com/mpaykin1/world-server-tech-lab/blob/main/LIVE_STATUS.json — current checkpoint, blockers and next action.
3. https://github.com/mpaykin1/world-server-tech-lab/blob/main/AGENTS.md — recovery and safety contract.
4. https://github.com/mpaykin1/world-server-tech-lab/blob/main/catalog/active_capabilities.json — EXACT existing capabilities, source/asset/test/evidence and next step.
5. https://github.com/mpaykin1/world-server-tech-lab/blob/main/docs/V9_EXECUTION_BRIEF_RU.md — current work objective.
6. https://github.com/mpaykin1/world-server-tech-lab/blob/main/checkpoints/history.jsonl and https://github.com/mpaykin1/World_server/issues/80 — freshest historical and technical proof.

## Same user-owned files, exact version pin
Use ChatGPT Library path: /World Server/Graphics Reference/GRAPHICS-DEMO-001-playable-sandbox-v8(1).zip
SHA256: 419e7dd925f8b60beaeca662c1f19e86553113f4f1572490ffec5137f3beea11.
Verified by directly materializing that file, hashing bytes, and inspecting archive 135 members. In the ZIP find original medieval_world_infinite_pack_v3/demo.html, graphics-v8.js, tools/upgrade_to_v8.py, tools/test_graphics_v8.py, assets/tiles/shoreline_blob_47_v8.png and shoreline_blob_47_v8.json, assets/objects/tree_round_v8.png and tree_pine_v8.png. There is a DIFFERENT user Library file without the (1) suffix: do NOT silently substitute it.

Autotiler 47-mask adapter is available in GitHub Lab scripts/autotiler_47_index.py. The Pixelorama integration is a PNG-compatible FOUR-frame sprite layout in the ZIP; Pixelorama itself was NOT installed. Other V9 art goals are NOT IMPLEMENTED and must be developed with evidence.

## Six checks before continuing
- Fresh World and Lab HEAD SHAs, active PRs, and latest checks, not old printed percentages.
- LIVE_STATUS checkpoint number equals last history event; status links to registry + V9 brief.
- Every active capability resolves source + actual asset + test + evidence; ZIP digest matches exact pinned SHA.
- Know which V9 features still say NOT_IMPLEMENTED. Never report them as done until real tested code.
- World PR #491/#496/#379 current independent status: BLOCK/INCONCLUSIVE != PASS; use same PR if capacity full.
- 50% GRAPHICS/50% CLEAN_SERVER productive work target intact; actual ratio UNKNOWN until measured. No sixth automation.

On real output: commit Lab PR, pass CI, merge only if clean, update LIVE_STATUS/history/capability registry and append evidence checkpoint to existing issue #80. Owner PASS/FAIL only after playable MVP. Do not infer all-chat access for another user account lacking project/library permissions.

## CHECKPOINT 17 — V10 ART, ORIGINAL GAME (2026-10-13)

The latest locally browser-tested V10 faceted cliff/meadow/shore slice is **EXPERIMENTAL, NOT production**. No owner PASS/FAIL, no independent 85/100 reference score, no real iPhone11 proof. Do not confuse verified V8 asset adapters in `catalog.implemented` with V10 under `catalog.experimental_capabilities`.

- GitHub source: `scripts/landscape-art-v10.js`, `scripts/paint_cliffs_v10.py`, `scripts/rebuild_v10_landscape.py`, `scripts/browser_verify_v10.py`
- Exact playable: owner Library `/World Server/Graphics Reference/GRAPHICS-DEMO-001-playable-v10-landscape-checkpoint15.zip` SHA256 `d5ecdbae1a5885799e508d2a72780b3815bb149a67740c43a19ac046b451ad5f`
- Original baseline Library `GRAPHICS-DEMO-001-playable-v9-scene-art-checkpoint13.zip`, sha `63d0a624e7c982b7df2151b0de38b300a393437a21a5f65f78ef5b9935295ef7`
- Reproduce: `python scripts/rebuild_v10_landscape.py ORIGINAL_CHECKPOINT14.zip reconstructed-v10.zip`; then extract and run `tools/test_scene_v10.py`. Actual browser evidence and before/after 3 locations are in Library `/World Server/Graphics Reference/` and experiment `experiments/graphics-landscape-v10.json`.
- Same 52×28 owner map; original Canvas/player/controls, no new renderer. New script and separate atlas are additive. No user visibility threshold proven, no public preview link yet.
- CLEAN_SERVER: keep existing #491, #496, #379 independent BLOCK. Preserve five hourly agents and required target 50/50 allocation; actual productive minutes still unverified.

Continue from LIVE_STATUS; do not restart from V8 or silently treat the V10 prototype as production.
