# Claim-to-evidence audit

The six contracts below identify the exact v1 statement, its producer,
durable evidence, verdict, and boundary. They are not a claim that the paper
has one undifferentiated pass/fail result.

## C1 — Unified framework and Algorithms 1–6

The target is the structural framework and six concrete algorithm paths in
Sections 3.2 and Appendix B, including WGF, WFR, SVGD, and RGO.

Production path:

1. <code>published_space/evidence/claim_1/algorithms.py</code> implements the
   smooth eight-dimensional fixture.
2. <code>verifier.py</code> executes Algorithms 1–6 under recorded seeds.
3. <code>independent_checker.py</code> recomputes WGF/SVGD transitions and
   checks WFR mass conservation, birth/death, and an RGO envelope.
4. <code>negative_control.py</code> injects six omitted/reversed operations and
   requires each defect to be rejected.

The raw result and independent output pass. Verdict:
<strong>VERIFIED · HIGH</strong>. This is structural conformance, not a
convergence or CIFAR-10 performance proof.

## C2 — Proposition 1 necessary WGF time

The target v1 wording says that under its smoothness and gradient-dominance
assumptions, an epsilon-accurate gradient estimate needs positive WGF time of
the displayed order.

Production path:

1. <code>certificate.py</code> defines a continuous delta-initialized case and
   verifies smoothness, PL/gradient-dominance, non-warm-start, and the exact
   target oracle.
2. The initial and target gradient oracles are both zero at time zero.
3. The independent checker evaluates first-hit time over decreasing tolerances
   without deriving a horizon from the claimed formula.
4. A theta=1 control must produce a strictly positive first-hit time.

The admissible case reaches every positive tolerance at time zero while the
claimed lower scale is positive and increasing. Verdict:
<strong>FALSIFIED · HIGH</strong> for the universal v1 necessary-time contract.

## C3 — Theorem 1 outer iteration rate

The target v1 theorem claims constant-step outer-loop complexity
<code>O(epsilon_opt^-2)</code> under the listed assumptions and sampling
accuracy.

Production path:

1. <code>certificate.py</code> derives an exact one-dimensional Gaussian
   entropy-Wasserstein instance with exact sampler error zero.
2. The stochastic recurrence is solved symbolically; mean-square
   last-iterate stationarity forces a smaller step size.
3. <code>independent_checker.py</code> calibrates minimum horizons by
   optimizing the step size and searching the recurrence directly.
4. An antithetic zero-variance control must reject the lower-bound instance.

The exact instance requires
<code>Omega(epsilon_opt^-2 log(1/epsilon_opt))</code>. Verdict:
<strong>FALSIFIED · HIGH</strong> for the v1 contract.

## C4 — Theorem 2 total complexity

The target v1 theorem claims soft-<code>O(epsilon_opt^-4)</code> total
Algorithm 3 complexity under Assumptions 1–4.

Four independent routes are retained:

- <code>route_1_proof_audit.py</code> reconstructs the proof dependencies.
- <code>route_2_version_audit.py</code> compares v1 with the current source and
  author correction.
- <code>route_3_primary_sources.py</code> audits lower/upper-bound sources.
- <code>route_4_falsification.py</code> searches for a valid
  assumption-satisfying class-specific contradiction.

The routes identify unresolved proof/version issues but do not establish a
valid counterexample in the entropy-Wasserstein Algorithm 3 class. Verdict:
<strong>BLOCKED · LOW</strong>. The repository explicitly does not infer
falsification from a proof flaw alone.

## C5 — Strict CIFAR-10 Figure 6 dominance wording

The judged contract is stronger than the paper's qualitative phrase: WGF and
WFR must strictly beat Dual and WRM at every nonzero plotted attack setting
for all three entropy values.

Production path:

1. <code>vector_extractor.py</code> reads the authors' complete Figure 6 vector
   data from the pinned official-code/data provenance.
2. <code>independent_checker.py</code> enumerates every method, entropy, and
   nonzero perturbation setting, with a two-percentage-point margin criterion.
3. The raw counterexample bundle preserves the violating rows and the
   no-counterexample control.

There are 49 nonzero violations of the strict judged wording, including the
recorded <code>epsilon=0.2, Delta=0.008</code> WRM/WFR/WGF comparison.
Verdict: <strong>FALSIFIED · MEDIUM</strong>. The literal paper wording
“high degree of robustness” is qualitative and is not declared falsified by
this exact contract.

## C6 — Lemma 1 entropy-DRO/Schrödinger half-bridge identity

The target is a functional identity over the stated admissible measured
spaces, not a finite toy equality.

Production path:

1. <code>certificate.py</code> eliminates the free marginal, performs
   conditional disintegration, and reduces the integrand to the exact
   KL/Gibbs identity.
2. <code>independent_checker.py</code> checks normalization, stationarity,
   strict objective increases under feasible perturbations, and the raw
   generator over continuous non-Gaussian quartic cases.
3. A wrong-temperature Gibbs control must fail.

The symbolic residual is zero and the continuous checks pass with the
recorded machine-precision residuals. Verdict:
<strong>VERIFIED · HIGH</strong>. Numerical quadrature is an independent
regression layer; the functional certificate carries the claim.

## Orchestration and controls

<code>reproduction/run_all.py</code> validates the historical manifest, pinned
judge snapshot, all claim verifiers, and the evaluator-visible release audit.
The published-space verifier expects exactly
<code>{VERIFIED, FALSIFIED, FALSIFIED, BLOCKED, FALSIFIED, VERIFIED}</code>
for Claims 1–6 and fails closed on changed raw evidence or controls.
