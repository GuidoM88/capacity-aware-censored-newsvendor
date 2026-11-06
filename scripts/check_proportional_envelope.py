"""Relaxed depth-one envelope under charges proportional to standalone costs.

Equal shares with equal pinned standalone costs c_j = a_j / r, so rho = r
equals L / sum_j c_j. Compares the seminorm relaxation with the proved C31
ceiling and, for three players, with Proposition 4. Exploratory: the
maximization is a grid search with refinement, and realizability is checked
separately by scripts/check_zonotope_realizability.py.
"""

import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from censored_newsvendor.seminorm_envelope import (
    c31_ceiling, depth_one_envelope, proportional_three_player_bound, separable_bound,
)

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-6
CASES = ([(3, r, .01) for r in (.05, .1, .15, .17, .2, .3, .5, .7)]
         + [(4, r, .025) for r in (.04, .06, .08, .1, .12, .14, .17, .2, .25, .3, .4, .5, .7)]
         + [(5, r, .05) for r in (.03, .05, .07, .09, .12, .15, .2, .3, .5)])


def run(case):
    n, r, step = case
    found = depth_one_envelope([1 / n] * n, r, step=step, pinned_singletons=True)
    c31 = c31_ceiling([1 / n] * n, r)
    row = {"n": n, "r": r, "step": step, "value": found["value"],
           "membership": found["membership"], "c31": c31,
           "separable": separable_bound(n, r)}
    if n == 3:
        row["proposition_4"] = proportional_three_player_bound(r)
    assert row["value"] <= min(c31, row["separable"]) + TOL, row
    if n == 3:
        assert abs(row["value"] - row["proposition_4"]) < TOL, row
    row["equals_c31"] = bool(abs(row["value"] - c31) < TOL)
    return row


def main():
    with ProcessPoolExecutor() as pool:
        rows = list(pool.map(run, CASES))
    sources = [ROOT / "src/censored_newsvendor/seminorm_envelope.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06", "tolerance": TOL,
               "scope": "Seminorm relaxation with pinned equal standalone costs; realizability separate.",
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/proportional_envelope.json"
    output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    lines = ["# Proportional-charge envelope (exploratory)", "",
             "2026-11-06, branch `pulp-fiction`. Equal shares and equal standalone costs pinned at "
             "a_j/r, so rho = r = L / sum_j c_j. Values are the relaxed depth-one gap (D1-B)/L, B=0, "
             "from the seminorm oracle of [docs/seminorm_envelope.md](../../docs/seminorm_envelope.md). "
             "For n=3 they equal the proved Proposition 4 bound.", "",
             "| n | r | relaxation | C31 | equals C31 | best membership |",
             "| ---: | ---: | ---: | ---: | :---: | --- |"]
    for row in rows:
        z = ", ".join(f"{x:.3f}" for x in row["membership"])
        lines.append(f"| {row['n']} | {row['r']:.2f} | {row['value']:.6f} | {row['c31']:.6f} | "
                     f"{'yes' if row['equals_c31'] else 'no'} | ({z}) |")
    small = {n: min((r for r in rows if r["n"] == n), key=lambda r: r["r"]) for n in (3, 4, 5)}
    lines += ["", "Negative result: the three-player shape (zero gap under strong pooling, half of C31 "
              "above r=1/5) does not persist. At the smallest sampled ratio the relaxed gap is "
              + ", ".join(f"{small[n]['value']:.4f} for n={n} (r={small[n]['r']:.2f})" for n in (3, 4, 5))
              + f"; for n=5 it equals C31 in {sum(r['equals_c31'] for r in rows if r['n'] == 5)} "
              f"of {sum(1 for r in rows if r['n'] == 5)} sampled ratios.", "",
              "Reproduce: `python scripts/check_proportional_envelope.py`. The "
              "[JSON](proportional_envelope.json) stores every case and source hashes.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"Checked {len(rows)} proportional cases.")


if __name__ == "__main__":
    main()
