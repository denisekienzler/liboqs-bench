'''

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

__init__.py for importing package.
'''

__name__ = 'liboqs_bench'
__package__= 'liboqs_bench'
__version__ = '0.2.1'

# Capture warnings and and disable logging from oqs library
import logging
logging.captureWarnings(True)
logging.getLogger('oqs.oqs').disabled = True

from liboqs_bench.bench import liboqs_bench