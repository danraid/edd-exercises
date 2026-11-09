# Chapter 1. From Test-Driven Development to Eval-Driven Development: Exercises

Companion to Chapter 1 of *Eval-Driven Development*.
[Worked answers](solutions.md) | [Laboratory](../../labs/01/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** A unit test verifies that a response contains a citation identifier. An acceptance test verifies that an answer and citation appear together. Explain what neither test establishes about the cited policy. State one assumption under which exact identifier matching would be a useful proxy, and one situation in which it would be misleading.

2. **Recompute against a baseline.** In a new **synthetic** candidate run on the same four scenarios, suppose S3 passes both checks but S4 fails both. Calculate the check and scenario pass rates. Compare them with the baseline in the worked example and apply all three thresholds, assuming zero marker violations. Explain why the comparison alone does not establish which change caused the result.

3. **Extend the laboratory.** Add a fifth synthetic case whose answer is correct but whose citation is wrong. Write an executable unit test asserting the new counts, the scenario gate and the release decision. Preserve the original baseline under a separate fixture directory and give the extended dataset a new version. Explain why merely editing the original fixture without changing its identifier would weaken provenance.

4. **Design for holdout and slices.** Propose a small development set, challenge set and protected holdout for multilingual Mosaic. Identify the unit of analysis, a plausible failure slice and a process for reviewing labels. Explain what you would do if one language had too few cases for a reliable rate.

5. **Interpret a green dashboard.** A candidate meets every recorded threshold after ten prompt revisions on the same cases. List two reasons not to infer deployment fitness. Describe one additional observation or controlled comparison that would help, and state what it still would not prove.
