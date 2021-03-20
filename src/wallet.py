from secrets import token_hex
from src.words import get_entropy_from_words
from src.converters import int_to_hex
import hashlib
import ecdsa
import mnemonic
import base58
import codecs
from enum import Enum

mnemo = mnemonic.Mnemonic("english")

# class Network(Enum):
#     MAINNET = b'00'
#     TESTNET = b'6f'
NETWORK_BYTE = b'00'

class Wallet:
    def __init__(self, 
                # network: Network = Network.TESTNET,
                mnemonic_words: str = None):
        if mnemonic_words:
            self._load_from_mnemonic(mnemonic_words)
        else:
            self._create_new()
        self.compressed_public_key = self.get_compressed_public_key()
        # if network == Network.MAINNET:
        #     self.NETWORK_BYTE = b'00'
        # else:
        #     self.NETWORK_BYTE = b'6f'

    def load_from_entropy(self, entropy: hex):
        # random_hex = '60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2'
        secret_exponent = int(entropy, 16)

        self.secret_exponent = secret_exponent
        self.sk = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, ecdsa.curves.SECP256k1, hashlib.sha256
        )

    def _load_from_mnemonic(self, words):
        entropy = get_entropy_from_words(words)
        secret_exponent = int(entropy.hex(), 16)
        # random_hex = '60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2'
        # secret_exponent = int(random_hex, 16)

        self.secret_exponent = secret_exponent
        self.sk = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, ecdsa.curves.SECP256k1, hashlib.sha256
        )
    
    def _create_new(self):
        secret_exponent = self.random_secret_exponent()
        self.secret_exponent = secret_exponent
        self.sk = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, ecdsa.curves.SECP256k1, hashlib.sha256
        )

    def sign_message(self, message):
        signature = self.sk.sign(message)
        print(f"signature: {signature.hex()}")
        return signature

    def verify_message(self, signature, message):
        return self.sk.verifying_key.verify(signature, message)

    def get_public_key(self):
        key_bytes = self.sk.verifying_key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        return f"04{key_hex.decode('utf-8')}"
    
    def get_compressed_public_key(self):
        key_bytes = self.sk.verifying_key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex').decode('utf-8')
        key_x = key_hex[:int(len(key_hex)/2)]
        if (int(key_hex[len(key_hex)-1:], 16) % 2) == 0:
            return f"02{key_x}"
        return f"03{key_x}"
    
    def get_encrypted_public_key(self, public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        # return public_key_bytes
        # Run SHA-256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        # # Run RIPEMD-160 for the SHA-256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # xx = f"{self.prefix}{ripemd160_bpk_hex.decode('utf-8')}"
        # print(xx)
        # print(self.checksum(bytes(xx, 'utf-8')))
        # print(self.checksum((xx)))
        # print(self.checksum(bytes(ripemd160_bpk_hex)))
        return ripemd160_bpk_hex

    @classmethod
    def checksum(cls, encrypted_public_key):
        # Double SHA256 to get checksum
        sha256_nbpk = hashlib.sha256(encrypted_public_key)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        return sha256_2_hex[:8]

    @classmethod
    def random_secret_exponent(cls):
        """ Generates a random secret exponent. """

        while True:
            # generate a random 256 bit hex string
            # is token hex random enough?
            random_hex = token_hex(32)
            random_int = int(random_hex, 16)
            if random_int >= 1 and (random_int < ecdsa.curves.SECP256k1.order - 1):
                break
        return random_int
    
    def get_menmonic(self):
        entropy_key_hex = f"{self.secret_exponent:02x}"
        data = bytes.fromhex(entropy_key_hex)
        return mnemo.to_mnemonic(data)

    def show_exponent_info(self):
        print(f"\nhex: {int_to_hex(self.secret_exponent)}")
        print(f"\nint {self.secret_exponent}")
        unencoded_string = bytes.fromhex(f"{self.secret_exponent:02x}")
        encoded_string= base58.b58encode(unencoded_string)
        print(f"\nbase58: {encoded_string.hex()}")
        print(f"\npublic key: {self.get_public_key()}")
        compressed_public_key = self.get_compressed_public_key()
        print(f"\ncompressed publc key: {compressed_public_key}")

        encrypted_public_key = self.get_encrypted_public_key(compressed_public_key)
        print(f"\nencrypted publc key: {encrypted_public_key}")
        # Add network byte
        network_bitcoin_public_key = NETWORK_BYTE + encrypted_public_key
        print(network_bitcoin_public_key)
        network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')

        # encrypted_public_key = self.get_encrypted_public_key(self.get_compressed_public_key())
        # print(f"\nencrypted public key: {encrypted_public_key}")
        encrypted_public_key_checksum = self.checksum(network_bitcoin_public_key_bytes)
        # hex_address = f"{NETWORK_BYTE.decode('utf-8')}{encrypted_public_key.decode('utf-8')}{encrypted_public_key_checksum.decode('utf-8')}"
        # print(f"hex_address: {hex_address}")
        # unencoded_string = bytes.fromhex(f"{self.secret_exponent:02x}")
        # addr = base58.b58encode(hex_address)
        # print(f"addr: {addr}")
        address_hex = (network_bitcoin_public_key + encrypted_public_key_checksum).decode('utf-8')
        addr = b58(address_hex)
        print(f"addr: {addr}")

        # print(self.checksum(bytes(encrypted_public_key, 'utf-8')))
        # print(f"\nchecksum: {self.checksum(self.get_encrypted_public_key(self.get_compressed_public_key()))}")

def b58(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    # Get the number of leading zeros and convert hex to decimal
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    # Convert hex to decimal
    address_int = int(address_hex, 16)
    # Append digits to the start of string
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    # Add '1' for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string

# Example
# phrase = "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
# # phrase = "remain fee stone genuine puzzle liar play globe measure snake regular sphere soon easily unlock rubber want onion peasant refuse degree donate soul uncle"
# w = Wallet(phrase)
# # w = Wallet()
# phrase = w.get_menmonic()
# w.show_exponent_info()
# print(f"menmonic: {phrase}")

# msg = b"some message data"

# signature = w.sign_message(msg)
# if not w.verify_message(signature, msg):
#     print('The signature is valid')
