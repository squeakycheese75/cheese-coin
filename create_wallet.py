from src.walllet import Wallet

w = Wallet()

data = b"some data"
signature = w.sign_data(data)
if not  w.verify_message(signature, data):
    print('Signature is valid')