import datetime
from time import perf_counter_ns
import Utils


def results(data):
    start = datetime.datetime.now()
    start1 = perf_counter_ns()
    prime = Utils.countPrimes(data)
    finish = datetime.datetime.now()
    finish1 = perf_counter_ns()

    results = {
        'primes':prime,
        'time_in_secs':(finish - start).total_seconds(),
        'time_in_ms':(finish1 - start1)/1000000
    }

    return results
