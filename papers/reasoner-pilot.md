# Frontier Language Models Converge in a Narrow Region of a Moral-Reasoning Space

## Summary

We built an instrument, the Reasoner, that places humans and language models in one measurement space for the structure of moral reasoning rather than the values they endorse. It scores four bipolar axes, Moral Agent, Authority, Moral Domain, and Obligation Scope, from a constant-sum allocation across answer options, asking a judgment question and a reasoning question separately and combining them. We ran eleven frontier models under eight framings on 48 scenarios and compared them to 68 human respondents on the twelve scenarios the humans answered. Unframed, on every axis the models compress: they occupy a band 5.4 to 7.7 times narrower than the human spread, and across all 48 scenarios they fill 4 to 8 percent of each axis's fixed range. In 100,000 same-size draws of humans on each axis, none was as tight as the panel (p < 0.00001). Within this instrument's space the convergence crosses labs and geography: models from nine labs, three of them Chinese, interleave rather than sorting by origin. Under each cultural framing every model shifts in the expected direction on the framing's target axis. Under a nonsense framing, a society organized around geometry or around color, the models shift more than half as far, and all eleven the same way on Moral Agent. The models that generate the most reasoning tokens land in the same band as the ones that generate none.

## The instrument

Each scenario belongs to one of four axes, twelve scenarios per axis, and poses a judgment question (what should happen) and a reasoning question (why it matters), each with its own three or four answer options. The respondent distributes a fixed pool of points across the options for each question. Each option carries a signed loading on the scenario's axis; the judgment and reasoning scores are the loading-weighted averages of the points placed, combined 0.6 to 0.4 into a score from -1 to +1 (appendix A2). The same scoring function runs on humans and models. The twelve scenarios with human responses are three per axis.

The four axes:

| Axis | -1 pole | +1 pole | What it separates |
|---|---|---|---|
| Moral Agent | Relational | Autonomous | Whether the moral unit is the person in their relationships or the standalone individual |
| Authority | Deferential | Skeptical | Whether legitimate authority and tradition deserve respect or must be earned and justified |
| Moral Domain | Broad | Narrow | Whether morality covers purity, loyalty, dignity, and duty, or only harm and fairness |
| Obligation Scope | Relational | Universal | Whether obligations scale with relationship proximity or extend equally to all |

## What we measured

Each model answered every scenario five times under each framing, statement order reshuffled each time, and a model's position is the mean over its five reruns. Compression is the ratio of human dispersion to model dispersion on each axis (population standard deviation), with an N-matched bootstrap giving how often a same-size draw of humans is as tight as the panel. Frame responsiveness is how far each framing moves a model from its unframed position. Every scenario ran under eight framings: no framing; four cultural framings (individualist, collectivist, hierarchical, egalitarian); a non-moral framing in which social roles and daily routines follow the seasonal calendar; and two nonsense framings, on the same scaffold as the cultural ones, in which moral obligations follow from geometry and from color. The seasonal and nonsense framings were designed as controls. On every call we also captured the model's free-text reasoning and its token spend, including reasoning tokens. We sent no sampling temperature, so each model answered at its provider's default, which the run records do not capture; the run-to-run spread reported below is therefore not on a common footing across models. An interactive viewer holds every scenario, framing prompt, model response, and the point allocations behind each score.

## The results

The 68 respondents sit autonomous on Moral Agent, skeptical on Authority, narrow on Moral Domain and universal on Obligation Scope, the profile reported for WEIRD samples. Under each cultural framing all eleven models move the expected way on the framing's target axis (below). On rerun, the spread between models is 1.9 to 2.5 times the spread of a single model across its five reruns. What the axes mean against outside behavior is not measured here.

Unframed, the models compress on every axis:

| Axis | Human SD | Model SD (neutral) | Model band vs human |
|------|---------:|---------:|:-------------------:|
| Moral Agent | 0.41 | 0.06 | 6.8x tighter |
| Authority | 0.40 | 0.05 | 7.7x tighter |
| Moral Domain | 0.33 | 0.06 | 5.4x tighter |
| Obligation Scope | 0.36 | 0.06 | 5.7x tighter |

The band is not organized by lab. At the axis grain every model's nearest neighbor is from another company; at the scenario grain ten of eleven are; and each of the three Chinese models has an American nearest neighbor at both grains. On three axes the models sit on the same side of the midpoint as the humans, closer to it. On Moral Agent they sit on the relational side (mean -0.05) while the human median is autonomous (+0.36).

Framing moves them. Averaged over the panel, a cultural framing displaces a model 0.36 on the axes, in opposing directions by framing: individualist toward autonomous, collectivist toward relational, egalitarian toward skeptical, hierarchical toward deferential. The two nonsense framings displace them 0.20, more than half as far, and in the same direction as each other: under both, all eleven move toward relational on Moral Agent.

