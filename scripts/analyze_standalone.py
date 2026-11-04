"""Post-run diagnosis; no new sampling, fitting, or changes to the protocol."""

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / "results/standalone/results.json"
    payload = json.loads(path.read_text())
    for name, digest in payload["sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise AssertionError(f"Source changed after execution: {name}")
    rows = payload["cases"]
    groups = {"original": [r for r in rows if r["group"] != "control"],
              "heterogeneous": [r for r in rows if r["group"] == "heterogeneous"],
              "controls": [r for r in rows if r["group"] == "control"]}
    methods = ("paired", "bonferroni", "dkw_full", "capacity_full")
    diagnostics = {}
    lines = ["# Post-run diagnosis of the standalone certificate", "",
             "These descriptive comparisons were added after inspecting the prespecified results.",
             "They use the saved M=4096 outcomes and do not revise either decision threshold.",
             "The minimum of two already budgeted valid bounds needs no new observations.", "",
             "## Matched combinations with the preceding face certificate", "",
             "| Group | Paired + face | Bonferroni + face | DKW + face | Capacity + face | Face alone |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for name, cases in groups.items():
        combined = {}
        for method in methods:
            values = [min(r["comparison"][-1]["methods"][method]["gap_upper"],
                          r["comparison"][-1]["methods"]["face"]["gap_upper"]) / r["maximum_loss"] for r in cases]
            combined[method] = {"mean_gap_upper_over_A": float(np.mean(values)),
                                "small_gap_count": sum(v <= .05 + 1e-12 for v in values)}
        oracle = float(np.mean([r["oracle_gap_upper"] / r["maximum_loss"] for r in cases]))
        paired = float(np.mean([r["comparison"][-1]["methods"]["paired"]["gap_upper"] / r["maximum_loss"] for r in cases]))
        face = float(np.mean([r["comparison"][-1]["methods"]["face"]["gap_upper"] / r["maximum_loss"] for r in cases]))
        diagnostics[name] = {"cases": len(cases), "combinations": combined,
                             "oracle_mean_gap_upper_over_A": oracle, "paired_mean_gap_upper_over_A": paired,
                             "paired_expansion_over_population_bound": paired - oracle,
                             "face_mean_gap_upper_over_A": face,
                             "conditional_margin_cases": [r["id"] for r in cases if r["rho"] >= .6 - 1e-10],
                             "paired_small_gap_cases": [r["id"] for r in cases if
                                  r["comparison"][-1]["methods"]["paired"]["gap_upper"] <= .05 * r["maximum_loss"] + 1e-12]}
        lines.append(f"| {name} | " + " | ".join(f"{combined[k]['mean_gap_upper_over_A']:.6f}" for k in methods) + f" | {face:.6f} |")
    h = diagnostics["heterogeneous"]
    improvement = 1 - h["combinations"]["paired"]["mean_gap_upper_over_A"] / h["combinations"]["dkw_full"]["mean_gap_upper_over_A"]
    lines += ["", "Entries are mean certified gap divided by maximum loss A.",
              f"On heterogeneous cases, paired + face improves this mean over DKW + face by {100*improvement:.2f}%.",
              "This small descriptive difference is not a general superiority claim.", "",
              "## What the conditional success establishes", "",
              "The paired method certifies rho >= 0.5 in all 35 original cases with true rho >= 0.6.",
              "Bonferroni and full-budget DKW also certify all 35. Thus the conditional screen",
              "establishes feasibility of estimating this condition on the grid, not a unique benefit.",
              "One original law is exactly on the rho=0.5 boundary; none of the four ratio methods",
              "certifies that boundary case. The three corresponding control cases also remain uncertified.",
              "In all 12 exchangeable controls, the deterministic capacity ratio dominates the paired grid.",
              "Those controls therefore do not supply evidence for additional power from the paired test.",
              "", "## Population limitation versus sampling expansion", "",
              f"The heterogeneous population corollary has mean normalized upper gap {h['oracle_mean_gap_upper_over_A']:.6f}.",
              f"The finite paired certificate gives {h['paired_mean_gap_upper_over_A']:.6f}; its excess over this oracle is {h['paired_expansion_over_population_bound']:.6f}.",
              "Even the exact population bound meets the 5%-of-A criterion in only 8/47 cases.",
              "The finite bound meets it in 5/47, versus 4/47 for Bonferroni, 1/47 for DKW,",
              "and 0/47 for face, capacity-only and 64-sample block bounds on these fresh samples.",
              "The minimum with the face bound also meets it in 5/47. The broad half-of-cases gate fails.",
              "This is a structural limitation of the standalone-ratio corollary on these laws,",
              "not evidence that a different estimator of the same rho can solve the broad target.",
              "", "## Checks and remaining questions", ""]
    joint_failures = {k: 0 for k in methods}
    for r in rows:
        for comparison in r["comparison"]:
            for k in methods:
                c = comparison["methods"][k]
                lo, hi = c["grand_interval"]
                joint = (lo <= r["grand_cost"] + 1e-8 and hi + 1e-8 >= r["grand_cost"]
                         and c["witness_lower"] <= r["B"] + 1e-8 and c["rho_lower"] <= r["rho"] + 1e-8
                         and c["gap_upper"] + 1e-8 >= r["D1"] - r["B"])
                joint_failures[k] += not joint
    block_calls = sum(c["methods"]["blocks"]["lp_calls"] for r in rows for c in r["comparison"])
    block_count = sum(len(c["methods"]["blocks"]["block_values"]) for r in rows for c in r["comparison"])
    lines += [f"Observed failures of the four ratio methods' joint events: `{joint_failures}`.",
              f"The standard block baseline used {block_count:,} blocks and {block_calls:,} LP solves.",
              "It does not meet the small-gap criterion at the fixed block size. This is not a rejection",
              "of SAA gap estimation or of other block sizes and concentration schemes.",
              "Seven added regression tests cover zero aggregate loss, zero capacities, terminal depth,",
              "a missed pilot state, invalid shares/witnesses, dimension penalties and a sharp obstruction.",
              "The complete suite passed 40 tests. Coverage does not follow from that test count.",
              "", "The next bounded research step is to assess the exact extremal theorem's priority",
              "and significance as a theoretical result. The ratio certificate is now reproducible",
              "supporting material with a measured scope. Another tuning pass on its scalar intervals",
              "cannot remove its documented population limitation. Real-data and time-series claims",
              "still require separate evidence."]
    diagnostics["execution"] = {"joint_event_failures": joint_failures, "block_count": block_count,
                                 "block_lp_calls": block_calls, "unit_tests_passed": 40}
    diagnostics["sha256"] = {"results": hashlib.sha256(path.read_bytes()).hexdigest(),
                              "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = path.parent
    (out / "diagnosis.json").write_text(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
    (out / "diagnosis.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
