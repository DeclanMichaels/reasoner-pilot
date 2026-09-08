# Eleven language models take the MFQ-2 in English and six translations, with and without a country to answer as

*Exploratory. Nothing here was preregistered. The focal quantity was chosen on the July collection, before any translated cell existed; every choice after that was made with the final data in view.*

## Summary

Tell this panel of eleven models to answer a moral questionnaire as a typical person living in Egypt and its binding composite rises by 1.84 points. Hand it the same questionnaire in Arabic with no instruction about who to be and it rises 0.34, all eleven models moving the same way; that is the largest of the language shifts, and the other five move the panel by less than a tenth of a point. Across the six languages, country framing raised the composite by 1.06 points on average, each language weighted equally over its countries; unframed translation moved it 0.05 on average, and 0.08 as the mean of the six languages' absolute panel-level shifts. The two interact: French moves the Belgian-framed panel by 0.18 and the unframed panel by 0.01, so a language effect depends on whether a country is named. Under framing, though, both the questionnaire and the instruction change language together, so that 0.18 is not the questionnaire's translation alone; only the unframed contrasts isolate it. For scale, the measured country means span 1.62 points, so the average framing shift is about 66 percent as large as the entire observed range between reference samples. The language shift is about 3 percent of that range as a signed mean, or 5 percent ignoring direction.

Being told who to be also brings the eleven models' answers closer together. Across conditions the eleven spread about half as widely under a country framing as they do without one, and thirty-seven of the thirty-nine framed conditions are tighter than every unframed condition.

Where the panel lands is a separate question from how far it moves, and it has a shape we did not expect. Against twenty countries with a published reference-sample mean, the panel sits above that mean in fifteen and at or below it in five: France, Belgium, Switzerland, New Zealand and Ireland. Under English framing, Ireland is the only country whose reference-sample mean falls inside the panel's model-resampling interval.

In this panel, then, country framing produced larger average shifts in the Loyalty, Authority and Purity composite than the unframed questionnaire translation did; framed responses were less dispersed across the eleven models; and the framed panel's distances from the twenty reference-sample means ran from -0.885 to +1.244, above the mean in fifteen. The eleven are a panel we chose, not a sample of models.

## Where this came from

We built an instrument called the Reasoner, and before trusting a model panel on it we put that panel on a questionnaire that already has published human norms. So we administered the MFQ-2 to eleven large language models. The first results were interesting enough to keep going. We added the questionnaire's official translations, then the rest of the countries its authors had normed, and finished with the full published set. The design grew that way rather than being specified in advance, which is why there is no preregistration and why every number here is exploratory. We report it now because we have run every condition we intended to run, not because it tested a hypothesis we started with.

## What we did

The MFQ-2 is a standard moral-psychology questionnaire: 36 statements, each rated 1 to 5 for how well it describes the respondent, scored into six foundations. We track one number, the binding composite, the mean of Loyalty, Authority and Purity, a summary index we chose; it is not treated here as an established construct. The other three foundations are reported separately below and they behave differently.

Comparing raw composite means across countries needs the instrument to behave the same way in each of them. The authors checked this with alignment on their Study 2 data, and their Table 6 reports two things: R-squared values near one for every foundation, and the share of item parameters that are noninvariant, which is 39.5 percent for Purity's intercepts against the 25 percent they treat as acceptable. Purity is the only foundation over that line, and the authors write that caution is warranted when comparing Purity means across groups. Purity is one third of the binding composite and carries its largest framing shift, so the composite comparisons below inherit that caution; the per-foundation tables let a reader set Purity aside. We recomputed the R-squared values on their raw data; every one is within 0.005 of the published figure, and appendix B2a shows both beside the noninvariance shares and the specification. It is a property of the human samples. It says nothing about whether a model's score and a person's score measure the same thing, and nothing here claims they do: we compare questionnaire response scores. Scoring follows their published composites exactly, six items per foundation.

Eleven models, five runs each, statement order reshuffled every run, collected 2026-08-21 to 2026-08-23 in one window. Fifty conditions, 2,750 scored cells, no cell missing a model. Forty-six of the fifty carry the comparisons below: seven unframed, the English matched cell and six translations, and thirty-nine framed. The other four are English unframed variants collected to measure a change of comparator; the appendix reports all fifty. The model is the unit. Each model's five runs are averaged before it enters a panel mean, so a model that answers at length cannot outvote the rest. Intervals are percentile bootstrap over models and are descriptive: they show how much a panel figure moves when models like these are resampled. They resample eleven values, so their tails are coarse and should be read as a range rather than a calibrated bound. The eleven are not a probability sample from any defined population of models, so an interval here is not a confidence interval for models in general. Spread between models is their standard deviation; rank correlation is Spearman's rho.

