# Chapter 12. Reference EDD Harness and End-to-End Case Study: Exercises

Companion to Chapter 12 of *Eval-Driven Development*.
[Worked answers](solutions.md) | [Laboratory](../../labs/12/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Explain why an attempted `send_external` action is a release blocker even when no external transmission occurs in this lab. State one assumption under which an attempted action should be treated differently from an executed action, and describe what additional evidence would be needed.

2. **Metric and baseline.** Suppose a new **synthetic** candidate passes nine of the same ten cases, but has one new failure on a case the baseline passed. Construct a possible paired outcome table consistent with those totals. Calculate its absolute improvement over the seven-pass baseline. Explain why its aggregate rate alone cannot determine release.

3. **Executable extension.** Add a synthetic case in which the answer is correct but cites the wrong document. Write an assertion that the combined scorer fails that case. Record the modified source and dataset hashes, and explain whether the old and new scores are directly comparable.

4. **Governance.** Design a human-adjudication record for an ambiguous citation. Include the rubric version, reviewer identity, disagreement procedure and privacy restriction. Explain how you would prevent the reviewer’s decision from being silently altered after release.
