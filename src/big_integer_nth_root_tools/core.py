"""Core implementation of the integer nth root.

The algorithm is a Newton iteration on the integer floor of the root.
Starting from a power-of-two upper bound, each step replaces ``x`` with
``((k - 1) * x + n // x**(k - 1)) // k``.  For integer arithmetic this
iteration converges to the floor of the real kth root, and we stop as soon
as the candidate stops decreasing.

Why integer Newton rather than ``math.isqrt`` or ``int(n ** (1/k))``?
``math.isqrt`` only handles square roots, and floating point conversion
loses precision for integers above 2**53, which is exactly the range this
library targets.  Integer Newton stays exact for any size.
"""

from __future__ import annotations

__all__ = ["integer_nth_root"]


def _bit_length(n: int) -> int:
    """Return the number of bits needed to represent ``n``.

    ``int.bit_length`` already exists, but keeping the helper explicit makes
    the intent clear and avoids a method lookup in the hot loop.
    """
    return n.bit_length()


def integer_nth_root(n: int, k: int) -> int:
    """Return the integer floor of the ``k``-th root of ``n``.

    Parameters
    ----------
    n:
        A non-negative integer.  Negative values raise :class:`ValueError`
        because the integer floor of a root of a negative number is not
        well-defined for even ``k`` and is rarely wanted for odd ``k``.
    k:
        A positive integer.  ``k = 0`` raises :class:`ValueError` because
        the zeroth root is undefined.

    Returns
    -------
    int
        The largest integer ``r`` such that ``r ** k <= n``.

    Examples
    --------
    >>> integer_nth_root(27, 3)
    3
    >>> integer_nth_root(28, 3)
    3
    >>> integer_nth_root(0, 5)
    0
    >>> integer_nth_root(10**100, 10)
    10000000000
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if not isinstance(k, int):
        raise TypeError("k must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    if k <= 0:
        raise ValueError("k must be positive")

    # Trivial cases keep the main loop free of special-casing.
    if n < 2:
        return n
    if k == 1:
        return n

    # An upper bound of 2**ceil(bit_length / k) is always >= the true root,
    # because 2**bit_length > n.  Starting from a power of two makes the
    # first Newton step cheap and the convergence proof straightforward.
    x = 1 << ((_bit_length(n) + k - 1) // k)

    while True:
        # Newton step for f(x) = x**k - n.  Using integer division means the
        # iterate can undershoot the real root by at most one; the loop
        # condition below detects that and stops.
        y = ((k - 1) * x + n // (x ** (k - 1))) // k
        if y >= x:
            return x
        x = y
