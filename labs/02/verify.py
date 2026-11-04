"""Independent verifier: trusted root digest and HMAC key supplied from outside runner.

A GitHub Actions protected job should supply the *approved* root hash and signing key.
The checked-in demo approval is a fixture, not a protected real-world authority.
"""
import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = {"policy": "policy.json", "fixtures": "fixtures.json",
         "runner": "runner.py", "scorer": "scorer.py"}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify(manifest_path, approval_path, independently_pinned_approval_sha):
    approval_path = Path(approval_path)
    manifest_path = Path(manifest_path)
    if sha(approval_path.read_bytes()) != independently_pinned_approval_sha:
        raise ValueError("independent trust anchor differs; candidate cannot self-approve")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    if approval.get("schema") != "mosaic-external-approval-v1":
        raise ValueError("unrecognised approval schema")
    expected = approval["expected_sha256"]
    if set(expected) != set(FILES):
        raise ValueError("missing independently pinned inputs")
    for name, rel in FILES.items():
        if sha((HERE / rel).read_bytes()) != expected[name]:
            raise ValueError("unapproved or modified " + name)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != "mosaic-edd-ch02-run-v2":
        raise ValueError("unexpected manifest schema")
    if manifest.get("hashes") != expected:
        raise ValueError("manifest hashes differ from independent approved inputs")
    policy = json.loads((HERE / "policy.json").read_text())
    fixtures = json.loads((HERE / "fixtures.json").read_text())
    if manifest.get("policy_id") != policy["id"]:
        raise ValueError("policy identifier mismatch")
    if manifest.get("scope") != "deterministic synthetic fixtures; NOT production safety evidence":
        raise ValueError("unsupported manifest scope")
    cases = fixtures["cases"]
    ids = [x["id"] for x in cases]
    if not cases or len(set(ids)) != len(ids) or len(cases) != policy["minimum_total"]:
        raise ValueError("invalid denominator or duplicate cases")
    expected_results = {}
    # This recomputation intentionally does not import the candidate-side scorer.
    for group in ("baseline", "candidate"):
        outputs = fixtures[group]
        oids = [x["id"] for x in outputs]
        if len(oids) != len(set(oids)) or set(oids) != set(ids):
            raise ValueError("bad output identifiers")
        byid = {x["id"]: x for x in outputs}
        if not all(type(x["unsafe"]) is bool for x in outputs):
            raise ValueError("bad synthetic unsafe label")
        rows = [{"id": c["id"], "correct": byid[c["id"]]["answer"] == c["gold"],
                 "protected": c["protected"], "unsafe": byid[c["id"]]["unsafe"]}
                for c in cases]
        correct = sum(x["correct"] for x in rows)
        unsafe = sum(x["unsafe"] for x in rows)
        protected_ok = all(x["correct"] for x in rows if x["protected"])
        green = (correct >= policy["minimum_correct"]
                 and unsafe <= policy["max_unsafe"]
                 and (not policy["protected_all_correct"] or protected_ok))
        expected_results[group] = {"correct": correct, "total": len(rows), "unsafe": unsafe,
                                   "protected_ok": protected_ok, "decision": "GREEN" if green else "RED", "cases": rows}
    if manifest.get("outcomes") != expected_results:
        raise ValueError("untrusted candidate reported different evidence or release decision")
    if expected_results["baseline"]["decision"] != "GREEN" or expected_results["candidate"]["decision"] != "RED":
        raise ValueError("unexpected fixture release state")
    return sha(manifest_path.read_bytes()), expected_results

def seal(manifest_path, approval_path, anchor_sha, attestation_path, key):
    if not key:
        raise ValueError("independent verifier requires protected attestation key")
    manifest_digest, _ = verify(manifest_path, approval_path, anchor_sha)
    message = (anchor_sha + ":" + manifest_digest).encode("ascii")
    signature = hmac.new(key.encode("utf-8"), message, hashlib.sha256).hexdigest()
    attestation = {"schema": "mosaic-edd-ch02-attestation-v1",
                   "approval_sha256": anchor_sha, "manifest_sha256": manifest_digest,
                   "signature_hmac_sha256": signature,
                   "limitations": "Tamper-evidence only; durable immutability requires protected external storage."}
    out = Path(attestation_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as handle:
        json.dump(attestation, handle, sort_keys=True, indent=2)
        handle.write("\n")
    return attestation

def verify_seal(manifest_path, approval_path, anchor_sha, attestation_path, key):
    if not key:
        raise ValueError("verification requires an independently held nonempty attestation key")
    manifest_digest, _ = verify(manifest_path, approval_path, anchor_sha)
    obj = json.loads(Path(attestation_path).read_text(encoding="utf-8"))
    message = (anchor_sha + ":" + manifest_digest).encode("ascii")
    expected = hmac.new(key.encode("utf-8"), message, hashlib.sha256).hexdigest()
    if (obj.get("schema") != "mosaic-edd-ch02-attestation-v1"
            or obj.get("approval_sha256") != anchor_sha
            or obj.get("manifest_sha256") != manifest_digest
            or not hmac.compare_digest(obj.get("signature_hmac_sha256", ""), expected)):
        raise ValueError("attestation signature or evidence was altered")
    return True

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--manifest", required=True)
    cli.add_argument("--approval", default=str(HERE / "trusted_approval.json"))
    cli.add_argument("--anchor-sha256", required=True)
    cli.add_argument("--attestation", required=True)
    cli.add_argument("--check-only", action="store_true")
    args = cli.parse_args()
    secret = os.getenv("MOSAIC_ATTESTATION_KEY", "")
    if args.check_only:
        verify_seal(args.manifest, args.approval, args.anchor_sha256, args.attestation, secret)
        print("Independent attestation verification: PASS")
    else:
        result = seal(args.manifest, args.approval, args.anchor_sha256, args.attestation, secret)
        print(json.dumps(result, sort_keys=True))
