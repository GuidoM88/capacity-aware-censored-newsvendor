"""Analytical identities and independent optimization checks for the research example."""

import unittest
from itertools import product

import numpy as np
from numpy.testing import assert_allclose
from scipy.integrate import quad
from scipy.optimize import minimize

from censored_newsvendor.allocation import solve_allocation, total_cost
from censored_newsvendor.distributions import PiecewiseUniform, toy_marginals
from censored_newsvendor.experiment import run_experiment
from censored_newsvendor.robust import solve_finite_scenario_regret


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.models = toy_marginals()

    def test_censored_histories_are_identical_under_common_uniform_draws(self):
        u = np.linspace(0, 1, 10001)
        a, b = self.models["A"], self.models["B"]
        assert_allclose(np.minimum(a.ppf(u), 40), np.minimum(b.ppf(u), 40), atol=1e-12)
        self.assertEqual(a.censor(40), b.censor(40))
        self.assertAlmostEqual(a.censor(40).atom_mass, 0.6)

    def test_expected_loss_matches_independent_numerical_integration(self):
        for name, model in self.models.items():
            for cap in [None, 25, 40, 55]:
                evaluated = model if cap is None else model.censor(cap)
                for q in [0, 20, 40, 60, 120, 180]:
                    total = 0.0
                    for lo, hi, mass in zip(model.knots[:-1], model.knots[1:], model.masses):
                        def integrand(demand):
                            demand = demand if cap is None else min(demand, cap)
                            return 4 * max(demand - q, 0) + max(q - demand, 0)
                        points = [x for x in [q, cap] if x is not None and lo < x < hi]
                        total += mass * quad(integrand, lo, hi, points=points)[0] / (hi - lo)
                    with self.subTest(model=name, cap=cap, q=q):
                        self.assertAlmostEqual(float(evaluated.expected_cost(q)), total, places=8)

    def test_uniform_hand_calculation(self):
        self.assertAlmostEqual(float(self.models["A"].expected_cost(30)), 102.5)

    def test_atom_is_handled_as_a_subgradient_interval(self):
        d = self.models["A"].censor(40)
        self.assertAlmostEqual(float(d.cdf_left(40)), 0.4)
        self.assertAlmostEqual(float(d.cdf(40)), 1.0)
        self.assertEqual(float(d.ppf(0.8)), 40)

    def test_invalid_distributions_are_rejected(self):
        for knots, masses, atom in [((0, 10), (0.8,), 0), ((0, 10, 20), (1, 0), 0),
                                   ((5, 10), (1,), 0), ((0, 0), (1,), 0)]:
            with self.subTest(knots=knots, masses=masses), self.assertRaises(ValueError):
                PiecewiseUniform(knots, masses, atom)


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.models = toy_marginals()

    def test_analytical_ab_allocation_over_the_binding_region(self):
        for capacity in [81, 100, 120, 160, 199]:
            result = solve_allocation([self.models["A"], self.models["B"]], capacity)
            assert_allclose(result.quantities, [(capacity + 40) / 3, (2 * capacity - 40) / 3], atol=1e-9)

    def test_all_tail_pairs_agree_below_the_threshold(self):
        models = list(self.models.values()) + [PiecewiseUniform((0, 40, 1000), (0.4, 0.6))]
        for pair in product(models, repeat=2):
            for capacity in [0, 1, 60, 79.999, 80]:
                assert_allclose(solve_allocation(pair, capacity).quantities, [capacity / 2] * 2, atol=1e-9)

    def test_ab_and_ba_diverge_above_the_threshold(self):
        for capacity in [80.01, 120, 199, 260]:
            ab = solve_allocation([self.models["A"], self.models["B"]], capacity)
            ba = solve_allocation([self.models["B"], self.models["A"]], capacity)
            self.assertGreater(np.max(abs(ab.quantities - ba.quantities)), 1e-4)

    def test_slack_capacity_does_not_force_excess_ordering(self):
        result = solve_allocation([self.models["A"], self.models["B"]], 260)
        assert_allclose(result.quantities, [80, 120], atol=1e-10)
        self.assertEqual(result.multiplier, 0)
        self.assertAlmostEqual(result.capacity_used, 200)

    def test_sales_baseline_has_an_upper_atom_and_leaves_capacity_unused(self):
        observed = [self.models["A"].censor(40)] * 2
        assert_allclose(solve_allocation(observed, 60).quantities, [30, 30], atol=1e-10)
        result = solve_allocation(observed, 120)
        assert_allclose(result.quantities, [40, 40])
        self.assertAlmostEqual(result.kkt_residual, 0)

    def test_heterogeneous_costs_and_resources_against_independent_optimizer(self):
        rng = np.random.default_rng(7)
        models = [self.models["A"], self.models["B"], PiecewiseUniform((0, 20, 90), (0.6, 0.4))]
        for _ in range(8):
            b, h, a = rng.uniform(1, 8, 3), rng.uniform(0.5, 3, 3), rng.uniform(0.3, 2, 3)
            capacity = float(rng.uniform(20, 150))
            solved = solve_allocation(models, capacity, b, h, a)
            reference = minimize(
                lambda q: total_cost(models, q, b, h), np.full(3, capacity / (3 * a.sum())),
                method="SLSQP", bounds=[(0, None)] * 3,
                constraints=[{"type": "ineq", "fun": lambda q: capacity - a @ q}],
                options={"ftol": 1e-10, "maxiter": 1000},
            )
            self.assertTrue(reference.success, reference.message)
            self.assertAlmostEqual(solved.expected_cost, reference.fun, places=6)
            self.assertLess(solved.kkt_residual, 1e-7)

    def test_invalid_capacity_is_rejected(self):
        for capacity in [-1, np.nan, np.inf]:
            with self.assertRaises(ValueError):
                solve_allocation([self.models["A"]], capacity)


