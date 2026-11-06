import random
import unittest
from fractions import Fraction as F

from censored_newsvendor.certificates import certificate_bound
from censored_newsvendor.exact_envelopes import best_equal_share_construction, last_depth_value


class CertificateBoundTests(unittest.TestCase):
    def test_reproduces_theorem_2_at_the_last_depth(self):
        rng = random.Random(11)
        for _ in range(12):
            n = rng.choice([3, 4, 5])
            raw = [rng.randint(1, 15) for _ in range(n)]
            shares = [F(x, sum(raw)) for x in raw]
            r = F(rng.randint(1, 20), 20)
            bound, _ = certificate_bound([float(x) for x in shares], float(r), n - 2)
            self.assertAlmostEqual(bound, float(last_depth_value(shares, r)), places=9)

    def test_reproduces_the_four_producer_curve(self):
        for r in (F(1, 10), F(1, 4), F(2, 5), F(7, 10)):
            bound, _ = certificate_bound([.25] * 4, float(r), 1)
            self.assertAlmostEqual(bound, float(best_equal_share_construction(4, r)["value"]), places=9)

    def test_unequal_four_producer_case_attained_by_a_law(self):
        # Attained by an explicit eight-atom law (results/exclusion/realizability_conjecture.md).
        bound, z = certificate_bound([.1, .2, .6, .1], .5, 1)
        self.assertAlmostEqual(bound, .45, places=7)
        self.assertAlmostEqual(max(z), 1.0)

    def test_rejects_invalid_depth(self):
        with self.assertRaises(ValueError):
            certificate_bound([.25] * 4, .5, 3)


if __name__ == "__main__":
    unittest.main()
