# Claim 4 exact source audit

The judged source is arXiv `2510.25956v1`, PDF SHA-256
`796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`.
Theorem 2 is in Section 5, PDF page 8 (plain-text line 527). Appendix C.4
derives it on PDF page 19 (lines 1314-1363).

The derivation multiplies three factors:

- v1 Theorem 1 outer iterations `S=O(epsilon_opt^-2)`;
- ULA inner iterations `T=soft-O(epsilon_opt^-2)`;
- an `O(d)` inner-gradient cost.

The resulting `epsilon_opt^-4` exponent therefore depends directly on the
Claim 3 rate falsified by the preceding exact counterexample.

Current arXiv v3, PDF SHA-256
`88720453447d8affcefd3e63097c52f512d5b275766ba3e73dff9af2ca1c0f8f`,
changes the outer factor to `epsilon_opt^-4` and Theorem 5.5 total complexity
to `epsilon_opt^-6`. Its acknowledgment says Jie Wang pointed out a flaw in
the original proof of Theorem 5.5 and that the authors fixed it.

That is strong evidence that the v1 derivation is invalid. It is not, by
itself, a mathematical counterexample to the old upper bound: a theorem can
have a broken proof and still be true. The exact contract therefore remains
BLOCKED unless a valid instance lower-bounds Algorithm 3 above
`soft-O(epsilon_opt^-4)`.
