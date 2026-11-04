import hashlib
import json
import unittest

RUBRIC = {
    "version": "mosaic-grounding-1",
    "labels": ["supported", "unsupported", "uncertain"],
    "rule": "Every substantive claim must follow from the evidence."
}

# All passages, answers and reviewer events are synthetic.
CASES = [
    {"id": "s1", "passage": "The library opens on Monday.",
     "answer": "The library opens on Monday."},
    {"id": "s2", "passage": "The library opens on Monday.",
     "answer": "The library opens daily."},
    {"id": "s3", "passage": "The library opens on Monday.",
     "answer": "The library opens on Sunday."},
    {"id": "s4", "passage": "The library opens on Monday.",
     "answer": "It opens at the usual time."},
]

def event(case, reviewer, label, span, reason):
    return {"case": case, "reviewer": reviewer, "label": label,
            "span": span, "reason": reason}

ANNOTATIONS = [
    event("s1", "A", "supported", "opens on Monday", "Direct support."),
    event("s1", "B", "supported", "opens on Monday", "Direct support."),
    event("s2", "A", "unsupported", "opens on Monday", "Daily is broader."),
    event("s2", "B", "uncertain", "opens on Monday", "Opening days unclear."),
    event("s3", "A", "unsupported", "opens on Monday", "Sunday not stated."),
    event("s3", "B", "unsupported", "opens on Monday", "Sunday not stated."),
    event("s4", "A", "uncertain", "opens on Monday", "Time is unspecified."),
    event("s4", "B", "uncertain", "opens on Monday", "Usual time is unclear."),
]

# A separate event; it does not replace either original annotation.
ADJUDICATIONS = [
    event("s2", "C", "uncertain", "opens on Monday",
          "Escalate interpretation of the daily claim.")
]

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def validate_event(e, cases):
    if e["case"] not in cases:
        raise ValueError("Unknown case")
    if e["label"] not in RUBRIC["labels"]:
        raise ValueError("Unknown label")
    if not e["reason"].strip() or not e["span"].strip():
        raise ValueError("Reason and evidence span are required")
    if e["span"] not in cases[e["case"]]["passage"]:
        raise ValueError("Evidence span not found in passage")

def run(cases_list, annotations, adjudications):
    cases = {c["id"]: c for c in cases_list}
    if len(cases) != len(cases_list):
        raise ValueError("Duplicate case")

    pairs = {cid: [] for cid in cases}
    for e in annotations:
        validate_event(e, cases)
        pairs[e["case"]].append(e)

    adj = {}
    for e in adjudications:
        validate_event(e, cases)
        if e["reviewer"] != "C":
            raise ValueError("Only adjudicator C can submit adjudication")
        if e["case"] in adj:
            raise ValueError("Duplicate adjudication")
        adj[e["case"]] = e

    decisions = {}
    agreements = 0
    for cid, pair in pairs.items():
        if len(pair) != 2 or {e["reviewer"] for e in pair} != {"A", "B"}:
            raise ValueError("Each case needs one label from A and B")
        labels = [e["label"] for e in pair]
        # An adjudication is meaningful only for a disagreement or an unresolved
        # matching uncertain label, never for two agreeing decisive reviewers.
        if cid in adj and labels[0] == labels[1] and labels[0] != "uncertain":
            raise ValueError("Cannot adjudicate an already-agreed decisive label")
        if labels[0] == labels[1]:
            agreements += 1
        if labels[0] == labels[1] and labels[0] != "uncertain":
            decisions[cid] = {"status": "accepted", "label": labels[0]}
        elif cid in adj and adj[cid]["label"] != "uncertain":
            decisions[cid] = {"status": "adjudicated",
                              "label": adj[cid]["label"]}
        else:
            decisions[cid] = {"status": "unresolved", "label": None}

    inputs = {"rubric": RUBRIC, "cases": cases_list,
              "annotations": annotations, "adjudications": adjudications}
    return {
        "input_sha256": digest(inputs),
        "inputs": inputs,
        "agreement": {"matched_cases": agreements, "total_cases": len(cases)},
        "decisions": decisions,
    }

class LabTests(unittest.TestCase):
    def test_decisions_and_agreement(self):
        result = run(CASES, ANNOTATIONS, ADJUDICATIONS)
        self.assertEqual(result["agreement"],
                         {"matched_cases": 3, "total_cases": 4})
        self.assertEqual(result["decisions"]["s1"]["label"], "supported")
        self.assertEqual(result["decisions"]["s3"]["label"], "unsupported")
        self.assertEqual(result["decisions"]["s2"]["status"], "unresolved")
        self.assertEqual(result["decisions"]["s4"]["status"], "unresolved")
        self.assertEqual(len(result["inputs"]["annotations"]), 8)

    def test_bad_evidence_is_rejected(self):
        bad = [dict(e) for e in ANNOTATIONS]
        bad[0]["span"] = "not in the passage"
        with self.assertRaises(ValueError):
            run(CASES, bad, ADJUDICATIONS)

    def test_changed_input_changes_hash(self):
        changed = [dict(c) for c in CASES]
        changed[0]["answer"] = "Changed answer."
        original = run(CASES, ANNOTATIONS, ADJUDICATIONS)
        revised = run(changed, ANNOTATIONS, ADJUDICATIONS)
        self.assertNotEqual(original["input_sha256"], revised["input_sha256"])

    def test_agreed_decision_cannot_be_adjudicated(self):
        illegal = [event("s1", "C", "unsupported", "opens on Monday",
                         "Attempt to overwrite already agreed label.")]
        with self.assertRaises(ValueError):
            run(CASES, ANNOTATIONS, illegal)

    def test_resolved_disagreement_retains_original_annotations(self):
        resolved = [event("s2", "C", "unsupported", "opens on Monday",
                          "The cited Monday statement does not entail daily opening.")]
        outcome = run(CASES, ANNOTATIONS, resolved)
        self.assertEqual(outcome["decisions"]["s2"],
                         {"status": "adjudicated", "label": "unsupported"})
        self.assertEqual(len([a for a in outcome["inputs"]["annotations"]
                              if a["case"] == "s2"]), 2)
        self.assertEqual([a["label"] for a in outcome["inputs"]["annotations"]
                          if a["case"] == "s2"], ["unsupported", "uncertain"])

    def test_missing_second_reviewer_fails(self):
        with self.assertRaises(ValueError):
            run(CASES, ANNOTATIONS[:-1], ADJUDICATIONS)

if __name__ == "__main__":
    print(canonical(run(CASES, ANNOTATIONS, ADJUDICATIONS)))
    unittest.main()
