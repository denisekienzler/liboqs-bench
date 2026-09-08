''' Unit test file for client module.'''

import sys
import socket
import unittest
import threading
import pickle
import logging

sys.path.append("../src")

from liboqs_bench_client.client import liboqs_bench_client

_logger = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.WARNING)

HOST = '127.0.0.1'
PORT = 31031
req_data = {'alg':'ALGORITHM','schemes':('SCHEMES_TPL',),'iterations':1000}


server_event = threading.Event()
server_lock = threading.Lock()

class StubServer():
    '''Stub server class on localhost.'''

    def __init__(self):
        global server_event
        self.server_thread = threading.Thread(target=self._open_server)
        server_event.clear()
        self.server_thread.start()
        _logger.debug(f'{self.server_thread.name}: Started server thread')

    def _open_server(self):
        '''Stub server function on localhost.'''
        global server_event
        with socket.socket() as soc:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            with server_lock:
                soc.bind((HOST, PORT))
                soc.listen()
                _logger.debug(f'{self.server_thread.name}: Listening on stub server')
                while True:
                    _logger.debug(f'{self.server_thread.name}: Accepting connections')
                    server_event.set()
                    conn,addr = soc.accept()
                    _logger.debug(f'{self.server_thread.name}: Connection accepted')
                    with conn:
                        req = conn.recv(1024)
                        _logger.debug(f'{self.server_thread.name}: Request received')
                        if req == b'SERVER_SHUTDOWN':
                            _logger.debug(f'{self.server_thread.name}: Shutdown signal received')
                            break
                        elif isinstance(req, bytes):
                            conn.sendall(req)
                            _logger.debug(f'{self.server_thread.name}: Sent back copy of {req}')
                        else:
                            conn.sendall(pickle.dumps(False))
                            _logger.debug(f'{self.server_thread.name}: Sent False')
                _logger.debug(f'{self.server_thread.name}: Shutdown')

    def close_server(self):
        with socket.socket() as cli:
            server_event.wait()
            cli.connect((HOST, PORT))
            cli.sendall(b'SERVER_SHUTDOWN')
            _logger.debug(f'{self.server_thread.name}: Sent shutdown signal')

class TestClientNoArgument(unittest.TestCase):
    '''Test class for no argument passed.'''

    @classmethod
    def setUpClass(cls):
        cls.server = StubServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close_server()

    def test_no_argument(self):
        '''No argument returns doc string.'''
        server_event.wait()
        self.assertEqual(liboqs_bench_client(),liboqs_bench_client.__doc__)


class TestClientHostArgument(unittest.TestCase):
    '''Test class on host argument.'''

    @classmethod
    def setUpClass(cls):
        cls.server = StubServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close_server()

    def test_valid_true_IP(self):
        '''Valid and right IPv4 host argument sends request to server.'''
        server_event.wait()
        self.assertEqual(liboqs_bench_client(HOST, PORT, 'ALGORITHM','SCHEMES_TPL'), req_data)

    def test_valid_false_IPv4(self):
        '''Valid but false IPv4 address raises NoServerError (ConnectionRefusedError).'''
        args = {}
        args['IPv4_str_wlp'] = '192.168.178.47'
        args['IPv4_str_virbr'] = '192.168.122.1'

        for arg in args.values():
            server_event.wait()
            with self.subTest():
                self.assertRaises(ConnectionRefusedError, liboqs_bench_client, arg, PORT ,'ALGORITHM', 'SCHEMES_TPL', iterations=1000)

    def test_valid_IPv6(self):
        '''Valid IPv6 address raises IPv6Error (socket.gaierror).'''
        args_v6 = {}
        args_v6['IPv6_comp_lowest'] = '::1'
        args_v6['IPv6_comp_low'] = '::2'
        args_v6['IPv6_comp_mid'] = '::48d6:ffff:ffff'
        args_v6['IPv6_short_low'] = '0:0:0:0:0:0:0:0'
        args_v6['IPv6_short_mid'] = '0:0:0:0:ffff:5a68:c4a8:7a00'
        args_v6['IPv6_exp_low'] = '0000:0000:0000:0000:0000:0000:0000:0000'
        args_v6['IPv6_exp_mid'] = '0000:ffff:0000:0000:0000:2f4e:c4a8:7a00'
        args_v6['IPv6_exp_high'] = 'ffff:08e3:ffff:ffff:ffff:ffff:ffff:ffff'

        for arg in args_v6.values():
            server_event.wait()
            with self.subTest():
                self.assertRaises(socket.gaierror, liboqs_bench_client, arg, PORT, 'ALGORITHM', 'SCHEMES_TPL', iterations=1000)

    def test_no_help_or_IP(self):
        '''Invalid host address raises InvalidHostError (TypeError, ValueError).'''
        args = {}
        args['neg'] = -1
        args['str'] = 'string'
        args['float'] = 4.5
        args['int'] = 246548
        args['True'] = True
        args['False'] = False
        for arg in args.values():
            server_event.wait()
            with self.subTest(arg=arg):
                self.assertRaises((TypeError, ValueError), liboqs_bench_client, arg, PORT, 'ALGORITHM', 'SCHEMES_TPL', iterations=1000)

