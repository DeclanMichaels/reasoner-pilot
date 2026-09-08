# 017 - Published means a DOI and moral-os.com, and drafts do not cite earlier drafts

**Date:** 2026-09-08
**Status:** active

## The decision

A document is published when it has a DOI and is on moral-os.com. Until then it is a draft, however
public the repository holding it. The papers refer to no earlier draft of themselves: no "an earlier
draft said", no errata section describing what a previous version reported, no pointer to the commit
that last carried a withdrawn figure. Corrections to a draft are recorded where the record already
lives - the commit message, the decision log and the tracker - and the draft simply says what is now
true.

This entry governs references between drafts. It does not loosen anything pinned: the fifteen pilot
outputs and the seventeen validity outputs stay pinned under decision 14 and `CLAUDE.md`, and a
pinned number still moves only with its reason recorded.

## Why

This repository is public, so "public" and "published" had run together. The appendix acquired an
errata section, B10, describing a test family that no reader outside this workflow had seen, and the
paper acquired "an earlier draft said the data did not exist". Both describe a publication history
that does not exist and charge every reader for it. The history is fully recorded already, in
`d441f7c`, decision 15 and issue #18, where someone who wants it can find it.

Raised by DeepSeek's review of 2026-09-08, which read the earlier-draft sentence as a reference to a
published document.

## Rejected alternatives

**Keep errata sections in drafts**, decision 15's B10. Rejected as redundant with the record and
misleading about what was ever published.

**Treat every push as publication.** Rejected: it would freeze a draft's numbers at each push, which
is the opposite of what a draft is for, and the never-changes-silently rule already has its object.

## Consequences and gotchas

B10 is struck from the appendix and its emitter. The `[d12]` and `[*]` markers in B3 stay: they point
to a decision and a caveat, not to a draft.

The pilot paper is on moral-os.com and its DOI is still `TBD` in `LOCATIONS.md`. Under this
definition it is not yet published either. Its numbers are pinned regardless, by decision 14; the
definition changes nothing about them and this entry says so above.

## Supersedes / amends

Amends #15: supersedes its clause that "the current B4 is kept as errata, the way decision 11 kept
the old English comparator". Decision 11's mechanism was a data cell, `en_neutral_ours`, and stands;
decision 15's errata section was a document reference and is withdrawn. The rest of #15 stands in
force.
