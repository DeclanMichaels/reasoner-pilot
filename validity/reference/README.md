The human reference for the in-language MFQ-2 work: what each file is, where it comes from, and
which script builds it. Everything here is built from the sources' shared respondent-level data,
which stays in the gitignored _raw/ (item wording and microdata are not ours to redistribute,
decision 7); the aggregate CSVs are committed and are what the appendix reads.

Provenance: build_mfq2_means.py, build_mfq2_dispersion.py and compute_alignment_r2.R were written
in reasoner-study (instruments/MFQ-PVQ/mfq/reference/) and copied here on 2026-09-10 at its
commit 4f65f14 so this repository stands alone (#114). The means builder's default input path was
anchored to _raw/ in the copy and two header comments no longer say EXACTLY (#118); nothing else
differs. Both repositories build the same CSVs.

mfq2_country_means.csv: per-country foundation means and standard errors for Atari et al.'s
(2023) Study 2 nineteen countries, n per country. Built by build_mfq2_means.py from
_raw/Study_2_raw_dat.csv (osf.io/9dwzt; the authors' scoring code is osf.io/vwrpn), replicating
that code: the three attention checks as the inclusion rule, each foundation the mean of its six
items over respondents who answered all six. Rebuilt here 2026-09-10, byte-identical to the
committed file.

mfq2_country_dispersion.csv: per-country respondent-level SDs for the six foundations, the binding
composite (mean of Loyalty, Authority and Purity) and, since 2026-09-10, the Loyalty-Authority
composite (mean of the two), with each composite's mean; same respondents and scoring as the means
file, composites per respondent over those with all six foundations complete. The means builder
admits a respondent per complete foundation; every respondent the attention checks keep is
complete on all six, so both builders count the same 3,902 (n per country agrees). Built by
build_mfq2_dispersion.py. The composite SDs are not recoverable from the means file (they need
the covariances among the foundations); the paper's distances in human SDs rest on them.

mfq2_alignment_r2.csv: per-foundation Muthen-Asparouhov alignment R-squared across the nineteen,
loadings and intercepts, from compute_alignment_r2.R on the same raw file. R with lavaan and
sirt pinned to 3.13-228; sirt 4.x carries an es.invariance R-squared regression. Appendix B2a is
generated from it, beside the published figures below. Not on the python reproduce path.

mfq2_iran_dispersion.csv: built by build_iran_dispersion.py from the two respondent-level SPSS
files Hazrati, Nejat and Daneshi (2025) share on their view-only OSF project (zt3u2, the link in
anchors_iran.json), which stay in _raw/. Scoring follows the authors' own composite columns,
verified against their precomputed foundation columns to 0.0000; the published Table 2 means are
reproduced as means of item means to 0.005. Binding and Loyalty-Authority SDs are sample SDs over
the authors' own composite columns, so their inclusion rule applies: sample 1 n=376, sample 2
n=989. The builder needs pyreadstat (a scratch venv/, gitignored) and is not on the reproduce
path; only its CSV is read by the appendix. Loyalty-Authority columns added 2026-09-10.

mfq2_alignment_table6_published.csv is TRANSCRIBED HERE, 2026-09-08, from Table 6 of the accepted
manuscript of Atari et al. (2023), "The Measurement Invariance Alignment Results (Study 2)":
the authors' own loading and intercept R-squared and their percentage of non-invariant item
parameters per foundation. The table's note gives the criterion: 25 percent non-invariance or less
is acceptable (Muthen and Asparouhov, 2014). The text excepts Purity from the foundations meeting
it and says caution should be practiced when comparing Purity group-level means. Not a
computation; a record of what the source reports, read by B2a beside the recomputation in
mfq2_alignment_r2.csv.
