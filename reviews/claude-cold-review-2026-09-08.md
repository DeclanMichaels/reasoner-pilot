# Claude's cold review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Claude (Fable 5.1), the workflow that wrote most of both documents. Not an independent
adversarial review; the six external rounds are, and a seventh is being sent.
**Reviewed:** the documents at `2457833`, after Kimi's round and the retitle.
**Adjudicated:** 2026-09-08. Twelve tickets, #40 to #51, all closed the same day in `aa7b7f7`.

## What was checked

Every number in the paper was recomputed from the appendix, the committed reference CSVs or the raw
runs: the six language contrasts and their 0.05 and 0.08 means; the 1.04 framing average and its
1.011 and 1.061 reweightings; the 64, 3 and 5 percent scale figures; the twenty distances and their
fifteen-five split; Ireland's interval; the three Spearman correlations in Ordering and the 0.00 in
the Arabic-four subsection; the six per-foundation framing shifts; the French foundation moves; the
d table; the dispersion medians, endpoint shares and item-level spreads; the five-run medians; the
seeds against B1a; the condition, cell, call and rating counts. Every one reproduced. The findings
are prose and structure.

## Diff against prior rounds

The "populations" wording (#44) is the residue of Astra's #10 and #19: the sweep missed the
hand-written Arabic-four subsection and one sentence of the Summary. The unpinned paper figures
(#49) are the handoff's claim-check candidate made concrete. The novelty sentence (#50) is the
kind of language DeepSeek's round objected to. Nothing here touches a numbered decision.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1 | Paper's d-table lead says "the same distances"; the table is in-language framed, the one above it English framed | Verified: Iran +1.22 = 0.981/0.802; English-framed would be +1.55. Reworded | #40 |
| 2 | Appendix preface says B9 names the human-side builders; B9 names none | Verified. B9 gains the paragraph; the R script's home is the companion repository, not public | #41 |
| 3 | No blank line between B3's distance table and the Atari paragraph; GFM parses it as a row | Verified against the table extension. Generator emits the line; artifact re-pinned, no number moved | #42 |
| 4 | B1 and B3a name the five English unframed conditions in two unmapped sets | Verified. B1 adopts the B3a keys and says what each is | #43 |
| 5 | "Populations" at appendix 153 and 162 and paper line 7 | Verified. Reference sample(s) | #44 |
| 6 | Rank correlation "0.16" | Recomputed 0.168; truncated, not rounded. Now 0.17 | #45 |
| 7 | Summary's Ireland sentence and the Ordering table leave their framing unnamed | Verified: English framing and in-language framing respectively. Named | #46 |
| 8 | "Tell one of these eleven models ... rises by 1.84" | 1.84 is the panel mean of within-model differences. Now addresses the panel | #47 |
| 9 | B6a states the temperature was fixed per model where B1a says it was never captured | Reworded as the assumption it is | #48 |
| 10 | Paper's 0.129 and 0.188 and the d table have no artifact | Both medians recomputed from the raw runs and now emitted in B6a. The d table remains unpinned | #49 |
| 11 | "What this study adds ..." | Novelty claim, register rule 3. Cut | #50 |
| 12 | "equalising" against "randomized" | American spelling; the only British form in either document | #51 |

Two stale lines in `docs/DEVELOPMENT_NOTES.md` were corrected in the same commit as documentation
below the level of a published claim: the 1,100-cell appendix description and the failed-call
count, now 46 of 2,796.
