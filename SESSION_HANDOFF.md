# Handoff: reasoner-pilot - 2026-09-08

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Local and remote agree, and the working tree is clean apart from this file. The session's work
  is 40 commits since `303e79e`.
- **The published record reproduces**, run 2026-09-08, no keys and no network: 15 regenerated
  outputs reproduced, 17 committed-only outputs verified.
- **Six adversarial rounds on the in-language paper and appendix are adjudicated and worked
  through**, all in `reviews/`: Astra's first (sixteen tickets), Grok's (one), Astra's second
  (eight), DeepSeek's (folded into those eight), Gemini's (three) and Kimi's (six). Thirty-nine
  issues have existed; none is open.
- **The paper is titled** "Adding a country-role instruction shifts responses more than
  translating the questionnaire", Kimi's proposal, taken 2026-09-08. The viewer's title and
  heading match it, and its wording says reference sample where the paper does.
- **Every data section of the appendix is generated**: B1a, B4, B5 and B7 by
  `audit_inlanguage.py`; B2a, B3, B3a, B6 and B6a by `build_appendix_tables.py`. The splice map
  is in `docs/DEVELOPMENT_NOTES.md`. B4 is a 70-contrast set over the full grid with intervals,
  sign counts and leave-one-out ranges, no p-values (decision 15). There is no errata section
  (decision 17).
- `DECISIONS.md` holds 17 entries. This is the Black M2 Air; `validity/` holds the completed
  grid and `validity/reconcile.py` reports it identical to the 2026-09-05 archive.

## What changed outside the repository

`reasoner-study` received decision 27 and a README pointer to it, both pushed, private. Hazrati
et al.'s respondent-level SPSS files were downloaded from their view-only OSF project into the
gitignored `validity/reference/_raw/` and read with `pyreadstat` in a scratchpad virtualenv; only
the aggregate CSV is committed. The Atari and Hazrati preprints and the Zewail PMC text were read.
The viewer was rendered locally, on every tab, at desktop and phone widths.

No model calls, nothing written to S3, nothing spent.

## The tracker

Empty. #1 to #39 are closed, each with its disposition on the ticket. Where a ticket was closed
before its work had landed, the ticket carries the correction and the hash that did it.

## Next session

Nothing is queued for an agent. Declan is sending the current state for further external review.

1. **Review.** Five model families have read across six rounds. Every family raised the same
   four things - panel composition, temperature, five runs, the framing prompt's two components -
   and the documents state each where the reader meets it. Unread by anyone: the retitle, the
   viewer's title and wording, the four appendix lines fixed at close, and Kimi's six fixes.
2. **Zenodo**, and whether paper and appendix are combined first. `LOCATIONS.md` has three
   `TBD`s and `CITATION.cff` a commented `doi:`. Under decision 17 nothing here is published
   until that is done.

Candidates for tickets, not filed: a tracked claim-check that recomputes every number in the paper
(the script that did it for #2 lives only in the scratchpad); the `[*]` versus `[d12]` marker
asymmetry; `viewer_data.json`'s generation timestamp, which makes its pin detect re-runs rather
than data changes and stamps the viewer with the 7th; the appendix's hand-written Arabic-four
subsection still says "populations" where the generated sections say reference sample.

## Open items

- Sampling temperature is unset and unrecorded in the runners; B1a states this and that
  defaults are not reconstructed from documentation. Every reviewer's recommendation to pin it,
  raise the run count, add a country-neutral framing arm or harmonise seeding is a future
  collection's design and is recorded as not taken here.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.

## Unresolved - needs a decision

Item 2 under Next session. Iran's anchor is settled (decision 16); the title is settled.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**The audit scripts write tracked outputs.** A clean exit says nothing about whether the right
data was present; `reconcile.py` is the check. **Never redirect a generator straight into its
tracked output**; write to a temp file, check the exit code and the expected strings, then move it.
**Copy the audit's stdout to the trail only from a run that printed `wrote results/appendix_b4_b5.md`.**
**Multi-file edit scripts assert every anchor before writing any file.** All four rules are in
`docs/DEVELOPMENT_NOTES.md` and each was learned by breaking it on 2026-09-08.

**B1a is bound to the runner source.** A change to `run_validity.py`'s `SYSTEM` or
`run_framed.frame_system` changes the appendix or fails the emitter, on purpose.

**Things this workflow got wrong on 2026-09-08 and corrected on the record**, each in its commit
message: the first Iran SD build's inclusion rule (`afb185d`); Iran's anchor carried as open after
it was settled (decision 16); B1a's unframed-protocol sentence and the Iran caveat's attribution,
both the 7th's writing (#23, #25); the B10 strike breaking the emitter (`0cb58e0`); the Iran
re-attribution reaching only the paper (`8ef77a0`); the E2 sign quoted backwards (`052a05a`);
the language table's Farsi row, which two reviewers flagged and were told was well-formed after
the wrong table was checked (#34); and two consecutive commits, `6610467` and `19e35cf`, that
claimed appendix work their edit scripts had not done, one of them pinning a truncated artifact,
repaired in `6c72418`.

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules. Not
  restyled, since nothing in it was otherwise touched.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design; the
  builder's two gates are the record that it was computed the authors' way.
