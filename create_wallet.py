from src.wallet import Wallet

# # Generate a new wallet
# w1 = Wallet()
# phrase = w1.get_menmonic()
# w1.show_exponent_info()

# Generate a new wallet from a mnemonic
phrase = "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
# phrase = "aware report movie exile buyer drum poverty supreme gym oppose float elegant"
w2 = Wallet(phrase)
phrase = w2.get_menmonic()
w2.show_exponent_info()
print(f"\nmenmonic: {phrase}")

msg = b"some message data"

signature = w2.sign_message(msg)
if not w2.verify_message(signature, msg):
    print('\nThe signature is valid')

# print(w2.get_public_key())