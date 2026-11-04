"""Synthetic Mosaic support-scoring lab; Python 3.9+."""
import math
import sys
import unittest

VERSION = "mosaic-support-v1"
GOLD =      [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
BASELINE =  [1, 1, 1, 1, 0, 0, 1, 0, 0, 0]
CANDIDATE = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1]


def validate(gold, pred):
    if not gold or len(gold) != len(pred):
        raise ValueError("need equally sized, non-empty sequences")
    if any(x not in (0, 1) for x in list(gold) + list(pred)):
        raise ValueError("labels must be binary")


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def score(gold, pred):
    validate(gold, pred)
    tp = sum(g == 1 and p == 1 for g, p in zip(gold, pred))
    fp = sum(g == 0 and p == 1 for g, p in zip(gold, pred))
    fn = sum(g == 1 and p == 0 for g, p in zip(gold, pred))
    tn = sum(g == 0 and p == 0 for g, p in zip(gold, pred))
    n = len(gold)
    return {
        "version": VERSION, "unit": "synthetic task",
        "n": n, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "denominators": {"accuracy": n, "precision": tp + fp,
                         "recall": tp + fn, "f1": 2 * tp + fp + fn},
        "accuracy": ratio(tp + tn, n),
        "precision": ratio(tp, tp + fp),
        "recall": ratio(tp, tp + fn),
        "f1": ratio(2 * tp, 2 * tp + fp + fn),
    }


def paired_interval(gold, before, after, alpha=0.05):
    validate(gold, before)
    validate(gold, after)
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between zero and one")
    differences = [
        int(a == g) - int(b == g)
        for g, b, a in zip(gold, before, after)
    ]
    n = len(differences)
    delta = sum(differences) / n
    margin = math.sqrt(2 * math.log(2 / alpha) / n)
    return delta, max(-1.0, delta - margin), min(1.0, delta + margin)


class MetricTests(unittest.TestCase):
    def test_fixture_counts_and_metrics(self):
        b = score(GOLD, BASELINE)
        c = score(GOLD, CANDIDATE)
        self.assertEqual((b["tp"], b["fp"], b["fn"], b["tn"]),
                         (4, 1, 2, 3))
        self.assertEqual((c["tp"], c["fp"], c["fn"], c["tn"]),
                         (5, 1, 1, 3))
        self.assertAlmostEqual(b["precision"], 0.8)
        self.assertAlmostEqual(b["recall"], 2 / 3)
        self.assertAlmostEqual(c["accuracy"], 0.8)
        self.assertEqual(b["denominators"],
                         {"accuracy": 10, "precision": 5,
                          "recall": 6, "f1": 11})
        self.assertEqual(c["denominators"],
                         {"accuracy": 10, "precision": 6,
                          "recall": 6, "f1": 12})
        self.assertEqual(b["unit"], "synthetic task")

    def test_undefined_boundaries(self):
        result = score([0, 0], [0, 0])
        self.assertIsNone(result["precision"])
        self.assertIsNone(result["recall"])
        self.assertIsNone(result["f1"])

    def test_invalid_inputs(self):
        for gold, pred in [([], []), ([1], []), ([2], [1])]:
            with self.assertRaises(ValueError):
                score(gold, pred)

    def test_input_and_version_provenance(self):
        report = score(GOLD, CANDIDATE)
        self.assertEqual(report["version"], VERSION)
        self.assertEqual(report["n"], len(GOLD))
        self.assertEqual(report["tp"] + report["fp"] +
                         report["fn"] + report["tn"], report["n"])

    def test_undefined_denominators_reported(self):
        value = score([0, 0], [0, 0])
        self.assertEqual(value["denominators"]["precision"], 0)
        self.assertEqual(value["denominators"]["recall"], 0)
        self.assertIsNone(value["precision"])

    def test_paired_difference_and_interval(self):
        delta, low, high = paired_interval(GOLD, BASELINE, CANDIDATE)
        self.assertAlmostEqual(delta, 0.1)
        self.assertLess(low, 0)
        self.assertGreater(high, 0)
        self.assertGreaterEqual(low, -1)
        self.assertLessEqual(high, 1)


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        unittest.main()
    else:
        print("Evaluation:", VERSION)
        print("Baseline:", score(GOLD, BASELINE))
        print("Candidate:", score(GOLD, CANDIDATE))
        delta, low, high = paired_interval(GOLD, BASELINE, CANDIDATE)
        print(f"Paired difference: {delta:.3f}; "
              f"95% Hoeffding interval: [{low:.3f}, {high:.3f}]")
