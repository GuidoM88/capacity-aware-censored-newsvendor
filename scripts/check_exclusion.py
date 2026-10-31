"""Evaluate the exclusion hierarchy on the fixed diagnostic and analytical cases."""

import hashlib
import json
import platform
from itertools import product
from pathlib import Path

import numpy as np
import scipy

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, exact_excess, forecast_rule
from censored_newsvendor.exclusion import ExclusionEnvelope


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results/certificates/results.json"
TOL = 1e-8


def evaluate(envelope, reference, milp_check):
    levels = [envelope.level(k) for k in (0, 1, 2)]
    bounds = [level["upper"] for level in levels]
    assert bounds[0] + TOL >= bounds[1] and bounds[1] + TOL >= bounds[2]
    assert bounds[2] + TOL >= reference
    assert all(level["integer_witness"] <= reference + TOL for level in levels)
    binary = envelope.binary_reference() if milp_check else None
    if binary is not None:
        assert abs(binary - reference) < TOL, (binary, reference)
    return {"reference": reference, "levels": levels, "milp": binary}


def replay(row, milp_check):
    rule = FrozenRule(row["rule"]["offer"], row["rule"]["weights"], row["rule"]["rated"],
                      row["over"], row["under"], row["rule"]["tie_score"])
    truth = FiniteLaw(row["truth"]["states"], row["truth"]["probabilities"])
    population = evaluate(ExclusionEnvelope.population(rule, truth), row["exact"]["excess"], milp_check)
    assert abs(population["levels"][0]["upper"] - row["fractional_primal"]["bound"]) < TOL
    finite = []
    for sample in row["validation"]:
        observed = np.repeat(truth.states, sample["counts"], axis=0)
        envelope = ExclusionEnvelope.validation(rule, observed, sample["enumeration"]["delta"])
        comparison = evaluate(envelope, sample["enumeration"]["upper"], milp_check)
        comparison["sample_size"] = sample["size"]
        comparison["moment_reference"] = sample["moment"]["upper"]
        comparison["covers_population"] = [
            level["upper"] + TOL >= row["exact"]["excess"] for level in comparison["levels"]]
        finite.append(comparison)
    return {"id": row["id"], "population": population, "validation": finite}


def symmetric_cases():
    rows = []
    for n in range(3, 9):
        y = np.array(list(product([0., 1.], repeat=n)))
        independent = np.prod(np.where(y == 1, .37, .63), axis=1)
        comonotone = np.zeros(len(y))
        comonotone[0], comonotone[-1] = .63, .37
        forecast = FiniteLaw([[0.] * n, [1.] * n], [.5, .5])
        rule = forecast_rule(forecast, np.ones(n))
        for label, mass in [("independent", independent),
                            ("mixture", (independent + comonotone) / 2)]:
            law = FiniteLaw(y, mass)
            envelope = ExclusionEnvelope.population(rule, law)
            exact = exact_excess(rule, law)["excess"]
            formula = max(0., envelope.integer_value(np.r_[0., np.ones(n - 1)]))
            output = evaluate(envelope, exact, False)
            assert abs(formula - exact) < TOL
            assert abs(output["levels"][1]["upper"] - formula) < TOL
            rows.append({"n": n, "family": label, "leave_one_out_formula": formula, **output})
    return rows


def asymmetric_case():
    w = np.array([3 / 5, 1 / 5, 1 / 5])
    rule = forecast_rule(FiniteLaw(np.stack([.75 * w, 1.25 * w]), [.75, .25]), np.ones(3))
    truth = FiniteLaw([[1., 0., 0.], [0., .6, .4]], [.5, .5])
    result = evaluate(ExclusionEnvelope.population(rule, truth), exact_excess(rule, truth)["excess"], True)
    assert abs(result["reference"]) < TOL
    assert abs(result["levels"][1]["upper"] - 7 / 50) < TOL
    assert abs(result["levels"][2]["upper"]) < TOL
    return result


