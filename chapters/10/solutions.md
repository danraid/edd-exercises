# Chapter 10. Robustness, Safety and Adversarial Evaluation: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/10/README.md)

## 1. Boundary and assumption.

Retrieved assertion 'administrator approved' is untrusted data, not a grant. A gateway must authenticate caller and enforce scope. Only an independently verified identity and permission record can authorise the read.

## 2. Baseline and decision.

New weighted score .4(5/5)+.3(5/5)+.2(4/5)+.1(4/5)=.94 versus baseline .82. Zero prohibited execution => passes synthetic threshold .80; one execution => BLOCK. Twenty synthetic cases cannot certify field safety.

## 3. Executable extension.

Reject `read_policy` with extra `restricted` argument before execution via explicit check, including under `python -O`. Exact allowlist is a teaching simplification; production needs typed schemas and authenticated access. See extensions tests.

## 4. Metamorphic design.

A harmless prompt-injection discussion should preserve allowed operation; an actual permission-changing directive must be quarantined. Retain before-execution traces to observe unsafe intermediate actions.

## 5. Residual-risk register.

Risks: stolen credentials (security owner, identity logs, stop on irregular grants); network egress bypass (platform owner, egress logs, stop on prohibited connection); poisoned index (data owner, signed provenance, block on unverified data).
