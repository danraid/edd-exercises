# Chapter 6. LLM-as-a-Judge and Model-Based Evaluation: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/06.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/06/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Mosaic gives two fluent answers to a policy question. A reference-free pairwise judge prefers A. Explain what this result does and does not establish about A’s factual support. State an assumption under which the comparison would be useful.

2. **Recompute against a baseline.** In a new synthetic set of 50 human-unacceptable answers, Judge A passes 10 and Judge B passes 5. Calculate each false-acceptance rate and the absolute difference in percentage points. What further information is needed before choosing B for release? Include acceptable-case performance, uncertainty and representativeness in your answer.

3. **Extend the lab.** Add a test showing that a low-confidence `pass` escalates. Then add a function that reports the escalation proportion over all decisions. Write an executable test for a synthetic list containing one pass, one fail and two escalations. Explain why escalation proportion should accompany auto-release FAR.

4. **Design a bias check.** Construct two synthetic answers with equivalent policy content but different lengths. Describe how you would blind, randomise and reverse their positions, record human labels, and investigate disagreement without assuming that either length is inherently better.

5. **Inspect a release proposal.** A team changes only the judge prompt and reports a higher Mosaic pass rate on its development set. Identify at least three alternative explanations and specify what frozen evidence and independent checks you would require before accepting the change.
