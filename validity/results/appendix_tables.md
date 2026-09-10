## B2a. Measurement invariance across the nineteen

Comparing raw composite means across countries needs the instrument to behave the same way in each. Atari et al. checked this with Muthen-Asparouhov alignment on their Study 2 data and report the result in their Table 6: a loadings R-squared and an intercepts R-squared per foundation, and the percentage of item parameters the alignment left non-invariant, against the 25 percent that Muthen and Asparouhov (2014) treat as acceptable. We recomputed the R-squared values on the same raw data in `reasoner-study` (`compute_alignment_r2.R`: sirt 3.13-228, `invariance.alignment`, align.scale c(.2, .4), align.pow c(.25, .25), lavaan) and show them beside the published ones; the percentages are Atari et al.'s, transcribed and not recomputed. Loadings R-squared concerns loading (metric) invariance, intercepts R-squared concerns intercept (scalar) invariance, the one that bears on comparing means. Neither establishes exact invariance. This is a property of the nineteen human samples. It says nothing about whether a model's score and a person's score measure the same thing, and nothing in this appendix claims they do.

| foundation | loadings R-squared, published / recomputed | intercepts R-squared, published / recomputed | non-invariant loadings | non-invariant intercepts |
|---|:--:|:--:|--:|--:|
| Care | 0.994 / 0.9945 | 0.999 / 0.9994 | 0.0% | 5.3% |
| Equality | 0.988 / 0.9873 | 0.995 / 0.9955 | 0.0% | 21.9% |
| Proportionality | 0.977 / 0.9760 | 0.999 / 0.9986 | 0.0% | 11.4% |
| Loyalty | 0.982 / 0.9816 | 0.998 / 0.9982 | 0.0% | 24.6% |
| Authority | 0.982 / 0.9846 | 0.996 / 0.9962 | 0.0% | 16.7% |
| Purity | 0.968 / 0.9646 | 0.989 / 0.9934 | 2.6% | 39.5% |

Every recomputed R-squared is within 0.0044 of the published one; the recomputation used Atari et al.'s shared data and the pinned sirt 3.13-228, and the residual is not traced. Purity is the one foundation over the 25 percent line, at 39.5 percent of intercept parameters, and Atari et al. write that caution should be practiced when comparing Purity group-level means; they trace most of it to unique intercepts in Argentina and Chile and to one item. Purity is one third of the binding composite and carries its largest framing shift, so every composite comparison in this appendix inherits that caution. B6 gives each foundation separately, and the report gives the Loyalty and Authority shifts on their own.

## B3. Where the panel lands, by country

Binding composite, panel mean over eleven models, each model's five iterations averaged first. The English unframed column is one condition and repeats down the table; the unframed in-language column is one condition per language and repeats across the countries that share a language, because neither condition names a country. Dashes mark arms not run. Morocco's local cells are the Spanish arm in both tables, decision 18; its Arabic-framed cells appear in B3a, B6 and B4.

| country | language | human | human SE | EN unframed | local unframed | EN framed | local framed |
|---|---|--:|--:|--:|--:|--:|--:|
| Egypt | Arabic | 4.267 | 0.040 | 2.769 | 3.104 | 4.605 | 4.604 |
| Saudi Arabia | Arabic | 4.083 | 0.045 | 2.769 | 3.104 | 4.733 | 4.757 |
| United Arab Emirates | Arabic | 3.892 | 0.057 | 2.769 | 3.104 | 4.629 | 4.726 |
| Argentina | Spanish | 3.283 | 0.046 | 2.769 | 2.780 | 3.437 | 3.349 |
| Chile | Spanish | 3.220 | 0.052 | 2.769 | 2.780 | 3.654 | 3.576 |
| Colombia | Spanish | 3.497 | 0.046 | 2.769 | 2.780 | 4.100 | 3.996 |
| Mexico | Spanish | 3.512 | 0.043 | 2.769 | 2.780 | 4.141 | 3.947 |
| Morocco [d18] | Spanish | 4.014 | 0.049 | 2.769 | 2.780 (Spanish arm) | 4.570 | 4.589 (Spanish arm) |
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
| Saudi Arabia | -1.315 | -0.979 | +0.650 | +0.673 |
| United Arab Emirates | -1.123 | -0.788 | +0.738 | +0.835 |
| Argentina | -0.515 | -0.504 | +0.154 | +0.066 |
| Chile | -0.451 | -0.440 | +0.433 | +0.356 |
| Colombia | -0.728 | -0.717 | +0.603 | +0.499 |
| Mexico | -0.743 | -0.732 | +0.629 | +0.435 |
| Morocco [d18] | -1.245 | -1.234 (Spanish arm) | +0.556 | +0.575 (Spanish arm) |
| Peru | -0.745 | -0.734 | +0.619 | +0.524 |
| Belgium | -0.675 | -0.667 | -0.822 | -0.647 |
| France | -0.841 | -0.833 | -0.885 | -0.775 |
| Switzerland | -0.580 | -0.572 | -0.286 | -0.273 |
| Japan | +0.117 | +0.024 | +1.016 | +0.782 |
| Iran [*] | -0.564 | -0.524 | +1.244 | +0.981 |
| Russia | -0.830 | -0.811 | +0.519 | +0.449 |
| Ireland | -0.327 | - | -0.002 | - |
| Kenya | -1.099 | - | +0.565 | - |
| New Zealand | -0.326 | - | -0.217 | - |
| Nigeria | -1.270 | - | +0.477 | - |
| South Africa | -0.980 | - | +0.187 | - |

