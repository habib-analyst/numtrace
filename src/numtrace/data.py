"""Synthetic corpus generation (deterministic, seeded).

Universe
--------
- GROUPS: synthetic co-filing groups, each with 1-5 member firms.
- Each member firm holds a number of shares of one synthetic ticker in a period.
- A group question asks for the GROUP TOTAL of one ticker in one period.
  Reference = sum of that group's member holdings for that ticker/period.
- A direct question asks for ONE firm's holding (benign / exact-binding case).

Invariants enforced by construction (and tested):
- Every holding is a distinct positive integer within a (ticker, period) slice,
  so no single-firm value can accidentally equal a multi-member group total
  (all holdings positive, so a multi-member total strictly exceeds each part).
- Group totals are therefore never equal to any single record value.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Record:
    firm: str
    group: str
    ticker: str
    period: str
    shares: int
    doc_id: str


@dataclass(frozen=True)
class GroupQuestion:
    qid: str
    group: str
    ticker: str
    period: str
    reference: int  # group total
    member_firms: tuple


@dataclass(frozen=True)
class DirectQuestion:
    qid: str
    firm: str
    ticker: str
    period: str
    reference: int


def generate(seed: int, n_group: int = 300, n_direct: int = 200):
    """Return (records, group_questions, direct_questions), fully deterministic."""
    rng = random.Random(seed)
    tickers = ["SYN-A", "SYN-B", "SYN-C", "SYN-D"]
    periods = ["2025Q4", "2026Q1"]
    records: list[Record] = []
    group_questions: list[GroupQuestion] = []
    direct_questions: list[DirectQuestion] = []

    # Groups: 80% multi-member (2-5), 20% single-member, in fixed pattern order
    # shuffled only by the seeded rng for document order (candidate order).
    groups: dict[str, list[str]] = {}
    gid = 0
    n_groups = max(20, n_group // 6)
    for i in range(n_groups):
        gid += 1
        gname = f"GROUP-{gid:03d}"
        n_members = 1 if (i % 5 == 4) else rng.randint(2, 5)
        groups[gname] = [f"FIRM-{gid:03d}-{j}" for j in range(n_members)]

    # Holdings: distinct values per (ticker, period) via a shuffled pool.
    pool_base = list(range(100, 100_000, 7))
    for ticker in tickers:
        for period in periods:
            rng.shuffle(pool_base)
            pool = iter(pool_base)
            for gname, firms in groups.items():
                for firm in firms:
                    shares = next(pool)
                    records.append(Record(
                        firm=firm, group=gname, ticker=ticker, period=period,
                        shares=shares,
                        doc_id=f"DOC-{ticker}-{period}-{gname}-{firm}",
                    ))
    # Document order for the naive first-hit agent: seeded shuffle of records.
    rng.shuffle(records)

    by_group_ticker_period: dict[tuple, list[Record]] = {}
    for r in records:
        by_group_ticker_period.setdefault((r.group, r.ticker, r.period), []).append(r)

    # Group questions: sample (group, ticker, period) combos deterministically.
    combos = sorted(by_group_ticker_period.keys())
    rng.shuffle(combos)
    for k in range(n_group):
        gname, ticker, period = combos[k % len(combos)]
        members = by_group_ticker_period[(gname, ticker, period)]
        total = sum(r.shares for r in members)
        group_questions.append(GroupQuestion(
            qid=f"G-{k:04d}", group=gname, ticker=ticker, period=period,
            reference=total, member_firms=tuple(r.firm for r in members),
        ))
    # Direct questions: exact firm lookups.
    rng.shuffle(records)
    for k in range(n_direct):
        r = records[k % len(records)]
        direct_questions.append(DirectQuestion(
            qid=f"D-{k:04d}", firm=r.firm, ticker=r.ticker, period=r.period,
            reference=r.shares,
        ))
    return records, group_questions, direct_questions
