# Claim 2 — FALSIFIED

## Exact claim

The live judged statement interprets Proposition 1 as a necessary positive WGF
runtime of order `(1/lambda) log(L/sqrt(lambda epsilon))` for an
`epsilon`-accurate gradient estimate. Source: v1 Section 4, Proposition 1 and
Appendix C.2.

## Assumption audit

The certificate uses `rho0=delta0`,
`loss(theta,y)=theta*y+y²/2`, squared transport cost, `tau=1/4`, and entropy
regularization `1/2`. At `theta=0`:

- loss smoothness and gradient-observable Lipschitz constant: 1;
- conditional energy strong convexity: 3;
- Wasserstein-PL constant: 6;
- initial-to-target `W2`: `1/sqrt(3)=0.577350`;
- all moments and normalizers are finite.

The gradient observable is `y`. Its expectation is exactly zero initially and
under the target Gaussian, so the first-hit time is exactly 0 for every
positive tolerance.

| epsilon | claimed positive scale | exact first-hit |
|---:|---:|---:|
| `1e-2` | `0.234451` | 0 |
| `1e-4` | `0.618215` | 0 |
| `1e-6` | `1.001979` | 0 |
| `1e-8` | `1.385743` | 0 |
| `1e-10` | `1.769508` | 0 |
| `1e-12` | `2.153272` | 0 |

The `theta=1` negative control starts with error `1/3`, first hits tolerance
`0.1` at `0.401324`, and exits 1 as expected.

Code: [certificate](../../../evidence/claim_2/certificate.py),
[checker](../../../evidence/claim_2/independent_checker.py),
[verifier](../../../evidence/claim_2/verifier.py), and
[control](../../../evidence/claim_2/negative_control.py).

Raw: [sweep](../../../evidence/claim_2/raw_results.json),
[checker output](../../../evidence/claim_2/independent_checker_output.json),
[control output](../../../evidence/claim_2/negative_control_output.json).
Contract and source:
[claim contract](../../../evidence/claim_2/claim_contract.json) and
[source audit](../../../evidence/claim_2/source_audit.md).

## Reproducibility

Run `uv run --frozen --no-dev python -m reproduction.run_all` with Python
3.12 and the linked repository-level [`uv.lock`](../../../uv.lock). Evidence
SHA: `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`. The proof, analytic Gaussian
flow, and numerical root are deterministic (seed: not applicable). The HF
`cpu-upgrade` job reported 64 logical CPUs; the verifier is single-process.
Claim-verifier runtime was 4.113555 s (8.479088 s cumulative).

## Verdict and limitation

**FALSIFIED · HIGH confidence.** The counterexample satisfies the displayed
assumptions and contradicts the universal necessary-time interpretation. The
appendix proves a sufficient upper time; an upper bound cannot imply the stated
lower necessity.
