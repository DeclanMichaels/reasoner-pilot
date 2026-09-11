# 023 - The Zenodo deposit is the repository snapshot, and both documents cite it

**Date:** 2026-09-11
**Status:** active

## The decision

One Zenodo deposit: the repository at the publication commit, as `LOCATIONS.md` describes, not the
two documents alone. The Reasoner pilot paper with its appendix and the MFQ-2 document publish
together and both cite that one DOI. Minting it remains Declan's act, after the pre-publication
pass in `SESSION_HANDOFF.md`.

## Why

Both documents claim reproduction from the committed runs, the ratings dataset and the harness. A
documents-only deposit would fix the prose and leave every such claim pointing at a repository
that can move; a snapshot fixes what the claims point at.

## Rejected alternatives

The documents alone, one deposit each; two snapshots, one per document, for one repository.

## Consequences and gotchas

`LOCATIONS.md`'s three `TBD`s and `CITATION.cff`'s commented `doi:` resolve together when the DOI
exists, and not before. Decision 17 still gates: published means the DOI and moral-os.com.
