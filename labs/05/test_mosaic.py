import importlib.util
import pathlib
import unittest

LAB=pathlib.Path(__file__).resolve().parent/'mosaic_human.py'
spec=importlib.util.spec_from_file_location('mosaic_human_ch05',LAB)
human=importlib.util.module_from_spec(spec)
spec.loader.exec_module(human)

class HumanEvaluationRegressionTests(unittest.TestCase):
    def test_retain_both_original_annotators_and_adjudicator_event(self):
        r=human.run(human.CASES,human.ANNOTATIONS,human.ADJUDICATIONS)
        self.assertEqual(len(r['inputs']['annotations']),8)
        self.assertEqual(r['inputs']['adjudications'][0]['reviewer'],'C')
        self.assertEqual(r['decisions']['s2']['status'],'unresolved')

    def test_no_adjudication_when_decisive_labels_agree(self):
        a=[human.event('s1','C','unsupported','opens on Monday','Invalid relabel')]
        with self.assertRaisesRegex(ValueError,'already-agreed'):
            human.run(human.CASES,human.ANNOTATIONS,a)

    def test_adjudicator_identity_rejected(self):
        a=[human.event('s2','A','unsupported','opens on Monday','Invalid identity')]
        with self.assertRaisesRegex(ValueError,'Only adjudicator C'):
            human.run(human.CASES,human.ANNOTATIONS,a)

    def test_disagreement_can_be_adjudicated_without_original_overwrite(self):
        a=[human.event('s2','C','unsupported','opens on Monday','Daily is not entailed')]
        result=human.run(human.CASES,human.ANNOTATIONS,a)
        self.assertEqual(result['decisions']['s2']['status'],'adjudicated')
        self.assertEqual([e['label'] for e in result['inputs']['annotations'] if e['case']=='s2'],
                         ['unsupported','uncertain'])

    def test_duplicate_case_and_adjudication_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate case'):
            human.run(human.CASES+[human.CASES[0]],human.ANNOTATIONS,human.ADJUDICATIONS)
        with self.assertRaisesRegex(ValueError,'Duplicate adjudication'):
            human.run(human.CASES,human.ANNOTATIONS,human.ADJUDICATIONS*2)

    def test_unknown_span_rejected(self):
        bad=[dict(e) for e in human.ANNOTATIONS]
        bad[0]['span']='not evidence'
        with self.assertRaisesRegex(ValueError,'Evidence span not found'):
            human.run(human.CASES,bad,human.ADJUDICATIONS)

    def test_missing_or_duplicate_original_reviewers_rejected(self):
        with self.assertRaisesRegex(ValueError,'one label from A and B'):
            human.run(human.CASES,human.ANNOTATIONS[:-1],human.ADJUDICATIONS)
        changed=[dict(e) for e in human.ANNOTATIONS]
        changed[1]['reviewer']='A'
        with self.assertRaisesRegex(ValueError,'one label from A and B'):
            human.run(human.CASES,changed,human.ADJUDICATIONS)

    def test_span_presence_is_not_entailment(self):
        # The program deliberately cannot prove logical entailment; a misleading
        # agreed label could pass the structural tests. This is a documented limit.
        altered=[dict(e) for e in human.ANNOTATIONS]
        for e in altered:
            if e['case']=='s2':e['label']='supported'
        r=human.run(human.CASES,altered,[])
        self.assertEqual(r['decisions']['s2']['status'],'accepted')
        self.assertEqual(r['decisions']['s2']['label'],'supported')

if __name__=='__main__':unittest.main()
