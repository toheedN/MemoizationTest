import datetime

hits = misses = 0
name = ""


def memoize(user_func, resolver=None, timeout=None):
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

    cache = {}

    # timeouts should be int or float and by default python timers are in Milliseconds
    if not (isinstance(timeout, int) or isinstance(timeout, float)):
        raise TypeError("timeout must be integer or float")
    else:
        timeout = datetime.timedelta(milliseconds=timeout)

    if resolver is not None and not hasattr(resolver, '__call__'):
        raise TypeError('unable to derive key with non-callable object ' + str(resolver))

    if not hasattr(user_func, '__call__'):
        raise TypeError("user_func cannot be a non-callable object")

    def memoize_cache_function(*args):
        global misses
        global hits
        global name
        resolved_key = str(args[0]) if resolver is None else resolver(*args)
        now = datetime.datetime.now()
        if resolved_key in cache and now - cache[resolved_key][0] <= timeout:
            hits += 1
            name = resolved_key
            print(f"cache {resolved_key} value is still valid Returning value {cache[resolved_key][1]} from cache")
            return cache[resolved_key][1]
        elif resolved_key in cache and now - cache[resolved_key][0] >= timeout:
            misses += 1
            name = resolved_key
            print(
                f"Deleting Cache Key {resolved_key} and Value{cache[resolved_key][1]} as timeout {cache[resolved_key][0]} has occurred")
            del cache[resolved_key]

        print("No cache entry found or cache has expired recalculating values")
        expensive_calc_values = user_func(*args)
        cache[resolved_key] = (now, expensive_calc_values)
        return expensive_calc_values

    return memoize_cache_function


def get_cache_stats():
    global hits
    global misses
    global name
    return {
        "cache": name,
        "hits": hits,
        "misses": misses,
    }
