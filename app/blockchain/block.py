import hashlib
import json
from time import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index" : self.index,
            "transactions" : self.transactions,
            "timestamp" :self.timestamp,
            "previous_hash" : self.previous_hash,
            "nonce" : self.nonce
        },  sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()