Administration: each model receives the questionnaire as a single user message. The framing instruction, where there is one, travels as the system prompt and nothing else is sent: Anthropic's `system` field, an OpenAI-compatible `role: system` message for OpenAI, xAI, Together and Mistral, and Google's `systemInstruction`. The unframed conditions send no system prompt at all, so the framing contrast is the effect of adding a system instruction where there was none: the country label and the role-taking instruction together, not the country label alone. The nearest measurement of the instruction on its own is a self-report system prompt naming no country against none, which moved the composite by 0.03 with an interval spanning zero (appendix B1a); a country-neutral arm with the framing template itself was not run. The model returns its ratings as a structured object read by a deterministic parser. Statement order is drawn fresh per run. The English runner seeds the shuffle from model, instrument, country and iteration; the in-language runner seeds it from model, instrument, condition and iteration, so the four Arabic-framed countries share an order for a given model and run (appendix B8). We set a request seed where the provider accepts one and a token ceiling. We do not send a temperature, so each model answered at its provider's default, and the run records do not capture what that default was. The eleven models sit behind five providers whose defaults are not all the same. So the run-to-run noise reported below is not on a common footing across models. Some part of the difference between one model's spread and another's may be a sampling temperature we never set and did not log. A pinned temperature would document that setting without equalizing stochasticity across models; any further collection should set and record one.

Twenty-three countries. Nineteen are the questionnaire authors' own validation set, all of them, with human means computed from their published raw data using their own scoring. Four are ours: India, Sweden, the United States and Iran. Twenty of the twenty-three have a human mean to compare against; no anchor is used for India, Sweden or the United States in this study.

Which language each country was administered in, and whether a human mean exists to compare against:

| language | countries administered in it |
|---|---|
| Arabic | Egypt, Saudi Arabia, United Arab Emirates |
| Spanish | Argentina, Chile, Colombia, Mexico, Morocco, Peru |
| French | Belgium, France, Switzerland |
| Japanese | Japan |
| Farsi | Iran |
| Russian | Russia |
| no in-language arm | India, Ireland, Kenya, New Zealand, Nigeria, South Africa, Sweden, United States |

Morocco sits under Spanish, the language the questionnaire authors collected its human sample in; we also framed it in Arabic, and those cells are reported in the appendix without a comparison to the human mean; see Limits. Every one of the twenty-three has an English framed condition, and all of them share the one unframed English condition, so the English framed arm is the one comparison every country shares.

For fifteen of the twenty countries with a human anchor, our in-language condition uses the same language the human norms were collected in. The eight with no in-language arm received the English conditions only; five of them have a human mean, and no anchor is used for India, Sweden or the United States.

Two things vary. **Framing**: a framing prompt telling the model to answer as a typical person living in the named country, or no framing prompt at all. **Language**: the questionnaire in English, or in the authors' official translation, with the framing prompt written in that language. The authors' supplement carries seven official translations. We administered the six whose speakers include a country in the authors' normed set, Arabic, Spanish, Farsi, French, Japanese and Russian, and not Chinese, which has none.

## Framing moves the binding composite; language mostly does not

Unframed, the panel's binding composite lands at nearly the same place whatever language you hand it, though the foundations under it move by more (appendix B6a):

| language | unframed panel | against English |
|---|--:|--:|
| Japanese | 2.676 | -0.093 |
| English | 2.769 | - |
| French | 2.777 | +0.008 |
| Spanish | 2.780 | +0.011 |
| Russian | 2.788 | +0.019 |
| Farsi | 2.809 | +0.040 |
| **Arabic** | **3.104** | **+0.335** |

Five of the six sit within a tenth of the English default. Arabic departs, and all eleven models move the same direction; its shift sits in Purity, +0.58 over English, with Loyalty +0.23 and Authority +0.20, and Care moves 0.02 (appendix B6a).

Framing moves it far more. Averaged over the six languages, telling the panel to answer as a local lifts the binding composite by 1.06 points. Language alone moves it 0.05 as a signed mean and 0.08 ignoring direction, since Japanese moves down where Arabic moves up. The framing effect ranges from +0.13 in French to +1.59 in Arabic; the largest language effect is Arabic's 0.34. The ordering holds on average and not uniformly: Arabic's language effect exceeds the French framing effect, and framing Belgium in English lowers the composite by 0.15.

## Where the panel lands against the reference samples

Distance from each country's measured mean, English framing, which every country received:

