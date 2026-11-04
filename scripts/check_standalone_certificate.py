"""Prespecified known-law comparison with fresh, independent iid streams."""

import hashlib
import json
import platform
from dataclasses import asdict
from math import comb
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, loss, optimal_offer
from censored_newsvendor.face_residuals import empirical_law, fit_prices, residual_certificate
from censored_newsvendor.standalone_certificate import (
    block_gap_certificate, fit_standalone_audit, marginal_certificate, standalone_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/certificates/results.json"
EXCLUSION = ROOT / "results/exclusion/results.json"
SIZES = (256, 1024, 4096)
DELTA = .05 / 18
METHODS = ("paired", "bonferroni", "dkw_full", "capacity_full", "face", "blocks")
RATIO_METHODS = METHODS[:4]


def rng_for(index, stream):
    entropy = [20261104, index, stream]
    return np.random.default_rng(np.random.SeedSequence(entropy)), entropy


def compare(rule, pilot, validation):
    result, seconds = {}, {}
    audit = fit_standalone_audit(rule, pilot)
    tasks = {
        "paired": lambda: standalone_certificate(rule, audit, validation, DELTA),
        "bonferroni": lambda: standalone_certificate(rule, audit, validation, DELTA, bonferroni=True),
        "dkw_full": lambda: marginal_certificate(rule, audit, pilot, validation, DELTA),
        "capacity_full": lambda: marginal_certificate(rule, audit, pilot, validation, DELTA, capacity_only=True),
        "face": lambda: residual_certificate(rule, fit_prices(rule, empirical_law(pilot)), validation, DELTA),
        "blocks": lambda: block_gap_certificate(rule, audit, validation, DELTA),
    }
    for name, run in tasks.items():
        start = perf_counter()
        result[name] = run()
        seconds[name] = perf_counter() - start
    # Retain all scalar certificates; large per-face interval arrays are not needed.
    result["face"] = {k: v for k, v in result["face"].items() if k != "faces"}
    return {"m": len(validation), "audit": asdict(audit), "methods": result,
            "paired_face_gap": min(result["paired"]["gap_upper"], result["face"]["gap_upper"]),
            "seconds_excluding_shared_audit_fit": seconds}


def check_case(index, name, group, rule, grand, rho, b, d1, draws, streams, source):
    comparisons = []
    actual_gap = max(0., d1 - b)
    oracle_gap = (1 - rho) * max(0., (1 - rule.weights.min()) * grand - b)
    if actual_gap > oracle_gap + 1e-8:
        raise AssertionError(f"Population corollary failed for {name}")
    for m in SIZES:
        result = compare(rule, draws[0][:m], draws[1][:m])
        result["gap_covered"] = {k: v["gap_upper"] + 1e-8 >= actual_gap
                                  for k, v in result["methods"].items()}
        result["rho_covered"] = {k: v["rho_lower"] <= rho + 1e-8
                                  for k, v in result["methods"].items() if k in RATIO_METHODS}
        comparisons.append(result)
    return {"id": name, "group": group, "stream_index": index, "n": len(rule.weights),
            "rule": {"offer": rule.offer, "weights": rule.weights.tolist(), "rated": rule.rated.tolist(),
                     "over": rule.over, "under": rule.under, "tie_score": rule.tie_score},
            "maximum_loss": rule.loss_range, "grand_cost": grand, "rho": rho,
            "B": b, "D1": d1, "oracle_gap_upper": float(oracle_gap), "source": source,
            "streams": streams, "comparison": comparisons}


def original_case(index, record, d1):
    r = record["rule"]
    rule = FrozenRule(r["offer"], r["weights"], r["rated"], record["over"], record["under"], r["tie_score"])
    if (rule.weights <= 0).any():
        return None
    truth = FiniteLaw(**record["truth"])
    grand = float(truth.probabilities @ loss(rule.offer, truth.states.sum(axis=1), rule.over, rule.under))
    costs = np.array([optimal_offer(y, truth.probabilities, rule.over, rule.under)[1] for y in truth.states.T])
    positive = costs > 0
    rho = min(1., float(np.min(rule.weights[positive] * grand / costs[positive]))) if positive.any() else 1.
    draws, streams = [], []
    for stream in (0, 1):
        rng, entropy = rng_for(index, stream)
        ix = rng.choice(len(truth.states), max(SIZES), p=truth.probabilities)
        draws.append(truth.states[ix])
        streams.append({"entropy": entropy, "counts": {
            str(m): np.bincount(ix[:m], minlength=len(truth.states)).tolist() for m in SIZES}})
    name = record["id"]
    group = "heterogeneous" if "_same_total_" in name or "_shifted_" in name else "original"
    source = {"path": str(BASE.relative_to(ROOT)), "case_index": index,
              "standalone_costs": costs.tolist()}
    return check_case(index, name, group, rule, grand, rho, record["exact"]["excess"],
                      d1, draws, streams, source)


def control_case(index, n, target):
    mad = sum(comb(n, k) * abs(k - n / 2) for k in range(n + 1)) / 2 ** n
    independent_rho = 2 * mad / n
    mixture = (target - independent_rho) / (1 - independent_rho)
    assert 0 <= mixture <= 1
    grand = mixture * n / 2 + (1 - mixture) * mad
    rule = FrozenRule(n / 2, np.full(n, 1 / n), np.ones(n))
    draws, streams = [], []
    for stream in (0, 1):
        rng, entropy = rng_for(index, stream)
        y = rng.integers(0, 2, size=(max(SIZES), n)).astype(float)
        common = rng.random(max(SIZES)) < mixture
        common_coin = rng.integers(0, 2, size=max(SIZES)).astype(float)
        y[common] = common_coin[common, None]
        draws.append(y)
        streams.append({"entropy": entropy, "array_sha256": hashlib.sha256(y.tobytes()).hexdigest(),
                        "common_rows": {str(m): int(common[:m].sum()) for m in SIZES}})
    source = {"model": "common/independent Bernoulli(0.5) mixture", "common_probability": mixture,
              "independent_rho": independent_rho, "target_rho": target,
              "population_reference": "Binomial expected absolute deviation and exchangeability; B=D1=0"}
    return check_case(index, f"exchangeable_n{n}_rho{target:g}", "control", rule, grand,
                      2 * grand / n, 0., 0., draws, streams, source)


def aggregate(rows, j):
    comparisons = [r["comparison"][j] for r in rows]
    metrics = {}
    for method in METHODS:
        certificates = [c["methods"][method] for c in comparisons]
        normalized = np.array([c["gap_upper"] / r["maximum_loss"] for r, c in zip(rows, certificates)])
        item = {"mean_gap_upper_over_A": float(normalized.mean()),
                "small_gap_count": int((normalized <= .05 + 1e-12).sum()),
                "gap_coverage_failures": sum(not c["gap_covered"][method] for c in comparisons),
                "fallbacks": sum(c["fallback"] for c in certificates),
                "total_seconds_excluding_shared_audit_fit": sum(c["seconds_excluding_shared_audit_fit"][method] for c in comparisons)}
        if method in RATIO_METHODS:
            item.update({"half_certified": sum(c["half_certified"] for c in certificates),
                         "false_half_certified": sum(c["half_certified"] and r["rho"] < .5 - 1e-10
                                                     for r, c in zip(rows, certificates)),
                         "rho_coverage_failures": sum(not c["rho_covered"][method] for c in comparisons),
                         "mean_rho_shortfall": float(np.mean([r["rho"] - c["rho_lower"]
                                                              for r, c in zip(rows, certificates)]))})
        metrics[method] = item
    combined = [c["paired_face_gap"] / r["maximum_loss"] for r, c in zip(rows, comparisons)]
    strong = [(r, c) for r, c in zip(rows, comparisons) if r["rho"] >= .6 - 1e-10]
    boundary = [(r, c) for r, c in zip(rows, comparisons) if abs(r["rho"] - .5) <= 1e-10]
    return {"cases": len(rows), "m": SIZES[j], "methods": metrics,
            "combined": {"mean_gap_upper_over_A": float(np.mean(combined)),
                         "small_gap_count": sum(v <= .05 + 1e-12 for v in combined)},
            "population": {"rho_ge_half": sum(r["rho"] >= .5 - 1e-10 for r in rows),
                           "rho_ge_six_tenths": len(strong),
                           "oracle_small_gap": sum(r["oracle_gap_upper"] <= .05 * r["maximum_loss"] + 1e-12 for r in rows)},
            "strong_half_detections": {k: sum(c["methods"][k]["half_certified"] for _, c in strong) for k in RATIO_METHODS},
            "boundary_cases": len(boundary),
            "boundary_half_detections": {k: sum(c["methods"][k]["half_certified"] for _, c in boundary) for k in RATIO_METHODS},
            "paired_grid_dominates_cap": sum(c["methods"]["paired"]["rho_grid"] >
                                              c["methods"]["paired"]["rho_capacity"] + 1e-10 for c in comparisons),
            "paired_grid_half_detections": sum(c["methods"]["paired"]["rho_grid"] >= .5 for c in comparisons)}


def summarize(payload):
    rows = payload["cases"]
    groups = {"original": [r for r in rows if r["group"] != "control"],
              "heterogeneous": [r for r in rows if r["group"] == "heterogeneous"],
              "controls": [r for r in rows if r["group"] == "control"]}
    stats = {k: [aggregate(v, j) for j in range(len(SIZES))] for k, v in groups.items()}
    final = stats["original"][-1]
    detections, eligible = final["strong_half_detections"]["paired"], final["population"]["rho_ge_six_tenths"]
    false = final["methods"]["paired"]["false_half_certified"]
    hetero = stats["heterogeneous"][-1]
    stats["gate"] = {"strong_detections": detections, "eligible_strong_cases": eligible,
                     "false_half_certified": false,
                     "conditional_detection_pass": detections >= .8 * eligible and false == 0,
                     "broad_precision_pass": hetero["methods"]["paired"]["small_gap_count"] >= hetero["cases"] / 2,
                     "combined_precision_pass": hetero["combined"]["small_gap_count"] >= hetero["cases"] / 2}
    lines = ["# Standalone-cost certificate: fresh iid comparison", "",
             "Generated from results.json. M pilot plus M validation observations; all methods use the same draws.",
             "Each method-size pair has delta = 0.05/18; the 18 guarantees are simultaneous per instance at level 0.95.",
             "This is not a 95% joint guarantee over all instances, and one draw per law is not a power study.",
             "The estimand is D1−B, the relaxation error, not B itself. A is maximum possible grand loss.", "",
             "## Mean certified gap divided by A", "",
             "| Group | M | Paired | Bonferroni | DKW, 2M | Capacity, 2M | Face | Blocks | Paired + face |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for group, entries in stats.items():
        if group == "gate":
            continue
        for s in entries:
            numbers = [s["methods"][k]["mean_gap_upper_over_A"] for k in METHODS] + [s["combined"]["mean_gap_upper_over_A"]]
            lines.append(f"| {group} | {s['m']} | " + " | ".join(f"{v:.5f}" for v in numbers) + " |")
    lines += ["", "## Number certifying a gap at most 5% of A", "",
              "| Group | M | Paired | Bonferroni | DKW, 2M | Capacity, 2M | Face | Blocks | Paired + face |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for group in groups:
        for s in stats[group]:
            counts = [s["methods"][k]["small_gap_count"] for k in METHODS] + [s["combined"]["small_gap_count"]]
            lines.append(f"| {group} | {s['m']} | " + " | ".join(f"{v}/{s['cases']}" for v in counts) + " |")
    lines += ["", "## Conditional detection at M=4096", "",
              "| Group | True rho ≥ 0.6 | Paired | Bonferroni | DKW, 2M | Capacity, 2M | Paired grid alone ≥ 0.5 | Grid strictly improves cap |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for group in groups:
        s = stats[group][-1]
        counts = [s["strong_half_detections"][k] for k in RATIO_METHODS]
        lines.append(f"| {group} | {s['population']['rho_ge_six_tenths']} | " + " | ".join(map(str, counts)) +
                     f" | {s['paired_grid_half_detections']} | {s['paired_grid_dominates_cap']} |")
    lines += ["", "The last two columns count all cases in the group, not only rho ≥ 0.6 cases.",
              f"Conditional gate passed: **{stats['gate']['conditional_detection_pass']}** ({detections}/{eligible}; false half-certifications: {false}).",
              f"Broad precision gate passed: **{stats['gate']['broad_precision_pass']}**. Combined precision gate: **{stats['gate']['combined_precision_pass']}**.",
              "", "## Exchangeable controls at M=4096", "",
              "All controls have true B=D1=0; standalone ratios need not explain their exactness.", "",
              "| Case | True rho | Paired grid | Capacity rho | Final rho | Paired gap/A | Face gap/A | Blocks gap/A |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in groups["controls"]:
        c = r["comparison"][-1]["methods"]
        p = c["paired"]
        lines.append(f"| {r['id']} | {r['rho']:.2f} | {p['rho_grid']:.2f} | {p['rho_capacity']:.5f} | {p['rho_lower']:.5f} | " +
                     " | ".join(f"{c[k]['gap_upper']/r['maximum_loss']:.5f}" for k in ("paired", "face", "blocks")) + " |")
    gap_failures = {k: sum(not c["gap_covered"][k] for r in rows for c in r["comparison"]) for k in METHODS}
    rho_failures = {k: sum(not c["rho_covered"][k] for r in rows for c in r["comparison"]) for k in RATIO_METHODS}
    fallbacks = sum(v["fallback"] for r in rows for c in r["comparison"] for v in c["methods"].values())
    stats["diagnostics"] = {"gap_coverage_failures": gap_failures, "rho_coverage_failures": rho_failures, "fallbacks": fallbacks}
    lines += ["", "## Diagnostics and exclusions", "", f"Gap coverage failures: `{gap_failures}`.",
              f"Rho coverage failures: `{rho_failures}`. Numerical fallbacks: {fallbacks}.",
              "These observations check this run; finite-sample coverage follows from the assumptions and proof.",
              "Four original cases were excluded before sampling because their shares were not strictly positive:",
              "", *[f"- `{name}`" for name in payload["excluded_ids"]], "",
              "The block baseline solves n LPs per block. Recorded elapsed times exclude the shared pilot audit fit;",
              "they are descriptive single-process timings, not a controlled scalability benchmark."]
    return stats, "\n".join(lines) + "\n"


def main():
    original = json.loads(BASE.read_text())["cases"]
    d1s = {r["id"]: r["population"]["levels"][1]["upper"]
           for r in json.loads(EXCLUSION.read_text())["original_cases"]}
    rows, excluded = [], []
    for i, record in enumerate(original):
        row = original_case(i, record, d1s[record["id"]])
        if row is None:
            excluded.append(record["id"])
        else:
            rows.append(row)
        if (i + 1) % 10 == 0:
            print(f"Completed {i + 1}/100 original cases", flush=True)
    for n in (6, 12, 24):
        for target in (.4, .5, .6, .8):
            index = len(original) + len(rows) - (len(original) - len(excluded))
            rows.append(control_case(index, n, target))
            print(f"Completed control n={n}, rho={target}", flush=True)
    files = ["scripts/check_standalone_certificate.py", "src/censored_newsvendor/standalone_certificate.py",
             "docs/standalone_protocol.md", "src/censored_newsvendor/coalition_audit.py",
             "src/censored_newsvendor/exclusion.py", "src/censored_newsvendor/face_residuals.py",
             "results/certificates/results.json", "results/exclusion/results.json"]
    payload = {"date": "2026-11-04", "versions": {"python": platform.python_version(),
               "numpy": np.__version__, "scipy": scipy.__version__}, "sizes": SIZES,
               "delta_per_method_size": DELTA, "excluded_ids": excluded, "cases": rows,
               "sha256": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files}}
    directory = ROOT / "results/standalone"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "results.json"
    path.write_text(json.dumps(payload, separators=(",", ":"), allow_nan=False) + "\n")
    stats, md = summarize(json.loads(path.read_text()))
    (directory / "summary.json").write_text(json.dumps(stats, indent=2, allow_nan=False) + "\n")
    (directory / "summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
