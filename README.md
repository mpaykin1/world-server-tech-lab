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
