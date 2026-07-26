# Evaluator-blind pre-publication review

The reviewer was restricted to this downloaded candidate and the rubric. It
started at README/logbook and received no hint about evidence locations.

## First traversal

Opened: README, current index, visibility matrix, verification page, Claims
1–6, historical page, and visual report.

Missing conclusions:

1. The original candidate `logbook.json` had a stale trailing fragment.
2. Reproducibility metadata was not inline on every claim page.
3. The exact upload allowlist, current manifest, release report, and
   historical-subset mapping were absent.

Those items were treated as missing evidence, not supplied from the research
repository.

## Fix and repeated traversal

The JSON fragment was removed; every claim gained its exact command, pinned
environment, Git SHA, seed policy, CPU/runtime, contract, and source links.
The [release report](#/release-report), [upload allowlist](../../upload_allowlist.txt),
and [manifest](../../manifest.sha256) were added.

The repeat review is fail-closed and executable:

```bash
uv run --frozen --no-dev python -m reproduction.run_all
```

It records every opened page, requires the complete six-row visibility matrix,
runs all current verifiers, maps all 17 judged hashes into the candidate, and
scans every upload file for secrets.

The repeated short structural traversal opened 19 pages, discovered 89 linked
files, mapped all 17 judged files, checked 110 allowlisted UTF-8 files, and
found zero secret-pattern matches. Evaluator-blind traversal: **PASS**. The
same audit, including the scientific verifier omitted from the short local
pass, must pass on managed HF CPU before publication.
