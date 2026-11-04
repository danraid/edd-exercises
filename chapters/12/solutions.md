# Chapter 12. Reference EDD Harness and End-to-End Case Study: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/12/README.md)

## 1. Boundary and assumption.

An attempted `send_external` violates an attempt-level invariant even if a mock denies it. A committed-effect-only policy would distinguish the states, requiring reliable pre- and post-execution traces.

## 2. Metric and baseline.

Paired outcomes: both pass 6, baseline-only pass 1, candidate-only pass 3, both fail 0. Thus baseline 7/10, candidate 9/10, +20 percentage points. Aggregate hides which case regressed and whether it was protected.

## 3. Executable extension.

Add correct-answer/wrong-citation fixture; conjunctive scorer must return false. Update data/source hashes and version. Scores across different case populations are not directly paired estimates.

## 4. Governance.

Adjudication record: case/rubric versions, reviewer and adjudicator identities, evidence spans, dissent, timestamp, privacy constraints and append-only signed decision hash. Require independent approval for amendments.
