# Statistical Appendix

Companion to the in-language MFQ-2 report. Every number here regenerates from the raw runs with three stdlib scripts: `validity/audit_inlanguage.py` (the test families, intervals and sweeps), `validity/build_appendix_tables.py` (B3, B3a and B6), and `validity/audit_inlanguage_grid.py` (the language-by-framing grid and the per-foundation errors). Random seed 20260723; bootstrap 100,000 iterations; sign-flip tests enumerate all 2,048 sign patterns exactly. Each interval is drawn from a stream seeded by that seed and the quantity's own name, so an interval does not depend on how many other quantities the run computed, and adding a condition cannot move an existing one. The tables here are emitted by script rather than transcribed.

## B1. Sample and data

Eleven models, 50 conditions, five iterations each: **2,750 scored cells**, collected 2026-08-21 to 2026-08-23 in a single window under a single protocol.

All fifty are reported in B3a and B6. Five of them are English unframed, because the English comparator changed during the study: `official_nosystem` is the matched cell used as the baseline, `en_neutral_ours` is the comparator it replaced, and `ours_nosystem`, `ours_selfreport` and `official_selfreport` are the variants collected to measure that change. The test families in B4 draw on the conditions each test names.

- **In-language**, 22 conditions, 1,210 cells. Arabic framed as Egypt, Morocco, Saudi Arabia and the United Arab Emirates; Spanish framed as Argentina, Chile, Colombia, Mexico, Morocco and Peru; French framed as Belgium, France and Switzerland; Japanese framed as Japan; Farsi framed as Iran; Russian framed as Russia; and one unframed condition per language. The unframed conditions name no country, so there is one of each, six in all.
- **English framed**, 23 conditions, 1,265 cells: every country named above plus India, Ireland, Kenya, New Zealand, Nigeria, South Africa, Sweden and the United States.
- **English unframed**, 5 conditions, 275 cells: the matched comparator `official_nosystem`, the retained `en_neutral_ours`, and the three variants named above.

Instruments are the official MFQ-2 translations from the validation materials. Framing instructions in Arabic, Spanish, French, Japanese, Farsi and Russian are ours, built from one template per language that varies only the country name and the demonym, and each cell records the instruction it was sent verbatim.

Calls that failed during collection were all retried to success, so no cell is missing and no condition rests on fewer than five iterations. B7 has the counts.

The configured roster holds fifteen models; four are absent from every cell. Both Gemini models and Command A fell to vendor rate-limit and access policies. Kimi-K2.6 was in the panel until Together moved it off serverless during this collection, at which point it returned `model_not_available` on every call; **Kimi-K3 replaced it** under its own roster key so no cell can be confused between the two. All four exclusions are infrastructural, decided by availability before any response was seen, and no cell from any of them was scored or discarded on content.

## B2. Scoring and the unit of analysis

Foundation score: mean of its six items, scale 1 to 5. Binding composite: mean of Loyalty, Authority and Purity. The independent unit is the model: each model's five iterations are averaged first, and every test below operates on eleven per-model values. Panel SDs are population SDs over those eleven means.

## B3. Where the panel lands, by country

Binding composite, panel mean over eleven models, each model's five iterations averaged first. The English unframed column is one condition and repeats down the table; the unframed in-language column is one condition per language and repeats across the countries that share a language, because neither condition names a country. Dashes mark arms not run.

