# Astra's second review of the Reasoner pilot paper and appendix, 2026-09-11

**Reviewer:** Astra (the current ChatGPT model), second round on this paper. It had the clone: it
reran `analysis/build_appendix.py` and matched the committed JSON, and ran its own tie-handling
and rerun-selection diagnostics.
**Reviewed:** the documents at `a3e1c9e`, after its first round, the cold review, Gemini, Grok
and Kimi were applied.
**Adjudicated:** 2026-09-11. Seven tickets, #135 to #141. Every number it reported reproduced:
the tie counts (43/40 of 352; 70/95 of 655; Llama 22 of 60), the three tie rules, the per-item
collapsed range, the 209 of 240, the 0.0639 to 0.0650, the rerun script's formula and the
one-rerun medians. Declan's decision, 2026-09-11: shared-among-ties is the primary rule and the
Summary leads with it, giving the range across rules and the as-scored ratio beside it.

## Diff against prior rounds

Its resolved table matches the record for #120 to #131 and it reopens none of them. Everything
new concerns text added after its first round: the allocation-style analysis from Kimi's round
(#133), the exclusion sensitivity (#134), and my own additions to A3.

## Adjudication

| # | finding | disposition | ticket |
|---|---|---|---|
| 1 | "Removes that component" and "the rest of the ratio is flatter allocations" claim a decomposition the collapse cannot identify | Verified. Rewritten as a sensitivity to allocation format in Summary, Results, Limits, A8, with the reviewer's reasons (nonlinear, discards secondary preferences, magnifies near-ties, changes both sides) | #135 |
| 2 | The collapse used Python's first-tied maximum, undisclosed; ties are common; the headline depends on the rule | Verified and recomputed. Shared-among-ties is the primary rule (Declan); the three rules tabled; per-item collapsed ratios tabled (1.19 to 6.11 shared) | #136 |
| 3 | Kimi's geometry cell is scored on 209 of 240, not 29 of 60 | Verified; my error, the twelve-scenario subset's size used as the cell's. Three places corrected | #137 |
| 4 | "Unchanged to three decimals" is false; the stored allocation is not always uniform | Verified against the JSON. The four changes stated; "stored allocation" with its two forms | #138 |
| 5 | The rerun script inflates variance by the median run SD squared; the 6 to 9 percent is an approximation; the recount sentence had no code | Verified in the script. Relabelled; one-rerun selection emitted (20,000 draws, seed 20260911: medians 6.17, 6.97, 5.02, 4.99); the recount emitted, and it is 0, 0, 0 and 1 of 100,000, not 0 on every axis as I had written | #139 |
| 6 | Figure template says "classic WEIRD" and "bootstrap"; figure seed unlisted; unsorted human order is not portable | Verified. Template rewritten, figure regenerated and re-pinned; seeds listed by script; human files sorted and the A3 intervals re-pinned, moving in the second decimal (recorded) | #140 |
| 7 | Eight wording items | Verified each against the text and the code; all applied, including the seasonal prompt's "daily routines and communal life" and "no seed was sent" | #141 |

Its "safer central statement" was not adopted as written; its substance is in the Summary.

## Shape of the round

Mechanical again, and again everything it computed was right. Three of its seven findings were
errors introduced in this repository the same day, two of them mine; the round caught them
within hours. Its request for a prespecified treatment of ties was the one design change.
