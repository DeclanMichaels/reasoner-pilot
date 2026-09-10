# Handoff: reasoner-pilot - 2026-09-10 (fifth)

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Working tree clean. This is the Black M2 Air. The last substantive commit is `1f9274c`, the
  MFQ-2 document rendered to PDF with its recipe; everything after it is this handoff. Pushed
  2026-09-10; local and origin agree. Six sessions since the last full handoff, 2026-09-08
  (second): two on 2026-09-09 and three on 2026-09-10 before this one. Every repository under
  `~/Code/` is cloned on this Air.
- **The document has a PDF**: `papers/inlanguage-mfq2-DRAFT.pdf`, 44 pages, Letter, the render of
  `papers/inlanguage-mfq2-DRAFT.md` at `1f9274c`. It is built by `papers/render.sh`, the
  Python-Markdown plus WeasyPrint recipe from `rcp-experiment/papers`, adapted in
  `papers/render_html_pdf.py` for this document (right-to-left Arabic and Farsi quotes, verbatim
  prompts unhyphenated and kept with their label, table headers kept with their rows, `<int>`
  placeholders escaped). Checked by eye on the first page, the B1a page with the six translated
  instructions, the B3a, B6 and B6a tables and the last page; a sweep found no text outside any
  page and no heading stranded at a page foot. The document itself did not change. **The PDF is
  not checked by the harness**: after any change to the document, re-run the recipe and commit the
  new render with it, or the PDF is stale and looks current.
- **The published record reproduces**, run 2026-09-10 after #106 to #118 moved the in-language
  artifacts on prose alone, re-pinned each time in a commit that says so, and on 2026-09-09 in a
  fresh clone that had no run files: 20 regenerated outputs reproduced (the pilot's 15, the four
  in-language appendix artifacts and the viewer payload, all from the committed ratings dataset),
  14 committed-only verified, the 47 pinned condition means rebuilt from the dataset, and every
  generated section of the document matching its artifact. Not re-run this session; nothing under
  `analysis/` or `validity/` changed.
- **The report and its appendix are one document**, `papers/inlanguage-mfq2-DRAFT.md`, titled
  "Eleven language models take the MFQ-2 in English and six translations, with and without a
  country to answer as" (decision 20). `validity/splice_appendix.py` splices the ten generated
  sections and the harness runs its check.
- **External review of the document is finished, Declan's decision of 2026-09-10**: fifteen rounds
  are adjudicated and worked through in `reviews/`, and the later rounds were returning nitpicks,
  repeats and points already answered. Astra's sixth round read the document at `8d058ad`; the
  state after #115 to #118, every change in it a sentence Astra asked for, has not been read
  externally and will not be sent out. One hundred and eighteen issues have existed; none is open.
