# Handoff: reasoner-pilot - 2026-09-11

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Working tree clean. This is the Black M2 Air. Last commit `56889d4` (this handoff's previous
  revision); the last substantive ones are the website pass (in `moral-os-website`, `06dcd2d`),
  the pilot viewer read (`44619a7`), the claim-check (`4df3982`, corrected in `067fa8d`), and
  Astra's second round (#135 to #141). Pushed 2026-09-11; local and origin agree. Every
  repository under `~/Code/` is cloned on this Air.
- **Both papers are at the state the pre-publication pass leaves them**, with the DOI and the
  nudge the only items left (Next session). The Reasoner pilot paper (`papers/reasoner-pilot.md`,
  6-page PDF) and appendix (`papers/reasoner-appendix.md`, 15 pages) have had, on 2026-09-10 and
  11, a prose pass (`5961507`), a cold review, and six external rounds: Astra (twelve findings,
  #120 to #131), Gemini and Grok (nothing new), Kimi (the allocation-format sensitivity, #133,
  #134) and Astra again (#135 to #141: ties shared, three same-day corrections, the rerun
  approximation, the figure template). Records in `reviews/`, one file per round, each with its
  diff against the earlier ones. The title is "Eleven Language Models in a Narrow Band of a
  Moral-Judgment Instrument"; the Summary leads with the collapsed compression ratio (2.3 to 4.9,
  ties shared; 2.1 to 6.2 across three tie rules; 5.4 to 7.7 as scored), Declan's decision.