| country | language | human | EN unframed | local unframed | EN framed | local framed |
|---|---|--:|--:|--:|--:|--:|
| Egypt | Arabic | 4.267 | 2.769 | 3.104 | 4.605 | 4.604 |
| Morocco [d12] | Arabic | 4.014 | 2.769 | 3.104 | 4.570 | 4.582 |
| Saudi Arabia | Arabic | 4.083 | 2.769 | 3.104 | 4.733 | 4.757 |
| United Arab Emirates | Arabic | 3.892 | 2.769 | 3.104 | 4.629 | 4.726 |
| Argentina | Spanish | 3.283 | 2.769 | 2.780 | 3.437 | 3.349 |
| Chile | Spanish | 3.220 | 2.769 | 2.780 | 3.654 | 3.576 |
| Colombia | Spanish | 3.497 | 2.769 | 2.780 | 4.100 | 3.996 |
| Mexico | Spanish | 3.512 | 2.769 | 2.780 | 4.141 | 3.947 |
| Peru | Spanish | 3.514 | 2.769 | 2.780 | 4.133 | 4.038 |
| Belgium | French | 3.444 | 2.769 | 2.777 | 2.622 | 2.797 |
| France | French | 3.610 | 2.769 | 2.777 | 2.725 | 2.834 |
| Switzerland | French | 3.349 | 2.769 | 2.777 | 3.063 | 3.076 |
| Japan | Japanese | 2.652 | 2.769 | 2.676 | 3.668 | 3.434 |
| Iran [*] | Farsi | 3.333 | 2.769 | 2.809 | 4.577 | 4.314 |
| Russia | Russian | 3.599 | 2.769 | 2.788 | 4.117 | 4.047 |
| India | n/a | n/a | 2.769 | - | 4.439 | - |
| Ireland | n/a | 3.096 | 2.769 | - | 3.094 | - |
| Kenya | n/a | 3.867 | 2.769 | - | 4.432 | - |
| New Zealand | n/a | 3.094 | 2.769 | - | 2.878 | - |
| Nigeria | n/a | 4.038 | 2.769 | - | 4.515 | - |
| South Africa | n/a | 3.749 | 2.769 | - | 3.935 | - |
| Sweden | n/a | n/a | 2.769 | - | 2.282 | - |
| United States | n/a | n/a | 2.769 | - | 3.331 | - |

The same table as distance from that country's measured human mean. Positive is above the population.

| country | EN unframed | local unframed | EN framed | local framed |
|---|--:|--:|--:|--:|
| Egypt | -1.498 | -1.163 | +0.338 | +0.337 |
| Morocco [d12] | -1.245 | -1.234 | +0.556 | +0.575 |
| Saudi Arabia | -1.314 | -0.979 | +0.650 | +0.674 |
| United Arab Emirates | -1.123 | -0.788 | +0.737 | +0.834 |
| Argentina | -0.514 | -0.503 | +0.154 | +0.066 |
| Chile | -0.451 | -0.440 | +0.434 | +0.356 |
| Colombia | -0.728 | -0.717 | +0.603 | +0.499 |
| Mexico | -0.743 | -0.732 | +0.629 | +0.435 |
| Peru | -0.745 | -0.734 | +0.619 | +0.524 |
| Belgium | -0.675 | -0.667 | -0.822 | -0.647 |
| France | -0.841 | -0.833 | -0.885 | -0.776 |
| Switzerland | -0.580 | -0.572 | -0.286 | -0.273 |
| Japan | +0.117 | +0.024 | +1.016 | +0.782 |
| Iran [*] | -0.564 | -0.524 | +1.244 | +0.981 |
| Russia | -0.830 | -0.811 | +0.518 | +0.448 |
| Ireland | -0.327 | - | -0.002 | - |
| Kenya | -1.098 | - | +0.565 | - |
| New Zealand | -0.325 | - | -0.216 | - |
| Nigeria | -1.269 | - | +0.477 | - |
| South Africa | -0.980 | - | +0.186 | - |
Each of those nineteen means rests on 205 to 207 respondents for its country, 3,902 in all, collected by Atari et al. in May 2021 through Qualtrics Panels and stratified within each nation on age, gender and political orientation. Education was not a stratification variable, and the authors state their results rest on "a subset of these populations who were educated enough to complete the surveys online", noting that people from traditional, small-scale communities are absent. Every overshoot in this appendix is a distance from those samples' means.

