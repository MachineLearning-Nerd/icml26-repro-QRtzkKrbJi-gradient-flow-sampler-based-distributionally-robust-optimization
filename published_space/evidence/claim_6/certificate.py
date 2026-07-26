"""Exact algebraic certificate for the conditional Gibbs identity."""

from __future__ import annotations

import json

import sympy as sp


def main() -> int:
    a, energy, density, normalizer = sp.symbols(
        "a A q Z", positive=True, finite=True
    )
    log_target = -energy / a - sp.log(normalizer)
    kl_integrand = a * density * (sp.log(density) - log_target)
    objective_plus_constant = (
        energy * density
        + a * density * sp.log(density)
        + a * density * sp.log(normalizer)
    )
    residual = sp.simplify(kl_integrand - objective_plus_constant)
    if residual != 0:
        raise AssertionError(f"conditional identity residual is {residual}")

    result = {
        "status": "PASS",
        "symbolic_integrand_residual": str(residual),
        "substitutions": {
            "a": "epsilon/(2*tau)",
            "A_x(y)": "V(y)+c(x,y)/(2*tau)",
            "log_p_x(y)": "-A_x(y)/a-log(Z_x)",
        },
        "normalization_fact": "integral q_x(y) dy = 1",
        "integrated_identity": "J_x(q_x)=a*KL(q_x||p_x)-a*log(Z_x)",
        "marginal_elimination": (
            "rho(dy)=integral Pi(dx,dy) implies "
            "integral V(y)rho(dy)=integral V(y)Pi(dx,dy)"
        ),
        "entropy_disintegration": (
            "integral Pi log Pi = E_rho0[integral q_x log q_x] "
            "+ integral rho0 log rho0; the last term is fixed"
        ),
        "optimizer": "q_x=p_x almost everywhere by KL nonnegativity",
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
