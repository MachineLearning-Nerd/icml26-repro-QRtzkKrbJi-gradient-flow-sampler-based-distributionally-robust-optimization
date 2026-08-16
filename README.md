# Gradient Flow Sampler-based Distributionally Robust Optimization

Paper-first reproduction workspace and exact-claim audit for
[*Gradient Flow Sampler-based Distributionally Robust Optimization*](https://arxiv.org/abs/2510.25956)
by Zusen Xu and Jia-Jie Zhu.

This repository was previously named
<code>icml26-repro-QRtzkKrbJi-gradient-flow-sampler-based-distributionally-robust-optimization</code>.
Its normalized home is
<code>MachineLearning-Nerd/icml26-gradient-flow-sampler-distributionally-robust-optimization</code>.
The judged challenge record is
[OpenReview QRtzkKrbJi](https://openreview.net/forum?id=QRtzkKrbJi).

## What the paper does

The paper proposes a PDE gradient-flow framework for sampling worst-case
distributions in distributionally robust optimization (DRO). It specializes
the framework to six algorithms, including Wasserstein Gradient Flow (WGF),
Wasserstein Fisher–Rao flow (WFR), SVGD, and restricted Gaussian sampling
variants. It also studies a gradient-flow outer loop, a total-complexity
bound, CIFAR-10 robustness experiments, and an entropy-regularized
Wasserstein/Schrödinger half-bridge identity.

## Version boundary and current status

The live judge scored the exact arXiv <strong>v1</strong> contract. The
repository pins v1 for the six claim audits and records v2/v3 separately;
the current v3 changes several theorem numbers and rates. The scientific
status below is therefore about the named v1/judged contracts, not an
unqualified statement about every later version.

| Claim | Exact target | Verdict | Evidence boundary |
| --- | --- | --- | --- |
| C1 | Unified framework and Algorithms 1–6 | VERIFIED · HIGH | All six structural paths, independent transitions, WFR mass controls, RGO envelope, and six defect controls pass; finite conformance is not a convergence proof |
| C2 | Proposition 1 positive necessary WGF time | FALSIFIED · HIGH | An assumption-satisfying continuous case has zero first-hit time for every tolerance; applies to the universal necessary-time contract |
| C3 | Theorem 1 <code>O(epsilon^-2)</code> outer iterations | FALSIFIED · HIGH | An exact stochastic recurrence requires <code>Omega(epsilon^-2 log(1/epsilon))</code>; the counterexample has exact sampling error zero |
| C4 | Theorem 2 soft-<code>O(epsilon^-4)</code> total complexity | BLOCKED · LOW | Four proof/version/source/falsification routes completed; no valid class-specific counterexample or corrected v1 proof |
| C5 | Strict all-setting CIFAR-10 dominance in the judged wording | FALSIFIED · MEDIUM | The authors' complete Figure 6 vector data contain 49 nonzero violations; the paper's weaker qualitative prose is kept distinct |
| C6 | Lemma 1 entropy-DRO/Schrödinger half-bridge identity | VERIFIED · HIGH | Universal symbolic functional certificate plus independent continuous normalization, stationarity, and perturbation checks |

Overall status: <strong>MIXED_RESULTS</strong>. The evidence-release gate
passes, but Claim 4 remains unresolved and the exact C5 verdict is scoped to
the stronger judged wording. The historical live score is 4/12; this
repository claims no new judge score or author endorsement.

## How each claim is produced

The fixed cumulative entry point is:

~~~text
reproduction/run_all.py
  -> historical manifest and judged-verdict snapshot
  -> published_space/evidence/claim_1..claim_6/verifier.py
  -> release/audit_candidate.py
  -> fail-closed cumulative summary
~~~

| Claim | Production path | Durable evidence |
| --- | --- | --- |
| C1 | <code>published_space/evidence/claim_1/verifier.py</code> runs the six-algorithm fixture, independent transition checker, WFR/RGO checks, and six negative controls | <code>published_space/evidence/claim_1/</code>, raw results, independent output, and canonical Claim 1 page |
| C2 | <code>claim_2/certificate.py</code> proves the continuous counterexample assumptions and <code>claim_2/independent_checker.py</code> checks normalization, zero first-hit times, and the nonzero control | <code>published_space/evidence/claim_2/</code> and Claim 2 page |
| C3 | <code>claim_3/certificate.py</code> derives the exact stochastic recurrence and <code>claim_3/independent_checker.py</code> calibrates minimum horizons without using a formula-derived horizon | <code>published_space/evidence/claim_3/</code> and Claim 3 page |
| C4 | <code>claim_4/route_1_proof_audit.py</code>, <code>route_2_version_audit.py</code>, <code>route_3_primary_sources.py</code>, and <code>route_4_falsification.py</code> independently audit the unresolved complexity claim | <code>published_space/evidence/claim_4/</code>, route outputs, and Claim 4 page |
| C5 | <code>claim_5/vector_extractor.py</code> extracts the authors' full Figure 6 vectors and <code>claim_5/independent_checker.py</code> checks strict dominance and controls | <code>published_space/evidence/claim_5/</code>, vector audit, and Claim 5 page |
| C6 | <code>claim_6/certificate.py</code> performs the functional algebra; the independent checker runs continuous quadrature and wrong-temperature controls | <code>published_space/evidence/claim_6/</code> and Claim 6 page |

The evaluator-visible subset is checked by
<code>release/audit_candidate.py</code>, which also verifies navigation,
historical preservation, upload hashes, and a secret scan.

## Repository contents

- <code>published_space/</code> — evaluator-visible current evidence, claim pages, release manifest, and cumulative verifier
- <code>space_candidate/</code> — staged mirror used by the release audit
- <code>reproduction/</code> — fixed repository-level campaign entry point
- <code>historical/</code> — immutable 4/12 judged baseline
- <code>sources/paper/</code> — v1/v2/v3 source contract and provenance
- <code>sources/judge/</code> — pinned historical judge verdict
- <code>reports/reproduction/</code> — technical report and generated figures
- <code>notebooks/gfs_dro_reproduction.py</code> — bounded interactive tutorial
- <code>third_party/GFS-DRO/</code> — explicitly attributed official-code provenance
- <code>paper_2510.25956v1.pdf</code>, <code>paper_2510.25956v3.pdf</code>, and <code>source/arxiv/2510.25956v1.tar</code> — pinned paper artifacts

## Final branch vocabulary

The old <code>orx/*</code> names are mapped to descriptive evidence roles:

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| <code>main</code> | <code>main</code> | Integrated paper-first publication surface |
| <code>baseline/judged-4-12</code> | <code>orx/judged-4-of-12-baseline</code> | Immutable historical judged baseline |
| <code>audit/claim-1-algorithm-conformance</code> | <code>orx/claim-1-six-algorithm-conformance-suite</code> | Six-algorithm structural audit |
| <code>audit/claim-2-necessary-time</code> | <code>orx/claim-2-necessary-time-counterexample</code> | Proposition 1 counterexample |
| <code>audit/claim-3-outer-rate</code> | <code>orx/claim-3-stochastic-outer-loop-lower-bound</code> | Theorem 1 rate counterexample |
| <code>audit/claim-4-complexity</code> | <code>orx/claim-4-four-route-complexity-audit</code> | Four-route blocked complexity audit |
| <code>audit/claim-5-figure-6</code> | <code>orx/claim-5-exact-figure-6-vector-falsification</code> | Exact Figure 6 vector audit |
| <code>audit/claim-6-half-bridge</code> | <code>orx/claim-6-continuous-half-bridge-certificate</code> | Functional half-bridge certificate |
| <code>release/evaluator-visible</code> | <code>orx/evaluator-visible-cumulative-release-candidate</code> | Evaluator-visible cumulative release |

The complete mapping and final branch invariants are in
[BRANCH_AUDIT.md](BRANCH_AUDIT.md). No public <code>master</code> or
<code>orx/*</code> branch remains after normalization.

## Reproduce

Requirements are Python 3.12 and uv. The lockfile is authoritative.

~~~bash
uv sync --frozen
uv run --frozen --no-dev python -m reproduction.run_all
~~~

The command is CPU-only in the recorded campaign and runs all six claim
verifiers plus the evaluator-visible release audit. It fails closed on any
claim result, independent checker, negative control, historical hash, or
release-manifest mismatch. The historical 4/12 snapshot is preserved and is
not silently replaced by the current mixed-result evidence.

## Citation

Please cite the paper for its mathematical and algorithmic results and cite
this repository when using the audit artifacts. A machine-readable citation
is in [CITATION.cff](CITATION.cff).

~~~bibtex
@article{xu2025gradient,
  title         = {Gradient Flow Sampler-based Distributionally Robust Optimization},
  author        = {Xu, Zusen and Zhu, Jia-Jie},
  year          = {2025},
  journal       = {arXiv preprint arXiv:2510.25956},
  doi           = {10.48550/arXiv.2510.25956}
}
~~~

## Thank you

Thank you to Zusen Xu and Jia-Jie Zhu for making the paper, its mathematical
framework, and the associated implementation/data provenance available for
inspection. The authors' exact Figure 6 vectors and the paper's detailed
functional formulation made it possible to distinguish structural,
theoretical, and empirical claims instead of reducing them to toy checks.

This is independent work by MachineLearning-Nerd. The verdicts are scoped to
the contracts documented here and do not imply author review, endorsement, or
agreement with the audit.

See [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) for the longer note.
