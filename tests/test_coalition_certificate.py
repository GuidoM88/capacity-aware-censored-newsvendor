"""Independent optimization and analytical checks for the research certificate."""

import unittest
from itertools import product

import numpy as np
from numpy.testing import assert_allclose

from censored_newsvendor.coalition_audit import (
    FiniteLaw, FrozenRule, best_common_dual, coalition_program, coalition_table,
    enumeration_certificate, exact_excess, finite_certificate, forecast_rule,
    loss, optimal_offer, population_bound, proper_subset_support,
)


class CoalitionCertificateTests(unittest.TestCase):
    def test_three_producer_dependence_counterexample(self):
        forecast = FiniteLaw([[1, 0, 0], [0, 1, 1]], [0.5, 0.5])
        truth = FiniteLaw([[0, 1, 0], [1, 0, 1]], [0.5, 0.5])
        rule = forecast_rule(forecast, np.ones(3))
        assert_allclose(rule.weights, [-1, 1, 1])
        self.assertAlmostEqual(rule.offer, 1.5)
        self.assertAlmostEqual(exact_excess(rule, truth)["excess"], 1)
        self.assertAlmostEqual(population_bound(rule, truth)["bound"], 1)
        self.assertAlmostEqual(best_common_dual(rule, truth)["bound"], 1)
        self.assertAlmostEqual(coalition_program(rule, truth, integral=True)["bound"], 1)

    def test_stable_rule_can_have_a_fixed_score_gap(self):
        states = np.array(list(product([0., 1.], repeat=4)))
        p = np.full(16, 1 / 16)
        q = p.copy()
        for k in range(4):
            unit = np.eye(4)[k]
            selected = np.all(states == unit, axis=1) | np.all(states == 1 - unit, axis=1)
            q[selected] += (-3 if k < 2 else 3) / 160
        forecast, truth = FiniteLaw(states, q), FiniteLaw(states, p)
        assert_allclose(q @ states, p @ states)
        assert_allclose(np.bincount(states.sum(1).astype(int), weights=q),
                        np.bincount(states.sum(1).astype(int), weights=p))
        rule = forecast_rule(forecast, np.ones(4))
        assert_allclose(rule.weights, [.3, .3, .2, .2])
        self.assertAlmostEqual(exact_excess(rule, truth)["excess"], 0)
        self.assertAlmostEqual(population_bound(rule, truth)["bound"], 3 / 40)
        self.assertAlmostEqual(best_common_dual(rule, truth)["bound"], 0)

    def test_even_best_common_score_has_a_fractional_gap(self):
        truth = FiniteLaw(list(product([0., 1.], repeat=4)), np.full(16, 1 / 16))
        forecast = FiniteLaw([[1 / 3] * 4, [.5] * 4], [.75, .25])
        rule = forecast_rule(forecast, np.ones(4))
        assert_allclose(rule.weights, [.25] * 4)
        self.assertAlmostEqual(rule.offer, 4 / 3)
        self.assertAlmostEqual(exact_excess(rule, truth)["excess"], 0)
        self.assertAlmostEqual(population_bound(rule, truth)["bound"], 3 / 4)
        for solve in (best_common_dual, coalition_program):
            self.assertAlmostEqual(solve(rule, truth)["bound"], 3 / 16)
        self.assertAlmostEqual(coalition_program(rule, truth, integral=True)["bound"], 0)
        z = np.full(4, .75)
        _, fractional_cost = optimal_offer(truth.states @ z, truth.probabilities)
        self.assertAlmostEqual(z @ rule.weights - fractional_cost, 3 / 16)

    def test_forecast_dual_is_core_with_asymmetric_costs_and_atoms(self):
        law = FiniteLaw([[0, 0, 0], [1, 0, 1], [1, 1, 1]], [.1, .5, .4])
        for over, under in [(1, 1), (1, 3), (3, 1)]:
            rule = forecast_rule(law, np.ones(3), over, under)
            self.assertAlmostEqual(float(law.probabilities @ rule.score(law.states)), 0)
            self.assertLessEqual(max(row["excess"] for row in coalition_table(rule, law)), 1e-10)

    def test_quantile_minimum_matches_exhaustive_support_actions(self):
        totals, p = np.array([0., .4, .4, 2., 3.]), np.array([.1, .1, .2, .5, .1])
        for over, under in [(1, 1), (1, 3), (3, 1)]:
            _, value = optimal_offer(totals, p, over, under)
            expected = min(p @ loss(q, totals, over, under) for q in totals)
            self.assertAlmostEqual(value, expected)

    def test_proper_support_excludes_grand_coalition_and_handles_signed_entries(self):
        for values in [[1, 2, 3], [-2, 1, 1], [0, -1, -2], [-1, -1, -1]]:
            choices = list(product([0, 1], repeat=3))[:-1]
            expected = max(np.dot(mask, values) for mask in choices)
            self.assertEqual(proper_subset_support(values), expected)

    def test_certificates_enclose_population_when_empirical_law_equals_truth(self):
        y = np.array([[0., .2, 1.], [1., .8, 0.], [.5, .1, .4], [.2, .9, .3]])
        law = FiniteLaw(y, np.full(4, .25))
        for weights in [[-2., 1.5, 1.5], [.2, .3, .5]]:
            rule = FrozenRule(1.1, weights, np.ones(3), 3., 1.)
            sample = np.tile(y, (256, 1))
            self.assertGreaterEqual(finite_certificate(rule, sample)["upper"] + 1e-12,
                                    population_bound(rule, law)["bound"])
            self.assertGreaterEqual(enumeration_certificate(rule, sample)["upper"] + 1e-12,
                                    exact_excess(rule, law)["excess"])

    def test_invalid_bounds_and_zero_forecast_division_are_rejected(self):
        with self.assertRaises(ValueError):
            forecast_rule(FiniteLaw([[1, 1], [0, 2]], [.5, .5]), [1, 2])
        rule = FrozenRule(1, [.5, .5], [1, 1])
        for data in [[[1.1, 0]], [[-1, 0]], [[float('nan'), 0]], []]:
            with self.assertRaises(ValueError):
                finite_certificate(rule, data)
        with self.assertRaises(ValueError):
            finite_certificate(rule, [[0, 0]], delta=0)
        with self.assertRaises(ValueError):
            FrozenRule(1, [.5, .5], [1, 1], tie_score=2)


if __name__ == "__main__":
    unittest.main()
