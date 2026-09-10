# Astra's sixth review of the in-language document, 2026-09-10

**Reviewer:** Astra, sixth round on the document; pasted into the session by Declan and read in
full. Astra had the clone: it ran the newly shipped means and dispersion builders against the
respondent file and reproduced both committed CSVs, and recomputed the country-weighted framing
shift (1.0328) and the Loyalty-Authority sign pattern.
**Reviewed:** the document at `8d058ad`, the state after #113 and #114.
**Adjudicated:** 2026-09-10. Four tickets, #115 to #118, all closed the same day. Nothing touched
a numbered decision. Declan said "do it" to the adjudication as presented, taking the
recommendation to cut the Summary's lead sentence rather than open with numerals, and leaving
the glossary line in `CONTEXT.md` and decision 3 as they are.

## Diff against prior rounds

Finding 1 is the third raise of the Egypt attribution (Astra 4 item 1, #88; Astra 5 item 2,
#107): both earlier fixes kept "naming Egypt" as the subject and appended the qualifier, which
Astra now says does not undo the attribution. Finding 2 continues Astra 5 item 1 and Astra 3
item 4. Finding 3 continues Astra 5 item 5 (#110): the nineteen clause went, the Ireland
sentence kept the interval distinction. The six smaller items are new; two of them (the builders'
completeness rules and the EXACTLY comment) follow from shipping the builders under #114. The
sentence "tails too coarse" is quoted for the second round running and is not in the document,
the viewer, or any file in the repository.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1 | "naming Egypt raised it a further 1.14" in the Summary and "naming Egypt widened the panel" in B4a attribute the increment to the country | Verified, both. Summary now reads "the Egypt-framed condition scored a further 1.14 higher, a comparison that also changed the questionnaire file"; B4a's emitter now says the Egypt-framed condition had greater between-model dispersion than the country-free one | #115 |
| 2 | The Summary and the section lead with a characterization ("barely moves", "nearly the same place whatever language"); "0.08 ignoring direction" hides cancellation among models | Verified, three sentences. The Summary's lead sentence is cut so "Five of the six translations..." opens the paragraph, in words rather than Astra's numerals (Declan's register); the section lead describes the table; "0.08 as the mean absolute panel-level shift" | #116 |
| 3 | Ireland "the only reference-sample mean ... falling within the panel's resampling range" restores the interval distinction; replace "tails too coarse" | The Ireland sentence verified and rewritten: the near-match and the foundation offsets lead, the two-uncertainties sentence stays without its numbers and points to B3 and B3a. "Tails too coarse" is not in the document; downgraded to a question, nothing to change | #117 |
| a | "a model that answers at length cannot outvote the rest" is the wrong rationale | Verified in Methods and the viewer's Models tab; each run yields one ratings object. Now: equal weight per model, runs not treated as independent models. The same rationale stands in `CONTEXT.md` and decision 3 for the pilot instrument, left as written | #118 |
| b | "not a sample of models" is absolute | Verified in the Summary and Limits. Now a selected panel, not a probability sample | #118 |
| c | The means builder admits a respondent per complete foundation, the dispersion builder per complete respondent | Verified in the code; n per country agrees, 3,902 in both, so every kept respondent is complete. Documented in the reference README and B9 | #118 |
| d | "without ties" on the four-values statement | Verified, two occurrences (the paper and B3's Arabic subsection); both amended | #118 |
| e | "Two countries a point apart come out the same" | Verified; now "Iran and Egypt receive nearly identical composite scores" | #118 |
| f | The R script says it replicates the authors' code "EXACTLY" while B2a reports a 0.0044 residual | Verified in the R script and the means builder's header; both now say following the procedure, and the reference README's provenance line records the comment change against the `reasoner-study` copies | #118 |

One regenerated artifact moved on prose alone and was re-pinned in the #115 commit; the harness
passes.

## Review as received

This revision is materially stronger. I now regard it as close to ready for release as an exploratory report, with a few targeted corrections remaining. The central results are credible within the stated scope. The remaining problems are mainly inconsistencies between the careful methods and stronger wording elsewhere.

I reread the revision and checked the newly added human-reference builders. Both the means and dispersion scripts ran successfully against the locally available respondent data and reproduced their committed CSVs exactly, covering 3,902 respondents across nineteen countries. I also independently reproduced the country-weighted framing shift, 1.0328, and the nineteen-country Loyalty–Authority sign pattern: only Belgium, France, New Zealand, and Switzerland are below their reference means. I did not rerun the R alignment analysis or independently authenticate the source files.

What the revisions resolve

* Human-reference reproducibility: the actual scoring and dispersion builders are now available locally, and their outputs reproduce. This substantially addresses my previous concern.
* Dependence on Purity: the new benchmark sensitivity analysis is useful. Ireland changes sign, but the broad pattern survives. You also correctly calculate human SDs for the two-foundation composite.
* Weighting: reporting 1.03 under equal country weighting alongside 1.06 under equal language weighting shows that the average framing result is not sensitive to that particular choice.
* Interpretation: the added qualifications about opposing model-level movements, estimated human rankings, mixed-language instructions, and collection dates all improve accuracy.
* September control: B4a now correctly says the collection measures the instruction without the country, rather than claiming complete separation.

These are substantive improvements, not merely additional caveats.

Three corrections I would make before release

1. Fix the Egypt attribution in the summary.
The summary still says:
"naming Egypt raised it a further 1.14"
That attributes the increment to the country cue, although the contrast also changes the questionnaire file. Appending that fact does not undo the causal attribution.
Use the more accurate wording already present in the main results:
"The Egypt-framed condition scored a further 1.14 points higher, although this contrast also changed the questionnaire file."
Likewise, B4a's "naming Egypt widened the panel" should become:
"The Egypt-framed condition had greater between-model dispersion than the country-free condition."
You can report these results without another experiment. A same-instrument experiment is necessary only if you want to isolate the country contribution.

2. Make the language claim precise in its first sentence.
The new qualification about cancellation helps considerably. Nevertheless:
"Translating the questionnaire barely moves the panel's composite."
still leads with a broad characterization that immediately needs an Arabic exception. Later, "nearly the same place whatever language you hand it" repeats the problem.
A stronger opening is simply:
"Five of six translations changed the unframed panel-average binding score by less than 0.10 points; Arabic increased it by 0.34."
That is concise, accurate, and lets readers judge magnitude. Keep the following sentence about opposing changes across models and foundations.
Also change "0.08 ignoring direction" to "0.08 as the mean absolute panel-level shift." Taking absolute values after averaging models still permits cancellation among models; "ignoring direction" alone obscures that distinction.

3. Remove the interval-based distinction around Ireland.
You deleted "the other nineteen fall outside it," but:
"Ireland's is the only reference-sample mean … falling within the panel's resampling range"
makes essentially the same distinction.
The cancellation example is scientifically more informative than whether a human mean falls within a model-reweighting interval. I would start that paragraph:
"Ireland's composite nearly matches its reference-sample mean, but the agreement conceals differences across foundations."
Then give the Loyalty, Authority, and Purity values. Keep the resampling intervals in the appendix.
Also replace "tails too coarse" in the methods. The central limitation is the small, selected, potentially dependent model panel—not numerical coarseness of the bootstrap tails.

A few smaller accuracy issues

* "A model that answers at length cannot outvote the rest" is the wrong explanation for model-level averaging. Response length never contributes additional ratings here. Say that every model receives equal weight and repeated runs are not treated as independent models.
* "Eleven models is not a sample of models" is unnecessarily absolute. It is a selected sample, just not a probability sample from a defined population. Use that distinction consistently.
* The missing-data rules differ between the new human builders. The means builder accepts a respondent separately for each complete foundation; the dispersion builder requires all six foundations to be complete. Both currently retain all 3,902 complete respondents, so this does not change these results. Document that completeness explicitly so the apparent difference is resolved.
* Add "without ties" to the four-possible-values statement about three-country Spearman correlations.
* Change "Two countries a point apart come out the same" to "Iran and Egypt receive nearly identical composite scores." This avoids implying equality of full response profiles or treating the reference samples as the countries themselves.
* The alignment script's comment says it replicates the authors' code "EXACTLY," while the paper reports unexplained numerical discrepancies. Distinguish following their procedure from reproducing their numerical results.

I would not keep expanding the study to answer every possible methodological objection. The controls and sensitivity analyses now support a useful, bounded contribution. My recommendation is a final precision edit, followed by release as an explicitly exploratory report. Its strongest finding remains that these instructions substantially change this panel's composite responses and reduce dispersion, with a country-free instruction already producing both effects.


## Correction, 2026-09-10 (#119)

The adjudication above says "tails too coarse" is not in the document. It is, at line 27 of
the Methods: "with tails too coarse to read as a calibrated bound". The search that cleared it
failed and the finding was dismissed on that basis. Declan found the sentence on his own read
before the re-render; the finding is reinstated and the sentence replaced under #119.
