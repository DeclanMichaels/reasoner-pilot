# Grok's review of the Reasoner pilot paper and appendix, 2026-09-11

**Reviewer:** Grok, one of the model families Declan runs adversarial review through; first round
on this paper.
**Reviewed:** the documents after `e221888` (it cites the request parameters, the per-cell
exclusions, the item-level and ten-respondent checks, and the no-temperature, top-p or reasoning
sentence, which dates from that commit).
**Adjudicated:** 2026-09-11. No ticket; one table change as a documentation correction below the
level of a published claim.

## Diff against prior rounds

Its six weaknesses are the paper's Limits and appendix restated: the convenience sample and
single-item exposure (#120), no scaffold-only control (#128), rerun averaging (decision 8, A3),
the weak clustering evidence and the 0.4 expected same-lab links (#125), the seven-model token
counts (#123), the single-instrument scope (Limits, "One instrument"). Astra raised each of them
(`reviews/astra-paper-review-pilot-2026-09-10.md`); Gemini restated four
(`reviews/gemini-paper-review-pilot-2026-09-11.md`). One sentence overstates the text: Grok says the
known-groups profile "was used to set" the sign convention; the text and `analysis/README.md` say the
convention was checked against it. No change.

## The one change

Weakness 3: the Results table carries the averaged ratios and the exposure-matched figures sit in the
paragraph after it, "disclosed but easy to miss". The table now carries two more columns from A3, the
item-by-item range and the ten-respondent ratio per axis, and the paragraph says which columns match
the exposure. Nothing new is computed.

## Shape of the round

Confirmatory. It read the repository ("regenerable from the described pipeline") and characterised
each result as the text does. Its praise of the limitations section and of the paper relative to
"most contemporaneous LLM values papers" is positioning, not a finding. Third round to return
nothing new after Astra's; the text is exhausted for this generation of reviewers.
