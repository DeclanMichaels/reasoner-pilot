# Kimi's review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Kimi, first round on this write-up.
**Reviewed:** the documents after Gemini's round was worked, at or after `952611f`: it cites B1a's
E2 bracket, the corrected Kimi-K2.6 sentence and the 70-contrast B4.
**Adjudicated:** 2026-09-08. Six tickets, #34 to #39, all closed the same day. Kimi spot-checked
about twenty numbers across both documents and every one reconciles.

## Diff against prior rounds

Item 4, a "stereotype convergence" interpretation assembling the overshoot, the endpoint use and the
dispersion finding, is the fourth request to interpret the fifteen-above shape; decision 13 records
the first three and it is declined again, as mechanism and as a label the data does not earn.
Item 6's request to surface the sign-flip enumeration re-raises what decision 15 withdrew; reported,
not re-argued. Item 1, retitling to "adding a country-framing instruction", is new and is Declan's.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| minor | The language table's Farsi row reads `\| Farsi \| +1.22 \| Iran only \|` | **Verified, this workflow's error, and twice wrongly called refuted** when Astra and DeepSeek raised it: the d table was checked instead of the language table. Fixed; the earlier record corrected | #34 |
| minor | "and and" | Verified | #35 |
| 2 | Language under framing changes questionnaire and instruction together | Verified by design; stated in the paper and B4's lead | #36 |
| 5 | "Framing > language" holds on average, not uniformly | Verified: Arabic unframed +0.335 exceeds French framing +0.126; Belgium's English framing is -0.146. Stated | #36 |
| 3 | Arabic unframed anomaly never probed | Verified: Purity +0.58 over English, Loyalty +0.23, Authority +0.20, Care +0.02. A language-by-foundation table of unframed contrasts is added to B6a and one sentence to the paper. Whether it is a translation artifact is mechanism; not taken | #37 |
| 6 | Sign counts function as a sign test; multiplicity unstated | Verified as a reading the text invites. B4's lead now says the counts and ranges carry no test and that no family-wise claim is made across the 70 contrasts. Enumeration stays out: decision 15 | #38 |
| minor | Unframed baseline gap unremarked; Morocco arms; Spanish caveat | Verified: unframed English sits at 2.769, below every reference mean but Japan's; one sentence. B3's caption names Morocco's arms. The Spanish caveat already sits with its only mention | #39 |
| 1 | Retitle to "adding a country-role instruction shifts responses more than translating the questionnaire" | Fair reading of the design, now stated in the methods and B1a. Taken: Declan, 2026-09-08 | none |
| 4 | Stereotype convergence | Declined: decision 13, fourth request; scope rule | none |
| refs | Hazrati article number unconfirmed | Confirmed: the DOI resolves to `collabra/article/11/1/140952` | none |

## Review as received

I've read both documents closely, checked the internal arithmetic against the appendix tables, and verified the citations. Here is an honest review.

---

## Overall verdict

This is an unusually candid piece of exploratory work — closer to a well-kept lab notebook than a typical results paper — and most of the methodological moves are defensible. The descriptive-statistics posture (no p-values, descriptive bootstrap intervals, explicit decision log) is internally consistent and mostly well-executed. However, the headline claim overstates what the design can support, there is one unaddressed confound inside the central "language under framing" contrast, the most interesting anomaly (Arabic unframed) is never probed, and there are several concrete errors, including one wrong table cell. I would not circulate it as-is.

## What is genuinely strong

