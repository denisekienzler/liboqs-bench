'''
Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

Module for client-side timed secret key establishment.
'''

import logging
_logger = logging.getLogger(__name__)
_logger.debug(logging.getLogger())

import time
from typing import Callable
from functools import wraps

logging.captureWarnings(True)
logging.getLogger('oqs.oqs').disabled = True
from oqs import oqs

def timed_once(func: Callable) -> Callable:
    '''Method decorator function to one-time benchmark time.'''
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> tuple[bytes, int]:
        start = time.perf_counter_ns()
        _logger.debug(f'start: {start}, type: {type(start)}')
        key = func(self, *args, **kwargs)
        stop = time.perf_counter_ns()
        _logger.debug(f'stop: {stop}, type: {type(stop)}')
        alg_time = stop - start
        _logger.debug(f'alg_time: {alg_time}')
        return key,alg_time
    return wrapper

class ClientKeyEstablishment(oqs.KeyEncapsulation):
    '''Class to generate a client-side key pair and decapsulate a server-provided encapsulated secret (cipher) with the decapsulation key.'''

    @timed_once
    def generate_keys(self) -> bytes:
        return self.generate_keypair()

    @timed_once
    def decapsulate_cipher(self, server_cipher) -> bytes:
        return self.decap_secret(server_cipher)
