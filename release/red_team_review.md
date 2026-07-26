# Evaluator-blind pre-publication review

The review used only `space_candidate/` and the evaluator rubric. Repository
source, OpenResearch descriptions, and run logs were not used to fill gaps.

## Review 1 — findings

Files opened from the canonical entrypoint:

- `README.md`
- `logbook.json`
- `pages/current/index.md`
- `pages/current/visibility.md`
- `pages/current/verification.md`
- `pages/current/claims/claim-1.md` through `claim-6.md`
- `pages/current/historical.md`
- `pages/current/report.md`

Three release-blocking defects were found:

1. `logbook.json` contained a stale trailing fragment and did not parse.
2. Claim pages did not all expose the exact command, lockfile, Git SHA, seed
   policy, CPU allocation, and per-claim runtime inline.
3. No exact text-only upload allowlist, current manifest, release forecast
   page, or machine-enforced historical-subset mapping was reachable.

No scientific verdict was inferred for a page with missing material.

## Fixes

- Removed the stale JSON fragment and validated the canonical root.
- Added reproducibility blocks and source/contract links to all six pages.
- Added a release report, exact allowlist/manifest builder, fail-closed
  traversal, secret scan, and 17-file historical-subset proof.
- Put the current verifier and exact evidence before the historical navigation.

## Review 2 — result and acceptance rule

The second review is executable as:

```bash
uv run --frozen --no-dev python release/audit_candidate.py
```

It begins only at candidate README/logbook, records every page opened, requires
all nine visibility columns and six claim rows, verifies every linked current
contract/source/verifier, runs the evaluator-visible cumulative verifier,
proves the old 17-file set is preserved, and checks the exact UTF-8 upload
manifest for secrets. Any missing conclusion exits nonzero.

The short one-core structural pass opened 19 canonical/historical pages,
discovered 89 linked local files, mapped all 17 judged files, checked 110
allowlisted UTF-8 files, and found zero secret-pattern matches.

Final evaluator-blind traversal result: **PASS**. The same audit, including the
six-claim scientific verifier omitted from this short local pass, must pass in
the immutable managed HF CPU regression before publication.
