import importlib.util
import itertools
import unittest
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from censored_newsvendor.asymmetric import level_for_ratio, pinball_cost

ROOT = Path(__file__).resolve().parents[1]


def load():
    spec = importlib.util.spec_from_file_location("illustrate", ROOT / "scripts/illustrate_wind_audit.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IllustrationTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        rng = np.random.default_rng(3)
        self.Y = rng.integers(0, 9, size=(40, 3)).astype(float)

    def test_cost_matches_exact_pinball(self):
        for kappa in (1, 2):
            tau = level_for_ratio(kappa)
            states = [tuple(F(int(v)) for v in row) for row in self.Y]
            probs = [F(1, len(states))] * len(states)
            for x in ([1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0.5, 0.25]):
                exact = pinball_cost(states, probs, tuple(F(v) for v in x), tau)
                self.assertAlmostEqual(self.m.cost(self.Y @ np.array(x), kappa), float(exact), places=9)

    def test_fractional_excess_beats_a_grid(self):
        charges = np.array([1.1, 0.9, 0.7])
        for kappa in (1, 2):
            value, z = self.m.fractional_excess(self.Y, charges, [0, 1, 2], kappa)
            grid = max(charges @ np.array(p) - self.m.cost(self.Y @ np.array(p), kappa)
                       for p in itertools.product(np.linspace(0, 1, 11), repeat=3))
            self.assertGreaterEqual(value, grid - 1e-9)
            self.assertAlmostEqual(value, charges @ z - self.m.cost(self.Y @ z, kappa), places=7)


if __name__ == "__main__":
    unittest.main()
