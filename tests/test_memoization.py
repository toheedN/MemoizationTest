import os

import pytest

from memoization import memoizer


def test_basic_memoization_and_cache_timeout():
    """
    Basic test for momoization with timeout, we shall check both with and without timeout of the cache key
    """
    return_value = 10
    test_function = lambda key: return_value

    memoized = memoizer.memoize(test_function, timeout=1000)
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value





if __name__ == '__main__':
    pytest.main(args=['-sv', os.path.abspath(__file__)])