[*] Iran's anchor is the only one not drawn from Atari et al. (2023) Study 2. B4 carries the source, the sample's own caveats and the sensitivity across every anchor that source offers.

[d12] Morocco: grouped with Arabic above, compared against its human mean on the Spanish arm, because Atari et al. administered Morocco's sample in Spanish. Both runs are carried in the data.

Human anchors, treated as constants, binding as the mean of loyalty, authority and purity: Egypt 4.267 (Atari 2023 Study 2), Morocco 4.014 (Atari 2023 Study 2), Saudi Arabia 4.083 (Atari 2023 Study 2), United Arab Emirates 3.892 (Atari 2023 Study 2), Argentina 3.283 (Atari 2023 Study 2), Chile 3.220 (Atari 2023 Study 2), Colombia 3.497 (Atari 2023 Study 2), Mexico 3.512 (Atari 2023 Study 2), Peru 3.514 (Atari 2023 Study 2), Belgium 3.444 (Atari 2023 Study 2), France 3.610 (Atari 2023 Study 2), Switzerland 3.349 (Atari 2023 Study 2), Japan 2.652 (Atari 2023 Study 2), Iran 3.333 (Hazrati 2025 sample 2), Russia 3.599 (Atari 2023 Study 2), Ireland 3.096 (Atari 2023 Study 2), Kenya 3.867 (Atari 2023 Study 2), New Zealand 3.094 (Atari 2023 Study 2), Nigeria 4.038 (Atari 2023 Study 2), South Africa 3.749 (Atari 2023 Study 2). India, Sweden and the United States are not in the MFQ-2 nineteen-nation set, so no overshoot is computable for them. Iran's sample was administered on a 0-4 scale and shifted linearly by +1 for comparability with the 1-5 runs; anchors_iran.json carries the detail and the caveats.


### The four Arabic-speaking countries

One instrument, one language, four populations with published means. The human means span 0.375, from Egypt at 4.267 down to the United Arab Emirates at 3.892. Framed in Arabic, the panel spans 0.175, and its ordering of the four is uncorrelated with the human ordering (Spearman +0.00). Framed in English the picture is the same: panel spread 0.164, Spearman +0.00.

| | human order | panel order |
|---|---|---|
| Arabic framed | Egypt > Saudi Arabia > Morocco > UAE | Saudi Arabia > UAE > Egypt > Morocco |
| English framed | Egypt > Saudi Arabia > Morocco > UAE | Saudi Arabia > UAE > Egypt > Morocco |

Framed in Arabic, 2 of 11 models order the four the way the populations do; framed in English, 6 of 11.

The unframed Arabic condition sits at 3.104, below all four populations, between 0.788 and 1.163 under them.

## B3a. Every condition, with intervals