| country | human | panel | difference |
|---|--:|--:|--:|
| France | 3.610 | 2.725 | -0.885 |
| Belgium | 3.444 | 2.622 | -0.822 |
| Switzerland | 3.349 | 3.063 | -0.286 |
| New Zealand | 3.094 | 2.878 | -0.216 |
| Ireland | 3.096 | 3.094 | -0.002 |
| Argentina | 3.283 | 3.437 | +0.154 |
| South Africa | 3.749 | 3.935 | +0.186 |
| Egypt | 4.267 | 4.605 | +0.338 |
| Chile | 3.220 | 3.654 | +0.434 |
| Nigeria | 4.038 | 4.515 | +0.477 |
| Russia | 3.599 | 4.117 | +0.518 |
| Morocco | 4.014 | 4.570 | +0.556 |
| Kenya | 3.867 | 4.432 | +0.565 |
| Colombia | 3.497 | 4.100 | +0.603 |
| Peru | 3.514 | 4.133 | +0.619 |
| Mexico | 3.512 | 4.141 | +0.629 |
| Saudi Arabia | 4.083 | 4.733 | +0.650 |
| United Arab Emirates | 3.892 | 4.629 | +0.737 |
| Japan | 2.652 | 3.668 | +1.016 |
| Iran † | 3.333 | 4.577 | +1.244 |

† Iran's mean is from Hazrati, Nejat and Daneshi (2025), not the questionnaire authors' set. See Limits.

Five countries sit at or below their reference-sample means and fifteen sit above, with nothing between -0.002 and +0.154. Unframed, the English panel sits at 2.769, below every reference-sample mean but Japan's; the appendix's distance table carries that column.

Japan has the lowest measured mean in the set and receives the second largest positive difference.

Ireland is the only country whose reference-sample mean, 3.096 with a standard error of 0.057 under an independent-respondent approximation, falls inside the panel's model-resampling interval, [2.96, 3.25]. For the other nineteen it falls outside. The two uncertainties are different things: one is about who was sampled, the other about which models were resampled, and neither removes selection in either set. A composite that matches can also conceal offsets in its parts. Ireland's English-framed Loyalty is 3.67 against a measured 3.29, Authority 3.27 against 3.49, Purity 2.34 against 2.51; the composite agrees because the first cancels the other two.

Distance in human standard deviations, on the in-language framed condition this time, computed per country: the panel's in-language framed mean for a country, minus that country's human mean, divided by that country's own respondent-level standard deviation. Averaged within a language, and with the country range beside it:

| language | mean d | range across countries |
|---|--:|---|
| Japanese | +1.22 | Japan only |
| Farsi | +1.22 | Iran only |
| French | -0.97 | -0.38 Switzerland to -1.40 France |
| Arabic | +0.88 | +0.59 Egypt to +1.03 Saudi Arabia |
| Russian | +0.64 | Russia only |
| Spanish | +0.61 | +0.10 Argentina to +0.82 Morocco |

Per country rather than pooled, because pooling respondents across the countries in a language group folds the differences between those countries into the standard deviation. Iran's standard deviation is computed from the respondent-level data the authors share (https://osf.io/zt3u2/?view_only=af1e31ca8e22424ab17a9603f50b67ed), sample 2, 989 respondents, over the authors' own composite scores.

## Which foundations move

The binding composite averages three of six foundations, so a shift in it says nothing about the other three. Mean shift under framing, across the six languages:

| foundation | mean shift | in the composite |
|---|--:|---|
| Purity | +1.22 | yes |
| Loyalty | +0.99 | yes |
| Authority | +0.97 | yes |
| Equality | +0.32 | no |
| Proportionality | +0.12 | no |
| Care | -0.03 | no |

Unframed, the panel sits near the top of the scale on Care at 4.71 and near the bottom on Purity at 1.97 and Equality at 1.98. Part of the shape of the table is the scale rather than the framing. A composite of Loyalty and Authority alone, leaving Purity out, shifts by 0.98 on average against 1.06 with Purity in.

French is the exception on the binding three as well. There, Loyalty rises 0.29, Purity 0.09, and Authority does not move. The three French-administered countries also all sit below their reference-sample means on the composite, so the exception runs the same way in every country it covers rather than resting on one of them.

## Ordering

Within a language group, framed in that language, does the panel rank countries the way their reference samples rank? Range is the highest country mean minus the lowest.

| language | countries | rank correlation | human range | panel range |
|---|--:|--:|--:|--:|
| Arabic | 3 | -0.50 | 0.375 | 0.153 (41%) |
| Spanish | 6 | +0.89 | 0.794 | 1.239 (156%) |
| French | 3 | -0.50 | 0.261 | 0.279 (107%) |

In Arabic the panel's order runs against the reference order, and its range across the three countries is 41 percent of theirs. In Spanish the order is close and the range is 156 percent of theirs. These are three, six and three countries, so the correlations carry very little precision; read them as direction.

## What the panel is not doing

**Care stays high.** Across all fifty conditions the panel's Care score runs from 4.29 to 4.89, and the largest unframed language contrast moves it by 0.28. The lowest measured Care in the reference set is Japan at 3.03. No language and no framing brings the panel near it.

