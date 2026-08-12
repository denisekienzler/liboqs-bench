'''
Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Command line argument parser.
'''

import logging
_logger = logging.getLogger(__name__)

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
        scheme_choices=[scheme_name for scheme_name in kem_schemes()]
        scheme_choices.append('all')
        self.parser = argparse.ArgumentParser(prog='liboqs_bench', 
                                              description='Small Python utility benchmarking PQC KEM algorithms and \
                                              schemes from the liboqs-python library. The program measures each \
                                              algorithm step separately for as many schemes as required by running \
                                              the step a specified number of iterations for five trials in total. \
                                              It then chooses the fastest trial and calculates the average.')
        self.parser.add_argument('alg',  metavar='algorithm', choices=alg_choices, nargs='?',
                            help=f'the desired algorithm step or "complete": {alg_choices}')
        self.parser.add_argument('scheme', nargs='*', choices=scheme_choices, metavar='schemes',
                           help=f'at least one KEM scheme or "all" - for full list use -l option')
        self.parser.add_argument('-d', '--debug', action='store_true', help='set log level to DEBUG and enable oqs warnings and logs (STUB FUNCTIONALITY)')
        self.parser.add_argument('-H', '--host', default='127.0.0.1', help='IP address of host server interface (127.0.0.1 by default)')
        self.parser.add_argument('-i', '--info', action='store_true', help='set log level to INFO and enable oqs warnings and logs (STUB FUNCTIONALITY)')
        self.parser.add_argument('-I', '--iterations', type=int, default=1000, metavar='int', 
                                 help='set the number of iterations of each benchmark trial (default=1000)')
        self.parser.add_argument('-l', '--list-schemes', action='store_true', help='print the full list of supported KEM schemes and exit')
        self.parser.add_argument('-P', '--port', type=int, default=31021, help='registered port (1024-49151) on which to expose service (default=31021)')
        self.parser.add_argument('-s', '--server', action='store_true', help='expose liboqs_bench as network service')
        self.parser.add_argument('-v', '--version', action='version', version=f'%(prog)s-{__version__}')