| condition | panel mean | 95% CI | between-model SD |
|---|--:|:--:|--:|
| EN_framed_Argentina | 3.437 | [3.316, 3.557] | 0.20 |
| EN_framed_Belgium | 2.622 | [2.523, 2.742] | 0.19 |
| EN_framed_Chile | 3.654 | [3.534, 3.788] | 0.21 |
| EN_framed_Colombia | 4.100 | [3.981, 4.220] | 0.20 |
| EN_framed_Egypt | 4.605 | [4.502, 4.703] | 0.17 |
| EN_framed_France | 2.725 | [2.637, 2.838] | 0.17 |
| EN_framed_India | 4.439 | [4.335, 4.543] | 0.18 |
| EN_framed_Iran | 4.577 | [4.470, 4.671] | 0.17 |
| EN_framed_Ireland | 3.094 | [2.957, 3.252] | 0.25 |
| EN_framed_Japan | 3.668 | [3.479, 3.869] | 0.33 |
| EN_framed_Kenya | 4.432 | [4.365, 4.504] | 0.12 |
| EN_framed_Mexico | 4.141 | [4.071, 4.223] | 0.13 |
| EN_framed_Morocco | 4.570 | [4.482, 4.648] | 0.14 |
| EN_framed_New Zealand | 2.878 | [2.816, 2.943] | 0.11 |
| EN_framed_Nigeria | 4.515 | [4.425, 4.606] | 0.15 |
| EN_framed_Peru | 4.133 | [4.017, 4.242] | 0.19 |
| EN_framed_Russia | 4.117 | [3.982, 4.262] | 0.24 |
| EN_framed_Saudi Arabia | 4.733 | [4.654, 4.803] | 0.13 |
| EN_framed_South Africa | 3.935 | [3.841, 4.024] | 0.16 |
| EN_framed_Sweden | 2.282 | [2.194, 2.365] | 0.14 |
| EN_framed_Switzerland | 3.063 | [2.913, 3.219] | 0.26 |
| EN_framed_United Arab Emirates | 4.629 | [4.551, 4.704] | 0.13 |
| EN_framed_United States | 3.331 | [3.193, 3.456] | 0.22 |
| ar_framed_Egypt | 4.604 | [4.486, 4.718] | 0.20 |
| ar_framed_Morocco | 4.582 | [4.473, 4.682] | 0.18 |
| ar_framed_Saudi Arabia | 4.757 | [4.682, 4.822] | 0.12 |
| ar_framed_United Arab Emirates | 4.726 | [4.658, 4.791] | 0.11 |
| ar_neutral | 3.104 | [2.840, 3.374] | 0.45 |
| en_baseline_official_selfreport | 2.695 | [2.526, 2.860] | 0.28 |
| en_baseline_ours_nosystem | 2.760 | [2.548, 2.983] | 0.37 |
| en_baseline_ours_selfreport | 2.733 | [2.560, 2.924] | 0.31 |
| en_neutral | 2.769 | [2.608, 2.934] | 0.28 |
| en_neutral_ours | 2.713 | [2.541, 2.897] | 0.30 |
| es_framed_Argentina | 3.349 | [3.236, 3.475] | 0.20 |
| es_framed_Chile | 3.576 | [3.478, 3.677] | 0.17 |
| es_framed_Colombia | 3.996 | [3.909, 4.091] | 0.16 |
| es_framed_Mexico | 3.947 | [3.849, 4.045] | 0.17 |
| es_framed_Morocco | 4.589 | [4.496, 4.669] | 0.15 |
| es_framed_Peru | 4.038 | [3.920, 4.157] | 0.20 |
| es_neutral | 2.780 | [2.582, 2.967] | 0.33 |
| fa_framed_Iran | 4.314 | [4.148, 4.476] | 0.28 |
| fa_neutral | 2.809 | [2.565, 3.066] | 0.43 |
| fr_framed_Belgium | 2.797 | [2.713, 2.893] | 0.15 |
| fr_framed_France | 2.834 | [2.755, 2.921] | 0.14 |
| fr_framed_Switzerland | 3.076 | [2.972, 3.185] | 0.18 |
| fr_neutral | 2.777 | [2.590, 2.977] | 0.33 |
| ja_framed_Japan | 3.434 | [3.353, 3.514] | 0.14 |
| ja_neutral | 2.676 | [2.494, 2.885] | 0.33 |
| ru_framed_Russia | 4.047 | [3.908, 4.189] | 0.24 |
| ru_neutral | 2.788 | [2.582, 3.004] | 0.36 |

## B4. The test families

Two families, one per headline claim, both post hoc and both exploratory. Paired tests use per-model differences; anchor tests subtract the constant from each model's mean. Exact sign-flip permutation: with eleven models the minimum attainable two-sided p is 2/2048, reported as 0.001. Nothing was pre-registered.

**Family A, the framing claim.** Ten comparisons, Holm across the ten.

