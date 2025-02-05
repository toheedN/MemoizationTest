import os
import sys
import time
from time import sleep

import pytest

# Setup project paths
sys.path.append(os.getcwd())
sys.path.append("../")

# local imports
from memoization import memoizer
from memoization.memoizer import get_cache_stats


@pytest.fixture(autouse=True)
def reset_stats():
    """
    reset cache access stats for each case
    :return:
    """
    print("################# Pre-Test Conditions #####################")
    print("################### Resetting Stats #######################")
    memoizer.hits = 0
    memoizer.misses = 0
    memoizer.cache_stats = {}


def test_basic_memoization_and_cache_timeout():
    """
    Basic test for momoization with timeout, we shall check both with and without timeout of the cache key
    """

    def sum_up_all_values(*args):
        """
        :param args: User input arguments for sum function
        :return: sum of input arguments
        """
        summed_value = 0
        for arg_ in list(args):
            summed_value += arg_
        return summed_value

    return_value = 10
    cache_hit_count = 2

    # List of numbers to add
    test_arg = [1, 2, 3, 4]
    memoized = memoizer.memoize(sum_up_all_values, timeout=2000)
    assert memoized(*test_arg) == return_value
    print(get_cache_stats())
    # access value twice and check cache his count hits should be = 2 and misses = 0 for the key
    assert memoized(*test_arg) == return_value
    assert memoized(*test_arg) == return_value
    localKey = str(test_arg[0]) + "_" + sum_up_all_values.__name__
    assert get_cache_stats()[localKey]["hits"] == cache_hit_count and get_cache_stats()[localKey]["misses"] == 0
    sleep(2)
    assert memoized(*test_arg) == return_value
    assert get_cache_stats()[localKey]["hits"] == cache_hit_count and get_cache_stats()[localKey]["misses"] == 1
    # Cache Stats should be 2 his and one miss
    print(f"Final Cache Stats : {get_cache_stats()}")


def test_memoization_first_func_param_as_key():
    """
    Memoization to ensure that first parameter is used as key.

    """
    return_value = 5

    def test_function(*args):
        return return_value

    memoized = memoizer.memoize(test_function, timeout=10000)

    test_arg = ["firstArgument", "secondArgument"]

    # perform the expensive operation
    assert memoized(*test_arg) == return_value

    # Ensure key from cache_stats should be the first argument of the  function we called
    assert test_arg[0] + "_" + test_function.__name__ in get_cache_stats()
    print(get_cache_stats())


def test_memoization_with_resolver():
    """
    Test memoization with resolver, resolver should provide the key for cache
    """

    def resolver_cb(*func_args, **kwargs):
        """
        resolver fucntion to resolve the key for momoization
        :param func_args: parameters provided to the function to momoize
        :return: returns the resolved key
        """

        resolved_key = "Sum = {}".format('_'.join(str(x) for x in list(func_args)))
        return resolved_key

    def test_function(*args, **kwargs):
        return "Some costly calculation to save with resolved key"

    memoized = memoizer.memoize(test_function, resolver_cb, 1000)

    test_arg = [1, 2, 3, 4, 6]

    assert memoized(*test_arg, userinput="test_kargs") == "Some costly calculation to save with resolved key"

    # Ensure the key is same as the key generated by resolver
    print(get_cache_stats())
    resolved_key_Local = resolver_cb(*test_arg)+"_userinput_test_kargs"
    assert resolved_key_Local in get_cache_stats()


def test_memoize_Different_data_types():
    """
    Test memoization with different data types e.g sting,tuple, dictionary.
    Note : All data types will be converted into sting to store as a key value pair
    """

    def test_function(*args):
        return "Some costly calculation to save with resolved key"

    memoized = memoizer.memoize(test_function, resolver=None, timeout=10000)

    # memoize list as a key
    test_arg = "stringAsAKey"
    assert memoized(test_arg) == "Some costly calculation to save with resolved key"

    # memoize list as a key
    test_arg = [1, 2, 3, 4, 6]
    assert memoized(test_arg) == "Some costly calculation to save with resolved key"

    # memoize list as a key
    test_arg = {"key": "testKey"}
    assert memoized(test_arg) == "Some costly calculation to save with resolved key"

    # Memoize tuple
    test_arg = ("key", "value")
    assert memoized(test_arg) == "Some costly calculation to save with resolved key"
    print(get_cache_stats())

    # ensure there are 4 entries in cache wit different data types
    assert len(get_cache_stats()) == 4


