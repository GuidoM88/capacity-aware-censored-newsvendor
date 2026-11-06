import unittest

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, coalition_table
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.seminorm_envelope import (
    PROPORTIONAL_ZERO_THRESHOLD, c31_ceiling, c39_envelope, configuration_prediction,
    depth_one_envelope, face_gap, minimal_cost, proportional_three_player_bound,
    proportional_three_player_closed_form, separable_bound, symmetric_unit_law,
    three_player_bound, zonotope_minimal_cost,
)

EQUAL3 = [1 / 3] * 3


class RealizabilityTests(unittest.TestCase):
    def test_four_inequality_bound_is_attained_by_an_explicit_law(self):
        # Three unequal shares: the zonotope LP gives a finite symmetric law;
        # the original audit code confirms gap 0.607143 with B=0 and rho=r.
        shares, r = np.array([.6, .25, .15]), .2
        z = [1.25 / 2.1, 1, 0]
        found = zonotope_minimal_cost(z, shares, r, samples=100_000)
        self.assertAlmostEqual(found["value"], 0, places=8)
        states, probabilities, offer, scale = symmetric_unit_law(found["generators"], shares)
        law, rule = FiniteLaw(states, probabilities), FrozenRule(offer, shares, np.ones(3))
        grand = float(probabilities @ np.abs(offer - states.sum(axis=1)))
        self.assertAlmostEqual(grand, scale, places=10)
        d1 = ExclusionEnvelope.population(rule, law).level(1)["upper"]
        table = coalition_table(rule, law)
        integer = max(0., max(row["excess"] for row in table))
        singles = [row["cost"] for row in table if len(row["coalition"]) == 1]
        self.assertLess(integer / grand, 1e-9)
        self.assertAlmostEqual(min(grand * w / c for w, c in zip(shares, singles)), r, places=8)
        self.assertAlmostEqual((d1 - integer) / grand, three_player_bound(shares, r), places=6)


class SeminormEnvelopeTests(unittest.TestCase):
    def test_c39_witnesses_have_the_expected_minimal_cost(self):
        # Low regime: the attaining law has zero cost at z=(1,0,1-2r).
        r = .2
        cost, _ = minimal_cost([1, 0, 1 - 2 * r], EQUAL3, r)
        self.assertAlmostEqual(cost, 0, places=8)
        self.assertAlmostEqual(face_gap([1, 0, 1 - 2 * r], EQUAL3, r), c39_envelope(r), places=8)
        # High regime: the optimal witness z=(1,0,(1-r)/2) has positive cost (3a-M)/2.
        r = .5
        cost, _ = minimal_cost([1, 0, (1 - r) / 2], EQUAL3, r)
        self.assertAlmostEqual(cost, 1 / 6, places=8)
        self.assertAlmostEqual(face_gap([1, 0, (1 - r) / 2], EQUAL3, r), .25, places=8)

    def test_relaxation_reproduces_c39_and_c30(self):
        for r in (0, .2, 1 / 3, .4, .8, 1):
            found = depth_one_envelope(EQUAL3, r, step=.02)
            self.assertAlmostEqual(found["value"], c39_envelope(r), places=6)
        self.assertAlmostEqual(c39_envelope(0), 2 / 3)

    def test_closed_form_bounds_agree_for_three_equal_shares(self):
        for r in np.linspace(.01, 1, 40):
            self.assertAlmostEqual(separable_bound(3, r), c39_envelope(r), places=12)
            self.assertAlmostEqual(three_player_bound(EQUAL3, r, fourth=False), c39_envelope(r), places=12)
            self.assertAlmostEqual(three_player_bound(EQUAL3, r), c39_envelope(r), places=12)

    def test_three_inequality_bound_is_not_sharp_for_unequal_shares(self):
        # Negative result: the C39 proof applied verbatim gives 0.68, but the
        # integral coordinate's standalone cap lowers the bound to 0.6071...
        shares, r = [.6, .25, .15], .2
        self.assertAlmostEqual(three_player_bound(shares, r, fourth=False), .68)
        four = three_player_bound(shares, r)
        self.assertAlmostEqual(four, .25 + .6 * 1.25 / 2.1)
        # The relaxation attains the four-inequality bound at z = e_2 + t e_1.
        t = 1.25 / 2.1
        self.assertAlmostEqual(face_gap([t, 1, 0], shares, r), four, places=6)
        self.assertLess(four, c31_ceiling(shares, r) - .07)

    def test_proportional_variant_closed_form_and_zero_region(self):
        for r in (.1, .15, .16, .17, .19, .2, .3, .7):
            self.assertAlmostEqual(proportional_three_player_bound(r),
                                   proportional_three_player_closed_form(r), places=12)
        self.assertEqual(proportional_three_player_closed_form(PROPORTIONAL_ZERO_THRESHOLD - 1e-3), 0)
        self.assertAlmostEqual(proportional_three_player_closed_form(.2), 4 / 15)
        found = depth_one_envelope(EQUAL3, .17, step=.02, pinned_singletons=True)
        self.assertAlmostEqual(found["value"], proportional_three_player_bound(.17), places=6)
        found = depth_one_envelope(EQUAL3, .1, step=.05, pinned_singletons=True)
        self.assertEqual(found["value"], 0)

    def test_four_players_window_below_c31(self):
        # Best point found at r=1/4 lies strictly below the proved bound 0.5625.
        r = .25
        self.assertAlmostEqual(separable_bound(4, r), c31_ceiling([.25] * 4, r))
        self.assertAlmostEqual(face_gap([1, 6 / 7, 5 / 14, 0], [.25] * 4, r), 31 / 56, places=6)
        # The natural symmetric C31 witness does not attain the bound here.
        t = (1 - r) - r / 2
        self.assertLess(face_gap([1, t, t, 0], [.25] * 4, r), separable_bound(4, r) - 1e-3)
        self.assertEqual(configuration_prediction(4, r), "below")
        self.assertEqual(configuration_prediction(4, .4), "c31")
        self.assertEqual(configuration_prediction(4, .2), "c31")  # zero-depth endpoint
        self.assertEqual(configuration_prediction(4, .6), "high")

    def test_infeasible_constraints_are_reported(self):
        # Artificial input exercising the infeasibility branch: a negative
        # grand-cost bound leaves the dual polytope empty.
        cost, _ = minimal_cost([1, 0, 0], EQUAL3, .2, grand_cost=-1)
        self.assertEqual(cost, float("inf"))


if __name__ == "__main__":
    unittest.main()
