"""Can general finite laws beat kappa-segment laws where the bound is not reached?

Exploratory local search (a heuristic, not a certificate). Under pinball loss
the cost of a finite law at a vector x is linear in the atom positions once
the order of the atoms along x is fixed, with the optimal offer at the atom
where the cumulative mass reaches tau. Fixing the order at every test vector
(singletons, proper coalitions, the grand coalition and the witness z)
therefore turns "best law in this order cell" into one LP, with the order
itself as linear constraints. Starting from the best kappa-segment law
(optimized over the witness as well), each hop perturbs the atoms, re-solves
the cell LP a few times and keeps any improvement that passes an independent
evaluation of the pinball costs.

Outcomes go to results/asymmetric/general_law_probe.json; the summary is
generated from that file.
"""

import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize

from censored_newsvendor.asymmetric import asymmetric_zonotope_minimal_cost, three_point_law
from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.seminorm_envelope import proper_coalitions

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/asymmetric"
CASES = [  # (label, shares, depth, kappa, r)
    ("equal shares, window", [0.25] * 4, 1, 1.2, 0.2405),
    ("equal shares, window", [0.25] * 4, 1, 1.1, 0.2538),
    ("arbitrary shares, seed 7591", None, 1, 1.5, 0.62),
]


def pinball(atoms, mass, x, tau):
    values = atoms @ x
    order = np.argsort(values, kind="stable")
    offer = values[order][np.searchsorted(np.cumsum(mass[order]), tau - 1e-12)]
    u = values - offer
    return float(mass @ np.where(u > 0, tau * u, -(1 - tau) * u))


def test_vectors(n, z):
    rows = [np.eye(n)[j] for j in range(n)]
    for s in proper_coalitions(n):
        if len(s) >= 2:
            v = np.zeros(n)
            v[list(s)] = 1.0
            rows.append(v)
    return np.array(rows + [np.ones(n), np.asarray(z, dtype=float)])


def evaluate(atoms, mass, a, r, tau, vectors):
    """Normalized gap and constraint slacks, with L = c(1)."""
    n = len(a)
    c = np.array([pinball(atoms, mass, x, tau) for x in vectors])
    grand = c[-2]
    caps = min(a[j] * grand / r - c[j] for j in range(n))
    stability = min(c[t] - (vectors[t] @ a) * grand for t in range(len(vectors) - 2))
    return (vectors[-1] @ a) - c[-1] / grand, grand, caps / grand, stability / grand


def cell_lp(atoms, mass, a, r, tau, vectors):
    count, n = atoms.shape
    width = count * n
    rows, rhs, costs = [], [], []
    for x in vectors:
        order = np.argsort(atoms @ x, kind="stable")
        k = int(np.searchsorted(np.cumsum(mass[order]), tau - 1e-12))
        pivot = order[k]
        row = np.zeros(width)
        for position, i in enumerate(order):
            weight = -(1 - tau) * mass[i] if position < k else tau * mass[i]
            row[i * n:(i + 1) * n] += weight * x
            row[pivot * n:(pivot + 1) * n] -= weight * x
        costs.append(row)
        for s in range(count - 1):
            order_row = np.zeros(width)
            order_row[order[s] * n:(order[s] + 1) * n] += x
            order_row[order[s + 1] * n:(order[s + 1] + 1) * n] -= x
            rows.append(order_row)
            rhs.append(0.0)
    rows.append(costs[-2])
    rhs.append(1.0)
    for j in range(n):
        rows.append(costs[j])
        rhs.append(a[j] / r)
    for t in range(len(vectors) - 2):
        rows.append(-costs[t])
        rhs.append(-(vectors[t] @ a))
    result = linprog(costs[-1], A_ub=np.array(rows), b_ub=np.array(rhs),
                     bounds=[(-50, 50)] * width, method="highs")
    return None if result.status != 0 else result.x.reshape(count, n)


