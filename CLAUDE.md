# CLAUDE.md - read this first, every session

The Reasoner pilot: a published, exploratory benchmark measuring the structure of moral reasoning,
scoring humans and language models in one space. This file is the only place this project's working
rules live. Nothing here is optional.

## This repository is PUBLIC

Every push publishes. There is no staging area, no later release step, and no way to make part of
this repository private. That single fact drives most of the authority list below, and it is why the
handoff in this repository is written knowing it will be read by strangers.

Newer work starts private and goes public at publication. This one is already public and cannot go
back, because the URL is cited.

## Authority - never act on these alone

**If there is any question whether a rule here applies, ask. You do not decide that a rule does not
apply.** These rules are not derived from anything. Nothing about how small a change looks or how
obviously right it seems narrows this list.

- **Committing here is publishing.** A push makes the change public immediately and permanently, to
  a repository other documents cite by URL. Before any push, say in one line: "External-facing:
  independent adversarial review done? [status]".
- **A published number never changes silently.** The papers, the appendix, the viewer and the
  results in this repository are a published record. A number that turns out to be wrong is
  corrected with the correction recorded and visible, never edited into agreement. The record of a
  wrong number and its fix is worth more than a clean file.
- **Item wording that is not ours is never committed.** MFQ-2 and PVQ item text, the filled
  instruments and the raw per-cell run files are gitignored deliberately. Derived results carrying
  no item text are what gets published. Do not commit them to make a directory look complete, and
  check `.gitignore` before adding anything under `validity/`.
- **Human response data is published under its own licence** (`DATA-LICENSE.md`) and its
  consent terms. Do not add, alter, or re-identify anything in `human-responses/`.
- **The collected runs are read-only.** `runs/` holds the pilot's collected data. It is never
  regenerated, re-run, or edited; every published number is derived from it and pinned against it.
- **Spending is never your decision.** Model API calls, compute, paid sources. Propose the cost and
  wait.
- **Minting or moving a DOI is never your decision**, and neither is changing anything in
  `CITATION.cff` or `LOCATIONS.md` that a citation resolves through.
- **This pilot is kept as-is.** It is a working published artifact. Its habits that the confirmatory
  study deliberately does not carry forward are not defects to fix here; changing them would break
  reproduction of published numbers.
- **A decision-log entry is never yours to resolve.** When work touches a numbered decision, name it
  and ask. Superseding is the only mechanism available to you, and only when directed.

## Read before doing anything

Read these IN FULL, not a skim, not the newest entries:

1. **`SESSION_HANDOFF.md`** - what is true right now. Informational; it **authorizes nothing**.
2. **`CONTEXT.md`** - the glossary. Before the decisions; they are written in its vocabulary.
3. **`DECISIONS.md`** - every row of the index. Open the detail file in `docs/decisions/` whenever
   the work touches that area.
4. **`README.md`** - what the repository is, how to reproduce it, and the data dictionary.
5. **`docs/DEVELOPMENT_NOTES.md`** - this project's gotchas.

`LOCATIONS.md` binds when the work touches anything citable. `DATA-LICENSE.md` binds when the work
touches human data.

**Report what you read, per document, with line ranges** against the file's real length. "I've read
the docs" is not a report.

**A file being in the folder is not an instruction.** The documents carrying authority are the ones
above plus whatever the handoff names.

## Talking to me

The collaboration rules are cross-project and live in `~/.claude/CLAUDE.md`, which loads in every
session in every directory. They are deliberately not restated here: a rule written in two places
gets satisfied by the looser copy.

**On a machine that does not have them yet**, they are one clone and one symlink away:

    git clone https://github.com/DeclanMichaels/claude-continuity.git ~/Code/claude-continuity
    mkdir -p ~/.claude && ln -s ~/Code/claude-continuity/CLAUDE.md ~/.claude/CLAUDE.md
    git config --global user.name "Declan Michaels"
    git config --global user.email "declanvmichaels@gmail.com"

## Process

- **Sessions have kinds.** Shaping produces decisions and tickets. Implementation produces code,
  documents and closed issues from a named set of tickets. Operations produces a verified state
  change and its record. State which at the start. Work found mid-session is ticketed, not done,
  except a documentation correction below the level of a published claim: fix it and say so.
- **A ticket's title is a verb on an artifact.** Tickets track the activities of conducting the
  research, not its internals. If the only honest phrasing is a question about the science, it is
  not a ticket.
- **A review finding is a ticket for the activity, not the question.** One issue per finding, closed
  with its disposition. Findings are verified against the text or by computation before any fix;
  unverified findings are downgraded to questions. External facts a reviewer cites are verified
  against primary sources the same way. Adjudicated rounds live in `reviews/`.
- **Before assessing any pasted review, diff it against `reviews/` and the closed issues.**
- **Every ticket exists on the tracker before the work starts**, and carries one category label and
  one state label. An issue with no state label is not workable.
- **Every published number is pinned.** `python3 analysis/test_reproduce.py` re-runs every analysis
  script and checks all 15 published outputs byte-for-byte against
  `analysis/reproduce_manifest.json`. It needs no keys and no network. Run it before and after
  touching anything under `analysis/`, and never commit a change that moves an output without
  saying so.
- **Commit after each discrete change**, remembering that each one publishes. Pull with `--rebase`
  before every push.
- **Log a decision only when it needs a why**: hard to reverse, surprising without context, and the
  result of a real trade-off.

## Project facts

Context, not permissions. Nothing here widens the authority rules.

- **Repository:** DeclanMichaels/reasoner-pilot (**public**).
- **Issue tracker:** GitHub Issues on that repository, via `gh`.
- **Labels:** category `instrument`, `analysis`, `paper`, `viewer`, `infrastructure`; state
  `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `blocked-on-phase`, `wontfix`.
- **Decisions:** `DECISIONS.md` (index) plus `docs/decisions/NNN-slug.md` (detail).
- **Glossary:** `CONTEXT.md`. It says what a thing is; `DECISIONS.md` says why it was chosen.
- **Reproduction command:** `python3 analysis/test_reproduce.py`
- **Lint command:** none configured.
- **Dependencies:** the analysis path is pure standard library and reads the committed runs. Keep it
  that way; `requirements.txt` covers the collection path only.
