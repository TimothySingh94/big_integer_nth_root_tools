"""Integer nth root utilities.

This package exposes a single function, :func:`integer_nth_root`, which
computes the floor of the kth root of an arbitrarily large integer using
Newton's method adapted to integer arithmetic.
"""

from .core import integer_nth_root

__all__ = ["integer_nth_root"]
