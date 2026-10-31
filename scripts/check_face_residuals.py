"""Out-of-sample comparison on fixed laws, using independent pilot and validation RNGs."""

import hashlib
import json
import platform
from pathlib import Path
from itertools import product

import numpy as np
import scipy

from censored_newsvendor.coalition_audit import (
    FiniteLaw, FrozenRule, enumeration_certificate, exact_excess, finite_certificate, forecast_rule,
)
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.face_residuals import (
    empirical_law, fit_prices, population_diagnostic, residual_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/certificates/results.json"
EXCL = ROOT / "results/exclusion/results.json"
SIZES = (256, 1024, 4096)
DELTA = .05 / 18
METHODS = ("pilot_face", "pilot_grand", "forecast_face_full", "forecast_grand_full",
           "enumeration_validation", "enumeration_full")


def compare(rule, forecast, pilot, validation, delta):
    together = np.concatenate([pilot, validation])
    pilot_law = empirical_law(pilot)
    face = fit_prices(rule, pilot_law)
    grand = fit_prices(rule, pilot_law, grand=True)
    forecast_face = fit_prices(rule, forecast)
    primary = residual_certificate(rule, face, validation, delta)
    matched = residual_certificate(rule, grand, validation, delta, grand=True)
    from_forecast = residual_certificate(rule, forecast_face, together, delta)
    upper = {
        "pilot_face": primary["upper"], "pilot_grand": matched["upper"],
        "forecast_face_full": from_forecast["upper"],
        "forecast_grand_full": finite_certificate(rule, together, delta)["upper"],
        "enumeration_validation": enumeration_certificate(rule, validation, delta)["upper"],
        "enumeration_full": enumeration_certificate(rule, together, delta)["upper"],
    }
    return {"upper": upper, "primary": primary, "forecast_face": from_forecast,
            "grand": matched, "prices": [{"offer": p.offer, "tie": p.tie} for p in face]}, face


def fresh_check(index, name, rule, forecast, truth, b, d1, group):
    draws, streams = [], []
    for stream in [0, 1]:
        entropy = [20261031, index, stream]
        rng = np.random.default_rng(np.random.SeedSequence(entropy))
        ix = rng.choice(len(truth.states), max(SIZES), p=truth.probabilities)
        draws.append(ix)
        streams.append({"entropy": entropy,
                        "counts": {str(m): np.bincount(ix[:m], minlength=len(truth.states)).tolist()
                                   for m in SIZES}})
    results = []
    for m in SIZES:
        pilot, val = [truth.states[ix[:m]] for ix in draws]
        result, prices = compare(rule, forecast, pilot, val, DELTA)
        oracle = population_diagnostic(rule, prices, truth)
        assert oracle["lower"] <= b + 1e-8 and oracle["upper"] + 1e-8 >= d1
        assert oracle["gap_upper"] + 1e-8 >= d1 - b
        result.update({"m": m, "frozen_prices_population": oracle,
                       "covers_B": {k: u + 1e-8 >= b for k, u in result["upper"].items()},
                       "primary_joint_event_check": bool(
                           result["primary"]["lower"] <= b + 1e-8 and
                           result["primary"]["upper"] + 1e-8 >= d1 and
                           result["primary"]["gap_upper"] + 1e-8 >= d1 - b)})
        results.append(result)
    return {"id": name, "group": group, "n": len(rule.weights), "maximum_loss": rule.loss_range,
            "B": b, "D1": d1, "streams": streams, "comparison": results}


def aggregate(rows, j):
    n = len(rows)
    bounds = {method: float(np.mean([(r["comparison"][j]["upper"][method] - r["B"]) /
                                     r["maximum_loss"] for r in rows])) for method in METHODS}
    probes = [r["comparison"][j]["primary"] for r in rows]
    tight_gap = sum(p["gap_upper"] <= .05 * r["maximum_loss"] for r, p in zip(rows, probes))
    tight_width = sum(p["upper"] - p["lower"] <= .05 * r["maximum_loss"] for r, p in zip(rows, probes))
    failures = {method: sum(not r["comparison"][j]["covers_B"][method] for r in rows) for method in METHODS}
    return {"cases": n, "m": SIZES[j], "mean_normalized_upper_slack": bounds,
            "small_certified_structural_gap": tight_gap, "small_total_width": tight_width,
            "coverage_failures": failures,
            "joint_failures": sum(not r["comparison"][j]["primary_joint_event_check"] for r in rows),
            "fallbacks": sum(p["fallback"] for p in probes)}


def summarize(payload):
    groups = {"original": payload["cases"][:100],
              "heterogeneous": [r for r in payload["cases"] if r["group"] == "heterogeneous"],
              "mixtures": payload["cases"][100:]}
    stats = {k: [aggregate(v, j) for j in range(len(SIZES))] for k, v in groups.items()}
    final = stats["heterogeneous"][-1]
    achieved = final["small_certified_structural_gap"] >= final["cases"] / 2
    improved = final["mean_normalized_upper_slack"]["pilot_face"] < final["mean_normalized_upper_slack"]["forecast_grand_full"]
    stats["gate"] = {"certifies_half": achieved, "beats_fixed_moment_mean": improved, "pass": achieved and improved}
    lines = ["# Residual certificate on fresh iid samples", "",
             "Slack is the upper bound minus exact B divided by the maximum grand loss A, averaged equally across instances.",
             "M denotes the validation size. The pilot has another M observations.", "",
             "| Group | M | Fit faces | Fit grand | Forecast faces, 2M | Original moment, 2M | Exhaustive, M | Exhaustive, 2M | Gap ≤ 5% A | Width ≤ 5% A |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for name in groups:
        for s in stats[name]:
            v = s["mean_normalized_upper_slack"]
            lines.append(f"| {name} | {s['m']} | " + " | ".join(f"{v[k]:.5f}" for k in METHODS) +
                         f" | {s['small_certified_structural_gap']}/{s['cases']} | {s['small_total_width']}/{s['cases']} |")
    lines.extend(["", "## Precision decision", "",
                  f"Both prespecified conditions passed: {stats['gate']['pass']}. "
                  f"The face method certified a small structural gap in {final['small_certified_structural_gap']} of {final['cases']} heterogeneous instances at M=4096.",
                  "", "## Four-producer obstruction example", "",
                  "| M | Actual B | Actual D1−B | Certified gap | Lower B | Upper B |", "| ---: | ---: | ---: | ---: | ---: | ---: |"])
    r = groups["original"][3]
    for c in r["comparison"]:
        p = c["primary"]
        lines.append(f"| {c['m']} | {r['B']:.6g} | {r['D1']-r['B']:.6g} | {p['gap_upper']:.6g} | {p['lower']:.6g} | {p['upper']:.6g} |")
    lines += ["", "## Mixture path at M=4096", "", "| Case | B | D1−B | Certified gap/A | Width/A |",
              "| --- | ---: | ---: | ---: | ---: |"]
    for r in groups["mixtures"]:
        p = r["comparison"][-1]["primary"]
        lines.append(f"| {r['id']} | {r['B']:.6g} | {r['D1']-r['B']:.6g} | {p['gap_upper']/r['maximum_loss']:.5f} | {(p['upper']-p['lower'])/r['maximum_loss']:.5f} |")
    return stats, "\n".join(lines) + "\n"


def main():
    original = json.loads(BASE.read_text())["cases"]
    excl = {r["id"]: r["population"]["levels"][1]["upper"]
            for r in json.loads(EXCL.read_text())["original_cases"]}
    out = []
    for i, r in enumerate(original):
        truth = FiniteLaw(**r["truth"])
        forecast = FiniteLaw(**r["forecast"])
        rule = FrozenRule(r["rule"]["offer"], r["rule"]["weights"], r["rule"]["rated"],
                          r["over"], r["under"], r["rule"]["tie_score"])
        group = "heterogeneous" if ("_same_total_" in r["id"] or "_shifted_" in r["id"]) else "original"
        out.append(fresh_check(i, r["id"], rule, forecast, truth, r["exact"]["excess"], excl[r["id"]], group))
    y = np.array(list(product([0., 1.], repeat=6)))
    symmetric = np.prod(np.where(y == 1, .35, .65), axis=1)
    perturbation = (y == [1, 1, 0, 0, 0, 0]).all(axis=1)
    forecast = FiniteLaw([[0.] * 6, [1.] * 6], [.5, .5])
    rule = forecast_rule(forecast, np.ones(6))
    for lam in (0., .25, .5, 1.):
        truth = FiniteLaw(y, (1 - lam) * symmetric + lam * perturbation)
        b = exact_excess(rule, truth)["excess"]
        d1 = ExclusionEnvelope.population(rule, truth).level(1)["upper"]
        out.append(fresh_check(len(out), f"mixture_{lam:g}", rule, forecast, truth, b, d1, "mixture"))
    files = ["scripts/check_face_residuals.py", "src/censored_newsvendor/face_residuals.py",
             "docs/residual_protocol.md", "src/censored_newsvendor/coalition_audit.py",
             "src/censored_newsvendor/exclusion.py", "results/certificates/results.json", "results/exclusion/results.json"]
    payload = {"date": "2026-10-31", "versions": {"python": platform.python_version(),
               "numpy": np.__version__, "scipy": scipy.__version__},
               "delta_per_method_size": DELTA, "cases": out,
               "sha256": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files}}
    directory = ROOT / "results/residuals"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "results.json"
    path.write_text(json.dumps(payload, separators=(",", ":"), allow_nan=False) + "\n")
    stats, md = summarize(json.loads(path.read_text()))
    (directory / "summary.md").write_text(md)
    (directory / "summary.json").write_text(json.dumps(stats, indent=2, allow_nan=False) + "\n")
    print(md)


if __name__ == "__main__":
    main()

