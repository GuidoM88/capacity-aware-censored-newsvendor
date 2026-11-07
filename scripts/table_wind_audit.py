"""LaTeX table for the paper from results/illustration/wind_audit.json.

One row per panel and allocation; ranges over the two years and the two
penalty ratios.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def span(values, digits=3):
    lo, hi = min(values), max(values)
    return f"{lo:.{digits}f}" if f"{lo:.{digits}f}" == f"{hi:.{digits}f}" else f"{lo:.{digits}f}--{hi:.{digits}f}"


def main():
    rows = json.loads((ROOT / "results/illustration/wind_audit.json").read_text())["rows"]
    lines = [r"\begin{tabular}{llcccccc}", r"\toprule",
             r"panel & allocation & $r$ & $B/L$ & \multicolumn{2}{c}{depth one} & "
             r"\multicolumn{2}{c}{depth two}\\",
             r"&&&& observed & worst case & observed & worst case\\", r"\midrule"]
    seen = []
    for r in rows:
        key = (r["panel"], r["allocation"])
        if key not in seen:
            seen.append(key)
    for panel, allocation in seen:
        group = [r for r in rows if r["panel"] == panel and r["allocation"] == allocation]
        lines.append(" & ".join([
            panel.split(" (")[0], allocation, span([r["r"] for r in group], 2),
            f"{max(r['B_over_L'] for r in group):.4f}",
            f"{max(r['gap1'] for r in group):.4f}",
            span([r["depth1_lower"] for r in group] + [r["depth1_upper"] for r in group]),
            f"{max(r['gap2'] for r in group):.4f}",
            span([r["depth2_exact"] for r in group])]) + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    (ROOT / "paper_exact/wind_table.tex").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
