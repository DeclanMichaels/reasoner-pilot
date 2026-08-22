# Statistical Appendix

Companion to the in-language MFQ-2 report. Every number here regenerates from the raw runs with three stdlib scripts: `validity/audit_inlanguage.py` (the test families, intervals and sweeps), `validity/build_appendix_tables.py` (B3, B3a and B6), and `validity/audit_inlanguage_grid.py` (the language-by-framing grid and the per-foundation errors). Random seed 20260723; bootstrap 100,000 iterations; sign-flip tests enumerate all 2,048 sign patterns exactly. Each interval is drawn from a stream seeded by that seed and the quantity's own name, so an interval does not depend on how many other quantities the run computed, and adding a condition cannot move an existing one. The tables here are emitted by script rather than transcribed.

## B1. Sample and data

Eleven models, 20 conditions, five iterations each: **1,100 scored cells**, collected 2026-08-21 in a single window under a single protocol.

- **In-language**, 9 conditions, 495 cells. Arabic framed as Egypt, Morocco, Saudi Arabia and the United Arab Emirates; Japanese framed as Japan; Farsi framed as Iran; and one unframed condition per language. The unframed conditions name no country, so there is one of each.
- **English framed**, 10 conditions, 550 cells: the four Arabic-speaking countries plus India, Iran, Japan, Nigeria, Sweden and the United States.
- **English unframed**, 1 condition, 55 cells.

Instruments are the official MFQ-2 translations from the validation materials. Framing instructions in Arabic, Japanese and Farsi are ours, built from one template per language that varies only the country name and the demonym, and each cell records the instruction it was sent verbatim.

Twelve calls failed during collection, all from provider rate limits or a reply that carried no ratings object. Every one was retried to success, so no cell is missing and no condition rests on fewer than five iterations.

The configured roster holds fifteen models; four are absent from every cell. Both Gemini models and Command A fell to vendor rate-limit and access policies. Kimi-K2.6 was in the panel until Together moved it off serverless during this collection, at which point it returned `model_not_available` on every call; **Kimi-K3 replaced it** under its own roster key so no cell can be confused between the two. All four exclusions are infrastructural, decided by availability before any response was seen, and no cell from any of them was scored or discarded on content.

## B2. Scoring and the unit of analysis

Foundation score: mean of its six items, scale 1 to 5. Binding composite: mean of Loyalty, Authority and Purity. The independent unit is the model: each model's five iterations are averaged first, and every test below operates on eleven per-model values. Panel SDs are population SDs over those eleven means.

## B3. Where the panel lands, by country

Binding composite, panel mean over eleven models. The English unframed column is one condition and repeats down the table; the unframed in-language column is one condition per language and repeats across the countries sharing that language, because neither condition names a country. Dashes mark arms not run.

| country | language | human | EN unframed | local unframed | EN framed | local framed |
|---|---|--:|--:|--:|--:|--:|
| Egypt | Arabic | 4.267 | 2.713 | 3.104 | 4.605 | 4.604 |
| Morocco | Arabic | 4.014 | 2.713 | 3.104 | 4.570 | 4.582 |
| Saudi Arabia | Arabic | 4.083 | 2.713 | 3.104 | 4.733 | 4.757 |
| United Arab Emirates | Arabic | 3.892 | 2.713 | 3.104 | 4.629 | 4.726 |
| Japan | Japanese | 2.652 | 2.713 | 2.676 | 3.668 | 3.434 |
| Iran | Farsi | 3.333 | 2.713 | 2.809 | 4.577 | 4.314 |
| Nigeria | n/a | 4.038 | 2.713 | - | 4.515 | - |
| India | n/a | n/a | 2.713 | - | 4.439 | - |
| Sweden | n/a | n/a | 2.713 | - | 2.282 | - |
| United States | n/a | n/a | 2.713 | - | 3.331 | - |

The same table as distance from that country's measured human mean. Positive is above the population.