class RobustTests(unittest.TestCase):
    def setUp(self):
        m = toy_marginals()
        self.scenarios = [tuple(m[key] for key in pair) for pair in product("AB", repeat=2)]

    def test_closed_form_minimax_at_capacity_120(self):
        result = solve_finite_scenario_regret(self.scenarios, 120)
        assert_allclose(result.quantities, [60, 60], atol=1e-7)
        self.assertAlmostEqual(result.worst_regret, 5 / 3, places=8)
        assert_allclose(result.scenario_regrets, [0, 5 / 3, 5 / 3, 0], atol=1e-8)

    def test_zero_regret_when_the_common_optimum_is_identified(self):
        for capacity in [0, 60, 80]:
            result = solve_finite_scenario_regret(self.scenarios, capacity)
            assert_allclose(result.quantities, [capacity / 2] * 2, atol=1e-8)
            self.assertLess(result.worst_regret, 1e-8)

    def test_asymmetric_scenario_family_against_dense_grid(self):
        scenarios = self.scenarios[:2]
        result = solve_finite_scenario_regret(scenarios, 120)
        oracle_costs = [solve_allocation(s, 120).expected_cost for s in scenarios]
        # Both products have negative marginal cost on the relevant frontier;
        # these instances use the entire capacity. Check all two-dimensional
        # feasible grid points as an independent finite-search reference.
        best = float("inf")
        for q1 in np.linspace(0, 120, 61):
            for q2 in np.arange(0, 120 - q1 + 1, 2):
                best = min(best, max(total_cost(s, [q1, q2]) - c for s, c in zip(scenarios, oracle_costs)))
        self.assertLessEqual(result.worst_regret, best + 1e-7)
        self.assertGreaterEqual(result.worst_regret, best - 0.5)

    def test_end_to_end_population_outcomes(self):
        rows = run_experiment([60, 80, 120])
        self.assertEqual(len(rows), 48)
        worst_naive = max(r["regret"] for r in rows if r["capacity"] == 120 and r["policy"] == "sales_as_demand")
        self.assertAlmostEqual(worst_naive, 70)
        self.assertTrue(all(r["regret"] >= 0 for r in rows))


if __name__ == "__main__":
    unittest.main()
