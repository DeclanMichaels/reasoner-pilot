#!/usr/bin/env python3
"""Splice the generated appendix sections into the combined document (decision 20).

    python3 validity/splice_appendix.py            # rewrite the document's generated sections
    python3 validity/splice_appendix.py --check    # exit nonzero if any section differs

The document is papers/inlanguage-mfq2-DRAFT.md. Its generated sections come verbatim from two
pinned artifacts: results/appendix_tables.md (B2a, B3 up to the hand-written Arabic subsection,
B3a, B6 up to the hand-written Care sentence, B6a) and results/appendix_b4_b5.md (B1a, B4, B5, B7).
B1, B2, B8, B9, the Arabic subsection and the Care sentence are hand-written and untouched.
Every header and hand-written boundary is asserted before anything is written; a renamed header
fails here rather than leaving stale text in place.
"""
import sys
from pathlib import Path

VDIR = Path(__file__).resolve().parent
DOC = VDIR.parent / "papers" / "inlanguage-mfq2-DRAFT.md"
TABLES = VDIR / "results" / "appendix_tables.md"
B4B5 = VDIR / "results" / "appendix_b4_b5.md"

# (artifact, section start, end of the section in the document, end of the section in the artifact)
PLAN = [
    (B4B5,   "## B1a. ", "## B2. ",                                 "## B4. "),
    (TABLES, "## B2a. ", "## B3. ",                                 "## B3. "),
    (TABLES, "## B3. ",  "### The three Arabic-speaking countries", "## B3a. "),
    (TABLES, "## B3a. ", "## B4. ",                                 "## B6. "),
    (B4B5,   "## B4. ",  "## B5. ",                                 "## B5. "),
    (B4B5,   "## B5. ",  "## B6. ",                                 "## B7. "),
    (TABLES, "## B6. ",  "Care sits between",                       "## B6a. "),
    (TABLES, "## B6a. ", "## B7. ",                                 None),
    (B4B5,   "## B7. ",  "## B8. ",                                 None),
]


def block(text, start, end, where):
    try:
        i = text.index(start)
        j = text.index(end, i + len(start)) if end else len(text)
    except ValueError as e:
        raise SystemExit("anchor not found in %s: %s" % (where, e))
    return i, j


def main(check):
    doc = DOC.read_text()
    arts = {p: p.read_text() for p in (TABLES, B4B5)}
    out, differs = doc, []
    for art, start, doc_end, art_end in PLAN:
        di, dj = block(out, start, doc_end, DOC.name)
        ai, aj = block(arts[art], start, art_end, art.name)
        new = arts[art][ai:aj].rstrip("\n") + "\n\n"
        if out[di:dj] != new:
            differs.append(start.strip())
        out = out[:di] + new + out[dj:]
    if check:
        if differs:
            print("  splice: %d generated section(s) differ from their artifact: %s" % (len(differs), ", ".join(differs)))
            return 1
        print("  splice: every generated section matches its artifact")
        return 0
    DOC.write_text(out)
    print("spliced %d sections into %s; %d changed" % (len(PLAN), DOC.name, len(differs)))
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
