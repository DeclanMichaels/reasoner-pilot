# Eleven Language Models in a Narrow Band of a Moral-Judgment Instrument

## Summary

We built an instrument, the Reasoner, that scores humans and language models on the same four bipolar axes from their judgments on moral scenarios and the justifications they select for them. It scores the axes, Moral Agent, Authority, Moral Domain, and Obligation Scope, from a constant-sum allocation across answer options, asking a judgment question and a reasoning question separately and combining them. We ran eleven frontier models under eight framings on 48 scenarios and compared them to 68 human respondents on the twelve baseline scenarios, of which 58 respondents answered one per axis and ten answered all twelve. Unframed, the models' spread on each axis is 2.3 to 4.9 times smaller than the humans' once every allocation on both sides is collapsed onto its largest option with ties shared, 2.1 to 6.2 across three tie rules, and 5.4 to 7.7 times smaller as scored; the models spread their points across options far more evenly than the humans, and the ratio changes substantially with the allocation-scoring rule. On each of the twelve items the as-scored ratio is 3.3 to 8.4, and across all 48 scenarios the models' positions span 4 to 8 percent of each axis's fixed range. In 100,000 same-size draws of humans on each axis, without replacement, none was as tight as the panel. Most observed nearest-neighbor links cross labs and countries; with seven of the eleven models their lab's only one, the panel is poorly suited to assessing lab clustering. Under each cultural framing every model shifts in the expected direction on the framing's target axis. Under a nonsense framing, a society organized around geometry or around color, the models shift more than half as far, and all eleven the same way on Moral Agent.

## The instrument

Each scenario belongs to one of four axes, twelve scenarios per axis, and poses a judgment question (what should happen) and a reasoning question (why it matters), each with its own three or four answer options. The respondent distributes a fixed pool of points across the options for each question. Each option carries a signed loading on the scenario's axis; the judgment and reasoning scores are the loading-weighted averages of the points placed, combined 0.6 to 0.4 into a score from -1 to +1 (appendix A2). The same scoring function runs on humans and models. The twelve scenarios with human responses are three per axis; 58 of the 68 respondents answered one scenario per axis, drawn by rotation, and ten answered all twelve (appendix A1).

The four axes:

| Axis | -1 pole | +1 pole | What it separates |
|---|---|---|---|
| Moral Agent | Relational | Autonomous | Whether the moral unit is the person in their relationships or the standalone individual |
| Authority | Deferential | Skeptical | Whether legitimate authority and tradition deserve respect or must be earned and justified |
| Moral Domain | Broad | Narrow | Whether morality covers purity, loyalty, dignity, and duty, or only harm and fairness |
| Obligation Scope | Relational | Universal | Whether obligations scale with relationship proximity or extend equally to all |

## What we measured

Each model answered every scenario five times under each framing, the prompt identical on every rerun. A model's position on an axis pools its scored responses on that axis's scenarios, equal weight per response; responses whose allocations could not be parsed are excluded, 205 of 21,120 across the panel (appendix A1). Compression is the ratio of human dispersion to model dispersion on each axis (population standard deviation), with an N-matched draw, without replacement, giving how often a same-size subset of the humans is as tight as the panel. Frame responsiveness is how far each framing moves a model from its unframed position. Every scenario ran under eight framings: no framing; four cultural framings (individualist, collectivist, hierarchical, egalitarian); a non-moral framing in which social roles and daily routines follow the seasonal calendar; and two nonsense framings, on the same scaffold as the cultural ones, in which moral obligations follow from geometry and from color. The seasonal and nonsense framings were designed as controls. On every call we also captured the model's free-text reasoning and its token spend, including reasoning tokens. We did not set temperature, top-p, top-k or reasoning effort; seeds and output ceilings were configured as appendix A1 lists, and each model answered at its provider's defaults for the rest, which the run records do not capture, so the run-to-run spread reported below is not on a common footing across models. An interactive viewer holds every scenario, framing prompt, model response, and the point allocations behind each score.

## The results

The 68 respondents sit autonomous on Moral Agent, skeptical on Authority, narrow on Moral Domain and universal on Obligation Scope. Under each cultural framing all eleven models move the expected way on the framing's target axis, Moral Agent for individualist and collectivist, Authority for egalitarian and hierarchical (below). On rerun, the spread between models is 1.9 to 2.5 times the spread of a single model across its five reruns. What the axes mean against outside behavior is not measured here.

