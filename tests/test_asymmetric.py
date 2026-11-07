import random
import unittest
from fractions import Fraction as F

from censored_newsvendor.asymmetric import (
    _vec, asymmetric_best_block, asymmetric_equal_share_construction, asymmetric_equal_share_value,
    asymmetric_last_depth_construction, asymmetric_last_depth_value, asymmetric_windows,
    level_for_ratio, pinball_cost, ratio_for_level, segment_cost, three_point_law,
    verify_segments)
from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.exact_envelopes import (
    equal_share_value, general_cap_binding_candidates, general_share_construction, last_depth_value)
from censored_newsvendor.seminorm_envelope import minimal_cost


def attained(check):
    return all(v >= 0 for v in check.values()) and check["witness"] == 0


class PinballTests(unittest.TestCase):
    def test_ratio_and_level(self):
        self.assertEqual(ratio_for_level(F(1, 3)), 2)
        self.assertEqual(ratio_for_level(F(3, 4)), 3)
        self.assertEqual(level_for_ratio(2), F(1, 3))

    def test_two_point_cost(self):
        # +-1 with equal mass: the cost is min(tau, 1 - tau).
        states, probabilities = [(F(1),), (F(-1),)], [F(1, 2), F(1, 2)]
        self.assertEqual(pinball_cost(states, probabilities, (F(1),), F(1, 3)), F(1, 3))
        self.assertEqual(pinball_cost(states, probabilities, (F(1),), F(3, 4)), F(1, 4))

    def test_three_point_law_reproduces_an_asymmetric_segment(self):
        segments = [((F(1), F(-1)), F(3), F(2)), ((F(0), F(1)), F(1), F(1))]
        tau = level_for_ratio(2)
        states, probabilities, scale = three_point_law(segments, tau)
        for x in [(1, 0), (0, 1), (1, 1), (F(1), F(1, 3)), (-1, 0), (0, -1)]:
            x = tuple(F(v) for v in x)
            self.assertEqual(pinball_cost(states, probabilities, x, tau),
                             scale * segment_cost(segments, x))
        self.assertTrue(all(0 <= v <= 1 for state in states for v in state))

    def test_three_point_law_rejects_a_ratio_above_kappa(self):
        with self.assertRaises(ValueError):
            three_point_law([((F(1),), F(3), F(1))], level_for_ratio(2))


class LastDepthTests(unittest.TestCase):
    def test_kappa_one_is_theorem_2(self):
        rng = random.Random(5)
        for _ in range(20):
            n = rng.choice([3, 4, 5])
            raw = [rng.randint(1, 12) for _ in range(n)]
            shares = [F(x, sum(raw)) for x in raw]
            r = F(rng.randint(1, 19), 20)
            self.assertEqual(asymmetric_last_depth_value(shares, r, 1), last_depth_value(shares, r))

    def test_constructions_attain_the_certificate_bound(self):
        rng = random.Random(9)
        for _ in range(12):
            n = rng.choice([3, 4])
            raw = [rng.randint(1, 12) for _ in range(n)]
            shares = [F(x, sum(raw)) for x in raw]
            r = F(rng.randint(1, 19), 20)
            kappa = rng.choice([F(3, 2), F(2), F(5)])
            con = asymmetric_last_depth_construction(shares, r, kappa)
            check = verify_segments(con["segments"], shares, r, kappa, con["membership"], con["value"])
            self.assertTrue(attained(check), (shares, r, kappa, check))
            bound, _ = certificate_bound([float(x) for x in shares], float(r), n - 2, kappa=float(kappa))
            self.assertAlmostEqual(bound, float(con["value"]), places=9)

    def test_value_grows_with_kappa_up_to_the_ceiling(self):
        shares, r = [F(1, 3)] * 3, F(3, 5)
        values = [asymmetric_last_depth_value(shares, r, k) for k in (1, 2, 4, 100)]
        self.assertEqual(values, sorted(values))
        self.assertLessEqual(values[-1], (1 - r) * F(2, 3))


class EqualShareTests(unittest.TestCase):
    def test_kappa_one_is_theorem_1(self):
        for n in (4, 5, 7):
            for depth in range(1, n - 1):
                for k in range(1, 20):
                    r = F(k, 20)
                    self.assertEqual(asymmetric_equal_share_value(n, r, depth, 1),
                                     equal_share_value(n, r, depth))

    def test_constructions_are_exact(self):
        for n, depth, kappa in [(4, 1, F(3, 2)), (5, 1, F(2)), (6, 2, F(10)), (5, 2, F(6, 5))]:
            for k in range(1, 20):
                r = F(k, 20)
                value = asymmetric_equal_share_value(n, r, depth, kappa)
                con = asymmetric_equal_share_construction(n, r, depth, kappa)
                if value is None:
                    self.assertIsNone(con)
                    continue
                check = verify_segments(con["segments"], [F(1, n)] * n, r, kappa,
                                        con["membership"], value)
                self.assertTrue(attained(check), (n, depth, kappa, r, check))

    def test_windows_close_at_two_m_minus_one_over_m(self):
        for m in (3, 4, 5, 6):
            closing = F(2 * (m - 1), m)
            self.assertEqual(asymmetric_windows(m + 1, 1, closing), [])
            self.assertNotEqual(asymmetric_windows(m + 1, 1, closing - F(1, 100)), [])

    def test_four_producer_example_with_kappa_two(self):
        # The symmetric window value 31/56 rises to the ceiling 9/16.
        self.assertEqual(asymmetric_equal_share_value(4, F(1, 4), 1, 2), F(9, 16))
        bound, _ = certificate_bound([.25] * 4, .25, 1, kappa=2.0)
        self.assertAlmostEqual(bound, 9 / 16, places=9)


