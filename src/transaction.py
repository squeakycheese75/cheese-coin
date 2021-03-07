#!/usr/bin/env python
"""For handling all operations related to the a transaction.
"""

import json
from time import time

class Transaction:
    """
        A class to represent a transaction.
        ...
        Attributes
        ----------
        sender : str
            the sender address
        recipient : str
            the recipient address
        amount : int
            the transaction value.
        """
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time()

    def validate(self):
        """
        Simple check to ensure the transations is greater than zero.
        """
        if self.amount > 0:
            return True
        return False

    def __str__(self) -> str:
        return json.dumps({"sender": self.sender,
                           "recipient": self.recipient,
                           "amount": self.amount,
                           "timestamp": self.timestamp},
                                sort_keys=True, indent=4)

    def serialize(self) -> str:
        """
        Serialize the transaction, allow for removal of

        :return: None
        """
        return json.dumps(self.__dict__)
