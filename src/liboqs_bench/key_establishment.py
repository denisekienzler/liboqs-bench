'''

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Module for server-side timed secret key establishment.
'''

# import timeit
import time
from typing import Callable
import logging
_logger = logging.getLogger(__name__)

from oqs import oqs

def timed_once(func: Callable) -> Callable:
    '''Method decorator function to benchmark time.'''
    def wrapper(self, *args, **kwargs):
        start = time.perf_counter_ns()
        cipher,secret = func(self, *args, **kwargs)
        stop = time.perf_counter_ns()
        alg_time = start - stop
        return cipher,alg_time
    return wrapper

class _ServerKeyEstablishment(oqs.KeyEncapsulation):
    '''
    Class for server-side secret key establishment using the client-provided encapsulation key.
    '''
    def __init__(self, scheme: str) -> None:
        self.server_party = self.KeyEncapsulation(scheme)

    @timed_once
    def encapsulate_secret(self, encap_key: bytes) -> tuple[bytes,bytes]:
        '''
        Function encapsulates a random secret with client-provided encapsulation key and returns a tuple with the cipher (encapsulated secret) and secret as byte objects.
        '''
        return self.server_party.encap_secret(encap_key)

# class ServerKeyEstablishmentTimer(timeit.Timer):
#     '''Class to time encapsulation.'''
#
#     def __init__(self, scheme: str, encap_key: bytes) -> None:
#         super().__init__(stmt=f"server.encapsulate_secret({encap_key})", setup=f"server = _ServerKeyEstablishment({scheme})",
#                          timer=time.perf_counter_ns, globals=globals())
#
#     def cipher_time(self):
#         try:
#             return self.timeit(number=1)
#         except oqs.MechanismNotSupportedError:
#             raise UnsupportedSchemeError(self.scheme)

# NEED TO FIND WAY TO RETURN RESULT AS WELL
