# Handoff: reasoner-pilot - 2026-09-10

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Working tree clean. This is the Black M2 Air. The last substantive commits are #115 to #118,
  Astra's sixth document round; everything after them is this handoff. Pushed 2026-09-10; local and origin agree. Five
  sessions since the last full handoff, 2026-09-08 (second), two on 2026-09-09 and two on
  2026-09-10. Every repository under `~/Code/` is now cloned on this Air, `reasoner-study` and
  the site's included.
- **The published record reproduces**, run 2026-09-10 here after #106 to #118 moved the
  in-language artifacts on prose alone, re-pinned each time in a commit that says so, and earlier after #103 moved the
  viewer payload's pin, and on 2026-09-09 in a fresh clone that had no run files: 20 regenerated outputs reproduced (the pilot's 15, the four in-language appendix
  artifacts and the viewer payload, all from the committed ratings dataset), 14 committed-only
  verified, the 47 pinned condition means rebuilt from the dataset, and every generated section
  of the document matching its artifact. The full harness takes about a minute.
- **The report and its appendix are one document**, `papers/inlanguage-mfq2-DRAFT.md`, titled
  "Eleven language models take the MFQ-2 in English and six translations, with and without a
  country to answer as" (decision 20; the title is Declan's, 2026-09-08). The appendix file is
  gone. `validity/splice_appendix.py` splices the ten generated sections and the harness runs its
  check.
