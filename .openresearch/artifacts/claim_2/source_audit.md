# Claim 2 source and direction audit

## Exact statement

The judged source is arXiv `2510.25956v1`, PDF SHA-256
`796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`.
Proposition 1 is in Section 4, PDF page 7 (plain-text line 439). Its proof is
Appendix C.2, PDF pages 16-17 (lines 1112-1196).

The proposition says the WGF sampler “needs to run for time at least”

`t ≳ O((1/lambda) log(L/sqrt(lambda epsilon)))`

to obtain an `epsilon`-gradient estimate. The assumptions stated in v1 are an
`L`-smooth loss in the sampled variable and a conditional energy satisfying
gradient dominance with `lambda>0`.

Current v3 retains the necessary phrase in Proposition 4.2 and clarifies that
`y -> grad_theta ell(theta,y)` is `L_f`-Lipschitz, the energy is smooth and
lambda-convex or lambda-LSI, and the error is in expectation for sufficiently
large `N`. The counterexample below also satisfies these clarified conditions
for every `N`.

## Proof-direction audit

Appendix C.2 obtains an upper bound of the form

`gradient_error(t) <= L exp(-lambda t)/sqrt(lambda)`.

Solving an upper bound for a target tolerance supplies a **sufficient** time:
running at least that long guarantees the bound is small. It cannot establish
that every admissible instance requires that time. A necessary lower bound
would need a matching worst-case construction or information-theoretic
argument; neither appears in the proof.

This direction error is independently testable because an admissible
observable can be integrated exactly long before the whole distribution has
mixed.

## Assumption-satisfying counterexample

Use `rho_0=delta_0`, squared cost, `tau=1/4`, entropy regularization
`epsilon_ent=2 tau=1/2`, and

`ell(theta,y)=theta*y+y^2/2`

at `theta=0`. The sampled-variable Hessian is exactly 1, and the parameter
gradient `y` is exactly 1-Lipschitz. With `x=0`, the conditional energy is

`U(y)=-ell(0,y)+(1/(2 tau))(y-x)^2=3y^2/2`.

The entropy choice makes the conditional density proportional to `exp(-U)`.
It is 3-strongly convex, and after its zero minimum is fixed,
`|grad U|^2=9y^2=6U`; hence it satisfies the displayed PL condition with
`lambda=6`. The Gibbs target is a centered continuous Gaussian with variance
`1/3`, so the initial `delta_0` is not a warm start equal to the target:
their `W2` distance is `1/sqrt(3)`.

Nevertheless, the initial oracle is `grad_theta ell(0,0)=0`, and the exact
target oracle is `E[Y]=0`. The gradient error is exactly zero at `t=0` for
every `epsilon>0`. With `L=1` and `lambda=6`, the claimed scale is positive
for `epsilon<1/6` and diverges as `epsilon` tends to zero. No positive hidden
constant can turn a sequence of zero required times into this divergent lower
order.

## Negative control

At `theta=1`, all smoothness and curvature constants are unchanged, but the
target mean becomes `1/3`. Starting from zero gives error `1/3`. Under the
quadratic WGF, the error is `(1/3)exp(-3t)`, so tolerance `0.1` is first met at
`t=0.4013242681...`. This control shows that the checker can detect an instance
that genuinely needs positive flow time.
