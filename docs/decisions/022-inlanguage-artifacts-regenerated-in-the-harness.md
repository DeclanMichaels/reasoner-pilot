# 022 - The in-language emitters' outputs are regenerated in the harness, not hashed as committed

**Date:** 2026-09-09
**Status:** active

## The decision

`analysis/test_reproduce.py` runs `validity/build_appendix_tables.py` and
`validity/audit_inlanguage.py` and compares their four outputs byte for byte with the manifest:
`results/appendix_tables.md`, `results/appendix_b4_b5.md`, `results/condition_means.json` and
`results/inlanguage_audit.txt`. The harness captures each emitter's standard output to a temporary
file and requires a clean exit before it writes anything tracked. The dataset builder's two
outputs, `results/mfq2_ratings.csv` and `results/collection_record.json`, and the rest of the
validity module's results stay hashed as committed, since they need the run files or other
inputs a clone does not have.

## Why

Decision 14 hashed the validity outputs because a partial-data run could rewrite one silently
and a clone could not regenerate them at all. Since #71 the two emitters read only the committed
dataset and collection record, so a clone regenerates them, and the partial-data failure cannot
happen: the dataset is complete or the builder's assertions fail. Regenerating in the harness is
what makes the reproducibility statement in B9 a tested claim rather than a described one.

## Rejected alternatives

Leaving the four hashed. Accurate but weaker: a hash proves the file did not change, not that the
code and data still produce it.

## Consequences and gotchas

The harness now takes about as long as the audit's bootstraps. A change to either emitter or to
the dataset that moves a number fails the harness, which is the point; re-pin deliberately and
say what moved. The builder still needs the run files and is run by hand after a collection.

## Supersedes / amends

Supersedes decision 14 for the four emitter outputs. Decision 14 stands for the builder's two
outputs and for `aggregation_artifact.json`, `convergent_validity.*`, `domain_scenario_audit.md`,
`english_baseline_audit.txt`, `inlanguage_grid_audit.txt`, `inlanguage_mfq2.md`,
`instrument_scores.json`, `model_vs_human_profiles.md`, `reasoning_cost.txt`,
`society_framing_mfq2.md` and `viewer_data.json`.
