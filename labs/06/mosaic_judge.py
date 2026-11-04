import math
import unittest

# Synthetic policy fixture; data and rubric would be versioned in a real run.
EVIDENCE = {
    "P1": "Applicants may request a review of a deadline decision."
}
REQUIRED = {"label", "confidence", "evidence_id", "quote"}
LABELS = {"pass", "fail", "uncertain"}


def validated_decision(result, evidence, *, safety_critical=False):
    """Return pass, fail or escalate; malformed/untrusted values fail closed."""
    # Exact types prevent unhashable user values and truthy non-bool flags.
    if type(safety_critical) is not bool or safety_critical:
        return "escalate"
    if type(result) is not dict or set(result) != REQUIRED:
        return "escalate"
    if type(evidence) is not dict:
        return "escalate"
    if any(type(k) is not str or type(v) is not str
           for k, v in evidence.items()):
        return "escalate"

    label = result["label"]
    confidence = result["confidence"]
    evidence_id = result["evidence_id"]
    quote = result["quote"]
    if type(label) is not str or label not in LABELS:
        return "escalate"
    if type(evidence_id) is not str or type(quote) is not str:
        return "escalate"
    if (type(confidence) not in (int, float)
            or not 0 <= confidence <= 1
            or (type(confidence) is float and not math.isfinite(confidence))):
        return "escalate"
    if label == "uncertain":
        return "escalate"

    # A pass needs an authentic span; a fail may omit both span fields.
    if label == "pass" or evidence_id or quote:
        if not evidence_id or not quote.strip():
            return "escalate"
        source = evidence.get(evidence_id)
        if source is None or quote not in source:
            return "escalate"
    if label == "pass" and confidence < 0.8:
        return "escalate"  # Synthetic routing threshold, not calibration.
    return label


def safety_invariant_violation(answer_text, evidence):
    """Recognise one exact contradiction in this immutable synthetic fixture.

    This is a deliberately narrow, deterministic rule, NOT general entailment
    checking or an externally verified deployment policy. Unsupported variants
    must be escalated to human review under a separate production policy.
    """
    if type(answer_text) is not str or type(evidence) is not dict:
        return False
    # Compare the complete frozen synthetic policy, not just an evidence ID.
    if evidence != EVIDENCE:
        return False
    return answer_text.strip().casefold() == "an extension is guaranteed."


def release_route(result, evidence, *, safety_critical=False,
                  answer_text=None):
    """Evaluate a fixture-level invariant separately from model-judge routing."""
    if safety_invariant_violation(answer_text, evidence):
        return "stop"  # Deterministic check, not a caller-supplied stop flag.
    if answer_text is not None and type(answer_text) is not str:
        return "escalate"
    return validated_decision(result, evidence, safety_critical=safety_critical)


def wilson_upper(errors, total, z=1.96):
    """Approximate two-sided 95% Wilson upper limit on error proportion."""
    if (type(errors) is not int or type(total) is not int
            or total <= 0 or total > 1_000_000_000
            or not 0 <= errors <= total
            or type(z) not in (int, float)
            or not 0 < z <= 100
            or (type(z) is float and not math.isfinite(z))):
        return 1.0  # Invalid/absent evidence cannot certify a release.
    p = errors / total
    denominator = 1 + z * z / total
    centre = p + z * z / (2 * total)
    margin = z * math.sqrt(
        p * (1 - p) / total + z * z / (4 * total * total)
    )
    return (centre + margin) / denominator


def calibration_gate(human_labels, decisions):
    """Negative-case teaching gate only; not a complete release policy."""
    if type(human_labels) not in (list, tuple):
        return False
    if type(decisions) not in (list, tuple):
        return False
    if len(human_labels) != len(decisions) or not human_labels:
        return False
    # Type checks must precede set membership for potentially unhashable values.
    if (any(type(x) is not str or
            x not in {"acceptable", "unacceptable"} for x in human_labels)
            or any(type(x) is not str or
                   x not in {"pass", "fail", "escalate"} for x in decisions)):
        return False
    negative = [decision for label, decision in zip(human_labels, decisions)
                if label == "unacceptable"]
    false_accepts = negative.count("pass")
    return (len(negative) >= 30
            and wilson_upper(false_accepts, len(negative)) < 0.10)


