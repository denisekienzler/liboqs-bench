'''
Client for liboqs_bench, a small Python utility benchmarking PQC KEM algorithms and \
schemes from the liboqs-python library. The client connects with a liboqs_bench server which measures each \
algorithm step separately for as many schemes as required by running \
the step a specified number of iterations for five trials in total. \
It then chooses the fastest trial and calculates the average.

TCP client.
'''

import ipaddress
import socket
import pickle
import logging
_logger = logging.getLogger(__name__)

def liboqs_bench_client(host:str='help', port:int=31021, alg=None, *schemes, iterations:int=1000):
    '''
Usage:

liboqs_bench_client({'help'|host} [,port] [,alg] [,scheme1[,scheme2[,scheme3,...]]] [,iterations=int])

Client for liboqs_bench, a small Python utility \
benchmarking PQC KEM algorithms and schemes from the \
liboqs-python library. The client connects with a \
liboqs_bench server which measures each algorithm \
step separately for as many schemes as required by \
running the step a specified number of iterations \
for five trials in total. It then chooses the \
fastest trial and calculates the average.    

Usage is as follows:

First two arguments are host and port address of the server.

Then comes the algorithm step: "KeyGeneration", "Encapsulation", "Decapsulation", or "complete".

Afterwards as many scheme names as desired can be provided as positional arguments or the argument "all" in order to compare all schemes with each other.

Finally, the user can provide an integer as keyword argument "iterations" to specify the number of iterations each benchmark round should use. The default number is 1000.

For help, the user can pass as the first argument "help", which prints out this docstring.
    ''' 

    # Help
    if host == 'help' or alg == None:
        return liboqs_bench_client.__doc__

    # Check network address
    ipaddress.ip_address(host)
    if port not in range(1024,49151):
        raise ValueError(f'{port} not in range of registered ports 1024-49151')
    _logger.debug('Network address legitimate.')

    # Limit iterations to 1000
    if iterations > 1000:
        iterations = 1000
        _logger.warning('Number of iterations higher than 1000 disallowed, setting to 1000.')
    

    # Serialize
    req_data = {'alg':alg,'schemes':schemes,'iterations':iterations}
    _logger.debug(f'Data to serialize: {req_data}.')
    req_payload = pickle.dumps(req_data, pickle.HIGHEST_PROTOCOL)
    _logger.debug(f'Payload to send as request: {req_payload}.')

    # Open socket, connect, send, and receive
    with socket.socket() as s:
        _logger.info('Connecting to unsecured server.')
        s.connect((host,port))
        s.sendall(req_payload)
        _logger.info('Request sent.')
        resp_payload = s.recv(4096)
        _logger.info('Response received.')
    
    # Deserialize
    resp_data = pickle.loads(resp_payload)

    # Return results
    return resp_data