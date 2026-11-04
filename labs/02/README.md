# Mosaic Chapter 02: independent approval and tamper-evident evaluation

This is a **synthetic, deterministic educational fixture**. It does not evaluate a real model, agent, or live deployment, and does not supply production safety guarantees.

## Roles and trust model

- `runner.py`: candidate-owned producer; writes a non-overwriting JSON manifest, but **does not certify it**.
- `scorer.py`: candidate-side deterministic score function.
- `policy.json`, `fixtures.json`: example policy, cases and outputs.
- `trusted_approval.json`: simulated independently approved digests of policy, fixtures and code.
- `verify.py`: separately invoked verifier, whose source SHA-256 must be pinned by independent CI; checks an **externally supplied** SHA-256 of the approval root, rechecks policy, fixture, runner and scorer hashes, and recomputes results independently of the scorer. With a verifier-held key, it creates an HMAC attestation.
- `test_mosaic.py`: deliberately changes candidate code, policy, approval and manifest to ensure the verifier refuses unsafe substitutions.

The `trusted_approval.json` fixture is stored alongside the lab only for **reproducibility**. In real CI, neither the candidate nor its build job may modify the trust anchor, reference digest, verification code, key, or decision about what constitutes approval. Those must come from a protected and independently administered job, protected branch or signing service. A self-calculated digest is not an approval.

The separately pinned demonstration approval SHA-256 is:

`73d86bf1d7d411054a44df086776b7237753878984338e8023f7463291dd1d5d`

This SHA is hard-coded in the unit-test fixture rather than derived from candidate code. It is **not** protected against someone who can modify both the trusted tests and the candidate. That stronger adversary is outside this tutorial's trust boundary.

## Run (Python 3.9+, no external packages)

From the repository root:

```bash
python -m unittest discover -s labs/02 -p test_mosaic.py -v
python labs/02/runner.py --output lab-output/manifest.json
MOSAIC_ATTESTATION_KEY='local-demo-only' python labs/02/verify.py \
  --manifest lab-output/manifest.json \
  --approval labs/02/trusted_approval.json \
  --anchor-sha256 73d86bf1d7d411054a44df086776b7237753878984338e8023f7463291dd1d5d \
  --attestation lab-output/attestation.json
MOSAIC_ATTESTATION_KEY='local-demo-only' python labs/02/verify.py \
  --manifest lab-output/manifest.json \
  --approval labs/02/trusted_approval.json \
  --anchor-sha256 73d86bf1d7d411054a44df086776b7237753878984338e8023f7463291dd1d5d \
  --attestation lab-output/attestation.json --check-only
```

For repeat executions, choose a new output pathname. The runner and attestation writer use exclusive creation; they **only prevent accidental overwrite**. They do not create immutable storage. To prevent undetected modifications after storage, store the attestation in a separate protected location and keep the signing key secret from the candidate. To ensure durable immutability, configure a real append-only or object-lock storage policy and test its enforcement independently.

Expected synthetic result: baseline `GREEN` with 2/3 correct, candidate `RED` with 3/3 correct but an injected unsafe flag. The unsafe flag is an artificial test label, not an autonomous classifier. A green fixture result is not a statistical confidence interval or evidence of deployment fitness.

## Reproduced checks

1. Nominal case is green baseline, red candidate, independently verified and sealed.
2. Duplicate output path does not overwrite an existing manifest.
3. Post-write manifest tampering fails verification.
4. Candidate scorer modification fails approved-source digest verification.
5. Simultaneous policy and local-approval modifications fail the independently pinned approval hash.
6. Tampered HMAC attestation fails verification.
7. Runner modification fails approval verification.

Only the protected CI role should ever receive a real attestation secret. Do not put it in this repository.

The independent CI additionally verifies the exact SHA-256 of `verify.py` before running any acceptance test. The adversarial suite modifies verifier code to ensure this separate pin rejects it.