1. **The unit-of-analysis choice is right.** Averaging five runs per model before any contrast, treating the model as the resampling unit, and reporting leave-one-out ranges shows real statistical maturity. The careful distinction between the human SE and the model-resampling interval (the Ireland passage) is the kind of thing most papers get wrong.
2. **Transparency is exemplary.** The dated design history, the decision log, the mid-study comparator change kept as errata rather than silently swapped, the Kimi-K2.6→K3 roster change disclosed, the unlogged-temperature admission, and the selection-on-compliance caveat for retried calls — this is how exploratory work should be documented.
3. **Robustness is handled well.** The Iran anchor sensitivity across all three published means (and choosing the most conservative one), the Morocco two-arm check, the ceiling-restriction analysis in B6a, and the ordering audit in B8 all anticipate the obvious objections. I spot-checked roughly twenty numbers across the two documents (condition counts: 22+23+5=50, 1,210+1,265+275=2,750 cells; the 1.04 framing average from the per-language means; Egypt +1.836 = 4.605−2.769; the 1.62-point human span; the 99,000-rating total; B7's 46/2,796) and everything reconciles.
4. **The measurement-invariance caveat is exactly right.** Recomputing the alignment diagnostics and then explicitly stating they say nothing about model-vs-person comparability is honest and correct.
5. **References check out.** Zewail et al. (2026) in PNAS is confirmed . Hazrati, Nejat & Daneshi (2025) exists — it appears as a July 2025 preprint (DOI 10.31234/osf.io/43t5s) and is cited by a third party as appearing in *Collabra: Psychology* , though I could not confirm the exact article number 140952; the authors should verify that detail against the published version rather than the preprint.

## Major issues

1. **The headline compares two manipulations that are not commensurable, and the paper knows it.** "Country framing" is *adding a system instruction where there was none*; "questionnaire language" is *swapping the instrument's language*. The +1.04 vs +0.05 comparison is therefore "instruction vs. no instruction" as much as "framing vs. language." The appendix states this precisely (B1a: the contrast is "the country label and the role-taking instruction together"), and the self-report audit (+0.026, interval spanning zero) brackets the instruction-alone component — but then the title, summary, and "Framing moves the panel; language mostly does not" section all phrase the result as if framing and language were two levels of one factor. They are not. Worse, the cleanest fix (a country-neutral arm using the framing template itself) was not run, so even the bracket is loose. Either run that arm or retitle: the honest claim is "adding a country-role instruction shifts responses more than translating the questionnaire."

2. **The "language under framing" contrast confounds questionnaire language with instruction language.** In the local-framed conditions, both the questionnaire *and* the system prompt are in the local language; the English-framed conditions have both in English. The contrast labeled "language under framing" (e.g., French +0.175 for Belgium) therefore cannot be attributed to the questionnaire translation — it may be entirely an instruction-language effect, or an interaction. The main text's gloss ("a language effect depends on whether a country is named") blurs this. Since the unframed contrasts isolate questionnaire language cleanly, and the framed ones do not, the paper's two "language" claims rest on different identifications, and the reader is never told this in one place.

3. **The Arabic unframed anomaly — the largest language effect, 11/11 models moving together — is never investigated.** +0.335 with unanimous direction is the single most interesting unframed result, and it goes undiscussed beyond being reported. The appendix data point at a mechanism: ar_neutral's Purity is 2.55 vs. English 1.97, a 0.58 gap that accounts for most of the composite shift, and Arabic Care is also the highest unframed Care (4.73). A per-item or at least per-foundation breakdown of the unframed language contrasts belongs in the main text, with some discussion of whether this is a translation/anchor-behavior artifact or a genuine "Arabic elicits higher binding responses" effect. As it stands, a skeptical reader can dismiss the whole unframed-language table because the one large effect is unexplored.

4. **The dispersion finding needs an interpretive guardrail, not just a ceiling check.** B6a does the hard work of ruling out the obvious mechanical explanation (restriction by distance from the ceiling), and that's good. But tighter agreement under framing is never given a substantive interpretation, and the natural one — convergence on a shared stereotype — is supported by everything else in the paper: endpoint use rises (0.23→0.27), 15 of 20 framed means overshoot their human anchors, and the five undershoots are all Western European/NZ while Japan (lowest human mean) gets the second-largest overshoot. The paper reports every piece of this pattern but never assembles it. Tighter spread plus systematic overshoot is evidence of *stereotype convergence*, which is a finding about what the panel is doing, not just how dispersed it is. One or two paragraphs engaging with this would substantially raise the paper's value; without them, the dispersion section reads as precision without a subject.

5. **"Framing > language" is an average, and the paper should say so.** Arabic's language effect (+0.335) exceeds French's framing effect (+0.126) and dwarfs the French/Belgium English-framing effect (−0.146). The ordering claim holds on average but not uniformly, and the summary's flat statement invites the stronger reading.

6. **The sign-count device is a de facto sign test, and multiplicity is unaddressed.** Dropping p-values is a defensible stance, but "11 up, 0 down" recurs dozens of times, and the paper itself notes the exact sign-flip enumeration exists in the audit output. If enumeration was computed, report it (even as a parenthetical per family of contrasts), or at minimum state the stance on the ~120-contrast family explicitly. As written, the no-p-value policy mostly transfers the inference burden onto a device that functions like a p-value without saying so.

## Minor issues and concrete errors

- **Wrong cell in the main text.** In the "Which language each country was administered in" table, the Farsi row reads `| Farsi | +1.22 | Iran only |` — a stray "+1.22" (copied from the later d-score table, where it is Japanese's mean) has leaked into a two-column table. This must be fixed; as printed it corrupts the one table every reader checks first.
- **Morocco arm inconsistency between B3's two tables.** Table 1 shows Morocco's local-framed value as 4.582 (Arabic arm), but the distance table's +0.575 is computed from the Spanish arm (4.589). The footnote says Morocco is compared on the Spanish arm, so Table 1 shows one arm while the analysis uses the other — and the caption doesn't reconcile them. Pick one convention and label it consistently.
- **Typo:** "and and we read that composition" (Limits, Iran paragraph).
- **Unframed baseline gap goes unremarked.** The unframed panel (2.77) sits far below nearly every human mean — models answering "as themselves" respond like extremely low-binding respondents. That gap is arguably as interesting as the framing shift, and it gets one sentence about Arabic only.
- **"Human spread" percentages**: 47% / 234% / 107% — fine arithmetically, but the Spanish 234% rests on panel exaggeration that spans less than a point (0.689); with five countries the rank correlation (ρ=0.80) carries essentially no precision, which the paper does say — keep that caveat attached to every mention of the Spanish ordering, not just in the Ordering section.

## Recommendations before this goes out

1. Retitle or reframe the central claim to "adding a country-framing instruction," and state the instruction-vs-questionnaire-language confound in the main text wherever "language under framing" is reported.
2. Add a per-foundation (ideally per-item) breakdown of the unframed language contrasts and engage with the Arabic anomaly.
3. Fix the Farsi table cell, reconcile the Morocco arms, and proofread.
4. Add a short interpretive passage on stereotype convergence tying together overshoot, endpoint use, and the dispersion finding.
5. State the multiplicity stance explicitly, and either surface the sign-flip enumeration or stop leaning on sign counts.
6. Verify the Hazrati article number against the published *Collabra* record.

None of these requires new data except the country-neutral framing arm (worth running before anyone cites the framing-vs-language comparison as evidence about *language*). As a descriptive, meticulously documented account of what eleven models did under fifty conditions, the work is solid; as evidence for the claim its title makes, it currently overreaches in ways the appendix itself documents but the main text elides.
