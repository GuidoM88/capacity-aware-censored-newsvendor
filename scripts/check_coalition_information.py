"""Check an information counterexample for forecast-based cost allocation.

This is a research-screening example, not a new allocation algorithm or a
claim of scientific novelty. Exact rational costs are checked against a
separate least-core linear program.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import scipy
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
PLAYERS = tuple(range(3))
COALITIONS = [s for size in (1, 2, 3) for s in combinations(PLAYERS, size)]
PROPER = [s for s in COALITIONS if len(s) < 3]


def distribution(states, indices):
    result = {}
    for state in states:
        total = sum(state[i] for i in indices)
        result[total] = result.get(total, Fraction(0)) + Fraction(1, len(states))
    return result


def optimal_cost(states, indices):
    """The minimum expected absolute loss occurs at a support point."""
    law = distribution(states, indices)
    return min(sum(p * abs(q - y) for y, p in law.items()) for q in law)


def coalition_name(indices):
    return "".join(str(i + 1) for i in indices)


def main():
    worlds = {}
    for k in PLAYERS:
        one_hot = tuple(int(i == k) for i in PLAYERS)
        worlds[f"Q{k + 1}"] = (one_hot, tuple(1 - y for y in one_hot))

    observed = [distribution(worlds["Q1"], s) for s in [(0,), (1,), (2,), PLAYERS]]
    for states in worlds.values():
        assert [distribution(states, s) for s in [(0,), (1,), (2,), PLAYERS]] == observed

    costs = {name: {s: optimal_cost(states, s) for s in COALITIONS}
             for name, states in worlds.items()}
    allocation = (Fraction(-1, 2), Fraction(1, 2), Fraction(1, 2))
    assert sum(allocation) == costs["Q1"][PLAYERS] == Fraction(1, 2)
    excess = {name: {s: sum(allocation[i] for i in s) - c for s, c in table.items()}
              for name, table in costs.items()}
    assert max(excess["Q1"].values()) == 0
    assert excess["Q2"][(1, 2)] == 1

    # At q=3/2, aggregate absolute loss is 1/2 in every state of every world.
    # Thus proportional ex-post scaling by realized/forecast aggregate cost
    # is exactly one; it does not remove the counterexample.
    assert all(abs(Fraction(3, 2) - sum(state)) == Fraction(1, 2)
               for states in worlds.values() for state in states)

    rows, rhs = [], []
    for table in costs.values():
        for s in PROPER:
            rows.append([int(i in s) for i in PLAYERS] + [-1])
            rhs.append(float(table[s]))
    result = linprog([0, 0, 0, 1], A_ub=rows, b_ub=rhs,
                     A_eq=[[1, 1, 1, 0]], b_eq=[0.5],
                     bounds=[(None, None)] * 3 + [(0, None)], method="highs")
    assert result.success, result.message
    assert abs(result.fun - 1 / 3) < 1e-10
    assert max(abs(x - 1 / 6) for x in result.x[:3]) < 1e-10

    equal_allocation = (Fraction(1, 6),) * 3
    exact_worst_excess = max(sum(equal_allocation[i] for i in s) - table[s]
                            for table in costs.values() for s in PROPER)
    assert exact_worst_excess == Fraction(1, 3)

    payload = {
        "purpose": "Early counterexample check for research-direction selection; novelty not claimed",
        "information": "Each binary marginal and the full aggregate distribution are known exactly",
        "loss": "absolute imbalance cost with both penalties equal to one",
        "worlds": {name: {"states": states, "probabilities": ["1/2", "1/2"]}
                   for name, states in worlds.items()},
        "same_marginals_and_aggregate": True,
        "coalition_costs": {name: {coalition_name(s): str(c) for s, c in table.items()}
                            for name, table in costs.items()},
        "Q1_core_allocation": [str(x) for x in allocation],
        "max_positive_excess_of_Q1_allocation": {
            name: str(max(Fraction(0), max(table.values()))) for name, table in excess.items()},
        "Q2_blocking_coalition": "23",
        "Q2_blocking_excess": "1",
        "grand_cost": "1/2",
        "ex_post_scaling": "1 in every listed realization at aggregate offer 3/2",
        "uniform_allocation": [str(x) for x in equal_allocation],
        "exact_common_least_core_epsilon": str(exact_worst_excess),
        "independent_lp_epsilon": result.fun,
        "scope": "The analytical extension to all compatible binary joint laws is in docs/research_directions.md",
        "scipy_version": scipy.__version__,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out = ROOT / "results/audit/coalition_information.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"worlds": len(worlds), "coalitions_per_world": len(COALITIONS),
                      "identical_observed_summaries": True,
                      "blocking_excess": "1", "least_core_epsilon": "1/3",
                      "independent_lp_epsilon": result.fun, "result": str(out)}))


if __name__ == "__main__":
    main()
