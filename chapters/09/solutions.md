# Chapter 9. Regression Testing, CI/CD and Eval-Driven Release Gates: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/09/README.md)

## 1. Boundary and assumption.

A smoke check establishes only ID presence and parseability, not entailment or correctness. Assume canonical citation parser. Add a case with a real ID but a contradictory cited passage.

## 2. Paired comparison.

Baseline 15/20=75%, candidate 16/20=80%, improvement 5 percentage points. Three fixes and two regressions imply net +1; a protected regression blocks even though total increases.

## 3. Executable extension.

Count ordinary regressions where b=1,c=0 on nonprotected cases. Limit one: two => BLOCK; one can pass only if protected all-pass and aggregate conditions also pass. Executable extension tests demonstrate both.

## 4. Rerun policy and governance.

Predeclare rerun attempts and seeds; timeouts count as fails or escalations, never selectively discard failures. Protect adjudicated gold-label revisions with independent approval and version changes. Rare unseen failures remain a risk.