Each of those nineteen means rests on 205 to 207 respondents for its country, 3,902 in all, collected by Atari et al. in May 2021 through Qualtrics Panels and stratified within each nation on age, gender and political orientation. Education was not a stratification variable, and Atari et al. state their results rest on "a subset of these populations who were educated enough to complete the surveys online", noting that people from traditional, small-scale communities are absent. Every overshoot in this appendix is a distance from those samples' means.

The human SE column is SD over root n from the per-country dispersion file, 0.039 to 0.059 across the nineteen: a standard error under an independent-respondent approximation. The stratified recruitment does not by itself justify a design-based population SE. It is a different quantity from the model-resampling interval in B3a, which describes panel composition, and neither one removes selection in who was sampled. Iran's comes from Hazrati et al.'s shared respondent-level files, sample 2, 989 respondents, over their own composite scores, binding SD 0.802.

[*] Iran's anchor is the only one not drawn from Atari et al. (2023) Study 2. B4 carries the source, the sample's own caveats and the sensitivity across every anchor that source offers.

[d18] Morocco: reported under Spanish, the language Atari et al. administered its sample in, and compared on the Spanish arm. We also ran an Arabic-framed arm; its cells are in B3a, B6 and B4 and enter no comparison against the human mean.

Human anchors, treated as constants, binding as the mean of loyalty, authority and purity: Egypt 4.267 (Atari 2023 Study 2), Saudi Arabia 4.083 (Atari 2023 Study 2), United Arab Emirates 3.892 (Atari 2023 Study 2), Argentina 3.283 (Atari 2023 Study 2), Chile 3.220 (Atari 2023 Study 2), Colombia 3.497 (Atari 2023 Study 2), Mexico 3.512 (Atari 2023 Study 2), Morocco 4.014 (Atari 2023 Study 2), Peru 3.514 (Atari 2023 Study 2), Belgium 3.444 (Atari 2023 Study 2), France 3.610 (Atari 2023 Study 2), Switzerland 3.349 (Atari 2023 Study 2), Japan 2.652 (Atari 2023 Study 2), Iran 3.333 (Hazrati 2025 sample 2), Russia 3.599 (Atari 2023 Study 2), Ireland 3.096 (Atari 2023 Study 2), Kenya 3.867 (Atari 2023 Study 2), New Zealand 3.094 (Atari 2023 Study 2), Nigeria 4.038 (Atari 2023 Study 2), South Africa 3.749 (Atari 2023 Study 2). India, Sweden and the United States are not in the MFQ-2 nineteen-nation set, so no overshoot is computable for them. Hazrati et al. administered Iran's sample on a 0-4 scale and we shift it linearly by +1 for comparability with the 1-5 runs; anchors_iran.json carries the detail and the caveats.

**Loyalty and Authority alone.** The English-framed comparison again, leaving out Purity, the foundation Atari et al. flag (B2a): the panel's mean of Loyalty and Authority against each reference sample's, the human figure the mean of the two published foundation means, Iran's from Hazrati et al. The last column divides the difference by that country's respondent-level standard deviation of the same two-foundation composite, computed over respondents the way the binding SD is (B9). Ordered by difference.