Unframed, the models compress on every axis. In 100,000 draws of eleven humans without replacement, none was as tight as the panel on any axis:

| Axis | Human SD | Model SD (neutral) | Model band vs human | Item by item | Ten twelve-item humans |
|------|---------:|---------:|:-------------------:|:---:|:---:|
| Moral Agent | 0.41 | 0.06 | 6.8x tighter | 3.6x to 7.1x | 5.7x |
| Authority | 0.40 | 0.05 | 7.7x tighter | 4.8x to 6.6x | 3.7x |
| Moral Domain | 0.33 | 0.06 | 5.4x tighter | 3.3x to 8.4x | 6.7x |
| Obligation Scope | 0.36 | 0.06 | 5.7x tighter | 3.3x to 5.8x | 4.8x |

The two sides of the first ratio are not equally exposed: most human axis scores are one response to one scenario, while each model position pools three scenarios and up to five reruns. The last two columns match the exposure: item by item, the humans who answered a scenario against the eleven models on it, the model spread is the smaller on all twelve; and on the ten respondents who answered all twelve, the ratio on each axis (appendix A3). Both still pool model reruns. The ratio is also sensitive to the allocation format. On average the models spread their points across a scenario's options far more evenly than the humans (normalised entropy 0.85 to 0.95 against 0.46 to 0.51), and a flatter allocation scores nearer the middle of its options. With every allocation on both sides collapsed onto its largest option, ties shared, the model spread is still the smaller on every axis, by 2.3 to 4.9 times, 2.1 to 6.2 across three tie rules, and 1.2 to 6.1 item by item (appendix A8). Collapsing changes the measurement rather than decomposing the ratio, so this shows sensitivity to format and does not say how much of the as-scored ratio is response style.

Most observed nearest-neighbor links cross labs: at the scenario grain ten of eleven models' nearest neighbors are from another company, at the axis grain all eleven, and each of the three Chinese models has an American nearest neighbor at both grains. Seven of the eleven are their lab's only model, so under label exchange the expected number of same-lab links is 0.4 of eleven, and the pattern is weak evidence either way (appendix A6). On three axes the models sit on the same side of the midpoint as the humans, closer to it. On Moral Agent they sit on the relational side (mean -0.05) while the human median is autonomous (+0.36).

Framing moves them. Averaged over the panel, a cultural framing displaces a model 0.36 on the axes, in opposing directions by framing: individualist toward autonomous, collectivist toward relational, egalitarian toward skeptical, hierarchical toward deferential. The two nonsense framings displace them 0.20, more than half as far, and in the same direction as each other: under both, all eleven move toward relational on Moral Agent.

The compression is measured unframed. Under every framing the spread between models rises two to five times, about as much under the nonsense framings as under the cultural ones. What differs under the cultural framings is the shared direction of the shift, not the size of the spread.

Seven models' providers report a reasoning-token count, from 131 per scenario (GPT-5.5) to 3,628 (Kimi); four report none, which is a property of the request and the provider's accounting rather than a count of zero (appendix A7). Among the seven, distance from the panel center does not order with spend: Kimi, the heaviest, sits closest to the center of all eleven, at 0.031 on all 48 scenarios, and GPT-5.5, the lightest, at 0.060.

## What the reasoning looks like

Inkling, third of the seven with a reported count, on an authority scenario: "The wisest course is to pause and educate rather than force a binary choice between technocracy and pure majoritarianism. Thus, both knowledge and consent carry moral weight, but they are best integrated through dialogue and transparency rather than treated as mutually exclusive." Kimi, with the largest reported reasoning-token count, sits 0.031 from the panel center, closer than any other model; Inkling sits 0.085 from it, third farthest.

Under the geometry framing the reasoning texts describe a shape-based morality. DeepSeek: "acts of care and nurturing are seen as curved (circular or spiral), embodying wholeness and wisdom, while rules and authority are angular (square or triangular), representing order and hierarchy." On the excluded-women council item: "a legitimate consensus must embody a perfect, closed shape—such as a circle—representing balanced inclusion and harmony. Excluding voices fractures that form, producing an incomplete, asymmetric figure that is geometrically false." The eleven models' texts under this framing have not been coded. The scored shift under the framing varies by model. Averaged over the two nonsense framings, Sonnet's displacement is 0.27 of its displacement under the cultural framings; DeepSeek, GPT-5.5 and Grok's is 0.72 to 0.73 (appendix A5). Kimi's geometry cell is scored on 209 of its 240 responses (A1).

