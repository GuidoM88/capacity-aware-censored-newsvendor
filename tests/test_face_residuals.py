import unittest
from itertools import product

import numpy as np

from censored_newsvendor.coalition_audit import FiniteLaw, FrozenRule, exact_excess, forecast_rule
from censored_newsvendor.exclusion import ExclusionEnvelope
from censored_newsvendor.face_residuals import (
    Price, empirical_law, fit_prices, population_diagnostic, residual_certificate,
)


class FaceResidualTests(unittest.TestCase):
    def test_price_drift_is_needed_when_pilot_misses_positive_output(self):
        pilot = empirical_law(np.zeros((8, 3)))
        truth = empirical_law(np.ones((8, 3)))
        rule = FrozenRule(0., [1/3] * 3, [1.] * 3)
        prices = fit_prices(rule, pilot)
        result = population_diagnostic(rule, prices, truth)
        self.assertAlmostEqual(exact_excess(rule, truth)["excess"], 2.)
        self.assertAlmostEqual(result["upper"], 2.)
        self.assertAlmostEqual(result["faces"][0]["mu_interval"][0], 1.)
        self.assertAlmostEqual(result["faces"][0]["drift_upper"], 2.)
        # Ignoring drift gives residual 1-1=0 for each member, an invalid zero bound.

    def test_optimal_face_scores_certify_exchangeable_gap_is_zero(self):
        states = np.array(list(product([0., 1.], repeat=4)))
        truth = FiniteLaw(states, np.full(16, 1/16))
        rule = forecast_rule(FiniteLaw([[1/3] * 4, [.5] * 4], [.75, .25]), np.ones(4))
        result = population_diagnostic(rule, fit_prices(rule, truth), truth)
        self.assertAlmostEqual(result["upper"], 0.)
        self.assertAlmostEqual(result["gap_upper"], 0.)

    def test_signed_asymmetric_obstruction_is_not_misreported_as_exact(self):
        truth = FiniteLaw([[0., .6, .1], [1., 0., 0.]], [.5, .5])
        forecast = FiniteLaw([[.25, .1, .35], [.55, .2, .25]], [.5, .5])
        rule = forecast_rule(forecast, np.ones(3))
        d1 = ExclusionEnvelope.population(rule, truth).level(1)["upper"]
        self.assertAlmostEqual(d1, 7 / 50)
        for pilot in (forecast, truth):
            result = population_diagnostic(rule, fit_prices(rule, pilot), truth)
            self.assertGreaterEqual(result["gap_upper"] + 1e-12, d1)
            self.assertGreaterEqual(result["upper"] + 1e-12, d1)
            self.assertAlmostEqual(result["lower"], 0.)

    def test_finite_oracle_and_independent_enumeration_with_negative_weights(self):
        y = np.array([[0., .2, 1.], [1., .8, 0.], [.5, .1, .4], [.2, .9, .3]])
        pilot = empirical_law(y[[0, 0, 1, 2]])
        truth = empirical_law(y)
        sample = np.tile(y, (128, 1))
        for rule in [FrozenRule(1.1, [-1., .8, 1.2], np.ones(3), 3, 1),
                     FrozenRule(1.1, [.2, .3, .5], np.ones(3), 1, 3)]:
            prices = fit_prices(rule, pilot)
            res = residual_certificate(rule, prices, sample, .05)
            pop = population_diagnostic(rule, prices, truth)
            b = exact_excess(rule, truth)["excess"]
            d1 = ExclusionEnvelope.population(rule, truth).level(1)["upper"]
            self.assertLessEqual(res["lower"], b + 1e-12)
            self.assertGreaterEqual(res["upper"] + 1e-12, pop["upper"])
            self.assertGreaterEqual(res["gap_upper"] + 1e-12, d1 - b)
            self.assertFalse(res["fallback"])

    def test_grand_control_excludes_grand_and_invalid_prices_are_rejected(self):
        rule = FrozenRule(0., [.45, .3, .25], [1.] * 3)
        truth = empirical_law(np.ones((4, 3)))
        r = population_diagnostic(rule, (Price(2., 0.),), truth, grand=True)
        self.assertAlmostEqual(r["upper"], 2.25)
        with self.assertRaises(ValueError):
            residual_certificate(rule, (Price(0., 2.),) * 3, truth.states)
        with self.assertRaises(ValueError):
            residual_certificate(rule, (Price(0., 0.),) * 3, truth.states[:1])

