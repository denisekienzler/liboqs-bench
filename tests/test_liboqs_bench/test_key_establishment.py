'''Unit test script for server key establishment module.'''

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

logging.getLogger('py.warnings').disabled = True

sys.path.insert(0,"../src")

_logger.debug(f'Root logger: {logging.getLogger()}')
_logger.debug(f'sys.path: {sys.path}')

from liboqs_bench.key_establishment import *

_logger.debug(f'Root logger: {logging.getLogger()}')

class TestTimedOnceDec(unittest.TestCase):
    '''Test class for decorator for timing once.'''

    def test_timed_once(self):
        self.assertIsInstance(timed_once(lambda x:x), Callable)

class TestServerKeyEstablishment(unittest.TestCase):
    '''Test class for ServerKeyEstablishment Class'''

    def setUp(self):
        self.key_agent = ServerKeyEstablishment('ML-KEM-512')
        self.encap_key = self.key_agent.generate_keypair()

    def tearDown(self):
        del self.key_agent

    def test_init(self):
        self.assertIsInstance(self.key_agent, oqs.KeyEncapsulation)

    def test_encapsulate_without_dec(self):
        _logger.debug(f'dir(self.key_agent.encapsulate_secret: {dir(self.key_agent.encapsulate_secret)}')
        _logger.debug(f'self.key_agent.encapsulate_secret.__dict__: {self.key_agent.encapsulate_secret.__dict__}')
        self.assertIsInstance(self.key_agent.encapsulate_secret.__wrapped__(self.key_agent, self.encap_key), tuple)

    def test_encapsulate_without_dec_tuple_items(self):
        for i in range(1):
            with self.subTest(arg=i):
                self.assertIsInstance(self.key_agent.encapsulate_secret.__wrapped__(self.key_agent, self.encap_key)[i], bytes)

    def test_encapsulate_with_dec(self):
        self.assertIsInstance(self.key_agent.encapsulate_secret(self.encap_key), tuple)

    def test_encapsulate_with_dec_cipher_bytes(self):
        self.assertIsInstance(self.key_agent.encapsulate_secret(self.encap_key)[0], bytes)

    def test_encapsulate_with_dec_time_int(self):
        self.assertIsInstance(self.key_agent.encapsulate_secret(self.encap_key)[1], int)


if __name__ == '__main__':
    unittest.main()
