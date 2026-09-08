# Development notes - this project's technical rules and gotchas

Durable working knowledge for anyone, human or agent, changing this repository: things that cost a
session if you do not know them, and that are not obvious from a quick read of the code.

**What belongs here:** technique that stays true across sessions. **What does not:** current state
(`SESSION_HANDOFF.md`), choices that need a why (`DECISIONS.md`), what a term means (`CONTEXT.md`),
rules about how to work (`CLAUDE.md`).

**If an entry here stops being true, fix or delete it.** A stale line reads as current.

## Repo and tooling

**This repository is public. Every commit publishes.** There is no staging step and nothing here is
revocable once pushed, because other documents cite the URL.

Reproduction: `python3 analysis/test_reproduce.py` re-runs every analysis script and checks all 15
published outputs byte for byte against `analysis/reproduce_manifest.json`. No API keys, no
network. Run it before and after touching anything under `analysis/`. Set `REASONER_ROOT` to point
the scripts at a copy of the tree living elsewhere.

The analysis path is Python standard library only and reads the committed runs. Only the collection
runner needs `requests`. Keep the analysis path dependency-free: a reader reproducing the published
numbers should need nothing but python3 and this clone.

Every build script raises on a duplicate complete cell, so a stray extra run cannot silently change
a number. If one raises, the cell is genuinely duplicated; do not work around it.

Scripts anchor with `Path(__file__).resolve().parent`. Two framed-analysis scripts once used
`Path(".")` and ran correctly only from `validity/`, which is invisible until someone runs them from
elsewhere.

Pushing from a non-interactive shell fails. The credential helper needs a terminal to unlock and
reports `could not read Username for 'https://github.com/...': Device not configured`. The commit
succeeds and only the push fails, which is easy to miss. `gh` is authenticated separately:

    git -c credential.helper='!gh auth git-credential' push origin main

## Running model panels

**Sampling temperature is never set and never recorded.** The runners send model, messages, a token
ceiling and a seed to five providers, and no temperature field; run records capture the seed only.
Every collection in this repository was therefore made at five different unrecorded provider
defaults, so run-to-run variance across models is not on a common footing and any figure computed
from it is partly measuring an unlogged parameter. A reviewer asked for the decoding parameters and
the honest answer was that we do not have them. Set it explicitly and write it into the run record
before any further collection.

**Preflight a handful of calls for across-rerun variance before paying for a multi-rerun run.** A
provider returning byte-identical output across distinct seeds is invisible in the output until you
look for duplicate rows, and reruns collected that way are pseudoreplicated with every interval
falsely narrow.

**Providers withdraw served models mid-programme.** Qwen and GLM dropped from the panel in July;
Kimi-K2.6 went off Together's serverless tier in August, returning HTTP 400 `model_not_available`
with a message directing to a dedicated endpoint. Verify against the live API rather than inferring
from the error text, and give the replacement its own roster key rather than reusing the old one.

Parse and rate-limit failures are expected at low rates and are retried inside the collection
window. In the in-language collection, 12 of 1,112 attempted calls returned no ratings object, all
retried to success, so no condition rests on fewer than five reruns.

API keys live in `~/.config/ccas/keys.env`, mode 600. A non-interactive shell does not have them:

    set -a && source ~/.config/ccas/keys.env && set +a

Never echo a value or write one into a script, a log or the repository. `.gitignore` excludes
`.env`, `*.key`, `*.pem` and `.aws-key*` as a backstop, not as the plan.

## What is not committed, and where it is

The convergent-validity module's filled instruments and raw per-cell run files are gitignored
because the item wording is not ours to redistribute. `validity/README.md` names the working copy
and the S3 archive prefix with the restore command. **Consequence:** the in-language appendix
numbers do not regenerate from a fresh clone until that data is restored, and
`analysis/test_reproduce.py` does not cover them.

`.gitignore` also excludes `*.smbdelete*`, residue from the retired SMB share. If those appear,
something is reading from dead infrastructure.

**Syncing the 2026-08-21 archive root into `validity/` overwrites tracked files.** `aws s3 sync <archive root> validity/`
restores the ignored run data and also writes the archive's versions of every tracked file it
contains. Run on 2026-09-05 it reverted five of them to their 2026-08-21 state, including
`audit_inlanguage.py`, which lost 162 lines and the matched English-baseline change that is
decision 11. The sync reports success and the tree looks restored. Check `git status` immediately
after any sync into `validity/` and `git checkout --` anything tracked that it touched. Tracked by
issue 3; `validity/reconcile.py` classifies a working copy against an archive before and after any
sync, and the documented recipe runs it.

**The 2026-08-21 archive does not cover the completed grid; the 2026-09-05 one does.** The prefix
root holds the 2026-08-21 snapshot: Arabic, Farsi and Japanese only, 929 objects, 14 conditions,
tracked files mixed in. `archive-reasoner-pilot-validity/2026-09-05/` holds the fifty-condition
grid: 2,690 data files, no tracked files, a sha256 manifest and a coverage note; the restore recipe
is in `validity/README.md`. A clean clone plus a restore from the root gives the three-language
family, and `audit_inlanguage.py` runs clean against it and reconciles, which makes the shortfall
easy to miss. Restore from the dated prefix. Issue 4.

