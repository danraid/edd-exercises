# Mosaic dataset lab

Run: python mosaic_lab.py

Inputs: synthetic fixtures embedded in mosaic_lab.py.
Outputs: cases.json and manifest.json, written locally.
Tests: standard-library unittest tests run by the script.

Acceptance: tests pass; validation returns no errors; every case
has a rationale; no identifier or normalised question is duplicated anywhere in the dataset,
including within the same split or across different splits.
The manifest records the canonical dataset and script SHA-256 hashes.
This visible holdout is a teaching fixture, not an access-controlled release holdout.
Do not treat these fixtures as a protected operational holdout.
