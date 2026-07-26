"""Executable implementations of Algorithms 1--6 from arXiv:2510.25956v1.

The shared test problem uses a smooth, non-quadratic loss so that the RGO
accept/reject step and the particle interactions are non-vacuous.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.float64]


@dataclass(frozen=True)
class SmoothDROProblem:
    nominal: Array
    tau: float = 0.8
    epsilon: float = 0.7
    loss_smoothness: float = 0.35
    theta_bound: float = 0.6

    def loss(self, theta: Array, y: Array) -> Array:
        return y @ theta + self.loss_smoothness * np.logaddexp(y, -y).sum(axis=-1)

    def grad_theta_loss(self, theta: Array, y: Array) -> Array:
        del theta
        return y

    def reward(self, theta: Array, x: Array, y: Array) -> Array:
        return self.loss(theta, y) - np.square(y - x).sum(axis=-1) / (2.0 * self.tau)

    def grad_reward(self, theta: Array, x: Array, y: Array) -> Array:
        return (
            theta
            + self.loss_smoothness * np.tanh(y)
            - (y - x) / self.tau
        )

    def scaled_potential(self, theta: Array, x: Array, y: Array) -> Array:
        return -(2.0 * self.tau / self.epsilon) * self.reward(theta, x, y)

    def grad_scaled_potential(
        self, theta: Array, x: Array, y: Array
    ) -> Array:
        return -(2.0 * self.tau / self.epsilon) * self.grad_reward(theta, x, y)

    def project(self, theta: Array) -> Array:
        return np.clip(theta, -self.theta_bound, self.theta_bound)


@dataclass
class Trace:
    algorithm: int
    counters: dict[str, int] = field(default_factory=dict)
    scalars: dict[str, float] = field(default_factory=dict)

    def hit(self, name: str, count: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + count


def algorithm_1(
    problem: SmoothDROProblem,
    theta: Array,
    rng: np.random.Generator,
    flow_sampler: Callable[[Array, Array, np.random.Generator], Array],
) -> tuple[Array, Trace]:
    """Worst-case distribution sampler via a supplied gradient flow."""
    trace = Trace(algorithm=1)
    index = int(rng.integers(len(problem.nominal)))
    trace.hit("nominal_sample")
    x = problem.nominal[index]
    y = flow_sampler(theta, x, rng)
    trace.hit("conditional_gradient_flow")
    trace.hit("worst_case_output")
    return y, trace


def algorithm_2(
    problem: SmoothDROProblem,
    theta0: Array,
    rng: np.random.Generator,
    flow_sampler: Callable[[Array, Array, np.random.Generator], Array],
    outer_steps: int = 4,
    outer_lr: float = 0.04,
) -> tuple[Array, Trace]:
    """General gradient-flow-sampler-based DRO outer loop."""
    theta = theta0.copy()
    trace = Trace(algorithm=2)
    for _ in range(outer_steps):
        y, inner_trace = algorithm_1(problem, theta, rng, flow_sampler)
        trace.hit("algorithm_1_call")
        trace.hit("conditional_gradient_flow", inner_trace.counters["conditional_gradient_flow"])
        theta = problem.project(
            theta - outer_lr * problem.grad_theta_loss(theta, y)
        )
        trace.hit("projected_dro_step")
    return theta, trace


def wgf_inner(
    problem: SmoothDROProblem,
    theta: Array,
    x: Array,
    rng: np.random.Generator,
    *,
    particles: int,
    inner_steps: int,
    inner_lr: float,
    noise_scale: float = 1.0,
) -> tuple[Array, Trace]:
    """Algorithm 3 inner ULA update (paper equation 12)."""
    y = np.repeat(x[None, :], particles, axis=0)
    trace = Trace(algorithm=3)
    trace.hit("particle_initialization", particles)
    sigma = np.sqrt(inner_lr * problem.epsilon / problem.tau) * noise_scale
    for _ in range(inner_steps):
        xi = rng.standard_normal(y.shape)
        trace.hit("standard_normal_draw", y.size)
        y = y + inner_lr * problem.grad_reward(theta, x, y) + sigma * xi
        trace.hit("wgf_euler_update", particles)
    trace.scalars["noise_sigma"] = float(sigma)
    return y, trace


def algorithm_3(
    problem: SmoothDROProblem,
    theta0: Array,
    rng: np.random.Generator,
    *,
    outer_steps: int = 3,
    outer_lr: float = 0.03,
    particles: int = 192,
    inner_steps: int = 80,
    inner_lr: float = 0.015,
) -> tuple[Array, Trace]:
    theta = theta0.copy()
    trace = Trace(algorithm=3)
    for _ in range(outer_steps):
        x = problem.nominal[int(rng.integers(len(problem.nominal)))]
        trace.hit("nominal_sample")
        y, inner = wgf_inner(
            problem,
            theta,
            x,
            rng,
            particles=particles,
            inner_steps=inner_steps,
            inner_lr=inner_lr,
        )
        for name, count in inner.counters.items():
            trace.hit(name, count)
        theta = problem.project(
            theta
            - outer_lr
            * np.mean(problem.grad_theta_loss(theta, y), axis=0)
        )
        trace.hit("projected_dro_step")
    trace.scalars["noise_sigma"] = float(
        np.sqrt(inner_lr * problem.epsilon / problem.tau)
    )
    return theta, trace


def wfr_inner(
    problem: SmoothDROProblem,
    theta: Array,
    x: Array,
    rng: np.random.Generator,
    *,
    particles: int,
    inner_steps: int,
    inner_lr: float,
    weight_lr: float,
    weight_threshold: float,
    disable_reaction: bool = False,
) -> tuple[Array, Array, Trace]:
    """Algorithm 4 location, mass, normalization, and birth-death updates."""
    y = np.repeat(x[None, :], particles, axis=0)
    weights = np.full(particles, 1.0 / particles)
    trace = Trace(algorithm=4)
    trace.hit("particle_initialization", particles)
    sigma = np.sqrt(inner_lr * problem.epsilon / problem.tau)
    exponent = 1.0 - problem.epsilon * weight_lr / (2.0 * problem.tau)
    for _ in range(inner_steps):
        xi = rng.standard_normal(y.shape)
        y = y + inner_lr * problem.grad_reward(theta, x, y) + sigma * xi
        trace.hit("standard_normal_draw", y.size)
        trace.hit("wfr_location_update", particles)

        if not disable_reaction:
            reward = problem.reward(theta, x, y)
            shifted = reward - float(np.max(reward))
            weights = np.power(weights, exponent) * np.exp(weight_lr * shifted)
            trace.hit("fisher_rao_mass_update", particles)
            weights /= float(weights.sum())
            trace.hit("weight_normalization")

            low_indices = np.flatnonzero(weights < weight_threshold)
            for low in low_indices:
                donor = int(rng.choice(particles, p=weights))
                combined = 0.5 * (weights[low] + weights[donor])
                y[low] = y[donor]
                weights[low] = combined
                weights[donor] = combined
                trace.hit("birth_death_replacement")
            if len(low_indices):
                weights /= float(weights.sum())
                trace.hit("post_birth_death_normalization")
    trace.scalars["weight_sum"] = float(weights.sum())
    trace.scalars["minimum_weight"] = float(weights.min())
    return y, weights, trace


def algorithm_4(
    problem: SmoothDROProblem,
    theta0: Array,
    rng: np.random.Generator,
    *,
    outer_steps: int = 3,
    outer_lr: float = 0.03,
    particles: int = 192,
    inner_steps: int = 45,
    inner_lr: float = 0.015,
    weight_lr: float = 0.18,
    weight_threshold: float | None = None,
) -> tuple[Array, Trace]:
    theta = theta0.copy()
    trace = Trace(algorithm=4)
    threshold = (
        0.95 / particles if weight_threshold is None else weight_threshold
    )
    for _ in range(outer_steps):
        x = problem.nominal[int(rng.integers(len(problem.nominal)))]
        trace.hit("nominal_sample")
        y, weights, inner = wfr_inner(
            problem,
            theta,
            x,
            rng,
            particles=particles,
            inner_steps=inner_steps,
            inner_lr=inner_lr,
            weight_lr=weight_lr,
            weight_threshold=threshold,
        )
        for name, count in inner.counters.items():
            trace.hit(name, count)
        theta = problem.project(
            theta
            - outer_lr
            * np.sum(
                weights[:, None] * problem.grad_theta_loss(theta, y), axis=0
            )
        )
        trace.hit("weighted_projected_dro_step")
    trace.scalars["last_weight_sum"] = float(weights.sum())
    return theta, trace


def rbf_kernel_and_repulsion(y: Array, bandwidth: float) -> tuple[Array, Array]:
    """Return K[j,i] and grad with respect to source y[j], summed over j."""
    difference = y[:, None, :] - y[None, :, :]
    squared = np.square(difference).sum(axis=2)
    kernel = np.exp(-squared / bandwidth)
    source_gradient = -(2.0 / bandwidth) * difference * kernel[:, :, None]
    return kernel, source_gradient


def svgd_inner(
    problem: SmoothDROProblem,
    theta: Array,
    x: Array,
    rng: np.random.Generator,
    *,
    particles: int,
    inner_steps: int,
    inner_lr: float,
    initial_deviation: float,
    bandwidth: float,
    repulsion_sign: float = 1.0,
) -> tuple[Array, Trace]:
    """Algorithm 5 with score and positive-definite-kernel repulsion."""
    y = x + rng.normal(0.0, initial_deviation, size=(particles, x.size))
    trace = Trace(algorithm=5)
    trace.hit("gaussian_particle_initialization", particles)
    for _ in range(inner_steps):
        kernel, kernel_gradient = rbf_kernel_and_repulsion(y, bandwidth)
        score = (2.0 * problem.tau / problem.epsilon) * problem.grad_reward(
            theta, x, y
        )
        driving = kernel.T @ score
        repulsion = kernel_gradient.sum(axis=0)
        phi = (driving + repulsion_sign * repulsion) / particles
        y = y + inner_lr * phi
        trace.hit("kernel_pair_evaluation", particles * particles)
        trace.hit("score_force", particles)
        trace.hit("kernel_repulsion", particles)
        trace.hit("svg_transport_update", particles)
    return y, trace


def algorithm_5(
    problem: SmoothDROProblem,
    theta0: Array,
    rng: np.random.Generator,
    *,
    outer_steps: int = 3,
    outer_lr: float = 0.03,
    particles: int = 96,
    inner_steps: int = 30,
    inner_lr: float = 0.04,
    initial_deviation: float = 0.5,
    bandwidth: float = 4.0,
) -> tuple[Array, Trace]:
    theta = theta0.copy()
    trace = Trace(algorithm=5)
    for _ in range(outer_steps):
        x = problem.nominal[int(rng.integers(len(problem.nominal)))]
        trace.hit("nominal_sample")
        y, inner = svgd_inner(
            problem,
            theta,
            x,
            rng,
            particles=particles,
            inner_steps=inner_steps,
            inner_lr=inner_lr,
            initial_deviation=initial_deviation,
            bandwidth=bandwidth,
        )
        for name, count in inner.counters.items():
            trace.hit(name, count)
        theta = problem.project(theta - outer_lr * np.mean(y, axis=0))
        trace.hit("projected_dro_step")
    return theta, trace


def rgo_minimizer(
    problem: SmoothDROProblem, theta: Array, x: Array
) -> tuple[Array, float]:
    """Find the unique minimizer of the scaled conditional potential."""
    y = x.copy()
    for _ in range(40):
        gradient = problem.grad_scaled_potential(theta, x, y)
        diagonal_hessian = (2.0 * problem.tau / problem.epsilon) * (
            1.0 / problem.tau
            - problem.loss_smoothness / np.square(np.cosh(y))
        )
        y -= gradient / diagonal_hessian
    residual = float(np.max(np.abs(problem.grad_scaled_potential(theta, x, y))))
    return y, residual


def rgo_inner(
    problem: SmoothDROProblem,
    theta: Array,
    x: Array,
    rng: np.random.Generator,
    *,
    particles: int,
    accept_all: bool = False,
    max_trials: int = 500_000,
) -> tuple[Array, Trace]:
    """Algorithm 6 restricted Gaussian oracle rejection sampler."""
    if not problem.tau < 1.0 / problem.loss_smoothness:
        raise ValueError("RGO requires tau < 1/L")
    mode, residual = rgo_minimizer(problem, theta, x)
    trace = Trace(algorithm=6)
    trace.hit("approximate_minimizer")
    trace.scalars["minimizer_gradient_inf"] = residual
    strong_convexity = 2.0 * (
        1.0 - problem.loss_smoothness * problem.tau
    ) / problem.epsilon
    proposal_std = np.sqrt(1.0 / strong_convexity)
    u_mode = float(problem.scaled_potential(theta, x, mode))
    accepted: list[Array] = []
    trials = 0
    maximum_log_acceptance = -np.inf
    while len(accepted) < particles and trials < max_trials:
        proposal = mode + proposal_std * rng.standard_normal(mode.shape)
        log_acceptance = (
            -float(problem.scaled_potential(theta, x, proposal))
            + u_mode
            + 0.5 * strong_convexity * float(np.square(proposal - mode).sum())
        )
        maximum_log_acceptance = max(maximum_log_acceptance, log_acceptance)
        trace.hit("gaussian_proposal")
        trials += 1
        if accept_all or np.log(rng.random()) <= min(0.0, log_acceptance):
            accepted.append(proposal)
            trace.hit("rejection_accept")
        else:
            trace.hit("rejection_reject")
    if len(accepted) != particles:
        raise RuntimeError("RGO exhausted its deterministic trial budget")
    trace.scalars["acceptance_rate"] = particles / trials
    trace.scalars["maximum_log_acceptance"] = float(maximum_log_acceptance)
    trace.scalars["proposal_std"] = float(proposal_std)
    return np.stack(accepted), trace


def algorithm_6(
    problem: SmoothDROProblem,
    theta0: Array,
    rng: np.random.Generator,
    *,
    outer_steps: int = 3,
    outer_lr: float = 0.03,
    particles: int = 192,
) -> tuple[Array, Trace]:
    theta = theta0.copy()
    trace = Trace(algorithm=6)
    for _ in range(outer_steps):
        x = problem.nominal[int(rng.integers(len(problem.nominal)))]
        trace.hit("nominal_sample")
        y, inner = rgo_inner(
            problem, theta, x, rng, particles=particles
        )
        for name, count in inner.counters.items():
            trace.hit(name, count)
        for name, value in inner.scalars.items():
            trace.scalars[f"last_{name}"] = value
        theta = problem.project(theta - outer_lr * np.mean(y, axis=0))
        trace.hit("projected_dro_step")
    return theta, trace


def make_problem() -> SmoothDROProblem:
    grid = np.linspace(-0.7, 0.7, 48, dtype=np.float64).reshape(6, 8)
    nominal = np.sin(1.7 * grid) + 0.15 * np.cos(3.1 * grid)
    return SmoothDROProblem(nominal=nominal)
