import random
import unittest
from fractions import Fraction as F

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exact_envelopes import (
    equal_share_construction, equal_share_value, four_line_bound, last_depth_construction,
    last_depth_value, pair_regime, verify_generators, windows,
)
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.seminorm_envelope import symmetric_unit_law


def attains(construction, shares, r):
    check = verify_generators(construction["generators"], shares, r,
                              construction["membership"], construction["value"])
    return (check["cap"] >= 0 and check["stability"] >= 0 and check["grand"] >= 0
            and check["witness"] == 0 and check["rho"] == r)


class EqualShareTests(unittest.TestCase):
    def test_windows_for_small_n(self):
        self.assertEqual(windows(3), [])
        self.assertEqual(windows(4), [(F(1, 5), F(1, 3))])
        self.assertEqual(windows(5), [(F(1, 3), F(1, 2))])
        self.assertEqual(windows(8), [(F(2, 5), F(3, 7)), (F(5, 9), F(5, 7))])
        # Windows depend only on the number of free producers n - depth.
        self.assertEqual(windows(6, depth=3), windows(4))

    def test_constructions_attain_c31_and_high_values(self):
        cases = [(4, 1, F(1, 10), "c31", F(27, 40)), (4, 1, F(2, 5), "c31", F(9, 20)),
                 (4, 1, F(3, 5), "high", F(4, 15)), (6, 2, F(1, 4), "c31", F(1, 2)),
                 (7, 1, F(9, 10), "high", F(19, 252))]
        for n, depth, r, regime, value in cases:
            construction = equal_share_construction(n, r, depth)
            self.assertEqual(construction["regime"], regime)
            self.assertEqual(construction["value"], value)
            self.assertTrue(attains(construction, [F(1, n)] * n, r), (n, depth, r))

    def test_window_has_no_construction(self):
        self.assertIsNone(equal_share_construction(4, F(1, 4)))
        self.assertIsNone(equal_share_value(4, F(1, 4)))


class LastDepthTests(unittest.TestCase):
    def test_three_player_example_and_regimes(self):
        shares, r = [F(3, 5), F(1, 4), F(3, 20)], F(1, 5)
        self.assertEqual(last_depth_value(shares, r), F(17, 28))
        construction = last_depth_construction(shares, r)
        self.assertEqual(construction["regime"], "g1g4")
        self.assertTrue(attains(construction, shares, r))

    def test_regimes_meet_continuously(self):
        a_j, r = F(1, 3), F(1, 4)
        for x in ((1 - r) / (1 + r), (1 - r) / (2 * r)):
            left = pair_regime(x * a_j - F(1, 10**9), a_j, r)[2]
            right = pair_regime(x * a_j, a_j, r)[2]
            self.assertLess(abs(left - right), F(1, 10**6))

    def test_closed_form_matches_four_line_bound_and_constructions(self):
        rng = random.Random(7)
        for _ in range(60):
            n = rng.randint(3, 6)
            raw = [F(rng.randint(1, 25)) for _ in range(n)]
            shares = [x / sum(raw) for x in raw]
            r = F(rng.randint(1, 30), 30)
            value = last_depth_value(shares, r)
            self.assertAlmostEqual(float(value), four_line_bound(shares, r), places=10)
            self.assertTrue(attains(last_depth_construction(shares, r), shares, r))

    def test_original_audit_code_confirms_one_law(self):
        shares, r = [F(3, 5), F(1, 4), F(3, 20)], F(1, 5)
        construction = last_depth_construction(shares, r)
        g = np.array([[float(x) for x in v] for v in construction["generators"]])
        w = np.array([float(x) for x in shares])
        states, probabilities, offer, _ = symmetric_unit_law(g, w)
        law, rule = FiniteLaw(states, probabilities), FrozenRule(offer, w, np.ones(3))
        grand = float(probabilities @ np.abs(offer - states.sum(axis=1)))
        d1 = ExclusionEnvelope.population(rule, law).level(1)["upper"]
        integer = max(0., max(row["excess"] for row in coalition_table(rule, law)))
        self.assertAlmostEqual((d1 - integer) / grand, 17 / 28, places=8)


if __name__ == "__main__":
    unittest.main()
