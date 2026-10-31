"""Upper bounds from excluding whole producers in a coalition audit."""

from itertools import combinations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

from .coalition_audit import FiniteLaw, loss, optimal_offer, proper_subset_support


class ExclusionEnvelope:
    """One finite-scenario population objective or validation confidence envelope."""

    def __init__(self, rule, law, endpoints, radius):
        self.rule = rule
        self.states = rule.validate(law.states)
        self.mass = law.probabilities
        self.endpoints = tuple(sorted(set(float(x) for x in endpoints)))
        self.radius = np.asarray(radius, dtype=float)
        self.n = len(rule.weights)

    @classmethod
    def population(cls, rule, law):
        y = rule.validate(law.states)
        grand = law.probabilities @ loss(rule.offer, y.sum(axis=1), rule.over, rule.under)
        return cls(rule, law, [grand], np.zeros(len(rule.weights)))

    @classmethod
    def validation(cls, rule, observations, delta):
        y = rule.validate(observations)
        if not 0 < delta < 1:
            raise ValueError("delta must be in (0,1)")
        samples, n = y.shape
        states, counts = np.unique(y, axis=0, return_counts=True)
        law = FiniteLaw(states, counts / samples)
        mean_loss = loss(rule.offer, y.sum(axis=1), rule.over, rule.under).mean()
        loss_radius = rule.loss_range * np.sqrt(np.log(4 / delta) / (2 * samples))
        endpoints = [max(0., mean_loss - loss_radius),
                     min(rule.loss_range, mean_loss + loss_radius)]
        cost_eps = np.sqrt(np.log(4 * (2 ** n - 2) / delta) / (2 * samples))
        radius = max(rule.over, rule.under) * rule.rated * cost_eps
        return cls(rule, law, endpoints, radius)

    def integer_value(self, membership):
        _, cost = optimal_offer(self.states @ membership, self.mass,
                                self.rule.over, self.rule.under)
        weight = float(self.rule.weights @ membership)
        return max(self.endpoints[0] * weight, self.endpoints[-1] * weight) - max(
            0., cost - float(self.radius @ membership))

    def _face(self, excluded, endpoint):
        free = [i for i in range(self.n) if i not in excluded]
        s, f = len(self.mass), len(free)
        root = len(excluded) == 0
        # Variables are discounted scenario scores, discount, positive parts,
        # and a threshold for the cardinality constraint at the root.
        width = s + 1 + f + int(root)
        objective = np.zeros(width)
        objective[s + 1:s + 1 + f] = 1
        if root:
            objective[-1] = self.n - 1
        rows = np.zeros((f + 2 * s, width))
        rows[:f, :s] = -self.states[:, free].T * self.mass
        rows[:f, s] = self.radius[free]
        rows[:f, s + 1:s + 1 + f] = -np.eye(f)
        if root:
            rows[:f, -1] = -1
        rows[f:f + s, :s] = np.eye(s)
        rows[f:f + s, s] = -self.rule.over
        rows[f + s:, :s] = -np.eye(s)
        rows[f + s:, s] = -self.rule.under
        values = endpoint * self.rule.weights[free]
        equality = np.zeros((1, width))
        equality[0, :s] = self.mass
        result = linprog(
            objective, A_ub=rows, b_ub=np.r_[-values, np.zeros(2 * s)],
            A_eq=equality, b_eq=[0],
            bounds=[(None, None)] * s + [(0, 1)] + [(0, None)] * (f + int(root)),
            method="highs")
        if not result.success:
            raise RuntimeError(result.message)

        # Recompute an upper bound even if the returned mean-zero equation
        # has a rounding residual. Weak duality supplies the capacity correction.
        discount = float(np.clip(result.x[s], 0., 1.))
        scores = np.clip(result.x[:s], -self.rule.under * discount,
                         self.rule.over * discount)
        moments = self.states[:, free].T @ (self.mass * scores)
        drift = max(0., float(self.mass @ scores))
        residual = (values + discount * self.radius[free] - moments
                    + self.rule.rated[free] * drift)
        upper = (proper_subset_support(residual) if root
                 else float(np.maximum(residual, 0).sum()))
        fractional = np.zeros(self.n)
        fractional[free] = np.clip(-result.ineqlin.marginals[:f], 0., 1.)
        rounded = (fractional >= .5).astype(float)
        if rounded.sum() == self.n:
            rounded[np.argmin(fractional)] = 0
        return upper, max(0., self.integer_value(rounded))

    def level(self, k):
        if not isinstance(k, int) or not 0 <= k < self.n:
            raise ValueError("The exclusion level must be an integer in [0,n-1]")
        witness, lp_calls, direct_checks = 0., 0, 0
        for number in range(1, k):
            for absent in combinations(range(self.n), number):
                membership = np.ones(self.n)
                membership[list(absent)] = 0
                witness = max(witness, self.integer_value(membership))
                direct_checks += 1
        upper = witness
        for absent in combinations(range(self.n), k):
            for endpoint in self.endpoints:
                face_value, feasible = self._face(absent, endpoint)
                upper = max(upper, face_value)
                witness = max(witness, feasible)
                lp_calls += 1
        return {"upper": float(upper), "integer_witness": float(witness),
                "work_gap": max(0., float(upper - witness)),
                "lp_calls": lp_calls, "large_coalitions_checked": direct_checks,
                "rounding_checks": lp_calls}

    def binary_reference(self):
        """Independent primal MILP for the exact integer envelope."""
        s, n = self.states.shape
        # Variables are memberships, offer, surplus, shortfall and excess.
        width = n + 2 + 2 * s
        scenario = np.zeros((s, width))
        scenario[:, :n] = -self.states
        scenario[:, n] = 1
        scenario[:, n + 1:n + 1 + s] = np.eye(s)
        scenario[:, n + 1 + s:-1] = -np.eye(s)
        objective = np.zeros(width)
        objective[-1] = -1
        lower = np.zeros(width)
        lower[-1] = -np.inf
        upper = np.full(width, np.inf)
        upper[:n] = 1
        upper[n] = self.rule.rated.sum()
        best = 0.
        for endpoint in self.endpoints:
            rows = np.zeros((3, width))
            rows[0, :n] = 1
            rows[1:, :n] = -endpoint * self.rule.weights
            rows[1:, -1] = 1
            rows[2, :n] -= self.radius
            rows[2, n + 1:n + 1 + s] = self.rule.over * self.mass
            rows[2, n + 1 + s:-1] = self.rule.under * self.mass
            result = milp(objective, integrality=np.r_[np.ones(n), np.zeros(width - n)],
                          bounds=Bounds(lower, upper),
                          constraints=[LinearConstraint(scenario, 0, 0),
                                       LinearConstraint(rows, -np.inf, [n - 1, 0, 0])],
                          options={"mip_rel_gap": 0.})
            if not result.success:
                raise RuntimeError(result.message)
            best = max(best, -float(result.fun))
        return best
