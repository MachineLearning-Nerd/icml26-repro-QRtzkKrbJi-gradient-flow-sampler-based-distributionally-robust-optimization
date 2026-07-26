# Claim 1 — VERIFIED

## Exact claim

The v1 manuscript presents a common worst-case gradient-flow sampler and DRO
outer loop (Algorithms 1–2), with concrete WGF, WFR, SVGD, and RGO
instantiations (Algorithms 3–6). Source: Sections 3.2 and B.1–B.2, PDF pages
3–5 and 14–15, extracted lines 201–341 and 945–1079.

## Assumption audit

The eight-dimensional conformance instance uses
`loss(theta,y)=theta·y+0.35 sum(log(2 cosh(y_j)))`, `tau=0.8`, and
`epsilon=0.7`. Its sample Hessian is bounded by `0.35 I`; RGO's extra condition
holds because `tau < 1/L` (`0.8 < 2.85714`).

## Direct evidence

| Check | Result |
|---|---:|
| Algorithms executed | 1, 2, 3, 4, 5, 6 |
| WGF equation-(12) max transition error | 0 |
| SVGD score+repulsion max transition error | `8.67e-19` |
| WFR weight-sum error | 0 |
| WFR birth–death events in independent transition check | 72 |
| RGO acceptance rate | `0.75572` |
| RGO rejected proposals | 331 |
| Distinct injected defects rejected | 6/6 |
| Expected control exit | 1 |

Code: [all six algorithms](../../../evidence/claim_1/algorithms.py),
[independent checker](../../../evidence/claim_1/independent_checker.py),
[verifier](../../../evidence/claim_1/verifier.py), and
[negative control](../../../evidence/claim_1/negative_control.py).

Raw: [results JSON](../../../evidence/claim_1/raw_results.json),
[checker output](../../../evidence/claim_1/independent_checker_output.json),
and [control output](../../../evidence/claim_1/negative_control_output.json).

Contract and interpretation:
[claim contract](../../../evidence/claim_1/claim_contract.json) and
[source audit](../../../evidence/claim_1/source_audit.md).

## Reproducibility

Run `uv run --frozen --no-dev python -m reproduction.run_all` with Python
3.12 and the linked repository-level [`uv.lock`](../../../uv.lock). Evidence
SHA: `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`. Seeds are
`101–106`, `310–314`, and `401–404`, exactly enumerated in the raw JSON. The
HF `cpu-upgrade` job reported 64 logical CPUs; the verifier is single-process.
Claim-verifier runtime was 1.014116 s (8.479088 s for the cumulative suite).

## Verdict and limitation

**VERIFIED · HIGH confidence.** This establishes the exact constructive
framework claim and replaces the old WGF-only finite/std toy check. The smooth
fixture is a conformance test, not a CIFAR-10 experiment and not a convergence
proof.
