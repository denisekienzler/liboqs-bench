'''
Unit test file for liboqs_bench.bench.
'''

import unittest
import sys
sys.path.append('../src')

from liboqs_bench import liboqs_bench

class Testliboqsbench(unittest.TestCase):
    '''
    Test class for liboqs_bench.bench.liboqs_bench() function.
    '''
    def test_alg_eq_help(self):
        '''Print docstring when typing 'help' as first argument.'''
        self.assertIs(liboqs_bench('help'),liboqs_bench.__doc__)

    def test_alg_eq_schemes_is_cls(self):
        '''Print string when typing 'schemes' as first argument.'''
        self.assertIsInstance(liboqs_bench('schemes'),str)

    @unittest.skip('Skipping server test.')
    def test_alg_eq_server_is_server(self):
        '''Start server when typing 'server' as first argument.'''
        self.assertIs(liboqs_bench('server'),liboqs_bench_server('127.0.0.1',31021))

if __name__ == '__main__':
    unittest.main()