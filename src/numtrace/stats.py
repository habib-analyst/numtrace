"""Paired bootstrap 95% CIs (percentile method, seeded, deterministic)."""
from __future__ import annotations

import random


def paired_bootstrap_ci(a: list[int], b: list[int], reps: int = 10_000,
                        seed: int = 0):
    """CI for mean(a) - mean(b) over paired binary outcomes."""
    assert len(a) == len(b) and len(a) > 0
    rng = random.Random(seed)
    n = len(a)
    diffs = [x - y for x, y in zip(a, b)]
    boots = []
    for _ in range(reps):
        s = sum(rng.choice(diffs) for _ in range(n)) / n
        boots.append(s)
    boots.sort()
    lo = boots[int(0.025 * reps)]
    hi = boots[int(0.975 * reps) - 1]
    return (lo, hi)


def rate(xs: list[int]) -> float:
    return sum(xs) / len(xs) if xs else 0.0