| country | human | human SD | panel, EN framed | difference | d |
|---|--:|--:|--:|--:|--:|
| France | 3.869 | 0.614 | 3.085 | -0.785 | -1.28 |
| Belgium | 3.663 | 0.635 | 2.962 | -0.701 | -1.10 |
| Switzerland | 3.547 | 0.781 | 3.417 | -0.130 | -0.17 |
| New Zealand | 3.350 | 0.884 | 3.248 | -0.102 | -0.12 |
| Ireland | 3.390 | 0.883 | 3.470 | +0.080 | +0.09 |
| Argentina | 3.627 | 0.699 | 3.870 | +0.243 | +0.35 |
| South Africa | 3.926 | 0.737 | 4.203 | +0.277 | +0.38 |
| Chile | 3.559 | 0.798 | 3.989 | +0.431 | +0.54 |
| Egypt | 4.303 | 0.609 | 4.762 | +0.459 | +0.75 |
| Nigeria | 4.160 | 0.621 | 4.676 | +0.516 | +0.83 |
| Mexico | 3.861 | 0.658 | 4.450 | +0.589 | +0.89 |
| Kenya | 4.008 | 0.797 | 4.636 | +0.628 | +0.79 |
| Peru | 3.772 | 0.689 | 4.409 | +0.638 | +0.93 |
| Colombia | 3.755 | 0.695 | 4.411 | +0.656 | +0.94 |
| Morocco [d18] | 4.054 | 0.754 | 4.730 | +0.676 | +0.90 |
| Russia | 3.775 | 0.747 | 4.503 | +0.728 | +0.97 |
| Saudi Arabia | 4.136 | 0.705 | 4.864 | +0.728 | +1.03 |
| United Arab Emirates | 3.967 | 0.862 | 4.827 | +0.860 | +1.00 |
| Japan | 2.664 | 0.687 | 4.017 | +1.353 | +1.97 |
| Iran [*] | 3.340 | 0.820 | 4.705 | +1.365 | +1.66 |

On Loyalty and Authority the panel sits above the reference sample in 16 countries and at or below it in 4; against the composite, the sign changes for Ireland and for no other country. Framed in the local language, the Spanish six rank with rho +0.77 against the reference order, +0.89 on the composite; the Arabic panel order is United Arab Emirates, Saudi Arabia, Egypt against a reference order of Egypt, Saudi Arabia, United Arab Emirates, and the French Switzerland, France, Belgium against France, Belgium, Switzerland.


## B3a. Every condition, with intervals

