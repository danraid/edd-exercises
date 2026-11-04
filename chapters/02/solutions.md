# Chapter 2. The EDD Feedback Loop and Evaluation Contracts: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/02/README.md)

## 1. Boundary and assumption.

The evaluated boundary begins with already retrieved documents passed into generation; retrieval selection is outside scope. Missing relevant pages or poisoned retrieval are invisible. Capture rank, retrieved IDs, version and provenance in a full-pipeline eval.

## 2. Baseline and trade-off.

C = .70(76/80)+.30(17/20)=.92 (92%), above baseline 90%. Protected 17/20=85% meets minimum, zero unsafe events meets invariant: synthetic gate PASS. Twenty protected cases cannot establish a precise deployment rate.

## 3. Executable extension.

Create version-2 four-case fixture with unique IDs, approved new policy and documented denominator 4. Reject duplicate output IDs and block on any protected-case failure even with an adequate overall count; see extensions tests.

## 4. Diagnose leakage.

Repeated selection on a disclosed holdout produces an optimistic maximum. Restrict holdout access, freeze scoring and candidate before final evaluation; account for distribution changes and imperfect labels.

## 5. Deployment decision.

Offline: independent grounding/entailment check with redacted query and release-owner sign-off. Shadow: record unsupported-claim rates without impacting users with privacy limits. Canary: stop on prohibited action, under incident and release-owner authority.
