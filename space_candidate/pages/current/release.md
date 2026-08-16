# Release forecast and evidence ledger

Previous live judged score: `4/12`

Conservative projected score range after the proposed change: **8–10/12**

Best-supported possible new score: **10/12 (forecast only; not a judge result)**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 1 | 2 | HIGH | VERIFIED | Algorithms 1–6 execute and independent transition/operation checks plus six defect controls pass; this verifies the constructive framework, not convergence or CIFAR-10 performance |
| 2 | 0 | 2 | HIGH | FALSIFIED | An assumption-satisfying exact case has zero gradient error at time 0 for every tolerance, contradicting the strict necessary-positive-time interpretation |
| 3 | 1 | 2 | HIGH | FALSIFIED | An exact admissible stochastic instance needs `Omega(epsilon^-2 log(1/epsilon))` last-iterate work; independent calibration and zero-variance control isolate the mechanism |
| 4 | 1 | 0 | LOW | BLOCKED | Three verification routes and the mandatory fourth falsification route are complete; neither a valid proof nor an assumption-satisfying super-`epsilon^-4` Algorithm-3 family is available |
| 5 | 0 | 2 | MEDIUM | FALSIFIED | The authors' complete exact Figure 6 vectors contradict strict all-setting dominance; risk remains because the paper's literal prose is qualitative and no independent retraining was possible from the incomplete official release |
| 6 | 1 | 2 | HIGH | VERIFIED | A universal symbolic KL identity has zero residual and continuous non-Gaussian checks plus a wrong-temperature control independently regress coefficients and signs |

## Totals and interpretation

- Current live total: **4/12**
- Conservative projected total: **8–10/12**
- Best-supported possible total: **10/12**
- Changed since the previous judge result: Claims 1 and 6 move from toy
  evidence to proof/conformance evidence; Claims 2, 3, and the strict Claim 5
  wording receive direct falsifications; Claim 4 is downgraded from a toy
  formula product to an honest BLOCKED result.
- Remaining BLOCKED claim: Claim 4. It requires either a correct proof of the
  version-1 Algorithm-3 upper bound or a rigorous entropy-DRO direct-product
  construction combining a hard stochastic outer oracle with unavoidable
  inner ULA work.
- Exact publication action: upload only the paths in
  `space_candidate/upload_allowlist.txt`, through the text-only Hugging Face
  commit API, to the existing Space `DineshAI/QRtzkKrbJi`; then download the
  returned revision, verify every manifest hash and canonical link, mark it
  awaiting the live judge, and mirror the published text to GitHub `main`.

## Experiment tree and winning evidence

The tree is stacked: a frozen root, followed by one promoted child per exact
claim, followed by a release-only child.

| Node | Branch | Git SHA | Managed result |
|---|---|---|---|
| Judged control | `orx/judged-4-of-12-baseline` | `a719ad2657a5f12cb03de181606dac1d63197347` | Historical 4/12 state protected |
| Claim 6 | `orx/claim-6-continuous-half-bridge-certificate` | `11396183ec4d725d75881cd87341a84d772e0287` | VERIFIED |
| Claim 2 | `orx/claim-2-necessary-time-counterexample` | `24660fdaf03faf172e40fd65996ea826726dfbf3` | FALSIFIED |
| Claim 3 | `orx/claim-3-stochastic-outer-loop-lower-bound` | `d3dea06ec215a5f1519475ab411b97d60775bc74` | FALSIFIED |
| Claim 4 | `orx/claim-4-four-route-complexity-audit` | `eb33b37c727036d98a6b78ffab80f67c98bcc591` | BLOCKED |
| Claim 1 | `orx/claim-1-six-algorithm-conformance-suite` | `a8c56d4634f75a17cd9a8812ebd43b79c27cd228` | VERIFIED |
| Claim 5 / winning scientific evidence | `orx/claim-5-exact-figure-6-vector-falsification` | `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7` | FALSIFIED; all earlier claims rerun |
| Release candidate | `orx/evaluator-visible-cumulative-release-candidate` | `04f9bbb5081236a27139b433363fe3b8ddc3490e` | PASS; all claims plus visibility/release gates |

The fixed command on every node is:

```bash
uv run --frozen --no-dev python -m reproduction.run_all
```

## Compute and cost

