"""Exploratory seminorm-envelope map for the depth-one exclusion gap.

Compares the symmetric-loss seminorm relaxation (an upper bound on what demand
laws can realize) with the proved bounds C31, C39, the separable bound and the
three-player face bounds of docs/seminorm_envelope.md. Realizability by demand
laws is not checked. Strict gaps below a proved bound come from a grid search
with local refinement and are numerical observations, not certificates.
"""

import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from censored_newsvendor.seminorm_envelope import (
    PROPORTIONAL_ZERO_THRESHOLD, c31_ceiling, c39_envelope, configuration_prediction,
    depth_one_envelope, proportional_three_player_bound,
    proportional_three_player_closed_form, separable_bound, three_player_bound,
)

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-6
EQUAL3 = [1 / 3] * 3


def equal(n):
    return [1 / n] * n


def cases():
    out = []
    for r in (0, 1 / 20, 1 / 10, 1 / 5, 1 / 3, 2 / 5, 1 / 2, 4 / 5, 9 / 10, 1):
        out.append({"section": "c39", "shares": EQUAL3, "r": r, "step": 0.01})
    for shares in ([.5, .3, .2], [.6, .25, .15], [.45, .45, .1], [.7, .2, .1]):
        for r in (.1, .2, .3, .4, .5, .7):
            out.append({"section": "unequal", "shares": shares, "r": r, "step": 0.01})
    for r in (.1, .15, .2, .22, .25, .3, 1 / 3, .4, .5, .6, .8):
        out.append({"section": "general_n", "shares": equal(4), "r": r, "step": 0.025})
    for r in (.25, .35, .4, .5, .7):
        out.append({"section": "general_n", "shares": equal(5), "r": r, "step": 0.05})
    for r in (.1, .15, .16, .17, .18, .19, .2, .25, .3, .4, .5, .7, .9):
        out.append({"section": "proportional", "shares": EQUAL3, "r": r, "step": 0.01,
                    "pinned": True})
    for b in (0, .01, .03, .06):
        for r in (.25, .3):
            out.append({"section": "integer_excess", "shares": equal(4), "r": r,
                        "step": 0.025, "integer_excess": b})
    for b in (0, .02, .05):
        out.append({"section": "integer_excess", "shares": [.6, .25, .15], "r": .2,
                    "step": 0.01, "integer_excess": b})
        out.append({"section": "integer_excess", "shares": EQUAL3, "r": .2,
                    "step": 0.01, "integer_excess": b, "pinned": True})
    return out


def run(case):
    kwargs = {}
    if case.get("integer_excess"):
        kwargs["integer_excess"] = case["integer_excess"]
    if case.get("pinned"):
        kwargs["pinned_singletons"] = True
    found = depth_one_envelope(case["shares"], case["r"], step=case["step"], **kwargs)
    row = dict(case)
    row.update(found)
    return row


def annotate(row):
    shares, r, n = row["shares"], row["r"], len(row["shares"])
    value = row["value"]
    bounds = {"c31": c31_ceiling(shares, r)}
    equal_shares = max(shares) - min(shares) < 1e-12
    if equal_shares:
        bounds["separable"] = separable_bound(n, r)
    if n == 3:
        bounds["three_inequality"] = three_player_bound(shares, r, fourth=False)
        bounds["four_inequality"] = three_player_bound(shares, r)
    if row.get("pinned"):
        bounds = {"proportional": proportional_three_player_bound(r)}
        assert abs(bounds["proportional"]
                   - proportional_three_player_closed_form(r)) < 1e-12, r
    if row["section"] == "c39":
        bounds["c39"] = c39_envelope(r)
    proved = min(bounds.values())
    assert value is not None and value <= proved + TOL, (row, bounds)
    row["bounds"] = bounds
    row["attains_proved_bound"] = bool(abs(value - proved) < TOL)
    if row["section"] == "c39":
        assert row["attains_proved_bound"], row
    if row["section"] == "general_n":
        row["heuristic_label"] = configuration_prediction(n, r)
        row["heuristic_consistent"] = (row["heuristic_label"] != "below") == row["attains_proved_bound"]
    return row


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmt(x):
    return "n/a" if x is None else f"{x:.6f}"


