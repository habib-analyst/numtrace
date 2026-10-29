"""Scripted agents only. No LLM, no retrieval model, no learned component.

- naive_agent: scope-blind first-hit. For a group question it takes the FIRST
  record (in shuffled document order) matching ticker+period, whatever group
  it belongs to, and reports it as the group's total. This is the disease
  agent: the number is real (in-source) but the scope is wrong.
  For a direct question it does the exact firm lookup (binding already exact).
- traced_agent: provenance mechanism under test. For a group question it
  filters records to the asked group's members, SUMS them, asserts the group
  scope, and cites exactly those member records (binding check: the answer
  must be the group total, not any single record). For a direct question it
  does the same exact firm lookup as the control, so any benign difference
  would be caused by the mechanism itself.
"""
from __future__ import annotations

from .audit import Claim


def naive_group(records, question) -> Claim:
    cands = [r for r in records
             if r.ticker == question.ticker and r.period == question.period]
    first = cands[0]
    return Claim(value=first.shares, asserted_scope=f"{question.group} total",
                 citations=(first.doc_id,))


def traced_group(records, question) -> Claim:
    members = [r for r in records if r.group == question.group
               and r.ticker == question.ticker and r.period == question.period]
    total = sum(r.shares for r in members)
    return Claim(value=total, asserted_scope=f"{question.group} total",
                 citations=tuple(r.doc_id for r in members))


def exact_direct(records, question) -> Claim:
    r = next(r for r in records if r.firm == question.firm
             and r.ticker == question.ticker and r.period == question.period)
    return Claim(value=r.shares, asserted_scope=question.firm,
                 citations=(r.doc_id,))
