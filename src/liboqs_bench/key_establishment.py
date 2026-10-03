'''

Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Module for server-side timed secret key establishment.
'''

import logging
_logger = logging.getLogger(__name__)
_logger.debug(logging.getLogger())

import time
from typing import Callable
from functools import wraps

from oqs import oqs

def timed_once(func: Callable) -> Callable:
    '''Method decorator function to benchmark time.'''
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> tuple[bytes, int]:
        start = time.perf_counter_ns()
        _logger.debug(f'start: {start}, type: {type(start)}')
        cipher,secret = func(self, *args, **kwargs)
        stop = time.perf_counter_ns()
        _logger.debug(f'stop: {stop}, type: {type(stop)}')
        alg_time = stop - start
        _logger.debug(f'alg_time: {alg_time}')
        return cipher,alg_time
    return wrapper

class ServerKeyEstablishment(oqs.KeyEncapsulation):
    '''
    Class for server-side secret key establishment using the client-provided encapsulation key.
    '''
    def __init__(self, scheme: str) -> None:
        super().__init__(scheme)
        _logger.debug(f'self.__dict__: {self.__dict__}')

    @timed_once
    def encapsulate_secret(self, encap_key: bytes) -> tuple[bytes,bytes]:
        '''
        Function encapsulates a random secret with client-provided encapsulation key and returns a tuple with the cipher (encapsulated secret) and secret as byte objects.
        '''
        return self.encap_secret(encap_key)
