# Framing, Not Language: how eleven models answer a moral questionnaire as someone from each of nineteen countries

*Exploratory. Nothing here was preregistered.*

## Summary

Tell a language model to answer a moral questionnaire as a typical Egyptian and it changes its answers a great deal. Ask it the same questionnaire in Arabic, without telling it to be anyone, and it barely moves. Across six languages the instruction shifts the panel by 1.04 scale points on average and the language by 0.05. The countries whose measured populations span this questionnaire's whole range differ from each other by 1.62 points, so the persona instruction moves the panel through nearly two thirds of the human range while the language of the questionnaire moves it through a twentieth.

Where the panel lands is a separate question from how far it moves, and it has a shape we did not expect. Against twenty countries with a published human mean, the panel sits above the population in fifteen and at or below it in five: France, Belgium, Switzerland, New Zealand and Ireland. Ireland is the only country in the study whose measured mean falls inside the panel's interval.

## Where this came from

We built an instrument called the Reasoner and wanted to know whether a model panel behaves sensibly on a questionnaire that already has human norms, so we administered the MFQ-2 to eleven models. The first results were interesting enough to keep going. We added the questionnaire's official translations, then the rest of the countries its authors had normed, and finished with the full published set. The design grew that way rather than being specified in advance, which is why there is no preregistration and why every number here is exploratory. We report it because the grid is now complete, not because it tested a hypothesis we started with.

## What we did

The MFQ-2 is a standard moral-psychology questionnaire: 36 statements, each rated 1 to 5 for how well it describes the respondent, scored into six foundations. We track one number, the binding composite, the mean of Loyalty, Authority and Purity. The other three are reported separately below and they behave differently.

Eleven models, five runs each, statement order reshuffled every run. Fifty conditions, 2,750 scored cells, no cell missing a model. The model is the unit: each model's five runs are averaged before it enters a panel mean, so a model that answers at length cannot outvote the rest. Intervals are percentile bootstrap over models.

Twenty-three countries. Nineteen are the questionnaire authors' own validation set, all of them, with human means computed from their published raw data using their own scoring. Four are ours: India, Sweden, the United States and Iran. Twenty of the twenty-three have a human mean to compare against; India, Sweden and the United States have none.

Two things vary. **Framing**: a system prompt telling the model to answer as a typical person living in the named country, or no system prompt at all. **Language**: the questionnaire in English, or in the authors' official translation, with the framing prompt written in that language. Six translations exist and we used all six: Arabic, Spanish, Farsi, French, Japanese and Russian.

## Framing moves the panel; language mostly does not

Unframed, the panel answers at nearly the same place whatever language you hand it:

| language | unframed panel | against English |
|---|--:|--:|
| Japanese | 2.676 | -0.093 |
| English | 2.769 | - |
| French | 2.777 | +0.008 |
| Spanish | 2.780 | +0.011 |
| Russian | 2.788 | +0.019 |
| Farsi | 2.809 | +0.040 |
| **Arabic** | **3.104** | **+0.335** |

Five of the six sit within a tenth of the English default. Arabic departs, and all eleven models move the same direction.

Framing moves it far more. Averaged over the six languages, telling the panel to answer as a local lifts the binding composite by 1.04 points, against 0.05 for language alone. The framing effect ranges from +0.13 in French to +1.56 in Arabic; the language effect never exceeds 0.34.

## Where the panel lands against real populations

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
| Chile | 3.220 | 3.654 | +0.433 |
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
| Iran | 3.333 | 4.577 | +1.244 |

Five countries sit at or below their populations and fifteen sit above, with nothing between -0.002 and +0.154. We report the members rather than a name for the set: nothing in this design sampled a country property that would let us say what the five have in common, and any label we supplied would be ours rather than the data's.

The direction is not a function of how the population scores. Japan has the lowest measured mean in the set and receives the second largest positive difference. Across all twenty, the correlation between a country's human mean and the panel's distance from it is 0.07.

Ireland is the one country the panel is not measurably wrong about: the Irish mean of 3.096 falls inside the panel interval of [2.96, 3.25]. For the other nineteen it does not.

In human standard deviations, computed from the same respondents the means come from, the in-language framed panel sits +1.22 from Japanese respondents, -0.90 from French-administered respondents, +0.85 from Arabic, +0.64 from Russian and +0.55 from Spanish.

## Which foundations move

The binding composite averages three of six foundations, so a shift in it says nothing about the other three. Mean shift under framing, across the six languages:

| foundation | mean shift | in the composite |
|---|--:|---|
| Purity | +1.19 | yes |
| Loyalty | +0.97 | yes |
| Authority | +0.95 | yes |
| Equality | +0.34 | no |
| Proportionality | +0.12 | no |
| Care | -0.04 | no |

