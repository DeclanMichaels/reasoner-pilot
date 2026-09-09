# 014 - The validity outputs are pinned as committed, not as regenerated

**Date:** 2026-09-07
**Status:** superseded by #22 for the four emitter outputs

## The decision

`analysis/reproduce_manifest.json` now has two groups, and `analysis/test_reproduce.py` reports
them separately:

- **`regenerated`** - the 15 pilot outputs. The harness re-runs the five `analysis/` scripts,
  then hashes what they wrote. A mismatch means the numbers moved.
- **`committed_only`** - the 16 files in `validity/results/`. Hashed exactly as committed. The
  harness does not attempt to recompute them. A mismatch means something rewrote them.

The two are never merged into one count. The pass line names both.

## Why

The validity module's outputs are derived from run data that is gitignored, because the item
wording in it is not ours to redistribute (decision 7). They therefore cannot be recomputed on a
fresh clone, or on any machine that does not hold the grid, and `test_reproduce.py` is the one
command in this repository that a reader is promised will work with no keys and no network.
Adding the validity scripts to the harness would break that promise for everyone who clones.

Leaving the outputs unpinned was the status quo, and it is what let the 2026-09-05 failure
through. `audit_inlanguage.py` run against a partial three-language restore rewrote
`validity/results/condition_means.json` from 26 conditions to 11, dropping every Spanish, French
and Russian condition and three of the four Arabic ones. It exited clean and printed RECONCILED,
because it reconciles whatever it can see. Committed, that file would have reproduced perfectly
against itself. A hash pinned in git is the only check that fires on that, because the corruption
is internally consistent and only the comparison to the previous state reveals it.

So the guarantee on the second group is weaker on purpose: it is a tamper check, not a
recomputation check. That is worth having, and worth labelling, because a single count of 31 would
claim a strength 16 of them do not have.

## Rejected alternatives

**Add the validity scripts to `SCRIPTS` in the harness.** Rejected: they need the gitignored grid,
so the harness would fail for every reader on a clean clone, and the README's central claim about
reproduction would stop being true.

**Add the 16 hashes to the existing flat manifest and change nothing else.** The code needed no
change and the run would have reported "31 reproduced". Rejected: the word is false for 16 of
them, and the next person to read that line would reasonably conclude the validity numbers
recompute from data.

**Leave them unpinned and rely on `git status`.** That is the current instruction in
`docs/DEVELOPMENT_NOTES.md`, and it depends on a human running it at the right moment. It did not
fire on 2026-09-05.

## Consequences and gotchas

Regenerating the in-language appendix will move files in `committed_only`, and the harness will
fail. **That failure is correct and expected**, and the fix is never to edit a hash to match. Run
the regeneration with the full grid present, confirm the new numbers on their merits, re-pin, and
say in the commit that an output moved and why - the published-number rule in `CLAUDE.md` governs,
not this entry.

Re-pinning is a deliberate act. There is intentionally no `--update-manifest` flag; a one-command
way to make the check agree with whatever is on disk would defeat the entry.

The harness verifies the second group on a machine that does not hold the grid, including a fresh
clone, because it only reads committed files. It says nothing about whether the right run data was
present when those files were last generated. Issue #5 covers that question.

---

**Superseded by #22 (2026-09-09)** for `appendix_tables.md`, `appendix_b4_b5.md`, `condition_means.json` and `inlanguage_audit.txt`, which the harness now regenerates from the committed dataset; stands for everything else.
