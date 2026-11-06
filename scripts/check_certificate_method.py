"""The two-LP method on random instances with arbitrary shares.

For each instance: the certificate LP gives an upper bound valid for every
demand law (censored_newsvendor.certificates). The exact seminorm relaxation
(Lemma 1) evaluated at the LP's maximizer gives a lower bound on the relaxed
envelope; if the two agree, the relaxed worst gap is determined. For the
four-producer instances and a few five-producer ones, the zonotope LP then
builds an explicit finite symmetric law at that membership, re-evaluated with
the original audit code; if it reaches the bound, the worst gap over demand
laws is determined too.
"""

import hashlib
import json
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.seminorm_envelope import minimal_cost, symmetric_unit_law, zonotope_minimal_cost

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-6


def instances():
    rng = random.Random(1107)
    out = []
    plan = [(4, 1, 24), (4, 2, 12), (5, 1, 10), (5, 2, 10), (5, 3, 6), (6, 1, 6)]
    for n, depth, count in plan:
        for k in range(count):
            raw = [rng.randint(1, 12) for _ in range(n)]
            shares = [x / sum(raw) for x in raw]
            r = rng.choice([.05, .1, .2, .3, .4, .5, .6, .7, .8, .9])
            realize = n == 4 or (n == 5 and depth == 1 and k < 2)
            out.append({"n": n, "depth": depth, "shares": shares, "r": r, "realize": realize})
    return out


def run(case):
    shares, r, depth = np.array(case["shares"]), case["r"], case["depth"]
    bound, z = certificate_bound(shares, r, depth)
    row = dict(case)
    row.update({"certificate_bound": bound, "membership": z.tolist()})
    if bound <= 1e-12:
        row.update({"relaxation_at_point": 0.0, "relaxation_pinned": True})
        return row
    relaxed = float(shares @ z) - minimal_cost(z, shares, r)[0]
    row.update({"relaxation_at_point": relaxed,
                "relaxation_pinned": bool(abs(relaxed - bound) < TOL)})
    if case["realize"]:
        zono = zonotope_minimal_cost(z, shares, r, samples=2_000_000 if case["n"] == 4 else 4_000_000)
        states, probabilities, offer, _ = symmetric_unit_law(zono["generators"], shares)
        rule = FrozenRule(offer, shares, np.ones(len(shares)))
        law = FiniteLaw(states, probabilities)
        grand = float(probabilities @ np.abs(offer - states.sum(axis=1)))
        upper = ExclusionEnvelope.population(rule, law).level(depth)["upper"]
        table = coalition_table(rule, law)
        integer = max(0., max(item["excess"] for item in table))
        singles = [item["cost"] for item in table if len(item["coalition"]) == 1]
        rho = min([1.] + [grand * w / c for w, c in zip(shares, singles) if c > 1e-15])
        gap = (upper - integer) / grand
        row.update({"law_gap": gap, "law_atoms": len(probabilities),
                    "law_pinned": bool(abs(gap - bound) < TOL and integer / grand < TOL and rho >= r - TOL)})
    return row


def main():
    with ProcessPoolExecutor() as pool:
        rows = list(pool.map(run, instances()))
    sources = [ROOT / "src/censored_newsvendor/certificates.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06", "tolerance": TOL,
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/certificate_method.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    pinned = sum(row["relaxation_pinned"] for row in rows)
    realized = [row for row in rows if "law_pinned" in row]
    lines = ["# Two-LP method with arbitrary shares", "",
             "2026-11-06. Method: [docs/exact_envelopes.md](../../docs/exact_envelopes.md), Section 6. "
             "Certificate bound: valid for every demand law. Relaxation at point: exact seminorm "
             "relaxation (Lemma 1) at the bound's maximizer. Law: explicit finite symmetric law from the "
             "zonotope LP, re-evaluated with the original audit code.", "",
             f"* The certificate bound equals the relaxation at its maximizer in {pinned} of {len(rows)} "
             "random instances (n = 4, 5, 6; depths 1 to 3; tolerance 1e-6).",
             f"* An explicit law reaches the bound in {sum(r['law_pinned'] for r in realized)} of "
             f"{len(realized)} instances where a law was built.", "",
             "| n | depth | shares | r | certificate bound | relaxation at point | law |",
             "| ---: | ---: | --- | ---: | ---: | ---: | ---: |"]
    for row in rows:
        shares = "(" + ", ".join(f"{x:.3f}" for x in row["shares"]) + ")"
        law = f"{row['law_gap']:.6f}" if "law_gap" in row else ""
        lines.append(f"| {row['n']} | {row['depth']} | {shares} | {row['r']:.2f} | "
                     f"{row['certificate_bound']:.6f} | {row['relaxation_at_point']:.6f} | {law} |")
    lines += ["", "Reproduce: `python scripts/check_certificate_method.py`.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"relaxation pinned in {pinned}/{len(rows)}; law reaches bound in "
          f"{sum(r['law_pinned'] for r in realized)}/{len(realized)}")


if __name__ == "__main__":
    main()
