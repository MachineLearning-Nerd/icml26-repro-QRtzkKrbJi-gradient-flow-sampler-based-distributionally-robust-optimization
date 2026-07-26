"""Evaluator-visible fail-closed cumulative verifier.

Run exactly:
    uv run --frozen --no-dev python -m reproduction.run_all
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
EXPECTED = {
    1: "VERIFIED",
    2: "FALSIFIED",
    3: "FALSIFIED",
    4: "BLOCKED",
    5: "FALSIFIED",
    6: "VERIFIED",
}


def main() -> int:
    started = time.perf_counter()
    results: list[dict[str, object]] = []
    for claim_id, expected_verdict in EXPECTED.items():
        verifier = EVIDENCE / f"claim_{claim_id}" / "verifier.py"
        completed = subprocess.run(
            [sys.executable, str(verifier)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        print(f"\n--- Claim {claim_id}: {verifier.relative_to(ROOT)} ---")
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        if completed.returncode != 0:
            raise RuntimeError(
                f"Claim {claim_id} verifier exited {completed.returncode}"
            )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError(f"Claim {claim_id} emitted no JSON")
        payload = json.loads(lines[-1])
        if payload.get("claim_id") != claim_id:
            raise RuntimeError(f"Claim {claim_id} identity mismatch")
        if payload.get("verdict") != expected_verdict:
            raise RuntimeError(
                f"Claim {claim_id}: expected {expected_verdict}, "
                f"got {payload.get('verdict')}"
            )
        results.append(
            {
                "claim_id": claim_id,
                "verdict": expected_verdict,
                "exit_code": completed.returncode,
            }
        )
    print("\n=== CURRENT CUMULATIVE VERIFIER ===")
    print(
        json.dumps(
            {
                "status": "PASS",
                "fixed_command": (
                    "uv run --frozen --no-dev python -m reproduction.run_all"
                ),
                "results": results,
                "runtime_s": round(time.perf_counter() - started, 6),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

