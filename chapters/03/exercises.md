# Chapter 3. Evaluation Datasets, Sampling and Leakage: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/03.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/03/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Under the synthetic age policy in the lab, write cases for ages 17, 18 and 19. State the unit and assumption needed to determine eligibility. Explain why “almost 18” cannot safely be labelled without an interpretation of age and timing. Provide an expected response and rationale for each case.

2. **Coverage and baseline.** Add four Bengali positive cases and two Bengali abstention cases to the worked set, leaving the other two Bengali cells empty. Recalculate planned-cell coverage and the new total case count. Compare the result with the original 83.3% coverage. Explain why the improved coverage still does not establish representative performance.

3. **Executable split control.** Extend the lab schema with a non-empty `family_id`. Add a validation rule forbidding the same family in different splits, even when questions differ. Write a `unittest` case that fails under the new rule and another that demonstrates an allowed same-split family. State how your rule affects translations or paraphrases of one incident.

4. **Release decision.** Using the worked example, write a short decision record for the candidate. Include the aggregate baseline and candidate rates, abstention slice, missing language, applicable invariant and at least two follow-up actions. Identify which additional evidence would be needed before making a deployment-population claim.
