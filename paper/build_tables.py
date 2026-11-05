"""Build the draft tables and citation subset from the saved research records.

No new experiments are run. Numerical assertions check consistency between
stored analytical values, LP values, counts and the displayed tables.
"""

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


PAPER = Path(__file__).resolve().parent
ROOT = PAPER.parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bib_entries(text):
    entries = {}
    for match in re.finditer(r"(?m)^@\w+\{([^,]+),", text):
        start = match.start()
        opening = text.index("{", start)
        depth = 1
        end = opening + 1
        while depth:
            if end >= len(text):
                raise ValueError("Unbalanced BibTeX entry")
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
            end += 1
        entry = text[start:end]
        # Reading-status notes remain in the root bibliography and source audit.
        entry = re.sub(r"\n  note=\{(?:[^{}]|\{[^{}]*\})*\},?", "", entry)
        entries[match.group(1)] = entry
    return entries


def main():
    inputs = [ROOT / "results/exclusion/sharp_gap.json",
              ROOT / "results/standalone/summary.json",
              ROOT / "results/standalone/diagnosis.json",
              ROOT / "results/exclusion/prior_art_checks.json",
              ROOT / "references.bib", PAPER / "main.tex", Path(__file__)]
    sharp, summary, diagnosis, prior = [
        json.loads(path.read_text()) for path in inputs[:4]]
    assert len(sharp["instances"]) == 18
    assert sum(len(row["levels"]) for row in sharp["instances"]) == 84
    for row in sharp["instances"]:
        assert row["integer_excess"] == 0
        for level in row["levels"]:
            assert abs(float(Fraction(level["exact_family_ratio"])) - level["lp_ratio"]) < 1e-8
    assert len(prior["instances"]) == 18
    assert sum(x["cost_identity_points"] for x in prior["instances"]) == 1968
    for name, digest in prior["sha256"].items():
        assert sha256(ROOT / name) == digest, name
    for row in prior["instances"]:
        assert abs(row["root_primal"] - row["root_dual"]) < 1e-10
        assert abs(row["root_primal"] - row["burer_positive_negative_part"]) < 1e-10
    assert prior["canonical_example"]["exact_canonical_cost"] == "2/3"

    table_dir = PAPER / "tables"
    table_dir.mkdir(exist_ok=True)
    rows = [r"\begin{tabular}{lrrrrr}", r"\toprule",
            r"$m$ & $k=1$ & $k=2$ & $k=3$ & $k=4$ & $k=5$ \\",
            r"\midrule"]
    selected = [x for x in sharp["instances"] if x["n"] == 6 and x["share_units"] == [1] * 6]
    assert [x["size"] for x in selected] == [2, 20, 200]
    for row in selected:
        values = [f"{float(Fraction(x['exact_family_ratio'])):.6f}" for x in row["levels"]]
        rows.append(str(row["size"]) + " & " + " & ".join(values) + r" \\")
    rows.extend([r"\midrule",
                 r"Supremum & $5/6$ & $2/3$ & $1/2$ & $1/3$ & $0$ \\",
                 r"\bottomrule", r"\end{tabular}", ""])
    (table_dir / "sharp_family.tex").write_text("\n".join(rows))

    hetero = next(x for x in summary["heterogeneous"] if x["m"] == 4096)
    original = next(x for x in summary["original"] if x["m"] == 4096)
    assert hetero["cases"] == 47
    assert hetero["population"]["oracle_small_gap"] == 8
    assert original["population"]["rho_ge_six_tenths"] == 35
    assert all(original["strong_half_detections"][k] == 35
               for k in ("paired", "bonferroni", "dkw_full"))
    methods = [("paired", "Paired ratio (IUT/fixed sequence)"),
               ("bonferroni", "Bonferroni ratio"),
               ("dkw_full", "Marginal DKW, pooled moments"),
               ("capacity_full", "Capacity bound, pooled moments"),
               ("face", "Pilot-fitted face prices"),
               ("blocks", "Paired SAA blocks (size 64)")]
    rows = [r"\begin{tabular}{lrr}", r"\toprule",
            r"Method & Mean $G/A$ & $G\le0.05A$ \\",
            r"\midrule"]
    for key, label in methods:
        result = hetero["methods"][key]
        rows.append(f"{label} & {result['mean_gap_upper_over_A']:.6f} & "
                    f"{result['small_gap_count']}/{hetero['cases']}" + r" \\")
    rows.extend([r"\bottomrule", r"\end{tabular}", ""])
    (table_dir / "validation.tex").write_text("\n".join(rows))

    main_text = (PAPER / "main.tex").read_text()
    cited = set()
    for group in re.findall(r"\\cite[pt]?(?:\[[^]]*\])*\{([^}]+)\}", main_text):
        cited.update(x.strip() for x in group.split(","))
    entries = bib_entries((ROOT / "references.bib").read_text())
    missing = cited - entries.keys()
    assert not missing, missing
    (PAPER / "references.bib").write_text(
        "% Generated from the root bibliography; only cited entries are included.\n\n"
        + "\n\n".join(entries[key] for key in sorted(cited)) + "\n")
    outputs = [table_dir / "sharp_family.tex", table_dir / "validation.tex",
               PAPER / "references.bib"]
    payload = {
        "scope": "Manuscript assembly from saved outcomes; no new sampling",
        "inputs_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in inputs},
        "outputs_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in outputs},
        "deterministic_laws": 18, "depth_values": 84, "root_comparisons": 18,
        "norm_identity_points": 1968, "references": sorted(cited),
        "heterogeneous_cases": 47, "pilot_and_validation_size_each": 4096,
        "broad_gate_passed": False,
    }
    (PAPER / "build_manifest.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Built 2 tables and {len(cited)} cited references; checked source hashes and stored numerical identities.")


if __name__ == "__main__":
    main()
