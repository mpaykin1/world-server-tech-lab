#!/usr/bin/env python3
"""Record a material, evidenced state change before committing it to GitHub."""
import argparse
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "LIVE_STATUS.json"
HISTORY = ROOT / "checkpoints/history.jsonl"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--phase", required=True, choices=[
        "RECOVERY_INFRASTRUCTURE", "EXPERIMENTING", "AWAITING_CI",
        "INTEGRATION_REVIEW", "READY_FOR_USER", "PAUSED"])
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--active-experiment", action="append", default=[])
    args = parser.parse_args()
    if not (args.evidence.startswith("https://github.com/") or args.evidence.startswith("experiments/")):
        parser.error("evidence must be an exact GitHub reference or experiment path")
    state = json.loads(STATUS.read_text(encoding="utf-8"))
    if state["owner_decision"] is not None:
        parser.error("owner decision state requires separate explicit owner-authorized workflow")
    stamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state.update(checkpoint=state["checkpoint"] + 1, updated_at_utc=stamp,
                 phase=args.phase, blockers=args.blocker, next_action=args.next_action,
                 active_experiments=args.active_experiment)
    event = {"checkpoint": state["checkpoint"], "updated_at_utc": stamp,
             "event": args.event, "evidence": args.evidence, "owner_decision": None}
    STATUS.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with HISTORY.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    print("Checkpoint", state["checkpoint"], "recorded; commit BOTH files with substantive changes.")

if __name__ == "__main__":
    main()
