"""Research baselines for auditing a frozen cooperative imbalance-cost rule.

Finite-sample guarantees require iid validation data independent of the rule
and its score. Population LPs below are diagnostic oracles, not estimators.
See docs/coalition_certificate.md for proofs and the limits of each bound.
"""

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


@dataclass(frozen=True)
class FiniteLaw:
    states: np.ndarray
    probabilities: np.ndarray

    def __post_init__(self):
        y = np.array(self.states, dtype=float, copy=True)
        p = np.array(self.probabilities, dtype=float, copy=True)
        if (y.ndim != 2 or y.shape[0] == 0 or y.shape[1] < 2
                or p.shape != (len(y),) or not np.isfinite(y).all()
                or not np.isfinite(p).all() or (y < 0).any() or (p < 0).any()
                or not np.isclose(p.sum(), 1, atol=1e-12, rtol=1e-12)):
            raise ValueError("A finite law needs nonnegative states and probability mass one")
        p /= p.sum()
        y.setflags(write=False)
        p.setflags(write=False)
        object.__setattr__(self, "states", y)
        object.__setattr__(self, "probabilities", p)


def loss(q, totals, over=1.0, under=1.0):
    """over penalizes generation above the offer; under penalizes a shortfall."""
    totals = np.asarray(totals)
    return over * np.maximum(totals - q, 0) + under * np.maximum(q - totals, 0)


def optimal_offer(totals, probabilities, over=1.0, under=1.0):
    if over <= 0 or under <= 0:
        raise ValueError("Penalties must be positive")
    values, indices = np.unique(totals, return_inverse=True)
    masses = np.bincount(indices, weights=probabilities, minlength=len(values))
    positive = masses > 0
    values, masses = values[positive], masses[positive]
    cumulative = np.cumsum(masses)
    tau = over / (over + under)
    k = min(int(np.searchsorted(cumulative, tau, side="left")), len(values) - 1)
    q = values[k]
    if k + 1 < len(values) and abs(cumulative[k] - tau) <= 1e-12:
        q = (values[k] + values[k + 1]) / 2
    return float(q), float(np.dot(probabilities, loss(q, totals, over, under)))


@dataclass(frozen=True)
class FrozenRule:
    offer: float
    weights: np.ndarray
    rated: np.ndarray
    over: float = 1.0
    under: float = 1.0
    tie_score: float = 0.0

    def __post_init__(self):
        w = np.array(self.weights, dtype=float, copy=True)
        r = np.array(self.rated, dtype=float, copy=True)
        scalars = [self.offer, self.over, self.under, self.tie_score]
        if (w.ndim != 1 or len(w) < 2 or r.shape != w.shape
                or not np.isfinite(w).all() or not np.isfinite(r).all()
                or not np.isfinite(scalars).all() or (r < 0).any()
                or not np.isclose(w.sum(), 1, atol=1e-10, rtol=1e-10)
                or self.over <= 0 or self.under <= 0
                or not 0 <= self.offer <= r.sum()
                or not -self.under <= self.tie_score <= self.over):
            raise ValueError("Invalid frozen rule, capacities, penalties or shares")
        w.setflags(write=False)
        r.setflags(write=False)
        object.__setattr__(self, "weights", w)
        object.__setattr__(self, "rated", r)

    def validate(self, observations):
        y = np.asarray(observations, dtype=float)
        if (y.ndim != 2 or len(y) == 0 or y.shape[1] != len(self.weights)
                or not np.isfinite(y).all() or (y < 0).any()
                or (y > self.rated + 1e-12).any()):
            raise ValueError("Observations must lie within the declared production bounds")
        return y

    def score(self, observations):
        totals = self.validate(observations).sum(axis=1)
        values = np.where(totals > self.offer, self.over, -self.under)
        at_offer = np.isclose(totals, self.offer, atol=1e-12, rtol=1e-12)
        return np.where(at_offer, self.tie_score, values)

    @property
    def loss_range(self):
        return float(max(self.under * self.offer,
                         self.over * (self.rated.sum() - self.offer)))


