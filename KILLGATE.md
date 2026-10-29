# KILLGATE — numtrace

Per-gate verdicts (gate sequence followed in order, none skipped/reordered).

- Gate 0 (harness): PASS — deterministic scripted harness, no LLM anywhere;
  pytest 6 passed; re-run of seed 555 byte-identical, SHA-256
  d9a41e88a07880e237ef73301b863a69d709abf1be84f3fc847f6d8faa18574f
  (results-head2head-555.json).
- Gate 1 (author-code recheck, 2026-10-29): PASS (no kill) — arXiv abs page
  for 2610.34887 (fetched live 2026-10-29) lists no code/data repository in
  its "Code, Data and Media" section; web + GitHub-targeted searches for
  NumTrace / the paper title returned no author repository (only the paper
  itself and unrelated projects). Clean-room build therefore proceeded.
- Pilot-calibrate: PASS — seed 101, n_group=120, n_direct=80: naive
  value 1.000, joint 0.000, RNWA 1.000, RNWA share of failures 1.000.
  Disease exhibitable at scripted scale; no scope kill.
- PREREG lock: DONE before head-to-head (PREREG.md, seeds 555/556/557,
  n_group=300, n_direct=200). One pre-lock fix logged there: naive first-hit
  can accidentally be right on single-member groups, so disease is a rate.
- Gate 2 (disease, primary seed 555): PASS — naive value 1.000, joint 0.000,
  RNWA 1.000 (>= 0.50 bar), value-joint gap 1.000, paired bootstrap 95% CI
  [1.000, 1.000] (lower bound > 0), RNWA share of failures 1.000 (>= 0.50).
  Replication seeds 556/557 identical on all G2 bars.
- Gate 3 (load-bearing, primary seed 555): PASS — traced joint 1.000 vs
  naive joint 0.000, gain 1.000, paired bootstrap 95% CI [1.000, 1.000]
  (lower bound > 0, >= 0.50 bar); traced RNWA 0.000 (<= 0.10 bar);
  benign: traced direct joint 1.000 (>= 0.95), benign gap CI [0.000, 0.000]
  (lower bound 0.000 > -0.10). Replication seeds 556/557 identical.
- Overall: PASS — no kill triggered.

## Honest limitation (must travel with every number)
The bootstrap CIs are degenerate ([1.000, 1.000] / [0.000, 0.000]) because
the scripted agents are deterministic: every paired difference is identical.
The CIs therefore exclude 0 (and satisfy the preregistered bars) but carry
no sampling-width information. This is a property of a scripted analog, not
evidence about frontier LLM agents, and it is reported here rather than
hidden behind the CI numbers.
