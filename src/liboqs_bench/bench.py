'''

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Main module containing benchmark classes for algorithms and schemes as well as interactive function.
'''

import timeit
import time
import logging
_logger = logging.getLogger('__main__.' + __name__)

from oqs import oqs

from .custom_exceptions import *
from .schemes import *


class _Benchmark(timeit.Timer):

    '''
    _Benchmark class

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


class _Comparison():

    '''
    _Comparison class

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
        self.bench_list = [_Benchmark(alg, self.scheme_list[i]) for i, _ in enumerate(self.scheme_list)]

    def compare(self, iterations)->tuple:
        try:
            compare_zip = zip([scheme for scheme in self.scheme_list],
                              [min(bench.benchmark(iterations))/iterations for bench in self.bench_list])
            return ((f'{self.alg} - average runtime in nanoseconds:',dict(compare_zip)))
        except (NameError, TypeError) as e:
            raise UnsupportedAlgorithmError(self.alg)


class _ComparisonAllSchemes(_Comparison):

    '''
    Convenience class for comparing all enabled schemes with each other.

    The constructor generates a list of all schemes and passes it to its parent class
    '''

    def __init__(self, alg:str):
        all_schemes = [scheme_ for scheme_ in oqs.get_enabled_kem_mechanisms()]
        super().__init__(alg, *all_schemes)


class _ComparisonCompleteScheme:

    '''Convenience class for comparing complete schemes with all three algorithms\
and their total sum of at least one scheme.'''

    def __init__(self, *scheme):
        self.keygen = _Comparison('KeyGeneration',*scheme)
        self.encap = _Comparison('Encapsulation',*scheme)
        self.decap = _Comparison('Decapsulation',*scheme)

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


class _CompleteComparison(_ComparisonCompleteScheme):

    '''Convenience class for complete comparison of all schemes and all algorithms.'''

    def __init__(self):
        all_schemes = [scheme_ for scheme_ in oqs.get_enabled_kem_mechanisms()]
        super().__init__(*all_schemes)


def liboqs_bench(alg:str, *schemes, iterations:int=1000):

    '''
Usage: liboqs_bench({'help'|'schemes'|'server'|algorithm} [,host,port] [,scheme1[,scheme2[,scheme3,...]]] [,iterations=int])

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Main function for interactive usage, calls classes according to arguments provided.

Common usage is as follows:

First argument is the algorithm step: "KeyGeneration", "Encapsulation", "Decapsulation", or "complete".

After the first argument, as many scheme names as desired can be provided as positional arguments or
the argument "all" in order to compare all schemes with each other.

Finally, the user can provide an integer as keyword argument "iterations" to specify the number of 
iterations each benchmark round should use. The default number is 1000.

For help, the user can pass as the first argument "help", which prints out this docstring, or "schemes", 
which returns a list of supported KEM schemes.

In order to start an unencrypted server, type 'server' as the first argument, followed by a host and port number.
    '''

    # Limit iterations to 1000
    if iterations > 1000:
        iterations = 1000
        _logger.warning('Number of iterations higher than 1000 disallowed, setting to 1000.')

    
    match alg:
        case 'help':
            return liboqs_bench.__doc__

        case 'schemes':
            schemes_str = 'Supported KEM schemes:\n'
            for scheme_name in oqs.get_enabled_kem_mechanisms():
                schemes_str += f'\n"{scheme_name}"'
            return schemes_str

        case 'server':
            # Import only when required to avoid circular import
            from .server import liboqs_bench_server
            if schemes:
                host,port = schemes[0],schemes[1]
            else:
                host,port = '127.0.0.1',31021
            liboqs_bench_server(host,port)
            
        case 'complete':
            try:
                if schemes[0] == 'all':
                    
                    # Limit iterations to 100
                    if iterations > 100:
                        iterations = 100
                        _logger.warning('Number of iterations higher than 100 disallowed for all schemes, setting to 100.')

                    return _CompleteComparison().compare_complete(iterations)

                else:
                    return _ComparisonCompleteScheme(*schemes).compare_complete(iterations)

            except IndexError:
                raise NoSchemeProvidedError
            

        case _:
            try:

                if schemes[0] == 'all':
                    
                    # Limit iterations to 100
                    if iterations > 100:
                        iterations = 100
                        _logger.warning('Number of iterations higher than 100 disallowed for all schemes, setting to 100.')
                    
                    return [_ComparisonAllSchemes(alg).compare(iterations)]
                else:
                    return [_Comparison(alg, *schemes).compare(iterations)]

            except IndexError:
                raise NoSchemeProvidedError        
