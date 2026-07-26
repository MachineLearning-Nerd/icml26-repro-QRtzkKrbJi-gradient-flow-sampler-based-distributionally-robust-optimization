# Claim 1 source audit

## Exact source

- Contract source: arXiv `2510.25956v1`, PDF SHA-256 `796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`.
- Retrieved 2026-07-26 with an explicit browser User-Agent.
- Algorithm 1: Section 3.2, PDF page 3, extracted lines 201-206.
- Algorithm 2: Section 3.2, PDF page 3, extracted lines 216-222.
- Algorithm 3: Section 3.2.1, PDF page 5, extracted lines 268-285; its location update is equation (12).
- Algorithm 4: Section 3.2.2, PDF page 6, extracted lines 341-366.
- Algorithm 5: Appendix B.1, PDF page 14, extracted lines 945-987.
- Algorithm 6 and its RGO prerequisites: Appendix B.2, PDF pages 15-16, extracted lines 999-1079.

## Quantifiers and assumptions

The claim is existential and constructive: the manuscript presents one common sampler/outer-loop framework and four named concrete instantiations, for six numbered algorithms total. It is not a universal convergence statement.

The WGF/WFR/SVGD algorithms target the conditional Gibbs law of the entropy-regularized Wasserstein problem. RGO additionally requires the loss to be globally `L`-smooth in the perturbed sample and `tau < 1/L`. The audit instance uses `L=0.35`, `tau=0.8`, and therefore `tau < 2.857142857...`.

## Version caveat

The live verdict's wording and algorithm numbering match v1. Current arXiv v3 changes theoretical results but retains the six-algorithm framework. This contract is deliberately fixed to the exact judged v1 source.

## Sign and scaling audit

The manuscript alternates between the loss-reward representation and the negative potential `V=-loss`. The implementation uses the equivalent conditional reward

`R(theta,x,y) = loss(theta,y) - ||y-x||^2/(2 tau)`

and target density proportional to `exp((2 tau/epsilon) R)`. Thus WGF uses `+ grad R`, SVGD uses the target score `(2 tau/epsilon) grad R`, and RGO minimizes the scaled negative potential `-(2 tau/epsilon)R`. This resolves the notation without changing the target law.
