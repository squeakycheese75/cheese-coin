from src.wallet import Wallet

print("1 - New generate a new wallet")
w1 = Wallet()
phrase = w1.get_menmonic()
w1.show_exponent_info()

print("2 - Restoring a wallet from a mnemonic")
phrase = "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
# phrase = "aware report movie exile buyer drum poverty supreme gym oppose float elegant"
w2 = Wallet(phrase)
phrase = w2.get_menmonic()
w2.show_exponent_info()
print(f"\nmenmonic: {phrase}")

# 3 - Restoring with a private key (just for testing)


print("3 - Signing a Transaction")
msg = b"some message data"

signature = w2.sign_message(msg)
if not w2.verify_message(signature, msg):
    print('\nThe signature is valid')