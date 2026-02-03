from flask import Flask
from app.routes import register_routes
import sys
from app.blockchain.blockchain import Blockchain

app = Flask(__name__)

if __name__ == "__main__":
    port = 5000

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    address = f"http://localhost:{port}"

    # buat blockchain sesuai port
    blockchain = Blockchain(address)

    register_routes(app, blockchain)

    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)