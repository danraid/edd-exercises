# Chapter 10: Mosaic offline authority-boundary laboratory

This executable demonstration is a deterministic, synthetic broker test. It **does not** call an LLM, read real policies or documents, use a network or validate deployment security. It tests only explicitly specified request/permission outcomes.

Run from the repository root using Python 3.9+:

```sh
python labs/10/mosaic_safety.py
python -O labs/10/mosaic_safety.py
python -m unittest discover -s labs/10 -p test_mosaic.py -v
python -O -m unittest discover -s labs/10 -p test_mosaic.py -v
```

Expected cases, in order: `ordinary: answered`, followed by `authority_escalation`, `restricted_read`, `exfiltration`, `unknown_tool` all `denied`, then `All safety checks passed.`. The `malicious_tool_output: quarantined` line appears between `exfiltration` and `unknown_tool`, after a permitted synthetic read with untrusted returned instructions. The regression suite intentionally corrupts the expected result and verifies that the command **fails with a nonzero exit code** even under Python optimisation (`-O`).

**Invariant:** unauthorised tool requests, malformed retrieval fixtures, invalid policy structures and untrusted principals can never produce an executed operation. Separate boundaries enforce tool permission *before* the synthetic read and tool-output quarantine *after* the read but before the answer. A toy exact-match result schema is not general-purpose semantic prompt-injection detection. All executable safety/acceptance checks use explicit conditionals that raise `RuntimeError` on failure, not `assert` (which Python removes with optimisation).

**Limits:** the synthetic allowlist is loaded from trusted in-process configuration, not authenticated or validated against a production policy service. The tool output is a hard-coded string; no real secrets or network side effects exist. Do not use this fixture to claim that a real model resists prompt injection, that an application sandbox is secure, or that a small challenge matrix estimates deployment safety. Production systems require authenticated identities, immutable trusted policy distribution, restricted tool execution, security telemetry and redacted audit trails.