def forecast_rule(law, rated, over=1.0, under=1.0):
    totals, p = law.states.sum(axis=1), law.probabilities
    q, cost = optimal_offer(totals, p, over, under)
    if cost <= 1e-12:
        raise ValueError("Forecast cost is zero or too small for proportional division")
    at_offer = np.isclose(totals, q, atol=1e-12, rtol=1e-12)
    below = (totals < q) & ~at_offer
    above = (totals > q) & ~at_offer
    tie = ((under * p[below].sum() - over * p[above].sum()) / p[at_offer].sum()
           if at_offer.any() else 0.0)
    tie = float(np.clip(tie, -under, over))
    score = np.where(at_offer, tie, np.where(totals > q, over, -under))
    allocation = law.states.T @ (p * score)
    rule = FrozenRule(q, allocation / cost, rated, over, under, tie)
    rule.validate(law.states)
    return rule


def proper_subset_support(values):
    """max(0, max over nonempty proper subsets of their coordinate sum)."""
    positive = np.maximum(np.asarray(values, dtype=float), 0)
    return float(positive.sum() - positive.min())


def population_bound(rule, law):
    y, p = rule.validate(law.states), law.probabilities
    score = rule.score(y)
    total_cost = float(p @ loss(rule.offer, y.sum(axis=1), rule.over, rule.under))
    mu = float(p @ score)
    moments = y.T @ (p * score)
    d = rule.weights * total_cost - moments + rule.rated * max(mu, 0)
    raw = proper_subset_support(d)
    cap = proper_subset_support(rule.weights) * total_cost
    return {"bound": min(raw, cap), "raw_dual_bound": raw,
            "nonnegative_cost_cap": cap, "grand_cost": total_cost,
            "score_mean": mu, "score_moments": moments.tolist()}


def coalition_table(rule, law):
    y, p = rule.validate(law.states), law.probabilities
    total_cost = float(p @ loss(rule.offer, y.sum(axis=1), rule.over, rule.under))
    rows = []
    for size in range(1, y.shape[1]):
        for indices in combinations(range(y.shape[1]), size):
            q, cost = optimal_offer(y[:, indices].sum(axis=1), p, rule.over, rule.under)
            share = float(rule.weights[list(indices)].sum())
            rows.append({"coalition": [i + 1 for i in indices], "offer": q,
                         "cost": cost, "weight": share,
                         "excess": share * total_cost - cost})
    return rows


def exact_excess(rule, law):
    rows = coalition_table(rule, law)
    worst = max(rows, key=lambda row: row["excess"])
    return {"excess": max(0.0, worst["excess"]), "worst_coalition": worst,
            "coalitions_checked": len(rows)}


def finite_certificate(rule, observations, delta=0.05):
    """O(m*n) bound. The score/rule must be fixed independently of these data."""
    y = rule.validate(observations)
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0,1)")
    m, n = y.shape
    eps = float(np.sqrt(np.log((n + 3) / delta) / (2 * m)))
    score = rule.score(y)
    empirical_loss = float(loss(rule.offer, y.sum(axis=1), rule.over, rule.under).mean())
    lo = max(0.0, empirical_loss - rule.loss_range * eps)
    hi = min(rule.loss_range, empirical_loss + rule.loss_range * eps)
    width = rule.over + rule.under
    mu_upper = min(rule.over, float(score.mean()) + width * eps)
    moment_lower = np.maximum(-rule.under * rule.rated,
                              (y * score[:, None]).mean(axis=0) - width * rule.rated * eps)
    correction = -moment_lower + rule.rated * max(mu_upper, 0)
    # Use one common loss endpoint, rather than separately choosing signs per player.
    raw = max(proper_subset_support(rule.weights * endpoint + correction)
              for endpoint in (lo, hi))
    upper = min(raw, proper_subset_support(rule.weights) * hi)
    return {"upper": upper, "delta": delta, "samples": m,
            "loss_interval": [lo, hi], "score_mean_upper": mu_upper,
            "moment_lower": moment_lower.tolist(), "hoeffding_epsilon": eps}