class TwoBlockTests(unittest.TestCase):
    def test_laws_are_valid_at_intermediate_depths(self):
        rng = random.Random(4)
        for _ in range(10):
            n = rng.choice([4, 5])
            raw = [rng.randint(1, 20) for _ in range(n)]
            shares = [F(x, sum(raw)) for x in raw]
            r, kappa = F(rng.randint(1, 19), 20), rng.choice([F(1), F(2), F(10)])
            depth = rng.randint(1, n - 3)
            block = asymmetric_best_block(shares, r, depth, kappa)
            check = verify_segments(block["segments"], shares, r, kappa,
                                    block["membership"], block["value"])
            self.assertTrue(attained(check), (shares, r, kappa, depth, check))

    def test_last_depth_is_theorem_a(self):
        shares = [F(3, 10), F(1, 2), F(1, 5)]
        for r in (F(1, 5), F(1, 2), F(4, 5)):
            for kappa in (1, 2, 5):
                self.assertEqual(asymmetric_best_block(shares, r, 1, kappa)["value"],
                                 asymmetric_last_depth_value(shares, r, kappa))

    def test_kappa_one_is_the_best_of_the_three_symmetric_families(self):
        rng = random.Random(8)
        for _ in range(8):
            n = rng.choice([4, 5])
            raw = [rng.randint(1, 20) for _ in range(n)]
            shares = [F(x, sum(raw)) for x in raw]
            r, depth = F(rng.randint(1, 19), 20), rng.randint(1, n - 3)
            symmetric = [c["value"] for c in general_cap_binding_candidates(shares, r, depth)]
            two = general_share_construction(shares, r, depth)
            if two is not None:
                symmetric.append(two["value"])
            self.assertEqual(asymmetric_best_block(shares, r, depth, 1)["value"], max(symmetric))


class ConjectureCTests(unittest.TestCase):
    def test_counterexample_beats_every_two_block_law(self):
        from censored_newsvendor.asymmetric import asymmetric_zonotope_minimal_cost
        shares = [F(1, 50), F(24, 50), F(24, 50), F(1, 50)]
        r, kappa = F(33, 50), F(10)
        two_block = asymmetric_best_block(shares, r, 1, kappa)["value"]
        z = [1.0, 335440 / 818481, 3560 / 34401, 0.0]
        found = asymmetric_zonotope_minimal_cost(z, [float(x) for x in shares], float(r), float(kappa))
        law = sum(float(a) * b for a, b in zip(shares, z)) - found["value"]
        self.assertGreater(law, float(two_block) + 0.016)

    def test_ceiling_criterion_with_small_producers(self):
        # Every share of the largest face is below the window width, so the
        # two-block lower bound already reaches the elementary ceiling.
        shares = [F(k, 55) for k in range(1, 11)][:6]
        shares = [x / sum(shares) for x in shares]
        r, kappa = F(1, 5), F(2)
        face = sum(shares) - min(shares)
        self.assertEqual(asymmetric_best_block(shares, r, 1, kappa)["value"], (1 - r) * face)


class RelaxationTests(unittest.TestCase):
    def test_kappa_one_leaves_the_oracle_unchanged(self):
        z, shares = [1.0, 0.4, 0.2, 0.0], [0.25] * 4
        self.assertAlmostEqual(minimal_cost(z, shares, 0.5)[0],
                               minimal_cost(z, shares, 0.5, kappa=1.0)[0], places=12)

    def test_ceiling_bounds_every_ratio(self):
        rng = random.Random(2)
        for _ in range(6):
            raw = [rng.randint(1, 9) for _ in range(4)]
            shares = [x / sum(raw) for x in raw]
            r, kappa = rng.uniform(0.1, 0.9), rng.choice([1.5, 3.0, 20.0])
            bound, _ = certificate_bound(shares, r, 1, kappa=kappa)
            ceiling = (1 - r) * max(sum(shares) - x for x in shares)
            self.assertLessEqual(bound, ceiling + 1e-9)


if __name__ == "__main__":
    unittest.main()
