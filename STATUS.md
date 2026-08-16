# Status — Gradient Flow Sampler-based Distributionally Robust Optimization

Last updated: 2026-08-16.

## Overall status

<strong>MIXED_RESULTS</strong>. The evidence-release gate passes. Claims 1 and
6 have high-confidence scoped verification; Claims 2, 3, and the strict
judged wording of Claim 5 are falsified; Claim 4 remains blocked after four
independent routes.

The exact v1 judged snapshot remains 4/12 at revision
<code>735012f52396955c5734e8fc568adfdf2abda757</code>. Forecasts in the
historical report are not new scores.

## Claim ledger

| ID | Verdict | Main evidence | Remaining boundary |
| --- | --- | --- | --- |
| C1 | VERIFIED · HIGH | Six algorithm paths, independent transition checks, WFR/RGO controls, and six rejected defect injections | Finite conformance does not prove convergence or performance |
| C2 | FALSIFIED · HIGH | Continuous assumption-satisfying counterexample has zero first-hit time for every positive tolerance | Applies to the universal necessary-time v1 wording; v3 changes the theorem |
| C3 | FALSIFIED · HIGH | Exact stochastic recurrence and independent horizon calibration force an extra logarithmic factor | Applies to the v1 constant-step <code>O(epsilon^-2)</code> contract |
| C4 | BLOCKED · LOW | Four routes expose proof/version issues but no valid class-specific contradiction | Needs a correct v1 proof or a valid Algorithm 3 lower-bound embedding |
| C5 | FALSIFIED · MEDIUM | Authors' complete Figure 6 vectors contain 49 strict-dominance violations | The paper's weaker qualitative phrase is not declared false |
| C6 | VERIFIED · HIGH | Universal functional certificate plus continuous independent checks | Numerical checks are regression; the certificate carries the functional claim |

## Reproduction gate

~~~bash
uv run --frozen --no-dev python -m reproduction.run_all
python3 verify_final.py
~~~

The first command runs the scientific suite and release audit. The second
checks repository identity, evidence files, claim contracts, source hashes,
final branch vocabulary, and commit attribution without rerunning experiments.

## Scope limits

- The six claim contracts target arXiv v1 because that is what the historical
  judge scored.
- v3 is recorded as current source context; it is not substituted into the v1
  verdicts.
- A falsified judged wording is not automatically a falsification of weaker
  qualitative prose.
- The blocked complexity claim is not promoted to falsified merely because
  another theorem or version changed.
- No author endorsement or score increase is claimed.
