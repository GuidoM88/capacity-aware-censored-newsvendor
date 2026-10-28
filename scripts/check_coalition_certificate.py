"""Run the prespecified structural diagnostic; all generated cases are retained."""

import hashlib
import json
import platform
from itertools import product
from pathlib import Path

import numpy as np
import scipy

from censored_newsvendor.coalition_audit import (
    FiniteLaw, best_common_dual, coalition_program, enumeration_certificate,
    exact_excess, finite_certificate, forecast_rule, population_bound,
)


ROOT = Path(__file__).resolve().parents[1]
SIZES = [256, 1024, 4096]
SEEDS = [104729, 130363]
FAMILIES = ["matched", "same_total", "independent_vs_comonotone", "shifted"]
PENALTIES = [(1., 1.), (1., 3.), (3., 1.)]
DELTA = .05 / (2 * len(SIZES))


def analytical_cases():
    one = FiniteLaw([[1, 0, 0], [0, 1, 1]], [.5, .5])
    two = FiniteLaw([[0, 1, 0], [1, 0, 1]], [.5, .5])
    states = np.array(list(product([0., 1.], repeat=4)))
    p = np.full(16, 1 / 16)
    q = p.copy()
    for k in range(4):
        unit = np.eye(4)[k]
        selected = np.all(states == unit, axis=1) | np.all(states == 1 - unit, axis=1)
        q[selected] += (-3 if k < 2 else 3) / 160
    uniform = FiniteLaw(states, p)
    return [
        ("three_matched", one, one, (1., 1.)),
        ("three_dependence", one, two, (1., 1.)),
        ("four_fixed_score_gap", FiniteLaw(states, q), uniform, (1., 1.)),
        ("four_fractional_gap", FiniteLaw([[1 / 3] * 4, [.5] * 4], [.75, .25]),
         uniform, (1., 1.)),
    ]


def random_case(n, family, seed):
    states = np.array(list(product([0., 1.], repeat=n)))
    totals = states.sum(axis=1).astype(int)
    rng = np.random.default_rng(np.random.SeedSequence([seed, n, FAMILIES.index(family)]))
    q = rng.dirichlet(np.ones(len(states)))
    if family == "matched":
        p = q.copy()
    elif family == "same_total":
        p = np.zeros_like(q)
        for total in range(n + 1):
            mask = totals == total
            p[mask] = q[mask].sum() * rng.dirichlet(np.full(mask.sum(), .5))
    elif family == "independent_vs_comonotone":
        chance = .35 if seed == SEEDS[0] else .65
        q = np.prod(np.where(states == 1, chance, 1 - chance), axis=1)
        p = np.zeros_like(q)
        p[0], p[-1] = 1 - chance, chance
    else:
        p = .7 * q
        p[-1] += .3
    return FiniteLaw(states, q), FiniteLaw(states, p)


def evaluate(case_id, forecast, truth, penalties, check_integer, sample_seed):
    n = truth.states.shape[1]
    rule = forecast_rule(forecast, np.ones(n), *penalties)
    exact = exact_excess(rule, truth)
    fixed = population_bound(rule, truth)
    best = best_common_dual(rule, truth)
    fractional = coalition_program(rule, truth)
    integer = coalition_program(rule, truth, integral=True) if check_integer else None
    tolerance = 1e-8
    assert exact["excess"] <= fractional["bound"] + tolerance, case_id
    assert fractional["bound"] <= fixed["bound"] + tolerance, case_id
    assert abs(best["bound"] - fractional["bound"]) <= tolerance, case_id
    if integer:
        assert abs(integer["bound"] - exact["excess"]) <= tolerance, case_id

    rng = np.random.default_rng(sample_seed)
    sampled_indices = rng.choice(len(truth.states), size=max(SIZES), p=truth.probabilities)
    validations = []
    for size in SIZES:
        indices = sampled_indices[:size]
        sample = truth.states[indices]
        fast = finite_certificate(rule, sample, DELTA)
        enumerated = enumeration_certificate(rule, sample, DELTA)
        validations.append({"size": size, "counts": np.bincount(indices, minlength=len(truth.states)).tolist(),
                            "moment": fast, "enumeration": enumerated,
                            "moment_covered": fast["upper"] + tolerance >= exact["excess"],
                            "enumeration_covered": enumerated["upper"] + tolerance >= exact["excess"]})
    return {"id": case_id, "n": n, "over": penalties[0], "under": penalties[1],
            "forecast": {"states": forecast.states.tolist(), "probabilities": forecast.probabilities.tolist()},
            "truth": {"states": truth.states.tolist(), "probabilities": truth.probabilities.tolist()},
            "rule": {"offer": rule.offer, "weights": rule.weights.tolist(),
                     "rated": rule.rated.tolist(), "tie_score": rule.tie_score},
            "exact": exact, "fixed_population": fixed, "best_common_dual": best,
            "fractional_primal": fractional, "integer_primal": integer,
            "sample_seed": sample_seed, "validation": validations}


