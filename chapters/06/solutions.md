# Chapter 6. LLM-as-a-Judge and Model-Based Evaluation: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/06/README.md)

## 1. Boundary and assumption.

A reference-free preference says A is preferred, not factually supported. It is useful for style when truthfulness is independently fixed and order bias controlled.

## 2. Recompute against a baseline.

Judge A FAR=10/50=20%, B FAR=5/50=10%, reduction 10 percentage points. Also evaluate false rejections, acceptable-case coverage, uncertainty, escalation and representative holdout before release.

## 3. Extend the lab.

Low-confidence `pass` must escalate. In four decisions pass/fail/escalate/escalate, escalation rate is 2/4=50%. Record review workload and define auto-release FAR denominator.

## 4. Design a bias check.

Keep factual meaning identical but vary length; randomise order, reverse positions, blind source and record human labels. Diagnose disagreement and positional effects without assuming verbosity implies correctness.

## 5. Inspect a release proposal.

Development pass-rate increase could be prompt overfitting, relaxed rubric or position/length bias. Freeze judge, labels, rubric, version and thresholds; blind adjudicated holdout must report FAR, false rejects, escalations and slices.
