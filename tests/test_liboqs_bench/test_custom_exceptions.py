'''Stub test script'''

import unittest
import sys
sys.path.append('../src')

from liboqs_bench.custom_exceptions import *
from liboqs_bench import liboqs_bench

class TestCustomExceptions(unittest.TestCase):
    '''
    Test class on whether custom exceptions are raised when passing wrong or missing argument to liboqs_bench.liboqs_bench().
    '''
    
    def test_unsupported_algorithm_error(self):
        '''raise error when unsupported algorithm provided'''
        self.assertRaises(UnsupportedAlgorithmError, liboqs_bench, 'UNSUPPORTED', 'all')

    def test_unsupported_scheme_error(self):
        '''raises error when unsupported scheme provided'''
        self.assertRaises(UnsupportedSchemeError, liboqs_bench, 'complete', 'UNSUPPORTED')

    def test_no_scheme_provided_error(self):
        '''raise error when no scheme provided'''
        self.assertRaises(NoSchemeProvidedError, liboqs_bench, 'complete')

if __name__ == '__main__':
    unittest.main()