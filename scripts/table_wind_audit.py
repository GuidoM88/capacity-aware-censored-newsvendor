"""LaTeX table for the paper from results/illustration/wind_audit.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    rows = json.loads((ROOT / "results/illustration/wind_audit.json").read_text())["rows"]
    lines = [r"\begin{tabular}{llrrrrrrr}", r"\toprule",
             r"panel, year & allocation & $\kappa$ & $r$ & $B/L$ & \multicolumn{2}{c}{depth one} & "
             r"\multicolumn{2}{c}{depth two}\\",
             r"&&&&& observed & worst case & observed & worst case\\", r"\midrule"]
    for r in rows:
        worst1 = (f"{r['depth1_lower']:.4f}" if abs(r["depth1_upper"] - r["depth1_lower"]) < 5e-5
                  else f"{r['depth1_lower']:.4f}--{r['depth1_upper']:.4f}")
        panel = r["panel"].split(" ")[0]
        lines.append(f"{panel} {r['year']} & {r['allocation']} & {r['kappa']} & {r['r']:.3f} & {r['B_over_L']:.4f} & "
                     f"{r['gap1']:.4f} & {worst1} & {r['gap2']:.4f} & {r['depth2_exact']:.4f}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    (ROOT / "paper_exact/wind_table.tex").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
