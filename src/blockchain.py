import hashlib
from src.block import Block
from src.transaction import Transaction


class BlockChain:
    def __init__(self):
        self.__current_transactions = []
        self.__chain = []
        self._create_genesis()

    def _create_genesis(self):
        """
        Creates the Genesis block and passes it to the chain

        :return: None
        """
        genesis_block = Block(0, [], 0, '00')
        self.__chain.append(genesis_block)
        print(f"Genisis block has been created:  {genesis_block.hash}")

    @property
    def last_block(self):
        return self.__chain[-1]

    def add_block(self, block):
        """
        Creates a new block and passes it to the chain
        :param block: <Block> Block to add to the chain
        :return: <bool> True if the block is added to the chain, False if not.
        """
        if self.validate_block(block, self.last_block):
            self.__chain.append(block)
            print(f"\nBlock validated and addded to blockchain. {block.hash} \n{block.serialize()}")

            # Clear transactions list
            self.__current_transactions = []

            return True

        return False

    def create_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next block

        :param sender: <str> sender address
        :param recipient: <str> recipient address
        :param amount: <float> amount
        :return: <Transaction> generated transaction
        """
        transaction = Transaction(sender, recipient, amount)

        if transaction.validate():
            self.__current_transactions.append(transaction)

            return transaction, True

        return None, False

    @staticmethod
    def _validate_proof_of_work(last_nonce, last_hash, nonce):
        """
        Validates the nonce

        :param last_nonce: <int> Nonce of the last block
        :param last_hash: <str> Hash of the last block
        :param nonce: <int> Current nonce to be validated
        
        :return: <bool> True if correct, False if not.
        """
        sha = hashlib.sha256(f'{last_nonce}{last_hash}{nonce}'.encode())
        return sha.hexdigest()[:4] == '0000'

    def generate_proof_of_work(self, block):
        """
        Very simple proof of work algorithm:

        - Find a number 'p' such that hash(pp') contains 4 leading zeroes
        - Where p is the previous proof, and p' is the new proof

        :param block: <Block> reference to the last block object
        :return: <int> generated nonce
        """
        last_nonce = block.nonce
        last_hash = block.hash

        nonce = 0
        while not self._validate_proof_of_work(last_nonce, last_hash, nonce):
            nonce += 1

        return nonce

    def mine(self, reward_address):

        """
        Mines a new block into the chain

        :param reward_address: <str> address where the reward coin will be transferred to
        :return: result of the mining attempt and the new block
        """
        last_block = self.last_block
        index = last_block.index + 1
        previous_hash = last_block.hash

        # Let's start with the heavy duty, generating the proof of work
        nonce = self.generate_proof_of_work(last_block)

        print(f"Congratulations we have a POW!  Nonce is {nonce} for block hash {last_block.hash}")

        # In the next step we will create a new transaction to reward the miner
        # In this particular case, the miner will receive coins that are just "created", so there is no sender
        self.create_transaction(
            sender="0",
            recipient=reward_address,
            amount=1,
        )

        # Add the block to the new chain
        block = Block(index, self.__current_transactions, nonce, previous_hash)

        if self.add_block(block):
            return block

        return None
    
    def validate_block(self, current_block, previous_block):
        """
        Validates a block with reference to its previous
        :param current_block:
        :param previous_block:
        :return:
        """
        # Check the block index
        if current_block.index != previous_block.index + 1:
            return False

        if current_block.previous_hash != previous_block.hash:
            return False

        if not self._validate_proof_of_work(previous_block.nonce, previous_block.hash, current_block.nonce):
            return False

        return True

    def __str__(self):
        return(f"Block height: {len(self.__chain)}")