| test | difference | 95% CI | exact p | Holm |
|---|--:|:--:|--:|--:|
| T1 Egypt: EN-framed vs AR-framed | +0.001 | [-0.054, +0.048] | 1.0000 | 1.0000 |
| T2 Japan: EN-framed vs JA-framed | +0.233 | [+0.098, +0.384] | 0.0059 | 0.0234 |
| T3 JA-neutral vs Japan anchor | +0.024 | [-0.155, +0.233] | 0.8330 | 1.0000 |
| T4 FA-framed vs Iran anchor [*] | +0.981 | [+0.815, +1.144] | 0.0010 | 0.0098 |
| T5 FA-neutral vs EN-neutral | +0.040 | [-0.117, +0.184] | 0.6357 | 1.0000 |
| T6 AR-neutral vs EN-neutral | +0.335 | [+0.201, +0.483] | 0.0010 | 0.0098 |
| T7 AR-framed vs Egypt anchor | +0.337 | [+0.218, +0.450] | 0.0020 | 0.0117 |
| T8 Japan: framed vs neutral (in-lang) | +0.759 | [+0.592, +0.921] | 0.0010 | 0.0098 |
| T9 EN-framed Iran vs Iran anchor [*] | +1.244 | [+1.137, +1.338] | 0.0010 | 0.0098 |
| T10 Iran: EN-framed vs FA-framed | +0.263 | [+0.148, +0.380] | 0.0029 | 0.0146 |

Nulls are reported as bounds, not as demonstrated absence: any Egypt language effect is within 0.054, and any Japanese-neutral displacement from the Japanese mean is within 0.233.

**Family B, the language claim.** One comparison per language, asking whether that language's unframed condition departs from the panel's English default. Holm across the three. T5 and T6 sit in both families; the double membership is disclosed rather than removed by re-cutting family A, and every conclusion holds under either cut.

| test | difference | 95% CI | exact p | Holm | models moving up |
|---|--:|:--:|--:|--:|--:|
| T5 FA-neutral vs EN-neutral | +0.040 | [-0.117, +0.184] | 0.6357 | 0.8613 | 7 of 11 |
| T6 AR-neutral vs EN-neutral | +0.335 | [+0.201, +0.483] | 0.0010 | 0.0029 | 11 of 11, none down |
| T11 JA-neutral vs EN-neutral | -0.093 | [-0.299, +0.111] | 0.4307 | 0.8613 | 3 of 11 |

Arabic is the only language whose interval excludes zero, and no model moves against it. Farsi splits 7 up to 4 down and Japanese 3 up to 8 down. As bounds: any Farsi departure from the English default is within 0.184, and any Japanese departure is within 0.299.

One further comparison is reported outside both families as a single descriptive: the English default sits +0.117 from the Japanese human mean.

**[*] The Iran anchor, and what it costs.** Nineteen of the twenty anchors are Atari et al. (2023) Study 2. Iran is not in that set; its anchor is Hazrati, Nejat and Daneshi (2025), a different paper with different collection conditions. That sample is a Telegram and snowball convenience sample, n=989, 68 to 71 percent female, mean age 26 to 28, 57 to 59 percent educated to bachelor's or above, and the anchor file records it as likely less binding-endorsing than the general Iranian population - which would bias this overshoot upward. Collection began a year after the Woman, Life, Freedom movement and the authors note possible period effects. Iran is the only Farsi country, so it carries that group throughout.

Every anchor the source offers is shown. The one in use is the largest of the three, so the overshoot reported throughout is the smallest of the three:

| Iran anchor | binding | EN-framed overshoot | FA-framed overshoot |
|---|--:|--:|--:|
| sample 2, n=989 (in use) | 3.333 | +1.244 | +0.981 |
| sample 1, n=392 | 3.231 | +1.346 | +1.083 |
| n-weighted pool of both | 3.304 | +1.273 | +1.010 |

The sign and the ordering of the Iran result do not depend on the choice. Its magnitude does, by up to 0.102.

## B5. Robustness: leave-one-model-out

