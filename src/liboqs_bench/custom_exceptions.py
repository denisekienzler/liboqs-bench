'''
Custom exceptions for liboqs_bench package.
'''
import logging
_logger = logging.getLogger('__main__.' + __name__)

from oqs import oqs

class UnsupportedAlgorithmError(Exception):

    '''Custom exception for the user choosing an unsupported Algorithm or none at all.'''

    def __init__(self, alg)-> None:
        alg_str = '"KeyGeneration", "Encapsulation", "Decapsulation", or "all"'
        message = f'''
        "{alg}" is not a supported algorithm or argument.

        Type as argument(s):
        - "help" for general support on how to use the tool,
        - "schemes" for a list of supported KEM schemes, or
        - at least two arguments: 
            - One of the KEM algorithms {alg_str} and
            - at least one KEM scheme or "all".

        Optionally for the number of measurement iterations an integer can be passed as keyword argument 
        "iterations". The default value is 1000.
        '''
        super().__init__(message)

class UnsupportedSchemeError(Exception):

    '''Custom exception for user choosing unsupported scheme.'''

    def __init__(self, scheme:str)-> None:
        schemes_str = ''
        for scheme_name in oqs.get_enabled_kem_mechanisms():
            schemes_str += f'\n"{scheme_name}"'
        message = f'\n"{scheme}" is not a supported KEM scheme.\n\nInstead use one of these:\n{schemes_str}'
        super().__init__(message)

class NoSchemeProvidedError(Exception):

    '''Custom exception in case user doesn't provide a scheme.'''

    def __init__(self)-> None:
        schemes_str = ''
        for scheme_name in oqs.get_enabled_kem_mechanisms():
            schemes_str += f'\n"{scheme_name}"'
        message = f'No KEM scheme provided.\n\nUse at least one of these:\n{schemes_str}'
        super().__init__(message)

