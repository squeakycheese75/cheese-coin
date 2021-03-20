from mnemonic import Mnemonic

mnemo = Mnemonic("english")


def get_entropy_from_words(words: str) -> int:
    """
    Return entropy from mneumonic words list 
    """
    entropy = mnemo.to_entropy(words)
    return entropy


def get_menemonic_from_key(entropy: int) -> str:
    """
    Return mneumonic from entropy
    """
    entropy_key_hex = f"{entropy:02x}"
    data = bytes.fromhex(entropy_key_hex)
    return mnemo.to_mnemonic(data)

# words = generate_words_and_key()
# pkey = get_entropy_from_words(words)
# # print(pkey)
# words2 = get_words_from_key(pkey)

# test_int=int('24198057703540789806893747320277442008152250674708019270369458233569547728460')
# test_int_b = test_int.to_bytes()
# mnemo.to_hd_master_key(test_int)