- **The September wave is collected, archived and reported** (decision 21, #83): the framing
  template with its country slots deleted, on ten models, with same-day reruns of the unframed
  comparator and English-framed Egypt on identical item orders. B4a and the viewer's Control tab
  carry it. Run files tracked under `validity/runs_neutral_template/` and archived at
  `archive-reasoner-pilot-validity/2026-09-08-september-wave/`, restore-tested.
- **The integer ratings are a published dataset** (decision 19): `validity/results/mfq2_ratings.csv`,
  104,400 rows, 53 conditions, with `results/collection_record.json`. Both appendix emitters and
  the viewer builder read those two files and nothing under `runs*/` (#71, #92); the harness
  regenerates their outputs (decision 22). Only `build_ratings_dataset.py` needs the run files.
- **The MFQ-2 viewer**, `validity/viewer.html`, served from `validity/`: six tabs including
  Control; every number checked against the payload, the record, the appendix or the document on
  2026-09-09; clean at desktop, 640 and 375 pixels; text floor 15 px after #105. Its external
  rounds are done: Grok 2026-09-09 (no change), Astra 2026-09-10 (six findings, #99 to #104,
  fixed). The root `viewer.html` is the Reasoner pilot's and is unrelated.
- `DECISIONS.md` holds 22 entries. 12 is superseded by 18 (Morocco reported under Spanish), 14
  by 22 for the emitter outputs. 17 (published means a DOI and the site) still gates everything.

## What changed outside the repository

The PDF recipe was found in `~/Code/claude-continuity/4_toolbox.md`, which points at
`~/Code/rcp-experiment/papers/render.sh`; a Chrome-headless render built before that check was
discarded. The scratch `venv/` here gained `markdown`, `weasyprint` and `pymupdf` (the last used
only to rasterise pages for checking; there is no PDF rasteriser on this Air otherwise, and the
desktop app's Browser pane treats a PDF as a download). `papers/.render-venv/` is the recipe's
own environment, gitignored. Declan noted that the desktop app should be pointed at `~/Code/`,
the root holding every repository, rather than at one project folder, so the sibling
repositories and the toolbox are in reach. No model API calls; nothing spent. Nothing was
deposited anywhere.

## The tracker

Empty. #1 to #118 are closed, each with its disposition on the ticket.

## Next session

Nothing is queued for an agent. Declan's plan at close, 2026-09-10:

1. **The Reasoner pilot writeup and collateral.** `papers/reasoner-pilot.md` and
   `papers/reasoner-appendix.md` have had no prose pass and predate the register rules; their
   PDFs were printed through Chromium on 2026-09-04 and should come from the recipe once the
   prose is settled. moral-os.com's card follows them. The site's repository is cloned here
   (`~/Code/moral-os-website`) and is not set up with research-kit; that is its own session.
2. **Zenodo, held.** Declan held the DOI on 2026-09-10 until the pilot writeup is finished. Of the
   three gates his 2026-09-09 read put before a DOI, the PDF is done, the external read of the
   final state is waived by the decision above, and pinned artifacts for the two hand-written
   tables (d and Ordering) are still not done. `LOCATIONS.md` carries three `TBD`s and
   `CITATION.cff` a commented `doi:`. One document, so one deposit; what the deposit is, the
   repository snapshot `LOCATIONS.md` describes or the document alone, is undecided.

Left as disclosure, Declan's decision: the English-framed arm on the official questionnaire
(#53 states the confound; a rerun would be ten models in a second window). Not run: the six
translated country-free templates (decision 21 explains; they need translations first).

Candidates for tickets, not filed: a tracked claim-check for the paper's hand-written tables (the
d table and the Ordering table are still not emitted; the dataset makes such a check runnable
from a clone); the `[*]` versus `[d18]` marker asymmetry; the viewer's Every framed cell tab has
no September column, by design; from Astra's fifth round, the same-instrument three-arm
collection (unframed, template, Egypt template, one window, spending); and the
caveat-consolidation sweep, deferred to the editing session.

## Open items

- Sampling temperature is unset and unrecorded in the grid; the wave kept it that way on purpose
  (decision 21) and recorded that no provider returns one. Any collection that is not matched to
  the grid sets and records it.
- API keys on this Air are exported in the interactive shell; `~/.config/ccas/keys.env` does not
  exist here (notes updated).
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.

## Unresolved - needs a decision

What the Zenodo deposit is, item 2 above, when the DOI is unheld. Everything else settled.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**Rules learned by breaking them, all in `docs/DEVELOPMENT_NOTES.md`:** check a generator's exit
code before copying its output, a `set -e` chain does not do it inside `( ... && ... )`; the
builder's `mean` takes a list, not a generator (hit twice); sort the keys of any dict a bootstrap
draws from (the B3a and viewer intervals had taken their order from the filesystem and moved by
up to 0.003 when sorted, `d4d2b83` and `555189f`); never redirect a generator into its tracked
output; assert every anchor before writing any file; re-render the PDF after every change to the
document.

**Corrected on the record, 2026-09-10:** the viewer's Models tab drew Morocco's human marker on
the Arabic-framed arm, a comparison decision 18 excludes (#99, `4649a42`); its headline story
summarised the translated arm where the document's table is English framing (#101, `59bb943`).

**Corrected on the record, 2026-09-08 and 2026-09-09:** a Summary sentence pushed on the 8th said
the template's spread was tighter than under any country when four framed conditions were tighter
(`385a4f8`); the rewrite of the 9th attached "two thirds of the range" to the Arabic figure
(Astra 4, #84); the same rewrite called Egypt the largest contrast when Saudi Arabia and the
Emirates exceed it (#90); a French run-noise sentence compared a single-model five-run SD with a
six-country average (#90); the viewer's Control tab rendered a date as "[object Object]" (fixed
before push).

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design.
- The viewer's per-model token table has no counterpart in the document.
- The document carries its byline as a closing line; the pilot PDFs put author, affiliation and
  year under the title. Left as the file has it.
