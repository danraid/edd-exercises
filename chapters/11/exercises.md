# Chapter 11. Observability, Drift, Cost and Evaluation Governance: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/11.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/11/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Mosaic retains a manifest hash but deletes raw query content after a defined period. Explain which integrity claim remains possible and which replay claim no longer follows. State one assumption about how the retained manifest and hashes are protected.

2. **Recompute against a baseline.** Using the worked example, standardise both windows to a population that is 50% Group A and 50% Group B. Calculate each standardised unsupported-answer rate. Then explain why that result does not prove that the deployment is safe for Group B.

3. **Extend the laboratory.** Add a function that computes the current group rates standardised to baseline group proportions. Write an executable test asserting that the result is `0.024`. Add another test in which the current Group B unsupported count changes, and assert that the standardised result changes. Preserve the fixture and scorer hash checks.

4. **Design a triage decision.** Propose a second alert for a synthetic safety invariant. Identify its owner, immediate containment action, evidence needed and a condition for closing the incident. Explain why a low aggregate unsupported-answer rate must not cancel this alert.

5. **Cost comparison.** Recalculate the worked alert policy if the false-investigation cost is 200 units and the missed-incident cost remains 1,000 units. Compare it with investigating every window under the same restricted cost model. Identify one omitted cost or benefit that could alter the decision.
