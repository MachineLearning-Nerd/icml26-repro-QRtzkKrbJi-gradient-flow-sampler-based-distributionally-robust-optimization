# Claim 3 source and theorem-calibration audit

## v1 statement

The judged source is arXiv `2510.25956v1`, PDF SHA-256
`796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`.
Theorem 1 is in Section 5, PDF page 8 (plain-text line 496). Its proof is
Appendix C.3, PDF pages 17-18 (lines 1198-1308).

It assumes a smooth outer objective, a sampled-variable Lipschitz parameter
gradient, bounded stochastic-gradient variance, and bounded W2 sampler error.
It claims a constant step `r=O(1/L_Phi)` and
`S=O(1/epsilon_opt^2)` produce a **last-iterate** point satisfying
`E||grad Phi(theta_S)||^2 <= epsilon_opt^2`, provided the sampler error is
`O(epsilon_opt/L_f)`.

## Proof gap visible in v1

The last display of Appendix C.3 is an average-iterate bound:

`(1/S) sum_s E||grad Phi(theta_s)||^2
 <= 4(Phi(theta_0)-Phi_inf)/(rS)
    +4(L_f delta_sample)^2 +2 L_Phi r sigma^2`.

With nonzero variance, a step independent of the tolerance leaves a positive
noise floor. Taking `r=O(epsilon^2)` controls that term but changes the first
term; it cannot yield the stated `O(epsilon^-2)` rate. The proof also changes
from a last-iterate statement to an average without selecting or randomizing
an output iterate.

## Faithful entropy-DRO counterexample

Take one datum `x=0`, squared cost, `tau=1`, entropy regularization
`epsilon_ent=2`, and

`ell(theta,z)=theta^2/2+theta*z`.

The conditional Gibbs exponent is

`ell(theta,z)-z^2/2 = -(z-theta)^2/2+theta^2`,

so the exact worst-case law is `N(theta,1)`. Its log partition gives
`Phi(theta)=theta^2+constant`; hence `L_Phi=2`. The parameter gradient
`theta+z` is 1-Lipschitz in `z`. Drawing exactly from the target gives
`delta_sample=0`, and with `z_s=theta_s+xi_s`, `xi_s~N(0,1)`, the stochastic
gradient is unbiased with variance exactly 1. Every v1 assumption holds.

For `theta_0=1`,

`theta_(s+1)=(1-2r)theta_s-r xi_s`

and, for `0<r<=1/4`,

`E||grad Phi(theta_S)||^2
 =4(1-2r)^(2S)+[r/(1-r)](1-(1-2r)^(2S))`.

If this is at most `epsilon^2` for `epsilon<=1`, the variance term forces
`r <= 4 epsilon^2/(3+4 epsilon^2) <= 4epsilon^2/3`. The bias term and
`-log(1-2r)<=4r` then force

`S >= [3/(32 epsilon^2)] log(4/epsilon^2)`.

The required last-iterate count is therefore
`Omega(epsilon^-2 log(1/epsilon))`, not `O(epsilon^-2)`.

## Current-version correction

Current arXiv v3 no longer states the judged rate. Theorem 5.2 uses an
`S`-dependent step and states `S=O(epsilon_opt^-4)`; its proof explicitly
balances the variance term. Theorem 5.5 consequently changes total complexity
to `epsilon_opt^-6`. This source correction is consistent with, but not a
substitute for, the executable v1 counterexample.