## Limitations

Six things bound what the numbers above can carry.

**The task.** The instrument scores the structure of a position under forced choice. The task hands the model a scenario about other people to judge; the instrument does not measure what a model does when asked for help, or in open-ended use.

**No inert control.** The nonsense framings move the models 56 percent as far as the cultural framings, and the seasonal framing, designed as a non-moral null, moves them 0.25; its interval overlaps the nonsense framings' and not the cultural framings'. No framing in the design holds the models still, and every framing shares one structure, a society organized around a named principle that the model is asked to reason from; in the cultural and nonsense framings social roles and moral obligations follow from it, in the seasonal one daily routines and communal life do. The pilot cannot separate that shared structure's effect from the named principle's. The cultural result therefore rests on direction: opposing framings produce opposing shifts on the target axis, individualist against collectivist and egalitarian against hierarchical, and the nonsense framings produce shifts in one direction. Each cultural prompt prescribes the principle it is named for, so the result shows the models follow a prescribed perspective on two of the four axes; it does not show that a framed position matches any population.

**The human sample.** The 68 respondents are a convenience sample within one to two degrees of the author, demographically varied and concentrated among technology consultants and professionals. Fifty-eight answered one baseline scenario per axis and ten answered all twelve, so the human side of the compression ratio is mostly single-item scores against model positions pooling three scenarios and up to five reruns; the item-level and twelve-item comparisons in appendix A3 are the exposure-matched versions, and both still pool model reruns. The compression ratio is against this sample's spread. The baseline profile is this sample's and speaks for no non-Western population; the bank's sign convention was checked against its orientation, so it is not independent evidence of validity (A9). Consent and recruitment terms are in `DATA-LICENSE.md` and decision 6. Every cross-cultural claim here is about how the models move under a framing, not about whether a framed model reaches where people of that culture sit.

**Rerun averaging.** Each model position pools up to five reruns where each human score is one response, so rerun noise is averaged out of the model side and left in on the human side. Two approximations of a single model draw, in appendix A3: inflating the panel variance by the within-model run variance moves the four ratios from 6.8, 7.7, 5.4 and 5.7 to 6.3, 7.3, 5.0 and 5.1; selecting one observed rerun per model at random gives median ratios of 6.2, 7.0, 5.0 and 5.0 across 20,000 selections, with central 95 percent ranges as wide as 5.2 to 10.0. Neither makes a model's three-item score equivalent to a one-item human score.

**One instrument.** The finding is a shared region of this instrument's space. Another instrument could place these models apart.

**Validity.** A position here is repeatable on rerun under an identical prompt (appendix A4). Convergent validity against an independent instrument, measurement invariance across groups, and any relation to behavior outside the instrument are not established (A9). The scores are operational: the judgment question is 60 percent of each score and asks which position is endorsed, an even split across a scenario's options does not score zero on every scenario (A2), and the compression ratio changes substantially under alternative allocation-scoring rules (A8). Using the same options for humans and models standardises the scoring rule and does not establish measurement equivalence. The bank's factor structure and inter-item consistency are not reported.

## What comes next

Two things the pilot does not have. A control fixed before collection: a prompt with the same structure and no organizing principle, with a criterion set in advance for treating its displacement as negligible and a stated reading if it is not, so that the size of a framing shift can be read against it rather than against a framing chosen for holding still. Cross-cultural human samples: a model framed as a member of a population, scored on the same instrument against that population's reference-sample mean, with measurement invariance established first. The confirmatory study that followed this pilot uses a different instrument, and no crosswalk between the two exists; this pilot informs its design and underwrites no claim in it.

---

Analysis is stdlib-reproducible from the raw runs; figures regenerate from a single script. Responsibility for the work, and for any errors in it, is mine alone. Methodology was AI-assisted and that assistance is disclosed.

Declan Michaels | Cross-Cultural Alignment Study | moral-os.com
