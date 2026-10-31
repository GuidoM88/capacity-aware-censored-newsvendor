"""Check the separately derived worst-case construction for fixed exclusion depth."""

import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, exact_excess, forecast_rule
from censored_newsvendor.exclusion import ExclusionEnvelope


ROOT = Path(__file__).resolve().parents[1]


def extend(base, depth):
    noise = product([-1, 1], repeat=depth - 1)
    extras = [[.5 + sign / (20 * depth) for sign in outcome] for outcome in noise]
    states = [list(row) + added for row in base for added in extras]
    return FiniteLaw(states, np.full(len(states), 1 / len(states)))


def main():
    results = []
    for k in range(1, 6):
        forecast = extend([[.25, .1, .35], [.55, .2, .25]], k)
        truth = extend([[0., .6, .1], [1., 0., 0.]], k)
        n = k + 2
        rule = forecast_rule(forecast, np.ones(n))
        np.testing.assert_allclose(rule.weights, [1., 1 / 3, -1 / 3] + [0.] * (k - 1), atol=1e-12)
        np.testing.assert_allclose(np.sort(forecast.states.sum(axis=1)),
                                   np.sort(truth.states.sum(axis=1)), atol=1e-12)
        assert np.all(truth.states.var(axis=0) > 0)
        envelope = ExclusionEnvelope.population(rule, truth)
        exact = exact_excess(rule, truth)["excess"]
        candidate = envelope.level(k)["upper"]
        terminal = envelope.level(n - 1)["upper"]
        assert abs(exact) < 1e-8 and abs(candidate - 7 / 50) < 1e-8 and abs(terminal) < 1e-8
        results.append({"k": k, "n": n, "integer_excess": exact, "level_k": candidate,
                        "terminal_level": terminal, "true_support_size": len(truth.states),
                        "offer": rule.offer, "weights": rule.weights.tolist()})
    out = ROOT / "results/exclusion/obstruction.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    modules = [Path(__file__), ROOT / "src/censored_newsvendor/exclusion.py"]
    payload = {"scope": "Follow-up construction derived after the fixed comparison, 2026-10-31",
               "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in modules}, "instances": results}
    out.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    print(json.dumps(results))


if __name__ == "__main__":
    main()
