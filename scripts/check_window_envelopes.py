"""Equal-share windows: explicit laws against the certificate upper bound.

For every window of n = 4..12 producers at depths 1 to 3 (when the face has
at least three free producers) and nine ratios per window, endpoints
included, this script
1. builds the best explicit law among the families C31, H_p and V_p and
   checks every constraint in exact arithmetic;
2. computes the certificate LP bound, valid for every demand law;
3. records whether the two coincide, i.e. whether the worst gap is pinned
   down at that ratio, and which family attains it.
It also checks the closed form of the four-producer window.
"""

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from censored_newsvendor.exact_envelopes import (
    best_equal_share_construction, verify_generators, windows,
)
from censored_newsvendor.seminorm_envelope import c31_ceiling, equal_share_certificate_bound

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-9


def main():
    rows = []
    for n in range(4, 13):
        for depth in (1, 2, 3):
            if n - depth < 3:
                continue
            for lo, hi in windows(n, depth):
                for k in range(9):
                    r = lo + (hi - lo) * F(k, 8)
                    construction = best_equal_share_construction(n, r, depth)
                    check = verify_generators(construction["generators"], [F(1, n)] * n, r,
                                              construction["membership"], construction["value"])
                    assert (check["cap"] >= 0 and check["stability"] >= 0 and check["grand"] >= 0
                            and check["witness"] == 0 and check["rho"] == r), (n, depth, r, check)
                    bound, _ = equal_share_certificate_bound(n, float(r), depth)
                    value = float(construction["value"])
                    assert value <= bound + TOL, (n, depth, r, value, bound)
                    rows.append({"n": n, "depth": depth, "window": [str(lo), str(hi)], "r": str(r),
                                 "family": construction["regime"], "value": str(construction["value"]),
                                 "certificate_bound": bound, "c31": c31_ceiling([1 / n] * n, float(r)) * (n - depth) / (n - 1),
                                 "pinned": bool(abs(bound - value) < TOL)})
    for k in range(9):
        r = F(1, 5) + (F(1, 3) - F(1, 5)) * F(k, 8)
        closed = (2 - r + 3 * r * r) / (2 * (1 + 3 * r))
        assert best_equal_share_construction(4, r)["value"] == closed, r
    sources = [ROOT / "src/censored_newsvendor/exact_envelopes.py",
               ROOT / "src/censored_newsvendor/seminorm_envelope.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06", "tolerance": TOL,
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/window_envelopes.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    pinned = sum(row["pinned"] for row in rows)
    families = sorted({row["family"] for row in rows})
    lines = ["# Equal-share windows: explicit laws and certificate bound", "",
             "2026-11-06. Families and proofs: [docs/exact_envelopes.md](../../docs/exact_envelopes.md), "
             "Section 5.", "",
             f"{len(rows)} ratios (n = 4..12, depths 1-3, nine per window including endpoints). Every "
             "explicit law passes the exact check of all constraints. In "
             f"{pinned} of {len(rows)} cases its value equals the certificate LP bound to {TOL:g}, so "
             "the worst gap at that ratio is determined; the attaining families are "
             + ", ".join(families) + ". The four-producer closed form "
             "(2 - r + 3r^2)/(2(1+3r)) is confirmed at nine ratios of [1/5, 1/3].", "",
             "| n | depth | window | r | family | worst gap | certificate bound | C31 ceiling |",
             "| ---: | ---: | --- | ---: | --- | ---: | ---: | ---: |"]
    for row in rows:
        if F(row["r"]) in (F(row["window"][0]), F(row["window"][1])):
            continue
        k = (F(row["r"]) - F(row["window"][0])) / (F(row["window"][1]) - F(row["window"][0]))
        if k not in (F(1, 4), F(1, 2), F(3, 4)):
            continue
        lines.append(f"| {row['n']} | {row['depth']} | ({row['window'][0]}, {row['window'][1]}) | "
                     f"{float(F(row['r'])):.4f} | {row['family']} | {float(F(row['value'])):.6f} | "
                     f"{row['certificate_bound']:.6f} | {row['c31']:.6f} |")
    lines += ["", "The table shows the quarter points of each window; the JSON has all nine ratios.", "",
              "Reproduce: `python scripts/check_window_envelopes.py`.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"{len(rows)} window ratios: all laws exact; {pinned} pinned by the certificate bound.")


if __name__ == "__main__":
    main()
