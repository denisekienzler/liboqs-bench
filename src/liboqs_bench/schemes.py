'''
KEM schemes for liboqs_bench package
'''

from oqs import oqs

class KeyGeneration(oqs.KeyEncapsulation):

    '''
    Key Generation class

    Simple child class to generate a KEM keypair with the chosen scheme. It only exists so that the code is structured. 
    '''

    def to_measure(self):
        self.generate_keypair()            

class Encapsulation:

    '''
    Encapsulation class

    The constructor generates two Key Encapsulation instances of Alice and Bob, and generates Alice's keypair.

    The function to_measure() encapsulates a secret in a cipher text with Alice's public key.
    '''

    def __init__(self, scheme: str)-> None:
        self.alice = oqs.KeyEncapsulation(scheme)
        self.bob = oqs.KeyEncapsulation(scheme)
        self.alice_pub = self.alice.generate_keypair()

    def to_measure(self)-> tuple[bytes, bytes]:        
        return self.bob.encap_secret(self.alice_pub)

class Decapsulation:

    '''
    Decapsulation class

    The constructor generates an instance with Alice and her key pair, the shared cipher and secret as Bob sends them.

    The function to_measure() returns the secret as Alice decrypts them.

    The secret as Bob sends it and as Alice receives it can be called for testing reasons.
    '''

    def __init__(self, scheme: str)-> None:
        self.alice = oqs.KeyEncapsulation(scheme)
        self.bob = oqs.KeyEncapsulation(scheme)
        self.alice_pub = self.alice.generate_keypair()
        self.cipher,self.bob_secret = self.bob.encap_secret(self.alice_pub)

    def to_measure(self) -> bytes:
        return self.alice.decap_secret(self.cipher)
