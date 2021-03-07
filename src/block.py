import json
import hashlib
from time import time
from json import JSONEncoder

class Block:
    def __init__(self, index, transactions, nonce, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = time()
        self.nonce = nonce
        self.previous_hash = previous_hash

    @property
    def hash(self) -> str:
        """
        Hash the utf-8 encoded serialized block using sha256 

        :return: A hex 256 byte hash of the serialized block.
        """
        sha = hashlib.sha256()
        sha.update(self.serialize().encode('utf-8'))
        return sha.hexdigest()
    
    def register_transaction(self, transaction):
        """
        Adds a transaction the the block
        """
        self.transactions.append(transaction)

    def serialize(self) -> str:
        """
        Serialize the Block and Transactions
        """
        return json.dumps(self, cls=BlockEncoder)

    def __str__(self) -> str:

        return json.dumps(self, indent=4, cls=BlockEncoder)

class BlockEncoder(JSONEncoder):
        """
        Custom Block encoder for serielization
        """
        def default(self, o):
            return o.__dict__