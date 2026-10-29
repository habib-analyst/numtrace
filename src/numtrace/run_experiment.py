"""Run one head-to-head (or pilot) experiment and emit JSON + a text table.

Usage: python3 -m numtrace.run_experiment --seed S --n-group N --n-direct M
         --tag pilot|head2head --out results-<tag>.json
Deterministic: same seed + same code -> byte-identical JSON (sorted keys,
fixed float rounding). No network, no LLM, CPU only.
"""
from __future__ import annotations

import argparse
import json

from . import agents, audit
from .data import generate
from .stats import paired_bootstrap_ci, rate


def run(seed: int, n_group: int, n_direct: int):
    records, gqs, dqs = generate(seed, n_group, n_direct)
    naive_v, traced_v = [], []
    naive_joint, traced_joint, naive_value, traced_value = [], [], [], []
    for q in gqs:
        nv = audit.audit_group_claim(agents.naive_group(records, q), records, q)
        tv = audit.audit_group_claim(agents.traced_group(records, q), records, q)
        naive_v.append(nv); traced_v.append(tv)
        naive_joint.append(int(nv.joint)); traced_joint.append(int(tv.joint))
        naive_value.append(int(nv.value)); traced_value.append(int(tv.value))
    benign_naive, benign_traced = [], []
    for q in dqs:
        nv = audit.audit_direct_claim(agents.exact_direct(records, q), records, q)
        tv = audit.audit_direct_claim(agents.exact_direct(records, q), records, q)
        benign_naive.append(int(nv.joint)); benign_traced.append(int(tv.joint))

    rnwa = [int(v.rnwa) for v in naive_v]
    naive_fail = [i for i, v in enumerate(naive_v) if not v.joint]
    rnwa_share_fail = (sum(rnwa[i] for i in naive_fail) / len(naive_fail)
                       if naive_fail else 0.0)
    out = {
        "seed": seed, "n_group": len(gqs), "n_direct": len(dqs),
        "naive_value_rate": round(rate(naive_value), 4),
        "naive_joint_rate": round(rate(naive_joint), 4),
        "naive_rnwa_rate": round(rate(rnwa), 4),
        "naive_rnwa_share_of_failures": round(rnwa_share_fail, 4),
        "naive_failures": len(naive_fail),
        "traced_value_rate": round(rate(traced_value), 4),
        "traced_joint_rate": round(rate(traced_joint), 4),
        "traced_rnwa_rate": round(
            rate([int(v.rnwa) for v in traced_v]), 4),
        "benign_naive_joint_rate": round(rate(benign_naive), 4),
        "benign_traced_joint_rate": round(rate(benign_traced), 4),
        "rnwa_gap_ci": [round(x, 4) for x in paired_bootstrap_ci(
            naive_value, naive_joint, seed=seed + 1)],
        "joint_gain_ci": [round(x, 4) for x in paired_bootstrap_ci(
            traced_joint, naive_joint, seed=seed + 2)],
        "benign_gap_ci": [round(x, 4) for x in paired_bootstrap_ci(
            benign_traced, benign_naive, seed=seed + 3)],
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n-group", type=int, default=300)
    ap.add_argument("--n-direct", type=int, default=200)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = run(args.seed, args.n_group, args.n_direct)
    with open(args.out, "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(res, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
