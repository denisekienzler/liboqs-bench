''' Unit test file for client parser module.'''

import logging
import unittest
import sys
import argparse

sys.path.append('../src')

from liboqs_bench_client.client_parser import ClientParser

_logger = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.WARNING)

ARG_LST = ['liboqs_bench_client', 'ALGORITHM', 'SCHEMES_TPL']
ALG_CHOICES=['KeyGeneration', 'Encapsulation', 'Decapsulation', 'complete']

class TestClientParser(unittest.TestCase):
    '''Test class for client parser.'''

    def setUp(self):
        self.test_parser = ClientParser()

    def tearDown(self):
        del self.test_parser

    def test_no_arg(self):
        '''Passing no argument assigns None.'''
        arg_lst = []
        _logger.debug('Argument list: ' + str(arg_lst))
        arguments = self.test_parser.parser.parse_args(arg_lst)
        _logger.debug('arguments.alg: ' + str(arguments.alg))
        self.assertEqual(arguments.alg, None)

    def test_alg_valid(self):
        '''Valid algorithm argument assigns valid value.'''
        for arg in ALG_CHOICES:
            _logger.debug('Argument list: ' + str([arg]))
            with self.subTest(failed_argument=arg):
                arguments = self.test_parser.parser.parse_args([str(arg)])
                _logger.debug('arguments.alg: ' + str(arguments.alg))
                self.assertEqual(arguments.alg, arg)

    def test_alg_invalid(self):
        '''Invalid algorithm argument exits with SystemExit.'''
        false_dct = {}
        false_dct['int'] = 34
        false_dct['str'] = 'string'
        false_dct['float'] = 4.3
        false_dct['bool'] = False
        for arg in false_dct.values():
            _logger.debug('Argument list: ' + str([arg]))
            with self.subTest(failed_argument = arg):
                self.assertRaises(SystemExit, self.test_parser.parser.parse_args, [str(arg)])

if __name__ == '__main__':
    unittest.main()