def summary(payload):
    rows = payload["cases"]
    tol = 1e-8
    def max_gap(a, b):
        return max(row[a]["bound"] - row[b]["excess"] for row in rows)
    metrics = {
        "instances": len(rows),
        "population_coalitions_evaluated": sum(row["exact"]["coalitions_checked"] for row in rows),
        "independent_lp_equalities": len(rows),
        "independent_milp_checks": sum(row["integer_primal"] is not None for row in rows),
        "stable_instances": sum(row["exact"]["excess"] <= tol for row in rows),
        "strict_fixed_score_gaps": sum(row["fixed_population"]["bound"] > row["exact"]["excess"] + tol for row in rows),
        "strict_fractional_gaps": sum(row["fractional_primal"]["bound"] > row["exact"]["excess"] + tol for row in rows),
        "maximum_fixed_score_gap": max_gap("fixed_population", "exact"),
        "maximum_fractional_gap": max_gap("fractional_primal", "exact"),
        "maximum_lp_disagreement": max(abs(row["best_common_dual"]["bound"] - row["fractional_primal"]["bound"]) for row in rows),
        "finite_certificate_evaluations": 2 * len(SIZES) * len(rows),
        "moment_coverage_failures": sum(not v["moment_covered"] for row in rows for v in row["validation"]),
        "enumeration_coverage_failures": sum(not v["enumeration_covered"] for row in rows for v in row["validation"]),
    }
    lines = ["# Coalition certificate diagnostic", "", "Generated from `results.json`; exploratory synthetic results.", "",
             "## Analytical cases", "", "| Case | Actual excess | Fixed score | Best shared score / fractional LP |",
             "| --- | ---: | ---: | ---: |"]
    for row in rows[:4]:
        lines.append(f"| {row['id']} | {row['exact']['excess']:.6g} | {row['fixed_population']['bound']:.6g} | {row['fractional_primal']['bound']:.6g} |")
    lines += ["", "## Entire prespecified grid", "", "| Check | Value |", "| --- | ---: |"]
    for name, value in metrics.items():
        lines.append(f"| {name} | {value:.10g} |")
    lines += ["", "## Finite samples", "", "Means below are diagnostic averages over heterogeneous synthetic instances, not estimated deployment performance.", "",
              "| Validation size | Mean moment bound minus actual excess | Mean enumeration bound minus actual excess |",
              "| ---: | ---: | ---: |"]
    for j, size in enumerate(SIZES):
        moment = np.mean([r["validation"][j]["moment"]["upper"] - r["exact"]["excess"] for r in rows])
        enumeration = np.mean([r["validation"][j]["enumeration"]["upper"] - r["exact"]["excess"] for r in rows])
        lines.append(f"| {size} | {moment:.6g} | {enumeration:.6g} |")
    lines += ["", "Every rule and score is fixed before validation. Each entry uses delta=0.05/6,",
              "covering the two methods and three prespecified sample sizes simultaneously per instance.",
              "Coverage counts do not prove the confidence guarantee. Population inequalities and",
              "independent optimizations are checked separately. All cases and sampling counts are saved.", "",
              "The population best-score LP knows the true finite law; it is an oracle diagnostic,",
              "not a finite-sample method or an equal-information competitor. Its support size may",
              "grow exponentially in the number of producers.", ""]
    return metrics, "\n".join(lines)


def main():
    cases = []
    for i, (name, q, p, penalties) in enumerate(analytical_cases()):
        cases.append(evaluate(name, q, p, penalties, True, 2026102800 + i))
    for n in [3, 4, 5, 6]:
        for family in FAMILIES:
            for seed in SEEDS:
                q, p = random_case(n, family, seed)
                for over, under in PENALTIES:
                    name = f"n{n}_{family}_seed{seed}_over{over:g}_under{under:g}"
                    cases.append(evaluate(name, q, p, (over, under), seed == SEEDS[0],
                                          2026102800 + len(cases)))
    sources = ["src/censored_newsvendor/coalition_audit.py", "scripts/check_coalition_certificate.py",
               "docs/coalition_certificate_protocol.md", "tests/test_coalition_certificate.py"]
    payload = {"date": "2026-10-28", "purpose": "Baseline certificate and structural-gap diagnostic; novelty not claimed",
               "grid": {"n": [3, 4, 5, 6], "families": FAMILIES, "seeds": SEEDS,
                        "penalties": PENALTIES, "validation_sizes": SIZES, "delta_per_entry": DELTA},
               "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
               "source_sha256": {s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in sources},
               "cases": cases}
    out = ROOT / "results/certificates"
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    # Summary is derived from the serialized artifact, not a separate hand-built table.
    metrics, markdown = summary(json.loads((out / "results.json").read_text()))
    (out / "summary.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (out / "summary.md").write_text(markdown)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
