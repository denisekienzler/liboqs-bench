'''Command line argument parser.'''

import logging
_logger = logging.getLogger('__main__.' + __name__)

from liboqs_bench.__init__ import __version__
from oqs.oqs import get_enabled_kem_mechanisms as kem_schemes
import argparse

class ArgumentParser():

    '''
    Class for parsing command line arguments to be called by __main__.py.
    '''
    def __init__(self):
        global __version__
        alg_choices=['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']
        scheme_choices=[scheme_name for scheme_name in kem_schemes()].append('all')

        self.parser = argparse.ArgumentParser(prog='liboqs_bench', 
                                              description='Small Python utility benchmarking PQC KEM algorithms and \
                                              schemes from the liboqs-python library. The program measures each \
                                              algorithm step separately for as many schemes as required by running \
                                              the step a specified number of iterations for five trials in total. \
                                              It then chooses the fastest trial and calculates the average.')
        self.parser.add_argument('alg',  metavar='algorithm', choices=alg_choices, nargs='?',
                            help=f'the desired algorithm step or "complete": {alg_choices}')
        self.parser.add_argument('scheme', nargs='*',
                            choices=[scheme_name for scheme_name in kem_schemes()].append('all'),
                           help=f'at least one KEM scheme or "all" - for full list use -l option')
        self.parser.add_argument('-i', '--iterations', type=int, default=1000, metavar='int', 
                                 help='set the number of iterations of each benchmark trial (default=1000)')
        self.parser.add_argument('-l', '--list-schemes', action='store_true', help='print the full list of supported KEM schemes')
        self.parser.add_argument('-d', '--debug', action='store_true', help='set log level to DEBUG and enable oqs warnings and logs (STUB FUNCTIONALITY)')
        self.parser.add_argument('-v', '--version', action='version', version=f'%(prog)s-{__version__}')
