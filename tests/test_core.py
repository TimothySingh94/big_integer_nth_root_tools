import unittest

from big_integer_nth_root_tools import integer_nth_root


class TestIntegerNthRoot(unittest.TestCase):
    def test_square_roots(self):
        self.assertEqual(integer_nth_root(0, 2), 0)
        self.assertEqual(integer_nth_root(1, 2), 1)
        self.assertEqual(integer_nth_root(2, 2), 1)
        self.assertEqual(integer_nth_root(3, 2), 1)
        self.assertEqual(integer_nth_root(4, 2), 2)
        self.assertEqual(integer_nth_root(8, 2), 2)
        self.assertEqual(integer_nth_root(9, 2), 3)
        self.assertEqual(integer_nth_root(10, 2), 3)

    def test_cube_roots(self):
        self.assertEqual(integer_nth_root(26, 3), 2)
        self.assertEqual(integer_nth_root(27, 3), 3)
        self.assertEqual(integer_nth_root(28, 3), 3)
        self.assertEqual(integer_nth_root(63, 3), 3)
        self.assertEqual(integer_nth_root(64, 3), 4)

    def test_k_equals_one(self):
        self.assertEqual(integer_nth_root(123456789, 1), 123456789)

    def test_zero(self):
        self.assertEqual(integer_nth_root(0, 1), 0)
        self.assertEqual(integer_nth_root(0, 10), 0)

    def test_one(self):
        self.assertEqual(integer_nth_root(1, 1), 1)
        self.assertEqual(integer_nth_root(1, 100), 1)

    def test_large_power_of_ten(self):
        # 10**100 has an exact 10th root of 10**10.
        self.assertEqual(integer_nth_root(10**100, 10), 10**10)
        # One less than a perfect power should floor to the previous integer.
        self.assertEqual(integer_nth_root(10**100 - 1, 10), 10**10 - 1)

    def test_large_non_perfect_power(self):
        n = 2**1000
        # 2**1000 = (2**10)**100, so the 100th root is exactly 2**10.
        self.assertEqual(integer_nth_root(n, 100), 2**10)
        # Adding one keeps the floor at the same value.
        self.assertEqual(integer_nth_root(n + 1, 100), 2**10)

    def test_high_order_root(self):
        # 2**1000 has a 1000th root of 2.
        self.assertEqual(integer_nth_root(2**1000, 1000), 2)
        self.assertEqual(integer_nth_root(2**1000 - 1, 1000), 1)

    def test_negative_n_rejected(self):
        with self.assertRaises(ValueError):
            integer_nth_root(-1, 2)

    def test_non_positive_k_rejected(self):
        with self.assertRaises(ValueError):
            integer_nth_root(10, 0)
        with self.assertRaises(ValueError):
            integer_nth_root(10, -1)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            integer_nth_root(10.0, 2)
        with self.assertRaises(TypeError):
            integer_nth_root(10, 2.0)

    def test_floor_property(self):
        # For a range of n and k, verify r**k <= n < (r+1)**k.
        for k in range(1, 8):
            for n in range(0, 200):
                r = integer_nth_root(n, k)
                self.assertLessEqual(r**k, n)
                self.assertLess(n, (r + 1) ** k)


if __name__ == "__main__":
    unittest.main()
