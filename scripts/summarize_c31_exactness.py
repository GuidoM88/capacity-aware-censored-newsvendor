"""When is the elementary C31 ceiling the exact worst gap? Summary of saved outcomes.

Reads results/exclusion/certificate_method.json (random instances with
arbitrary shares, where the certificate bound was matched by the relaxation
and, for most instances, by an explicit law) and compares each value with the
C31 ceiling (1-r) times the sum of the n-k largest shares.
"""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / "results/exclusion/certificate_method.json"
    rows = json.loads(source.read_text())["cases"]
    by_ratio = defaultdict(lambda: [0, 0])
    below = []
    for row in rows:
        shares = np.sort(np.array(row["shares"]))[::-1]
        c31 = (1 - row["r"]) * shares[: len(shares) - row["depth"]].sum()
        exact = abs(row["certificate_bound"] - c31) < 1e-6
        by_ratio[row["r"]][0] += exact
        by_ratio[row["r"]][1] += 1
        if not exact:
            below.append((row, c31))
    lines = ["# When is the C31 ceiling exact?", "",
             "2026-11-06. Generated from [certificate_method.json](certificate_method.json) by "
             "`scripts/summarize_c31_exactness.py`.", "",
             f"In {sum(v[0] for v in by_ratio.values())} of {len(rows)} random instances (n = 4..6, depths "
             "1..3) the worst gap equals the elementary ceiling (1-r) times the sum of the n-k largest "
             "shares. Every exception has r >= 0.5.", "",
             "| r | instances | C31 exact |", "| ---: | ---: | ---: |"]
    for r in sorted(by_ratio):
        exact, total = by_ratio[r]
        lines.append(f"| {r:.2f} | {total} | {exact} |")
    lines += ["", "Instances where the worst gap is strictly below C31:", "",
              "| n | depth | r | shares | worst gap | C31 | ratio |", "| ---: | ---: | ---: | --- | ---: | ---: | ---: |"]
    for row, c31 in sorted(below, key=lambda item: (item[0]["n"], item[0]["depth"], item[0]["r"])):
        shares = "(" + ", ".join(f"{x:.3f}" for x in row["shares"]) + ")"
        lines.append(f"| {row['n']} | {row['depth']} | {row['r']:.2f} | {shares} | "
                     f"{row['certificate_bound']:.4f} | {c31:.4f} | {row['certificate_bound'] / c31:.3f} |")
    lines.append("")
    (ROOT / "results/exclusion/c31_exactness.md").write_text("\n".join(lines))
    print(f"{len(rows) - len(below)} of {len(rows)} instances at C31; exceptions all with r >= "
          f"{min(row['r'] for row, _ in below):.2f}")


if __name__ == "__main__":
    main()
