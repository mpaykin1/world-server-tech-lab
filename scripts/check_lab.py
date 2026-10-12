#!/usr/bin/env python3
"""Cheap, offline structural checks; never calls an AI provider or touches production."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATUSES = {"NOT_TESTED", "RESEARCH_ONLY", "EXPERIMENTING", "READY_FOR_USER", "USER_PASS", "USER_FAIL"}


def check_experiment(record):
    errors = []
    status = record.get("status")
    decision = record.get("user_decision")
    if status not in ALLOWED_STATUSES:
        errors.append("unknown experiment status")
    if decision not in (None, "PASS", "FAIL"):
        errors.append("user_decision must be null, PASS or FAIL")
    if status in {"USER_PASS", "USER_FAIL"}:
        expected = "PASS" if status == "USER_PASS" else "FAIL"
        if decision != expected or not record.get("user_decision_source"):
            errors.append("user verdict requires matching decision and user evidence")
    if decision is None and record.get("analysis_commit"):
        errors.append("no success/failure analysis commit before user verdict")
    if status == "READY_FOR_USER":
        measure = record.get("measurement") or {}
        if measure.get("user_visibility_percent") is None or measure["user_visibility_percent"] <= 85:
            errors.append("test link gate: user visibility must be evidenced above 85%")
        if not measure.get("visibility_evidence") or not measure.get("reproducible_test_command"):
            errors.append("test link gate: evidence and reproducible checks required")
    return errors


def validate(root=ROOT):
    errors = []
    candidates = json.loads((root / "catalog/candidates.json").read_text(encoding="utf-8"))
    ids = set()
    for candidate in candidates["candidates"]:
        if candidate["id"] in ids:
            errors.append("duplicate catalog id: " + candidate["id"])
        ids.add(candidate["id"])
        if not candidate["url"].startswith("https://github.com/"):
            errors.append("invalid candidate source URL")
        if candidate.get("license_verified") and not candidate.get("upstream_sha"):
            errors.append("license verification missing upstream SHA")
    for experiment in sorted((root / "experiments").glob("*.json")):
        record = json.loads(experiment.read_text(encoding="utf-8"))
        errors.extend(str(experiment.name) + ": " + err for err in check_experiment(record))
    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print("ERROR:", failure)
        raise SystemExit(1)
    print("LAB_STRUCTURE_OK")