def test_memoization_with_non_callable_function():
    """
    This test should raise and exception that function(func) "user_func cannot be a non-callable object"
    :return:
    """

    def key_resolver(*args):
        """
        dummy resolver
        :return:
        """
        agrs_flat = ""
        for argskey in list(args):
            agrs_flat += str(argskey)

    test_function = "test string"

    # test_function is non-callable and without resolver, memorizer should raise
    with pytest.raises(TypeError, match="user_func cannot be a non-callable object"):
        memoizer.memoize(test_function, resolver=None, timeout=10000)

    # test_function is non-callable and with resolver is valid, memorizer should raise function type error
    with pytest.raises(TypeError, match="user_func cannot be a non-callable object"):
        memoizer.memoize(test_function, resolver=key_resolver, timeout=10000)


def test_memoization_with_non_callable_resolver():
    """
    This test should raise and exception that key resolver function "unable to derive key with non-callable object"
    :return:
    """
    test_result = 5
    key_resolver = "InvlidResolver"
    test_function = lambda key: test_result

    # resolver is non-callable , memorizer should raise
    with pytest.raises(TypeError, match=f'unable to derive key with non-callable object {key_resolver}'):
        memoizer.memoize(test_function, resolver=key_resolver, timeout=10000)


def test_memoization_with_invalid_timeout_value():
    """
    This test should raise and exception for timeout None or any other value than int or float"
    :return:
    """
    test_result = 5
    test_function = lambda key: test_result

    # timeout = 0 should raise exception
    with pytest.raises(TypeError, match='timeout must be a positive integer or float grater than 0'):
        memoizer.memoize(test_function, resolver=None, timeout=0)

    # timeout = None should raise exception
    with pytest.raises(TypeError, match='timeout must be a positive integer or float grater than 0'):
        memoizer.memoize(test_function, resolver=None, timeout=0)

    # timeout = some string value  should raise exception
    with pytest.raises(TypeError, match='timeout must be a positive integer or float grater than 0'):
        memoizer.memoize(test_function, resolver=None, timeout="somestring")


def test_full_example_memoization_fibonacci_sequence():
    """
    Performing end to end testing using famous example of fibonacci sequence
    we will measure benefits in terms of execution time using timeit library
    """
    func_results = 3524578
    feb_value = None
    feb_value_no_memo = None

    def fibonacci_without_memoizer(feb_n):
        """
        fibonacci series function with memoization
        :param feb_n:
        :return:
        """
        # check that the input is a positive integer
        if type(feb_n) != int:
            raise TypeError("n must be a positive integer")
        if feb_n < 1:
            raise ValueError("n must be a positive integer")

        if feb_n == 1:
            return 1
        elif feb_n == 2:
            return 1
        return fibonacci_without_memoizer(feb_n - 1) + fibonacci_without_memoizer(feb_n - 2)

    def fibonacci(feb_n):
        """
        fibonacci series function without memoiaton
        :param feb_n:
        """
        # check that the input is a positive integer
        if type(feb_n) != int:
            raise TypeError("n must be a positive integer")
        if feb_n < 1:
            raise ValueError("n must be a positive integer")

        if feb_n == 1:
            return 1
        elif feb_n == 2:
            return 1
        return memoized(feb_n - 1) + memoized(feb_n - 2)

    memoized = memoizer.memoize(fibonacci, None, timeout=10000)

    # Calculate Fibnocci for only 33 with memoization
    start_memo_feb = time.time()
    for n in range(1, 34):
        feb_value = memoized(n)

    assert feb_value == func_results
    end_memo_feb = time.time()
    total_time_consumed_with_memo = end_memo_feb - start_memo_feb
    print(f"Time Lapsed during the function: {round(total_time_consumed_with_memo, 2)} seconds")

    # Calculate Fibnocci for 33 without memoization
    start = time.time()
    for n in range(1, 34):
        feb_value_no_memo = fibonacci_without_memoizer(n)
    assert feb_value_no_memo == func_results
    end = time.time()
    print(f"Time Lapsed during the function: {round((end - start), 2)} seconds")

    print(
        f"Without memoization fibonacci sequence function Took: {round((end - start), 2) - round(total_time_consumed_with_memo, 2)}  more seconds")


if __name__ == '__main__':
    pytest.main(args=['-sv', os.path.abspath(__file__)])
