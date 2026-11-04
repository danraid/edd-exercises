# Mosaic Chapter 04 - scoring, uncertainty, and denominators

This is an original, synthetic educational fixture, not deployment validation.
It does not call an LLM, access private data, or assert a protected holdout.

Requires Python 3.9+ (standard library only).

Run from the repository root:

```sh
python labs/04/mosaic_metrics.py
python labs/04/mosaic_metrics.py --test
python -m unittest discover -s labs/04 -p test_mosaic.py -v
```

Expected baseline: TP=4, FP=1, FN=2, TN=3; accuracy 0.700.
Expected candidate: TP=5, FP=1, FN=1, TN=3; accuracy 0.800.
Paired change is +0.100, with an intentionally broad Hoeffding interval
[-0.759, 0.959] at nominal 95% under independent, comparable tasks.

Both systems are scored on exactly the same ten synthetic cases. The case
sampling assumption pertains to dependence **between tasks**, not between
baseline and candidate measurements for the same task. The report identifies
the evaluation version, unit, n and each metric's denominator. Division by
zero produces None, never an invented accuracy.

This dataset proves only the program's arithmetic and boundary behaviour.
Scorer validity, sampling representativeness, calibration, safe deployment and
release invariants all require separate empirical evidence and controls.
