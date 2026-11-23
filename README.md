# big_integer_nth_root_tools

Computes the integer floor of the kth root of an arbitrarily large integer via a Newton iteration adapted for integers.

```python
from big_integer_nth_root_tools import integer_nth_root

integer_nth_root(27, 3)
# 3

integer_nth_root(10**100, 10)
# 10000000000

integer_nth_root(10**100 - 1, 10)
# 9999999999
```

The function takes two arguments: `n`, a non-negative integer, and `k`, a positive integer. It returns the largest integer `r` such that `r ** k <= n`.

## Why this exists

Python's `math.isqrt` covers square roots exactly, but there is no standard-library function for higher roots of big integers. The usual shortcut, `int(n ** (1 / k))`, converts `n` to a float, which loses precision above 2**53 and gives wrong answers for large inputs. This library keeps the whole computation in integer arithmetic, so the result is exact for any size.

The trade-off is speed: integer Newton converges in a logarithmic number of steps, but each step computes `x ** (k - 1)`, which for very large `k` costs more than a floating-point estimate would. For the sizes where correctness matters, that cost is acceptable.

## Edge cases

`n = 0` returns `0` for any positive `k`. `k = 1` returns `n`. Negative `n` and non-positive `k` raise `ValueError`; non-integer arguments raise `TypeError`.

When `n` is one less than a perfect kth power, the floor is one less than the exact root. For example, `integer_nth_root(10**100 - 1, 10)` is `9999999999`, not `10**10`.
