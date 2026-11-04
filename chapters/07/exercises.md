# Chapter 7. RAG Evaluation: Retrieval, Grounding and Faithfulness: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/07.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/07/README.md)

## Exercises and Knowledge Checks

1. **Explain a boundary.** Mosaic answers a current-policy question using an accurately quoted historical passage. Explain whether the answer is faithful and whether it is factually correct. State the assumption you make about the question’s effective date and describe what additional evidence would be needed to decide correctness.

2. **Recompute and compare.** In the worked example, calculate \(AP\) for the baseline order D1, D3, D2, D4, using the same four-passage gold set and the formula in this chapter. Compare it with the candidate’s \(0.6875\). Explain why neither result alone establishes a population-level improvement. Identify a query slice and a paired evaluation design that would make the comparison more informative.

3. **Extend the executable lab.** Add a synthetic passage version `D4@2` with a different deadline and a case whose policy date requires that version. Write an executable test proving that citing `D4@1` cannot support the new deadline. State how your fixture establishes which version is effective; merely choosing the larger version number is not enough.

4. **Design a multi-hop case.** Create two synthetic passages that are jointly necessary for an answer and a third that is relevant but insufficient. Specify acceptable evidence sets, a complete answer, a partial answer and an appropriate abstention. Explain how your scorer would avoid crediting a citation that supports only one part of a compound claim.
