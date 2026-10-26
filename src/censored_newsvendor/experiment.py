"""Reproduce the two-product population example and finite-scenario baseline."""

import argparse
import csv
import hashlib
import importlib.metadata
import itertools
import json
import platform
from pathlib import Path

import numpy as np

from .allocation import solve_allocation, total_cost
from .distributions import toy_marginals
from .robust import solve_finite_scenario_regret


def run_experiment(capacities):
    marginals = toy_marginals()
    names = ["".join(pair) for pair in itertools.product("AB", repeat=2)]
    scenarios = [tuple(marginals[key] for key in name) for name in names]
    observed = tuple(marginals["A"].censor(40) for _ in range(2))
    if observed[0] != marginals["B"].censor(40):
        raise RuntimeError("The two latent marginals must have identical censored laws.")
    rows = []
    for capacity in capacities:
        oracles = [solve_allocation(s, capacity) for s in scenarios]
        robust = solve_finite_scenario_regret(scenarios, capacity)
        decisions = {
            "sales_as_demand": solve_allocation(observed, capacity).quantities,
            "assume_A_tail": oracles[0].quantities,
            "finite_scenario_minimax": robust.quantities,
        }
        for name, scenario, oracle in zip(names, scenarios, oracles):
            policies = {"oracle": oracle.quantities, **decisions}
            for policy, q in policies.items():
                cost = total_cost(scenario, q)
                regret = cost - oracle.expected_cost
                if regret < -1e-7 or q.sum() > capacity + 1e-7:
                    raise RuntimeError("An experiment outcome failed the regret/feasibility check.")
                rows.append({
                    "capacity": float(capacity), "scenario": name, "policy": policy,
                    "q1": float(q[0]), "q2": float(q[1]),
                    "expected_cost": cost, "oracle_cost": oracle.expected_cost,
                    "regret": max(0.0, regret), "unused_capacity": max(0.0, capacity - float(q.sum())),
                })
    return rows


def plot_results(rows, destination):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    capacities = sorted({row["capacity"] for row in rows})
    lookup = {(r["capacity"], r["scenario"], r["policy"]): r for r in rows}
    colors = {"AA": "#475569", "AB": "#2563eb", "BA": "#dc2626", "BB": "#059669"}
    with plt.rc_context({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False}):
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), layout="constrained")
        for scenario, color in colors.items():
            axes[0].plot(capacities, [lookup[c, scenario, "oracle"]["q1"] for c in capacities],
                         label=f"Oracle {scenario}", color=color, linewidth=2,
                         linestyle=":" if scenario == "BB" else "-")
        axes[0].axhline(40, color="#94a3b8", linestyle="--", linewidth=1, label="Historical stock")
        axes[0].set(xlabel="Shared capacity", ylabel="Optimal quantity of product 1",
                    title="Identical sales histories, different optimal actions")
        labels = {
            "sales_as_demand": ("Sales as demand", "#dc2626"),
            "assume_A_tail": ("Assume both tails are A", "#64748b"),
            "finite_scenario_minimax": ("Minimax over four supplied scenarios", "#2563eb"),
        }
        for policy, (label, color) in labels.items():
            values = [max(lookup[c, s, policy]["regret"] for s in colors) for c in capacities]
            axes[1].plot(capacities, values, label=label, color=color, linewidth=2)
        axes[1].set(xlabel="Shared capacity", ylabel="Worst-case expected regret (cost units)",
                    title="Population comparison within the four-scenario family")
        for ax in axes:
            ax.axvline(80, color="#9ca3af", linestyle="--", linewidth=1)
            ax.grid(alpha=0.16)
            ax.legend(loc="upper left", fontsize=8)
        fig.suptitle("Censored newsvendor: capacity-dependent decision identifiability", fontsize=14)
        fig.savefig(destination, dpi=180)
        plt.close(fig)


def write_results(rows, output, make_plot=True):
    output.mkdir(parents=True, exist_ok=True)
    with (output / "capacity_sweep.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    source_root = Path(__file__).parent
    manifest = {
        "experiment": "two_product_population_example",
        "historical_stock": [40, 40], "underage": [4, 4], "overage": [1, 1],
        "resource_weights": [1, 1],
        "marginals": {key: {"knots": d.knots, "masses": d.masses} for key, d in toy_marginals().items()},
        "scenarios": ["AA", "AB", "BA", "BB"],
        "capacities": sorted({r["capacity"] for r in rows}),
        "evaluation": "Exact population expected loss; no sampling or fitted forecasting model.",
        "robust_scope": "Finite supplied scenario family only; not the full censoring ambiguity set.",
        "python": platform.python_version(),
        "dependencies": {name: importlib.metadata.version(name) for name in ["numpy", "scipy", "matplotlib"]},
        "source_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source_root.glob("*.py"))
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    report = [
        "# Population reference experiment", "",
        "Expected costs are integrated analytically. Capacity is an upper bound, not an equality.",
        "The finite-scenario baseline is given AA, AB, BA, BB in advance.", "",
        "| Capacity | Policy | Worst regret over AA/AB/BA/BB |",
        "| ---: | --- | ---: |",
    ]
    for capacity in [60, 80, 120, 200, 260]:
        for policy in ["sales_as_demand", "assume_A_tail", "finite_scenario_minimax"]:
            selected = [r for r in rows if r["capacity"] == capacity and r["policy"] == policy]
            if selected:
                report.append(f"| {capacity} | {policy} | {max(r['regret'] for r in selected):.6f} |")
    report += ["", "These results validate the constructed example. They do not establish novelty,",
               "finite-sample guarantees, or performance on retail data.", ""]
    (output / "summary.md").write_text("\n".join(report))
    if make_plot:
        plot_results(rows, output / "capacity_sweep.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/toy"))
    parser.add_argument("--max-capacity", type=int, default=260)
    parser.add_argument("--step", type=int, default=2)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()
    if args.max_capacity < 0 or args.step <= 0:
        parser.error("max-capacity must be nonnegative and step must be positive")
    capacities = list(range(0, args.max_capacity + 1, args.step))
    if capacities[-1] != args.max_capacity:
        capacities.append(args.max_capacity)
    rows = run_experiment(capacities)
    write_results(rows, args.output, make_plot=not args.no_plot)
    print(f"Wrote {len(rows)} outcomes across {len(capacities)} capacities to {args.output}")


if __name__ == "__main__":
    main()