Japanese neutral panel mean with each model removed spans 2.603 to 2.714 around an anchor of 2.652. English-framed Iran overshoot spans +1.220 to +1.284; Farsi-framed Iran overshoot spans +0.933 to +1.030. Every individual model overshoots both Iran conditions. T11, the Japanese language effect, spans -0.162 to -0.020 under the same sweep.

## B6. Per-foundation panel means

All fifty conditions, then the measured human mean for each of the twenty anchored countries, in the country order of B3. The measured rows are populations, not conditions; they are here to be read against the panel rows above.

| condition | Care | Equality | Proportionality | Loyalty | Authority | Purity |
|---|--:|--:|--:|--:|--:|--:|
| EN_framed_Argentina | 4.70 | 2.78 | 4.06 | 4.10 | 3.64 | 2.57 |
| EN_framed_Belgium | 4.48 | 2.35 | 3.94 | 3.08 | 2.85 | 1.94 |
| EN_framed_Chile | 4.58 | 2.62 | 4.15 | 4.05 | 3.93 | 2.98 |
| EN_framed_Colombia | 4.84 | 2.62 | 4.29 | 4.42 | 4.41 | 3.48 |
| EN_framed_Egypt | 4.74 | 2.54 | 4.25 | 4.73 | 4.80 | 4.29 |
| EN_framed_France | 4.39 | 2.63 | 3.90 | 3.31 | 2.86 | 2.01 |
| EN_framed_India | 4.77 | 2.50 | 4.22 | 4.60 | 4.71 | 4.01 |
| EN_framed_Iran | 4.85 | 2.55 | 4.23 | 4.72 | 4.69 | 4.32 |
| EN_framed_Ireland | 4.61 | 2.30 | 4.05 | 3.67 | 3.27 | 2.34 |
| EN_framed_Japan | 4.31 | 2.40 | 4.05 | 3.85 | 4.18 | 2.97 |
| EN_framed_Kenya | 4.81 | 2.58 | 4.31 | 4.58 | 4.69 | 4.02 |
| EN_framed_Mexico | 4.89 | 2.78 | 4.19 | 4.39 | 4.51 | 3.52 |
| EN_framed_Morocco | 4.84 | 2.53 | 4.20 | 4.69 | 4.77 | 4.25 |
| EN_framed_New Zealand | 4.52 | 2.35 | 4.03 | 3.48 | 3.02 | 2.14 |
| EN_framed_Nigeria | 4.76 | 2.59 | 4.41 | 4.58 | 4.78 | 4.19 |
| EN_framed_Peru | 4.78 | 2.77 | 4.22 | 4.39 | 4.42 | 3.58 |
| EN_framed_Russia | 4.32 | 2.59 | 4.17 | 4.53 | 4.48 | 3.35 |
| EN_framed_Saudi Arabia | 4.75 | 2.12 | 4.43 | 4.81 | 4.92 | 4.47 |
| EN_framed_South Africa | 4.81 | 2.93 | 4.06 | 4.18 | 4.22 | 3.40 |
| EN_framed_Sweden | 4.69 | 2.88 | 3.66 | 2.91 | 2.34 | 1.60 |
| EN_framed_Switzerland | 4.30 | 2.05 | 4.19 | 3.60 | 3.24 | 2.35 |
| EN_framed_United Arab Emirates | 4.72 | 2.18 | 4.35 | 4.78 | 4.87 | 4.23 |
| EN_framed_United States | 4.35 | 2.02 | 4.46 | 3.81 | 3.52 | 2.66 |
| ar_framed_Egypt | 4.87 | 2.78 | 4.46 | 4.74 | 4.74 | 4.33 |
| ar_framed_Morocco | 4.83 | 2.72 | 4.39 | 4.68 | 4.73 | 4.33 |
| ar_framed_Saudi Arabia | 4.85 | 2.27 | 4.62 | 4.84 | 4.89 | 4.53 |
| ar_framed_United Arab Emirates | 4.86 | 2.19 | 4.56 | 4.87 | 4.90 | 4.41 |
| ar_neutral | 4.73 | 2.32 | 4.24 | 3.42 | 3.35 | 2.55 |
| en_baseline_official_selfreport | 4.62 | 1.97 | 4.19 | 3.15 | 3.05 | 1.88 |
| en_baseline_ours_nosystem | 4.68 | 2.03 | 4.21 | 3.18 | 3.13 | 1.97 |
| en_baseline_ours_selfreport | 4.61 | 1.99 | 4.22 | 3.18 | 3.11 | 1.91 |
| en_neutral | 4.71 | 1.98 | 4.18 | 3.19 | 3.15 | 1.97 |
| en_neutral_ours | 4.70 | 2.05 | 4.20 | 3.14 | 3.12 | 1.88 |
| es_framed_Argentina | 4.63 | 2.65 | 4.07 | 3.92 | 3.68 | 2.45 |
| es_framed_Chile | 4.54 | 2.51 | 4.16 | 3.91 | 3.92 | 2.89 |
| es_framed_Colombia | 4.76 | 2.58 | 4.23 | 4.23 | 4.33 | 3.43 |
| es_framed_Mexico | 4.66 | 2.57 | 4.15 | 4.18 | 4.31 | 3.35 |
| es_framed_Morocco | 4.79 | 2.44 | 4.18 | 4.62 | 4.83 | 4.32 |
| es_framed_Peru | 4.72 | 2.66 | 4.22 | 4.25 | 4.36 | 3.51 |
| es_neutral | 4.57 | 1.99 | 4.07 | 3.07 | 3.21 | 2.06 |
| fa_framed_Iran | 4.71 | 2.62 | 4.32 | 4.42 | 4.38 | 4.15 |
| fa_neutral | 4.67 | 2.21 | 4.17 | 3.10 | 3.08 | 2.25 |
| fr_framed_Belgium | 4.55 | 2.42 | 4.00 | 3.25 | 2.93 | 2.22 |
| fr_framed_France | 4.43 | 2.48 | 3.97 | 3.34 | 2.93 | 2.23 |
| fr_framed_Switzerland | 4.38 | 2.08 | 4.18 | 3.54 | 3.18 | 2.51 |
| fr_neutral | 4.43 | 2.23 | 3.97 | 3.08 | 3.02 | 2.23 |
| ja_framed_Japan | 4.29 | 2.40 | 3.98 | 3.54 | 3.82 | 2.94 |
| ja_neutral | 4.61 | 2.10 | 4.00 | 2.94 | 3.06 | 2.03 |
| ru_framed_Russia | 4.54 | 2.57 | 4.32 | 4.38 | 4.41 | 3.35 |
| ru_neutral | 4.71 | 2.10 | 4.21 | 3.16 | 3.16 | 2.05 |
| **Egypt, measured** | 4.38 | 3.56 | 4.37 | 4.42 | 4.18 | 4.19 |
| **Morocco, measured** [d12] | 4.21 | 3.36 | 4.18 | 4.16 | 3.95 | 3.93 |
| **Saudi Arabia, measured** | 4.24 | 3.32 | 4.18 | 4.20 | 4.07 | 3.98 |
| **United Arab Emirates, measured** | 4.01 | 3.28 | 3.96 | 4.02 | 3.91 | 3.74 |
| **Argentina, measured** | 3.84 | 2.81 | 3.91 | 3.58 | 3.67 | 2.60 |
| **Chile, measured** | 3.77 | 2.77 | 3.70 | 3.45 | 3.67 | 2.54 |
| **Colombia, measured** | 3.83 | 2.91 | 3.69 | 3.67 | 3.84 | 2.98 |
| **Mexico, measured** | 3.77 | 2.87 | 3.80 | 3.78 | 3.94 | 2.81 |
| **Peru, measured** | 3.62 | 2.63 | 3.75 | 3.73 | 3.81 | 3.00 |
| **Belgium, measured** | 3.91 | 3.20 | 3.91 | 3.62 | 3.70 | 3.01 |
| **France, measured** | 4.08 | 3.23 | 4.12 | 3.86 | 3.88 | 3.09 |
| **Switzerland, measured** | 3.95 | 3.27 | 3.84 | 3.58 | 3.52 | 2.95 |
| **Japan, measured** | 3.03 | 2.27 | 3.14 | 2.66 | 2.67 | 2.63 |
| **Iran, measured** [*] | 3.95 | 2.67 | 4.15 | 3.63 | 3.05 | 3.32 |
| **Russia, measured** | 3.96 | 3.24 | 4.27 | 3.87 | 3.68 | 3.25 |
| **Ireland, measured** | 4.01 | 2.94 | 3.73 | 3.29 | 3.49 | 2.51 |
| **Kenya, measured** | 4.20 | 2.88 | 3.78 | 3.95 | 4.07 | 3.58 |
| **New Zealand, measured** | 3.84 | 2.61 | 3.61 | 3.22 | 3.48 | 2.58 |
| **Nigeria, measured** | 4.32 | 2.90 | 4.14 | 4.11 | 4.21 | 3.80 |
| **South Africa, measured** | 4.21 | 3.01 | 4.03 | 3.85 | 4.00 | 3.40 |

