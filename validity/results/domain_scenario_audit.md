# Moral Domain — scenario/scoring audit

> **Decision (adopted): Option A, plus scenario curation.** Describe Moral Domain as the
> *reach of moral judgment over harmless behavior* (communitarian "uphold shared standards"
> ↔ libertarian "mind your business"), i.e. **applied** domain breadth, anchored in the
> confirmatory study to a harmless-taboo / victimless-acts measure rather than the MFQ. The
> reading is clean for the three baseline scenarios (domain_1–3, `has_human_baseline`) that
> produced the convergent result, but the full 12-scenario bank is heterogeneous (see §6):
> scenarios 4–12 also tap purity-breadth, complicity/scope, and authenticity. So Option A
> governs the current result, and the domain bank is flagged for curation before the
> confirmatory study. Pre-registered MFQ predictions are left unchanged; this reading
> supersedes their interpretation.

Prompted by the convergent-validity result, in which the Moral Domain axis returned a
null against the MFQ *binding* foundations (r = -0.06) and a strong, wrong-signed
correlation with MFQ *individualizing* (r = -0.70 vs. a predicted +). This audit asks
whether that is a scoring bug or something about the construct.

## 1. The scoring is correct — no bug

The dimension is defined with `pole_a = Broad` ("morality includes purity, loyalty,
dignity, duty") and `pole_b = Narrow` ("morality covers harm and fairness only"). In the
scenarios, broad-reading options carry `pole = -1`, narrow-reading options carry
`pole = +1`, and the dimensional score is a weighted average of option poles — so a
higher score means *narrower*. That is exactly the convention the axis file and the
convergent-validity script assume (higher = narrow). There is no sign flip and no
mis-key. The failure is not mechanical.

## 2. But "narrow" is operationalized as libertarian withdrawal, not foundation-pruning

Reading the domain scenarios, every one pits a community/tradition/purity concern
against a "no one was harmed, so leave it alone" response. The narrow-pole options are
consistently libertarian: *"what he does privately is outside the scope of anyone else's
moral concern," "a business can serve whatever it chooses — customers will decide,"
"participation in traditions is a personal choice, not a moral obligation."* So the axis,
as built, measures **how far moral judgment should reach into behavior that harms no
one** — a libertarian↔communitarian dimension — more than it measures *which* moral
foundations a respondent admits.

That distinction is the whole ballgame. The pre-registered prediction ("narrow → high
individualizing") assumed that narrowing the domain *concentrates* moral energy onto harm
and fairness. But the scenarios operationalize narrowing as *withdrawing* moral judgment
altogether ("it's not a moral matter"). Those are different things, and they predict
opposite MFQ patterns.

## 3. The anomaly is robust, and coherent under the libertarian reading

The Domain↔individualizing correlation of -0.70 is stable under leave-one-out
([-0.78, -0.58]); it is not an outlier artifact. It is also coherent once you look at how
the MFQ individualizing items are worded: care and fairness on the MFQ are *interventionist*
("cared for someone weak or vulnerable," "compassion for the suffering is the most crucial
virtue," "justice is the most important requirement for a society," rights and equality).
A model at the libertarian/"leave-alone" pole is anti-interventionist, so it rates those
active-obligation items *lower* — pulling individualizing down, not up. The prediction was
mis-theorized; the data are behaving sensibly.

The Domain↔binding correlation, by contrast, is a genuine null (-0.06, unstable under
leave-one-out, [-0.31, +0.25]). This is itself a discriminant finding: declining to impose
community standards on harmless behavior is *not* the same as personally rejecting the
binding foundations. A model can say "leave the man to his private hobby" while still
endorsing loyalty, authority, and sanctity on the MFQ. So the axis does not track
foundation breadth the way its "broad vs narrow foundations" label implies.

## 4. Discriminant note: Domain moves with Scope (+0.51)

Among the four axes, Domain's largest inter-axis correlation at neutral is with Obligation
Scope (+0.51). Both are markers of a liberal-individualist outlook — universal obligations
plus a hands-off stance toward private/community morality — so they co-vary. Worth watching
for discriminant validity, though 0.51 is far from redundant.

## 5. Compression caveat (applies to the whole model-panel pass)

At neutral framing all four axes are compressed to sd ≈ 0.06 across the 11 models — the
documented neutral-compression effect. So the *magnitudes* and any significance claims from
the model panel are not trustworthy at n = 11. What survives is the *sign pattern*, which
leave-one-out shows is stable for the axes that matter (Authority, Scope, and this Domain
result). The decisive convergent test remains the human confirmatory sample, where
dispositional spread is real rather than compressed.

## Verdict and options

The Moral Domain axis is not mis-scored and its anomalous convergent result is real and
interpretable: the axis measures the **reach of moral judgment over harmless private and
communal behavior** (libertarian↔communitarian), which is a coherent construct — just not
the MFQ individualizing/binding *breadth* the pre-registration mapped it onto.

Two ways forward, and this is a scientific-framing call:

- **(A) Keep the axis, fix the analog.** Describe Moral Domain as the reach of moral
  judgment (libertarian↔communitarian), and in the confirmatory study test it against a
  purpose-built measure of that — moralization of harmless-taboo/victimless acts, or a
  liberty/communitarian scale — rather than MFQ individualizing. This is the most honest
  description of what the axis already does, and it turns the -0.70 from an embarrassment
  into a predicted result.

- **(B) Restore the original intent.** If Domain is meant to measure *which foundations
  count* (individualizing vs binding), the scenarios need rebalancing to separate two things
  they currently entangle: "should the community intervene in harmless behavior?" (liberty)
  from "do purity/loyalty violations count as moral at all?" (breadth). That is a
  scenario-authoring project, not a scoring fix.

Recommendation: **(A)**. The axis is measuring something real and stable; the cleaner move
is to name it accurately and predict against the right external construct, not to force it
back onto the MFQ breadth mapping it has now twice declined to fit.

## 6. Does the reading hold across all 12 domain scenarios? Only for the baseline three

The convergent Domain score (`b12`) uses only the three `has_human_baseline` scenarios —
domain_1, domain_2, domain_3 — and those are unambiguously the reach/mind-your-business
contrast (a private hobby neighbors find improper; refusing family traditions; a restaurant
disrespecting neighborhood custom). So the -0.70 rests cleanly on the reach construct.

Rescoring Domain on all twelve scenarios (`all48`) dilutes the pattern rather than
overturning it: Domain x MFQ individualizing weakens from -0.70 to -0.46, and Domain x MFQ
binding drifts from -0.06 to +0.12. Reading scenarios 4-12 explains the dilution — the fuller
bank is heterogeneous and taps at least four distinct contrasts:

- **Reach / mind-your-business** (clean): domain_1, 3, 6, 8.
- **Purity-breadth** (does a harmless impurity count as moral?): domain_7, 8, 11 — the original
  "which foundations count" construct; these push binding upward on the full set.
- **Complicity / scope-of-responsibility** (exploitative supply chains; the un-sharing rich
  villager): domain_5, 9, 12 — overlap Obligation Scope, consistent with Domain x Scope = +0.51.
- **Authenticity / self-expression** (empty mourning ritual; modest dress): domain_10, 11 — the
  "narrow" pole here is "performing without genuine feeling is dishonest," which is Moral Agent
  territory, not "leave them alone."

So the reach reading is the dominant theme and is clean for the baseline scenarios that carry
the validated result, but the domain bank as a whole is a blend. This is not a scoring defect;
it is construct heterogeneity, and it is what inflates Domain's overlap with Scope and Moral
Agent. Before the confirmatory study, the domain scenarios should be curated to whichever
construct is chosen (reach-of-judgment vs foundation-breadth), keeping only the scenarios that
measure it — a targeted revision of scenarios 4-12, not a wholesale rewrite.
