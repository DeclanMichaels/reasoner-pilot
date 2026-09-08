## B2a. Measurement invariance across the nineteen

Comparing raw composite means across countries needs the instrument to behave the same way in each. Atari et al. checked this with Muthen-Asparouhov alignment on their Study 2 data; the check was recomputed on the same raw data in `reasoner-study` (`compute_alignment_r2.R`: sirt 3.13-228, `invariance.alignment`, align.scale c(.2, .4), align.pow c(.25, .25), lavaan). The two figures are alignment diagnostics: loadings R-squared concerns loading (metric) invariance, intercepts R-squared concerns intercept (scalar) invariance, the one that bears on comparing means. Neither establishes exact invariance. Both are shown. This is a property of the nineteen human samples. It says nothing about whether a model's score and a person's score measure the same thing, and nothing in this appendix claims they do.

| foundation | loadings R-squared | intercepts R-squared |
|---|--:|--:|
| Care | 0.9945 | 0.9994 |
| Equality | 0.9873 | 0.9955 |
| Proportionality | 0.9760 | 0.9986 |
| Loyalty | 0.9816 | 0.9982 |
| Authority | 0.9846 | 0.9962 |
| Purity | 0.9646 | 0.9934 |

Purity is the weakest on intercepts at 0.9934. The item-level noninvariance behind each figure is not carried here; the script emits these six pairs only.

## B3. Where the panel lands, by country

Binding composite, panel mean over eleven models, each model's five iterations averaged first. The English unframed column is one condition and repeats down the table; the unframed in-language column is one condition per language and repeats across the countries that share a language, because neither condition names a country. Dashes mark arms not run. Morocco's local cells show the Arabic arm here and the Spanish arm in the distance table, per decision 12.

| country | language | human | human SE | EN unframed | local unframed | EN framed | local framed |
|---|---|--:|--:|--:|--:|--:|--:|
| Egypt | Arabic | 4.267 | 0.040 | 2.769 | 3.104 | 4.605 | 4.604 |
| Morocco [d12] | Arabic | 4.014 | 0.049 | 2.769 | 3.104 (Arabic arm) | 4.570 | 4.582 (Arabic arm) |
| Saudi Arabia | Arabic | 4.083 | 0.045 | 2.769 | 3.104 | 4.733 | 4.757 |
| United Arab Emirates | Arabic | 3.892 | 0.057 | 2.769 | 3.104 | 4.629 | 4.726 |
| Argentina | Spanish | 3.283 | 0.046 | 2.769 | 2.780 | 3.437 | 3.349 |
| Chile | Spanish | 3.220 | 0.052 | 2.769 | 2.780 | 3.654 | 3.576 |
| Colombia | Spanish | 3.497 | 0.046 | 2.769 | 2.780 | 4.100 | 3.996 |
| Mexico | Spanish | 3.512 | 0.043 | 2.769 | 2.780 | 4.141 | 3.947 |
| Peru | Spanish | 3.514 | 0.045 | 2.769 | 2.780 | 4.133 | 4.038 |
| Belgium | French | 3.444 | 0.040 | 2.769 | 2.777 | 2.622 | 2.797 |
| France | French | 3.610 | 0.039 | 2.769 | 2.777 | 2.725 | 2.834 |
| Switzerland | French | 3.349 | 0.050 | 2.769 | 2.777 | 3.063 | 3.076 |
| Japan | Japanese | 2.652 | 0.044 | 2.769 | 2.676 | 3.668 | 3.434 |
| Iran [*] | Farsi | 3.333 | 0.025 | 2.769 | 2.809 | 4.577 | 4.314 |
| Russia | Russian | 3.599 | 0.049 | 2.769 | 2.788 | 4.117 | 4.047 |
| India | n/a | n/a | n/a | 2.769 | - | 4.439 | - |
| Ireland | n/a | 3.096 | 0.057 | 2.769 | - | 3.094 | - |
| Kenya | n/a | 3.867 | 0.052 | 2.769 | - | 4.432 | - |
| New Zealand | n/a | 3.094 | 0.059 | 2.769 | - | 2.878 | - |
| Nigeria | n/a | 4.038 | 0.043 | 2.769 | - | 4.515 | - |
| South Africa | n/a | 3.749 | 0.051 | 2.769 | - | 3.935 | - |
| Sweden | n/a | n/a | n/a | 2.769 | - | 2.282 | - |
| United States | n/a | n/a | n/a | 2.769 | - | 3.331 | - |

The same table as distance from that country's reference-sample mean. Positive is above it.

| country | EN unframed | local unframed | EN framed | local framed |
|---|--:|--:|--:|--:|
| Egypt | -1.498 | -1.163 | +0.338 | +0.337 |
| Morocco [d12] | -1.245 | -1.234 (Spanish arm) | +0.556 | +0.575 (Spanish arm) |
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

The human SE column is SD over root n from the per-country dispersion file, 0.039 to 0.059 across the nineteen: a standard error under an independent-respondent approximation. The stratified recruitment does not by itself justify a design-based population SE. It is a different quantity from the model-resampling interval in B3a, which describes panel composition, and neither one removes selection in who was sampled. Iran's comes from the authors' shared respondent-level files, sample 2, 989 respondents, over their own composite scores, binding SD 0.802.

