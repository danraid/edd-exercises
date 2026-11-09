# Chapter 4. Metrics, Scoring and Statistical Uncertainty: Exercises

Companion to Chapter 4 of *Eval-Driven Development*.
[Worked answers](solutions.md) | [Laboratory](../../labs/04/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Mosaic predicts no positive cases on a synthetic set of 20 tasks, three of which are reference-positive. Calculate accuracy and recall; explain why precision is undefined under this chapter’s convention. State one assumption required before interpreting these results as estimates for future tasks.

2. **Baseline comparison.** On the same synthetic 100-task set used in the counterexample, suppose a third system has \(TP=3\), \(FN=2\), \(FP=1\), \(TN=94\). Calculate accuracy, precision and recall. Compare its error cost with both earlier systems using one unit per FP and five per FN. Then explain how the decision might change if false positives carry greater cost, and why no interval can be inferred from the counts without a sampling design.

3. **Extend the lab.** Add a `cost(result, fp_cost, fn_cost)` function and executable tests asserting that the worked baseline and candidate costs are 11 and 6 under the stated synthetic costs. Reject negative costs. Include the evaluation version, case count and units in a report, and explain why this cost does not replace a safety invariant.

4. **Design a regression study.** Propose a paired evaluation for two Mosaic versions across three languages. Specify the task or session unit, a protected holdout, a practically important regression, how correlated turns will be handled, and a plan for multiple slice comparisons. Explain what a wide interval would permit you to conclude.
