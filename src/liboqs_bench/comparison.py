'''

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Module containing benchmark classes for algorithms and schemes.
'''

import timeit
import time
import logging
_logger = logging.getLogger(__name__)

from oqs import oqs

from .custom_exceptions import *
from .schemes import *


class Benchmark(timeit.Timer):

    '''
    Benchmark class

    Constructor generates a benchmark instance from the timeit builtin and function benchmark() runs it five \
seperate times for a specified number of iterations.

    '''

    def __init__(self, alg:str, scheme:str):
        self.scheme = scheme
        super().__init__(stmt="bench.to_measure()", setup=f'bench = {alg}("{self.scheme}")', timer=time.perf_counter_ns,
                         globals=globals())

    def benchmark(self, iterations):
        try:
            return self.repeat(number=iterations)
        except oqs.MechanismNotSupportedError:
            raise UnsupportedSchemeError(self.scheme)


class Comparison():

    '''
    Comparison class

    The constructor generates two lists: one of the schemes to be benchmarked, one for the benchmark instances.

    The function compare() runs the benchmarks 5 times for a specified number of algorithm iterations (default 1000) 
    and returns a list containing a dictionary of scheme and lowest benchmark pairs.

    The lowest benchmark is chosen because they represent the lower bound. The result in seconds is the time the 
    scheme requires to compute the algorithm result for the speficied number of times.
    '''

    def __init__(self, alg:str, scheme:str, *schemes):
        self.alg = alg
        self.scheme_list = [scheme]
        self.scheme_list.extend([arg for arg in schemes])
        self.bench_list = [Benchmark(alg, self.scheme_list[i]) for i, _ in enumerate(self.scheme_list)]

    def compare(self, iterations)->tuple:
        try:
            compare_zip = zip([scheme for scheme in self.scheme_list],
                              [min(bench.benchmark(iterations))/iterations for bench in self.bench_list])
            return ((f'{self.alg} - average runtime in nanoseconds:',dict(compare_zip)))
        except (NameError, TypeError) as e:
            raise UnsupportedAlgorithmError(self.alg)


class ComparisonAllSchemes(Comparison):

    '''
    Convenience class for comparing all enabled schemes with each other.

    The constructor generates a list of all schemes and passes it to its parent class
    '''

    def __init__(self, alg:str):
        all_schemes = [scheme_ for scheme_ in oqs.get_enabled_kem_mechanisms()]
        super().__init__(alg, *all_schemes)


class ComparisonCompleteScheme:

    '''Convenience class for comparing complete schemes with all three algorithms\
and their total sum of at least one scheme.'''

    def __init__(self, *scheme):
        self.keygen = Comparison('KeyGeneration',*scheme)
        self.encap = Comparison('Encapsulation',*scheme)
        self.decap = Comparison('Decapsulation',*scheme)

    def compare_complete(self, iterations=1000):
        keygen_bench = self.keygen.compare(iterations)
        encap_bench = self.encap.compare(iterations)
        decap_bench = self.decap.compare(iterations)
        sum_list = []
        for i,_ in enumerate(keygen_bench[1]):
            sum_list.append(list(keygen_bench[1].values())[i] + list(encap_bench[1].values())[i] + list(decap_bench[1].values())[i])
        total_zip = zip(keygen_bench[1].keys(),sum_list)
        total_bench = ('Complete scheme - average runtime in nanoseconds:', dict(total_zip))
        return [keygen_bench, encap_bench, decap_bench, total_bench]


class CompleteComparison(ComparisonCompleteScheme):

    '''Convenience class for complete comparison of all schemes and all algorithms.'''

    def __init__(self):
        all_schemes = [scheme_ for scheme_ in oqs.get_enabled_kem_mechanisms()]
        super().__init__(*all_schemes)