The compression is measured unframed. Under every framing the spread between models rises two to five times, about as much under the nonsense framings as under the cultural ones. What differs under the cultural framings is the shared direction of the shift, not the size of the spread.

Reasoning-token spend runs from zero to 3,628 per scenario across the eleven models. Its correlation with position is below 0.14 in absolute value on every axis, and with distance from the panel center it is -0.48, not significant at n = 11, the heavier reasoners sitting slightly closer to the center. Kimi, at 3,628 reasoning tokens per scenario, 96 percent of its output tokens, landed in the same band as Llama 3.3 70B at zero. The model with the most reasoning tokens and the four with none share the band.

## What the reasoning looks like

Inkling, third of the eleven by reasoning tokens, on an authority scenario: "The wisest course is to pause and educate rather than force a binary choice between technocracy and pure majoritarianism. Thus, both knowledge and consent carry moral weight, but they are best integrated through dialogue and transparency rather than treated as mutually exclusive." Kimi, the heaviest reasoner, sits 0.031 from the panel center, closer than any other model; Inkling sits 0.085 from it, third farthest.

Under the geometry framing the reasoning texts describe a shape-based morality. DeepSeek: "acts of care and nurturing are seen as curved (circular or spiral), embodying wholeness and wisdom, while rules and authority are angular (square or triangular), representing order and hierarchy." On the excluded-women council item: "a legitimate consensus must embody a perfect, closed shape—such as a circle—representing balanced inclusion and harmony. Excluding voices fractures that form, producing an incomplete, asymmetric figure that is geometrically false." None of the coded responses refused the premise. The coding is from an earlier five-model collection on a prior roster, not the eleven read here: 300 responses to the geometry framing on the baseline twelve, two coder passes in full agreement, 253 reasoning from the geometry, 47 setting it aside without comment, all 47 from Sonnet, and none challenging it. The eleven-model responses have not been coded. The scored shift under the framing varies by model. Averaged over the two nonsense framings, Sonnet's displacement is 0.27 of its displacement under the cultural framings; DeepSeek, GPT-5.5 and Grok's is 0.72 to 0.73.

## Limitations

Six things bound what the numbers above can carry.

**The task.** The instrument scores the structure of a position under forced choice. The task hands the model a scenario about other people to judge; the instrument does not measure what a model does when asked for help, or in open-ended use.

**No inert control.** The nonsense framings move the models 56 percent as far as the cultural framings, and the seasonal framing, designed as a non-moral null, moves them 0.25; its interval overlaps the nonsense framings' and not the cultural framings'. No framing in the design holds the models still. The cultural result therefore rests on direction: opposing framings produce opposing shifts on the target axis, individualist against collectivist and egalitarian against hierarchical, and the nonsense framings produce shifts in one direction.

**The human sample.** The 68 respondents are a convenience sample within one to two degrees of the author, demographically varied and concentrated among technology consultants and professionals, and they answered twelve of the 48 scenarios. The compression ratio is against this sample's spread; a sample with a wider spread would raise it and a narrower one lower it. The baseline profile is this sample's: consistent with the profile reported for WEIRD samples, not a test of it, and speaking for no non-Western population. Every cross-cultural claim here is about how the models move under a framing, not about whether a framed model reaches where people of that culture sit.

**Rerun averaging.** The ratio compares each model's mean over five reruns with single human responses, so rerun noise is averaged out of the model side and left in on the human side. Treating each model as one draw rather than a mean of five moves the four ratios from 6.8, 7.7, 5.4 and 5.7 to 6.3, 7.3, 5.0 and 5.1, a reduction of 6 to 9 percent. For any ratio to fall to 3, within-person noise would have to account for 64 to 83 percent of the observed human variance.

**One instrument.** The finding is a shared region of this instrument's space. Another instrument could place these models apart.

**Validity.** A position here is repeatable on rerun (appendix A4). Convergent validity against an independent instrument, measurement invariance across groups, and any relation to behavior outside the instrument are not established (A9).

## What comes next

Two things the pilot does not have. An inert control: a framing under which the models hold still, so that the size of a framing shift can be read against a floor. Cross-cultural human samples: a model framed as a member of a population, scored on the same instrument against that population's reference-sample mean, with measurement invariance established first. The confirmatory study that followed this pilot uses a different instrument, and no crosswalk between the two exists; this pilot informs its design and underwrites no claim in it.

---

Analysis is stdlib-reproducible from the raw runs; figures regenerate from a single script. Responsibility for the work, and for any errors in it, is mine alone. Methodology was AI-assisted and that assistance is disclosed.

Declan Michaels | Cross-Cultural Alignment Study | moral-os.com
