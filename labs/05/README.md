# Chapter 05 — auditable dual annotation (synthetic Mosaic)

Run with Python 3.9+ and only the standard library:

```bash
python labs/05/mosaic_human.py
python -m unittest discover -s labs/05 -p test_mosaic.py -v
```

The first command prints canonical JSON evidence and runs six inline self-tests. The second runs an independent regression suite. Inputs are four synthetic answer–passage pairs, two original reviewer labels per case and a separate adjudication event; no live annotator data, network access, or credential is used.

## Release and scientific limits

- Every case must have exactly one A label and one B label, with a non-empty reason and a cited span appearing in its passage.
- A decisive agreeing pair cannot be adjudicated. A disputed or matching-uncertain pair can be escalated to C; unresolved cases are not automatically gold.
- Original reviewer events stay in the record even if C decides. The SHA-256 digest binds this synthetic record to input bytes but does not authenticate a reviewer or guard access.
- A cited span existing in a passage does **not** establish entailment, correctness or validity of the human judgement.
- The three-label four-case lab agreement and the worked 40-case binary kappa use different rubrics. Do not compare those scores directly.
- This fixture is demonstrative, not a real blinded, independent, representative or access-controlled deployment evaluation.
