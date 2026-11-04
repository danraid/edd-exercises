"""Mosaic: versioned, deterministic fixture-level evaluation and rollback lab.

No model access, network requests, personal data, actual deployments or real secrets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path

from scorer import SCORER_ID, score_case

VERSION = "mosaic-eval-01"
BASELINE_ID = "mosaic-fixture-baseline-01"
POLICY_ID = "synthetic-policy-01"
BASELINE_ADAPTER = "fixed-synthetic-response-fixture-v1"

CASES = [
    {"id": "S1", "question": "Where is the form?", "answer": "At the library.", "source": "DOC-01"},
    {"id": "S2", "question": "When is the office open?", "answer": "On Monday.", "source": "DOC-02"},
    {"id": "S3", "question": "Where is the advice desk?", "answer": "At the town hall.", "source": "DOC-03"},
    {"id": "S4", "question": "¿Dónde está el formulario?", "answer": "En la biblioteca.", "source": "DOC-04"},
]
RESPONSES = {
    "S1": {"answer": "At the library.", "source": "DOC-01"},
    "S2": {"answer": "On Monday.", "source": "DOC-02"},
    "S3": {"answer": "At the town hall.", "source": "DOC-99"},
    "S4": {"answer": "En la biblioteca.", "source": "DOC-04"},
}
POLICY = {
    "id": POLICY_ID,
    "check_pass_percent_min": 80,
    "scenario_pass_percent_min": 90,
    "safety_violations_max": 0,
}


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(canonical_bytes(value))
    tmp.replace(path)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def valid_id(value):
    return isinstance(value, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{3,70}", value) is not None


def validate_fixtures(cases, responses):
    if not isinstance(cases, list) or not isinstance(responses, dict):
        raise ValueError("Invalid cases or responses")
    ids = [case.get("id") for case in cases]
    if (not ids or len(set(ids)) != len(ids) or not all(isinstance(x, str) and x.isalnum() for x in ids)
            or set(ids) != set(responses)):
        raise ValueError("Invalid case IDs or response mapping")
    if any(not isinstance(responses[i], dict) or "answer" not in responses[i]
           or "source" not in responses[i] for i in ids):
        raise ValueError("Response is missing required fields")


def baseline_file(root, baseline_id):
    if not valid_id(baseline_id):
        raise ValueError("Invalid baseline ID")
    return root / "baselines" / (baseline_id + ".json")


def registered_baseline(root, baseline_id):
    registry = read_json(root / "baselines" / "index.json")
    path = baseline_file(root, baseline_id)
    if baseline_id not in registry or not path.is_file():
        raise ValueError("Unknown baseline")
    obj = read_json(path)
    if obj.get("id") != baseline_id or obj.get("adapter") != BASELINE_ADAPTER:
        raise ValueError("Baseline metadata mismatch")
    if registry[baseline_id] != sha256_file(path):
        raise ValueError("Baseline fingerprint mismatch; fixture may have been edited")
    return obj, registry[baseline_id]


def initialise(root):
    root = Path(root)
    if (root / "release_state.json").exists():
        raise ValueError("Already initialised: refusing to overwrite release history")
    base = {"id": BASELINE_ID, "adapter": BASELINE_ADAPTER,
            "model_settings": {"mode": "fixed-fixture", "sampling": "none"}, "responses": RESPONSES}
    write_json(root / "cases.json", CASES)
    write_json(root / "policy.json", POLICY)
    write_json(baseline_file(root, BASELINE_ID), base)
    write_json(root / "baselines" / "index.json", {BASELINE_ID: sha256_json(base)})
    write_json(root / "release_state.json", {
        "active": BASELINE_ID,
        "previous": None,
        "revision": 0,
        "history": [{"event": "INITIALISE", "baseline": BASELINE_ID}],
        "cases_sha256": sha256_file(root / "cases.json"),
        "policy_sha256": sha256_file(root / "policy.json"),
    })
    return root


def revision():
    # If the lab is not inside a Git checkout, say so explicitly.
    repo = Path(__file__).resolve().parents[2]
    try:
        result = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                capture_output=True, text=True, timeout=3, check=True)
        return result.stdout.strip() or "UNVERSIONED"
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "UNVERSIONED"


def provenance(root, obj, pinned, state):
    # Baseline fingerprint is *independent* of runner/scorer source files.
    return {
        "baseline_id": obj["id"], "baseline_manifest_sha256": pinned,
        "dataset_sha256": sha256_file(root / "cases.json"),
        "scorer_id": SCORER_ID,
        "scorer_source_sha256": sha256_file(Path(__file__).with_name("scorer.py")),
        "policy_id": POLICY_ID, "policy_sha256": sha256_file(root / "policy.json"),
        "runner_source_sha256": sha256_file(Path(__file__).resolve()),
        "source_control_revision": revision(),
        "runtime": {"python": platform.python_version(),
                    "implementation": platform.python_implementation(),
                    "platform": platform.platform()},
        "release_revision": state["revision"],
    }


def evaluate(root, obj, pinned, state, save=False):
    cases = read_json(root / "cases.json")
    policy = read_json(root / "policy.json")
    if policy.get("id") != POLICY_ID:
        raise ValueError("Policy version mismatch")
    if (sha256_file(root / "cases.json") != state["cases_sha256"] or
            sha256_file(root / "policy.json") != state["policy_sha256"]):
        raise ValueError("Case/policy fingerprint changed without versioned release")
    responses = obj["responses"]
    validate_fixtures(cases, responses)
    p = provenance(root, obj, pinned, state)
    outcomes = []
    for case in sorted(cases, key=lambda item: item["id"]):
        response = responses[case["id"]]
        checks, safe = score_case(case, response)
        trace_link = "traces/" + case["id"] + ".json"
        trace = {"case": case, "response": response, "checks": checks, "safe": safe,
                 "provenance": p}
        if save:
            write_json(root / trace_link, trace)
        outcomes.append({"id": case["id"], "checks": checks,
                         "scenario_pass": all(checks.values()), "safe": safe,
                         "trace": trace_link})
    checks_passed = sum(sum(x["checks"].values()) for x in outcomes)
    checks_total = 2 * len(outcomes)
    scenarios_passed = sum(x["scenario_pass"] for x in outcomes)
    violations = sum(not x["safe"] for x in outcomes)
    gates = {
        "checks": checks_passed * 100 >= policy["check_pass_percent_min"] * checks_total,
        "scenarios": scenarios_passed * 100 >= policy["scenario_pass_percent_min"] * len(outcomes),
        "safety": violations <= policy["safety_violations_max"],
    }
    report = {"eval_version": VERSION,
              "evaluation_scope": "synthetic fixture-level evaluation; not a live or production system",
              "baseline": obj["id"], "scorer": SCORER_ID, "policy": POLICY_ID,
              "provenance": p,
              "execution": "fixed synthetic fixtures; no model sampling, retrieval or intermediate tool actions",
              "thresholds": policy,
              "counts": {"checks_passed": checks_passed, "checks_total": checks_total,
                         "scenarios_passed": scenarios_passed, "scenarios_total": len(outcomes),
                         "safety_violations": violations},
              "gates": gates, "decision": "GO" if all(gates.values()) else "STOP",
              "outcomes": outcomes}
    if save:
        write_json(root / "report.json", report)
    return report


def run(root):
    root = Path(root)
    state = read_json(root / "release_state.json")
    obj, fingerprint = registered_baseline(root, state["active"])
    return evaluate(root, obj, fingerprint, state, save=True)


def promote(root, candidate_path):
    """Simulate a release: only an evaluated GO candidate can be promoted."""
    root = Path(root)
    candidate = read_json(Path(candidate_path))
    cid = candidate.get("id")
    if not valid_id(cid) or cid == BASELINE_ID or candidate.get("adapter") != BASELINE_ADAPTER:
        raise ValueError("Invalid candidate manifest")
    if (root / "baselines" / (cid + ".json")).exists():
        raise ValueError("Candidate identifier already registered")
    state = read_json(root / "release_state.json")
    validate_fixtures(read_json(root / "cases.json"), candidate.get("responses"))
    digest = sha256_json(candidate)
    test = evaluate(root, candidate, digest, state, save=False)
    if test["decision"] != "GO":
        raise ValueError("Candidate did not pass release gates")
    write_json(baseline_file(root, cid), candidate)
    index = read_json(root / "baselines" / "index.json")
    index[cid] = digest
    write_json(root / "baselines" / "index.json", index)
    state["previous"] = state["active"]
    state["active"] = cid
    state["revision"] += 1
    state["history"].append({"event": "PROMOTE", "baseline": cid,
                             "previous": state["previous"], "sha256": digest})
    write_json(root / "release_state.json", state)
    return run(root)


def rollback(root):
    """Preflight previous baseline before changing active state.

    Guarantees only fixture-level, single-process preflight safety; not a
    crash-atomic deployment transaction or restoration of external resources.
    """
    root = Path(root)
    state_path = root / "release_state.json"
    state = read_json(state_path)
    previous = state.get("previous")
    if not previous:
        raise ValueError("No previous release to restore")
    restored, pinned = registered_baseline(root, previous)
    next_state = json.loads(json.dumps(state))
    prior = state["active"]
    next_state["active"] = previous
    next_state["previous"] = None
    next_state["revision"] += 1
    next_state["history"].append({"event": "ROLLBACK", "from": prior,
                                "to": previous, "verified_sha256": pinned})
    # Do not mutate the active release pointer until the candidate restored
    # evaluation has passed all checks in-memory.
    checked = evaluate(root, restored, pinned, next_state, save=False)
    if (checked["baseline"] != previous or
            checked["provenance"]["baseline_manifest_sha256"] != pinned):
        raise RuntimeError("Rollback preflight failed")
    staged = []
    cases_by_id = {x["id"]: x for x in read_json(root / "cases.json")}
    for row in checked["outcomes"]:
        case = cases_by_id[row["id"]]
        response = restored["responses"][row["id"]]
        trace = {"case": case, "response": response, "checks": row["checks"],
                 "safe": row["safe"], "provenance": checked["provenance"]}
        staged.append((root / row["trace"], canonical_bytes(trace)))
    staged.append((root / "report.json", canonical_bytes(checked)))
    # Stage outputs before the active pointer commit. This is NOT an atomic
    # multi-file transaction; process crashes may leave partial output.
    for path, data in staged:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.with_name(path.name + ".rollback-stage").write_bytes(data)
    try:
        for path, _ in staged:
            path.with_name(path.name + ".rollback-stage").replace(path)
        write_json(state_path, next_state)
    finally:
        for path, _ in staged:
            path.with_name(path.name + ".rollback-stage").unlink(missing_ok=True)
    return checked


def cli():
    parser = argparse.ArgumentParser(description="Deterministic Mosaic laboratory")
    parser.add_argument("--root", type=Path, default=Path("mosaic_data"))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true")
    group.add_argument("--promote", type=Path, metavar="CANDIDATE_JSON")
    group.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    if args.init:
        initialise(args.root)
        print("Synthetic fixture baseline initialised.")
    elif args.promote:
        print("Simulated promotion:", promote(args.root, args.promote)["decision"])
    elif args.rollback:
        print("Verified synthetic rollback:", rollback(args.root)["decision"])
    else:
        print(run(args.root)["decision"], "report at", args.root / "report.json")


if __name__ == "__main__":
    cli()
