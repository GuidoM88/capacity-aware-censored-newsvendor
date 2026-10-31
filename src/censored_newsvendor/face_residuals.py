"""Statistical audit of a fixed cost-sharing rule with separately fitted dual prices."""

from dataclasses import dataclass

import numpy as np

from .coalition_audit import FiniteLaw, loss, optimal_offer, proper_subset_support


@dataclass(frozen=True)
class Price:
    offer: float
    tie: float


def empirical_law(observations):
    y = np.asarray(observations, dtype=float)
    if y.ndim != 2 or len(y) == 0:
        raise ValueError("A sample must contain joint production vectors")
    return FiniteLaw(y, np.full(len(y), 1 / len(y)))


def _groups(n, grand):
    indices = np.arange(n)
    return [indices] if grand else [indices[indices != i] for i in indices]


def fit_prices(rule, pilot, *, grand=False):
    """Fit scalar quantiles and atom scores using only the supplied pilot law."""
    y, p = rule.validate(pilot.states), pilot.probabilities
    prices = []
    for indices in _groups(y.shape[1], grand):
        totals = y[:, indices].sum(axis=1)
        q, _ = optimal_offer(totals, p, rule.over, rule.under)
        atom = p[totals == q].sum()
        tie = ((rule.under * p[totals < q].sum() - rule.over * p[totals > q].sum()) / atom
               if atom > 0 else 0.)
        prices.append(Price(q, float(np.clip(tie, -rule.under, rule.over))))
    return tuple(prices)


def _mean_interval(values, p, minimum, maximum, observations, tail):
    """Either an exact population moment or a clipped finite-sample interval."""
    values = np.asarray(values)
    weights = p if values.ndim == 1 else p[:, None]
    mean = np.sum(weights * values, axis=0)
    if observations is None:
        return mean, mean
    width = np.asarray(maximum) - minimum
    m = observations
    variance = (m / (m - 1)) * np.sum(weights * (values - mean) ** 2, axis=0)
    # tail covers one used direction of the mean. Split between inequalities.
    h = width * np.sqrt(np.log(2 / tail) / (2 * m))
    log_term = np.log(4 / tail)
    eb = np.sqrt(2 * variance * log_term / m) + 7 * width * log_term / (3 * (m - 1))
    radius = np.minimum(h, eb)
    return np.maximum(minimum, mean - radius), np.minimum(maximum, mean + radius)


def _audit(rule, prices, law, m, delta, grand):
    y, p = rule.validate(law.states), law.probabilities
    n = y.shape[1]
    groups = _groups(n, grand)
    if len(prices) != len(groups):
        raise ValueError("Each selected group needs one frozen price")
    if not 0 < delta < 1 or (m is not None and m < 2):
        raise ValueError("Use delta in (0,1) and at least two validation observations")
    count = (2 * (n + 1) + 1) if grand else (2 * n * n + n + 1)
    tail = delta / count
    grand_loss = loss(rule.offer, y.sum(axis=1), rule.over, rule.under)
    _, lhi = _mean_interval(grand_loss, p, 0., rule.loss_range, m, tail)
    cap = proper_subset_support(rule.weights) * float(lhi)
    faces = []
    for indices, price in zip(groups, prices):
        r = rule.rated[indices]
        w = rule.weights[indices]
        capacity = float(r.sum())
        if (not 0 <= price.offer <= capacity or not -rule.under <= price.tie <= rule.over):
            raise ValueError("Invalid offer or dual value at the atom")
        outputs = y[:, indices]
        total = outputs.sum(axis=1)
        score = np.where(total > price.offer, rule.over,
                         np.where(total < price.offer, -rule.under, price.tie))
        mu_lo, mu_hi = _mean_interval(score, p, -rule.under, rule.over, m, tail)
        x = grand_loss[:, None] * w - score[:, None] * outputs
        minimum = np.minimum(0., w * rule.loss_range) - rule.over * r
        maximum = np.maximum(0., w * rule.loss_range) + rule.under * r
        xlo, xhi = _mean_interval(x, p, minimum, maximum, m, tail)
        vlo = xlo + r * max(0., mu_lo)
        vhi = xhi + r * max(0., mu_hi)
        pos = float(np.maximum(0., vhi).sum())
        face = {"upper": proper_subset_support(vhi) if grand else pos,
                "mu_interval": [float(mu_lo), float(mu_hi)]}
        if not grand:
            # The sum of residuals differs from the face witness by drift alone.
            drift = max((capacity - price.offer) * max(0., mu_hi),
                        price.offer * max(0., -mu_lo))
            mixed = min(pos, float(np.maximum(0., -vlo).sum()) + drift)
            weight = float(w.sum())
            face_loss = loss(price.offer, total, rule.over, rule.under)
            face_range = max(rule.under * price.offer, rule.over * (capacity - price.offer))
            witness = weight * grand_loss - face_loss
            witness_lo, _ = _mean_interval(witness, p, min(0., weight * rule.loss_range) - face_range,
                                           max(0., weight * rule.loss_range), m, tail)
            face.update({"mixed_upper": float(mixed), "drift_upper": float(drift),
                         "witness_lower": max(0., float(witness_lo))})
        faces.append(face)
    upper = min(cap, max(face["upper"] for face in faces))
    lower = max((face.get("witness_lower", 0.) for face in faces))
    fallback = lower > upper + 1e-9
    if fallback:
        # Empty numerical/statistical interval. The deterministic range is always safe.
        lower, upper = 0., proper_subset_support(rule.weights) * rule.loss_range
    upper = max(lower, upper)
    result = {"lower": float(lower), "upper": float(upper), "fallback": bool(fallback),
              "one_sided_events": count, "faces": faces}
    if not grand:
        result["gap_upper"] = (float(upper) if fallback else
                               float(min(upper - lower, max(f["mixed_upper"] for f in faces))))
    return result


def residual_certificate(rule, prices, observations, delta=.05, *, grand=False):
    """Use iid observations independent of the fitted prices and implemented rule."""
    law = empirical_law(observations)
    return _audit(rule, prices, law, len(law.states), delta, grand)


def population_diagnostic(rule, prices, law, *, grand=False):
    """Evaluate the structural limitations of frozen prices with population access."""
    return _audit(rule, prices, law, None, .05, grand)

