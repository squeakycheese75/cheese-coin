import ecdsa
import hashlib
import binascii
# import mnemonic
import bip32utils
from mnemonic import Mnemonic
from secrets import token_hex

import mnemonic
# from src.converters import int_to_binary


class Wallet:
    def __init__(self, mnemonic_words: str = None):
        self._hash_function = hashlib.sha256
        self._curve =  ecdsa.curves.SECP256k1
        self.privatekey = self.publickey = self.addr = self.mnemonic_words = ""
        if mnemonic_words:
            self.bip39(mnemonic_words)
        else:
            self.create_key()

    def create_key(self):
        secret_exponent = self.random_secret_exponent()
        self.pk = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, ecdsa.curves.SECP256k1, hashlib.sha256
        )
        # ecdsa.keys.SigningKey().
        self.privatekey = self.pk.privkey

    def get_private_key(self):
        return self.pk.privkey

    def get_public_key(self):
        return self.pk.verifying_key

    def sign_data(self, data):
        signature = self.pk.sign(data)
        return signature
    
    def verify_message(self, signature, data):
        self.pk.verifying_key.verify(signature, data)


    def random_secret_exponent(self):
        """ Generates a random secret exponent. """

        while True:
            # generate a random 256 bit hex string
            # is token hex random enough
            # 32 byte number, so 256 bit
            random_hex = token_hex(32)
            # print(f"\nhex: {random_hex}")
            random_int = int(random_hex, 16)
            # print(f"\nint: {random_int}")
            # random_binary = bin(random_int)
            # print(f"\nbin: {random_binary}")
            # if random_int >= 1 and random_int < ecdsa.curves.SECP256k1.order:
            if random_int >= 1 and (random_int < ecdsa.curves.SECP256k1.order - 1):
                break
        return random_int

    @property
    def show(self):
        return {
            'mnemonic_words': self.mnemonic_words,
            'addr': self.addr,
            'publickey': self.publickey,
            'privatekey': self.privatekey,
            'pk': self.pk
        }

    def get_seed(self, mnemonic_words):
        mnemo = Mnemonic("english")
        # mobj = mnemonic.Mnemonic("english")
        seed = mnemo.to_seed(mnemonic_words, "")
        return seed

    def get_mnemonic(self, seed):
        mnemo = Mnemonic("english")
        # mobj = mnemonic.Mnemonic("english")
        seed = mnemo.to_mnemonic(seed)
        return seed


    def bip39(self, mnemonic_words):
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(mnemonic_words)
        # mobj.to_entropy(mnemonic_words)

        bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
        bip32_child_key_obj = bip32_root_key_obj.ChildKey(
            44 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(0).ChildKey(0)

        self.privatekey = bip32_child_key_obj.WalletImportFormat(),
        self.publickey = binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
        self.addr = bip32_child_key_obj.Address(),
        self.mnemonic_words = mnemonic_words

    # return {
    #     'mnemonic_words': mnemonic_words,
    #     # 'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
    #     # 'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
    #     # 'path': "m/44'/0'/0'/0",
    #     'addr': bip32_child_key_obj.Address(),
    #     'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
    #     'privatekey': bip32_child_key_obj.WalletImportFormat(),
    #     'coin': 'BTC'
    # }


# w = Wallet()
# print(w.random_secret_exponent())
# pkey_int = int('24198057703540789806893747320277442008152250674708019270369458233569547728460')

# pkey_bin = bin(pkey_int)
# pkey_hex = f"0x{pkey_int:02x}"
# m = w.get_mnemonic(pkey_hex)
# print(m)
# s = w.get_seed(m)
# print(s)

# Generate words from random key
mnemo = Mnemonic("english")
words = mnemo.generate(strength=256)
print(words)


# Get key from mneumonic words list 
entropy = mnemo.to_entropy(words)
print(entropy.hex())
print(int(entropy.hex(), 16))

# Get words list from key
words2 = mnemo.to_mnemonic(entropy)
print(words2)

# seed = mnemo.to_seed(words, "password")
# r = p.decode('utf-8')
# print(r)
# print(int(k[2:] , 2))