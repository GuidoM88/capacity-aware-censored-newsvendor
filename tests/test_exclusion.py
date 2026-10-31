import unittest
from itertools import product

import numpy as np

from censored_newsvendor.coalition_audit import (
    FiniteLaw, FrozenRule, enumeration_certificate, exact_excess, forecast_rule,
)
from censored_newsvendor.exclusion import ExclusionEnvelope


class ExclusionTests(unittest.TestCase):
    def test_one_exclusion_closes_the_known_three_sixteenths_gap(self):
        law = FiniteLaw(list(product([0., 1.], repeat=4)), np.full(16, 1 / 16))
        rule = forecast_rule(FiniteLaw([[1 / 3] * 4, [.5] * 4], [.75, .25]), np.ones(4))
        env = ExclusionEnvelope.population(rule, law)
        self.assertAlmostEqual(env.level(0)["upper"], 3 / 16)
        self.assertAlmostEqual(env.level(1)["upper"], 0)

    def test_larger_coalitions_are_retained_at_level_two(self):
        rule = FrozenRule(.75, [.6, .2, .2], [1, 1, 1])
        law = FiniteLaw([[1, 0, 0], [0, .6, .4]], [.5, .5])
        env = ExclusionEnvelope.population(rule, law)
        self.assertAlmostEqual(env.level(1)["upper"], 7 / 50)
        self.assertAlmostEqual(env.level(2)["upper"], 0)
        # A different rule's worst coalition is a pair, which a two-exclusion
        # face cannot contain. The separately evaluated large coalitions matter.
        pair_rule = FrozenRule(.75, [1, 1, -1], [1, 1, 1])
        pair_env = ExclusionEnvelope.population(pair_rule, law)
        self.assertAlmostEqual(pair_env.level(2)["upper"], .3)
        self.assertAlmostEqual(exact_excess(pair_rule, law)["excess"], .3)

    def test_finite_terminal_level_matches_clipped_enumeration_with_signed_shares(self):
        rule = FrozenRule(1.1, [-1., .8, 1.2], [1, 1, 1], over=3, under=1)
        sample = np.tile([[0., .2, 1.], [1., .8, 0.], [.5, .1, .4]], (120, 1))
        env = ExclusionEnvelope.validation(rule, sample, .04)
        reference = enumeration_certificate(rule, sample, .04)["upper"]
        self.assertAlmostEqual(env.level(2)["upper"], reference)
        self.assertAlmostEqual(env.binary_reference(), reference)
        self.assertGreaterEqual(env.level(1)["upper"] + 1e-10, reference)

    def test_exchangeability_can_include_strong_dependence(self):
        y = np.array(list(product([0., 1.], repeat=5)))
        p = np.full(32, .4 / 32)
        p[[0, -1]] += [.1, .5]
        law = FiniteLaw(y, p)
        rule = FrozenRule(1., np.full(5, .2), np.ones(5))
        env = ExclusionEnvelope.population(rule, law)
        formula = max(0., env.integer_value(np.array([0., 1., 1., 1., 1.])))
        self.assertAlmostEqual(env.level(1)["upper"], formula)
        self.assertAlmostEqual(exact_excess(rule, law)["excess"], formula)