**The audit scripts write tracked outputs, so running one against partial data corrupts the
published record.** Running `audit_inlanguage.py` on the restored three-language subset rewrote
`validity/results/condition_means.json` from 26 conditions to 11, dropping every Spanish, French
and Russian condition and three of the four Arabic ones. It exited clean and printed RECONCILED,
because it reconciles whatever it can see. Committed, that output would have reproduced perfectly
against itself. **Check `git status` after running anything under `validity/`, and treat a clean
exit as saying nothing about whether the right data was present.**

## The in-language appendix is generated, and the splice map is fixed

`papers/inlanguage-mfq2-appendix-DRAFT.md` is spliced verbatim from two artifacts. `build_appendix_tables.py`
emits B2a, B3, B3a, B6 and B6a; `audit_inlanguage.py` emits B1a, B4, B5 and B7. B1, B2, B8,
B9, the Arabic-four subsection inside B3 and the Care sentence after B6 are hand-written. A number
in the document that disagrees with its artifact is a splice that was not re-run; re-splice, do not
edit. `test_reproduce.py` pins the artifacts (decision 14), not the document.

`audit_inlanguage.py` loads every English-framed country since 2026-09-08. Before that it loaded
Egypt, Japan and Iran only, so `condition_means.json` carried 27 of 47 conditions and looked
complete.

**B1a quotes the prompts from the runner source.** The unframed system prompt is read from
`run_validity.py`'s `SYSTEM` literal and the framing template from `run_framed.frame_system`'s
AST. Change either runner and the appendix changes, or the emitter fails. A hand-copied version
was tried and failed its own assertion: the f-string is split across literals, and the copy had
swapped the em-dash the models actually receive.

**Copy the audit's stdout to `results/inlanguage_audit.txt` only from a run that printed
`wrote results/appendix_b4_b5.md`.** A run that fails partway leaves a truncated trail that
`test_reproduce.py` will happily re-pin.

**Multi-file edit scripts assert every anchor before writing any file.** A script that writes each
file as it goes and aborts on a later anchor leaves the earlier files changed and the later ones
not, and a commit that follows describes a change that half happened. That is how `695e173`
re-attributed the Iran caveat in the paper and nowhere else. The emitter's blocks are ordered
B7, B1a, then the write call; cut a block by its own two markers, never from a marker to the
write call.

**Never redirect a generator straight into its tracked output.** `python3 gen.py > results/x.md`
truncates the file at the point of a crash, and the splice, the pin and the harness all accept the
truncated file as the new truth; `19e35cf` pinned one. Write to a temp file, check the exit code and
the expected strings, then move it.

Replace a table row by its exact text, never by "the first line starting with". The paper has
three tables with a `| Farsi |` row; the #21 correction took the first and put a d-table row into
the language table, and two reviews that flagged it were refuted after the wrong table was checked.

A `%` inside a string that is later `%`-formatted raises `unsupported format character`; the
"95% model-resampling interval" header needs `%%` in the template.

## Human data

`human-responses/` is published under `DATA-LICENSE.md`. The `_server` block holding hashes of IP
and user agent was removed before publishing and plays no role in analysis; the retained `_meta`
block is coarse browser telemetry. Do not add to, alter, or attempt to re-identify anything here.

CSV exports anonymise respondents to sequential ids, `h01` onward, which are export-local and do not
correspond to the UUIDs across regenerations.

## Figures that are easy to get wrong

**Compression is 5.4 to 7.7 times, on eleven models and 68 humans**, with every ratio interval's
lower bound at or above 3.66. Older drafts say "three to four times", which was the lower-bound
reading presented as the estimate, and "five models", which is simply wrong. Both are corrected in
the paper and the appendix; if either phrasing turns up anywhere, it is stale.

**The in-language grid is fifty conditions and 2,750 cells.** `papers/inlanguage-mfq2-appendix-DRAFT.md`
still says eleven models, 20 conditions and 1,100 cells, which describes the earlier and smaller
collection it was written against. The appendix has not been regenerated since the grid completed.

**Human-to-model comparisons run on the baseline twelve**, the scenarios carrying
`has_human_baseline`. The other 36 are model-side only. A figure computed on all 48 and reported as
a human comparison is a category error.

## Findings that look like bugs and are not

**The panel's default sitting close to a population mean is not evidence the language moved it.**
The English neutral binding mean is 2.705 and the Japanese neutral mean 2.662 against a Japanese
human anchor of 2.65, so Japanese administration moves the panel by -0.04 and the English default
was already within 0.06. A default that happens to land near a population is not the language
carrying the population.

**Framed and unframed dispersion are not comparable.** Naming a country roughly halves between-model
spread by construction, so a contrast between a framed and an unframed agreement statistic is a
measurement property rather than a finding about the countries.

**The pilot's habits that the successor study abandoned are not defects here.** Three `axis_scores`
variants rounding differently, a shared RNG consumed top to bottom, the bespoke per-scenario answer
options. `reasoner-study/ENGINEERING.md` designs each of them out on purpose. Changing them here
would break reproduction of published numbers for no gain.
