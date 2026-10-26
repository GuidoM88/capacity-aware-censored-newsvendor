"""Exact piecewise-uniform marginals, including an upper-end censoring atom."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PiecewiseUniform:
    """Positive density on adjacent bins starting at zero, plus an upper atom.

    ``masses[j]`` is the unconditional probability on the open interval
    ``(knots[j], knots[j + 1])``. The remaining explicit ``atom_mass`` is
    concentrated at the final knot. This restricted family has a continuous
    quantile function, which the allocation solver requires.
    """

    knots: tuple[float, ...]
    masses: tuple[float, ...]
    atom_mass: float = 0.0

    def __post_init__(self):
        object.__setattr__(self, "knots", tuple(float(x) for x in self.knots))
        object.__setattr__(self, "masses", tuple(float(x) for x in self.masses))
        k, m = np.asarray(self.knots), np.asarray(self.masses)
        if len(k) < 2 or len(m) != len(k) - 1:
            raise ValueError("There must be one mass per interval and at least two knots.")
        if not np.all(np.isfinite(k)) or k[0] != 0 or np.any(np.diff(k) <= 0):
            raise ValueError("Knots must be finite, start at zero, and strictly increase.")
        if not np.all(np.isfinite(m)) or np.any(m <= 0):
            raise ValueError("Every interval must have strictly positive finite mass.")
        if not np.isfinite(self.atom_mass) or self.atom_mass < 0:
            raise ValueError("The upper atom must have finite nonnegative mass.")
        if not np.isclose(m.sum() + self.atom_mass, 1, rtol=0, atol=1e-12):
            raise ValueError("Interval masses and the upper atom must sum to one.")

    @property
    def upper(self):
        return self.knots[-1]

    @property
    def mean(self):
        k = np.asarray(self.knots)
        return float(np.dot(self.masses, (k[:-1] + k[1:]) / 2) + self.atom_mass * k[-1])

    def cdf(self, x):
        """Right-continuous distribution function, evaluated on scalars or arrays."""
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        for a, z, mass in zip(self.knots[:-1], self.knots[1:], self.masses):
            result += mass * np.clip((x - a) / (z - a), 0, 1)
        result += self.atom_mass * (x >= self.upper)
        return np.clip(result, 0, 1)

    def cdf_left(self, x):
        """Left limit; needed for optimality checks at a censoring atom."""
        x = np.asarray(x, dtype=float)
        return self.cdf(x) - self.atom_mass * (x == self.upper)

    def ppf(self, probability):
        """Generalized inverse, with the convention Q(0) = 0."""
        probability = np.asarray(probability, dtype=float)
        if not np.all(np.isfinite(probability)) or np.any((probability < 0) | (probability > 1)):
            raise ValueError("Probabilities must be finite and lie in [0, 1].")
        cumulative = np.r_[0.0, np.cumsum(self.masses)]
        return np.interp(probability, cumulative, self.knots, right=self.upper)

    def expected_overage(self, quantity):
        """Compute E[(q - D)+] by integrating each uniform component exactly."""
        q = np.asarray(quantity, dtype=float)
        value = np.zeros_like(q)
        for a, z, mass in zip(self.knots[:-1], self.knots[1:], self.masses):
            inside = np.clip(q - a, 0, z - a)
            value += mass * (inside**2 / (2 * (z - a)) + np.maximum(q - z, 0))
        return value + self.atom_mass * np.maximum(q - self.upper, 0)

    def expected_cost(self, quantity, underage=4.0, overage=1.0):
        """Expected underage/overage loss, including any upper-end atom."""
        if not np.isfinite(underage) or not np.isfinite(overage) or min(underage, overage) <= 0:
            raise ValueError("Underage and overage costs must be positive and finite.")
        q = np.asarray(quantity, dtype=float)
        if not np.all(np.isfinite(q)) or np.any(q < 0):
            raise ValueError("Quantities must be finite and nonnegative.")
        return (underage + overage) * self.expected_overage(q) + underage * (self.mean - q)

    def censor(self, stock):
        """Return the law of min(D, stock), discarding the unobserved tail."""
        if not np.isfinite(stock) or stock <= 0:
            raise ValueError("Historical stock must be finite and strictly positive.")
        if stock >= self.upper:
            return self
        knots, masses = [0.0], []
        for a, z, mass in zip(self.knots[:-1], self.knots[1:], self.masses):
            if a >= stock:
                break
            end = min(z, stock)
            knots.append(float(end))
            masses.append(mass * (end - a) / (z - a))
        return PiecewiseUniform(tuple(knots), tuple(masses), max(0.0, 1 - sum(masses)))


def toy_marginals():
    """Two different tails with the same observable CDF below stock 40."""
    return {
        "A": PiecewiseUniform((0, 100), (1,)),
        "B": PiecewiseUniform((0, 40, 160), (0.4, 0.6)),
    }
