"""Independent tests for the Chapter 04 canonical executable lab."""
import math
import unittest

from mosaic_metrics import GOLD, BASELINE, CANDIDATE, VERSION, score, paired_interval

class IndependentMosaicMetricTests(unittest.TestCase):
    def test_confusion_and_denominators(self):
        b=score(GOLD,BASELINE)
        c=score(GOLD,CANDIDATE)
        self.assertEqual((b['tp'],b['fp'],b['fn'],b['tn']),(4,1,2,3))
        self.assertEqual((c['tp'],c['fp'],c['fn'],c['tn']),(5,1,1,3))
        self.assertEqual(b['denominators'],{'accuracy':10,'precision':5,'recall':6,'f1':11})
        self.assertEqual(c['denominators'],{'accuracy':10,'precision':6,'recall':6,'f1':12})
        self.assertEqual((c['version'],c['unit'],c['n']),(VERSION,'synthetic task',10))
    def test_undefined_denominators_do_not_automatically_become_zero(self):
        s=score([0,0],[0,0])
        self.assertEqual(s['denominators']['precision'],0)
        for metric in ('precision','recall','f1'):
            self.assertIsNone(s[metric])
    def test_boundary_and_binary_inputs(self):
        for g,p in [([],[]),([1],[]),([2],[1]),([1],[0,1])]:
            with self.assertRaises(ValueError):score(g,p)
    def test_interval_matches_stated_equation(self):
        delta,low,high=paired_interval(GOLD,BASELINE,CANDIDATE)
        margin=math.sqrt(2*math.log(2/0.05)/10)
        self.assertAlmostEqual(delta,0.1)
        self.assertAlmostEqual(low,0.1-margin)
        self.assertAlmostEqual(high,0.1+margin)
        self.assertLess(low,0.0)
        self.assertGreater(high,0.0)
    def test_invalid_alpha_and_all_agree(self):
        for alpha in (-0.1,0,1,1.1):
            with self.assertRaises(ValueError):paired_interval([1],[1],[1],alpha)
        self.assertEqual(paired_interval([0,1],[0,1],[0,1])[0],0)

if __name__=='__main__':unittest.main()
