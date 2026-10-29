# numtrace

An open, clean-room, synthetic analog of number-provenance auditing,
inspired by arXiv 2610.34887 (NumTrace: Auditing the Number Provenance of
Financial Analyst Agents, Zhu et al.). **This is not a reproduction of the
paper's results.** It uses no LLM, no real SEC EDGAR data, no real filings
and no real companies — only seeded synthetic records and scripted agents.

## The idea in one paragraph
A number can be real yet wrong: one firm's holding quoted as a whole
co-filing group's holding. Splitting the verdict into *value* (is the
number in the source / arithmetically right?), *binding* (does it refer to
the entity, concept, period, unit and scope claimed?) and *support* (do the
cited records back both?) exposes that failure as RNWA — right number,
wrong account. A scope-blind first-hit agent commits it constantly; an
agent that filters to the group's members, sums them, and asserts the group
scope does not.

## Measured table (preregistered; see PREREG.md, KILLGATE.md)

| seed | agent | n | value | joint | RNWA |
|------|-------|---|-------|-------|------|
| 555 | naive first-hit | 300 group Qs | 1.000 | 0.000 | 1.000 |
| 555 | traced filter+sum+binding | 300 group Qs | 1.000 | 1.000 | 0.000 |
| 556 / 557 | naive / traced | 300 group Qs | 1.000 / 1.000 | 0.000 / 1.000 | 1.000 / 0.000 |

- Value−joint (RNWA) gap: 1.000, paired bootstrap 95% CI [1.000, 1.000].
- Joint gain (traced − naive): 1.000, paired bootstrap 95% CI [1.000, 1.000].
- Benign utility (200 direct firm questions/seed): traced joint 1.000,
  benign gap CI [0.000, 0.000] — correct cases unbroken.
- Pilot (seed 101, 120 group Qs): naive value 1.000, joint 0.000, RNWA 1.000.
- Determinism: seed-555 re-run byte-identical, SHA-256
  `d9a41e88a07880e237ef73301b863a69d709abf1be84f3fc847f6d8faa18574f`.
- Tests: 6 passed (`PYTHONPATH=src python3 -m pytest tests/ -q`).

## Honest scope limits
Scripted agents on synthetic data; CIs are degenerate (zero width) because
paired differences are constant — they exclude 0 but carry no sampling
uncertainty. The paper's own figures (RNWA 67.5–81.8% of frontier-agent
failures; ~91% value vs <50% binding on 13F co-filing groups, on real
EDGAR data) are **not** reproduced or claimed here.

## Run it (CPU only, $0, no network)
```bash
PYTHONPATH=src python3 -m pytest tests/ -q
PYTHONPATH=src python3 -m numtrace.run_experiment --seed 555 \
  --n-group 300 --n-direct 200 --out results-head2head-555.json
```

## Layout
- `src/numtrace/data.py` — seeded synthetic corpus generator
- `src/numtrace/agents.py` — scripted naive / traced / exact agents
- `src/numtrace/audit.py` — value / binding / support verdicts, RNWA
- `src/numtrace/stats.py` — paired bootstrap CIs
- `src/numtrace/run_experiment.py` — experiment runner
- `PREREG.md`, `KILLGATE.md`, `PAPER.md`, `LINKEDIN_DRAFT.md`
- `results-pilot.json`, `results-head2head-555/556/557.json`

License: MIT (see LICENSE).
