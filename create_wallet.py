from src.wallet import Wallet

# Generate a new wallet and private key
w = Wallet()

# Create some message to be signed and verified
data = b"some data"
signature = w.sign_data(data)
if not w.verify_message(signature, data):
    print('Signature is valid')
print(w.show)
print(w.get_private_key())
print(w.get_public_key())

w.random_secret_exponent()


# recovery_seed = "peace amazing couch oven meat stay between raise risk sunny load kitten exile athlete cart"
# w.bip39(recovery_seed)
# print(w.show)