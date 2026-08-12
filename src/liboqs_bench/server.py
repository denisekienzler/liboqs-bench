'''
Small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The program measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

TCP server.
'''

import ipaddress
import socket
import pickle
import logging
_logger = logging.getLogger(__name__)

from .bench import liboqs_bench
from .custom_exceptions import *

def liboqs_bench_server(host, port):

    # Check network address
    ipaddress.ip_address(host)
    if port not in range(1024,49151):
        raise ValueError(f'{port} not in range of registered ports 1024-49151')
    _logger.debug('Network address legitimate.')

    with socket.socket() as s:
        print(f'Starting unsecured server with endpoint at {host}:{port}...')
        s.bind((host, port))
        s.listen()
        while True:
            _logger.info('Accepting connections...')
            conn,addr = s.accept()
            _logger.info(f'Connected to by {addr}.')
            with conn:
                req_payload = conn.recv(1024)
                _logger.debug(f'Request received by {addr}')
                req_data = pickle.loads(req_payload)
                _logger.debug('Deserialized request. Sending data to liboqs_bench function ...')
                try:
                    resp_data = liboqs_bench(req_data['alg'], *req_data['schemes'], iterations=req_data['iterations'])
                    _logger.debug('Received data from liboqs_bench. Serializing and sending ...')
                except UnsupportedAlgorithmError as a:
                    _logger.warning('UnsupportedAlgorithmError')
                    resp_data = a.args[0]
                except UnsupportedSchemeError as c:
                    _logger.warning('UnsupportedSchemeError')
                    resp_data = c.args[0]
                except NoSchemeProvidedError as p:
                    _logger.warning('NoSchemeProvidedError')
                    resp_data = p.args[0]
                resp_payload = pickle.dumps(resp_data, pickle.HIGHEST_PROTOCOL)
                conn.sendall(resp_payload)
            _logger.info(f'Connection by {addr} closed.')