import unittest

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, exact_excess, forecast_rule
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.standalone_certificate import (
    StandaloneAudit, block_gap_certificate, fit_standalone_audit,
    marginal_certificate, standalone_certificate,
)


class StandaloneCertificateTests(unittest.TestCase):
    def test_identical_producers_do_not_incur_a_dimension_penalty(self):
        results = []
        for n in (3, 12):
            y = np.tile(np.array([[0.] * n, [1.] * n]), (2048, 1))
            rule = FrozenRule(n / 2, np.full(n, 1 / n), np.ones(n))
            audit = fit_standalone_audit(rule, y)
            primary = standalone_certificate(rule, audit, y)
            conservative = standalone_certificate(rule, audit, y, bonferroni=True)
            self.assertGreaterEqual(primary["rho_grid"], conservative["rho_grid"])
            self.assertGreater(primary["rho_grid"], .5)
            results.append(primary)
        self.assertEqual(results[0]["rho_grid"], results[1]["rho_grid"])
        self.assertEqual(results[0]["scalar_tail"], results[1]["scalar_tail"])

    def test_zero_grand_cost_does_not_imply_positive_standalone_coverage(self):
        y = np.tile(np.eye(3), (100, 1))
        rule = FrozenRule(1., np.full(3, 1 / 3), np.ones(3))
        audit = fit_standalone_audit(rule, y)
        result = standalone_certificate(rule, audit, y)
        self.assertEqual(result["rho_lower"], 0.)
        self.assertFalse(result["half_certified"])
        self.assertEqual(len(result["threshold_checks"]), 1)
        self.assertEqual(result["gap_by_depth"][-1], 0.)

    def test_sharp_obstruction_remains_covered(self):
        m, n = 20., 4
        h = m + 4
        states = np.array([[m, 2., 2., 0.], [0., 0., 0., h - 1]]) / h
        truth = FiniteLaw(states, [.5, .5])
        forecast = FiniteLaw(np.repeat(states.sum(axis=1)[:, None] / n, n, axis=1), [.5, .5])
        rule = forecast_rule(forecast, np.ones(n))
        y = np.tile(states, (512, 1))
        audit = fit_standalone_audit(rule, y)
        result = standalone_certificate(rule, audit, y)
        b = exact_excess(rule, truth)["excess"]
        self.assertAlmostEqual(b, 0.)
        for k, g in enumerate(result["gap_by_depth"], 1):
            actual = ExclusionEnvelope.population(rule, truth).level(k)["upper"] - b
            self.assertGreaterEqual(g + 1e-10, actual)
        self.assertLess(result["rho_lower"], .5)

    def test_pilot_missed_state_only_makes_ratio_test_more_conservative(self):
        rule = FrozenRule(1.5, [1 / 3] * 3, [1.] * 3)
        pilot = np.zeros((128, 3))
        validation = np.tile(np.array([[0.] * 3] + [[1.] * 3] * 9), (100, 1))
        wrong = fit_standalone_audit(rule, pilot)
        good = StandaloneAudit((1., 1., 1.), (), 0.)
        bad_result = standalone_certificate(rule, wrong, validation)
        good_result = standalone_certificate(rule, good, validation)
        self.assertLess(bad_result["rho_grid"], good_result["rho_grid"])
        self.assertLessEqual(bad_result["rho_lower"], 1.)

    def test_marginal_and_block_bounds_cover_independent_finite_reference(self):
        states = np.array([[0., .2, 1.], [1., .8, 0.], [.5, .1, .4], [.2, .9, .3]])
        truth = FiniteLaw(states, [.25] * 4)
        y = np.tile(states, (64, 1))
        rule = FrozenRule(1.1, [.2, .3, .5], np.ones(3), 1, 3)
        audit = fit_standalone_audit(rule, y)
        b = exact_excess(rule, truth)["excess"]
        gap = ExclusionEnvelope.population(rule, truth).level(1)["upper"] - b
        for result in (marginal_certificate(rule, audit, y, y),
                       marginal_certificate(rule, audit, y, y, capacity_only=True),
                       block_gap_certificate(rule, audit, y, block_size=64)):
            self.assertGreaterEqual(result["gap_upper"] + 1e-10, gap)
            self.assertFalse(result["fallback"])

    def test_all_zero_capacities_and_terminal_depth(self):
        rule = FrozenRule(0., [.4, .6], [0., 0.])
        y = np.zeros((8, 2))
        result = standalone_certificate(rule, fit_standalone_audit(rule, y), y)
        self.assertEqual(result["rho_lower"], 1.)
        self.assertEqual(result["gap_upper"], 0.)

    def test_invalid_scope_and_unfrozen_witness_are_rejected(self):
        y = np.zeros((4, 3))
        for weights in ([0., .5, .5], [-1., 1., 1.]):
            with self.assertRaises(ValueError):
                fit_standalone_audit(FrozenRule(0., weights, np.ones(3)), y)
        rule = FrozenRule(1.5, [1 / 3] * 3, np.ones(3))
        audit = fit_standalone_audit(rule, y)
        for bad in (StandaloneAudit((0., 0., 0.), (0, 1, 2), 0.),
                    StandaloneAudit((2., 0., 0.), (), 0.)):
            with self.assertRaises(ValueError):
                standalone_certificate(rule, bad, y)
        with self.assertRaises(ValueError):
            standalone_certificate(rule, audit, y[:1])
        with self.assertRaises(ValueError):
            standalone_certificate(rule, audit, y, delta=0)
        with self.assertRaises(ValueError):
            block_gap_certificate(rule, audit, y, block_size=3)
