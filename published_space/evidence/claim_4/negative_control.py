"""Corrected outer exponent must invalidate the v1 total exponent."""

from __future__ import annotations

import json


def main() -> int:
    corrected_outer = 4
    inner = 2
    claimed_v1_total = 4
    corrected_total = corrected_outer + inner
    rejected = corrected_total != claimed_v1_total
    output = {
        "status": "REJECTED_AS_EXPECTED" if rejected else "UNEXPECTED_PASS",
        "mutation": "v1 outer exponent 2 -> corrected v3 exponent 4",
        "reason": "total exponent becomes 6, not the claimed 4",
        "corrected_total_exponent": corrected_total,
        "claimed_v1_total_exponent": claimed_v1_total,
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