Care sits between 4.29 and 4.89 in every one of the fifty conditions. The lowest measured Care among the twenty anchored countries is Japan at 3.03.

## B7. Failed calls

Forty-six of 2,796 attempted calls returned no ratings object, from provider rate limits on the Together-hosted models and from replies that carried no parseable object. All forty-six were retried to success within the same collection window, so every one of the 2,750 scored cells is present and no condition rests on fewer than five iterations. The failures concentrate in three models - minimax 21, o3 16 and inkling 6 - with one each from deepseek_v4 and kimi_k3. This collection contains no refusal.

## B8. Presentation-order audit

Across all 2,750 scored runs: no two iterations of the same model in the same condition share an order, no two models share an order within the same condition and iteration, and no run used the canonical unshuffled order.

Orders **are** shared deliberately in one place. The four Arabic framed countries draw the same order for a given model and iteration, so the between-country contrast is paired on presentation order. All 55 model-iteration groups match this way. The English framed countries do not share orders, because that runner keys its draw on the country. The asymmetry costs the English four-country contrast some precision and introduces no bias, since order is randomized and ratings are keyed to item identity rather than position.

## B9. Reproducibility

`validity/build_lang_instruments.py` rebuilds the per-language instruments from the official translation files; item wording is not redistributed and the filled instruments are git-ignored. `validity/run_framed_lang.py`, `validity/run_framed.py` and `validity/run_validity.py` produced the cells; all are resumable, and every cell records its seed, presentation order, raw text and the framing instruction it was sent. `validity/fill.sh` re-invokes each runner until nothing remains, which is how the rate-limit gaps were closed.

`validity/audit_inlanguage.py` emits B4 and B5 as `results/appendix_b4_b5.md`, and reconciles first against an independent recomputation from the raw cells: the plain mean of the eighteen binding items against the average of three foundation means. Those agree only if each binding foundation carries the same number of items, so the gate verifies the counts it depends on. It writes `results/condition_means.json`, and `validity/audit_inlanguage_grid.py` reconciles against that file rather than against constants. `validity/build_appendix_tables.py` emits B3, B3a and B6 as `results/appendix_tables.md`. Both are spliced into this document verbatim, so a number here that disagrees with its artifact is a splice that was not re-run.

The July 2026 collection is preserved unchanged at `validity/archive-2026-07/`.

---

Analysis is stdlib-reproducible from the raw runs. Responsibility for the work, and for any errors in it, is mine alone. Methodology was AI-assisted and that assistance is disclosed.

Declan Michaels | Cross-Cultural Alignment Study | moral-os.com
