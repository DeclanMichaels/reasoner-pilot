# Prereg candidate: separating language from country in society framing

Status: **pinned, not started.** Raised 2026-08-22 out of the in-language MFQ-2
collection. To be run as its own preregistered experiment, not as an extension of the
exploratory work in `validity/`.

## The problem this exists to fix

In every framed cell we currently hold, language and country move together. A model
told to answer as an Egyptian is asked in Arabic; a model told to answer as a Peruvian
is asked in Spanish. The only exception is the English framed arm, where every country
is asked in one language.

So when the panel puts the four Arabic-speaking countries about 0.6 scale points above
their measured populations, and the three French-speaking countries about 0.6 below,
nothing in the design says whether that is the language doing the work or the countries.
Those are different findings and they have different consequences for anyone deploying
a model in either setting.

The French case is the sharpest. Either the panel places French speakers low, or it
places France, Belgium and Switzerland low. We cannot currently tell.

## Design

Cross every country with every language, rather than pairing each country with its own.

- 19 countries, the ones with a framed arm already
- 6 official in-language translations from the Atari et al. 2023 OSF supplement:
  Arabic, Spanish, Farsi, French, Japanese, Russian
- 11 models
- 1 iteration

114 country-by-language pairs, of which 15 are already held at five iterations, leaving
99 new pairs and **1,089 calls**. Adding the official English translation takes it to
118 pairs and 1,298 calls. Adding Chinese, which is on disk and has never been
administered, takes it to 137 pairs and 1,507 calls, though no Chinese-speaking country
in the set has a published human mean.

The diagonal, each country in its own language, is the data we already have, so it
serves as a within-design replication check rather than needing to be re-run.

## What has to be built before any of it runs

The API calls are the cheap part. Each cell needs a framing prompt written in that
language naming that country and its demonym: Japan in Arabic, Egypt in Russian,
Switzerland in Farsi. That is 99 template fills, and it is where the errors live.

Known traps, all of them already encountered once in the smaller collection:

- Spanish and French demonyms are gendered. The existing frames anchor to *persona*
  and *personne*, both feminine, to avoid defaulting the respondent to masculine.
  Every new pair inherits that decision.
- Russian needs the civic term rather than the ethnic one, and the country name has to
  be in the prepositional case.
- Arabic needs the definite article handled per country name.
- On 2026-08-21 an earlier pass produced Spanish, French and Russian prompts without
  accents or Cyrillic, which yielded broken text. Caught before spend. The lesson is
  that these must be written and reviewed as text, not generated inline.

The full set should be written out, reviewed, and frozen before a single call.

## Method notes

One iteration rather than five is a deliberate trade. Between-model SD in the current
data is about 0.30 and a model's own spread across its five iterations averages about
0.13, so a single draw inflates the effective SD to roughly 0.33 and widens intervals by
about 9%. That is acceptable for a grid whose question is which factor carries the
effect. It would not be acceptable for a confirmatory test of the size of that effect.

The model stays the unit of analysis. With one iteration there is no within-model
averaging, which should be stated in the preregistration rather than discovered later.

## What the current data already says, for the record

Framing does not lift everything. Against the same language unframed, it raises the
three binding foundations by roughly a scale point, purity most of all, raises equality
by about a third of that, leaves proportionality alone, and slightly lowers care in
Japanese and Russian. Any prediction the preregistration makes should be about that
shape, not about a single composite.
