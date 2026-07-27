# Statistical Appendix

Companion to "The Language Carries the Population; the Prompt Carries the Caricature." Every number here regenerates from the raw runs with one stdlib script, `validity/audit_inlanguage.py` (random seed 20260723; bootstrap 100,000 iterations; sign-flip tests enumerate all 2,048 sign patterns exactly). This appendix is deliberately terse and table-first; the readable account is in the main report.

## B1. Sample and data

Eleven models, the pilot panel. Six in-language cells per model (Arabic, Japanese, Farsi, each framed and neutral), five iterations each: 330 cells, 329 with parseable ratings. The single exception is a deterministic refusal (B7), scored as missing; that model-condition rests on four iterations. English baselines come from the country-framing run of 2026-07-20 (English MFQ-2 administered under "answer as a typical person living in {country}" for six countries, same panel, five iterations; internal results note: `validity/results/society_framing_mfq2.md`, raw cells in `validity/runs_framed/`): its framed cells for Egypt and Japan (55 each), the framed Iran arm added 2026-07-24 (55), and the neutral English run (55), all under the identical protocol and the same runner (`validity/run_framed.py`). Instruments are the official MFQ-2 translations from the validation materials; item-to-foundation keying confirmed against the scoring block in the Farsi file. Framing-instruction translations are ours and are recorded verbatim in every output cell.

## B2. Scoring and the unit of analysis

Foundation score: mean of its six items, scale 1 to 5. Binding composite: mean of Loyalty, Authority, Purity. The independent unit is the model: each model's iterations are averaged first, and every test below operates on eleven per-model values. Panel SDs are population SDs over the eleven per-model means.

## B3. Conditions: panel means and bootstrap CIs

Resampling models with replacement, 100,000 draws, percentile intervals.

| condition | panel mean | 95% CI | between-model SD |
|---|--:|:--:|--:|
| EN framed Egypt | 4.607 | [4.515, 4.693] | 0.15 |
| AR framed | 4.613 | [4.520, 4.702] | 0.15 |
| AR neutral | 3.033 | [2.770, 3.309] | 0.46 |
| EN framed Japan | 3.668 | [3.507, 3.844] | 0.29 |
| JA framed | 3.459 | [3.367, 3.556] | 0.16 |
| JA neutral | 2.662 | [2.495, 2.841] | 0.29 |
| EN framed Iran | 4.587 | [4.482, 4.680] | 0.17 |
| FA framed | 4.358 | [4.226, 4.486] | 0.22 |
| FA neutral | 2.720 | [2.415, 3.009] | 0.50 |
| EN neutral | 2.705 | [2.503, 2.897] | 0.34 |

Human anchors, treated as constants (their standard errors, at N of 989 to several thousand, are an order of magnitude below the effects tested): Egypt 4.27, Japan 2.65, Iran 3.33.

## B4. The test family

Ten comparisons, one declared family, Holm-corrected. Paired tests use per-model differences; anchor tests subtract the constant from each model's mean. Exact sign-flip permutation: with eleven models the minimum attainable two-sided p is 2/2048, reported as 0.001. Nothing was pre-registered; the family is exploratory. T9 and T10 were added with the English-framed Iran arm after the first-draft audit identified its absence.

| test | difference | 95% CI | exact p | Holm |
|---|--:|:--:|--:|--:|
| T1 Egypt: EN framed vs AR framed | -0.006 | [-0.038, +0.025] | .813 | 1.00 |
| T2 Japan: EN framed vs JA framed | +0.209 | [+0.080, +0.361] | .0098 | .039 |
| T3 JA neutral vs Japan anchor | +0.012 | [-0.155, +0.192] | .905 | 1.00 |
| T4 FA framed vs Iran anchor | +1.028 | [+0.894, +1.157] | .001 | .0098 |
| T5 FA neutral vs EN neutral | +0.015 | [-0.148, +0.173] | .872 | 1.00 |
| T6 AR neutral vs EN neutral | +0.328 | [+0.207, +0.457] | .001 | .0098 |
| T7 AR framed vs Egypt anchor | +0.343 | [+0.249, +0.432] | .001 | .0098 |
| T8 Japan: framed vs neutral, in-language | +0.797 | [+0.636, +0.961] | .001 | .0098 |
| T9 EN framed Iran vs Iran anchor | +1.257 | [+1.151, +1.350] | .001 | .0098 |
| T10 Iran: EN framed vs FA framed | +0.229 | [+0.142, +0.321] | .001 | .0098 |

