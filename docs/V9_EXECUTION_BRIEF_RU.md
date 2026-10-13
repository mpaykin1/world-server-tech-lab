# EXECUTION DIRECTIVE — V9 GRAPHICS + CLEAN_SERVER (Russian)

**НАЧНИ РЕАЛЬНУЮ РАБОТУ. НЕ ЗАМЕНЯЙ ЯВНО ПОСТАВЛЕННУЮ ЗАДАЧУ ПЛАНОМ. НЕ НАЧИНАЙ WORLD SERVER ЗАНОВО.**

## 0. Восстановление из GitHub (свежие данные, не из памяти)
- Main: https://github.com/mpaykin1/World_server/blob/master/AI_START_HERE.md
- Lab: https://github.com/mpaykin1/world-server-tech-lab/blob/main/LIVE_STATUS.json
- Lab: https://github.com/mpaykin1/world-server-tech-lab/blob/main/AGENTS.md
- Lab: https://github.com/mpaykin1/world-server-tech-lab/blob/main/catalog/active_capabilities.json
- Lab: https://github.com/mpaykin1/world-server-tech-lab/blob/main/docs/RECOVERY_ANY_CHAT_RU.md
- World issue: https://github.com/mpaykin1/World_server/issues/80
- Check latest HEAD, open PR count, CI, checkpoint and active experiment; don't rely on stale readiness numbers.

## 1. Source artifact is fixed
The valid owner-owned V8 ZIP in this user's Library is:
/World Server/Graphics Reference/GRAPHICS-DEMO-001-playable-sandbox-v8(1).zip
SHA256: 419e7dd925f8b60beaeca662c1f19e86553113f4f1572490ffec5137f3beea11
CAUTION: Another distinct V8 ZIP exists without (1); do not overwrite or substitute it.
The ZIP retains the original medieval_world_infinite_pack_v3/demo.html, map.json, graphics-enhancement.js, graphics-v8.js, tools/upgrade_to_v8.py and tools/test_graphics_v8.py, animations/atlases and player controls. Target image lives in Library at /World Server/Graphics Reference/target_pixel_art_reference_2026-10-10.png.
Do not replace the existing engine, assets or world model.

## 2. GRAPHICS — target 50% of documented productive work
Create an actual playable V9 vertical slice in the original V8 code, not an image-only mockup.
Priority 1: HOUSES — attractive roofs, windows, doors, wall depth, chimney, fences, contact shadows, and warm lights. Ground the style in the actual target screenshot. First finish one visible functional improvement and its regression tests.
Then cliffs (faceted irregular silhouette, no tile seams), water (waves/foam/fish), lighting (contact shadows/lanterns), environmental animation (smoke, wind, flags, foliage). Reuse the current 47-mask autotiler and four-frame Pixelorama-compatible sprite pipeline.
Take same-camera, same-frame real-browser before/after screenshots; show original reference side-by-side. Track source SHA, changes, screenshot, keyboard/touch movement, JS errors, asset counts, identical collision/map invariants, CPU render costs on desktop + mobile-size at least 3 times, and physical iPhone 11 when possible. Do not claim 85% visibility or device FPS from emulator and do not equate pixel change with improvement.
Use CPU-only pipelines and license-safe preexisting game assets. No paid AI, no GPU requirement, no duplicate engine, no new background work.

## 3. CLEAN_SERVER — target 50% of documented productive work
Maintain the existing World Server tail budget and alternation TAILS -> DEVELOPMENT -> TAILS. Check fresh exact-head checks for PR #491, #496, #379 before editing. If a reproducible reviewer defect exists, fix MINIMALLY in same PR branch with negative regression and clean CI+Fleet PRE+independent review. Model hallucinations need independent source reproduction; BLOCK, INCONCLUSIVE and 429 are not PASS. No bypass/rename of gate, duplicate PR, self-merge on BLOCK, or rerun of identical SHA for luck. Do not spawn 6th AKA automation.
Measure non-overlapping productive minutes if possible. 50/50 is the target; without telemetry actual split remains UNKNOWN. Plans/reports do not count as productive graphics change or tail closure.

## 4. Save proof and keep future chats able to resume
For each real useful graphic change save versioned game ZIP, generator, tests, screenshot, desktop/mobile performance evidence, user reference comparison, exact SHA-256 and true limitations. In a LAB PR with CI update the experiment, LIVE_STATUS.json, checkpoints/history.jsonl and catalog/active_capabilities.json in same commit. Work in Lab branches only; never push directly to World_server/master. On merge, append a concise exact-SHA checkpoint to existing World_server issue #80. Ensure an authorized new chat can follow AI_START_HERE -> LIVE_STATUS -> capability registry -> the exact game ZIP and original source/test/evidence. No fake PASS/FAIL: user alone decides after real MVP; leave user_decision null otherwise.

## TERMINAL CONDITIONS
Do not call V9 complete until houses/cliffs/water/lights/animations appear in the actual playable game and pass functional/visual tests. No test link before verified >85% user visibility and real live URL. New chat recovery and a truthful 50/50 ledger are independent requirements, not substitutes for graphics.
**FIRST OPTIMAL NEXT STEP**: unpack exact V8(1), inspect real house sprite/map/camera, implement ONE visible V9 house upgrade, then one reproduced CLEAN_SERVER fix in existing PR. Save test and checkpoint, repeat.
