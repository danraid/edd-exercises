# Chapter 4. Metrics, Scoring and Statistical Uncertainty: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/04/README.md)

## 1. Boundary and assumption.

All-negative predictions on 20 cases with three positives give TN=17,FN=3, accuracy 17/20=85%, recall 0/3=0, precision undefined (zero predicted-positive denominator). Population interpretation needs representative independent sampling.

## 2. Baseline comparison.

For TP=3,FN=2,FP=1,TN=94: accuracy 97%, precision 75%, recall 60%, error cost 1+5(2)=11 units. The chapter's separate ten-case lab baseline and candidate cost 11 and 6; they are different datasets and must not be directly compared. Changing FP cost can change ranking. Sample-design assumptions are needed for intervals.

## 3. Extend the lab.

Cost function: `fp*fp_cost+fn*fn_cost` with nonnegative input validation. Baseline (1,2) = 11, candidate (1,1) = 6. Report version mosaic-support-v1, n=10 and synthetic units. Invariants never become compensable.

## 4. Design a regression study.

Use paired cases stratified across three languages and a protected holdout; cluster turns by session, predeclare effect margins and multiple-comparison corrections. A wide interval means the sign and size of the effect remain unresolved.
