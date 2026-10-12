#!/usr/bin/env python3
"""Fail-closed, offline resume checkpoint verification. No GitHub/API polling."""
import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")
PHASES = {"RECOVERY_INFRASTRUCTURE", "EXPERIMENTING", "AWAITING_CI",
          "INTEGRATION_REVIEW", "READY_FOR_USER", "PAUSED"}


def validate(root=ROOT, now=None):
    errors = []
    try:
        status = json.loads((root / "LIVE_STATUS.json").read_text(encoding="utf-8"))
        history = [json.loads(line) for line in (root / "checkpoints/history.jsonl")
                   .read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, ValueError) as exc:
        return ["checkpoint missing or malformed: " + str(exc)]
    if status.get("schema_version") != 1 or status.get("phase") not in PHASES:
        errors.append("unsupported checkpoint schema/phase")
    if not isinstance(status.get("checkpoint"), int) or status["checkpoint"] < 1:
        errors.append("checkpoint must be a positive integer")
    if not history or history[-1].get("checkpoint") != status.get("checkpoint"):
        errors.append("latest history entry and LIVE_STATUS checkpoint differ")
    if history and history[-1].get("updated_at_utc") != status.get("updated_at_utc"):
        errors.append("latest history timestamp does not match LIVE_STATUS")
    if any(e.get("checkpoint") != i + 1 for i, e in enumerate(history)):
        errors.append("history checkpoint sequence is not continuous")
    if len(history) != status.get("checkpoint"):
        errors.append("history length and checkpoint sequence differ")
    try:
        stamp = dt.datetime.fromisoformat(status["updated_at_utc"].replace("Z", "+00:00"))
        now = now or dt.datetime.now(dt.timezone.utc)
        age = (now - stamp).total_seconds()
        if age < -600:
            errors.append("checkpoint timestamp is in the future")
        if age > 14 * 86400 and status.get("phase") != "PAUSED":
            errors.append("ACTIVE_CHECKPOINT_STALE: older than 14 days")
    except (ValueError, KeyError, TypeError):
        errors.append("invalid checkpoint timestamp")
    baseline = status.get("baseline") or {}
    if not all(SHA.fullmatch(str(baseline.get(k, ""))) for k in
               ("lab_main_sha", "world_master_sha", "upstream_opengame_sha")):
        errors.append("invalid exact baseline SHA")
    if status.get("owner_decision") is not None:
        errors.append("owner verdict may be set only after the owner's explicit decision")
    split = status.get("lane_policy") or {}
    if (split.get("GRAPHICS"), split.get("CLEAN_SERVER")) != (50, 50):
        errors.append("50/50 allocation contract changed")
    if split.get("new_scheduled_jobs") != 0 or split.get("world_server_runtime_changes") is not False:
        errors.append("isolation contract violated")
    if not isinstance(status.get("blockers"), list) or not status.get("next_action"):
        errors.append("blockers / next action must be explicit")
    experiments = status.get("active_experiments")
    if not isinstance(experiments, list) or len(experiments) != len(set(experiments)):
        errors.append("invalid active_experiments")
    else:
        for experiment in experiments:
            if not (root / "experiments" / (str(experiment) + ".json")).is_file():
                errors.append("active experiment missing: " + str(experiment))
    return errors


def check_material_changes():
    """Same-commit checkpoint gate; local checkout must have at least parent commit."""
    try:
        paths = subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            cwd=ROOT, text=True, timeout=8).splitlines()
    except (subprocess.CalledProcessError, OSError, subprocess.TimeoutExpired) as exc:
        return ["cannot prove changed file list: " + str(exc)]
    substantive = any(p.startswith(("experiments/", "catalog/", "scripts/opengame_")) for p in paths)
    if substantive and not {"LIVE_STATUS.json", "checkpoints/history.jsonl"}.issubset(paths):
        return ["material experiment/catalog change requires same-commit status and history"]
    return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--changes", action="store_true", help="validate current commit delta")
    args = parser.parse_args()
    errors = validate() + (check_material_changes() if args.changes else [])
    for error in errors:
        print("ERROR:", error)
    if errors:
        raise SystemExit(1)
    print("LAB_RESUME_CHECKPOINT_OK")
