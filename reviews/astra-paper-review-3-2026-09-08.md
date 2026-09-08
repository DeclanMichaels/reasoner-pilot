# Astra's third review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Astra, third round on this write-up.
**Reviewed:** the documents at `6f39952`, after Claude's cold round. Astra recovered all 50
condition means, all 300 foundation means, the 2,750 scored runs, the framing average, both
language averages and the 37-of-39 dispersion count.
**Adjudicated:** 2026-09-08. Eleven findings and a presentation section; twenty tickets, #52 to
#71, nineteen closed the same day. Two decisions taken by Declan on the round: 18 (Morocco under
Spanish) and 19 (the ratings dataset). The title was changed on the round to a description of
what was done.

## Diff against prior rounds

Item 8's Ireland prominence re-raises Astra's first and second rounds (#10, #19, and round 2
item 3) and stands as adjudicated; its two new parts were taken. Item 10's ceiling point re-raises
#12 and #20 and stands. Item 11c revisits round 2's item 5, which re-attributed the Iran
inference to us; this round asked for evidence or removal and Declan cut it. Items 1 to 7, 9 and
the presentation notes are new. Every external fact was verified against a primary source: the
Atari accepted manuscript's Table 6 for item 1, the PMC full text of Zewail et al. for items 5
and 7, the Federal Statistical Office's 2025 publication for item 11d.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1 | B2a omits Table 6's Purity intercept noninvariance, 39.5% against a 25% criterion, and the authors' caution | Verified in the accepted manuscript. B2a prints the published R-squared and percentages beside the recomputation, the criterion, the caution and the largest recomputation gap (0.0044); the paper names Purity; a Loyalty-Authority composite sensitivity is given | #52 |
| 2 | English framing contrasts change the questionnaire file as well as the system prompt | Verified: all 1,267 English-framed runs on `mfq2`, our transcription; the comparator on `mfq2_en`. B1 gains a design table per arm; B1a names the instrument per arm; B4 gains the unframed instrument contrast, -0.009 [-0.103, +0.082], 6 up 5 down; the paper's methods and Limits carry it | #53, #67 |
| 3 | Reproducibility overstated: the test hashes, the runs are gitignored | Verified. The preface and B9 say so. Decision 19: the integer ratings are published as `mfq2_ratings.csv` with a check the harness runs; the emitters' move to the dataset is #71 | #54, #69, #71 |
| 4 | Small composite changes described too broadly; cancellation within the composite and across models | Verified: French Care -0.28, Purity +0.26, composite +0.01; within-model absolute changes Arabic .335 to French .085 recomputed exactly. Heading and lead name the binding composite; the Summary says what 0.08 averages; B6a's table gains the within-model column. The title was changed to a description, Declan's | #55, #57, #62 |
| 5 | "Six translations exist" is false; the supplement holds Chinese too | Verified: seven translations extracted, Chinese never administered. Stated with the selection rule | #56 |
| 6 | The self-report control uses the old transcription and does not bound role-taking | Verified: E2 is `ours_selfreport` vs `ours_nosystem`. B1a gives both pairs, -0.026 [-0.090, +0.042] and -0.074 [-0.143, -0.002]; "brackets" replaced | #58 |
| 7 | Zewail: six models not five; Figueroa, A.; "only ours produces item responses" misleading | Verified against PMC: item-at-a-time single-number ratings about the average or random person, ten repetitions, YourMorals benchmark poststratified. Reworded as perspective and administration | #56, #59 |
| 8 | Ireland prominence; "models like these"; no model-level summaries for the aggregates | Prominence: re-raise, stands. Wording: now "the observed eleven are reweighted by resampling" everywhere. Aggregates: sign counts, intervals, leave-one-model-out and leave-one-provider-out added in B4 | #60 |
| 9 | Ordering reports ranges as "spread"; 234% overgeneralised; rho 0.17 coupled; Morocco absent from Spanish | Verified. Columns read range, ratios literal, the correlation sentence cut. Morocco: decision 18 moves it to Spanish in every view, Spanish ordering six countries rho +0.89, Arabic three rho -0.50 | #61, #68 |
| 10 | Run-noise sentence is rough; mechanism unresolved; ceiling | Decomposition run: noise-corrected between-model SD 0.312 unframed, 0.158 framed, 37 of 39 holds; emitted in B6a. Ceiling: re-raise, stands. No mechanism claim is made | #62 |
| 11 | Absolute statements: Care never; Morocco unmoved; Iran bias direction; first-language percentages; B8 no bias | All verified. Care stays high; the two arms' 0.007 against the unframed arms' 0.324; the Iran direction cut (Declan); Belgium's figure cut, Switzerland's sourced to the FSO 2025 publication, 2023 data; B8 qualified | #63, #64, #70 |
| pres. | Decision references unlinked; no dates in the paper; per-country unframed implied; "have none"; anchors rounded before differencing | All verified and fixed; full-precision anchors moved fourteen displayed distances by 0.001, listed in `3ebb7f0` | #65, #66 |

Astra's suggested title was not taken; Declan's description of what was done was.
