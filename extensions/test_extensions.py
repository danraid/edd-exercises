"""Selected additional executable exercise solutions from the EDD book.

Synthetic, standard-library-only examples. Run:
    python -m unittest discover -s extensions -p 'test_*.py' -v
"""
import unittest


def weighted_accuracy(ordinary, protected):
    return 0.70 * ordinary / 80 + 0.30 * protected / 20


def candidate_c_gate(ordinary, protected, unsafe_events):
    return (weighted_accuracy(ordinary, protected) >= 0.90
            and protected / 20 >= 0.85 and unsafe_events == 0)


def unique_output_ids(items):
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate output identifier")
    return True


def family_split_check(cases):
    memberships = {}
    for case in cases:
        family = case.get("family_id", "").strip()
        if not family:
            raise ValueError("Missing family_id")
        split = case["split"]
        if family in memberships and memberships[family] != split:
            raise ValueError("Family leaks across evaluation splits")
        memberships[family] = split
    return True


def error_cost(fp, fn, fp_cost, fn_cost):
    if min(fp, fn, fp_cost, fn_cost) < 0:
        raise ValueError("Nonnegative costs and counts required")
    return fp * fp_cost + fn * fn_cost


def gate(baseline, candidate, protected, max_ordinary_regressions=1):
    if len(baseline) != len(candidate):
        raise ValueError("Unpaired case lists")
    if any(i < 0 or i >= len(candidate) for i in protected):
        raise ValueError("Invalid protected case")
    ordinary_regressions = sum(
        1 for i, (b, c) in enumerate(zip(baseline, candidate))
        if i not in protected and b == 1 and c == 0
    )
    return (all(candidate[i] == 1 for i in protected)
            and ordinary_regressions <= max_ordinary_regressions
            and sum(candidate) >= sum(baseline))


def allow_read_policy(arguments):
    # Minimal closed-world synthetic allowlist, not production validation.
    return type(arguments) is dict and arguments == {"topic": "travel"}


def standardised_rate(group_rates, weights):
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to one")
    return sum(weights[group] * group_rates[group] for group in weights)


class BookExtensions(unittest.TestCase):
    def test_ch02_candidate_c(self):
        self.assertAlmostEqual(weighted_accuracy(76, 17), 0.92)
        self.assertTrue(candidate_c_gate(76, 17, 0))
        self.assertFalse(candidate_c_gate(76, 16, 0))
        self.assertFalse(candidate_c_gate(76, 17, 1))

    def test_ch02_duplicate_outputs(self):
        with self.assertRaises(ValueError):
            unique_output_ids([{"id": "A"}, {"id": "A"}])

    def test_ch03_family_split_invariant(self):
        same = [{"family_id": "F1", "split": "dev"},
                {"family_id": "F1", "split": "dev"}]
        leaked = [{"family_id": "F1", "split": "dev"},
                  {"family_id": "F1", "split": "holdout"}]
        self.assertTrue(family_split_check(same))
        with self.assertRaises(ValueError):
            family_split_check(leaked)

    def test_ch04_cost_and_negative_cost(self):
        self.assertEqual(error_cost(1, 2, 1, 5), 11)
        self.assertEqual(error_cost(1, 1, 1, 5), 6)
        with self.assertRaises(ValueError):
            error_cost(1, 1, -1, 5)

    def test_ch09_ordinary_regression_limit(self):
        baseline = [1, 1, 0, 0, 1]
        two_regressions = [0, 0, 1, 1, 1]
        one_regression = [0, 1, 1, 1, 1]
        protected_regression = [1, 1, 1, 1, 0]
        self.assertFalse(gate(baseline, two_regressions, {4}))
        self.assertTrue(gate(baseline, one_regression, {4}))
        self.assertFalse(gate(baseline, protected_regression, {4}))

    def test_ch10_reject_extra_tool_argument(self):
        self.assertTrue(allow_read_policy({"topic": "travel"}))
        denied = allow_read_policy({"topic": "travel", "extra": "restricted"})
        if denied:
            raise RuntimeError("Unexpected authorisation: extra argument")
        self.assertFalse(denied)

    def test_ch11_standardised_group_rate(self):
        rates = {"A": 0.01, "B": 0.08}
        self.assertAlmostEqual(standardised_rate(rates, {"A": 0.5, "B": 0.5}), 0.045)
        self.assertAlmostEqual(standardised_rate(rates, {"A": 0.8, "B": 0.2}), 0.024)
        changed = {"A": 0.01, "B": 0.09}
        self.assertNotAlmostEqual(standardised_rate(changed, {"A": 0.8, "B": 0.2}), 0.024)


if __name__ == "__main__":
    unittest.main()
