import importlib.util
import unittest
from pathlib import Path

try:
    import sympy  # noqa: F401
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False


@unittest.skipUnless(HAVE_SYMPY, "sympy not installed (see requirements-verify.txt)")
class SymbolicProofTests(unittest.TestCase):
    def test_every_symbolic_check_passes(self):
        path = Path(__file__).resolve().parents[1] / "scripts" / "verify_symbolic.py"
        spec = importlib.util.spec_from_file_location("verify_symbolic", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)       # the checks run at import time
        failed = [c for c in module.CHECKS if not c["passed"]]
        self.assertGreaterEqual(len(module.CHECKS), 130)
        self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()
