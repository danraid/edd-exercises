# Chapter 7. RAG Evaluation: Retrieval, Grounding and Faithfulness: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/07/README.md)

## 1. Explain a boundary.

A claim faithful to an old policy may be wrong for today's policy; inspect effective dates, supersession and authorisation. Evidence supporting the current date is essential.

## 2. Recompute and compare.

Relevant results in baseline D1,D3,D2,D4 occur at ranks 1,3,4: AP=(1+2/3+3/4+0)/4=29/48≈.60417; candidate .6875; gain ≈.08333. One query proves no population effect. Use a paired protected effective-date slice.

## 3. Extend the executable lab.

Give D4@2 a new deadline and explicit effective date, and test query date applicability. D4@1 must fail the updated-deadline entailment test. Larger version number alone proves nothing.

## 4. Design a multi-hop case.

Create passage A (eligibility), B (deadline), C (location only). Full answer requires A+B; one citation alone gives partial support and must fail a conjunctive claim scorer. Abstain if required authoritative support is missing.
