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
