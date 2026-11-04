"""Independent regression tests for the published Chapter 03 lab."""
import copy
import unittest
import mosaic_lab as lab

class LeakageRegressionTests(unittest.TestCase):
    def test_canonical_duplicate_within_train(self):
        bad = copy.deepcopy(lab.DATA)
        bad["cases"][1]["question"] = "  I AM 21. AM I ELIGIBLE?   "
        errors = lab.validate(bad)
        self.assertTrue(any("duplicate question within split" in e for e in errors), errors)

    def test_duplicate_within_holdout(self):
        bad = copy.deepcopy(lab.DATA)
        bad["cases"][5]["question"] = bad["cases"][4]["question"]
        self.assertTrue(any("duplicate question within split" in e for e in lab.validate(bad)))

    def test_cross_split_collision(self):
        bad = copy.deepcopy(lab.DATA)
        bad["cases"][2]["question"] = bad["cases"][0]["question"]
        self.assertTrue(any("question crosses splits" in e for e in lab.validate(bad)))

    def test_unique_fixture_and_idempotent_validation(self):
        self.assertEqual(lab.validate(lab.DATA), [])
        before = lab.canonical_json(lab.DATA)
        self.assertEqual(lab.validate(copy.deepcopy(lab.DATA)), [])
        self.assertEqual(lab.canonical_json(lab.DATA), before)

    def test_question_canonicalisation_and_unicode(self):
        self.assertEqual(lab.question_hash("  TEST   CASE  "), lab.question_hash("test case"))
        self.assertEqual(lab.question_hash("A\u00a0B"), lab.question_hash("a b"))

if __name__ == "__main__":
    unittest.main()
