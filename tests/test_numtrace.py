import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from numtrace import agents, audit
from numtrace.data import generate
from numtrace.run_experiment import run


def test_determinism_same_seed():
    a = generate(42, 50, 20)
    b = generate(42, 50, 20)
    assert a == b


def test_group_total_exceeds_parts():
    records, gqs, _ = generate(42, 100, 10)
    for q in gqs:
        parts = [r.shares for r in records if r.group == q.group
                 and r.ticker == q.ticker and r.period == q.period]
        assert sum(parts) == q.reference
        if len(parts) > 1:
            assert all(p < q.reference for p in parts)


def test_naive_group_claim_is_rnwa_or_wrong_binding():
    # Pre-lock fix (found by G0 tests, before any head-to-head): the naive
    # first-hit agent CAN accidentally be right when the asked group is
    # single-member and the first candidate happens to be that firm. So the
    # disease is a rate claim, not a per-claim absolute: value pass is
    # universal, joint pass is rare, RNWA dominates.
    records, gqs, _ = generate(7, 60, 5)
    verdicts = [audit.audit_group_claim(agents.naive_group(records, q), records, q)
                for q in gqs]
    assert all(v.value for v in verdicts)
    assert sum(v.rnwa for v in verdicts) / len(verdicts) > 0.8
    assert sum(v.joint for v in verdicts) / len(verdicts) < 0.2


def test_traced_group_always_joint():
    records, gqs, _ = generate(7, 60, 5)
    for q in gqs:
        v = audit.audit_group_claim(agents.traced_group(records, q), records, q)
        assert v.value and v.binding and v.support and v.joint


def test_direct_exact():
    records, _, dqs = generate(7, 10, 30)
    for q in dqs:
        v = audit.audit_direct_claim(agents.exact_direct(records, q), records, q)
        assert v.joint


def test_run_repeatable():
    assert run(123, 50, 20) == run(123, 50, 20)