All managed jobs used Hugging Face `cpu-upgrade`; no GPU was requested or
used. The jobs exposed 64 logical CPUs, while each scientific verifier was
single-process. Successful managed durations were 26, 26, 32, 32, 32, 32, and
37 seconds through Claim 5. The final Claim-5 cumulative scientific runtime was
8.479088 seconds. One 10-second baseline preflight failed because the first
container image lacked `uv`; no scientific result was produced, and the
successful rerun used `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.
The release regression took 42 managed seconds and 14.535772 seconds in the
cumulative verifier. Hugging Face monetary billing is not exposed by `orx`,
so no unsupported cost amount is claimed.

## Evidence paths

- Exact internal contracts and checkers:
  `.openresearch/artifacts/claim_1/` through
  `.openresearch/artifacts/claim_6/`
- Evaluator-visible candidate: `space_candidate/`
- Canonical candidate page: `space_candidate/pages/current/index.md`
- Visibility matrix: `space_candidate/pages/current/visibility.md`
- Evaluator-blind review: `space_candidate/pages/current/red-team.md`
- Historical judged revision:
  `historical/judged_space_735012f52396955c5734e8fc568adfdf2abda757/`
- Illustrated report: `reports/reproduction/report.md`
- Tutorial notebook: `notebooks/gfs_dro_reproduction.py`

## Historical subset, visibility, and release safety

The exact judged tree contains 17 files. The release audit requires every old
hash either at its unchanged path or at the protected revision-qualified path;
README and logbook copies are protected because their root versions now point
to current evidence. Old pages and assets remain byte-identical at their
original paths. The current verifier precedes all historical navigation.

The upload is text-only and exact: the sorted allowlist and SHA-256 manifest
are generated from `space_candidate/`, checked for UTF-8 decodability, and
scanned for token/private-key patterns. The canonical traversal begins only at
README/logbook, records every opened page, and requires all six rows of the
specified visibility matrix.

## Command ledger

The campaign's material commands, in execution order, were:

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 3e4dc845-5628-4f69-acd4-bf91bf9af239
git branch -a
git status --short
git rev-parse HEAD
curl -A "OpenResearch-Reproduction/1.0" -L https://arxiv.org/pdf/2510.25956v1
orx paper 2510.25956 --full
uv lock
orx create-experiment 3e4dc845-5628-4f69-acd4-bf91bf9af239 --title "Judged 4-of-12 baseline" --run-command "uv run --frozen --no-dev python -m reproduction.run_all"
orx exp run 62c063cf-d4e6-432f-b849-dc065814ac63 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait 62c063cf-d4e6-432f-b849-dc065814ac63 --timeout 480
orx logs 11788b06-67e9-43b8-ab1b-130ebc6690bb
orx exp run <each promoted claim node> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait <each promoted claim node> --timeout 480
orx logs <each completed managed run id>
uv run --frozen --no-dev marimo check notebooks/gfs_dro_reproduction.py
uv run --frozen --no-dev python release/build_space_release.py
uv run --frozen --no-dev python release/audit_candidate.py
orx exp run 7b0884c8-8299-453c-a218-d2fcb6da257e --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait 7b0884c8-8299-453c-a218-d2fcb6da257e --timeout 480
orx logs 715d6e79-9b83-4da7-9fda-d7252ea7e0e8 --bytes 100000
hf upload DineshAI/QRtzkKrbJi <exact-staging-directory> . --repo-type space --commit-message "Exact claim audit with cumulative evidence" --format json
HfApi.create_commit(repo_id="DineshAI/QRtzkKrbJi", repo_type="space", parent_commit="735012f52396955c5734e8fc568adfdf2abda757", operations=<110 manifest-verified text additions>)
hf download DineshAI/QRtzkKrbJi <110 allowlisted paths> --repo-type space --revision f519e2341f486db7539b161e1929b78a1ff3d01f --max-workers 1
uv run --frozen --no-dev python release/audit_candidate.py --structure-only --candidate-dir <fresh-published-download>
git merge --ff-only orx/evaluator-visible-cumulative-release-candidate
git push origin main
git ls-remote origin refs/heads/main refs/heads/orx/evaluator-visible-cumulative-release-candidate
```

The generic `hf upload` attempt made no commit because its internal
repository-creation preflight was rate-limited. Publication therefore used the
listed direct existing-repository `HfApi.create_commit` call, with the judged
revision as the required parent and no token printed or passed on the command
line.

The per-node exact IDs, immutable run IDs, commands, results, and actual
durations remain in `orx exp desc`, `orx runs`, and `orx logs`; the report does
not substitute unpublished logs for evaluator-visible evidence.

## Pre-upload summary

| Claim | Status | Expected points | Confidence | Expected evaluator status |
|---|---|---:|---|---|
| 1 | VERIFIED | 2 | HIGH | Full credit supported |
| 2 | FALSIFIED | 2 | HIGH | Full credit supported |
| 3 | FALSIFIED | 2 | HIGH | Full credit supported |
| 4 | BLOCKED | 0 | LOW | No increase supported |
| 5 | FALSIFIED | 2 | MEDIUM | Full credit supported for strict judged wording; interpretation risk |
| 6 | VERIFIED | 2 | HIGH | Full credit supported |

Conservative projected total: **8–10/12**. Best-supported possible total:
**10/12**. Claim 4 is the remaining BLOCKED risk.

Publication state at the uploaded revision: **AWAITING LIVE JUDGE**. This state
becomes active only after the managed release regression passes and the
revision is actually published.

Published Hugging Face revision:
`f519e2341f486db7539b161e1929b78a1ff3d01f`. Post-publication verification
compared all 110 uploaded files with zero mismatches, repeated the canonical
19-page traversal, preserved 17/17 judged files, and checked 37 displayed
numbers against raw data.
