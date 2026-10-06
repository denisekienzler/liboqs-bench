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

from .key_establishment import ClientKeyEstablishment

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

    # Key Establishment
    if alg == 'KeyEstablishment':

        _logger.warning('Key establishment measures the time of each algorithm step only once and is not a statistical method.')

        # Generate dictionary of objects
        key_agent_dct = {}
        scheme_key_dct = {}
        for index,scheme in enumerate(schemes):
            session = f'session_no {index}'
            _logger.debug(f'schemes: {schemes}')
            _logger.debug(f'scheme: {scheme}')
            agent = ClientKeyEstablishment(scheme)
            encap_key, keygen_time = agent.generate_keys()
            key_agent_dct[session] = {'scheme':scheme, 'agent':agent, 'encap_key':encap_key, 'keygen_time':keygen_time}
            scheme_key_dct[session] = {'scheme':scheme, 'encap_key':encap_key}
        _logger.debug(f'key_agent_dct = {key_agent_dct}')
        _logger.debug(f'scheme_key_dct = {scheme_key_dct}')

        # Dictionary to serialize
        req_data = {'alg':alg,'scheme_key_dct':scheme_key_dct}
        _logger.debug(f'Data to serialize: {req_data}.')

    # Benchmark at server
    else:

        # Limit iterations to 1000
        if iterations > 1000:
            iterations = 1000
            _logger.warning('Number of iterations higher than 1000 disallowed, setting to 1000.')

        # Dictionary to serialize
        req_data = {'alg':alg,'schemes':schemes,'iterations':iterations}
        _logger.debug(f'Data to serialize: {req_data}.')

    # Serialize
    req_payload = pickle.dumps(req_data, pickle.HIGHEST_PROTOCOL)
    _logger.debug(f'Payload to send as request: {req_payload}.')

    # Open socket, connect, send, and receive
    with socket.socket() as s:
        _logger.info('Connecting to unsecured server.')
        s.connect((host,port))
        s.sendall(req_payload)
        _logger.info('Request sent.')
        resp_payload = s.recv(8192)
        _logger.info('Response received.')
    
    # Deserialize
    resp_data = pickle.loads(resp_payload)

    # Return results
    if alg == 'KeyEstablishment':
        for session in resp_data:
            key_agent_dct[session].update(resp_data[session])
            shared_key, decap_time = key_agent_dct[session]['agent'].decapsulate_cipher(key_agent_dct[session]['server_cipher'])
            key_agent_dct[session].update([('shared_key',shared_key), ('decap_time',decap_time)])
        _logger.debug(f'key_agent_dct = {key_agent_dct}')
        return key_agent_dct
    else:
        return resp_data
