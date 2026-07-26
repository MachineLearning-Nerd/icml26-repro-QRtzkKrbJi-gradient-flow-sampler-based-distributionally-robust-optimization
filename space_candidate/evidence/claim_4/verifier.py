"""Fail-closed verifier that enforces all four BLOCKED routes."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HERE / name)],
        cwd=HERE,
        capture_output=True,
        text=True,
    )


def output(completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise AssertionError(f"route emitted no JSON: {completed.args}")
    return json.loads(lines[-1])


def main() -> int:
    route_outputs: list[dict[str, object]] = []
    for route in (
        "route_1_proof_audit.py",
        "route_2_version_audit.py",
        "route_3_primary_sources.py",
    ):
        process = run(route)
        if process.returncode != 0:
            raise AssertionError(process.stderr)
        result = output(process)
        if result["status"] != "INCONCLUSIVE_FOR_EXACT_CLAIM":
            raise AssertionError(f"route overclaimed: {route}")
        route_outputs.append({"exit_code": process.returncode, **result})

    falsification_process = run("route_4_falsification.py")
    falsification = output(falsification_process)
    if falsification_process.returncode != 1:
        raise AssertionError(
            "route 4 must not claim falsification without a counterexample"
        )
    if falsification["status"] != "FALSIFICATION_NOT_ESTABLISHED":
        raise AssertionError("route 4 failed for an unintended reason")
    route_outputs.append(
        {"exit_code": falsification_process.returncode, **falsification}
    )

    control_process = run("negative_control.py")
    control = output(control_process)
    if control_process.returncode != 1:
        raise AssertionError("corrected-exponent control did not exit 1")
    recorded_control = json.loads(
        (HERE / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if recorded_control != {"exit_code": 1, **control}:
        raise AssertionError("recorded negative-control output changed")

    result = {
        "claim_id": 4,
        "verdict": "BLOCKED",
        "confidence": "LOW",
        "route_count": len(route_outputs),
        "routes": route_outputs,
        "negative_control": {
            "exit_code": control_process.returncode,
            "status": control["status"],
            "reason": control["reason"],
        },
        "blocker": (
            "No rigorous direct-product embedding currently proves that an "
            "Algorithm 3 instance satisfying Assumptions 1-4 requires more "
            "than soft-O(epsilon^-4) total work."
        ),
        "unblocker": (
            "Provide that lower-bound embedding or a correct proof of the "
            "v1 epsilon^-4 upper bound."
        ),
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
