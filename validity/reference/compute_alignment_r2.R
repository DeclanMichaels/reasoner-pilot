#!/usr/bin/env Rscript
# Per-foundation measurement-invariance alignment R2 for the MFQ-2 across the 19 Study-2
# countries, following the procedure of Atari et al. (2023) Code_Study2.R (osf.io/vwrpn); appendix B2a
# reports the residual against their published figures. For each
# foundation, fit a configural CFA per country and run Muthen-Asparouhov alignment
# (sirt::invariance.alignment, align.scale=c(.2,.4), align.pow=c(.25,.25)), then read
# es.invariance["R2",]: loadings = metric invariance, intercepts = scalar invariance.
# Scalar (intercept) R2 governs cross-country MEAN comparability.
#
# VERSION PIN (matters): sirt 3.13-228 (2023, paper era). sirt 4.x has a regression in the
# es.invariance R2 (nonsensical for most foundations; Care still computes and matches 3.13,
# cross-validating the pipeline). lavaan required for the per-group CFA.
#   install.packages("https://cran.r-project.org/src/contrib/Archive/sirt/sirt_3.13-228.tar.gz", repos=NULL, type="source")
#   install.packages("lavaan")
# Raw microdata NOT shipped (osf.io/9dwzt). Download, then: Rscript compute_alignment_r2.R Study_2_raw_dat.csv
suppressMessages(library(sirt))
args <- commandArgs(trailingOnly=TRUE)
path <- if (length(args) > 0) args[1] else "Study_2_raw_dat.csv"
d <- read.csv(path, stringsAsFactors=FALSE); grp <- d$country
items <- list(
  care=c("care1","care3","care11","care12","care13","care14"),
  equality=c("equalFairness6","equalFairness10","equality2","equality4","equality6","equality10"),
  proportionality=c("propFairness1","propFairness3","proportionality5","proportionality9","proportionality12","proportionality17"),
  loyalty=c("loyalty5","loyalty6","loyalty12","loyalty13","loyalty14","loyalty16"),
  authority=c("authority6","authority8","authority11","authority14","authority18","authority20"),
  purity=c("purity2","purity3","purity6","purity9","purity13","purity17"))
cat("foundation,R2_loadings,R2_intercepts\n")
for (f in names(items)) {
  par <- invariance_alignment_cfa_config(dat=as.matrix(d[, items[[f]]]), group=grp)
  mod <- invariance.alignment(lambda=par$lambda, nu=par$nu, align.scale=c(.2,.4), align.pow=c(.25,.25))
  r2 <- mod$es.invariance["R2",]
  cat(sprintf("%s,%.4f,%.4f\n", f, r2["loadings"], r2["intercepts"]))
}
