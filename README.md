# Memoization

[![py|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://github.com/toheedN/MemoizationTest)

# What is Memoization.
A general introduction into memoization: https://en.wikipedia.org/wiki/Memoization

# Project Focus 
This project is basic implementation of Memoization in python. Project implements memoization with following features.With key focus on Testing/QA .
>Creates a function that memoizes the result of func. If resolver is provided,
>it determines the cache key for storing the result based on the arguments provided to the memorized function.
>By default, the first argument provided to the memorized function is used as the map cache key. The memorized values
>timeout after the timeout exceeds. The timeout is in defined in milliseconds.
>
>Example:
>function addToTime(year, month, day) {
> return Date.now() + Date(year, month, day);
>}
>
>const memoized = memoization.memoize(addToTime, (year, month, day) => year + month + day, 5000)
>
>// call the provided function cache the result and return the value
>const result = memoized(1, 11, 26); // result = 1534252012350
>
>// because there was no timeout this call should return the memorized value from the first call
>const secondResult = memoized(1, 11, 26); // secondResult = 1534252012350
>
>// after 5000 ms the value is not valid anymore and the original function should be called again
>const thirdResult = memoized(1, 11, 26); // thirdResult = 1534252159271
>
>@param func      the function for which the return values should be cached
>@param resolver  if provided gets called for each function call with the exact same set of parameters as the
>                 original function, the resolver function should provide the memoization key.
>@param timeout   timeout for cached values in milliseconds


# Key Features of Memoization

 - func(input fuction) is a cpu/memory expensive operation for which we want to perform memoization
  - Resolver (optional if provided shall be used for cache key derivation)
  - Memoization timeout  in MS(millisconds)

# Good to have (Not part of this project scope)

  - Impliment thread based timouts and cache clear functionality
  - Update the memoization/cache function to be thtead safe(current implimentation is not thread safe)
  - Support can be added to Limit the cache size with a user define value

# Test cases to cover all funcationality
| Test Case Name | Description |
| - | - |
| Test basic memoization with timeout | We should be able to memoize and read cache if user func is called within before timeout and we should perform the func call again if cache value has timed out |
| Test basic memoization without resolver | This test should memoize the function results based on first parameter of user function,upon calling it should recover the value if timeout has not exceeded yet|
| Memoize Different data type | Memoization should be able to use differnt data types(keys) to memoize int,float,sting,dict should be supported|
| Test basic memoization with resolver | We should provide the resolver function which will provide the cache key and recover the value based on the resover |
| Test memoization timeout | This test covers different scenarios of timeouts parameter for memoiation which includes negetive testing as well|
| Test memoization with non-callable function | This test should raise and exception that function(func) "user_func cannot be a non-callable object" |
| Test memoization with non-callable resolver | This test should raise and exception that key resolver function "unable to derive key with non-callable object" |
| Test full example memoization fibonacci sequenc| Performing end to end testing using famous example of fibonacci sequence we will measure benefits in terms of execution time using timeit library|



### Tech

This Memoization project is based on python and uses following libraries

* [pytest] - A test framework for python!
* [datetime] - Default python library for time and date


### Test execution instructions

Memoization_tests requires [Python](https://www.python.org/downloads/) 3+ to run.

Install pytest:
```
pip install pytest
```

Download the source code from github [Memoization](https://github.com/toheedN/MemoizationTest/archive/main.zip) as a zip or using command.


Get the source Code :
```
git clone https://github.com/toheedN/MemoizationTest.git
```

```sh
$ cd MemoizationTest
$ python python tests\test_memoization.py
```
License
----

MIT


[pytest]: <https://docs.pytest.org/en/stable/>
[datetime]: <https://docs.python.org/3/library/datetime.html>
  
  
