'''
Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Main entry point for user interaction. 

Calls the argument parser for command line arguments, passes them to liboqs_bench, and prints the results.
'''
import logging
_logger = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)

from oqs.oqs import get_enabled_kem_mechanisms as kem_schemes
from .liboqs_bench import liboqs_bench

from .argument_parser import ArgumentParser

def main():
    argparser = ArgumentParser()
    arguments = argparser.parser.parse_args()

    if arguments.debug:
        logging.captureWarnings(False)
        logging.getLogger('oqs.oqs').disabled = False
        _logger.setLevel(logging.DEBUG)

    if arguments.list_schemes:
        schemes_str = 'Supported KEM schemes:\n'
        for scheme_name in kem_schemes():
            schemes_str += f'\n"{scheme_name}"'
        print(schemes_str)

    else:
        results = liboqs_bench(arguments.alg, *arguments.scheme, iterations=arguments.iterations)
        for outer in results:
            print(outer[0])
            for result in outer[1].items():
                print(result)

if __name__ == '__main__':
    main()
