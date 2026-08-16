# Branch audit

Branch names describe the evidence role of each preserved research line. They
do not imply that every branch independently proves the paper.

## Mapping

| Original public ref | Final public ref | Purpose |
| --- | --- | --- |
| <code>main</code> | <code>main</code> | Integrated publication surface |
| <code>orx/judged-4-of-12-baseline</code> | <code>baseline/judged-4-12</code> | Historical judged baseline |
| <code>orx/claim-1-six-algorithm-conformance-suite</code> | <code>audit/claim-1-algorithm-conformance</code> | Six-algorithm conformance |
| <code>orx/claim-2-necessary-time-counterexample</code> | <code>audit/claim-2-necessary-time</code> | Proposition 1 counterexample |
| <code>orx/claim-3-stochastic-outer-loop-lower-bound</code> | <code>audit/claim-3-outer-rate</code> | Theorem 1 rate counterexample |
| <code>orx/claim-4-four-route-complexity-audit</code> | <code>audit/claim-4-complexity</code> | Four-route blocked audit |
| <code>orx/claim-5-exact-figure-6-vector-falsification</code> | <code>audit/claim-5-figure-6</code> | Exact Figure 6 vector check |
| <code>orx/claim-6-continuous-half-bridge-certificate</code> | <code>audit/claim-6-half-bridge</code> | Functional identity certificate |
| <code>orx/evaluator-visible-cumulative-release-candidate</code> | <code>release/evaluator-visible</code> | Evaluator-visible release gate |

## Final invariants

- Default branch: <code>main</code>.
- Final public branch set: exactly the nine branches in the mapping.
- Old <code>master</code> and <code>orx/*</code> refs are absent.
- Main contains this paper-first README and the audit documents.
- Reachable commits use the canonical MachineLearning-Nerd identity.
- Exact final tips are recorded in the collection tracker after publication,
  because a commit cannot contain its own hash.