| country | EN unframed | local unframed | EN framed | local framed |
|---|--:|--:|--:|--:|
| Egypt | -1.554 | -1.163 | +0.338 | +0.337 |
| Morocco | -1.301 | -0.910 | +0.556 | +0.568 |
| Saudi Arabia | -1.370 | -0.979 | +0.650 | +0.674 |
| United Arab Emirates | -1.179 | -0.788 | +0.737 | +0.834 |
| Japan | +0.061 | +0.024 | +1.016 | +0.782 |
| Iran | -0.620 | -0.524 | +1.244 | +0.981 |
| Nigeria | -1.325 | - | +0.477 | - |

Human anchors, treated as constants: Egypt 4.267, Saudi Arabia 4.083, Nigeria 4.038, Morocco 4.014, United Arab Emirates 3.892 and Japan 2.652, all from Atari et al. (2023) Study 2; Iran 3.333 from Hazrati et al. (2025) sample 2, on a shifted response scale rescaled linearly. India, Sweden and the United States are not in the MFQ-2 nineteen-nation set, so no overshoot is computable for them.

### The four Arabic-speaking countries

One instrument, one language, four populations with published means. The human means span 0.375, from Egypt at 4.267 down to the United Arab Emirates at 3.892. Framed in Arabic, the panel spans 0.175, and its ordering of the four is uncorrelated with the human ordering (Spearman +0.00). Framed in English the picture is the same: panel spread 0.164, Spearman +0.00.

| | human order | panel order |
|---|---|---|
| Arabic framed | Egypt > Saudi Arabia > Morocco > UAE | Saudi Arabia > UAE > Egypt > Morocco |
| English framed | Egypt > Saudi Arabia > Morocco > UAE | Saudi Arabia > UAE > Egypt > Morocco |

Framed in Arabic, 2 of 11 models order the four the way the populations do; framed in English, 6 of 11.

The unframed Arabic condition sits at 3.104, below all four populations, between 0.788 and 1.163 under them.

## B3a. Every condition, with intervals

Resampling models with replacement, 100,000 draws, percentile intervals.

| condition | panel mean | 95% CI | between-model SD |
|---|--:|:--:|--:|
| EN framed Egypt | 4.605 | [4.502, 4.703] | 0.17 |
| EN framed India | 4.439 | [4.335, 4.543] | 0.18 |
| EN framed Iran | 4.577 | [4.470, 4.671] | 0.17 |
| EN framed Japan | 3.668 | [3.479, 3.869] | 0.33 |
| EN framed Morocco | 4.570 | [4.482, 4.648] | 0.14 |
| EN framed Nigeria | 4.515 | [4.425, 4.606] | 0.15 |
| EN framed Saudi Arabia | 4.733 | [4.654, 4.803] | 0.13 |
| EN framed Sweden | 2.282 | [2.194, 2.365] | 0.14 |
| EN framed United Arab Emirates | 4.629 | [4.551, 4.704] | 0.13 |
| EN framed United States | 3.331 | [3.193, 3.456] | 0.22 |
| AR framed Egypt | 4.604 | [4.486, 4.718] | 0.20 |
| AR framed Morocco | 4.582 | [4.473, 4.682] | 0.18 |
| AR framed Saudi Arabia | 4.757 | [4.682, 4.822] | 0.12 |
| AR framed United Arab Emirates | 4.726 | [4.658, 4.791] | 0.11 |
| AR neutral | 3.104 | [2.840, 3.374] | 0.45 |
| EN neutral | 2.713 | [2.542, 2.898] | 0.30 |
| FA framed Iran | 4.314 | [4.148, 4.476] | 0.28 |
| FA neutral | 2.809 | [2.565, 3.066] | 0.43 |
| JA framed Japan | 3.434 | [3.353, 3.514] | 0.14 |
| JA neutral | 2.676 | [2.494, 2.885] | 0.33 |

## B4. The test families

Two families, one per headline claim, both post hoc and both exploratory. Paired tests use per-model differences; anchor tests subtract the constant from each model's mean. Exact sign-flip permutation: with eleven models the minimum attainable two-sided p is 2/2048, reported as 0.001. Nothing was pre-registered.

**Family A, the framing claim.** Ten comparisons, Holm across the ten.