def best_segment_law(a, r, kappa, depth):
    bound, z0 = certificate_bound(list(a), r, depth, kappa=kappa)
    free = [i for i in range(len(a)) if 1e-9 < z0[i] < 1 - 1e-9]

    def gap(z):
        found = asymmetric_zonotope_minimal_cost(z, a, r, kappa)
        return float(a @ z) - found["value"], found

    def objective(s):
        z = z0.copy()
        z[free] = np.clip(s, 0, 1)
        return -gap(z)[0]

    result = minimize(objective, z0[free], method="Nelder-Mead",
                      options={"maxiter": 150, "xatol": 1e-10, "fatol": 1e-12})
    z = z0.copy()
    z[free] = np.clip(result.x, 0, 1)
    value, found = gap(z)
    return bound, z, value, found["segments"]


def probe(label, a, depth, kappa, r, hops=150, seed=1):
    a = np.asarray(a, dtype=float)
    tau = 1 / (1 + kappa)
    bound, z, segment_value, segments = best_segment_law(a, r, kappa, depth)
    k = F(kappa).limit_denominator(1000)
    exact = []
    for d, alpha, beta in segments:
        al, be = F(float(alpha)).limit_denominator(10**9), F(float(beta)).limit_denominator(10**9)
        exact.append((tuple(F(float(x)).limit_denominator(10**6) for x in d),
                      min(al, k * be), min(be, k * al)))
    states, probabilities, _ = three_point_law(exact, 1 / (1 + k))
    atoms = np.repeat(np.array([[float(v) - 0.5 for v in s] for s in states]), 3, axis=0)
    mass = np.repeat(np.array([float(p) for p in probabilities]), 3) / 3
    vectors = test_vectors(len(a), z)
    atoms /= evaluate(atoms, mass, a, r, tau, vectors)[1]
    start = evaluate(atoms, mass, a, r, tau, vectors)[0]
    best, best_atoms = start, atoms.copy()
    rng = np.random.default_rng(seed)
    for hop in range(hops):
        scale = 0.05 * (1 - hop / hops) + 1e-4
        trial = best_atoms + scale * np.abs(best_atoms).max() * rng.standard_normal(best_atoms.shape)
        for _ in range(4):
            new = cell_lp(trial, mass, a, r, tau, vectors)
            if new is None:
                break
            value, grand, caps, stability = evaluate(new, mass, a, r, tau, vectors)
            if caps > -1e-7 and stability > -1e-7 and value > best + 1e-9:
                best, best_atoms = value, new.copy()
            trial = new
    return {"label": label, "shares": a.tolist(), "depth": depth, "kappa": kappa, "r": r,
            "certificate": float(bound), "membership": [round(float(x), 6) for x in z],
            "best_segment_law": float(segment_value), "segment_law_as_atoms": float(start),
            "atoms": int(len(mass)), "hops": hops, "best_general_law": float(best)}


def main():
    general = json.loads((OUT / "general_shares.json").read_text())
    seed_7591 = next(row for row in general["instances"] if row["seed"] == 7591)
    rows = []
    for label, shares, depth, kappa, r in CASES:
        if shares is None:
            shares = [float(F(x)) for x in seed_7591["shares"]]
            depth, kappa, r = seed_7591["depth"], float(F(seed_7591["kappa"])), float(F(seed_7591["r"]))
        rows.append(probe(label, shares, depth, kappa, r))
        print(rows[-1])
    (OUT / "general_law_probe.json").write_text(json.dumps({"date": "2026-11-07", "cases": rows}, indent=1) + "\n")
    saved = json.loads((OUT / "general_law_probe.json").read_text())["cases"]
    lines = ["# General finite laws where segment laws fall short", "",
             "2026-11-07. Generated by `scripts/probe_general_laws.py` from "
             "[general_law_probe.json](general_law_probe.json). A local search (cell LPs and random "
             "hops), so a failure to improve is evidence, not proof.", "",
             "| case | kappa | r | certificate | best segment law | best general law found | atoms | hops |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for c in saved:
        lines.append(f"| {c['label']} | {c['kappa']} | {c['r']} | {c['certificate']:.6f} | "
                     f"{c['best_segment_law']:.6f} | {c['best_general_law']:.6f} | {c['atoms']} | {c['hops']} |")
    (OUT / "general_law_probe.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
