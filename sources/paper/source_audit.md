# Paper source and quantifier audit

Retrieved 2026-07-26 with the explicit User-Agent recorded in
`source_manifest.json`.

## Contract version

The live judge's six claims match arXiv `2510.25956v1`, not the current v3.
This campaign therefore tests the exact v1 statements the judge scored while
also recording v3 as the current source. The ar5iv endpoint ignored explicit
`v1`, `v2`, and `v3` suffixes and returned the same v3 HTML hash for all three;
the versioned arXiv PDFs are therefore the authoritative versioned sources.

## Exact scopes

1. **Framework / algorithms.** Sections 3.2 and Appendix B define Algorithms
   1-6. Algorithms 3 and 4 instantiate entropy-regularized Wasserstein DRO with
   WGF and WFR respectively. This is an existence and conformance claim, not a
   performance theorem.
2. **Proposition 1.** For initial data samples, an L-smooth loss in the sampled
   variable, and a conditional energy satisfying gradient dominance with
   constant lambda > 0, v1 states that obtaining an epsilon-accurate gradient
   estimate requires a positive-time order involving lambda, L, and epsilon.
   The wording is universal over losses satisfying those assumptions and uses
   necessary-time language. Appendix C.2 derives it from a sufficient
   convergence bound; that direction must be audited.
3. **Theorem 1.** Under smoothness of the DRO objective, Lipschitz dependence
   of the parameter gradient on the sampled variable, bounded stochastic
   gradient variance, and W2 sampling error, v1 states that a constant outer
   step size of order 1/L_Phi and S = O(epsilon_opt^-2) suffice, provided the
   sampling error is O(epsilon_opt/L_f).
4. **Theorem 2.** Under Assumptions 1-4, v1 states a finite total Algorithm 3
   complexity scaling as epsilon_opt^-4 (up to a logarithm) with the displayed
   L_Phi, L_U, L_f, dimension, and LSI-constant factors.
5. **CIFAR-10.** Section 6.3 of v1 uses 512-dimensional features from an
   ImageNet-pretrained ResNet-50, multiclass logistic regression, feature-only
   L2 PGD, normalized perturbations from 0 to 0.08, 10 epochs, and 100 inner
   steps. Figure 6 spans three entropy values. The prose says WGF and WFR are
   robust across all settings; this is a full-dataset empirical claim.
6. **Lemma 1.** For the entropy-regularized JKO variational problem, the free
   first marginal can be eliminated to obtain a one-sided Schrödinger bridge.
   Conditional disintegration then yields an expected KL minimization and the
   conditional Gibbs worst-case distribution. This is a functional identity,
   so a finite toy comparison is insufficient.

## Version drift relevant to verdicts

Current v3 renumbers the half-bridge result as Proposition 3.1, replaces the
old outer theorem with Theorem 5.2 using an S-dependent step size, changes the
total bound to an epsilon_opt^-6 dependence in Theorem 5.5, and acknowledges a
flaw in the original proof that was later fixed. It also moves the original
CIFAR feature experiment to Appendix D.2 and adds end-to-end CIFAR-10
ResNet-18 experiments. These changes are evidence about the v1 contracts, but
they do not silently replace the contracts the live judge scored.

