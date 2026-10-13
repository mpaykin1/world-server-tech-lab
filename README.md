# World Server Tech Lab

Изолированная лаборатория открытых игровых технологий для [World Server](https://github.com/mpaykin1/World_server). **Не отдельная production-игра** и не замена существующему движку.

## Что делает лаборатория

- Исследует open-source генераторы браузерных игр, 2D/2.5D/3D-графику, анимации, физику и инструменты AI-разработки.
- Проверяет **один узкий воспроизводимый эксперимент** за раз, фиксирует upstream SHA/tag, лицензию кода и ассетов отдельно.
- Сравнивает результат с конкретным эталоном, baseline FPS/памяти и скриншотами; при доступности проверяет iPhone 11.
- Передаёт в World Server только измеримые улучшения, через **отдельную ветку → CI/ревью → PR**. Никогда не пишет напрямую в `World_server/master`.
- Хранит результаты и открытые ограничения в GitHub, чтобы любой новый чат продолжал работу с последнего checkpoint.

## Постоянные ограничения

1. **50% GRAPHICS / 50% CLEAN_SERVER** — политика основной системы World Server. Лаборатория не отменяет закрытие технических хвостов и не создаёт новые очереди задач.
2. **Без новых ежечасных задач AKA**, платных ИИ API, бесконтрольного GPU/CPU и запуска внешнего кода без проверки. GitHub CI здесь работает только при push/PR/ручном запуске.
3. Кандидаты в [каталоге](catalog/candidates.json) имеют статус `RESEARCH_ONLY` до проверки лицензии, конкретного коммита, ресурсов и практической совместимости. Наличие ссылки в каталоге не означает, что технология установлена.
4. Пользователь единолично выставляет **PASS или FAIL после MVP**. Только после его решения можно коммитить анализ успеха/неудачи. До этого: `user_decision: null`.
5. Нельзя утверждать `user_visibility > 85%` или выдавать рабочую **ссылку для тестирования MVP**, пока это не подтверждено измерениями и свежей проверкой URL. Репозиторий и PR — ссылки на код, не на протестированный MVP.

## Для нового чата / любого агента

1. Прочти [AGENTS.md](AGENTS.md) и этот README.
2. В основном проекте открой [AI_START_HERE.md](https://github.com/mpaykin1/World_server/blob/master/AI_START_HERE.md), [AGENTS.md](https://github.com/mpaykin1/World_server/blob/master/AGENTS.md) и [issue #80](https://github.com/mpaykin1/World_server/issues/80).
3. Проверь, нет ли уже активного эксперимента или дублирующего PR; если есть — продолжай, а не запускай новый.
4. Выбери из [catalog/candidates.json](catalog/candidates.json) один эксперимент; скопируй [experiments/TEMPLATE.json](experiments/TEMPLATE.json) в новый `experiments/<id>.json`.
5. Проверь upstream-версию и лицензию, протестируй изолированно и приложи измеримое evidence. До доказательств не ставь `READY_FOR_USER`, `USER_PASS` или `USER_FAIL`.
6. Переноси в World Server только необходимые компоненты через его существующие integration gates; не строй второй движок.

## Минимальные проверки (Python 3.11+, без зависимостей и платных сервисов)

```sh
python scripts/check_lab.py
python -m unittest discover -s tests -v
```

[GitHub Actions](../../actions) выполняет их при изменениях без почасового расписания.

**Текущий этап: BOOTSTRAP.** Создана только лабораторная инфраструктура и проверки. Готового игрового MVP, подтверждённого прироста качества или установленного OpenGame/Project Orbit пока нет.

## Resume state (canonical Tech Lab entrypoint)

Always read [LIVE_STATUS.json](LIVE_STATUS.json) and [the compact checkpoint history](checkpoints/history.jsonl) first, then refresh GitHub exact HEAD/PR/CI. Do not replay long chat logs.

After **material changes**, run `python scripts/checkpoint.py --event IMPLEMENTED --evidence experiments/<id>.json --phase EXPERIMENTING --next-action "..." --active-experiment <id> --blocker "..."`. Commit `LIVE_STATUS.json` and `checkpoints/history.jsonl` **with** the material change. The existing GitHub Actions checks `python scripts/check_status.py --changes`; no scheduler, no extra hourly role. Staleness >14 days is reported at the next CI run, not by polling.

The first OpenGame-inspired experiment is [opengame-medieval-visual-diagnostics-001](experiments/opengame-medieval-visual-diagnostics-001.json). Reproduce without internet or extra packages using `python scripts/opengame_medieval_preflight.py PATH_TO_AUTHORIZED_ZIP`. Real archive inputs are in ChatGPT Library `/World Server/Graphics Reference/`, not duplicated into GitHub. Evidence is in [v3](evidence/opengame-medieval-v3.json) / [v4](evidence/opengame-medieval-v4.json). This is read-only, not a claim of visual readiness.

## Latest real medieval terrain experiment (V5, separate from production)

[Experiment](experiments/graphics-terrain-v5.json) · [measured local Chromium smoke](evidence/graphics-terrain-v5-browser.json) · [offline reproduction script](scripts/terrain_v5_upgrade.py) · [authored 45-variant PNG atlas](artifacts/terrain_transitions_v5.png).

The source V4 and the new full playable V5 ZIP are in ChatGPT Library `/World Server/Graphics Reference/`. Exact V5 SHA256 `19d382484984858ad8c896ca030eeb65b2a8892a2dd6379d6e3d240b5d491125`; never substitute a synthetic preview. The **same original** 52×28 map was modified on 18 non-blocking cells, 45 border overlays are genuine authored pixel assets rendered by the existing canvas engine. Headless Chromium loaded 39/39 assets and preserved keyboard movement. The pixel-delta fraction 0.3114 means visual change, NOT 31% improvement; reference fidelity/owner verdict remain UNKNOWN. The lab keeps code/evidence, not another production runtime.

To rebuild locally, extract authorized V4 ZIP; run `python scripts/terrain_v5_upgrade.py path/to/medieval_world_infinite_pack_v3` with Pillow installed. No network/API/GPU necessary. Follow V4/V5 pack tests and browser smoke; compare actual reference before any >=85% visibility claim.

## V6 real material diversification and benchmark

[Experiment](experiments/graphics-terrain-v6.json) and [measured evidence](evidence/graphics-terrain-v6.json), [CPU-only source generator](scripts/terrain_v6_upgrade.py), [V6 pack regression](scripts/test_graphics_v6.py). Full playable original-game ZIP and saved Chromium v5/v6 frames are in ChatGPT Library `/World Server/Graphics Reference/`; ZIP SHA256 `dd011f5b7d0a84c33785c67af2f1e2527efea229188bb69e7fb0696050f944df`. A fresh agent should fetch that Library file rather than synthesize another demo.

V6 adds 96 material frame/variant cells based on existing owner-owned source textures and palette experiments. Same player, 52x28 tiled map, original engine and collision. Exact local pack tests and desktop/mobile-emulated browser smoke PASS (40/40 assets); three browser trials observed faster median/mean draw time than V5. However target visual fidelity, physical iPhone 11 performance and user visibility >85% remain UNKNOWN. No test link or owner PASS/FAIL is implied.

## Real medieval sprite silhouettes — V7 (2026-10-12)

[Original V6→V7 authored source](scripts/terrain_v7_upgrade.py) · [pack regression](references/test_graphics_v7_pack.py) · [experiment](experiments/graphics-terrain-v7.json) · [Chromium performance](evidence/graphics-terrain-v7-performance.json) · [reference metrics](evidence/graphics-terrain-v7-reference.json).

The **existing user-owned game** was upgraded in-place from V6 to V7. V7 adds five actual PNG assets changing broadleaf/pine crown silhouettes, faceted rock geometry, and shape overlays for shore/cliff; no new renderer, world rules, collision, API, nightly job, or production server changes. Optimized static 52×28 edge-mask precomputation avoids per-frame neighbor scans. Exact original map SHA is preserved. Full V7 ZIP SHA256 `296b778bda35f203079933b1a6ae41f293c433e5b6933d9afb8b944b08114622` is in Library `/World Server/Graphics Reference/GRAPHICS-DEMO-001-playable-sandbox-v7.zip`, not a deployed URL. Tests original V4/V5/V6/V7 + keyboard smoke PASS; 42/42 assets loaded. Three-run Chromium render time is slightly slower than V6; real iPhone 11 remains untested. Image pixel delta is not similarity nor improvement percentage. Owner PASS/FAIL unset; 85% visibility unmeasured. CLEAN_SERVER #491 has exact reproduction test; external reviewer at latest head returned INCONCLUSIVE due HTTP 429. Keep review gate blocked.

## GRAPHICS-DEMO-001 v8 — verified Autotiler 47-mask and Pixelorama PNG interchange

V7 original game upgraded in an isolated V8 sandbox. Full exact ZIP in Library: `/World Server/Graphics Reference/GRAPHICS-DEMO-001-playable-sandbox-v8(1).zip` SHA256 `419e7dd925f8b60beaeca662c1f19e86553113f4f1572490ffec5137f3beea11`. **Another older, different v8.zip exists**: do not overwrite or confuse them. User-owned original 52×28 map, collisions and canvas engine unchanged. 47 edge-neighbor masks + four animated foam phases; 4-frame tree canopy PNG sheets. Autotiler MIT (exact upstream `bc573b8e`) and Pixelorama MIT (`fe856859`) have verified GitHub sources and interoperability patterns, but full apps were **not installed/copied**. Actual generator and game are inside exact full ZIP (`tools/upgrade_to_v8.py`, `tools/test_graphics_v8.py`), and the lightweight 47-mask adapter is [scripts/autotiler_47_index.py](scripts/autotiler_47_index.py).

[Experiment](experiments/graphics-terrain-v8.json) and [CLEAN_SERVER exact-SHA review triage](evidence/clean-review-v8.json). Five prior graphics tests plus new V8 and pack check PASS, real local Chromium loaded 43/43 images and preserved controls; CPU desktop approximately 1.135ms vs 1.111ms v7, emulated mobile approximately 0.611ms vs 0.684ms. Variance: 3 short runs, not physical phone. No reference similarity score or >85% user visibility proof; owner PASS/FAIL remains unset. 50/50 productive-time rule maintained, actual minutes UNMEASURED. No new scheduled jobs, third-party executables, API costs, World PR or game engine.

## New Chat / V9 current work order

Read [V9 EXECUTION BRIEF](docs/V9_EXECUTION_BRIEF_RU.md), [cross-chat recovery](docs/RECOVERY_ANY_CHAT_RU.md) and [VERIFIED capability registry](catalog/active_capabilities.json). V9 artistic improvements are NOT IMPLEMENTED; V8 autotile and spritesheet adapters are lab-only. Current checkpoint in [LIVE_STATUS](LIVE_STATUS.json); owner verdict UNSET and 50/50 actual minutes UNMEASURED. Re-check exact V8(1) Library SHA before work.

## Animation Tech Lab A1 — 2026-10-13 (isolated V9 runtime, **NOT** full upstream engines)

The [reproducible animation adapter](scripts/animation-lab-v1.js), [exact pinned experiment](experiments/animation-tech-lab-v1.json), [local Chromium benchmark](evidence/animation-tech-lab-v1-browser.json), and [CI contract](tests/test_animation_lab_v1.py) are in Lab. Full original user-owned game ZIP with animation is stored in ChatGPT Library at `/World Server/Graphics Reference/GRAPHICS-DEMO-001-v9-animation-lab-a1.zip`, SHA256 `58d72dc5e044862fd708d0e7becef0b21c3de11997300e3b1d6d6946b80446eb`. GIF proof: `/World Server/Graphics Reference/GRAPHICS-DEMO-001-v9-animation-proof.gif`. Original knight bob + two-segment arm rig and smoke/leaf/fire/water particles were observed in Chromium (44/44 assets, zero JS errors). Median desktop cost rose from 1.112 to 1.228 ms, mobile-size 0.760 to 0.776 ms; physical iPhone11 untested.

Downloaded MIT source references: Tween.js `84a27a74` full Windows archive, DragonBonesJS `64b6c69a` and Pixi Particle Emitter `0fffdd9d` selected reference modules only; these **have NOT been loaded into the actual game**. Adapter is original, no PixiJS or DragonBones runtime. **Parallel V9 house-art work may be newer**, so do not overwrite it with this ZIP; rebase animation *module* onto freshly tested V9 candidate. World Server production unchanged; 50/50 actual work minutes not measured; user PASS/FAIL null.
