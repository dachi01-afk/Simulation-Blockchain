class ProofOfWork:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def mine(self, block):
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()

        return block