[*] Iran's anchor is the only one not drawn from Atari et al. (2023) Study 2. B4 carries the source, the sample's own caveats and the sensitivity across every anchor that source offers.

[d12] Morocco: grouped with Arabic above, compared against its human mean on the Spanish arm, because Atari et al. administered Morocco's sample in Spanish. Both runs are carried in the data.

Human anchors, treated as constants, binding as the mean of loyalty, authority and purity: Egypt 4.267 (Atari 2023 Study 2), Morocco 4.014 (Atari 2023 Study 2), Saudi Arabia 4.083 (Atari 2023 Study 2), United Arab Emirates 3.892 (Atari 2023 Study 2), Argentina 3.283 (Atari 2023 Study 2), Chile 3.220 (Atari 2023 Study 2), Colombia 3.497 (Atari 2023 Study 2), Mexico 3.512 (Atari 2023 Study 2), Peru 3.514 (Atari 2023 Study 2), Belgium 3.444 (Atari 2023 Study 2), France 3.610 (Atari 2023 Study 2), Switzerland 3.349 (Atari 2023 Study 2), Japan 2.652 (Atari 2023 Study 2), Iran 3.333 (Hazrati 2025 sample 2), Russia 3.599 (Atari 2023 Study 2), Ireland 3.096 (Atari 2023 Study 2), Kenya 3.867 (Atari 2023 Study 2), New Zealand 3.094 (Atari 2023 Study 2), Nigeria 4.038 (Atari 2023 Study 2), South Africa 3.749 (Atari 2023 Study 2). India, Sweden and the United States are not in the MFQ-2 nineteen-nation set, so no overshoot is computable for them. Iran's sample was administered on a 0-4 scale and shifted linearly by +1 for comparability with the 1-5 runs; anchors_iran.json carries the detail and the caveats.


## B3a. Every condition, with intervals

| condition | panel mean | 95% model-resampling interval | between-model SD |
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

## B6. Per-foundation panel means

All fifty conditions, then the measured human mean for each of the twenty anchored countries, in the country order of B3. The measured rows are reference samples, not conditions; they are here to be read against the panel rows above.

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

## B6a. The dispersion finding, by foundation and against the ceiling

The between-model spread in B3a is on the binding composite. This section takes it apart. Spread is the population standard deviation of the 11 model means, the median over the 7 unframed conditions against the median over the 39 framed ones, per foundation; the last column counts framed conditions whose spread is below every unframed condition's.

| foundation | unframed | framed | framed / unframed | framed tighter than every unframed |
|---|--:|--:|--:|--:|
| Care | 0.370 | 0.272 | 0.73 | 27 of 39 |
| Equality | 0.391 | 0.271 | 0.69 | 34 of 39 |
| Proportionality | 0.349 | 0.216 | 0.62 | 38 of 39 |
| Loyalty | 0.396 | 0.223 | 0.56 | 37 of 39 |
| Authority | 0.319 | 0.171 | 0.53 | 34 of 39 |
| Purity | 0.449 | 0.203 | 0.45 | 32 of 39 |

Endpoint use, the share of item ratings at 1 or 5, panel mean and then the median over conditions: 0.234 unframed, 0.267 framed. Item-level between-model spread, the same statistic on each of the 36 items and then the median: 0.425 unframed, 0.299 framed.

Within a model, the five-run spread of the binding composite has a median of 0.185 in the unframed conditions and 0.114 in the framed ones. A between-model spread of five-run means carries run noise of roughly that over root five, 0.083 and 0.051, so run noise contributes less to the framed between-model spread, not more. Sampling temperature is fixed per model across conditions and cannot produce a difference between them.

Restricting the framed set by its distance from the top of the scale, against the same 7 unframed conditions, whose binding means run 2.68 to 3.10:

| framed conditions with binding mean below | conditions | tighter than every unframed | median spread |
|---|--:|--:|--:|
| 5.0 | 39 | 37 | 0.171 |
| 4.5 | 28 | 26 | 0.183 |
| 4.0 | 19 | 18 | 0.172 |
| 3.5 | 13 | 13 | 0.180 |

**The unframed language contrasts by foundation.** Each translated unframed condition minus the English unframed one, panel means, so the composite rows of B4 can be read in their parts.

| language | Care | Equality | Proportionality | Loyalty | Authority | Purity | binding |
|---|--:|--:|--:|--:|--:|--:|--:|
| Arabic | +0.02 | +0.33 | +0.06 | +0.23 | +0.20 | +0.58 | +0.34 |
| Spanish | -0.14 | +0.01 | -0.11 | -0.12 | +0.06 | +0.09 | +0.01 |
| French | -0.28 | +0.24 | -0.21 | -0.12 | -0.12 | +0.26 | +0.01 |
| Japanese | -0.10 | +0.12 | -0.18 | -0.26 | -0.08 | +0.06 | -0.09 |
| Farsi | -0.04 | +0.22 | -0.01 | -0.10 | -0.07 | +0.29 | +0.04 |
| Russian | +0.00 | +0.11 | +0.03 | -0.03 | +0.01 | +0.08 | +0.02 |
