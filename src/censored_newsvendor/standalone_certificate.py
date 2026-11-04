"""Standalone-cost coverage and a finite-data bound on the exclusion gap.

The rule and pilot must be independent of iid validation observations. The
ratio test uses an intersection-union test followed by a fixed sequence;
individual diagnostic lower bounds are NOT simultaneous confidence intervals.
See docs/standalone_certificate.md for the proof and the baseline mappings.
"""

from dataclasses import dataclass

import numpy as np

from .coalition_audit import FiniteLaw, loss, optimal_offer
from .exclusion import ExclusionEnvelope
from .face_residuals import _mean_interval


THRESHOLDS = tuple(j / 20 for j in range(1, 21))


@dataclass(frozen=True)
class StandaloneAudit:
    offers: tuple[float, ...]
    witness_indices: tuple[int, ...]
    witness_offer: float


def _sample(rule, observations):
    if (rule.weights <= 0).any():
        raise ValueError("The standalone bound requires strictly positive shares")
    y = rule.validate(observations)
    if len(y) < 2:
        raise ValueError("Use at least two observations")
    return y


def _validate_audit(rule, audit):
    offers = np.asarray(audit.offers, dtype=float)
    indices = audit.witness_indices
    if (offers.shape != rule.rated.shape or not np.isfinite(offers).all()
            or (offers < 0).any() or (offers > rule.rated).any()
            or len(set(indices)) != len(indices) or len(indices) >= len(offers)
            or any(not isinstance(i, (int, np.integer)) or not 0 <= i < len(offers)
                   for i in indices)
            or not np.isfinite(audit.witness_offer)
            or not 0 <= audit.witness_offer <= rule.rated[list(indices)].sum()):
        raise ValueError("Invalid pilot offers or feasible coalition witness")


def _interval(values, minimum, maximum, tail):
    m = len(values)
    return _mean_interval(values, np.full(m, 1 / m), minimum, maximum, m, tail)


def _grand(rule, y, tail):
    values = loss(rule.offer, y.sum(axis=1), rule.over, rule.under)
    lo, hi = _interval(values, 0., rule.loss_range, tail / 2)
    return values, float(lo), float(hi)


def fit_standalone_audit(rule, pilot):
    """Fit individual offers and choose one leave-one-out witness on the pilot."""
    y = _sample(rule, pilot)
    p = np.full(len(y), 1 / len(y))
    offers = tuple(optimal_offer(column, p, rule.over, rule.under)[0] for column in y.T)
    totals = y.sum(axis=1)
    grand = float(p @ loss(rule.offer, totals, rule.over, rule.under))
    best, indices, offer = 0., (), 0.
    for j in range(y.shape[1]):
        q, cost = optimal_offer(totals - y[:, j], p, rule.over, rule.under)
        candidate = (1 - rule.weights[j]) * grand - cost
        if candidate > best:
            best, indices, offer = candidate, tuple(i for i in range(y.shape[1]) if i != j), q
    return StandaloneAudit(offers, indices, offer)


def _witness_values(rule, audit, y, grand):
    indices = list(audit.witness_indices)
    weight = float(rule.weights[indices].sum())
    capacity = float(rule.rated[indices].sum())
    q = audit.witness_offer
    cost_range = max(rule.under * q, rule.over * (capacity - q))
    values = weight * grand - loss(q, y[:, indices].sum(axis=1), rule.over, rule.under)
    return values, weight, cost_range


def _witness_lower(rule, audit, validation, tail):
    if not audit.witness_indices:
        return 0.
    grand = loss(rule.offer, validation.sum(axis=1), rule.over, rule.under)
    values, weight, cost_range = _witness_values(rule, audit, validation, grand)
    lower, _ = _interval(values, -cost_range, weight * rule.loss_range, tail)
    return max(0., float(lower))


def _cost_caps(rule):
    return rule.over * rule.under / (rule.over + rule.under) * rule.rated


def _ratio_from_cost_upper(rule, grand_lower, costs):
    positive = np.asarray(costs) > 0
    if not positive.any():
        return 1.
    return float(np.clip(np.min(rule.weights[positive] * grand_lower / costs[positive]), 0., 1.))


def _finish(rule, rho, lower, upper, witness):
    n = len(rule.weights)
    shares = np.cumsum(np.sort(rule.weights)[::-1])
    fallback = witness > shares[n - 2] * upper + 1e-9
    if fallback:
        rho, lower, upper, witness = 0., 0., rule.loss_range, 0.
    gaps = [(1 - rho) * max(0., shares[n - k - 1] * upper - witness)
            for k in range(1, n - 1)] + [0.]
    return {"rho_lower": float(rho), "grand_interval": [float(lower), float(upper)],
            "witness_lower": float(witness), "gap_by_depth": [float(g) for g in gaps],
            "gap_upper": float(gaps[0]), "half_certified": bool(rho >= .5),
            "fallback": bool(fallback)}


