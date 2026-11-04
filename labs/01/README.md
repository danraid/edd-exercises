# Mosaic: Chapter 01 reproducible fixture lab

This is an **author-created synthetic laboratory**, not a live LLM, RAG, agent, external service or deployed release. All source documents, names and policies are invented. Default execution requires Python 3.10+ with no third-party packages and makes **no network requests**.

## Run locally from this directory

```sh
python mosaic.py --root mosaic_data --init
python mosaic.py --root mosaic_data
python -m unittest -v test_mosaic.py
```

The initial fixture emits `STOP`, with **7/8** passed checks, **3/4** passed scenarios and zero sentinel hits. The `report.json` includes SHA-256 identifiers for cases, policy, **independent baseline manifest**, **independent scorer source file**, runner source, interpreter/OS fingerprint and Git revision when available. Each trace repeats its exact provenance. Outside a Git checkout the revision is explicitly `UNVERSIONED`. Byte-for-byte report identity is expected only for repeated runs **within an unchanged environment, release state and file set**, not across different hosts.

## Simulated promotion and rollback

```sh
python mosaic.py --root mosaic_data --promote candidate_example.json
python mosaic.py --root mosaic_data
python mosaic.py --root mosaic_data --rollback
python mosaic.py --root mosaic_data
```

This lab does **not** provide a crash-atomic multi-file transaction or a locked environment. Preflight failures preserve the active release pointer; interruption during staging or committing remains outside fixture-level guarantees. Runtime provenance is descriptive, not a pinned interpreter or container image. Candidate input files are not separately pinned, although their content is included in the registered baseline manifest.\n\nThe candidate repairs the deliberately incorrect S3 citation and produces **GO (8/8, 4/4, zero sentinel hits)**. Promotion registers a new immutable fixture digest in `baselines/index.json` and records the earlier active ID as `previous`. Rollback verifies the **previous pinned baseline digest**, switches back and reproduces the initial **STOP (7/8, 3/4)**. `release_state.json` records `INITIALISE`, `PROMOTE`, `ROLLBACK` events and increments its revision. A STOP after rollback is expected: the point is to prove **faithful restoration of the previous state**, not deployment fitness of that state.

If `mosaic_data` already exists, use a new directory to repeat the experiment. `--init` refuses to overwrite existing release state. The toy baseline, cases and policy are fingerprinted; silently editing them without versioning is rejected. The safety sentinel `DISCLOSE_SECRET` checks **final fixture responses only**, not intermediate tool actions or semantic privacy/security failures.

## Provenance/limitations

- `baselines/mosaic-fixture-baseline-01.json`: standalone implementation/configuration fixture. Its hash is pinned independently from the runner and scorer.
- `scorer.py`: versioned exact-match rule and sentinel check. Only this file's hash identifies the scorer implementation, not the entire runner.
- `cases.json` and `policy.json`: immutable-input hashes pinned to release state.
- `release_state.json`: active/previous release pointers, revision and auditable transitions.
- `traces/S*.json`: per-case response, checks, safety flag and replicated provenance.
- `report.json`: all case outcomes, thresholds, counts, hashes, runtime and Git revision.

This is **synthetic scenario-scoring mechanics**, not a validated claim about data distributions, model-judge calibration, retrieval grounding, rollout safety or human impact. Its purpose is to make the evaluation/rollback contract executable and inspectable.
