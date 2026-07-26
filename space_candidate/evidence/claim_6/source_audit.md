# Claim 6 source audit

## Exact source

The judged contract is arXiv `2510.25956v1`, PDF SHA-256
`796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`.
Lemma 1 appears in Section 3.1 on PDF page 3 (plain-text line 157); its
paper proof is Appendix C.1 on PDF page 16 (plain-text line 1083).

The lemma minimizes, over a coupling `Pi` whose `X` marginal is fixed to
`rho_0`,

`int V(y)dPi + (1/(2 tau)) int c(x,y)dPi
 + (epsilon/(2 tau)) int log(Pi)dPi`.

It then states equivalence to an expected conditional KL minimization with

`p_x(y) = Z_x^-1 exp(-(2 tau V(y)+c(y,x))/epsilon)`.

The live judge rejected the old five-element check because it passed identical
logits through the same function twice. That evidence is preserved only as the
historical rejected baseline.

## Assumptions and quantifiers

The paper writes densities formally and does not spell out a dominating
measure. The certificate makes the minimum regularity explicit: sigma-finite
base measures, an admissible disintegration `Pi(dx,dy)=rho_0(dx)q_x(y)dy`,
finite objective, and `0 < Z_x < infinity` almost everywhere. The identity is
pointwise in `x`, hence applies to every fixed marginal for which these
quantities exist. Both `tau` and `epsilon` are strictly positive.

## Independent reconstruction

Set

`a = epsilon/(2 tau)` and
`A_x(y) = V(y) + c(x,y)/(2 tau)`.

Then `p_x(y)=exp(-A_x(y)/a)/Z_x`. Direct substitution gives

`a q_x log(q_x/p_x)
 = A_x q_x + a q_x log q_x + a q_x log Z_x`.

After integration and `int q_x=1`,

`J_x(q_x) = a KL(q_x||p_x) - a log Z_x`.

Gibbs' inequality makes `q_x=p_x` the conditional minimizer. Integrating over
the unchanged `rho_0` proves the expected-KL form. Separately, the constraint
`rho(dy)=int Pi(dx,dy)` changes `int V d rho` to `int V(y)dPi` and eliminates
the otherwise free marginal, which is precisely the one-sided bridge
constraint.

This reconstruction does not use the paper's claimed optimizer as numerical
input and does not infer a functional theorem from a finite example.

## Important measure convention

If `rho_0` has density `r_0` relative to a chosen base measure, the joint
entropy contributes `a int r_0 log r_0`, which is constant because the
`X` marginal is fixed. For an empirical marginal, use counting measure on its
atoms. Mixing Lebesgue entropy with a singular empirical measure without
declaring a base measure would be undefined; the certificate does not make
that mistake.
