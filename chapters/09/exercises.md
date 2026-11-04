# Chapter 9. Regression Testing, CI/CD and Eval-Driven Release Gates: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/09.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/09/README.md)

## Exercises and Knowledge Checks

1. **Boundary and assumption.** Mosaic’s smoke suite checks that every citation identifier exists in the retrieved document set. Explain what this test establishes and what it does not establish about answer grounding. State one assumption about the citation parser, and propose a complementary eval case that could expose a false pass.

2. **Paired comparison.** In a new synthetic set of 20 cases, the baseline passes 15 and the candidate passes 16. Three baseline failures become passes, while two baseline passes become failures. One of the two regressions is protected, and the policy requires every protected case to pass. Calculate both pass rates and their difference in percentage points. State the gate decision and explain why the paired record adds information beyond the averages.

3. **Executable extension.** Add a trusted policy requiring the candidate to make no more than one ordinary-case regression relative to baseline. Define an ordinary regression as \(b_i=1\) and \(c_i=0\) for a non-protected case. Write a unit test with two such regressions that asserts `BLOCK`, and another with one that isolates and checks the boundary. Explain how your test ensures that the protected invariant still applies independently.

4. **Rerun policy and governance.** Design a predeclared policy for a stochastic grounding scorer, including the number of attempts, treatment of timeouts and which results are retained. Then describe how a correction to a protected gold label can be approved without allowing the candidate team to weaken its own gate. Identify one residual uncertainty in your design.
