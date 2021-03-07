import ecdsa
import hashlib
import os
from binascii import hexlify
from secrets import token_hex

class Wallet:
    def __init__(self):
        self._hash_function = hashlib.sha256
        self._curve =  ecdsa.curves.SECP256k1
        self.create_key()

    def create_key(self):
        secret_exponent = self.random_secret_exponent(self._curve.order)
        self.sk = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, ecdsa.curves.SECP256k1, hashlib.sha256
        )

    def verify_key(self):
        return self.sk.verifying_key

    def sign_data(self, data):
        signature = self.sk.sign(data)
        return signature
    
    def verify_message(self, signature, data):
        self.sk.verifying_key.verify(signature, data)


    def random_secret_exponent(self, curve_order):
        """ Generates a random secret exponent. """
        # run a rejection sampling algorithm to ensure the random int is less
        # than the curve order
        while True:
            # generate a random 256 bit hex string
            # 32 bytes, 256 bit
            random_hex = token_hex(32)
            random_int = int(random_hex, 16)
            if random_int >= 1 and random_int < ecdsa.curves.SECP256k1.order:
                break
        return random_int