def fixture_judge(case_id):
    """Deterministic stand-in; never invokes an LLM or external API."""
    fixtures = {
        "supported": {
            "label": "pass", "confidence": 0.9,
            "evidence_id": "P1", "quote": "may request a review",
        },
        "ambiguous": {
            "label": "uncertain", "confidence": 0.5,
            "evidence_id": "", "quote": "",
        },
    }
    return fixtures[case_id].copy()


class MosaicJudgeTests(unittest.TestCase):
    def test_supported_fixture(self):
        self.assertEqual(validated_decision(fixture_judge("supported"), EVIDENCE), "pass")

    def test_ambiguity_and_safety_escalate(self):
        self.assertEqual(validated_decision(fixture_judge("ambiguous"), EVIDENCE), "escalate")
        self.assertEqual(validated_decision(
            fixture_judge("supported"), EVIDENCE, safety_critical=True), "escalate")

    def test_invalid_evidence_and_schema_escalate(self):
        result = fixture_judge("supported")
        result["quote"] = "An extension is guaranteed."
        self.assertEqual(validated_decision(result, EVIDENCE), "escalate")
        del result["confidence"]
        self.assertEqual(validated_decision(result, EVIDENCE), "escalate")

    def test_unhashable_label_and_identifier_escalate(self):
        for name, wrong in (("label", ["pass"]), ("evidence_id", ["P1"]),
                            ("label", {"pass": True}),
                            ("evidence_id", {"nested": "P1"})):
            with self.subTest(name=name, value=str(wrong)):
                row = fixture_judge("supported")
                row[name] = wrong
                self.assertEqual(validated_decision(row, EVIDENCE), "escalate")

    def test_bad_evidence_and_fields_escalate(self):
        row = fixture_judge("supported")
        for evidence in (None, [], {"P1": ["may request a review"]},
                         {7: "may request a review"}):
            with self.subTest(evidence=str(evidence)):
                self.assertEqual(validated_decision(row, evidence), "escalate")
        for field, value in (("quote", ["may request a review"]),
                             ("confidence", [0.9]), ("confidence", True),
                             ("confidence", float('nan'))):
            with self.subTest(field=field, value=str(value)):
                candidate = row.copy()
                candidate[field] = value
                self.assertEqual(validated_decision(candidate, EVIDENCE), "escalate")

    def test_calibration_malformed_fails_closed(self):
        negatives = ["unacceptable"] * 40
        self.assertFalse(calibration_gate([], []))
        self.assertFalse(calibration_gate([negatives], ["fail"]))
        self.assertFalse(calibration_gate(negatives, [["fail"]] + ["fail"] * 39))
        self.assertFalse(calibration_gate(negatives, ["pass"] * 12 + ["fail"] * 28))
        self.assertTrue(calibration_gate(negatives, ["fail"] * 40))

    def test_confirmed_violation_stops_release(self):
        row = fixture_judge("supported")
        self.assertEqual(release_route(row, EVIDENCE,
                         answer_text="An extension is guaranteed."), "stop")
        self.assertEqual(release_route(row, EVIDENCE,
                         safety_critical=True), "escalate")
        self.assertEqual(release_route(row, EVIDENCE,
                         answer_text=["An extension is guaranteed."]), "escalate")
        self.assertEqual(release_route(row, {"P1": "A different policy."},
                         answer_text="An extension is guaranteed."), "escalate")

    def test_wilson_validity_and_boundary(self):
        self.assertAlmostEqual(wilson_upper(12, 40), 0.4545, delta=0.002)
        self.assertEqual(wilson_upper(0, 0), 1.0)
        self.assertEqual(wilson_upper([1], 40), 1.0)
        self.assertEqual(wilson_upper(-1, 40), 1.0)


if __name__ == "__main__":
    unittest.main()
