"""Full deterministic acceptance suite for the Chapter 01 Mosaic lab."""
import json
import tempfile
import unittest
from pathlib import Path

import mosaic


class MosaicTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        mosaic.initialise(self.root)

    def test_fixed_fixture_counts_and_environment_reproducibility(self):
        report = mosaic.run(self.root)
        first_bytes = (self.root / "report.json").read_bytes()
        self.assertEqual(report, mosaic.run(self.root))
        self.assertEqual(first_bytes, (self.root / "report.json").read_bytes())
        self.assertEqual(report["evaluation_scope"],
                         "synthetic fixture-level evaluation; not a live or production system")
        self.assertEqual(report["baseline"], mosaic.BASELINE_ID)
        self.assertEqual(report["counts"]["checks_passed"], 7)
        self.assertEqual(report["counts"]["checks_total"], 8)
        self.assertEqual(report["counts"]["scenarios_passed"], 3)
        self.assertEqual(report["counts"]["scenarios_total"], 4)
        self.assertEqual(report["counts"]["safety_violations"], 0)
        self.assertEqual(report["decision"], "STOP")
        self.assertTrue(report["gates"]["checks"])
        self.assertFalse(report["gates"]["scenarios"])
        for field in ("source_control_revision", "scorer_source_sha256",
                      "baseline_manifest_sha256", "policy_sha256", "dataset_sha256", "runtime"):
            self.assertIn(field, report["provenance"])
        self.assertEqual(report["provenance"]["scorer_source_sha256"],
                         mosaic.sha256_file(Path(mosaic.__file__).with_name("scorer.py")))
        self.assertEqual(report["provenance"]["baseline_manifest_sha256"],
                         mosaic.sha256_file(mosaic.baseline_file(self.root, mosaic.BASELINE_ID)))
        self.assertNotEqual(report["provenance"]["scorer_source_sha256"],
                            report["provenance"]["baseline_manifest_sha256"])
        for row in report["outcomes"]:
            trace = mosaic.read_json(self.root / row["trace"])
            self.assertEqual(trace["provenance"], report["provenance"])

    def test_pinned_baseline_cannot_be_silently_rewritten(self):
        path = mosaic.baseline_file(self.root, mosaic.BASELINE_ID)
        item = mosaic.read_json(path)
        item["responses"]["S1"]["source"] = "DOC-TAMPER"
        mosaic.write_json(path, item)
        with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
            mosaic.run(self.root)

    def test_policy_and_dataset_mutation_require_versioning(self):
        cases = mosaic.read_json(self.root / "cases.json")
        cases[0]["question"] = "Edited question"
        mosaic.write_json(self.root / "cases.json", cases)
        with self.assertRaisesRegex(ValueError, "fingerprint changed"):
            mosaic.run(self.root)

    def test_unsafe_candidate_is_not_promoted(self):
        candidate = self.make_candidate("mosaic-fixture-unsafe-02")
        candidate["responses"]["S1"]["answer"] = "DISCLOSE_SECRET"
        path = self.root / "unsafe-candidate.json"
        mosaic.write_json(path, candidate)
        with self.assertRaisesRegex(ValueError, "did not pass release gates"):
            mosaic.promote(self.root, path)
        self.assertEqual(mosaic.read_json(self.root / "release_state.json")["active"], mosaic.BASELINE_ID)

    def make_candidate(self, cid="mosaic-fixture-candidate-02"):
        candidate = mosaic.read_json(mosaic.baseline_file(self.root, mosaic.BASELINE_ID))
        candidate["id"] = cid
        candidate["responses"]["S3"]["source"] = "DOC-03"
        return candidate

    def test_promote_then_rollback_to_verified_previous_fixture(self):
        baseline = mosaic.run(self.root)
        old_digest = baseline["provenance"]["baseline_manifest_sha256"]
        candidate = self.make_candidate()
        path = self.root / "candidate.json"
        mosaic.write_json(path, candidate)
        promoted = mosaic.promote(self.root, path)
        self.assertEqual(promoted["decision"], "GO")
        self.assertEqual(promoted["counts"]["checks_passed"], 8)
        self.assertEqual(promoted["counts"]["scenarios_passed"], 4)
        self.assertNotEqual(promoted["provenance"]["baseline_manifest_sha256"], old_digest)
        restored = mosaic.rollback(self.root)
        self.assertEqual(restored["decision"], "STOP")
        self.assertEqual(restored["baseline"], mosaic.BASELINE_ID)
        self.assertEqual(restored["counts"], baseline["counts"])
        self.assertEqual(restored["provenance"]["baseline_manifest_sha256"], old_digest)
        state = mosaic.read_json(self.root / "release_state.json")
        self.assertEqual([e["event"] for e in state["history"]],
                         ["INITIALISE", "PROMOTE", "ROLLBACK"])
        self.assertEqual(state["revision"], 2)
        with self.assertRaisesRegex(ValueError, "No previous release"):
            mosaic.rollback(self.root)

    def test_rollback_preflight_failure_preserves_active_release(self):
        candidate = self.make_candidate()
        path = self.root / "candidate.json"
        mosaic.write_json(path, candidate)
        mosaic.promote(self.root, path)
        state_before = (self.root / "release_state.json").read_bytes()
        old_path = mosaic.baseline_file(self.root, mosaic.BASELINE_ID)
        original = old_path.read_bytes()
        old_path.write_bytes(original + b"\n")
        with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
            mosaic.rollback(self.root)
        self.assertEqual(state_before, (self.root / "release_state.json").read_bytes())
        old_path.write_bytes(original)
        self.assertEqual(mosaic.rollback(self.root)["baseline"], mosaic.BASELINE_ID)

    def test_bad_case_ids_are_rejected(self):
        state = mosaic.read_json(self.root / "release_state.json")
        case_path = self.root / "cases.json"
        cases = mosaic.read_json(case_path)
        cases.append({"id": "../escape", "question": "?", "answer": "a", "source": "s"})
        mosaic.write_json(case_path, cases)
        state["cases_sha256"] = mosaic.sha256_file(case_path)
        mosaic.write_json(self.root / "release_state.json", state)
        with self.assertRaisesRegex(ValueError, "Invalid case IDs"):
            mosaic.run(self.root)


if __name__ == "__main__":
    unittest.main()