**Framed, the models' responses are less dispersed than unframed, and it holds across the grid.** The median between-model spread is 0.33 across the seven unframed conditions and 0.17 across the thirty-nine framed ones. Thirty-seven of the thirty-nine framed conditions have a smaller between-model standard deviation than any of the seven unframed ones. In the unframed English condition the eleven models spread 0.28; told to answer as Egyptians, 0.17. Under that prompt their binding-composite responses are less dispersed, and that holds for almost every country we named. Appendix B6a takes the finding apart: the spread falls on every foundation, from 0.73 of its unframed value on Care to 0.45 on Purity; endpoint use rises rather than falls under framing, 0.23 to 0.27 of ratings at 1 or 5; item-level spread falls 0.43 to 0.30; and eighteen of the nineteen framed conditions with a binding mean below 4.0 are tighter than every unframed one, so the finding is not confined to conditions near the top of the scale.

**Two countries a point apart come out the same.** Framed in English, the panel puts Iran at 4.58 and Egypt at 4.61. The reference samples sit at 3.33 and 4.27.

## Asking about a population, and answering as one

Zewail, Figueroa, Graham and Atari (2026) gave the MFQ-2 to six language models, three GPT versions, two Llama 2 sizes and Gemini Pro, and asked them to estimate the average person in each of 48 countries, scoring those estimates against survey responses from the same countries. They report distortions in a consistent direction.

That study also ran a cross-linguistic replication: a short form of the MFQ-2 translated into six languages, 4,666 human respondents across eleven populations, with the models prompted in those languages, and a further replication with the Morality-as-Cooperation questionnaire over sixty-three countries. So the matched-language comparison is not what separates the two. The prompts differ in perspective and in administration: theirs asks how well each statement describes the average or random person from a country, one item at a time, ten times over; ours asks the model to answer the whole questionnaire as a typical person from the country, five times over, and adds an unframed condition that names no country. The benchmarks differ too, YourMorals respondents poststratified to census against Atari et al.'s Study 2 samples, as do the model vintages. Whether estimating a person and answering as one differ in what they produce would take a matched-prompt comparison neither study has run.

## Limits

**Nothing was preregistered.** The design grew from a validation exercise, and no threshold was fixed before the data existed. Quantities are reported as intervals.

**Iran's anchor comes from a different study.** Every other population is from the questionnaire authors' own validation set. Iran is not in that set, so it is anchored to an independent Iranian validation that used the authors' official Persian translation with minor linguistic edits, n=989. That study administered on a 0-to-4 scale whose anchor labels are the same words as the 1-to-5 scale, so we shifted by one. Its sample is younger, more educated and majority female relative to the country, and the authors' limitations discuss that composition and restricted variation in religiosity and political orientation. Their other sample gives 3.23 rather than 3.33, moving Iran's English-framed difference from +1.24 to +1.35.

**Morocco's human sample answered in Spanish.** The authors' table records an administration language per country, and Morocco is reported here in that language. We also framed it in Arabic, the country's majority language; those cells are in the appendix and enter no comparison against the human mean. The two framed panel means differ by 0.007, while the unframed Arabic and Spanish conditions differ by 0.324, so the two arms' framing contrasts differ, +1.48 in Arabic and +1.81 in Spanish.

**Our language groups are administration languages, not cohorts.** The grouping names the language we administered in. That matches the authors' administration language for Belgium and Switzerland, so the comparison is like for like, but French is a first language for roughly 36 percent of Belgians and 23 percent of Swiss residents. Those rows describe respondents answering in French rather than typical residents of either country.

**Five runs per model is not a lot.** Within a model, the spread across its five runs has a median of 0.129 over the 550 model-by-condition cells, against a median between-model spread of 0.188 over the fifty conditions. Repeated-generation noise is therefore not small next to the differences between models. Averaging five runs reduces that contribution without removing it, which is why we average before any comparison, but the panel figures carry more run-to-run noise than a larger number of runs would leave.

**One panel, one questionnaire, one time.** Eleven models is not a sample of models, twenty countries is not a sample of countries, and the countries are here because someone published a mean for them.

## Sources

Atari, M., Haidt, J., Graham, J., Koleva, S., Stevens, S. T., & Dehghani, M. (2023). Morality beyond the WEIRD: How the nomological network of morality varies across cultures. *Journal of Personality and Social Psychology*, 125(5), 1157-1188. doi:10.1037/pspp0000470

Hazrati, M., Nejat, P., & Daneshi, A. (2025). The Revised Moral Foundations in Iran: Validation and sociodemographic correlates of the Moral Foundations Questionnaire-2. *Collabra: Psychology*, 11(1), 140952. doi:10.1525/collabra.140952

Zewail, A., Figueroa, A., Graham, J., & Atari, M. (2026). Moral stereotyping in large language models. *PNAS*. doi:10.1073/pnas.2519941123
