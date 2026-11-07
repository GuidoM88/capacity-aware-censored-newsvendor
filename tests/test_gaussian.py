import unittest
from math import sqrt

import numpy as np

try:
    import cvxpy  # noqa: F401
    HAVE_CVXPY = True
except ImportError:  # the Gaussian module needs an SDP solver
    HAVE_CVXPY = False


@unittest.skipUnless(HAVE_CVXPY, "cvxpy not installed (requirements-verify.txt)")
class GaussianTests(unittest.TestCase):
    def test_odd_chain_law_attains_the_closed_form(self):
        from censored_newsvendor.gaussian import check_gaussian_law
        for n, depth in [(4, 1), (5, 2), (6, 1)]:
            m, a = n - depth, 1 / n
            G = np.diag([(2 * i - 1) * a * a for i in range(1, n + 1)])
            H = sum(1 / (2 * i - 1) for i in range(2, m + 1))
            z = np.zeros(n)
            z[0] = 1.0
            for i in range(2, m + 1):
                z[i - 1] = 1 / (sqrt(1 - H) * (2 * i - 1))
            check = check_gaussian_law(G, [a] * n, 0.999 / sqrt(2 * n - 1), z)
            self.assertTrue(check["valid"])
            self.assertAlmostEqual(check["excess"], a * (1 - sqrt(1 - H)), places=12)

    def test_sdp_search_matches_the_bound_and_never_exceeds_it(self):
        from censored_newsvendor.gaussian import gaussian_envelope
        bound = 0.25 * (1 - sqrt(1 - 1 / 3 - 1 / 5))
        for structure, r in [("independent", 0.2), ("nonnegative", 0.3), ("nonnegative", 0.6)]:
            value = gaussian_envelope([0.25] * 4, r, depth=1, step=0.05, structure=structure)["value"]
            self.assertLessEqual(value, bound + 1e-7)
            if r <= 1 / sqrt(7):
                self.assertAlmostEqual(value, bound, places=5)

    def test_negative_correlations_reach_the_general_worst_case_at_small_r(self):
        from censored_newsvendor.gaussian import gaussian_envelope
        value = gaussian_envelope([0.25] * 4, 0.1, depth=1, step=0.05, structure="any")["value"]
        self.assertAlmostEqual(value, 0.675, places=4)


if __name__ == "__main__":
    unittest.main()