| test | difference | 95% CI | exact p | Holm |
|---|--:|:--:|--:|--:|
| T1 Egypt: EN framed vs AR framed | +0.001 | [-0.054, +0.048] | 1.000 | 1.00 |
| T2 Japan: EN framed vs JA framed | +0.233 | [+0.098, +0.384] | .0059 | .023 |
| T3 JA neutral vs Japan anchor | +0.024 | [-0.155, +0.233] | .833 | 1.00 |
| T4 FA framed vs Iran anchor | +0.981 | [+0.815, +1.144] | .001 | .0098 |
| T5 FA neutral vs EN neutral | +0.096 | [-0.031, +0.214] | .176 | .527 |
| T6 AR neutral vs EN neutral | +0.391 | [+0.255, +0.529] | .002 | .014 |
| T7 AR framed vs Egypt anchor | +0.337 | [+0.218, +0.450] | .002 | .014 |
| T8 Japan: framed vs neutral, in-language | +0.759 | [+0.592, +0.921] | .001 | .0098 |
| T9 EN framed Iran vs Iran anchor | +1.244 | [+1.137, +1.338] | .001 | .0098 |
| T10 Iran: EN framed vs FA framed | +0.263 | [+0.148, +0.380] | .0029 | .015 |

Nulls are reported as bounds, not as demonstrated absence: any Egypt language effect is within 0.054, and any Japanese-neutral displacement from the Japanese mean is within 0.233.

**Family B, the language claim.** One comparison per language, asking whether that language's unframed condition departs from the panel's English default. Holm across the three. T5 and T6 sit in both families; the double membership is disclosed rather than removed by re-cutting family A, and every conclusion holds under either cut.

| test | difference | 95% CI | exact p | Holm | models moving up |
|---|--:|:--:|--:|--:|--:|
| T5 FA neutral vs EN neutral | +0.096 | [-0.031, +0.214] | .176 | .352 | 7 of 11 |
| T6 AR neutral vs EN neutral | +0.391 | [+0.255, +0.529] | .002 | **.006** | 10 of 11, none down |
| T11 JA neutral vs EN neutral | -0.037 | [-0.249, +0.164] | .750 | .750 | 4 of 11 |

Arabic is the only language that moves the panel, and no model moves against it. Farsi and Japanese split near evenly, which is what no effect looks like at this unit. As bounds: any Farsi departure from the English default is within 0.214, and any Japanese departure is within 0.249.

One further comparison is reported outside both families as a single descriptive: the English default sits +0.061 from the Japanese human mean. The panel's untouched English resting point is already close to Japan's measured binding composite.

## B5. Robustness: leave-one-model-out

Japanese neutral panel mean with each model removed spans 2.603 to 2.714 around an anchor of 2.652. English-framed Iran overshoot spans +1.219 to +1.269; Farsi-framed Iran overshoot spans +0.936 to +1.033. Every individual model overshoots both Iran conditions. T11, the Japanese language effect, spans -0.106 to +0.010 under the same sweep and does not change sign in a way that would carry the claim.

## B6. Per-foundation panel means

