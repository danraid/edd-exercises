# Chapter 3. Evaluation Datasets, Sampling and Leakage: Worked answers

Synthetic educational solutions, not deployment certification. [Questions](exercises.md) | [Lab](../../labs/03/README.md)

## 1. Boundary and assumption.

Using age in completed years on a fixed effective date: 17 -> ineligible; 18 -> eligible; 19 -> eligible. Record date, reference policy and rationale; 'almost 18' lacks sufficient date/time detail.

## 2. Coverage and baseline.

Two previously empty Bengali cells receive cases: coverage becomes 22/24=91.7% and count increases 120+6=126. Cell presence does not establish sampling representativeness.

## 3. Executable split control.

Require nonempty `family_id`; reject any same family across splits even for different text; allow within split. Translation/paraphrases of the same incident share an ID. See executable extension tests.

## 4. Release decision.

Baseline 100/120=83.3%, candidate 108/120=90%. Abstention falls 27/30=90% to 18/30=60%, Bengali is missing, and all-pass protected abstention gate fails: BLOCK. Repair, add Bengali cases and obtain population-based uncertainty before deployment claims.
