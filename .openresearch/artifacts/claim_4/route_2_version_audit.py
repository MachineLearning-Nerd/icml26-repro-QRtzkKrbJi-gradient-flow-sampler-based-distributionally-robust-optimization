"""Route 2: machine-check the authoritative v1-to-v3 correction."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> int:
    diff = json.loads(
        (HERE / "version_diff.json").read_text(encoding="utf-8")
    )
    if diff["judged"]["total_exponent"] != 4:
        raise AssertionError("judged exponent changed")
    if diff["current"]["total_exponent"] != 6:
        raise AssertionError("current corrected exponent changed")
    if "flaw in our original proof" not in diff["acknowledgment"]:
        raise AssertionError("author correction is no longer explicit")
    output = {
        "route": 2,
        "status": "INCONCLUSIVE_FOR_EXACT_CLAIM",
        "judged_version": diff["judged"]["arxiv_version"],
        "judged_exponent": diff["judged"]["total_exponent"],
        "current_version": diff["current"]["arxiv_version"],
        "current_exponent": diff["current"]["total_exponent"],
        "author_acknowledges_original_proof_flaw": True,
        "why_not_falsification": (
            "a corrected statement does not alone prove a lower bound "
            "contradicting the old upper bound"
        ),
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
