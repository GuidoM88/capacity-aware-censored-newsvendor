"""Explicit families against the certificate bound for random arbitrary shares.

For each random instance the best explicit law over the known families
(C31 configuration, positive cost, transitional and cap-binding)
is checked in exact arithmetic, and its value is compared with the certificate
LP bound, which holds for every demand law. Equality means the worst gap is
determined and given by the closed-form families.
"""

import hashlib
import json
import random
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from pathlib import Path

from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.exact_envelopes import best_general_construction, verify_generators

ROOT = Path(__file__).resolve().parents[1]


def one(seed):
    rng = random.Random(seed)
    n = rng.choice([3, 4, 4, 5, 5, 6])
    raw = [rng.randint(1, 25) for _ in range(n)]
    shares = [F(x, sum(raw)) for x in raw]
    r = F(rng.randint(1, 49), 50)
    depth = rng.randint(1, n - 2)
    best = best_general_construction(shares, r, depth)
    check = verify_generators(best["generators"], shares, r, best["membership"], best["value"])
    valid = (check["cap"] >= 0 and check["stability"] >= 0 and check["grand"] >= 0
             and check["witness"] == 0 and check["rho"] >= r
             and all(0 <= x <= 1 for x in best["membership"]))
    bound, _ = certificate_bound([float(x) for x in shares], float(r), depth)
    return {"seed": seed, "n": n, "depth": depth, "r": str(r), "shares": [str(x) for x in shares],
            "family": best["regime"], "value": str(best["value"]), "certificate_bound": bound,
            "law_valid": valid, "pinned": abs(float(best["value"]) - bound) < 1e-6}


def main():
    with ProcessPoolExecutor() as pool:
        rows = list(pool.map(one, range(5000, 6000)))
    sources = [ROOT / "src/censored_newsvendor/exact_envelopes.py",
               ROOT / "src/censored_newsvendor/certificates.py", Path(__file__).resolve()]
    payload = {"date": "2026-11-06",
               "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sources},
               "cases": rows}
    output = ROOT / "results/exclusion/general_formula.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    valid = sum(row["law_valid"] for row in rows)
    pinned = sum(row["pinned"] for row in rows)
    families = {}
    for row in rows:
        families[row["family"]] = families.get(row["family"], 0) + 1
    lines = ["# Closed-form families for arbitrary shares", "",
             "2026-11-06. Families: [docs/exact_envelopes.md](../../docs/exact_envelopes.md), Section 6.", "",
             f"* {len(rows)} random instances (n = 3..6, random depth and r = k/50, shares k/sum).",
             f"* The best explicit law is valid in exact arithmetic in {valid} of {len(rows)}.",
             f"* Its value equals the certificate bound, valid for every demand law, in {pinned} of "
             f"{len(rows)}; then the worst gap is given by the closed-form families.",
             "* Attaining family: " + ", ".join(f"{k} {v}" for k, v in sorted(families.items())) + ".", "",
             "Reproduce: `python scripts/check_general_formula.py`.", ""]
    output.with_suffix(".md").write_text("\n".join(lines))
    print(f"{valid}/{len(rows)} laws valid; {pinned}/{len(rows)} pinned by the certificate bound; {families}")


if __name__ == "__main__":
    main()
