# 019 - The integer ratings are published as a dataset; the run files and item wording are not

**Date:** 2026-09-08
**Status:** active

## The decision

Every scored rating in the in-language grid is committed as one tidy dataset keyed by model,
condition, iteration, item id and value, with seed and presentation order, and no item text and
no raw reply. A check script rebuilds `validity/results/condition_means.json` from it and
`analysis/test_reproduce.py` runs that check. The run files stay gitignored and archived in S3.

## Why

The appendix claimed the model-side numbers regenerate from the raw runs, and a fresh clone
could not do it: the runs are gitignored under decision 7 and the test hashes the committed
artifacts under decision 14. Astra's third round called the claim overstated, and it was. Item
ids and integers carry none of the wording decision 7 protects, so the dataset sits on the
public side of that boundary and makes the claim true rather than narrower.

## Rejected alternatives

Narrowing the claim and pointing to the S3 archive. Accurate, and it leaves every in-language
number unreproducible from the repository readers actually have.

Committing the run files. They carry the model's raw replies and the system prompts, and decision
7 keeps them local; the dataset is the clean cut.

## Consequences and gotchas

The dataset is derived from the runs by a builder and is regenerated whenever the runs change,
which under the read-only rule is never. The audit scripts still read the run files; moving them
to the dataset is a separate ticket, and until it lands the reconstruction check is the bridge
between what a clone has and what the appendix reports.

## Supersedes / amends

Amends decision 7 by naming the integer ratings as derived results that are published. The
wording clause of decision 7 stands in force.
