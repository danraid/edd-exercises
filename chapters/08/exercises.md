# Chapter 8. Agentic AI Evaluation and Tool-Use Traces: Exercises

Original: [book chapter](https://github.com/danraid/eval-driven-development/blob/main/manuscript/08.md).

[Worked answers](solutions.md) | [Laboratory](../../labs/08/README.md)

## Exercises and Knowledge Checks

1. **Explain an authority boundary.** Mosaic’s research agent passes a policy excerpt to a drafting agent. The drafting agent then asks a transmission agent to send a notice. Identify which hand-offs need evidence and which need delegated authority. State your assumption about whether the user authorised transmission. Explain why a useful policy excerpt is not itself permission to send.

2. **Recompute a comparison.** Use the two-episode baseline and candidate in the worked example. Calculate completion, invariant-pass and joint rates for each, with episodes as the denominator. Then decide under two explicitly different synthetic policies:  
   a. release requires every evaluated episode to pass the invariant;  
   b. release is based only on a completion rate of at least 75%.  
   Explain why decision (b) can hide a safety failure and why neither result supports a population-level claim.

3. **Extend the executable lab.** Add a `request_confirmation` mock action and a new `send_notice` rule that permits a simulated send only after both a draft and confirmation exist. Define precisely whose confirmation the fixture represents. Write assertions showing that sending before confirmation fails, sending after the required sequence succeeds, and a fresh replay cannot inherit confirmation. Keep the send entirely simulated. State whether your revised invariant concerns attempted unauthorised sends, committed sends, or both.

4. **Design a replay study.** Propose a protected set of multilingual Mosaic episodes, a baseline and a candidate. Specify the initial-state reset, trace fields, number and unit of observations, treatment of stochastic repetitions, and at least one challenge case involving an irreversible action. Explain what evidence would make a comparison inconclusive.
