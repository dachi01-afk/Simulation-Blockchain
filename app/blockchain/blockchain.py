import requests
from time import time
from app.blockchain.block import Block
from app.blockchain.consensus import ProofOfWork
from app.blockchain.utils import serialize_block
from config import Config
from app.network.node import Node

class Blockchain:
    
    def __init__(self, address):
        self.chain =[]
        self.pending_transactions = []
        self.node = Node(address)
        self.pow = ProofOfWork(Config.DIFFICULTY)
        self.create_genesis_block()

        # auto register bootstrap nodes
        self.connect_to_network()
    
    def create_genesis_block(self):
        # genesis_block = Block(0, [], time(), "0")
        genesis_block = Block(
            index=0,
            transactions=[],
            timestamp=1700000000,  # timestamp tetap
            previous_hash="0",
            nonce=0
    )
        self.chain.append(genesis_block)
    
    def register_node(self, address):
        self.node.register_node(address)

    
    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
    
    def mine_block(self):
        if not self.pending_transactions:
            return None

        last_block = self.get_last_block()

        new_block = Block(
            index = len(self.chain),
            transactions = self.pending_transactions,
            timestamp = time(),
            previous_hash = last_block.hash
        )
        self.pow.mine(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        self.node.broadcast_new_block(serialize_block(new_block))
        self.replace_chain()

        return new_block


    def is_chain_valid(self, chain=None):

        if chain is None:
            chain = self.chain

        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            # cek hash valid
            if current.hash != current.calculate_hash():
                return False

            # cek previous hash
            if current.previous_hash != previous.hash:
                return False
            
            # cek proof of work
            if not current.hash.startswith('0' * Config.DIFFICULTY):
                return False

        return True

    def replace_chain(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.node.nodes:
            try:
                response = requests.get(f"{node}/api/chain")

                if response.status_code == 200:
                    chain_data = response.json()
                    length = len(chain_data)

                    if length > max_length:
                        new_chain = []

                        for block_data in chain_data:
                            block = Block(
                                block_data["index"],
                                block_data["transactions"],
                                block_data["timestamp"],
                                block_data["previous_hash"],
                                block_data["nonce"]
                            )
                            block.hash = block_data["hash"]
                            new_chain.append(block)

                        if self.is_chain_valid(new_chain):
                            max_length = length
                            longest_chain = new_chain

            except:
                pass

        if longest_chain:
            self.chain = longest_chain
            return True

        return False


    def connect_to_network(self):
        for bootstrap in Config.BOOTSTRAP_NODES:

            if bootstrap == self.node.address:
                continue

            try:
                response = requests.post(f"{bootstrap}/api/register-node", json={"address": self.node.address})

                if response.status_code == 200:
                    print(f"Connected to boostrap : {bootstrap}" )
                    self.node.register_node(bootstrap)
                    nodes = response.json().get("nodes", [])

                    # register all nodes received
                    for node in nodes:
                        if node != self.node.address:
                            self.node.register_node(node)

                    
            except Exception:
                print(f"{bootstrap} not online, skipping...")
        print(f"Final peers :", self.node.nodes)
        self.replace_chain()



    def save_chain_to_db(self):
        pass    