The three null results (T1, T3, T5) are reported as bounds, not as demonstrated absence: any Egypt language effect is smaller than 0.04, any Japanese-neutral displacement from the population mean is within 0.19, any Farsi-neutral departure from the English default is within 0.17.

## B5. Robustness: leave-one-model-out

Japanese neutral panel mean with each model removed spans 2.603 to 2.707 around the anchor of 2.65; no single model creates the agreement. English-framed Iran overshoot with each model removed spans +1.234 to +1.289; Farsi-framed Iran overshoot spans +0.989 to +1.069. Every individual model overshoots both Iran conditions.

## B6. Per-foundation profiles

Panel means by foundation. Iranian anchor row from the independent validation (its larger sample, N = 989, rescaled +1).

| condition | Care | Equality | Proportionality | Loyalty | Authority | Purity |
|---|--:|--:|--:|--:|--:|--:|
| AR framed | 4.88 | 2.78 | 4.45 | 4.73 | 4.77 | 4.35 |
| AR neutral | 4.59 | 2.28 | 4.18 | 3.38 | 3.25 | 2.47 |
| JA framed | 4.28 | 2.31 | 3.98 | 3.57 | 3.85 | 2.96 |
| JA neutral | 4.56 | 2.16 | 3.94 | 2.90 | 3.09 | 2.00 |
| FA framed | 4.78 | 2.65 | 4.29 | 4.45 | 4.48 | 4.14 |
| FA neutral | 4.59 | 2.07 | 4.12 | 3.03 | 2.99 | 2.14 |
| Japan, measured | 3.03 | 2.27 | 3.14 | 2.66 | 2.67 | 2.63 |
| Iran, measured | 3.95 | 2.67 | 4.15 | 3.63 | 3.05 | 3.32 |

Japan measured row: Atari et al. (2023) Table 7. The framed-Iran error concentrates in the binding foundations (Authority +1.43, Loyalty +0.82, Purity +0.82 against the measured sample) while Equality is accurate to 0.02: the template misses exactly where the population departs from it.

Two properties of the JA-neutral match, quantified by the foundation-level extension (`validity/audit_foundations_ext.py`, same seed and conventions). Per-foundation deltas vs the Japan anchors: Care +1.53 [+1.31, +1.74], Proportionality +0.80 [+0.61, +1.03], Authority +0.42 [+0.27, +0.59], Purity -0.63 [-0.79, -0.47], all at the exact-test floor; Equality -0.11 [-0.34, +0.08] and Loyalty +0.24 [-0.03, +0.52] indistinguishable from zero. Within the binding composite the significant Authority and Purity misses offset, netting +0.01 [-0.16, +0.19], which reconciles with T3. The match does not extend beyond binding: Care is a panel constant, not a population-tracking quantity. Across all fourteen conditions ever run (this study's ten plus the country-framing run's India, Nigeria, Sweden, and United States arms), panel Care spans 4.29 to 4.88 with every CI floor at or above 4.11; the lowest condition (JA framed, 4.29) sits +1.26 [+1.09, +1.45] above the measured Japanese Care of 3.03.

## B7. The refusal

kimi, Arabic neutral, iteration 5. Four attempts under the fixed-seed protocol (which replays the identical item order and API seed): three returned empty text, one returned an explicit in-Arabic refusal, no ratings object in any. The same model completed the other four item orders of the same condition, and every English cell, normally. Recorded as a refusal, excluded from scoring.

## B8. Order randomization audit

Post-hoc verification across every recorded run in this study and its baselines: 770 runs, 770 distinct presentation orders; zero orders repeated within a model-condition across iterations; zero orders shared between models within the same condition and iteration; zero runs in canonical (unshuffled) order. Ratings are keyed to item identity, so scoring is order-independent by construction; the presented order is preserved per cell in `presentation_order`.

## B9. Reproducibility

`validity/build_lang_instruments.py` rebuilds the per-language instruments from the official translation files (item wording is not redistributed; filled instruments are git-ignored). `validity/run_framed_lang.py` and `validity/run_framed.py` produced the cells; both are resumable, and every cell records its seed, presentation order, raw text, and (for framed in-language cells) the framing translation used. `validity/analyze_lang.py` produces the descriptive tables; `validity/audit_inlanguage.py` produces every number in B3, B4, and B5 deterministically and reconciles its panel means against the descriptive analysis before testing.

---

Analysis is stdlib-reproducible from the raw runs. Responsibility for the work, and for any errors in it, is mine alone. Methodology was AI-assisted and that assistance is disclosed.

Declan Michaels | Cross-Cultural Alignment Study | moral-os.com
