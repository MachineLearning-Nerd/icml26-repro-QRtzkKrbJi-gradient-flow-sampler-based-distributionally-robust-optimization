# Claim 2 method

The falsification uses an exact counterexample, not a fitted scaling slope.

- `certificate.py` completes the square symbolically, proves the loss
  smoothness and mixed-gradient Lipschitz constants, proves strong convexity
  and PL, and proves equality of the initial and target gradient oracles at
  `theta=0`.
- `independent_checker.py` uses adaptive quadrature over the whole real line
  to normalize the target and integrate its mean and second moment. It also
  recomputes the claimed time scale over six tolerances without using that
  scale to select a horizon or sample count.
- `negative_control.py` retains the same family and assumptions but uses
  `theta=1`; it must exit 1 because time zero misses tolerance `0.1`.
- `verifier.py` requires the counterexample certificate/checker to pass and
  requires the negative control to fail for its intended reason.

There is no Monte Carlo sampling and no seed. The result is exact up to the
independent quadrature regression. The fixed cumulative command is:

`uv run --frozen --no-dev python -m reproduction.run_all`

The historical verifier that merely evaluated the paper's formula is preserved
as a historical rejected baseline and is not invoked as current evidence.
