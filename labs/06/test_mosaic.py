"""Independent Chapter 06 fail-closed regression tests."""
import importlib.util
import math
import unittest
from pathlib import Path

p = Path(__file__).resolve().with_name("mosaic_judge.py")
spec = importlib.util.spec_from_file_location("mosaic_judge_ch06", p)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class JudgeAdapterBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.good = lab.fixture_judge("supported")

    def test_unhashable_label_list_and_dict_never_raise(self):
        for value in (["pass"], {"value": "pass"}, set(["pass"])):
            with self.subTest(value=str(value)):
                row = self.good.copy(); row["label"] = value
                self.assertEqual(lab.validated_decision(row, lab.EVIDENCE), "escalate")

    def test_unhashable_evidence_identifier_never_raises(self):
        for value in (["P1"], {"id": "P1"}, set(["P1"])):
            with self.subTest(value=str(value)):
                row = self.good.copy(); row["evidence_id"] = value
                self.assertEqual(lab.validated_decision(row, lab.EVIDENCE), "escalate")

    def test_malformed_quotes_confidence_and_evidence(self):
        for field, value in (("quote", ["may request a review"]),
                             ("confidence", [0.9]), ("confidence", float("inf")),
                             ("confidence", True), ("confidence", -0.1),
                             ("confidence", 10**1000),
                             ("label", None)):
            with self.subTest(field=field, value=str(value)):
                row = self.good.copy(); row[field] = value
                self.assertEqual(lab.validated_decision(row, lab.EVIDENCE), "escalate")
        for evidence in ([], None, {"P1": ["may request a review"]},
                         {False: "may request a review"}):
            with self.subTest(evidence=str(evidence)):
                self.assertEqual(lab.validated_decision(self.good, evidence), "escalate")

    def test_missing_schema_and_untrusted_safety_flag(self):
        row = self.good.copy(); del row["confidence"]
        self.assertEqual(lab.validated_decision(row, lab.EVIDENCE), "escalate")
        self.assertEqual(lab.validated_decision(self.good, lab.EVIDENCE,
                                                safety_critical=[False]), "escalate")

    def test_valid_negative_routes_fail_but_uncertainty_escalates(self):
        failed = {"label": "fail", "confidence": 0.0,
                  "evidence_id": "", "quote": ""}
        self.assertEqual(lab.validated_decision(failed, lab.EVIDENCE), "fail")
        failed["label"] = "uncertain"
        self.assertEqual(lab.validated_decision(failed, lab.EVIDENCE), "escalate")

    def test_malformed_calibration_items_reject_without_exception(self):
        negatives = ["unacceptable"] * 40
        for labels,decisions in ((negatives, [["pass"]]+["fail"]*39),
                                  ([{"label":"unacceptable"}]+negatives[1:], ["fail"]*40),
                                  (None, ["fail"]*40),
                                  (negatives, None),
                                  (negatives, [False]+["fail"]*39)):
            with self.subTest(labels=str(labels)[:60],decisions=str(decisions)[:60]):
                self.assertFalse(lab.calibration_gate(labels, decisions))

    def test_safety_stop_is_not_judge_calibration_label(self):
        self.assertEqual(lab.release_route(self.good, lab.EVIDENCE,
                         answer_text="An extension is guaranteed."), "stop")
        self.assertEqual(lab.release_route(self.good, lab.EVIDENCE,
                         safety_critical=True), "escalate")
        self.assertFalse(lab.calibration_gate(["unacceptable"]*40,
                         ["stop"]*40))
        self.assertFalse(lab.safety_invariant_violation(
            "An extension is guaranteed.", {"P1": "Different policy"}))
        self.assertFalse(lab.safety_invariant_violation(
            ["An extension is guaranteed."], lab.EVIDENCE))

    def test_negative_only_calibration_is_not_full_release_certification(self):
        negatives = ["unacceptable"]*40
        self.assertTrue(lab.calibration_gate(negatives,["fail"]*40))
        self.assertFalse(lab.calibration_gate(negatives,["pass"]*12+["fail"]*28))
        self.assertFalse(lab.calibration_gate([],[]))
        self.assertGreater(lab.wilson_upper(12,40),0.45)


if __name__ == "__main__":
    unittest.main()
