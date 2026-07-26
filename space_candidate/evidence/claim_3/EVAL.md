# Claim 3 evaluator record

Verdict: **FALSIFIED**

An exact one-dimensional entropy-Wasserstein DRO instance satisfies every v1
assumption, including an exact inner sampler, while its best possible
constant-step last iterate needs
`Omega(epsilon^-2 log(1/epsilon))` stochastic-gradient iterations. The
counterexample is proof-level: the Gibbs target, log partition, recurrence,
and lower bound are algebraic. Continuous quadrature and independently
optimized first-hit searches are regression checks.

The previous d=4 experiment and slope `-0.289` neither verified nor falsified a
universal upper bound and remains historical rejected evidence. This result
instead directly contradicts the exact quantifier on an admissible instance.

## Limitations and interpretation

- The falsification applies to v1 Theorem 1 as judged. Current v3 replaces it
  with an `epsilon^-4` stochastic rate and an iteration-dependent step.
- The counterexample uses a one-dimensional parameter because one valid
  instance is sufficient to refute a universal theorem. It is not presented
  as an empirical proxy for neural-network training.
- The theorem's proof establishes only an average-iterate bound while its
  statement names the last iterate. This verifier evaluates the stated,
  stronger last-iterate contract.
- Evaluator-visible publication, navigation, and blind review remain pending.