def summarize(payload):
    original = payload["original_cases"]
    population = [row["population"] for row in original]
    finite = [sample for row in original for sample in row["validation"]]
    lines = ["# Exclusion diagnostic", "", "Computed from saved outcomes, with tolerance 1e-8.", "",
             "| Original comparisons | Level | Strict gaps | Largest gap | Mean gap | LP calls |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    metrics = {}
    for name, rows in [("Population vs actual excess", population),
                       ("Validation vs exhaustive confidence bound", finite)]:
        metrics[name] = []
        for k in (0, 1, 2):
            gaps = np.array([r["levels"][k]["upper"] - r["reference"] for r in rows])
            calls = sum(r["levels"][k]["lp_calls"] for r in rows)
            stats = {"comparisons": len(rows), "strict_gaps": int((gaps > TOL).sum()),
                     "largest_gap": float(gaps.max()), "mean_gap": float(gaps.mean()),
                     "lp_calls": calls,
                     "witness_closes": sum(r["levels"][k]["work_gap"] < TOL for r in rows)}
            metrics[name].append(stats)
            lines.append(f"| {name} | {k} | {stats['strict_gaps']}/{len(rows)} | "
                         f"{stats['largest_gap']:.8g} | {stats['mean_gap']:.8g} | {calls} |")
    lines += ["", "## Validation slack above actual population excess", "",
              "| Sample size | Level 0 | Level 1 | Level 2 | Exhaustive |",
              "| ---: | ---: | ---: | ---: | ---: |"]
    for j, size in enumerate([256, 1024, 4096]):
        gaps = []
        for key in (0, 1, 2, "exact"):
            vals = []
            for r in original:
                v = r["validation"][j]
                upper = v["reference"] if key == "exact" else v["levels"][key]["upper"]
                vals.append(upper - r["population"]["reference"])
            gaps.append(float(np.mean(vals)))
        lines.append(f"| {size} | " + " | ".join(f"{v:.6g}" for v in gaps) + " |")
    metrics["symmetric_formula_checks"] = len(payload["symmetric_cases"])
    metrics["population_milp_checks"] = sum(r["milp"] is not None for r in population) + 1
    metrics["validation_milp_checks"] = sum(r["milp"] is not None for r in finite)
    metrics["observed_coverage_failures"] = [sum(not r["covers_population"][k] for r in finite) for k in (0, 1, 2)]
    lines += ["", "## Analytical examples", "",
              "| Case | Actual | Root | One exclusion | Two exclusions |",
              "| --- | ---: | ---: | ---: | ---: |"]
    illustrative = [("Four producers", original[3]["population"]),
                    ("Three asymmetric producers", payload["asymmetric_case"])]
    for name, r in illustrative:
        values = [r["reference"]] + [entry["upper"] for entry in r["levels"]]
        lines.append(f"| {name} | " + " | ".join(f"{v:.8g}" for v in values) + " |")
    lines += ["", "The validation reference is the exhaustive upper confidence bound on the same observations.",
              "Residual statistical uncertainty is reported in the second table. Each level uses the same DKW event.",
              "A solver call has a different cost from one coalition evaluation. The counts alone do not measure speed.", ""]
    return metrics, "\n".join(lines)


def main():
    data = json.loads(INPUT.read_text())
    original = [replay(row, i < 4) for i, row in enumerate(data["cases"])]
    sources = ["src/censored_newsvendor/exclusion.py", "src/censored_newsvendor/coalition_audit.py",
               "scripts/check_exclusion.py", "docs/exclusion_protocol.md"]
    payload = {"date": "2026-10-31", "input": "results/certificates/results.json",
               "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
               "source_sha256": {s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in sources},
               "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
               "original_cases": original, "symmetric_cases": symmetric_cases(),
               "asymmetric_case": asymmetric_case()}
    directory = ROOT / "results/exclusion"
    directory.mkdir(parents=True, exist_ok=True)
    result_path = directory / "results.json"
    result_path.write_text(json.dumps(payload, separators=(",", ":"), allow_nan=False) + "\n")
    metrics, markdown = summarize(json.loads(result_path.read_text()))
    (directory / "summary.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (directory / "summary.md").write_text(markdown)
    print(markdown)


if __name__ == "__main__":
    main()
