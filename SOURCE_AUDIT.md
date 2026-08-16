# Paper and source audit

## Pinned paper records

- Title: *Gradient Flow Sampler-based Distributionally Robust Optimization*
- Authors: Zusen Xu and Jia-Jie Zhu
- arXiv record: [2510.25956](https://arxiv.org/abs/2510.25956)
- v1 submitted: 2025-10-29
- v3 revised: 2026-05-25
- OpenReview record: [QRtzkKrbJi](https://openreview.net/forum?id=QRtzkKrbJi)
- Audit retrieval date: 2026-08-16

The exact judged contract is v1. Current v3 is retained as a version-drift
comparison in <code>sources/paper/source_audit.md</code>.

## Pinned artifact hashes

| Artifact | URL | SHA-256 |
| --- | --- | --- |
| <code>paper_2510.25956v1.pdf</code> | <https://arxiv.org/pdf/2510.25956v1> | <code>796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6</code> |
| <code>paper_2510.25956v3.pdf</code> | <https://arxiv.org/pdf/2510.25956v3> | <code>88720453447d8affcefd3e63097c52f512d5b275766ba3e73dff9af2ca1c0f8f</code> |
| <code>source/arxiv/2510.25956v1.tar</code> | <https://arxiv.org/e-print/2510.25956v1> | <code>35a471bd60c11517db90b8e337064019c5a07faa621718aeca9800d425604488</code> |
| judged verdict snapshot | <code>sources/judge/verdict.json</code> | recorded in <code>sources/paper/source_manifest.json</code> |

The full v1/v2/v3, arXiv API, official-code, and judge-dataset provenance is
retained in [sources/paper/source_manifest.json](sources/paper/source_manifest.json)
and [sources/paper/source_audit.md](sources/paper/source_audit.md).

## Claim anchors

- C1: Sections 3.2 and Appendix B, Algorithms 1–6
- C2: Section 4, Proposition 1, Appendix C.2
- C3: Section 5, Theorem 1, Appendix C.3
- C4: Section 5, Theorem 2, Appendix C.4
- C5: Section 6.3, Figure 6
- C6: Section 3.1, Lemma 1, Appendix C.1

No later source version is silently substituted for the v1 judged claims.
