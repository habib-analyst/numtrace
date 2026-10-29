# numtrace: a clean-room synthetic analog of number-provenance auditing

## What the paper does (restated in our own words from the live abstract)
NumTrace (Zhu, White, Liu & Liu, arXiv 2610.34887, submitted 26 Oct 2026)
audits financial-analyst agents not just on whether a number they quote is
right, but on what that number *refers to*. A quoted number can match a
number in a filing yet belong to the wrong entity, concept, period, unit or
scope — e.g. one firm's holding reported as a whole co-filing group's
holding. The benchmark (540 questions over 2,163 SEC EDGAR documents,
covering Form 13F holdings and Item 402(i) executive deferred compensation)
therefore gives every numerical claim three separate verdicts — value,
binding and support — and defines an RNWA ("right number, wrong account")
error as passing value while failing binding. The paper's headline
measurements (NOT reproduced here): RNWA errors are 67.5–81.8% of each
audited agent's failing claims, and on 13F co-filing group questions about
91% of claims pass value but fewer than half pass binding.

## What we built instead (and what we did NOT do)
A fully synthetic, scripted analog at CPU scale. No LLM, no frontier agent,
no real EDGAR data, no real filings, no real companies or tickers. Groups,
firms, tickers, periods and holdings are generated from a seed. Two scripted
agents answer group-total questions: a scope-blind first-hit agent (the
disease control) and a traced agent that filters to the group's members,
sums them, asserts group scope and cites exactly those records (the
mechanism). A third verdict split — value / binding / support — is
implemented from scratch in `src/numtrace/audit.py`.

## Measured results (head-to-head, preregistered in PREREG.md)

| seed | agent | n_group | value | joint | RNWA | RNWA share of failures |
|------|-------|---------|-------|-------|------|------------------------|
| 555 (primary) | naive first-hit | 300 | 1.000 | 0.000 | 1.000 | 1.000 |
| 555 (primary) | traced (filter+sum+binding check) | 300 | 1.000 | 1.000 | 0.000 | — |
| 556 | naive / traced | 300 | 1.000 / 1.000 | 0.000 / 1.000 | 1.000 / 0.000 | 1.000 / — |
| 557 | naive / traced | 300 | 1.000 / 1.000 | 0.000 / 1.000 | 1.000 / 0.000 | 1.000 / — |

- G2 disease: value−joint gap 1.000, paired bootstrap 95% CI [1.000, 1.000].
- G3 load-bearing: joint gain (traced − naive) 1.000, paired bootstrap 95%
  CI [1.000, 1.000].
- Benign utility (n_direct = 200 direct firm questions per seed): traced
  joint 1.000, naive joint 1.000, benign gap CI [0.000, 0.000] — the
  mechanism does not break already-correct exact-binding cases.
- Pilot (seed 101, n_group=120): value 1.000, joint 0.000, RNWA 1.000.
- Determinism: seed-555 re-run byte-identical; SHA-256
  d9a41e88a07880e237ef73301b863a69d709abf1be84f3fc847f6d8faa18574f.
- Tests: 6 passed (pytest).

## Scope limits — read before citing any number above
1. Scripted agents, not LLM agents: the "disease" here is a retrieval
   rule (first-hit), not a model behaviour. Magnitudes (RNWA 1.000) are
   far more extreme than the paper's and must never be quoted as the
   paper's figures or as evidence about Claude/GPT/DeepSeek.
2. Degenerate CIs: because both agents are deterministic, every paired
   difference is identical, so bootstrap CIs have zero width. They satisfy
   the preregistered "excludes 0" bars but convey no sampling uncertainty.
3. Synthetic data: group totals are exact sums by construction, so the
   traced agent is correct by construction once it filters correctly. The
   load-bearing claim is narrow: *scope filtering + summation + a binding
   assertion removes the first-hit failure mode in this analog* — nothing
   broader.
4. No author code was found at check time (Gate 1); if the authors later
   release code/data, a direct comparison should replace this analog.
