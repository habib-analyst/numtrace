# PREREGISTRATION — numtrace (locked BEFORE head-to-head)

Locked: 2026-10-29, before any head-to-head run. Pilot (seed 101) was run
only to check exhibitable-ness; its numbers did NOT set these bars (bars are
deliberately far below the pilot's extreme values so they are not tuned to it).

## Design (frozen)
- Synthetic corpus only: synthetic groups/firms/tickers/periods/holdings.
  No real EDGAR data, no real filings, no real companies, no LLM anywhere.
- Agents are scripted: naive = scope-blind first-hit (control); traced =
  filter-to-group-members + sum + group-scope assertion + exact citations
  (mechanism under test). Direct questions use the exact firm lookup in both
  arms (benign set).
- Head-to-head seeds (fresh, never used in pilot/tests): 555 (primary),
  556, 557 (pre-registered replications). n_group = 300, n_direct = 200 each.
- Statistics: paired bootstrap 95% CIs, 10,000 reps, bootstrap seed =
  experiment seed + offset (1 = RNWA gap, 2 = joint gain, 3 = benign gap).
- Pre-lock design fixes (documented, before lock): G0 test correction —
  naive first-hit CAN accidentally be right on single-member groups, so the
  disease is stated as a rate, not a per-claim absolute. No code changes
  after lock except bug fixes that do not touch agents/audit/stats logic;
  any such fix must be logged here as an amendment with date.

## G2 disease bars (ALL must hold on primary seed 555)
- D1: naive RNWA rate >= 0.50
- D2: naive value-pass rate minus naive joint-pass rate >= 0.50, with paired
      bootstrap 95% CI lower bound > 0
- D3: RNWA share of naive failures >= 0.50
- Baseline comparison: the trivial baseline is the value-only reading —
  a value-only auditor would accept every RNWA claim as correct. D1/D2
  quantify exactly that gap; the sum-baseline (traced agent's arithmetic)
  is the G3 mechanism, not the G2 baseline, to avoid circularity.

## G3 load-bearing bars (ALL must hold on primary seed 555)
- L1: traced joint-pass rate minus naive joint-pass rate >= 0.50, with
      paired bootstrap 95% CI lower bound > 0
- L2: traced RNWA rate <= 0.10
- L3 (benign-utility bound): traced direct-question joint-pass rate >= 0.95
      AND benign paired gap (traced - naive) 95% CI lower bound > -0.10
      (the mechanism must not break already-correct exact-binding cases)
- Replication: L1-L3 must also hold in direction (same bars) on seeds 556
  and 557, else the claim is reported as primary-only, not robust.

## Kill conditions
- If any G2 bar fails on seed 555: KILL on G2 (disease not shown at
  pre-registered magnitude).
- If any G3 bar fails on seed 555: KILL on G3 (mechanism not load-bearing
  / breaks benign cases).
- Bars are never moved after head-to-head results are seen.

## Honest-scope note (carried into PAPER.md / README.md)
These are scripted-agent results on synthetic data. They demonstrate that
the RNWA failure mode and its tracing fix are exhibitable and measurable
in a clean-room analog. They do NOT reproduce the paper's figures
(67.5-81.8% RNWA share among frontier-agent failures on real EDGAR data,
91% value vs <50% binding on 13F co-filing groups), which used real filings
and frontier LLM agents we do not have and do not claim to replicate.
