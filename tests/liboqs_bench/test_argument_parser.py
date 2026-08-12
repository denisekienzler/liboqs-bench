'''Stub testing script for argument parser'''

import unittest
import sys
sys.path.append('../src')

from liboqs_bench.argument_parser import ArgumentParser

class TestArgumentParser(unittest.TestCase):
    '''
    Test class on argument parser
    '''

    def test_port_argument(self):
        '''don't raise error when port number in range'''
        self.assertIn(31021,list(range(1024,49152)))

    def test_wrong_port(self):
        '''raise error when port not in range'''
        self.assertNotIn(1023,list(range(1024,49152)))

if __name__ == '__main__':
    unittest.main()