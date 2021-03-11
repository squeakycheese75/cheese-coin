import binascii
import hashlib

"""
Just playing around with how the mnemonic is constructed!@
"""


def generate_menmonic(entropy_key: str, bits: int = 256):
    # Getting the binary from a hex string
    random_bin = binascii.unhexlify(entropy_key)
    # Converting back to hex
    random_hex = binascii.hexlify(random_bin)

    # Setting by bytes length 
    bytes = len(random_bin)

    # Applying SHA256
    hashed_sha256 = hashlib.sha256(random_bin).hexdigest()
    # print(f"My sha256: {hashed_sha256}")

    # checksum = bits/32

    # Creating an new key which is the binary + a checksum from the sha256. 
    bin_result = (
      bin(int(random_hex, 16))[2:].zfill(bytes * 8) + 
      bin(int(hashed_sha256, 16))[2:].zfill(256)[:bytes * 8 // 32]
    )
    print(f"Binary result: {bin_result}")

    # Reading in the list of 2048 supported words
    index_list = []
    with open("src/english.txt", "r", encoding="utf-8") as f:
        for w in f.readlines():
            index_list.append(w.strip())

    # Chunk into 11 bits, convert to int and lookup in the list
    wordlist = []
    for i in range(len(bin_result) // 11):
        idx = bin_result[i*11 : (i+1) * 11]
        wordlist.append(index_list[int(idx,2)])

    # Finally join all the words using space a seperator
    phrase = " ".join(wordlist)
    return phrase

phrase = generate_menmonic("68a79eaca2324873eacc50cb9c6eca8cc68ea5d936f98787c60c7ebc74e6ce7c")
print(phrase)
