"""Route 3: audit the two primary complexity sources."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> int:
    data = json.loads(
        (HERE / "primary_sources.json").read_text(encoding="utf-8")
    )
    ids = {source["arxiv_id"] for source in data["sources"]}
    if ids != {"1903.08568", "1912.02365"}:
        raise AssertionError("primary-source set changed")
    if "multiplying unrelated" not in data["unresolved_link"]:
        raise AssertionError("direct-product limitation was lost")
    output = {
        "route": 3,
        "status": "INCONCLUSIVE_FOR_EXACT_CLAIM",
        "primary_source_ids": sorted(ids),
        "ula_inner_upper_bound_found": True,
        "stochastic_outer_lower_bound_found": True,
        "algorithm3_direct_product_certificate_found": False,
        "why_not_falsification": data["unresolved_link"],
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
