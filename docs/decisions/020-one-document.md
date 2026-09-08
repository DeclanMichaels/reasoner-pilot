# 020 - The in-language report and its statistical appendix are one document

**Date:** 2026-09-08
**Status:** active

## The decision

`papers/inlanguage-mfq2-DRAFT.md` carries the report and, under an Appendix heading, every B
section. The generated sections are spliced into it by `validity/splice_appendix.py` from the two
pinned artifacts; the hand-written sections stay hand-written. There is no separate appendix file.

## Why

Two files sent for review as a pair came back reviewed as one, with findings that cited "the
appendix" against "the paper" and asked why a fact in one was not in the other. One document
removes the seam the reviewers kept catching on, and one splice script replaces the per-session
scripts that did the splicing by hand and twice half-did it (`19e35cf`, `6610467`).

## Rejected alternatives

Keeping the pair and cross-linking harder. The seam is the problem, not the links.

## Consequences and gotchas

Every "appendix B6a" reference in the report now points inside the same file and stays valid.
The splice script asserts each section header and each hand-written boundary before writing;
a header renamed in a generator fails the splice rather than silently leaving the old text.
Zenodo, when it comes, deposits one document.
