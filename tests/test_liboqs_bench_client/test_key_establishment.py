'''Unit test script for client key establishment module.'''

import sys
import logging
import unittest
from typing import Callable

_logger = logging.getLogger()
_handler = logging.StreamHandler()
_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.INFO)

logging.captureWarnings(True)
logging.getLogger('py.warnings').disabled = True
logging.getLogger('oqs.oqs').disabled = True

sys.path.insert(0,"../src")

_logger.debug(f'Root logger: {logging.getLogger()}')
_logger.debug(f'sys.path: {sys.path}')

from liboqs_bench_client.key_establishment import *

_logger.debug(f'Root logger: {logging.getLogger()}')

class TestTimedOnceDec(unittest.TestCase):
    '''Test class for decorator for timing once.'''

    def test_timed_once(self):
        self.assertIsInstance(timed_once(lambda x:x), Callable)

class TestClientKeyGeneration(unittest.TestCase):
    '''Test class for key generation function in client key establishment class.'''

    def setUp(self):
        self.key_agent = ClientKeyEstablishment('ML-KEM-512')

    def tearDown(self):
        del self.key_agent

    def test_generate_without_dec(self):
        self.assertIsInstance(self.key_agent.generate_keys.__wrapped__(self.key_agent), bytes)

    def test_generate_with_dec_tuple(self):
        self.assertIsInstance(self.key_agent.generate_keys(), tuple)

    def test_generate_with_dec_key(self):
        self.assertIsInstance(self.key_agent.generate_keys()[0], bytes)

    def test_generate_with_dec_time(self):
        self.assertIsInstance(self.key_agent.generate_keys()[1], int)

class TestClientKeyDecapsulation(unittest.TestCase):
    '''Test class for key decapsulation function in client key establishment class.'''

    def setUp(self):
        self.client_agent = ClientKeyEstablishment('ML-KEM-512')
        encap_key = self.client_agent.generate_keypair()
        server_agent = oqs.KeyEncapsulation('ML-KEM-512')
        self.server_cipher, secret = server_agent.encap_secret(encap_key)

    def tearDown(self):
        del self.client_agent
        del self.server_cipher

    def test_decapsulate_without_dec(self):
        self.assertIsInstance(self.client_agent.decapsulate_cipher.__wrapped__(self.client_agent, self.server_cipher), bytes)

    def test_decapsulate_with_dec(self):
        self.assertIsInstance(self.client_agent.decapsulate_cipher(self.server_cipher), tuple)

    def test_decapsulate_with_dec_key(self):
        self.assertIsInstance(self.client_agent.decapsulate_cipher(self.server_cipher)[0], bytes)

    def test_decapsulate_with_dec_time(self):
        self.assertIsInstance(self.client_agent.decapsulate_cipher(self.server_cipher)[1], int)

if __name__ == '__main__':
    unittest.main()
