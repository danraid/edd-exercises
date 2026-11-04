# Chapter 1. From Test-Driven Development to Eval-Driven Development: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/01/README.md)

## 1. Boundary and assumption.

ID matching checks syntax, not policy correctness, currency or claim entailment. Useful only with a trusted effective-version mapping; misleading when the referenced passage is unrelated or obsolete.

## 2. Recompute against a baseline.

S1,S2,S3 now pass both checks, S4 fails both: 6/8=75% checks, 3/4=75% scenarios, zero violations. Both the 80% check and 90% scenario gates fail: STOP. A paired change trace is needed for causal attribution.

## 3. Extend the laboratory.

Add fifth case to a version-2 fixture: correct answer, wrong citation. Original baseline plus this case yields 8/10 checks (80%), 3/5 scenarios (60%); STOP under scenario gate. Pin both dataset versions and hashes; editing v1 under the same ID destroys reproducibility.

## 4. Design for holdout and slices.

Example: 24 dev, 12 challenge and 20 protected holdout cases; one labelled question and effective policy version is a unit. Stratify by language and abstention, independently double-label and adjudicate. For sparse languages publish counts, widen uncertainty and collect further cases.

## 5. Interpret a green dashboard.

Ten adaptive prompt revisions risk overfitting; coverage and rare dangerous failures may be absent. Evaluate one frozen independent holdout and run redacted shadow observations. Neither proves future population safety.
