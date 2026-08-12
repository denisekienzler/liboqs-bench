'''
Client for liboqs_bench, a small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The client connects with a liboqs_bench server which measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Main entry point for user interaction. 

Calls the argument parser for command line arguments, passes them to liboqs_bench, and prints the results.
'''

import logging
_logger = logging.getLogger()
_handler = logging.StreamHandler()
_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)

from .client import liboqs_bench_client
from .client_parser import ClientParser

def main()->int:

    # Setup
    client_parser = ClientParser()
    arguments = client_parser.parser.parse_args()

    # Logging level
    if arguments.debug:
        logging.captureWarnings(False)
        _logger.setLevel(logging.DEBUG)

    elif arguments.info:
        logging.captureWarnings(False)
        _logger.setLevel(logging.INFO)
    
    # Handle missing argument by printing docstring and exit
    if arguments.alg == None:
        print(liboqs_bench_client.__doc__)
        return 0
    
    # List schemes and exit...
    if arguments.list_schemes:
        kem_schemes = liboqs_bench_client(arguments.host, arguments.port, 'schemes')
        print(kem_schemes)
        return 0
        
    # Or connect to server and run benchmark
    else:
        results = liboqs_bench_client(arguments.host, arguments.port, arguments.alg, *arguments.scheme, iterations=arguments.iterations)
        for outer in results:
            print(outer[0])
            for result in outer[1].items():
                print(f'"{result[0]}": {result[1]}')
        return 0

if __name__ == '__main__':
    main()
