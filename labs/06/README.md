# Chapter 06: synthetic judge adapter and release routing

Requires Python 3.10 or later; stdlib only. No credentials, network or real model are used.

```bash
python labs/06/mosaic_judge.py
python -m unittest discover -s labs/06 -p test_mosaic.py -v
```

The inline demonstration contains eight tests. The independent regression suite
checks unhashable nested values, confidence validation, malformed calibration
labels, safe evidence lookups, and the separate `stop` release invariant.

This is a **synthetic teaching fixture**, not an externally calibrated judge, a
real safety policy, or a green light to deploy Mosaic. All-fail may pass the
negative-only uncertainty gate while offering no useful service coverage.

The release-stop illustration now executes a narrow deterministic invariant
against the frozen synthetic policy and exact prohibited guarantee; callers
cannot assert `confirmed_safety_violation=True` to manufacture a stop.
This example has no external policy-authenticity proof or general entailment.
