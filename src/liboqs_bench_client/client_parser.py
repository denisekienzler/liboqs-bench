'''
Client for liboqs_bench, a small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The client connects with a liboqs_bench server which measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Client command line argument parser.
'''

import argparse
import logging
_logger = logging.getLogger(__name__)

from liboqs_bench_client.__init__ import __version__

class ClientParser():

    '''
    Class for parsing command line arguments to be called by __main__.py.
    '''
    def __init__(self):
        global __version__
        alg_choices=['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']
        self.parser = argparse.ArgumentParser(prog='liboqs_bench_client', 
                                              description='Client for liboqs_bench, a small Python utility \
                                              benchmarking PQC KEM algorithms and schemes from the liboqs-python \
                                              library. The client connects with a liboqs_bench server which measures each \
                                              algorithm step separately for as many schemes as required by running \
                                              the step a specified number of iterations for five trials in total. \
                                              It then chooses the fastest trial and calculates the average.')
        self.parser.add_argument('alg',  metavar='algorithm', choices=alg_choices, nargs='?',
                            help=f'the desired algorithm step or "complete": {alg_choices}')
        self.parser.add_argument('scheme', nargs='*', metavar='schemes',
                           help=f'at least one KEM scheme or "all" - for full list use -l option')
        self.parser.add_argument('-d', '--debug', action='store_true', help='set log level to DEBUG (STUB FUNCTIONALITY)')
        self.parser.add_argument('-H', '--host', default='127.0.0.1', help='IP address of host server interface (127.0.0.1 by default)')
        self.parser.add_argument('-i', '--info', action='store_true', help='set log level to INFO (STUB FUNCTIONALITY)')
        self.parser.add_argument('-I', '--iterations', type=int, default=1000, metavar='int', 
                                 help='set the number of iterations of each benchmark trial (default=1000)')
        self.parser.add_argument('-l', '--list-schemes', action='store_true', help='print the full list of supported KEM schemes and exit')
        self.parser.add_argument('-P', '--port', type=int, default=31021, help='registered port (1024-49151) on which to expose service (default=31021)')
        self.parser.add_argument('-v', '--version', action='version', version=f'%(prog)s-{__version__}')