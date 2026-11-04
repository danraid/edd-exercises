# Chapter 2. The EDD Feedback Loop and Evaluation Contracts: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/02.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/02/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Mosaic is evaluated with retrieved documents supplied directly to the answer generator. Draw the system-under-test boundary and state one assumption about retrieval. Describe a retrieval failure this evaluation cannot detect, and propose an additional observable output needed to test it.

2. **Baseline and trade-off.** In the worked example, suppose a further synthetic candidate C answers 76 ordinary and 17 protected cases correctly, with zero observed safety violations. Compute its weighted accuracy using the stated weights. Compare it with the baseline and apply every stated gate condition. Explain why the 20 protected cases do not establish a precise deployment failure rate.

3. **Executable extension.** Add a fourth synthetic case and update the policy through an explicitly reviewed version change. Write an executable test that rejects duplicate output identifiers. Add a second test showing that a candidate with a correct aggregate count but an incorrect protected case is red. Document the new denominator and expected output in the README.

4. **Diagnose leakage.** An engineer repeatedly reads holdout failures, revises the prompt and reports the best holdout score. Explain why the score is no longer a clean final assessment. Design a development/holdout access process and name one remaining source of uncertainty.

5. **Deployment decision.** Propose one offline check, one shadow observation and one canary stop condition for Mosaic. For each, identify the unit of analysis, data handling constraint and person or role authorised to decide whether to proceed.
