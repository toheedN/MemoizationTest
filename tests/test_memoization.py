import os
import sys
from time import sleep
import pytest

# local imports
from memoization import memoizer
from memoization.memoizer import get_cache_stats

# Setup project paths
sys.path.append(os.getcwd())
sys.path.append("../")


def reset_stats():
    """
    reset cache access stats for each case
    :return:
    """
    memoizer.hits = 0
    memoizer.misses = 0
    memoizer.name = None


def test_basic_memoization_and_cache_timeout():
    """
    Basic test for momoization with timeout
    """
    return_value = 10
    test_function = lambda key: return_value

    memoized = memoizer.memoize(test_function, timeout=1000)
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value
    print(get_cache_stats())
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value
    print(get_cache_stats())
    sleep(1)
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value
    print(get_cache_stats())
    reset_stats()


def test_basic_memoization_and_cache_timeout_2():
    """
    Basic test for momoization with timeout
    """
    return_value = 10
    test_function = lambda key: return_value

    memoized = memoizer.memoize(test_function, timeout=1000)
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value
    print(get_cache_stats())
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value
    print(get_cache_stats())
    sleep(1)
    assert memoized("c544d3ae-a72d-4755-8ce5-d25db415b776") == return_value
    print(get_cache_stats())
    reset_stats()


if __name__ == '__main__':
    pytest.main(args=['-sv', os.path.abspath(__file__)])
