# Claim 6 — VERIFIED

## Exact claim

Version-1 Lemma 1 states that the entropy-regularized DRO variational problem
is a Schrödinger half-bridge with fixed first marginal. Conditional
disintegration turns it into expected KL minimization, whose minimizer is the
conditional Gibbs density. Source: Section 3.1, PDF page 3 and Appendix C.1,
PDF page 16.

## Functional certificate

For sigma-finite measured spaces, fixed marginal `rho0`, `tau>0`,
`epsilon>0`, finite objective, and `0<Z_x<infinity`, the checker symbolically
reduces the conditional integrand to

`J_x(q)=a KL(q||p_x)-a log Z_x`, where `a=epsilon/(2 tau)`.

The symbolic integrand residual is exactly 0. Independent composite-Simpson
quadrature then checks four continuous, non-Gaussian quartic cases:

| Check | Worst/best observed value |
|---|---:|
| Maximum identity residual | `4.44e-16` |
| Maximum mass error | `2.22e-16` |
| Minimum unrelated-proposal KL | `0.15686` |
| Minimum nonzero perturbation objective gap | `0.00024184` |
| Wrong-temperature control stationarity span | `10.02857` |
| Expected control exit | 1 |

Code: [symbolic certificate](../../../evidence/claim_6/certificate.py),
[continuous checker](../../../evidence/claim_6/independent_checker.py),
[verifier](../../../evidence/claim_6/verifier.py), and
[control](../../../evidence/claim_6/negative_control.py).

Raw: [continuous cases](../../../evidence/claim_6/raw_results.json),
[checker output](../../../evidence/claim_6/independent_checker_output.json),
and [control output](../../../evidence/claim_6/negative_control_output.json).
Contract and source:
[claim contract](../../../evidence/claim_6/claim_contract.json) and
[source audit](../../../evidence/claim_6/source_audit.md).

## Reproducibility

Run `uv run --frozen --no-dev python -m reproduction.run_all` with Python
3.12 and the linked repository-level [`uv.lock`](../../../uv.lock). Evidence
SHA: `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`. Symbolic algebra and
fixed-grid quadrature are deterministic (seed: not applicable). The HF
`cpu-upgrade` job reported 64 logical CPUs; the verifier is single-process.
Claim-verifier runtime was 1.498278 s (8.479088 s cumulative).

## Verdict and limitation

**VERIFIED · HIGH confidence.** The proof certificate supplies the universal
functional argument. The continuous numerical cases are only independent
coefficient/sign regression checks, not the proof itself.