- **Corrected on the record this session**, in commit messages that quote the old wording: the
  human baseline's item exposure (58 respondents one scenario per axis, ten all twelve); the
  reshuffle claim; the A5 intervals (resampled models now, Cohen's d dropped); reasoning tokens
  (four models not reported, not zero); "p < 0.00001"; the o3-Llama country error; the five-model
  coding (cut; artifacts archived under `results/archive-five-model-2026-07/`); Kimi's geometry
  denominators; the exclusion statement; the recount at inflated SDs (0, 0, 0 and 1 of 100,000);
  the A3 ratio intervals (second decimal, sorted human order); five earlier claims in `5961507`.
- **The MFQ-2 document** (`papers/inlanguage-mfq2-DRAFT.md`, 44-page PDF) changed once, #119
  (`99ca5df`, the "tails too coarse" sentence Declan found after two adjudications had cleared
  it; the all-eleven clause scoped to Arabic). Its two hand-written tables are now emitted and
  spliced (#132). Fifteen external rounds, review finished by Declan's decision of 2026-09-10.
- **The published record reproduces and the prose is checked**: `python3 analysis/test_reproduce.py`
  passed at the last run (2026-09-11) with 20 regenerated outputs, 14 committed-only, 47
  condition means, every spliced section, and, new this session, `analysis/claim_check.py`,
  which fails on any number in either paper's prose that no artifact can produce. It matches by
  value, not meaning. `results/appendix_stats.json` was re-pinned six times today as the builder
  grew (exposure, exclusions, cluster intervals, token reporting, allocation style, tie rules,
  rerun selection, the recount); the A3 compression block never moved except its intervals.
- **All three PDFs are the recipe's** (`papers/render.sh`), re-rendered from the current text
  on 2026-09-11 and byte-identical to the committed files. Table rules in
  `papers/render_html_pdf.py`: a table of five data rows or fewer is never split; a short colon
  lead-in stays with its table or list; a table's last two rows are never orphaned. **The PDFs
  are not checked by the harness**: after any change to a document, re-run the recipe and commit
  the render with it.
- **moral-os.com carries both papers** (deployed 2026-09-11): the pilot page retitled with the
  current Summary, both pilot PDFs and the pilot viewer; the MFQ-2 page, PDF and refreshed
  viewer, **unlisted** (noindex, no sitemap, unlinked) until Declan lists them with the DOI.
- **The pilot viewer** (`viewer.html`, regenerated) was read against the final paper twice today
  and re-pinned each time; it says what the paper says about temperature, exposure and reruns.
- `DECISIONS.md` holds 23 entries. 23 (2026-09-11) is the Zenodo deposit: the repository
  snapshot, one DOI, both documents citing it. 17 still gates: published means the DOI and the
  site. 12 is superseded by 18, 14 by 22 for the emitter outputs.

## What changed outside the repository

- `moral-os-website`: one commit (`06dcd2d`), deployed; the two S3-canonical report files were
  restored from S3 into the clone before the sync (README rule), no deletes.
- `reasoner-study`: two design-input tickets filed from the pilot's rounds, #2 (balance the
  option loadings) and #3 (match human and model item exposure), each stating that no pilot
  data collection follows.
- No model API calls; nothing spent. Nothing deposited anywhere. The scratch `venv/` (pymupdf)
  and `papers/.render-venv/` (the recipe) are as before.

## The tracker

Empty. #1 to #141 are closed. #120 to #141 were filed and closed 2026-09-11 from the six
reviews of the pilot paper (cold, Astra, Gemini, Grok, Kimi, Astra again) and #132 from the
pre-publication list.

## Next session

Nothing is queued for an agent. **Declan's plan, 2026-09-11: the two papers publish together**, the
Reasoner pilot (paper and appendix) and the MFQ-2 document, and a pre-publication pass checks
everything below before either does. Nothing on this list is done until it is struck here.

**Pre-publication pass, both papers:**

- ~~Pilot: the title~~ Done 2026-09-11 (`d307c1b`): "Eleven Language Models in a Narrow Band of a
  Moral-Judgment Instrument". The opening sentence was narrowed under #127.
- ~~Pilot: one more external round~~ Done: five rounds. Astra read `5961507` (twelve findings,
  #120 to #131); Gemini and Grok read the corrected text and returned nothing new; Kimi read it
  without the repository and found the allocation-format sensitivity of the compression ratio
  (#133, #134); Astra's second round read `a3e1c9e` and caught three same-day errors plus the
  undisclosed tie rule (#135 to #141). Records in `reviews/`. Any further paste is diffed against
  the five records first.
- ~~Pilot: the five-model artifacts~~ Done (`d307c1b`): moved to `results/archive-five-model-2026-07/`
  with a README.
- ~~Pilot: the root `viewer.html` read against the final text once more, and the two PDFs
  re-rendered~~ Done (`44619a7`): three viewer lines on item exposure; both PDFs re-rendered from
  the final text and byte-identical to the committed ones.
- ~~MFQ-2: the two hand-written tables~~ Done (#132): emitted as P1 and P2 of `appendix_tables.md`
  and spliced; the document did not change.
- ~~MFQ-2: the PDF re-rendered from the final text; page 13~~ Done: re-rendered 2026-09-11,
  byte-identical to `edcf91c`. Page 13 traced and accepted: the six-column arm table under B1 is
  eight rows that WeasyPrint will not split, so it starts a new page and leaves the page above it
  mostly empty; relaxing the recipe's header rule changed nothing and the table is above the
  keep-whole threshold, so the recipe's rules are not the cause. Re-rendering is a one-command
  step once the text is final (`papers/render.sh <file>`), so the two render items are struck as
  done for the current text, not for a text that changes later.
- ~~Both: a claim-check of every prose number against its artifact, by machine~~ Done:
  `analysis/claim_check.py`, run by the harness; both papers check clean. It matches by value,
  not meaning: a number attached to the wrong quantity still passes.
- ~~Both: the moral-os.com pages~~ Done and deployed 2026-09-11 (moral-os-website, one commit):
  the pilot page retitled with the current Summary as abstract, both pilot PDFs and the pilot
  viewer replaced; a new MFQ-2 page and its PDF, **unlisted** (noindex, no sitemap, unlinked)
  like the MFQ-2 viewer, which was refreshed from `validity/` with its data; the index card's
  finding sentence rewritten. Listing the MFQ-2 page and viewer is Declan's, with the DOI. Any
  later text change reopens this: copy the renders and viewers, redeploy.
- Both: `LOCATIONS.md`'s three `TBD`s and `CITATION.cff`'s commented `doi:`, resolved together when
  Declan mints the DOI. What the deposit is was decided 2026-09-11: the repository snapshot, one
  DOI, both documents citing it (decision 23). Then: list the MFQ-2 page and viewer on the site
  (remove the two noindex blocks, add to `sitemap.xml`, link from `index.html`), redeploy.
- Both: the embarrassment nudge, once more, on the final state. Given at every push today; the
  answer as of this handoff is six rounds on the pilot paper and fifteen on the MFQ-2 document.

Open at close, 2026-09-11, in detail:

1. **External review of the pilot paper, continued.** One external round adjudicated (Astra).
   Any further paste is diffed against the two records and #119 to #131 before it is read. The new work Astra asked for went to the successor study's tracker as design inputs
   (reasoner-study #2, loading balance; #3, exposure matching): no further data collection for
   the pilot unless it makes a material difference (Declan, 2026-09-11). The eleven-model
   nonsense texts stay uncoded.
2. **The five-model artifacts in `results/`.** `pilot_reanalysis_findings.md`,
   `pilot_reanalysis_metrics.json`, `tightened_metrics.json`, `pilot_frame_shifts.json`,
   `coding_results.json`, `nonsense_texts.json`, `coder_check_result.json`, `coder_prompt.md`,
   `nonsense_coding_codebook.md` and `anchoring_metrics.json` describe an earlier collection on
   a prior roster (gemini-flash, gpt4o, grok, llama70b, sonnet) whose run files are not in the
   repository. None is in `analysis/reproduce_manifest.json`; the glossary defines everything
   under `results/` as the published record and warns against the "five models" figures. The
   paper now cites that coding with its scope. Whether the files stay, move or go is Declan's;
   removing any is a change to the published record.
3. **moral-os.com.** `papers/reasoner-pilot.html` on the site is a 2026-07-21 render of the old
   text and the card follows the paper. The site repository is cloned here
   (`~/Code/moral-os-website`) and is not set up with research-kit; its own session.
4. **Zenodo, held** since 2026-09-10 until the pilot writeup is finished. The pinned artifacts
   for the MFQ-2 document's two hand-written tables (d and Ordering) are still not done.
   `LOCATIONS.md` carries three `TBD`s and `CITATION.cff` a commented `doi:`. What the deposit
   is, snapshot or document, is undecided.

Candidates for tickets, not filed: a claim-check for the pilot paper's prose numbers against
`appendix_stats.json` (the harness pins the JSON, not the sentences that quote it); the MFQ-2
claim-check for the d and Ordering tables; the `[*]` versus `[d18]` marker asymmetry; the
same-instrument three-arm collection from Astra's fifth round (spending); the
caveat-consolidation sweep.

Left as disclosure, Declan's decision: the English-framed arm on the official questionnaire
(#53). Not run: the six translated country-free templates (decision 21).

## Open items

- Sampling temperature is unset and unrecorded in the pilot runs and the grid; both documents
  now say so. Any collection not matched to them sets and records it.
- The eleven-model nonsense texts are uncoded and the paper now says only that. Coding them is
  spending if a model codes them, and the five-model coding artifacts are the results-directory
  decision above.
- `analysis/README.md`'s sign check validates the bank's polarity against the expected human
  profile; A9 now says so. A mapping audit against the option meanings would replace it.
- API keys on this Air are exported in the interactive shell; `~/.config/ccas/keys.env` does not
  exist here.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.

## Unresolved - needs a decision

Items 2 and 4 above. Everything else settled.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**Rules learned by breaking them, all in `docs/DEVELOPMENT_NOTES.md`:** check a generator's exit
code before copying its output; the builder's `mean` takes a list, not a generator; sort the keys
of any dict a bootstrap draws from; never redirect a generator into its tracked output; assert
every anchor before writing any file; re-render the PDF after every change to the document.
Added this session, not yet in the notes: sweep a render for colon lead-ins and tables at a
page foot, not only headings; the first pilot render had both and the heading sweep passed it.

**Added to the record, 2026-09-11, Kimi's round and Astra's second:** the as-scored compression
ratio of 5.4 to 7.7 is sensitive to the allocation format; collapsed onto each response's largest
option with ties shared it is 2.3 to 4.9 (2.1 to 6.2 across three tie rules), still the model
spread smaller on every axis and every item. The Summary leads with the collapsed figure. Not a
decomposition: the collapse changes the measurement on both sides.

**Corrected on the record, 2026-09-11 (Astra's second round):** three errors introduced the same
day: Kimi's geometry cell "29 of 60" (209 of 240); "unchanged to three decimals" (Obligation
Scope 0.0639 to 0.0650); "still 0 of 100,000 on every axis" without code (0, 0, 0 and 1). And
the A3 ratio intervals moved in the second decimal when the human files were sorted.

**Corrected on the record, 2026-09-11:** the pilot-paper claims listed under Current state, in
`9f06413` and `9f0102a`.

**Corrected on the record, 2026-09-10:** five pilot-paper claims in `5961507` (relational pole
for a mean of -0.05; the ratio stated model over human; the seasonal framing "within" the
nonsense interval; the refusal claim's evidence; the successor "on the same instrument").

**Corrected on the record, 2026-09-10 (earlier):** the viewer's Models tab drew Morocco's human
marker on the Arabic-framed arm (#99, `4649a42`); its headline story summarised the translated
arm where the document's table is English framing (#101, `59bb943`).

**Corrected on the record, 2026-09-08 and 2026-09-09:** a Summary sentence said the template's
spread was tighter than under any country when four framed conditions were tighter (`385a4f8`);
the rewrite attached "two thirds of the range" to the Arabic figure (#84); the same rewrite
called Egypt the largest contrast when Saudi Arabia and the Emirates exceed it (#90); a French
run-noise sentence compared a single-model five-run SD with a six-country average (#90); the
viewer's Control tab rendered a date as "[object Object]" (fixed before push).

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design.
- The viewer's per-model token table has no counterpart in the document.
- MFQ-2 PDF page 13 carries one list item and nothing else: WeasyPrint starts the eight-row arm
  table on a fresh page rather than splitting it. Accepted 2026-09-11.
- A search that clears a reviewer's quoted phrase must be shown, not reported: #110 and the
  round-six adjudication both cleared "tails too coarse" and it was on line 27 the whole time.
- A cold review that says "every number reproduced" must have diffed the file against the JSON
  by machine, not by eye: three A5 intervals were off by 0.001 to 0.002 and passed.
- A method sentence taken from the glossary is not verified by the glossary. The reshuffle
  claim entered the paper from a reconstructed CONTEXT.md entry and was wrong.
- Every number in a table comes from the artifact by code, never typed: the A8 shared-rule SD
  column was typed and wrong on 2026-09-11 and caught before commit only by a check. And a
  collapse rule has to be stated: Python's max() picked the first tied option and the headline
  depended on it.
- A subset's size is not the cell's: 60 baseline responses against 240 in the cell, and "31 of
  60" went out three times.
- A commit chain stops on the harness: `4df3982` was pushed with the harness reporting FAIL
  because the chain joined the harness to the commit with a semicolon, and its message claimed a
  pass. `067fa8d` records it. The harness is `&&`-joined to any commit that follows it.
- The pilot appendix's A10 names the build scripts without their `analysis/` directory; A1 now
  gives the full path for one of them.
