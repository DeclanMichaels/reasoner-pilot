# Decision log - the Reasoner pilot

Every decision that needed a why, in the order it was made. This file is the **index**: one row
each, with a link to the full entry. The full text lives in [docs/decisions/](docs/decisions/).

Read this index in full each session; open a detail file whenever the work touches its area.

## Conventions

- **Append new decisions at the bottom** - a detail file plus an index row.
- **Entries are never deleted or rewritten.** Superseding is the only mechanism: a new numbered
  entry, a status flip on the old row, and a marker in the old detail file. An entry that supersedes
  only part of an earlier one says which part, and the rest stands in force.
- **Status** is `active`, `superseded by #N`, or `historic` (a completed one-time event with no
  ongoing constraint, kept because it explains how things got this way).

## What earns an entry

All three must be true: hard to reverse, surprising without context, and the result of a real
trade-off. What a thing **is** belongs in `CONTEXT.md`; a number, a correction, or a provider quirk
belongs in `docs/DEVELOPMENT_NOTES.md`.

## Provenance of this log

Written on 2026-09-05 by reconstruction, not by port. This repository had no decision log; the
entries below were recovered from commit messages and their bodies, the README, the papers, the
framing library's own description, and two settled entries held in `claude-continuity`. Dates are
the date of the commit or document that records the decision, not the date it was made in
conversation, and several were certainly made earlier.

**Nothing was decided during the reconstruction.** An entry here should be recognisable; if one is
not, it is a reconstruction error and the entry is wrong rather than the memory.

| # | Date | Status | Decision |
|---|------|--------|----------|
| 1 | 2026-07-19 | historic | [A global option-sign convention, fixed before release](docs/decisions/001-option-sign-convention.md) - every axis score's direction |
| 2 | 2026-07-20 | active | [The pilot is exploratory throughout, and says so](docs/decisions/002-exploratory-throughout.md) - the successor study's registered claims |
| 3 | 2026-07-20 | active | [The model is the unit, and reruns are averaged first](docs/decisions/003-model-is-the-unit.md) - panel figures against being dominated by verbose models |
| 4 | 2026-07-20 | active | [Every framed prompt uses one identical scaffold](docs/decisions/004-matched-framing-scaffold.md) - the cultural-versus-nonsense comparison |
| 5 | 2026-07-20 | active | [Nonsense framings name a principle without asserting a verdict](docs/decisions/005-nonsense-frames-assert-no-verdict.md) - the compliance finding against an easier explanation |
| 6 | 2026-07-20 | active | [Human responses are published, anonymised at collection](docs/decisions/006-human-data-published-anonymous.md) - respondents, and the reproducibility of the human side |
| 7 | 2026-07-20 | active | [Instrument item wording is not redistributed; derived results are](docs/decisions/007-item-wording-not-redistributed.md) - the licence position, without losing the results |
| 8 | 2026-08-18 | active | [The compression aggregation artifact is measured, and nothing published is corrected](docs/decisions/008-aggregation-artifact-accepted.md) - the published compression figures |
| 9 | 2026-08-20 | active | [The three absent panel models are disclosed, not back-filled](docs/decisions/009-absent-models-disclosed-not-rerun.md) - the collection's single-window integrity |
| 10 | 2026-08-21 | active | [A swapped model gets a distinguishable roster key](docs/decisions/010-roster-keys-are-distinguishable.md) - the meaning of a model name across collections |
| 11 | 2026-08-22 | active | [The English comparator is the matched cell, and the old one is kept as errata](docs/decisions/011-english-comparator-is-the-matched-cell.md) - the in-language contrasts |
| 12 | 2026-08-24 | active | [Morocco is compared on the Spanish arm and grouped with Arabic](docs/decisions/012-morocco-split-across-two-arms.md) - two analyses that want different arms |
| 13 | 2026-08-24 | active | [The fifteen-above, five-below shape is shown and not interpreted](docs/decisions/013-the-shape-stays-uninterpreted.md) - the report-scope rule, against three reviewers |