- **Fifteen review rounds are adjudicated and worked through**, all in `reviews/`: Astra's first to
  sixth on the document (the fifth on 2026-09-10, seven findings, seven tickets, #106 to #112,
  closed the same day, then #113 and #114; the sixth the same day on the state after #114,
  three findings and six small items, four tickets, #115 to #118, closed the same day: the Egypt
  increment is the condition's score, the Summary opens on the five-of-six observation, the
  Ireland paragraph leads with the cancellation, and Astra's read is "close to ready for release
  as an exploratory report" after "a final precision edit"; heading now "Framing moves the binding composite",
  B3 gains the Loyalty-Authority comparison with distances in human SDs, sixteen above and four
  at or below with Ireland the only sign change, d from -1.28 to +1.97, and the human reference
  builders now ship in `validity/reference/`, Declan's decision of 2026-09-10 reversing #108's
  link-and-recipe wording), Grok's paper round, DeepSeek's, Gemini's, Kimi's first to third, Claude's
  cold read of 2026-09-08, Grok's viewer round of 2026-09-09 (no change) and Astra's viewer round
  of 2026-09-10 (six findings, six tickets, #99 to #104, all closed the same day, plus #105 from
  the record's leftovers). One hundred and eighteen issues have existed; none is open.
- **The September wave is collected, archived and reported** (decision 21, #83): the framing
  template with its country slots deleted, on ten models, with same-day reruns of the unframed
  comparator and English-framed Egypt on identical item orders. B4a and the viewer's Control tab
  carry it: the template alone lifts the composite +0.652 [+0.459, +0.876], ten of ten up, about
  36 percent (model-resampling sensitivity 29 to 44) of the unframed-to-Egypt difference; naming
  Egypt adds +1.141 on a questionnaire file that also changed; drift +0.023 unframed, -0.017
  framed; spread 0.13 under the template against 0.30 unframed and 0.20 framed as Egyptians.
  DeepSeek-V4-Pro left Together's serverless tier after August and is absent. No temperature
  sent, none reported. Run files tracked under `validity/runs_neutral_template/` and archived at
  `archive-reasoner-pilot-validity/2026-09-08-september-wave/`, restore-tested.
- **The integer ratings are a published dataset** (decision 19): `validity/results/mfq2_ratings.csv`,
  104,400 rows, 53 conditions, with `results/collection_record.json` (failed calls, the rounding
  audit, the translated instructions as sent, token usage, collection dates). Both appendix
  emitters and the viewer builder read those two files and nothing under `runs*/` (#71, #92);
  the harness regenerates their outputs (decision 22). Only `build_ratings_dataset.py` needs the
  run files.
- **The MFQ-2 viewer**, `validity/viewer.html`, served from `validity/` (it fetches its payload):
  six tabs including Control; legends say what each mark represents; prose aligned with the
  document; every number checked against the payload, the record, the appendix or the document
  on 2026-09-09; clean at desktop, 640 and 375 pixels as of that date. Since Astra's round on
  2026-09-10: the headline story is the English-framed arm and says so; a translated arm gets a
  human marker only in the language the reference sample answered in (decision 18, #99); the
  document's three measurement qualifications sit under the first chart; the Foundations tab
  opens with a language-against-framing table on the composite, built from a new
  `language_contrasts` block in the payload whose twelve figures match the document's two tables;
  the matrix tab is "Every framed cell"; the footer links the document and the dataset. The
  changed tabs were screenshotted at 375 pixels on 2026-09-10 and are clean: no horizontal body
  scroll, wide tables scrolling in their own containers, footer links inline with padded hit
  boxes. #105 removed the one text under the 15 px floor; a computed sweep of the rendered page
  puts the minimum at 15. The root `viewer.html` is the Reasoner pilot's and is unrelated.
- `DECISIONS.md` holds 22 entries. 12 is superseded by 18 (Morocco reported under Spanish), 14
  by 22 for the emitter outputs. 17 (published means a DOI and the site) still gates everything.

## What changed outside the repository

The Atari et al. accepted manuscript, the Zewail et al. PMC full text and the Swiss Federal
Statistical Office's 2025 languages publication were read to verify reviewer facts. The AWS
session was renewed by Declan on 2026-09-09 and the wave archived. Model API calls: 2 preflight,
10 availability checks, 150 for the wave, all 2026-09-08; nothing else spent. On 2026-09-09 Astra
was asked to review the viewer and exhausted Declan's usage window without returning a response;
a free Grok instance did a round that day, and Astra's completed review arrived on 2026-09-10 at
`~/Documents/Codex/2026-09-10/tw/outputs/viewer-review.md` and was worked through. Later on
2026-09-10 Declan pasted Astra's fifth document round, which had recomputed from the clone's
ratings CSV. For #113, Atari et al.'s Study 2 respondent file was downloaded from OSF (9dwzt,
546 KB) into the gitignored `_raw/` of both this repository and `reasoner-study`, and a scratch
`venv/` with `pyreadstat` was created here for the Iran builder. `reasoner-study` gained the
Loyalty-Authority columns in its dispersion builder and CSV (its #1, commit `4f65f14`, pushed
on Declan's word the same day). Astra's sixth round arrived after that push and ran the shipped
builders itself. No model API calls on 2026-09-10; nothing spent.

## The tracker

Empty. #1 to #118 are closed, each with its disposition on the ticket.

## Next session

Nothing is queued for an agent.

1. **Zenodo**, the gate on calling any of this published (decision 17). `LOCATIONS.md` carries
   three `TBD`s and `CITATION.cff` a commented `doi:`. One document now, so one deposit.

The viewer's external rounds are done: Grok, 2026-09-09, no change; Astra, 2026-09-10, six
findings fixed (`reviews/astra-viewer-review-2026-09-10.md`). The viewer restates B4a, B3a, B6 and
B6a, now with the document's lead language-against-framing contrast, and adds nothing the
document does not carry except the per-model token table. Declan declined the unframed
instrument difference on the Control tab and the Loyalty-and-Authority table. The viewer as it
stands after #99 to #105 has not been read externally. Astra's sixth round read the document at
`8d058ad`, after #114; the state after #115 to #118 is unread, and every change in it is a
sentence Astra asked for.

**Declan's read at close, 2026-09-09:** the MFQ-2 document is one external round and a day of
release mechanics from ready, not a rewrite away. Before a DOI: one external read of the final
state (Astra's fourth-round fixes, the appendix sweep and the Control tab are unread by any
external reviewer; Grok's viewer round read the document at `3acd2cd` but as the viewer's
reference, not as a review of it), a PDF of the document with its tables and the non-Latin
instructions in B1a checked by eye, and pinned artifacts for the two hand-written tables (d and
Ordering). The Reasoner pilot paper and appendix have had no prose pass and predate the register
rules; they
get their own editing session before anything is called complete, and moral-os.com's card
follows them. The site's repository is now cloned on this Air (`~/Code/moral-os-website`) but is not set up
with research-kit; that is a separate session too. Chrome with the Claude extension works from here
under this account and reaches Declan's Zenodo login; nothing was deposited.

Left as disclosure, Declan's decision: the English-framed arm on the official questionnaire
(#53 states the confound; a rerun would be ten models in a second window). Not run: the six
translated country-free templates (decision 21 explains; they need translations first).

Candidates for tickets, not filed: a tracked claim-check for the paper's hand-written tables (the
d table and the Ordering table are still not emitted; the dataset makes such a check runnable
from a clone); the `[*]` versus `[d18]` marker asymmetry; the viewer's Every framed cell tab has
no September column, by design; from Astra's fifth round, the
same-instrument three-arm collection (unframed, template, Egypt template, one window, spending);
and the caveat-consolidation sweep, deferred to the editing session.

## Open items

- Sampling temperature is unset and unrecorded in the grid; the wave kept it that way on purpose
  (decision 21) and recorded that no provider returns one. Any collection that is not matched to
  the grid sets and records it.
- API keys on this Air are exported in the interactive shell; `~/.config/ccas/keys.env` does not
  exist here (notes updated).
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.

## Unresolved - needs a decision

Zenodo, item 1 above. Everything else settled.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**Rules learned by breaking them, all in `docs/DEVELOPMENT_NOTES.md`:** check a generator's exit
code before copying its output, a `set -e` chain does not do it inside `( ... && ... )`; the
builder's `mean` takes a list, not a generator (hit twice); sort the keys of any dict a bootstrap
draws from (the B3a and viewer intervals had taken their order from the filesystem and moved by
up to 0.003 when sorted, `d4d2b83` and `555189f`); never redirect a generator into its tracked
output; assert every anchor before writing any file.

**Corrected on the record, 2026-09-10:** the viewer's Models tab drew Morocco's human marker on
the Arabic-framed arm, a comparison decision 18 excludes (#99, `4649a42`); its headline story
summarised the translated arm where the document's table is English framing (#101, `59bb943`).

**Corrected on the record, 2026-09-08 and 2026-09-09:** a Summary sentence pushed on the 8th said the template's
spread was tighter than under any country when four framed conditions were tighter (`385a4f8`);
the rewrite of the 9th attached "two thirds of the range" to the Arabic figure (Astra 4, #84);
the same rewrite called Egypt the largest contrast when Saudi Arabia and the Emirates exceed it
(#90); a French run-noise sentence compared a single-model five-run SD with a six-country average
(#90); the viewer's Control tab rendered a date as "[object Object]" (fixed before push).

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design.
- The viewer's per-model token table has no counterpart in the document.
