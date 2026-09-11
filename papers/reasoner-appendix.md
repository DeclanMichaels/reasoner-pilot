# Statistical Appendix

Companion to "Frontier Language Models Converge in a Narrow Region of a Moral-Reasoning Space." Every number here regenerates from the raw runs with one stdlib script, `analysis/build_appendix.py` (random seed 20260720; the A5 model-resampling draws use their own seed, 20260910), except the rerun-averaging figures in A3, which `validity/aggregation_artifact.py` computes from this appendix's output. Tables first; the report carries the prose.

## A1. Sample and data

Eleven models from nine labs (three Chinese: DeepSeek, MiniMax, Moonshot), called by the identifiers below on 2026-07-18 and 2026-07-19. Two further models completed the unframed cell but not the framing grid, Cohere Command A (three of eight framings) and Google Gemini 3 Pro (one), and are outside the panel; they appear in A8 only.

| key | provider | model identifier |
|---|---|---|
| opus | Anthropic | `claude-opus-4-8` |
| sonnet | Anthropic | `claude-sonnet-5` |
| gpt55 | OpenAI | `gpt-5.5` |
| o3 | OpenAI | `o3` |
| grok45 | xAI | `grok-4.5` |
| mistral_large | Mistral | `mistral-large-2512` |
| deepseek_v4 | DeepSeek, via Together | `deepseek-ai/DeepSeek-V4-Pro` |
| minimax | MiniMax, via Together | `MiniMaxAI/MiniMax-M3` |
| kimi | Moonshot, via Together | `moonshotai/Kimi-K2.6` |
| inkling | Thinking Machines, via Together | `thinkingmachines/Inkling` |
| llama33 | Meta, via Together | `meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| command_a (outside panel) | Cohere | `command-a-plus-05-2026` |
| gemini3pro (outside panel) | Google | `gemini-3.1-pro-preview` |

**Request.** One user message carrying the scenario, both questions and their options in bank order, and the allocation instruction; the framing, where there is one, as the system prompt. The options are in the same order on every call. A request seed of 1000 plus the rerun index goes to OpenAI, xAI, Together (`seed`) and Mistral (`random_seed`); Anthropic, Google and Cohere accept none. Token ceilings are per provider: Anthropic 3072, OpenAI and xAI 4096, Together and Google 6144, Mistral and Cohere 2048. No sampling parameter of any kind is sent, no temperature, top-p, top-k or reasoning setting, so each model ran at its provider's defaults, which the run records do not capture.

**Scenarios.** Forty-eight, twelve per axis, each with a judgment question and a reasoning question; 93 of the 96 questions have three options and 3 have four. Twelve scenarios, three per axis, carry the human baseline (b12). Eight framings per scenario. Each (model, framing) cell is one file of 240 responses (48 scenarios times 5 reruns). No cell was run more than once. The build scripts read `runs/` non-recursively and raise if a duplicate complete cell appears; a superseded run would be moved to `runs/_superseded/`, which they do not read.

**Exclusions.** A response whose point allocations could not be parsed from the model's reply is marked `extraction_failed` and excluded from every score; the runner's uniform fallback allocation is never scored. A file of 240 responses is therefore not a cell of 240 scored answers. Across the panel 205 of 21,120 responses are excluded, concentrated in Kimi (99) and MiniMax (53); the largest single loss is Kimi's geometry cell, 31 of 60. Command A's 176 of 720 include 101 failed calls.

Columns are the eight framings in the order above (neutral, individualist, collectivist, hierarchical, egalitarian, seasonal, geometry, color), then the total excluded over the responses in the file.

| model | neu. | ind. | col. | hie. | ega. | sea. | geo. | clr. | excluded / responses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek_v4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 1920 |
| gpt55 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 1920 |
| grok45 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 | 4 / 1920 |
| inkling | 5 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 7 / 1920 |
| kimi | 3 | 14 | 9 | 10 | 13 | 6 | 31 | 13 | 99 / 1920 |
| llama33 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 / 1920 |
| minimax | 5 | 6 | 5 | 3 | 8 | 13 | 9 | 4 | 53 / 1920 |
| mistral_large | 4 | 0 | 16 | 4 | 0 | 0 | 0 | 0 | 24 / 1920 |
| o3 | 2 | 2 | 1 | 1 | 1 | 4 | 5 | 1 | 17 / 1920 |
| opus | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 1920 |
| sonnet | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 1920 |
| command_a (outside panel) | 38 | 79 | 59 | - | - | - | - | - | 176 / 720 |
| gemini3pro (outside panel) | 0 | - | - | - | - | - | - | - | 0 / 240 |

**Human respondents.** Sixty-eight, a convenience sample recruited within one to two degrees of the author, demographically varied but concentrated in educational and professional background (almost all technology consultants and professionals), scored with the identical function. Their item exposure is not the models': 58 respondents, on instrument version 1.1, answered four scenarios, one per axis drawn by rotation from that axis's three baseline scenarios; ten respondents, on version 1.0, answered all twelve. Most human axis scores are therefore single-item observations, and each baseline item has between 19 and 35 human responses. Consent and licence terms are in `DATA-LICENSE.md` and decision 6.

## A2. The scoring function

Every axis score, for humans and models alike, comes from one function (`compute_dimensional_score` in `scenario_bank.py`). Each scenario belongs to exactly one axis and poses two questions, judgment (what should happen) and reasoning (why it matters), each with three or four answer options. Every option carries a fixed signed loading toward its axis, a value in the interval from -1 to +1: an option that fully marks one pole loads at +1 or -1, an option that leans partway loads at a fraction (the bank uses +0.3, -0.3, +0.5, -0.5 and +0.7), and a neutral option loads at 0.

A respondent distributes a fixed pool of points across the options for each question. The judgment score is the loading-weighted average of the points they placed:

j = sum over judgment options of (loading times points), divided by the sum of points placed

The reasoning score r is the same over the reasoning options. Because points are non-negative and the loadings lie in the interval from -1 to +1, both j and r fall in that same interval: all points on full +1 options gives +1, all on full -1 options gives -1, points on neutral options pull toward 0. An even split across a question's options scores the mean of its loadings, which is zero only where the loadings are balanced; in 24 of the 48 scenarios an even split across both questions scores away from zero (between -0.15 and +0.17), or one question has no option at a full pole (mac_1's reasoning options load -1, 0 and -0.5, so its attainable maximum is +0.6). The same options are scored for humans and models, so this affects the meaning of a zero and the headroom under framing, not the comparison between the two populations. The axis score combines the two,

score = 0.6 times j, plus 0.4 times r,

weighting the judgment question above the reasoning question. A position on an axis pools every scored response on that axis's scenarios, each response's allocation normalised to sum to one, so each scored response carries equal weight; a model's position is not a mean of five rerun-level scores, although with no exclusions the two coincide. The blank-question rule applies at that pooled level: if no points were placed on one question across the pooled responses, the other is used at full weight rather than deflating the score toward zero. The 0.6 to 0.4 split is the single free parameter in the scoring; A8 shows the compression holds under judgment-only, reasoning-only, and the combined weighting, so the finding does not depend on it.

## A3. Compression

Dispersion is population standard deviation; the model figures are each model's unframed neutral position (A5 shows the panel widening two to five times under framing). The N-matched draw takes 11 of the 68 human scores on the axis at random without replacement, 100,000 times, and counts how often that subsample is at least as tight as the 11-model panel. It describes the observed human sample; it is not a test of equal dispersion between two populations. The ratio CI is a 5,000-draw percentile bootstrap resampling humans and models independently.

| Axis | Human SD | Model SD (neutral) | Ratio (human/model) | 95% CI on ratio | draws as tight as the panel |
|---|---:|---:|---:|:---:|---:|
| Moral Agent | 0.412 | 0.061 | 6.78x | [4.95, 13.2] | 0 of 100,000 |
| Authority | 0.401 | 0.052 | 7.69x | [5.83, 12.53] | 0 of 100,000 |
| Moral Domain | 0.327 | 0.061 | 5.37x | [3.66, 11.65] | 0 of 100,000 |
| Obligation Scope | 0.361 | 0.064 | 5.65x | [4.57, 8.41] | 0 of 100,000 |

Zero of 100,000 draws bounds the tail at about three in 100,000 (one-sided 95 percent), not at one in 100,000. The lower bound of every ratio CI is at least 3.66. The human sample is a convenience sample concentrated among technology professionals (A1).

**Item exposure.** The human SD above is mostly the spread of single-item scores across people (A1); the model SD is the spread of positions each pooling three items and up to five reruns. The two exposures can be matched two ways.

On the ten respondents who answered all twelve scenarios:

| Axis | Human SD (n = 10) | Model SD | Ratio |
|---|---:|---:|---:|
| Moral Agent | 0.348 | 0.061 | 5.72x |
| Authority | 0.192 | 0.052 | 3.69x |
| Moral Domain | 0.406 | 0.061 | 6.67x |
| Obligation Scope | 0.309 | 0.064 | 4.84x |

Item by item, the humans who answered that item against the eleven models' positions on it, reruns still pooled on the model side:

| item | axis | humans | human SD | model SD | ratio |
|---|---|---:|---:|---:|---:|
| mac_1 | Moral Agent | 33 | 0.404 | 0.111 | 3.64x |
| mac_2 | Moral Agent | 27 | 0.338 | 0.048 | 7.11x |
| mac_3 | Moral Agent | 28 | 0.457 | 0.114 | 4.02x |
| auth_1 | Authority | 34 | 0.319 | 0.067 | 4.78x |
| auth_2 | Authority | 35 | 0.464 | 0.070 | 6.60x |
| auth_3 | Authority | 19 | 0.340 | 0.057 | 5.97x |
| domain_1 | Moral Domain | 34 | 0.382 | 0.090 | 4.24x |
| domain_2 | Moral Domain | 21 | 0.351 | 0.042 | 8.40x |
| domain_3 | Moral Domain | 33 | 0.386 | 0.117 | 3.30x |
| scope_1 | Obligation Scope | 34 | 0.277 | 0.048 | 5.78x |
| scope_2 | Obligation Scope | 29 | 0.433 | 0.126 | 3.43x |
| scope_3 | Obligation Scope | 25 | 0.352 | 0.107 | 3.29x |

The model SD is the smaller on every item, by 3.3 to 8.4 times. The ten-respondent subset is small and on a different instrument version; the item rows still pool model reruns.

**Rerun averaging.** Each model position pools up to five reruns where each human score is one response. `validity/aggregation_artifact.py` treats each model as one draw instead: the four ratios become 6.32, 7.25, 5.03 and 5.14, a reduction of 6 to 9 percent, and for any ratio to reach 3, within-person noise would have to be 64 to 83 percent of the observed human variance. With those single-draw model SDs the N-matched count is still 0 of 100,000 on every axis.

Where the two populations sit, for context (the compression claim is about spread, not location):

| Axis | Human mean | Human median | Model mean |
|---|---:|---:|---:|
| Moral Agent | +0.29 | +0.36 | -0.05 |
| Authority | +0.17 | +0.20 | +0.12 |
| Moral Domain | +0.37 | +0.43 | +0.29 |
| Obligation Scope | +0.37 | +0.42 | +0.28 |

On Moral Agent the model mean and the human center sit on opposite sides of the midpoint.

## A4. Run reliability (test-retest)

Within-model dispersion is the standard deviation of a cell's axis score across its five reruns, reported as the median over the eleven models. Between-model dispersion is the panel SD from A3. The spread between models is 1.9 to 2.5 times the spread a single model shows on rerun. This within-model dispersion is what the interactive viewer draws as its optional run-spread overlay. No sampling temperature was sent; each model ran at its provider's default, which the run records do not capture, so the within-model figures are not on a common footing across models.

| Axis | Within-model run SD (median) | Between-model SD | Between / within |
|---|---:|---:|---:|
| Moral Agent | 0.026 | 0.061 | 2.33 |
| Authority | 0.021 | 0.052 | 2.50 |
| Moral Domain | 0.025 | 0.061 | 2.41 |
| Obligation Scope | 0.033 | 0.064 | 1.95 |

## A5. Frame responsiveness

Displacement is the mean absolute per-axis change from a model's own neutral position, averaged over the four axes; the group figures average that across models and framings. The intervals are 20,000-draw percentile bootstraps that resample the eleven models, each model carrying all its framings, so a model's framed displacements, which share its unframed baseline, stay together; the difference and the ratio are computed on the same resampled models. They describe how far the panel figure moves when the observed eleven are reweighted, conditional on these framings, and are not confidence intervals for models in general.

| Quantity | Estimate | 95% model-resampling interval |
|---|---:|:---:|
| Cultural (4 framings) | 0.363 | [0.302, 0.429] |
| Nonsense (geometry, color) | 0.203 | [0.150, 0.259] |
| Seasonal, non-moral (not a clean null) | 0.246 | [0.197, 0.298] |
| Cultural minus nonsense | 0.160 | [0.129, 0.199] |
| Nonsense over cultural | 0.558 | [0.464, 0.641] |

Per framing:

| Framing | Mean displacement |
|---|---:|
| individualist | 0.335 |
| collectivist | 0.442 |
| hierarchical | 0.543 |
| egalitarian | 0.132 |
| irrelevant (seasonal) | 0.246 |
| nonsense: geometry | 0.195 |
| nonsense: color | 0.211 |

The seasonal framing (labeled irrelevant in the data) was designed as a non-moral noise floor. Its displacement (0.246) is nearer the nonsense framings than zero, and its interval overlaps theirs and not the cultural framings'; it is reported as a non-moral framing, not a control.

The cultural result rests on direction, not distance. Each cultural framing names a principle that maps to one axis, so the four framings target two of the four axes. For each, the signed shift on its target axis in the expected direction, and the count of models that moved that way:

| Framing | Target axis | Mean signed shift (expected direction) | Models in expected direction |
|---|---|---:|:---:|
| individualist | Moral Agent (toward autonomous) | +0.46 | 11 / 11 |
| collectivist | Moral Agent (toward relational) | +0.56 | 11 / 11 |
| egalitarian | Authority (toward skeptical) | +0.16 | 11 / 11 |
| hierarchical | Authority (toward deferential) | +0.62 | 11 / 11 |

Under both nonsense framings all eleven models move the same way on Moral Agent (toward relational: geometry mean -0.25, color mean -0.24, 0 of 11 moving the other way). The nonsense prompts share the cultural prompts' scaffold, a society with social roles and moral obligations, so the shared shift is not attributable to geometry or color as against that scaffold; the pilot has no scaffold-only framing.

Per model, displacement under the two nonsense framings as a share of displacement under the four cultural framings:

| Model | Nonsense / cultural |
|---|---:|
| sonnet | 0.27 |
| kimi | 0.39 |
| opus | 0.46 |
| llama33 | 0.47 |
| o3 | 0.53 |
| minimax | 0.53 |
| mistral_large | 0.54 |
| inkling | 0.62 |
| deepseek_v4 | 0.72 |
| gpt55 | 0.72 |
| grok45 | 0.73 |

Kimi's geometry cell is scored on 29 of 60 responses (A1).

Between-model dispersion. The compression in A3 is measured at neutral. Under framing the panel does not stay equally tight: the standard deviation across the eleven models, averaged over the four axes, rises two to five times above its neutral value under every framing, cultural or nonsense alike.

| Framing | Between-model SD (b12) | vs neutral | Between-model SD (all 48) | vs neutral |
|---|---:|:---:|---:|:---:|
| neutral | 0.059 | 1.0x | 0.033 | 1.0x |
| individualist | 0.125 | 2.1x | 0.129 | 3.9x |
| collectivist | 0.148 | 2.5x | 0.132 | 4.0x |
| hierarchical | 0.160 | 2.7x | 0.154 | 4.7x |
| egalitarian | 0.130 | 2.2x | 0.074 | 2.2x |
| irrelevant (seasonal) | 0.129 | 2.2x | 0.093 | 2.8x |
| nonsense: geometry | 0.145 | 2.4x | 0.097 | 2.9x |
| nonsense: color | 0.142 | 2.4x | 0.109 | 3.3x |

The nonsense and seasonal framings widen the panel about as much as the cultural ones. What differs under the cultural framings is the shared direction of the signed shifts above, not the spread.

## A6. Cross-lab clustering

Each model is fingerprinted by its deviation from the panel consensus, and its nearest neighbor is the model with the highest Pearson correlation of deviations, a pattern-similarity measure rather than a distance. We report two grains. Seven of the eleven models are their lab's only model, so their nearest neighbor is cross-lab by construction; only the two Anthropic and the two OpenAI models have a same-lab candidate, and under label exchange the expected number of same-lab nearest-neighbor links is 0.4. The counts below are the observed pattern, not evidence that lab has no association with position.

Panel grain (deviation of the four axis positions, all 48 scenarios): no model's nearest neighbor is a same-lab sibling (0 of 11). A correlation over four values has two degrees of freedom; the values run high and carry little.

| Model | Nearest neighbor | r | Same lab |
|---|---|---:|:---:|
| deepseek_v4 | opus | 0.882 | no |
| gpt55 | mistral_large | 0.995 | no |
| grok45 | minimax | 0.971 | no |
| inkling | llama33 | 0.889 | no |
| kimi | gpt55 | 0.717 | no |
| llama33 | inkling | 0.889 | no |
| minimax | sonnet | 0.984 | no |
| mistral_large | gpt55 | 0.995 | no |
| o3 | llama33 | 0.739 | no |
| opus | deepseek_v4 | 0.882 | no |
| sonnet | minimax | 0.984 | no |

Fine grain (deviation of the 48 per-scenario positions): ten of eleven nearest neighbors are cross-lab. The single exception is Opus, whose nearest neighbor is Sonnet at r = 0.137, narrowly ahead of two OpenAI models (gpt55 at 0.115, o3 at 0.104). Sonnet itself is not the mirror of that tie: its own nearest neighbor is MiniMax at r = 0.500, a much stronger and cross-lab pairing. The same-lab pairing appears at the scenario grain only.

| Model | Nearest neighbor | r | Same lab |
|---|---|---:|:---:|
| deepseek_v4 | o3 | 0.223 | no |
| gpt55 | inkling | 0.144 | no |
| grok45 | sonnet | 0.394 | no |
| inkling | gpt55 | 0.144 | no |
| kimi | gpt55 | 0.112 | no |
| llama33 | o3 | 0.415 | no |
| minimax | sonnet | 0.500 | no |
| mistral_large | o3 | 0.233 | no |
| o3 | llama33 | 0.415 | no |
| opus | sonnet | 0.137 | yes |
| sonnet | minimax | 0.500 | no |

The tightest cross-lab pairs are MiniMax and Sonnet at 0.50, which crosses country as well as company, and o3 and Llama at 0.415, two American labs.

## A7. Reasoning token spend

Reasoning tokens are whatever the provider's usage object reports for the call; no reasoning or thinking setting was sent (A1). OpenAI, xAI and Together return a `reasoning_tokens` count, Google a thoughts count. The Anthropic, Cohere and Mistral adapters record no such field, and Together returns none for Llama, so four panel models have no reported count. That is a property of the request and the provider's accounting, not a count of zero, and it says nothing about whether those models reasoned. Providers also differ on whether reasoning tokens sit inside the output count, so no share of output is given. Mean reported reasoning tokens per unframed scenario, with each model's Euclidean distance from the panel centroid across the four axes (all 48 scenarios):

| Model | Reasoning tokens / scenario | Responses with a count | Distance from panel center |
|---|---:|---:|---:|
| kimi | 3628 | 240 | 0.031 |
| minimax | 1189 | 240 | 0.058 |
| inkling | 1141 | 235 | 0.085 |
| deepseek_v4 | 1066 | 240 | 0.058 |
| grok45 | 494 | 240 | 0.093 |
| o3 | 247 | 240 | 0.055 |
| gpt55 | 131 | 240 | 0.060 |
| llama33 | not reported | 0 | 0.061 |
| mistral_large | not reported | 0 | 0.109 |
| opus | not reported | 0 | 0.042 |
| sonnet | not reported | 0 | 0.079 |

Among the seven models with a count, spend runs from 131 to 3,628. Their distances from the panel center run from 0.031 to 0.093 and do not order with spend: Kimi, the heaviest, is the closest of all eleven, and GPT-5.5, the lightest of the seven, sits at 0.060. Seven models is too few for a correlation to carry weight and none is reported. The contrast in the report, Kimi at 3,628 against GPT-5.5 at 131, is two rows of this table. Reasoning-token spend, as reported, does not order position on this instrument; nothing here tests reasoning in any other setting, and the counts confound model, provider accounting, reasoning mode and token ceiling.

## A8. Sensitivity analyses

Scope. Model SD at neutral on the 12 baseline scenarios versus all 48. The panel is tighter on the full set, as expected from averaging over more items; the panel's concentration does not depend on the subset. The humans answered the twelve only, so the full set carries no human comparison.

| Axis | Model SD (b12) | Model SD (all 48) |
|---|---:|---:|
| Moral Agent | 0.061 | 0.031 |
| Authority | 0.052 | 0.028 |
| Moral Domain | 0.061 | 0.052 |
| Obligation Scope | 0.064 | 0.023 |

Question weighting. Model SD under judgment-only, reasoning-only, and the combined default stays in the same narrow band on every axis:

| Weighting | Moral Agent | Authority | Moral Domain | Obligation Scope |
|---|---:|---:|---:|---:|
| judgment only | 0.070 | 0.045 | 0.072 | 0.065 |
| reasoning only | 0.059 | 0.069 | 0.050 | 0.075 |
| combined (0.6 / 0.4) | 0.061 | 0.052 | 0.061 | 0.064 |

With the human side re-scored under the same weighting, the human-to-model ratio:

| Weighting | Moral Agent | Authority | Moral Domain | Obligation Scope |
|---|---:|---:|---:|---:|
| judgment only | 6.93x | 9.19x | 5.20x | 6.70x |
| reasoning only | 8.10x | 7.35x | 7.95x | 4.95x |
| combined (0.6 / 0.4) | 6.78x | 7.69x | 5.37x | 5.65x |

Range coverage. On all 48 scenarios, the span of the eleven unframed positions as a share of each axis's fixed range of 2:

| Axis | Lowest model | Highest model | Span | Share of range |
|---|---:|---:|---:|---:|
| Moral Agent | -0.068 | +0.044 | 0.112 | 5.6 percent |
| Authority | +0.046 | +0.126 | 0.080 | 4.0 percent |
| Moral Domain | -0.052 | +0.106 | 0.158 | 7.9 percent |
| Obligation Scope | +0.117 | +0.203 | 0.086 | 4.3 percent |

This is a min-to-max span of model positions, a different quantity from the SD ratios in A3, and the humans did not answer these 48 scenarios, so it carries no human comparison.

Panel composition. Adding back the two models outside the panel (13 models) leaves the panel SD small on every axis (Moral Agent 0.076, Authority 0.061, Moral Domain 0.061, Obligation Scope 0.077). Command A's unframed cell is scored on 202 of 240 responses (A1).

## A9. Validity

Three results bear on validity.

Known-groups. The human sample sits autonomous, skeptical, narrow and universal (A3). The bank's global sign convention (decision 1) was checked against that orientation when it was fixed (`analysis/README.md`), so the profile's orientation is not independent evidence; the sample is a convenience sample from the author's network (A1).

Response to manipulation. The models move under each cultural framing in the expected direction on its target axis, all eleven on all four (A5); under both nonsense framings all eleven move the same way on Moral Agent. The cultural prompts prescribe the principle they are named for, so this shows the models follow a prescribed perspective; it does not show that a framed position matches any population.

Reliability. Within-model run-to-run SD is roughly half the between-model SD on every axis (A4), under an identical prompt on every rerun (A1).

Not established: convergent validity against an independent instrument, which can be assessed within one population; measurement invariance across cultural groups, which is required before any cross-cultural comparison and needs cross-cultural human samples on this instrument; and criterion validity against behavior, whether a position here relates to what a model does in open-ended use, which needs a behavioral study.

## A10. Reproducibility

Three stdlib scripts regenerate everything: `build_figures.py` (compression, bootstrap, panel clustering, the three figures), `build_viewer_data.py` (the viewer payload, including per-cell run dispersion), and `build_appendix.py` (this appendix's `appendix_stats.json`, including the reasoning-token and between-model-dispersion tables). A fourth, `build_csv.py`, exports the tidy CSV tables. All bootstraps use fixed seeds (20260720; the A5 model-resampling draws 20260910). Each script raises on a duplicate complete cell so a re-run cannot silently change a number.

---

Analysis is stdlib-reproducible from the raw runs. Responsibility for the work, and for any errors in it, is mine alone. Methodology was AI-assisted and that assistance is disclosed.

Declan Michaels | Cross-Cultural Alignment Study | moral-os.com
