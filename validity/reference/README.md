mfq2_country_means.csv is a COPY. Owner: reasoner-study/instruments/MFQ-PVQ/mfq/reference/,
which builds it from Atari et al. 2023 Study 2 raw data (osf.io/9dwzt). Do not edit here;
re-copy when the owner changes. Repo-boundary rule, 4_toolbox.md Paths.

mfq2_country_dispersion.csv is a COPY of the same owner's file, taken 2026-09-08: per-country
person-level SDs for the six foundations and the binding composite, same respondents and scoring as
the means file. The binding composite's SD is not recoverable from the means file (it needs the
covariances among the three foundations), and the paper's distances-in-human-SDs table rests on it.
Same rule: do not edit here; re-copy when the owner changes.

mfq2_alignment_r2.csv is a COPY of the same owner's file, taken 2026-09-08: per-foundation
Muthen-Asparouhov alignment R-squared across the nineteen, loadings and intercepts, from
compute_alignment_r2.R (sirt 3.13-228). Appendix B2a is generated from it. Same rule.

mfq2_iran_dispersion.csv is BUILT HERE, 2026-09-08, by build_iran_dispersion.py from the two
respondent-level SPSS files Hazrati, Nejat and Daneshi (2025) share on their view-only OSF project
(zt3u2, the link in anchors_iran.json). The files stay in the gitignored _raw/. Scoring follows
the authors' own composites, verified against their precomputed foundation columns to 0.0000;
the published Table 2 means are reproduced as means of item means to 0.005. Binding SD is the
sample SD over respondents with complete binding items: sample 1 n=376, sample 2 n=988. The
builder needs pyreadstat and is not on the reproduce path; only its CSV is read by the appendix.
