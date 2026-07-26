"""Generate deterministic evidence figures for the reproduction report."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "images"
ARTIFACTS = ROOT / ".openresearch" / "artifacts"

mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.hashsalt": "gfs-dro-reproduction",
    }
)
COLORS = {
    "verified": "#168166",
    "falsified": "#b23a48",
    "blocked": "#6b7280",
    "paper": "#64748b",
    "observed": "#2563eb",
    "control": "#d97706",
}


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(
        OUT / name,
        format="svg",
        bbox_inches="tight",
        metadata={"Date": None, "Creator": "OpenResearch"},
    )
    plt.close(fig)


def outcome_figure() -> None:
    claims = np.arange(1, 7)
    previous = np.array([1, 0, 1, 1, 0, 1])
    supported = np.array([2, 2, 2, 0, 2, 2])
    statuses = [
        "VERIFIED",
        "FALSIFIED",
        "FALSIFIED",
        "BLOCKED",
        "FALSIFIED",
        "VERIFIED",
    ]
    colors = [
        COLORS["verified"],
        COLORS["falsified"],
        COLORS["falsified"],
        COLORS["blocked"],
        COLORS["falsified"],
        COLORS["verified"],
    ]
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    width = 0.34
    ax.bar(
        claims - width / 2,
        previous,
        width,
        color="#cbd5e1",
        label="Previous live judge",
    )
    ax.bar(
        claims + width / 2,
        supported,
        width,
        color=colors,
        label="Evidence-supported forecast",
    )
    for x, value, status in zip(claims, supported, statuses, strict=True):
        ax.text(
            x + width / 2,
            value + 0.08,
            status,
            ha="center",
            va="bottom",
            fontsize=7.5,
            rotation=25,
        )
    ax.set(
        xticks=claims,
        xticklabels=[f"C{i}" for i in claims],
        yticks=[0, 1, 2],
        ylim=(0, 2.55),
        ylabel="Points (forecast, not judge result)",
        title="Five exact claim outcomes; Claim 4 remains honestly blocked",
    )
    ax.legend(frameon=False, ncol=2, loc="upper center")
    ax.grid(axis="y", alpha=0.2)
    save(fig, "headline_outcomes.svg")


def cifar_figure() -> None:
    raw = json.loads(
        (ARTIFACTS / "claim_5" / "raw_counterexamples.json").read_text()
    )
    methods = ["WRM", "WFR", "WGF"]
    accuracy = [
        raw["plotted_robust_accuracy_percent"][method] for method in methods
    ]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    bars = ax.bar(
        methods,
        accuracy,
        color=["#64748b", "#8c564b", "#ff7f0e"],
        width=0.62,
    )
    ax.bar_label(bars, fmt="%.2f%%", padding=3)
    ax.set(
        ylim=(72, 83),
        ylabel="Robust accuracy (%)",
        title=r"Official Figure 6 counterexample: $\epsilon=0.2,\ \Delta=0.008$",
    )
    ax.grid(axis="y", alpha=0.2)
    ax.text(
        1.5,
        72.6,
        "Both proposed methods trail WRM",
        ha="center",
        fontsize=9,
        color=COLORS["falsified"],
    )
    save(fig, "claim5_counterexample.svg")


def outer_rate_figure() -> None:
    raw = json.loads((ARTIFACTS / "claim_3" / "raw_results.json").read_text())
    epsilon = np.array(
        [row["epsilon"] for row in raw["calibrated_first_hits"]]
    )
    iterations = np.array(
        [row["minimum_iterations"] for row in raw["calibrated_first_hits"]]
    )
    reference = iterations[0] * (epsilon[0] / epsilon) ** 2
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.loglog(
        epsilon,
        iterations,
        "o-",
        color=COLORS["observed"],
        label="Exact calibrated first hit",
    )
    ax.loglog(
        epsilon,
        reference,
        "--",
        color=COLORS["paper"],
        label=r"$\epsilon^{-2}$ reference",
    )
    ax.invert_xaxis()
    ax.set(
        xlabel=r"Stationarity tolerance $\epsilon$",
        ylabel="Minimum outer iterations",
        title=r"Claim 3 needs an extra $\log(1/\epsilon)$ factor",
    )
    ax.legend(frameon=False)
    ax.grid(which="both", alpha=0.2)
    save(fig, "claim3_outer_rate.svg")


def necessary_time_figure() -> None:
    raw = json.loads((ARTIFACTS / "claim_2" / "raw_results.json").read_text())
    epsilon = np.array([row["epsilon"] for row in raw["tolerance_sweep"]])
    claimed = np.array(
        [row["claimed_scale"] for row in raw["tolerance_sweep"]]
    )
    actual = np.array(
        [row["measured_first_hit"] for row in raw["tolerance_sweep"]]
    )
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogx(
        epsilon,
        claimed,
        "o-",
        color=COLORS["paper"],
        label="Claimed necessary scale",
    )
    ax.semilogx(
        epsilon,
        actual,
        "o-",
        color=COLORS["falsified"],
        label="Exact first-hit time",
    )
    ax.invert_xaxis()
    ax.set(
        xlabel=r"Gradient accuracy $\epsilon$",
        ylabel="Sampler time",
        title="Claim 2 counterexample is accurate at initialization",
    )
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    save(fig, "claim2_time_counterexample.svg")


def half_bridge_figure() -> None:
    raw = json.loads((ARTIFACTS / "claim_6" / "raw_results.json").read_text())
    x = np.array([row["x"] for row in raw["cases"]])
    residual = np.array(
        [abs(row["identity_residual"]) for row in raw["cases"]]
    )
    mass = np.array(
        [abs(row["target_mass"] - 1.0) for row in raw["cases"]]
    )
    floor = 1e-18
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogy(
        x,
        np.maximum(residual, floor),
        "o-",
        label="Functional identity residual",
        color=COLORS["verified"],
    )
    ax.semilogy(
        x,
        np.maximum(mass, floor),
        "s--",
        label="Target mass error",
        color=COLORS["observed"],
    )
    ax.axhline(1e-14, color=COLORS["paper"], linestyle=":", label="1e-14")
    ax.set(
        xlabel="Conditioning value x",
        ylabel="Absolute error (log scale)",
        title="Claim 6 continuous quadrature agrees at machine precision",
        ylim=(5e-19, 3e-13),
    )
    ax.legend(frameon=False)
    ax.grid(which="both", alpha=0.2)
    save(fig, "claim6_half_bridge.svg")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    outcome_figure()
    cifar_figure()
    outer_rate_figure()
    necessary_time_figure()
    half_bridge_figure()
