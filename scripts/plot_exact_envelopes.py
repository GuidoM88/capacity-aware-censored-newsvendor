"""Figure: exact depth-one worst gap against the standalone floor r.

One panel per number of producers (equal shares). The solid line is the worst
gap: Theorem 1 outside the windows, and inside them the best explicit law,
which equals the certificate bound at every ratio checked
(results/exclusion/window_envelopes.md) and is proved for n = 4 (Theorem 3).
The dashed line is the C31 ceiling (1-r)(n-1)/n; shaded bands are windows.
The plotted values are also written to a CSV next to the figure.
"""

import csv
from fractions import Fraction as F
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from censored_newsvendor.exact_envelopes import (  # noqa: E402
    best_equal_share_construction, equal_share_value, windows,
)

ROOT = Path(__file__).resolve().parents[1]
INK, MUTED, ACCENT, BAND, SURFACE = "#0b0b0b", "#52514e", "#2a78d6", "#e9e8e4", "#fcfcfb"
SIZES = (4, 5, 6, 8)
STEPS = 400


def worst_gap(n, r):
    value = equal_share_value(n, r)
    if value is None:
        value = best_equal_share_construction(n, r)["value"]
    return value


def main():
    rows = []
    fig, axes = plt.subplots(2, 2, figsize=(9.0, 6.4), sharex=True, sharey=True,
                             facecolor=SURFACE)
    for ax, n in zip(axes.flat, SIZES):
        ratios = [F(k, STEPS) for k in range(4, STEPS + 1)]
        exact = [float(worst_gap(n, r)) for r in ratios]
        ceiling = [float((1 - r) * (n - 1) / n) for r in ratios]
        gaps = windows(n)
        for r, e, c in zip(ratios, exact, ceiling):
            rows.append({"n": n, "r": float(r), "worst_gap": e, "c31": c,
                         "in_window": any(lo < r < hi for lo, hi in gaps)})
        ax.set_facecolor(SURFACE)
        for lo, hi in gaps:
            ax.axvspan(float(lo), float(hi), color=BAND, linewidth=0, zorder=0)
        x = [float(r) for r in ratios]
        ax.plot(x, ceiling, color=MUTED, linewidth=1.3, linestyle=(0, (4, 3)), zorder=2,
                label="C31 ceiling (1-r)(n-1)/n")
        ax.plot(x, exact, color=ACCENT, linewidth=1.8, zorder=3, label="exact worst gap")
        threshold = (n - 2) / n
        ax.axvline(threshold, color=MUTED, linewidth=0.6, linestyle=":", zorder=1)
        ax.text(threshold + 0.012, 0.03, "(n-2)/n", color=MUTED, fontsize=8)
        ax.set_title(f"{n} producers, equal shares", color=INK, fontsize=10, loc="left")
        ax.grid(axis="y", color="#e2e1dd", linewidth=0.6)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#b9b8b2")
        ax.tick_params(colors=MUTED, labelsize=8)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 0.9)
    for ax in axes[1]:
        ax.set_xlabel("standalone floor r (every charge covers at least r of its standalone cost)",
                      color=INK, fontsize=8.5)
    for ax in axes[:, 0]:
        ax.set_ylabel("(D1 - B) / L", color=INK, fontsize=9)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    handles.append(plt.Rectangle((0, 0), 1, 1, color=BAND))
    labels.append("window (value set by the families H_p, V_p)")
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, fontsize=8.5,
               labelcolor=INK, bbox_to_anchor=(0.5, 0.995))
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    output = ROOT / "results/exclusion/exact_envelopes.png"
    fig.savefig(output, dpi=200, facecolor=SURFACE)
    with open(output.with_name("exact_envelopes_curve.csv"), "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {output.relative_to(ROOT)} and {len(rows)} plotted values.")


if __name__ == "__main__":
    main()
