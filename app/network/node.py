import requests


class Node:
    def __init__(self, address):
        self.address = address
        self.nodes = set()
    
    def register_node(self, address):
        self.nodes.add(address)
    
    def broadcast_new_block(self, block):

        for node in self.nodes:
            try: 
                response = requests.post(f"{node}/api/receive-block", json=block)
                if response.status_code == 201:
                    print(f"Block accepted by {node}")
                else:
                    print(f"Block rejected by {node}")
            except Exception as e:
                print(f"Error broadcasting to {node}: {e}")