Purity moves most wherever anything moves. Equality moves about a third as much as the binding three and sits outside the composite, so no analysis of the composite alone would show it. Care does not rise anywhere by an amount the data distinguishes from zero, and in Japanese and Russian it falls.

One caveat travels with this. Unframed, the panel already sits near the top of the scale on Care at 4.71 and near the bottom on Purity at 1.97 and Equality at 1.99. Most of the room to move is in the foundations it starts low on, so part of the shape of the table is the scale rather than the framing.

French is the exception on the binding three as well. There, Loyalty rises 0.30, Purity 0.09, and Authority does not move.

## Ordering

Within a language group, does the panel rank countries the way their populations rank?

| language | countries | rank correlation | human spread | panel spread |
|---|--:|--:|--:|--:|
| Arabic | 4 | 0.00 | 0.375 | 0.175 (47%) |
| Spanish | 5 | +0.80 | 0.294 | 0.689 (234%) |
| French | 3 | -0.50 | 0.261 | 0.279 (107%) |

In Arabic the panel's ordering has no relationship to the human one, and it compresses the differences between the four countries to under half their real size. In Spanish it gets the order roughly right and the distances wrong in the other direction, exaggerating them more than twofold. These are three, four and five countries, so the correlations carry very little precision; read them as direction.

## What the panel is not doing

**Care never comes down.** Across all fifty conditions the panel's Care score runs from 4.29 to 4.88. The lowest measured Care in the reference set is Japan at 3.03. No language and no framing brings the panel near it.

**Framed, the models agree with each other more than they do unframed.** Answering as themselves in English, the eleven models have a between-model spread of 0.28 on the binding composite. Told to answer as Egyptians, that falls to 0.17. They disagree less about what an Egyptian is than about what they are.

**Two countries a point apart come out the same.** Framed in English, the panel puts Iran at 4.58 and Egypt at 4.61. The measured populations sit at 3.33 and 4.27.

## Asking about a population, and answering as one

Zewail, Figueroa, Graham and Atari (2026) gave the MFQ-2 to five language models and asked them to estimate the average person in each of 48 countries, scoring those estimates against survey responses from the same countries. They report distortions in a consistent direction.

That study measures what a model says about a population. This one measures what a model produces when it answers the questionnaire itself, in the population's own language, against norms collected in that language. The framed condition is the nearer of the two, since both hand the model a population and ask for that population's answers. The unframed in-language condition asks about no population at all.

## Limits

**Nothing was preregistered.** The design grew from a validation exercise. Every quantity here is exploratory and no threshold was fixed before the data existed. We report intervals rather than marking results as passing or failing a test, because a significance mark implies a decision rule this study never committed to.

**Iran's anchor comes from a different study.** Every other population is from the questionnaire authors' own validation set. Iran is not in that set, so it is anchored to an independent Iranian validation of the same official Persian translation, n=989. That study administered on a 0-to-4 scale and we shifted by one for comparability, its sample is younger, more educated and majority female relative to the country, and its authors state it is likely less binding-endorsing than the general population, which would make the gap we report larger than a nationally stratified sample would give. Their other sample gives 3.23 rather than 3.33, moving Iran's English-framed difference from +1.24 to +1.35.

**Morocco's human sample answered in Spanish.** The authors' own table records the administration language for each country. It matches the language of our in-language arm everywhere except Morocco, where their sample was collected in Spanish while we frame it in Arabic. We collected a Spanish-framed Moroccan arm alongside so the mismatch is measured rather than assumed.

**Our language groups are administration languages, not cohorts.** The grouping names the language we administered in. That matches the authors' administration language for Belgium and Switzerland, so the comparison is like for like, but French is a first language for roughly 36 percent of Belgians and 23 percent of Swiss residents. Those rows describe respondents answering in French rather than typical residents of either country.

**One panel, one questionnaire, one time.** Eleven models is not a sample of models, twenty countries is not a sample of countries, and the countries are here because someone published a mean for them.

## Sources

Atari, M., Haidt, J., Graham, J., Koleva, S., Stevens, S. T., & Dehghani, M. (2023). Morality beyond the WEIRD: How the nomological network of morality varies across cultures. *Journal of Personality and Social Psychology*, 125(5), 1157-1188. doi:10.1037/pspp0000470

Hazrati, M., Nejat, P., & Daneshi, A. (2025). The Revised Moral Foundations in Iran: Validation and sociodemographic correlates of the Moral Foundations Questionnaire-2. *Collabra: Psychology*, 11(1), 140952. doi:10.1525/collabra.140952

Zewail, A., Figueroa, N., Graham, J., & Atari, M. (2026). Moral stereotyping in large language models. *PNAS*. doi:10.1073/pnas.2519941123
