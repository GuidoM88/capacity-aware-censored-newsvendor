"""Check the sharp population gap against independent quantile and LP references."""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, exact_excess, forecast_rule
from censored_newsvendor.exclusion import ExclusionEnvelope


ROOT = Path(__file__).resolve().parents[1]


def check_instance(units, size):
    n = len(units)
    shares = [Fraction(x, sum(units)) for x in units]
    weights = np.array(shares, dtype=float)
    total = size + 2 * (n - 2)
    high = np.array([size] + [2] * (n - 2) + [0], dtype=float)
    low = np.array([0] * (n - 1) + [total - 1], dtype=float)
    truth = FiniteLaw(np.stack([low, high]) / total, [.5, .5])
    forecast = FiniteLaw(truth.states.sum(axis=1)[:, None] * weights, [.5, .5])
    rule = forecast_rule(forecast, np.ones(n))
    np.testing.assert_allclose(rule.weights, weights, rtol=0, atol=1e-12)
    np.testing.assert_allclose(forecast.states.sum(axis=1), truth.states.sum(axis=1), atol=1e-12)
    assert (truth.states.var(axis=0) > 0).all()
    loss = float(np.average(np.abs(truth.states.sum(axis=1) - rule.offer), weights=truth.probabilities))
    np.testing.assert_allclose(loss, 1 / (2 * total), rtol=0, atol=1e-12)
    integer = exact_excess(rule, truth)
    assert integer['excess'] == 0 and integer['worst_coalition']['excess'] < 0
    envelope = ExclusionEnvelope.population(rule, truth)
    # Under a symmetric two-state law, any median gives half the state difference as cost.
    singleton_costs = np.abs(truth.states[1] - truth.states[0]) / 2
    rho = min(1., float(np.min(weights * loss / singleton_costs)))
    levels = []
    for k in range(1, n):
        ceiling = sum(sorted(shares, reverse=True)[:n-k]) if k <= n - 2 else Fraction(0)
        ratio = ceiling - shares[-1] * Fraction(2 * k - 1, total - 1) if k <= n - 2 else Fraction(0)
        observed = envelope.level(k)['upper'] / loss
        np.testing.assert_allclose(observed, float(ratio), rtol=0, atol=1e-8)
        assert observed <= (1 - rho) * float(ceiling) + 1e-8
        levels.append({'k': k, 'exact_family_ratio': str(ratio), 'lp_ratio': observed,
                       'worst_case_supremum': str(ceiling)})
    return {'n': n, 'size': size, 'share_units': units, 'grand_loss': loss, 'maximum_loss': rule.loss_range,
            'minimum_charge_to_standalone_ratio': rho,
            'integer_excess': integer['excess'], 'coalitions_enumerated': integer['coalitions_checked'],
            'levels': levels}


def main():
    instances = []
    for n in (3, 6, 8):
        # Put the two largest shares on the large positive and negative state differences.
        for units in ([1] * n, [n, *range(1, n - 1), n - 1]):
            instances.extend(check_instance(units, size) for size in (2, 20, 200))
    inputs = [Path(__file__), ROOT / 'src/censored_newsvendor/coalition_audit.py',
              ROOT / 'src/censored_newsvendor/exclusion.py']
    payload = {'scope': 'Deterministic checks of a proved population construction. The denominator is expected grand loss L.',
               'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
               'instances': instances}
    target = ROOT / 'results/exclusion/sharp_gap.json'
    target.write_text(json.dumps(payload, indent=2, allow_nan=False) + '\n')
    print(f"Checked {len(instances)} two-state laws and {sum(len(r['levels']) for r in instances)} LP level values.")


if __name__ == '__main__':
    main()
