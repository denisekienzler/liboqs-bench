'''

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Main module containing interactive liboqs_bench function.
'''

import logging
_logger = logging.getLogger(__name__)

from oqs import oqs

from .custom_exceptions import *
from .comparison import *

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

                    return CompleteComparison().compare_complete(iterations)

                else:
                    return ComparisonCompleteScheme(*schemes).compare_complete(iterations)

            except IndexError:
                raise NoSchemeProvidedError
            

        case _:
            try:

                if schemes[0] == 'all':
                    
                    # Limit iterations to 100
                    if iterations > 100:
                        iterations = 100
                        _logger.warning('Number of iterations higher than 100 disallowed for all schemes, setting to 100.')
                    
                    return [ComparisonAllSchemes(alg).compare(iterations)]
                else:
                    return [Comparison(alg, *schemes).compare(iterations)]

            except IndexError:
                raise NoSchemeProvidedError        