def standalone_certificate(rule, audit, validation, delta=.05, *, bonferroni=False):
    """Lower confidence bound on rho and simultaneous gap bounds at every depth.

    Stop at the FIRST failed threshold. Taking later rejections after a failure
    would invalidate the fixed-sequence error guarantee. No dimension or grid
    penalty is necessary for the reported global lower rho bound.
    """
    y = _sample(rule, validation)
    _validate_audit(rule, audit)
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0,1)")
    grand, lower, upper = _grand(rule, y, delta / 3)
    individual = loss(np.asarray(audit.offers), y, rule.over, rule.under)
    ranges = np.maximum(rule.under * np.asarray(audit.offers),
                        rule.over * (rule.rated - audit.offers))
    tail = delta / 3
    if bonferroni:
        tail /= len(rule.weights) * len(THRESHOLDS)
    rho_grid, checked = 0., []
    for t in THRESHOLDS:
        values = grand[:, None] * rule.weights - t * individual
        lo, _ = _interval(values, -t * ranges, rule.weights * rule.loss_range, tail)
        passed = bool((lo > 0).all())
        checked.append({"threshold": t, "minimum_lower": float(lo.min()), "passed": passed})
        if not passed:
            break
        rho_grid = t
    rho_capacity = _ratio_from_cost_upper(rule, lower, _cost_caps(rule))
    witness = _witness_lower(rule, audit, y, delta / 3)
    result = _finish(rule, max(rho_grid, rho_capacity), lower, upper, witness)
    result.update({"rho_grid": rho_grid, "rho_capacity": rho_capacity,
                   "threshold_checks": checked, "scalar_tail": tail})
    return result


def marginal_certificate(rule, audit, pilot, validation, delta=.05, *, capacity_only=False):
    """Full-budget marginal DKW or deterministic-cap comparator.

    Grand cost and marginal optimized costs use all 2M samples. Only the
    independent validation evaluates the pilot-selected feasible witness.
    """
    p, v = _sample(rule, pilot), _sample(rule, validation)
    _validate_audit(rule, audit)
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0,1)")
    y = np.concatenate([p, v])
    _, lower, upper = _grand(rule, y, delta / 3)
    caps = _cost_caps(rule)
    costs = caps.copy()
    if not capacity_only:
        mass = np.full(len(y), 1 / len(y))
        estimated = np.array([optimal_offer(column, mass, rule.over, rule.under)[1]
                              for column in y.T])
        epsilon = np.sqrt(np.log(2 * len(rule.weights) / (delta / 3)) / (2 * len(y)))
        costs = np.minimum(caps, estimated + max(rule.over, rule.under) * rule.rated * epsilon)
    witness = _witness_lower(rule, audit, v, delta / 3)
    result = _finish(rule, _ratio_from_cost_upper(rule, lower, costs), lower, upper, witness)
    result.update({"cost_upper": costs.tolist(),
                   "rho_capacity": _ratio_from_cost_upper(rule, lower, caps)})
    return result


def block_gap_certificate(rule, audit, validation, delta=.05, *, block_size=64):
    """Bounded-mean calibration of the standard paired SAA block gap baseline."""
    y = _sample(rule, validation)
    _validate_audit(rule, audit)
    if not 0 < delta < 1 or not isinstance(block_size, int) or block_size < 2:
        raise ValueError("Use delta in (0,1) and an integer block size at least two")
    if len(y) % block_size or len(y) // block_size < 2:
        raise ValueError("Use at least two complete validation blocks")
    s1 = 1 - float(rule.weights.min())
    block_values, lp_calls = [], 0
    grand = loss(rule.offer, y.sum(axis=1), rule.over, rule.under)
    witness, weight, cost_range = _witness_values(rule, audit, y, grand)
    width = max(0., (s1 - weight) * rule.loss_range) + cost_range
    for start in range(0, len(y), block_size):
        stop = start + block_size
        states, counts = np.unique(y[start:stop], axis=0, return_counts=True)
        empirical = FiniteLaw(states, counts / block_size)
        level = ExclusionEnvelope.population(rule, empirical).level(1)
        d1_upper = min(level["upper"], s1 * grand[start:stop].mean())
        gap = max(0., d1_upper - float(witness[start:stop].mean()))
        if gap > width + 1e-8:
            raise RuntimeError("Block statistic exceeds its deterministic bound")
        block_values.append(min(gap, width))
        lp_calls += level["lp_calls"]
    _, hi = _interval(np.array(block_values), 0., width, delta / 2)
    _, lhi = _interval(grand, 0., rule.loss_range, delta / 2)
    return {"gap_upper": float(min(hi, s1 * lhi)), "block_values": block_values,
            "block_range": width, "block_size": block_size, "lp_calls": lp_calls,
            "grand_upper": float(lhi), "fallback": False}
