from secrets import token_hex
from words import get_entropy_from_words
from converters import int_to_hex
# from scratch import generate_menmonic
import ecdsa
# from mnemonic import Mnemonic,
import mnemonic

mnemo = mnemonic.Mnemonic("english")

class Wallet:
    def __init__(self, mnemonic_words: str = None, seed: str = ""):
        if mnemonic_words:
            self.load_from_mnemonic(mnemonic_words)
        else:
            self.create_new()

    def load_from_mnemonic(self, words):
        entropy = get_entropy_from_words(words)
        random_int = int(entropy.hex(), 16)
        self.exponent_int = random_int
    
    def create_new(self):
        exponent_int = self.random_secret_exponent()
        self.exponent_int = exponent_int

    def random_secret_exponent(self):
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
        entropy_key_hex = f"{self.exponent_int:02x}"
        data = bytes.fromhex(entropy_key_hex)
        return mnemo.to_mnemonic(data)

    def show_exponent_info(self):
        print(f"hex: {int_to_hex(self.exponent_int)}")
        print(f"int {self.exponent_int}")
        print(mnemonic.mnemonic.b58encode("asdasdas"))


# Example
phrase = "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
# phrase = "remain fee stone genuine puzzle liar play globe measure snake regular sphere soon easily unlock rubber want onion peasant refuse degree donate soul uncle"
w = Wallet(phrase)
# w = Wallet()
phrase = w.get_menmonic()
w.show_exponent_info()
print(phrase)


