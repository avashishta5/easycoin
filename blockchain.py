from hashlib import sha256
from datetime import datetime


class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        hash = sha256()
        hash.update(str(self.index).encode()
                   +str(self.data).encode()
                   +str(self.timestamp).encode()
                   +str(self.previous_hash).encode())
        return hash.hexdigest()



def genesis_block():
    return Block(0, 
                 datetime.now(),
                 {
                 "proof-of-work": 9,
                 "transactions": None
                 }, 
                 "0")
