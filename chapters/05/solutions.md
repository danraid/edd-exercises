# Chapter 5. Human Evaluation and Annotation Quality: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/05/README.md)

## 1. Rubric boundary.

Only 'Friday' is supported by the supplied quote. '17.00' is unsupported, so groundedness is unsupported unless separate effective evidence proves time. A passage-level verdict alone does not certify actual closing time.

## 2. Agreement and baseline.

Agreement matrix [[28,2],[2,8]] (A rows, B columns): observed 36/40=.9; marginals both 30/40 and 10/40, chance .75²+.25²=.625, kappa (.9-.625)/(.375)=.7333. Neither agreement nor kappa proves accuracy. If both always choose one label, kappa is undefined (0/0).

## 3. Extend the lab.

Create fifth case with conflicting labels; retain both reviews and adjudicator evidence span. Assert adjudicated result, original annotations preserved, span in passage; missing reviewer raises ValueError. Text-span matching does not prove entailment.

## 4. Sampling and release.

Blind candidate order, randomise AB/BA, stratify two languages by policy/task and retain unresolved reviews. Report slice and disagreement rates. Any verified prohibited disclosure blocks regardless of overall preference.
