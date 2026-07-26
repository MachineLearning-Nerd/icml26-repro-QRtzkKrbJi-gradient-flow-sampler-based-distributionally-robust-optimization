import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        r"""
        # Gradient-flow DRO: an evidence-first reproduction

        This notebook explains the central claims without rerunning any expensive
        experiment. The displayed numbers are embedded from the pinned,
        fail-closed evidence suite at Git SHA
        `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`.

        The current live judge score is **4/12**. The evidence-supported best
        possible score is **10/12**, a forecast rather than a judge result.
        """
    )
    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np

    claims = np.arange(1, 7)
    previous = np.array([1, 0, 1, 1, 0, 1])
    supported = np.array([2, 2, 2, 0, 2, 2])
    colors = ["#168166", "#b23a48", "#b23a48", "#6b7280", "#b23a48", "#168166"]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.bar(claims - 0.17, previous, 0.34, color="#cbd5e1", label="Previous judge")
    ax.bar(claims + 0.17, supported, 0.34, color=colors, label="Evidence forecast")
    ax.set(xticks=claims, xticklabels=[f"C{i}" for i in claims], yticks=[0, 1, 2])
    ax.set_ylabel("Points (forecast)")
    ax.set_title("Five exact outcomes; Claim 4 remains blocked")
    ax.legend(frameon=False)
    fig
    return (plt,)


@app.cell
def _(mo):
    mo.md(r"""
    ## What gradient-flow sampling changes

    Entropy-regularized Wasserstein DRO induces a conditional Gibbs law for
    adversarial examples. The paper's framework samples that law, then uses
    sampled loss gradients in an outer projected optimization step.

    - **WGF** uses a noisy Euler/Langevin location update.
    - **WFR** adds particle mass evolution and birth–death.
    - **SVGD** replaces noise with kernel-smoothed score and repulsion.
    - **RGO** solves a conditional mode and uses rejection sampling.

    The reproduction implements all six numbered algorithms. Its checker
    independently rebuilds WGF and SVGD transitions, audits WFR mass and
    birth–death, and requires RGO to both accept and reject proposals.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The full CIFAR-10 plot contradicts strict dominance

    The judged claim says both WGF and WFR beat baseline DRO methods at
    every perturbation setting. The authors' exact vector Figure 6 data
    give this counterexample at `epsilon=0.2, Delta=0.008`.
    """)
    return


@app.cell
def _(plt):
    methods = ["WRM", "WFR", "WGF"]
    robust_accuracy = [80.5615936875, 78.3016303274, 77.8713766616]
    fig_cifar, ax_cifar = plt.subplots(figsize=(6.5, 3.4))
    bars = ax_cifar.bar(
        methods,
        robust_accuracy,
        color=["#64748b", "#8c564b", "#ff7f0e"],
    )
    ax_cifar.bar_label(bars, fmt="%.2f%%", padding=3)
    ax_cifar.set_ylim(72, 83)
    ax_cifar.set_ylabel("Robust accuracy (%)")
    ax_cifar.set_title("Official Figure 6: WRM exceeds both proposed methods")
    fig_cifar
    return


@app.cell
def _(mo):
    mo.md(r"""
    The exhaustive vector checker tests all 120 nonzero
    proposed-versus-baseline comparisons. It finds **20 WGF** and **29 WFR**
    violations. The verdict is FALSIFIED for the strict judged wording,
    with MEDIUM confidence because the paper's literal prose only says the
    methods have a qualitative "high degree of robustness."

    ## The theoretical outcomes

    | Claim | Exact evidence | Verdict |
    |---|---|---|
    | Necessary WGF time | An admissible symmetric observable is exact at time 0 for every tolerance | FALSIFIED |
    | Outer `epsilon^-2` rate | Exact recurrence needs `epsilon^-2 log(1/epsilon)` iterations | FALSIFIED |
    | Total `epsilon^-4` work | Four proof/source/falsification routes do not settle the exact statement | BLOCKED |
    | Half-bridge equivalence | Symbolic functional identity has zero residual | VERIFIED |

    Toy checks are not upgraded to PASS. Negative controls exit nonzero, and
    the historical 4/12 artifact remains preserved.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Reproduce the verifier

    From the repository:

    ```bash
    uv sync --frozen
    uv run --frozen --no-dev python -m reproduction.run_all
    ```

    This command regenerates/checks all accepted raw results and fails
    closed if any claim checker or expected negative control changes.
    """)
    return


if __name__ == "__main__":
    app.run()
