# 008 - The compression aggregation artifact is measured, and nothing published is corrected

**Date:** 2026-08-18
**Status:** active

## The decision

Model positions are means of five reruns compared against single human responses, which inflates
the compression ratio. Measured rather than argued: correcting it moves the four ratios from
6.77, 7.70, 5.37 and 5.65 to 6.32, 7.25, 5.03 and 5.14, a reduction of 6 to 9 percent. The
action is a limitations paragraph. Nothing published needs correcting.

## Why

For the ratio to fall to 3.0, human within-person noise would have to be 64 to 83 percent of
observed human variance. The artifact is real and small enough that the finding survives it.

## Consequences and gotchas

Computed by `validity/aggregation_artifact.py`, cross-checked against `model_scores.csv`.