| condition | panel mean | 95% model-resampling interval | between-model SD |
|---|--:|:--:|--:|
| EN_framed_Argentina | 3.437 | [3.317, 3.556] | 0.20 |
| EN_framed_Belgium | 2.622 | [2.523, 2.741] | 0.19 |
| EN_framed_Chile | 3.654 | [3.533, 3.786] | 0.21 |
| EN_framed_Colombia | 4.100 | [3.982, 4.220] | 0.20 |
| EN_framed_Egypt | 4.605 | [4.502, 4.703] | 0.17 |
| EN_framed_France | 2.725 | [2.636, 2.837] | 0.17 |
| EN_framed_India | 4.439 | [4.336, 4.543] | 0.18 |
| EN_framed_Iran | 4.577 | [4.470, 4.671] | 0.17 |
| EN_framed_Ireland | 3.094 | [2.956, 3.253] | 0.25 |
| EN_framed_Japan | 3.668 | [3.478, 3.871] | 0.33 |
| EN_framed_Kenya | 4.432 | [4.365, 4.504] | 0.12 |
| EN_framed_Mexico | 4.141 | [4.071, 4.223] | 0.13 |
| EN_framed_Morocco | 4.570 | [4.482, 4.648] | 0.14 |
| EN_framed_New Zealand | 2.878 | [2.816, 2.943] | 0.11 |
| EN_framed_Nigeria | 4.515 | [4.425, 4.607] | 0.15 |
| EN_framed_Peru | 4.133 | [4.019, 4.243] | 0.19 |
| EN_framed_Russia | 4.117 | [3.983, 4.261] | 0.24 |
| EN_framed_Saudi Arabia | 4.733 | [4.653, 4.803] | 0.13 |
| EN_framed_South Africa | 3.935 | [3.841, 4.024] | 0.16 |
| EN_framed_Sweden | 2.282 | [2.194, 2.365] | 0.14 |
| EN_framed_Switzerland | 3.063 | [2.913, 3.220] | 0.26 |
| EN_framed_United Arab Emirates | 4.629 | [4.549, 4.704] | 0.13 |
| EN_framed_United States | 3.331 | [3.193, 3.456] | 0.22 |
| ar_framed_Egypt | 4.604 | [4.485, 4.717] | 0.20 |
| ar_framed_Morocco | 4.582 | [4.474, 4.682] | 0.18 |
| ar_framed_Saudi Arabia | 4.757 | [4.682, 4.822] | 0.12 |
| ar_framed_United Arab Emirates | 4.726 | [4.658, 4.791] | 0.11 |
| ar_neutral | 3.104 | [2.843, 3.374] | 0.45 |
| en_baseline_official_selfreport | 2.695 | [2.526, 2.861] | 0.28 |
| en_baseline_ours_nosystem | 2.760 | [2.547, 2.982] | 0.37 |
| en_baseline_ours_selfreport | 2.733 | [2.560, 2.923] | 0.31 |
| en_neutral | 2.769 | [2.608, 2.933] | 0.28 |
| en_neutral_ours | 2.713 | [2.540, 2.898] | 0.30 |
| es_framed_Argentina | 3.349 | [3.236, 3.475] | 0.20 |
| es_framed_Chile | 3.576 | [3.478, 3.678] | 0.17 |
| es_framed_Colombia | 3.996 | [3.908, 4.092] | 0.16 |
| es_framed_Mexico | 3.947 | [3.849, 4.044] | 0.17 |
| es_framed_Morocco | 4.589 | [4.497, 4.669] | 0.15 |
| es_framed_Peru | 4.038 | [3.920, 4.156] | 0.20 |
| es_neutral | 2.780 | [2.582, 2.967] | 0.33 |
| fa_framed_Iran | 4.314 | [4.147, 4.478] | 0.28 |
| fa_neutral | 2.809 | [2.565, 3.067] | 0.43 |
| fr_framed_Belgium | 2.797 | [2.713, 2.892] | 0.15 |
| fr_framed_France | 2.834 | [2.755, 2.921] | 0.14 |
| fr_framed_Switzerland | 3.076 | [2.971, 3.185] | 0.18 |
| fr_neutral | 2.777 | [2.591, 2.977] | 0.33 |
| ja_framed_Japan | 3.434 | [3.353, 3.514] | 0.14 |
| ja_neutral | 2.676 | [2.496, 2.884] | 0.33 |
| ru_framed_Russia | 4.047 | [3.907, 4.190] | 0.24 |
| ru_neutral | 2.788 | [2.585, 3.003] | 0.36 |

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
| **Saudi Arabia, measured** | 4.24 | 3.32 | 4.18 | 4.20 | 4.07 | 3.98 |
| **United Arab Emirates, measured** | 4.01 | 3.28 | 3.96 | 4.02 | 3.91 | 3.74 |
| **Argentina, measured** | 3.84 | 2.81 | 3.91 | 3.58 | 3.67 | 2.60 |
| **Chile, measured** | 3.77 | 2.77 | 3.70 | 3.45 | 3.67 | 2.54 |
| **Colombia, measured** | 3.83 | 2.91 | 3.69 | 3.67 | 3.84 | 2.98 |
| **Mexico, measured** | 3.77 | 2.87 | 3.80 | 3.78 | 3.94 | 2.81 |
| **Morocco, measured** [d18] | 4.21 | 3.36 | 4.18 | 4.16 | 3.95 | 3.93 |
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

Within a model, the five-run spread of the binding composite has a median of 0.185 in the unframed conditions and 0.114 in the framed ones, and 0.129 over all 550 model-by-condition cells; the between-model spread has a median of 0.188 over all 50 conditions. Taking run noise out condition by condition, under independence of a model's runs, by subtracting the mean within-model variance over five, scaled by (n-1)/n for a population variance over n model means, from the between-model variance of the five-run means: the estimated noise-adjusted between-model SD, truncated at zero, has a median of 0.313 in the unframed conditions and 0.159 in the framed ones, run noise is a median 11 and 13 percent of the between-model variance, and 37 of 39 framed conditions sit below every unframed one on the adjusted SD as well. Whatever default sampling temperature each provider applied, we assume the same default applied to a model's framed and unframed conditions, collected in one window.

Restricting the framed set by its distance from the top of the scale, against the same 7 unframed conditions, whose binding means run 2.68 to 3.10:

| framed conditions with binding mean below | conditions | tighter than every unframed | median spread |
|---|--:|--:|--:|
| 5.0 | 39 | 37 | 0.171 |
| 4.5 | 28 | 26 | 0.183 |
| 4.0 | 19 | 18 | 0.172 |
| 3.5 | 13 | 13 | 0.180 |

**The unframed language contrasts by foundation.** Each translated unframed condition minus the English unframed one, panel means, so the composite rows of B4 can be read in their parts. The last column is the mean over models of the absolute within-model change in the binding composite, the movement a panel-level shift near zero can hide.

