"""Post-run error decomposition from saved outcomes, without new fitted prices."""

import hashlib
import json
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "results/residuals"


def diagnose(rows):
    records = []
    for row in rows:
        comparison = next(c for c in row["comparison"] if c["m"] == 4096)
        finite = comparison["primary"]
        population = comparison["frozen_prices_population"]
        a, b = row["maximum_loss"], row["B"]
        records.append({
            "id": row["id"],
            "structural_gap": (row["D1"] - b) / a,
            "same_prices_population_gap_bound": population["gap_upper"] / a,
            "finite_gap_bound": finite["gap_upper"] / a,
            "same_prices_population_upper_slack": (population["upper"] - b) / a,
            "statistical_upper_expansion": (finite["upper"] - population["upper"]) / a,
            "finite_upper_slack": (finite["upper"] - b) / a,
        })
    metrics = list(records[0])[1:]
    return {
        "cases": len(rows), "m": 4096,
        "mean": {k: mean(r[k] for r in records) for k in metrics},
        "median": {k: median(r[k] for r in records) for k in metrics},
        "at_most_five_percent": {
            k: sum(r[k] <= .05 + 1e-12 for r in records)
            for k in ("structural_gap", "same_prices_population_gap_bound", "finite_gap_bound")
        },
        "instances": records,
    }


def main():
    source = DIRECTORY / "results.json"
    data = json.loads(source.read_text())
    groups = {
        "original": data["cases"][:100],
        "heterogeneous": [r for r in data["cases"] if r["group"] == "heterogeneous"],
        "mixtures": data["cases"][100:],
    }
    payload = {
        "date": "2026-11-01",
        "scope": "Post-run diagnosis. Prices remain fitted to the original pilot. Only validation moments are replaced by population moments.",
        "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (source, Path(__file__))},
        "groups": {name: diagnose(rows) for name, rows in groups.items()},
    }
    path = DIRECTORY / "diagnosis.json"
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    saved = json.loads(path.read_text())
    lines = [
        "# Where the face-price certificate loses precision", "",
        "Post-run decomposition at 4,096 pilot and 4,096 validation observations. All amounts are divided by the maximum grand loss A.",
        "The population calculation retains the very same pilot-fitted prices. It replaces estimated moments by their exact expectations under the known synthetic law.", "",
        "| Group | True D1−B, mean | Same-price population gap bound, mean | Finite gap bound, mean | Population gap bound ≤ 5% A | Finite gap bound ≤ 5% A |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, group in saved["groups"].items():
        m, counts, n = group["mean"], group["at_most_five_percent"], group["cases"]
        lines.append(f"| {name} | {m['structural_gap']:.6f} | {m['same_prices_population_gap_bound']:.6f} | {m['finite_gap_bound']:.6f} | {counts['same_prices_population_gap_bound']}/{n} | {counts['finite_gap_bound']}/{n} |")
    lines += ["", "## Upper-bound slack decomposition", "",
              "| Group | Population upper minus B | Finite upper minus population upper | Finite upper minus B |",
              "| --- | ---: | ---: | ---: |"]
    for name, group in saved["groups"].items():
        m = group["mean"]
        lines.append(f"| {name} | {m['same_prices_population_upper_slack']:.6f} | {m['statistical_upper_expansion']:.6f} | {m['finite_upper_slack']:.6f} |")
    lines += ["",
              "This isolates conservative statistical estimation within this implementation. It does not prove that uncertainty is intrinsically this large or that a different certificate will achieve a particular rate.",
              "All 48 heterogeneous population gaps are at most 5% A. This grid tests certification of small gaps, rather than balanced classification of small and large gaps. The explicit 7/50 structural obstruction is checked separately in the regression tests.", ""]
    md = "\n".join(lines)
    (DIRECTORY / "diagnosis.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
