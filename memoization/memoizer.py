import datetime

"""
/**
 * Creates a function that memoizes the result of func. If resolver is provided,
 * it determines the cache key for storing the result based on the arguments provided to the memorized function.
 * By default, the first argument provided to the memorized function is used as the map cache key. The memorized values
 * timeout after the timeout exceeds. The timeout is in defined in milliseconds.
 *
 * Example:
 * function addToTime(year, month, day) {
 *  return Date.now() + Date(year, month, day);
 * }
 *
 * const memoized = memoization.memoize(addToTime, (year, month, day) => year + month + day, 5000)
 *
 * // call the provided function cache the result and return the value
 * const result = memoized(1, 11, 26); // result = 1534252012350
 *
 * // because there was no timeout this call should return the memorized value from the first call
 * const secondResult = memoized(1, 11, 26); // secondResult = 1534252012350
 *
 * // after 5000 ms the value is not valid anymore and the original function should be called again
 * const thirdResult = memoized(1, 11, 26); // thirdResult = 1534252159271
 *
 * @param func      the function for which the return values should be cached
 * @param resolver  if provided gets called for each function call with the exact same set of parameters as the
 *                  original function, the resolver function should provide the memoization key.
 * @param timeout   timeout for cached values in milliseconds
 */
"""

# global variables to count number of his and misses
hits = misses = 0
name = ""

# Dict to maintain stats
cache_stats = {}


def memoize(user_func, resolver=None, timeout=None):
    cache = {}
    # timeouts should be int or float and by default python timers are in Milliseconds
    if not (isinstance(timeout, int) or isinstance(timeout, float)):
        raise TypeError("timeout must be integer or float")
    else:
        timeout = datetime.timedelta(milliseconds=timeout)

    if not hasattr(user_func, '__call__'):
        print("Raising TypeError : user_func cannot be a non-callable object")
        raise TypeError("user_func cannot be a non-callable object")

    if resolver is not None and not hasattr(resolver, '__call__'):
        print("Raising TypeError: unable to derive key with non-callable object " + str(resolver))
        raise TypeError('unable to derive key with non-callable object ' + str(resolver))

    def memoize_cache_function(*args, **kwargs):
        global misses
        global hits
        global name

        # Merge args and keyargs to generate the key
        cache_key_tmp = args
        if kwargs:
            for kwarg_ in kwargs.keys():
                cache_key_tmp += (kwarg_, kwargs[kwarg_])

        resolved_key = (str(cache_key_tmp[0])+"_" + user_func.__name__ if resolver is None else resolver(
            *cache_key_tmp))

        # get current for compare and timeout the existing entry
        now = datetime.datetime.now()
        if resolved_key in cache and now - cache[resolved_key][0] <= timeout:
            hits += 1
            print(
                f"Cache Key : {resolved_key} has not timedout yet, Returning value : {cache[resolved_key][1]} from cache")
            set_cache_stats(name)
            return cache[resolved_key][1]
        elif resolved_key in cache and now - cache[resolved_key][0] >= timeout:
            misses += 1
            print(
                f"Deleting Cache Key : {resolved_key} and Value : {cache[resolved_key][1]} as timeout : {cache[resolved_key][0]} has occurred")
            del cache[resolved_key]

        print("No cache entry found or cache has expired recalculating values")
        expensive_calc_values = user_func(*args)
        cache[resolved_key] = (now, expensive_calc_values)
        name = resolved_key
        set_cache_stats(name)
        return expensive_calc_values

    return memoize_cache_function


def set_cache_stats(name):
    """
    cache stats setter
    :param name:
    :return:
    """
    global hits
    global misses
    cache_stats[name] = {"hits": hits, "misses": misses}


def get_cache_stats():
    """
    Cache stats getter
    :return:
    """
    global cache_stats

    return cache_stats


def make_key(args, kwargs, kwargs_mark=(object(),)):
    """
    Make a cache key
    """

    try:
        hash_value = hash(key)
    except TypeError:  # process unhashable types
        return str(key)
    else:
        return HashedList(key, hash_value)
