import hashlib
import json
import tempfile
import unittest
from pathlib import Path

# All fixtures and thresholds are synthetic.
TRUSTED = {
    "cases": ["p1", "p2"] + [f"n{i}" for i in range(1, 9)],
    "protected": ["p1", "p2"],
    "baseline": {
        "p1": 1, "p2": 1,
        "n1": 1, "n2": 1, "n3": 1, "n4": 1, "n5": 1,
        "n6": 0, "n7": 0, "n8": 0,
    },
    "policy": {"require_all_protected": True,
               "candidate_not_below_baseline": True},
}
CANDIDATE = {
    "p1": 1, "p2": 0,
    "n1": 1, "n2": 1, "n3": 1, "n4": 1, "n5": 1,
    "n6": 1, "n7": 1, "n8": 0,
}

def encoded(value):
    return json.dumps(value, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")

def digest(data):
    return hashlib.sha256(data).hexdigest()

# In production this expected digest must come from an independently
# controlled release of the evaluator, not from the candidate branch.
EXPECTED_TRUSTED_DIGEST = digest(encoded(TRUSTED))

def make_fixtures(root):
    root = Path(root)
    trusted = root / "trusted.json"
    bundle = root / "candidate"
    bundle.mkdir()
    trusted.write_bytes(encoded(TRUSTED))
    (bundle / "results.json").write_bytes(encoded(CANDIDATE))
    return trusted, bundle

def gate(trusted_path, bundle):
    trusted_path, bundle = Path(trusted_path), Path(bundle)
    raw = trusted_path.read_bytes()
    if digest(raw) != EXPECTED_TRUSTED_DIGEST:
        raise ValueError("trusted fixture digest mismatch")
    rules = json.loads(raw)

    # An illustrative allow-list, not an OS security sandbox.
    entries = list(bundle.iterdir())
    if len(entries) != 1 or entries[0].name != "results.json":
        raise ValueError("candidate bundle contains unexpected files")
    result_path = entries[0]
    if result_path.is_symlink() or not result_path.is_file():
        raise ValueError("candidate result must be a regular file")
    candidate = json.loads(result_path.read_text(encoding="utf-8"))

    cases = rules["cases"]
    baseline = rules["baseline"]
    if not isinstance(candidate, dict) or set(candidate) != set(cases):
        raise ValueError("candidate must report exactly the trusted cases")
    if any(type(candidate[k]) is not int or candidate[k] not in (0, 1)
           for k in cases):
        raise ValueError("case results must be integer 0 or 1")

    baseline_passes = sum(baseline[k] for k in cases)
    candidate_passes = sum(candidate[k] for k in cases)
    protected = rules["protected"]
    protected_passes = sum(candidate[k] for k in protected)

    policy = rules["policy"]
    protected_ok = (
        not policy["require_all_protected"]
        or protected_passes == len(protected)
    )
    average_ok = (
        not policy["candidate_not_below_baseline"]
        or candidate_passes >= baseline_passes
    )
    return {
        "baseline": f"{baseline_passes}/{len(cases)}",
        "candidate": f"{candidate_passes}/{len(cases)}",
        "protected": f"{protected_passes}/{len(protected)}",
        "decision": "PASS" if protected_ok and average_ok else "BLOCK",
        "trusted_digest": digest(raw),
    }

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.trusted, self.bundle = make_fixtures(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_improved_average_does_not_override_protected_failure(self):
        report = gate(self.trusted, self.bundle)
        self.assertEqual(report["baseline"], "7/10")
        self.assertEqual(report["candidate"], "8/10")
        self.assertEqual(report["protected"], "1/2")
        self.assertEqual(report["decision"], "BLOCK")

    def test_candidate_cannot_supply_policy(self):
        (self.bundle / "policy.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unexpected files"):
            gate(self.trusted, self.bundle)

    def test_trusted_case_or_policy_tampering_is_detected(self):
        altered = json.loads(self.trusted.read_text(encoding="utf-8"))
        altered["protected"] = ["p1"]
        self.trusted.write_bytes(encoded(altered))
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            gate(self.trusted, self.bundle)

    def test_passing_candidate_can_be_promoted(self):
        passing = dict(CANDIDATE)
        passing["p2"] = 1
        (self.bundle / "results.json").write_bytes(encoded(passing))
        self.assertEqual(gate(self.trusted, self.bundle)["decision"], "PASS")

    def test_missing_case_is_not_a_pass(self):
        incomplete = dict(CANDIDATE)
        del incomplete["p2"]
        (self.bundle / "results.json").write_bytes(encoded(incomplete))
        with self.assertRaisesRegex(ValueError, "exactly"):
            gate(self.trusted, self.bundle)

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as directory:
        trusted_path, candidate_bundle = make_fixtures(directory)
        report = gate(trusted_path, candidate_bundle)
        print("Dry-run report:", json.dumps(report, sort_keys=True),
              flush=True)
    unittest.main(verbosity=2)