| condition | Care | Equality | Proportionality | Loyalty | Authority | Purity |
|---|--:|--:|--:|--:|--:|--:|
| EN framed Egypt | 4.74 | 2.54 | 4.25 | 4.73 | 4.80 | 4.29 |
| EN framed India | 4.77 | 2.50 | 4.22 | 4.60 | 4.71 | 4.01 |
| EN framed Iran | 4.85 | 2.55 | 4.23 | 4.72 | 4.69 | 4.32 |
| EN framed Japan | 4.31 | 2.40 | 4.05 | 3.85 | 4.18 | 2.97 |
| EN framed Morocco | 4.84 | 2.53 | 4.20 | 4.69 | 4.77 | 4.25 |
| EN framed Nigeria | 4.76 | 2.59 | 4.41 | 4.58 | 4.78 | 4.19 |
| EN framed Saudi Arabia | 4.75 | 2.12 | 4.43 | 4.81 | 4.92 | 4.47 |
| EN framed Sweden | 4.69 | 2.88 | 3.66 | 2.91 | 2.34 | 1.60 |
| EN framed United Arab Emirates | 4.72 | 2.18 | 4.35 | 4.78 | 4.87 | 4.23 |
| EN framed United States | 4.35 | 2.02 | 4.46 | 3.81 | 3.52 | 2.66 |
| AR framed Egypt | 4.87 | 2.78 | 4.46 | 4.74 | 4.74 | 4.33 |
| AR framed Morocco | 4.83 | 2.72 | 4.39 | 4.68 | 4.73 | 4.33 |
| AR framed Saudi Arabia | 4.85 | 2.27 | 4.62 | 4.84 | 4.89 | 4.53 |
| AR framed United Arab Emirates | 4.86 | 2.19 | 4.56 | 4.87 | 4.90 | 4.41 |
| AR neutral | 4.73 | 2.32 | 4.24 | 3.42 | 3.35 | 2.55 |
| EN neutral | 4.70 | 2.05 | 4.20 | 3.14 | 3.12 | 1.88 |
| FA framed Iran | 4.71 | 2.62 | 4.32 | 4.42 | 4.38 | 4.15 |
| FA neutral | 4.67 | 2.21 | 4.17 | 3.10 | 3.08 | 2.25 |
| JA framed Japan | 4.29 | 2.40 | 3.98 | 3.54 | 3.82 | 2.94 |
| JA neutral | 4.61 | 2.10 | 4.00 | 2.94 | 3.06 | 2.03 |
| **Japan, measured** | 3.03 | 2.27 | 3.14 | 2.66 | 2.67 | 2.63 |
| **Iran, measured** | 3.95 | 2.67 | 4.15 | 3.63 | 3.05 | 3.32 |

Care sits between 4.29 and 4.87 in every one of the twenty conditions, against a measured Japanese Care of 3.03 and a measured Iranian Care of 3.95. Equality is the only foundation on which the panel ever lands near a measured value.

## B7. Failed calls

Twelve of 1,112 attempted calls returned no ratings object, from provider rate limits on the Together-hosted models and from replies that carried no parseable object. All twelve were retried to success within the same collection window, so every one of the 1,100 scored cells is present and no condition rests on fewer than five iterations. This collection contains no refusal.

## B8. Presentation-order audit

Across all 1,100 scored runs: no two iterations of the same model in the same condition share an order, no two models share an order within the same condition and iteration, and no run used the canonical unshuffled order.

Orders **are** shared deliberately in one place. The four Arabic framed countries draw the same order for a given model and iteration, so the between-country contrast is paired on presentation order. All 55 model-iteration groups match this way. The English framed countries do not share orders, because that runner keys its draw on the country. The asymmetry costs the English four-country contrast some precision and introduces no bias, since order is randomized and ratings are keyed to item identity rather than position.

## B9. Reproducibility

`validity/build_lang_instruments.py` rebuilds the per-language instruments from the official translation files; item wording is not redistributed and the filled instruments are git-ignored. `validity/run_framed_lang.py`, `validity/run_framed.py` and `validity/run_validity.py` produced the cells; all are resumable, and every cell records its seed, presentation order, raw text and the framing instruction it was sent. `validity/fill.sh` re-invokes each runner until nothing remains, which is how the rate-limit gaps were closed.

`validity/audit_inlanguage.py` produces B4 and B5, and reconciles first against an independent recomputation from the raw cells: the plain mean of the eighteen binding items against the average of three foundation means. Those agree only if each binding foundation carries the same number of items, so the gate verifies the counts it depends on. It writes `results/condition_means.json`, and `validity/audit_inlanguage_grid.py` reconciles against that file rather than against constants. `validity/build_appendix_tables.py` emits B3, B3a and B6.

The July 2026 collection is preserved unchanged at `validity/archive-2026-07/`.

---

Analysis is stdlib-reproducible from the raw runs. Responsibility for the work, and for any errors in it, is mine alone. Methodology was AI-assisted and that assistance is disclosed.

Declan Michaels | Cross-Cultural Alignment Study | moral-os.com
