# Claim 3 method

This is a theorem-calibrated exact instance rather than a noisy log-log fit.

1. `certificate.py` reconstructs the entropy-DRO log partition and asks SymPy
   to verify the outer objective, stochastic recurrence, variance, and exact
   mean-square formula. It records the analytic lower bound.
2. `generate_raw.py` independently minimizes the exact last-iterate error over
   every admissible constant step using golden-section search, and uses binary
   search for the first feasible iteration count. Horizons are discovered by
   doubling; none are selected from the theorem's formula.
3. `independent_checker.py` uses SciPy adaptive quadrature to reconstruct the
   continuous Gibbs means/variances and SciPy bounded optimization to repeat
   the first-hit calibration. It compares against committed raw JSON.
4. `negative_control.py` replaces one stochastic draw by an antithetic pair,
   cancelling the variance. This mutation must reject the counterexample and
   converge well inside an `epsilon^-2` budget.

No random samples are used by the verifier, so no seed is required. The
cumulative fixed command remains:

`uv run --frozen --no-dev python -m reproduction.run_all`
