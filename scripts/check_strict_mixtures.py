"""Strict stability and positive definite covariance at no cost to the suprema.

Mix the explicit worst-case law at a slightly larger ratio r' with weight 1-eps
and, with weight eps, a fixed symmetric law X^s whose atoms are +-s(e_i - e_j)
for all pairs and +-zeta*1. Costs of centrally symmetric laws mix linearly,
so every proper coalition becomes strictly stable, the covariance becomes
positive definite, and the grand cost stays at most one. r' is chosen so that
the standalone caps still hold at r. As eps -> 0 the mixed gap tends to the
worst gap at r, because the closed forms are continuous in r.
Each mixed law is evaluated with ExclusionEnvelope and coalition_table.
"""

import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exact_envelopes import (
    best_equal_share_construction, last_depth_construction,
)
from censored_newsvendor.exclusion import ExclusionEnvelope

ROOT = Path(__file__).resolve().parents[1]


def strict_atoms(n):
    """Atoms and probabilities of X^s, scaled so every proper coalition is strict."""
    s, zeta = n / 2 + 1, 0.05
    atoms, probabilities = [], []
    pairs = list(itertools.combinations(range(n), 2))
    for i, j in pairs:
        v = np.zeros(n)
        v[i], v[j] = s, -s
        atoms += [v, -v]
        probabilities += [0.45 / len(pairs)] * 2
    atoms += [np.full(n, zeta), np.full(n, -zeta)]
    probabilities += [0.05, 0.05]
    return np.array(atoms), np.array(probabilities)


def cost(atoms, probabilities, x):
    return float(probabilities @ np.abs(atoms @ x))


def mixed_case(label, shares, r, depth, base, eps):
    a = np.array([float(x) for x in shares])
    n = len(a)
    s_atoms, s_prob = strict_atoms(n)
    strict_caps = np.array([cost(s_atoms, s_prob, np.eye(n)[j]) for j in range(n)])
    r_prime = (1 - eps) / min(1 / r - eps * strict_caps / a)
    construction = base(F(r_prime).limit_denominator(10**9))
    g = np.array([[float(x) for x in v] for v in construction["generators"]])
    m = len(g)
    atoms = np.vstack([m * g, -m * g, s_atoms])
    probabilities = np.concatenate([np.full(2 * m, (1 - eps) / (2 * m)), eps * s_prob])
    totals = atoms.sum(axis=1)
    lo, hi = 0.0, float(np.abs(totals).max()) + 2
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if probabilities @ np.abs(mid - totals) < 1 else (lo, mid)
    offer = (lo + hi) / 2 if probabilities @ np.abs(totals) < 1 else 0.0
    radius = float(np.abs(atoms).max())
    states = 0.5 + atoms / (2 * radius)
    rule = FrozenRule(n / 2 + offer / (2 * radius), a, np.ones(n))
    law = FiniteLaw(states, probabilities)
    grand = float(probabilities @ np.abs(rule.offer - states.sum(axis=1)))
    upper = ExclusionEnvelope.population(rule, law).level(depth)["upper"]
    table = coalition_table(rule, law)
    largest = max(row["excess"] for row in table)
    singles = [row["cost"] for row in table if len(row["coalition"]) == 1]
    rho = min([1.0] + [grand * w / c for w, c in zip(a, singles)])
    centered = states - probabilities @ states
    covariance = (centered * probabilities[:, None]).T @ centered
    return {"label": label, "n": n, "depth": depth, "r": r, "eps": eps, "r_prime": r_prime,
            "gap": (upper - max(0.0, largest)) / grand, "target": float(construction["value"]),
            "largest_excess_over_L": largest / grand, "rho": rho,
            "min_cov_eigenvalue": float(np.linalg.eigvalsh(covariance).min()), "atoms": len(probabilities)}


def main():
    cases = [
        ("four equal shares, window", [F(1, 4)] * 4, .25, 1,
         lambda r: best_equal_share_construction(4, r, 1), F(31, 56)),
        ("five equal shares, window", [F(1, 5)] * 5, .4, 1,
         lambda r: best_equal_share_construction(5, r, 1), None),
        ("four equal shares, high regime", [F(1, 4)] * 4, .6, 1,
         lambda r: best_equal_share_construction(4, r, 1), F(4, 15)),
        ("three unequal shares", [F(3, 5), F(1, 4), F(3, 20)], .2, 1,
         lambda r: last_depth_construction([F(3, 5), F(1, 4), F(3, 20)], r), F(17, 28)),
    ]
    rows = []
    for label, shares, r, depth, base, exact in cases:
        for eps in (.05, .01, .002):
            row = mixed_case(label, shares, r, depth, base, eps)
            row["exact_at_r"] = float(exact) if exact is not None else float(base(F(r).limit_denominator(1000))["value"])
            assert row["largest_excess_over_L"] < 0, row
            assert row["min_cov_eigenvalue"] > 0 and row["rho"] >= r - 1e-9, row
            rows.append(row)
    sources = [Path(__file__).resolve(), ROOT / "src/censored_newsvendor/exact_envelopes.py"]
    payload = {"date": "2026-11-06",
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/strict_mixtures.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    lines = ["# Strictly stable, positive definite mixtures", "",
             "2026-11-06. Argument: [docs/exact_envelopes.md](../../docs/exact_envelopes.md), Section 7.", "",
             "Every mixed law below has strictly negative excess for every proper coalition, positive "
             "definite covariance and standalone ratio at least r; its gap approaches the exact worst gap "
             "as eps shrinks.", "",
             "| case | r | eps | gap of the mixed law | exact worst gap | largest excess / L | "
             "min covariance eigenvalue |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in rows:
        lines.append(f"| {row['label']} | {row['r']:.2f} | {row['eps']:.3f} | {row['gap']:.6f} | "
                     f"{row['exact_at_r']:.6f} | {row['largest_excess_over_L']:.2e} | {row['min_cov_eigenvalue']:.2e} |")
    lines += ["", "Reproduce: `python scripts/check_strict_mixtures.py`.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"{len(rows)} mixed laws: all strictly stable with positive definite covariance.")


if __name__ == "__main__":
    main()
