'''

Client for liboqs_bench, a small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The client connects with a liboqs_bench server which measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

__init__.py for importing client package.
'''

__name__ = 'liboqs_bench_client'
__package__= 'liboqs_bench_client'
__version__ = '0.1.0'

from liboqs_bench_client.client import liboqs_bench_client