def enumeration_certificate(rule, observations, delta=0.05):
    """Exponential coalition enumeration with simultaneous DKW cost bounds."""
    y = rule.validate(observations)
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0,1)")
    m, n = y.shape
    count = 2 ** n - 2
    eps_cost = float(np.sqrt(np.log(4 * count / delta) / (2 * m)))
    eps_loss = float(np.sqrt(np.log(4 / delta) / (2 * m)))
    empirical_loss = float(loss(rule.offer, y.sum(axis=1), rule.over, rule.under).mean())
    lo = max(0.0, empirical_loss - rule.loss_range * eps_loss)
    hi = min(rule.loss_range, empirical_loss + rule.loss_range * eps_loss)
    table = coalition_table(rule, FiniteLaw(y, np.full(m, 1 / m)))
    upper = 0.0
    for row in table:
        indices = np.asarray(row["coalition"]) - 1
        radius = max(rule.over, rule.under) * rule.rated[indices].sum() * eps_cost
        cost_lower = max(0.0, row["cost"] - radius)
        worst_loss = hi if row["weight"] >= 0 else lo
        upper = max(upper, row["weight"] * worst_loss - cost_lower)
    return {"upper": float(upper), "delta": delta, "samples": m,
            "coalitions_checked": count, "dkw_epsilon": eps_cost}


def coalition_program(rule, law, integral=False):
    """Independent primal LP/MILP with fractional/binary coalition membership."""
    y, p = rule.validate(law.states), law.probabilities
    s, n = y.shape
    grand = float(p @ loss(rule.offer, y.sum(axis=1), rule.over, rule.under))
    objective = np.r_[-rule.weights * grand, 0, rule.over * p, rule.under * p]
    equality = np.zeros((s, n + 1 + 2 * s))
    equality[:, :n] = -y
    equality[:, n] = 1
    equality[:, n + 1:n + 1 + s] = np.eye(s)
    equality[:, n + 1 + s:] = -np.eye(s)
    cardinality = np.r_[np.ones(n), np.zeros(1 + 2 * s)][None, :]
    bounds = [(0, 1)] * n + [(0, float(rule.rated.sum()))] + [(0, None)] * (2 * s)
    if integral:
        result = milp(objective, integrality=np.r_[np.ones(n), np.zeros(1 + 2 * s)],
                      bounds=Bounds(np.zeros(len(objective)),
                                    [hi if hi is not None else np.inf for _, hi in bounds]),
                      constraints=[LinearConstraint(equality, 0, 0),
                                   LinearConstraint(cardinality, -np.inf, n - 1)],
                      options={"mip_rel_gap": 0.0})
    else:
        result = linprog(objective, A_ub=cardinality, b_ub=[n - 1],
                         A_eq=equality, b_eq=np.zeros(s), bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return {"bound": max(0.0, -float(result.fun)),
            "membership": result.x[:n].tolist(), "offer": float(result.x[n])}


def best_common_dual(rule, law):
    """Population diagnostic; polynomial in the explicitly supplied support size."""
    y, p = rule.validate(law.states), law.probabilities
    s, n = y.shape
    grand = float(p @ loss(rule.offer, y.sum(axis=1), rule.over, rule.under))
    allocation = rule.weights * grand
    objective = np.r_[np.zeros(s), np.ones(n), n - 1]
    rows = np.c_[-y.T * p, -np.eye(n), -np.ones(n)]
    equality = np.r_[p, np.zeros(n + 1)][None, :]
    result = linprog(objective, A_ub=rows, b_ub=-allocation,
                     A_eq=equality, b_eq=[0],
                     bounds=[(-rule.under, rule.over)] * s + [(0, None)] * (n + 1),
                     method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return {"bound": max(0.0, float(result.fun)),
            "score_mean": float(p @ result.x[:s]), "score": result.x[:s].tolist()}