class TestClientPortArgument(unittest.TestCase):
    '''Test class for port argument.'''

    @classmethod
    def setUpClass(cls):
        cls.server = StubServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close_server()

    def test_valid_right_port(self):
        '''Valid (registered) and right port sends request to server.'''
        server_event.wait()
        self.assertEqual(liboqs_bench_client(HOST, PORT, 'ALGORITHM', 'SCHEMES_TPL', iterations=1000), req_data)

    def test_valid_false_port(self):
        '''Valid (registered) but false port returns NoServerError (ConnectionRefusedError).'''
        port = 31030
        server_event.wait()
        self.assertRaises(ConnectionRefusedError, liboqs_bench_client, HOST, port, 'ALGORITHM', 'SCHEMES_TPL', iterations=1000)

    def test_invalid_port(self):
        '''Invalid (not registered) port raises ValueError.'''
        ports = [-1, 1023, 49151]
        for port in ports:
            server_event.wait()
            self.assertRaises(ValueError, liboqs_bench_client, HOST, port, 'ALGORITHM', 'SCHEMES_TPL', iterations=1000)

    def test_no_int_port(self):
        '''Other type than integer as port returns InvalidPortError (ValueError).'''
        args = {}
        args['string'] = 'string'
        args['bool'] = True
        args['float'] = 1024.5
        for arg in args.values():
            server_event.wait()
            with self.subTest(arg=arg):
                self.assertRaises(ValueError, liboqs_bench_client, HOST, arg, 'ALGORITHM', 'SCHEMES_TPL', iterations=1000)


class TestClientAlgorithmArgument(unittest.TestCase):
    '''Test class for algorithm argument.'''

    @classmethod
    def setUpClass(cls):
        cls.server = StubServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close_server()

    def test_none_algorithm(self):
        '''Passing None to algorithm argument returns docstring.'''
        server_event.wait()
        self.assertEqual(liboqs_bench_client(HOST, PORT, None), liboqs_bench_client.__doc__)

    def test_valid_algorithm(self):
        '''Passing a valid algorithm to argument returns valid request.'''
        _local_req = req_data.copy()
        args = ['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']
        for arg in args:
            _local_req['alg'] = arg
            server_event.wait()
            with self.subTest(arg=arg):
                self.assertEqual(liboqs_bench_client(HOST, PORT, arg, 'SCHEMES_TPL', iterations=1000), _local_req)

    def test_invalid_algorithm(self):
        '''Passing an invalid algorithm results in a valid request (Error handling on server side).'''
        _local_req = req_data.copy()
        args = {}
        args['str'] = 'string'
        args['int'] = 55
        args['float'] = 4.5
        args['bool'] = False
        for arg in args.values():
            _local_req['alg'] = arg
            server_event.wait()
            with self.subTest(arg=arg):
                self.assertEqual(liboqs_bench_client(HOST, PORT, arg, 'SCHEMES_TPL', iterations=1000), _local_req)


class TestClientSchemesArgument(unittest.TestCase):

    '''Test class for schemes argument.'''

    @classmethod
    def setUpClass(cls):
        cls.server = StubServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close_server()

    def test_no_schemes(self):
        '''Passing no scheme argument results in valid request (error handling in server).'''
        _local_req = req_data.copy()
        _local_req['schemes'] = ()
        server_event.wait()
        self.assertEqual(liboqs_bench_client(HOST, PORT, 'ALGORITHM', iterations=1000), _local_req)

    def test_str_schemes(self):
        '''Passing one or more strings as (in-)valid scheme arguments results in valid request (error handling in server).'''
        _local_req = req_data.copy()
        str_list = []
        for i in range(100):
            str_list.append('scheme')
            str_tpl = tuple(str_list)
            _local_req['schemes'] = str_tpl
            server_event.wait()
            with self.subTest():
                _logger.debug(f'Passing {i} strings to "schemes" argument.')
                self.assertEqual(liboqs_bench_client(HOST, PORT, 'ALGORITHM', *str_tpl, iterations=1000), _local_req)

    def test_invalid_schemes(self):
        '''Passing non string type as schemes argument returns valid request (error handling at server).'''
        _local_req = req_data.copy()
        args = {}
        args['int'] = 55
        args['float'] = 5.5
        args['bool'] = False
        for arg in args.values():
            schemes_tpl = (arg,)
            _local_req['schemes'] = schemes_tpl
            server_event.wait()
            with self.subTest():
                self.assertEqual(liboqs_bench_client(HOST, PORT, 'ALGORITHM', *schemes_tpl, iterations=1000), _local_req)


class TestClientIterationsArgument(unittest.TestCase):

    '''Test class for iterations argument.'''

    @classmethod
    def setUpClass(cls):
        cls.server = StubServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close_server()

    def test_valid_iterations(self):
        '''Positive integer to iterations argument results in valid request to server.'''
        _local_req = req_data.copy()
        args = [1, 100, 1000, 10000]
        for arg in args:
            if arg > 1000: arg = 1000
            _local_req['iterations'] = arg
            server_event.wait()
            with self.subTest(arg=arg):
                self.assertEqual(liboqs_bench_client(HOST, PORT, 'ALGORITHM', 'SCHEMES_TPL', iterations=arg), _local_req)

    @unittest.expectedFailure
    def test_invalid_iterations(self):
        '''Invalid iterations argument raises Exception.'''
        args = {}
        args['neg'] = -1
        args['str'] = 'string'
        args['float'] = 4.5
        args['bool'] = False
        for arg in args.values():
            server_event.wait()
            with self.subTest(arg=arg):
                self.assertRaises(Exception, liboqs_bench_client, HOST, PORT, 'ALGORITHM', 'SCHEMES_TPL', iterations=arg)

if __name__ == '__main__':
    unittest.main()