def summary(payload):
    rows = payload["cases"]
    by = {}
    for row in rows:
        by.setdefault(row["section"], []).append(row)
    lines = ["# Seminorm-envelope map (exploratory)", "",
             "2026-11-06, branch `pulp-fiction`. Method, proofs of the bounds and scope: "
             "[docs/seminorm_envelope.md](../../docs/seminorm_envelope.md).", "",
             "Every value is the relaxed depth-one gap (D1-B)/L over all symmetric-loss "
             "seminorms satisfying the game constraints, maximized by grid search plus local "
             "refinement. It is an upper bound on what demand laws can realize; realizability "
             "is not checked. Equality with a proved bound certifies the relaxation's value. "
             "A value strictly below every proved bound is a numerical observation.", "",
             "## Three equal shares: agreement with C39", "",
             "| r | relaxation | C39 |", "| ---: | ---: | ---: |"]
    for row in by["c39"]:
        lines.append(f"| {row['r']:.4f} | {fmt(row['value'])} | {fmt(row['bounds']['c39'])} |")
    lines += ["", "## Three players, unequal shares", "",
              "The three-inequality bound is the C39 proof applied to arbitrary shares; the "
              "four-inequality bound adds the standalone cap of the integral coordinate "
              "(Proposition 3).", "",
              "| shares | r | relaxation | three-ineq. | four-ineq. | C31 | four-ineq. attained |",
              "| --- | ---: | ---: | ---: | ---: | ---: | :---: |"]
    for row in by["unequal"]:
        b = row["bounds"]
        lines.append(f"| {tuple(row['shares'])} | {row['r']:.2f} | {fmt(row['value'])} | "
                     f"{fmt(b['three_inequality'])} | {fmt(b['four_inequality'])} | "
                     f"{fmt(b['c31'])} | {'yes' if row['attains_proved_bound'] else 'no'} |")
    lines += ["", "## Equal shares, n = 4 and 5", "",
              "| n | r | relaxation | separable bound | C31 | attained | heuristic label |",
              "| ---: | ---: | ---: | ---: | ---: | :---: | --- |"]
    for row in by["general_n"]:
        b = row["bounds"]
        lines.append(f"| {len(row['shares'])} | {row['r']:.4f} | {fmt(row['value'])} | "
                     f"{fmt(b['separable'])} | {fmt(b['c31'])} | "
                     f"{'yes' if row['attains_proved_bound'] else 'no'} | {row['heuristic_label']} |")
    consistent = sum(row["heuristic_consistent"] for row in by["general_n"])
    lines += ["", f"The configuration heuristic agrees with the attained/not-attained pattern "
              f"in {consistent} of {len(by['general_n'])} cases.", "",
              "## Proportional allocation, three equal shares and equal standalone costs", "",
              f"The proved bound is zero for r <= {PROPORTIONAL_ZERO_THRESHOLD:.6f}.", "",
              "| r | relaxation | proportional bound | C39 (rho >= r) |",
              "| ---: | ---: | ---: | ---: |"]
    for row in by["proportional"]:
        lines.append(f"| {row['r']:.2f} | {fmt(row['value'])} | "
                     f"{fmt(row['bounds']['proportional'])} | {fmt(c39_envelope(row['r']))} |")
    lines += ["", "## Positive integer excess", "",
              "| shares | variant | r | B | relaxation |", "| --- | --- | ---: | ---: | ---: |"]
    for row in by["integer_excess"]:
        variant = "proportional" if row.get("pinned") else "rho >= r"
        lines.append(f"| {tuple(round(x, 4) for x in row['shares'])} | {variant} | {row['r']:.2f} | "
                     f"{row.get('integer_excess', 0):.2f} | {fmt(row['value'])} |")
    lines += ["", f"All {len(rows)} relaxed values respect every applicable proved bound "
              f"(tolerance {TOL:g}); all C39 cases attain C39.", "",
              "Reproduce: `python scripts/check_seminorm_envelope.py`. The "
              "[JSON](seminorm_envelope.json) records every case, the maximizing membership "
              "and source hashes.", ""]
    return "\n".join(lines)


def main():
    with ProcessPoolExecutor() as pool:
        rows = [annotate(row) for row in pool.map(run, cases())]
    sources = [ROOT / "src/censored_newsvendor/seminorm_envelope.py", Path(__file__).resolve()]
    payload = {
        "date": "2026-11-06",
        "scope": "Exploratory symmetric-loss seminorm relaxation; realizability not checked.",
        "tolerance": TOL,
        "sha256": {str(p.relative_to(ROOT)): sha(p) for p in sources},
        "cases": rows,
    }
    output = ROOT / "results/exclusion/seminorm_envelope.json"
    output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    output.with_suffix(".md").write_text(summary(payload))
    print(f"Checked {len(rows)} cases; all relaxed values respect the proved bounds.")


if __name__ == "__main__":
    main()