| language | Care | Equality | Proportionality | Loyalty | Authority | Purity | binding | mean abs. within-model binding change |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Arabic | +0.02 | +0.33 | +0.06 | +0.23 | +0.20 | +0.58 | +0.34 | 0.34 |
| Spanish | -0.14 | +0.01 | -0.11 | -0.12 | +0.06 | +0.09 | +0.01 | 0.16 |
| French | -0.28 | +0.24 | -0.21 | -0.12 | -0.12 | +0.26 | +0.01 | 0.08 |
| Japanese | -0.10 | +0.12 | -0.18 | -0.26 | -0.08 | +0.06 | -0.09 | 0.26 |
| Farsi | -0.04 | +0.22 | -0.01 | -0.10 | -0.07 | +0.29 | +0.04 | 0.22 |
| Russian | +0.00 | +0.11 | +0.03 | -0.03 | +0.01 | +0.08 | +0.02 | 0.11 |

**A self-report system prompt without a country.** The four English unframed variants, none of which names a country, separate the presence of a self-report system prompt from its absence, across the two questionnaire files. Between-model SD is 0.28 with no system prompt and 0.28 with the self-report prompt on the official file, 0.37 and 0.31 on our transcription, against a median of 0.171 across the 39 framed conditions. The self-report prompt moves the spread by at most 0.06, while the framing conditions sit 0.16 below the unframed median; the country-free framing template in B4a moves it by about 0.17 in the September check, so the content of a country-free instruction, not the presence of one, is what separates the two.

A floor would work the other way. Unframed English Purity sits at 1.97 on a scale that starts at 1 and Purity has the largest unframed between-model spread of any foundation, a median of 0.449, so a floor compressing it would shrink the unframed spread, which is the larger one, not the framed.

**Framing by language, on the binding composite and on Loyalty and Authority alone.** In-language framed minus in-language unframed, panel means, averaged over the language's countries with Morocco under Spanish (decision 18); the last row averages the six languages with equal weight. The Loyalty-Authority column leaves out Purity, the foundation whose intercepts Atari et al. flag (B2a).

| language | countries | binding | Loyalty-Authority |
|---|--:|--:|--:|
| Arabic | 3 | +1.592 | +1.448 |
| Spanish | 6 | +1.136 | +1.072 |
| French | 3 | +0.126 | +0.142 |
| Japanese | 1 | +0.759 | +0.682 |
| Farsi | 1 | +1.505 | +1.312 |
| Russian | 1 | +1.260 | +1.235 |
| six languages, equal weight | 15 | +1.063 | +0.982 |

**The Arabic unframed shift, item by item.** Arabic unframed minus English unframed, panel mean per item, with the number of the eleven models whose own mean moved up. Item names give foundation and position in the official key; we do not reproduce wording (decision 7).

| item | shift | models up (of 11) |
|---|--:|--:|
| care_1 | +0.04 | 3 |
| care_2 | +0.02 | 3 |
| care_3 | +0.04 | 3 |
| care_4 | +0.02 | 3 |
| care_5 | +0.02 | 3 |
| care_6 | -0.02 | 4 |
| equality_1 | +0.45 | 9 |
| equality_2 | +0.47 | 8 |
| equality_3 | +0.42 | 9 |
| equality_4 | +0.22 | 6 |
| equality_5 | +0.18 | 8 |
| equality_6 | +0.24 | 7 |
| proportionality_1 | +0.20 | 7 |
| proportionality_2 | +0.05 | 5 |
| proportionality_3 | +0.00 | 3 |
| proportionality_4 | -0.11 | 3 |
| proportionality_5 | +0.09 | 4 |
| proportionality_6 | +0.13 | 6 |
| loyalty_1 | +0.36 | 8 |
| loyalty_2 | +0.07 | 6 |
| loyalty_3 | +0.40 | 9 |
| loyalty_4 | +0.18 | 4 |
| loyalty_5 | +0.22 | 8 |
| loyalty_6 | +0.13 | 6 |
| authority_1 | +0.13 | 5 |
| authority_2 | +0.11 | 4 |
| authority_3 | +0.40 | 9 |
| authority_4 | +0.11 | 4 |
| authority_5 | +0.27 | 7 |
| authority_6 | +0.18 | 6 |
| purity_1 | +0.40 | 7 |
| purity_2 | +0.82 | 10 |
| purity_3 | +0.67 | 11 |
| purity_4 | +0.38 | 9 |
| purity_5 | +0.71 | 10 |
| purity_6 | +0.49 | 9 |

13 of 36 items move by more than 0.25 and 3 by more than 0.5 (purity_2, purity_3, purity_5); 18 of the 18 binding items move up, and so do all six Equality items, by +0.18 to +0.47; the six Care items sit within 0.04 of their English values.

