"""Untrusted candidate runner. It cannot approve its own policy or its own outputs."""
import argparse
import hashlib
import json
from pathlib import Path
from scorer import evaluate

HERE = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def produce(output):
    policy = json.loads((HERE / "policy.json").read_text())
    fixtures = json.loads((HERE / "fixtures.json").read_text())
    outcome = {name: evaluate(fixtures["cases"], fixtures[name], policy)
               for name in ("baseline", "candidate")}
    manifest = {"schema": "mosaic-edd-ch02-run-v2", "policy_id": policy["id"],
                "hashes": {name: digest(HERE / file) for name, file in
                           (("policy", "policy.json"), ("fixtures", "fixtures.json"),
                            ("runner", "runner.py"), ("scorer", "scorer.py"))},
                "outcomes": outcome,
                "scope": "deterministic synthetic fixtures; NOT production safety evidence"}
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Non-overwriting creation ONLY. We do not call this immutable storage.
    with target.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, sort_keys=True, indent=2)
        handle.write("\n")
    return outcome

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--output", required=True)
    args = cli.parse_args()
    print(json.dumps(produce(args.output), sort_keys=True))
