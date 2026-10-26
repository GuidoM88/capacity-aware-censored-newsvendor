"""Population experiments for capacitated inventory decisions under censoring."""

from .allocation import Allocation, solve_allocation
from .distributions import PiecewiseUniform

__all__ = ["Allocation", "PiecewiseUniform", "solve_allocation"]
