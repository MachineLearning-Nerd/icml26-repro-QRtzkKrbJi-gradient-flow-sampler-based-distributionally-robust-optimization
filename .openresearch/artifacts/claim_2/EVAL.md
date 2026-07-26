# Claim 2 evaluator record

Verdict: **FALSIFIED**

The exact necessary-time statement is contradicted by an admissible continuous
quadratic instance. Its initial law is a point mass while its Gibbs target has
variance `1/3`, so this is not the vacuous case where initialization already
equals the target. The gradient observable is odd and both its initial and
target expectations are exactly zero. Therefore the gradient tolerance is met
at time zero for every positive epsilon, whereas the stated lower-order term
is positive and diverges over the recorded tolerance sequence.

The counterexample satisfies the v1 assumptions and the stronger clarifications
in v3: loss smoothness 1, mixed-gradient Lipschitz constant 1, conditional
strong convexity 3, PL constant 6, and arbitrary sample count. The `theta=1`
control keeps those constants but requires positive time, proving the verifier
is sensitive to the intended property.

## Limitations and interpretation

- This falsifies the literal “needs ... at least” universal lower-time claim.
  It does not dispute the exponential convergence upper bound.
- The same algebra supports a sufficient-time guarantee. Replacing “needs at
  least” with “it suffices to run” would avoid this counterexample.
- The asymptotic notation `t ≳ O(...)` is itself nonstandard. The contradiction
  is robust to any positive multiplicative hidden constant because the exact
  required time remains zero while the displayed function diverges.
- Evaluator-visible publication and a blind traversal are still required
  before this scientific result can receive release credit.
