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

if __name__ == '__main__':
    unittest.main()
