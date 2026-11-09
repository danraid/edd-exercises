# Chapter 5. Human Evaluation and Annotation Quality: Exercises

Companion to Chapter 5 of *Eval-Driven Development*.
[Worked answers](solutions.md) | [Laboratory](../../labs/05/README.md)

## Exercises and Knowledge Checks

1. **Rubric boundary.** Mosaic cites “applications close on Friday” and answers “applications close on Friday at 17.00”. Assign a label under the chapter’s groundedness rubric. State your assumption about the supplied evidence, identify the unsupported or supported claim, and explain what additional evidence might change the label. Would your answer establish the actual closing time?

2. **Agreement and baseline.** In a new **synthetic** set of 40 cases, both annotators agree on 36: 28 supported and eight unsupported. The four remaining cases are split equally between the two disagreement directions. Construct the matrix, calculate \(p_o\), \(p_e\) and \(\kappa\), and compare them with the worked example’s 0.80 and 0.60. Explain why neither comparison establishes improved correctness. For a further check, describe what happens to kappa if both reviewers use only one label.

3. **Extend the lab.** Add a fifth synthetic case with a disagreement and a decisive adjudication. Write an executable test asserting that the decision is `adjudicated`, that both original annotations remain in the run record, and that the adjudicator’s evidence span occurs in the case passage. Then add a test showing that a missing reviewer causes `ValueError`. Explain why a passing span test alone is insufficient to validate the adjudication.

4. **Sampling and release.** Design a blind paired review of an old and a candidate Mosaic version across two languages. Specify the unit, target population, sample allocation, order-balancing procedure and how you will report unresolved cases. Give one non-compensable safety invariant and explain how a strong average preference could coexist with a release-blocking regression.
