from flask import jsonify, request, render_template
from app.blockchain.blockchain import Blockchain
from app.blockchain.block import Block
from app.blockchain.utils import serialize_block
from config import Config



def register_routes(app, blockchain):

    # ======== PAGE ROUTES ========

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/chain-page")
    def chain_page():
        return render_template("chain.html")

    @app.route("/transaction-page")
    def transaction_page():
        return render_template("transaction.html")

    @app.route("/mine-page")
    def mine_page():
        return render_template("mine.html")

    @app.route("/nodes")
    def node_page():
        return render_template("nodes.html")

    # ======== API ROUTES ========

    @app.route("/api/chain", methods=["GET"])
    def get_chain():
        chain_data = [serialize_block(block) for block in blockchain.chain]
        return jsonify(chain_data)

    @app.route("/api/transactions", methods=["POST"])
    def add_transaction():
        data = request.json
        blockchain.add_transaction(data)
        return jsonify({"message": "Transaction added"}), 201

    @app.route("/api/mine", methods=["GET"])
    def mine():
        block = blockchain.mine_block()

        if block is None:
            return jsonify({"message": "No transactions to mine"}), 400

        return jsonify(serialize_block(block))

    @app.route("/api/validate", methods=["GET"])
    def validate():
        return jsonify({"is_valid": blockchain.is_chain_valid()})

    @app.route("/api/register-node", methods=["POST"])
    def register_node():
        data = request.json
        address = data.get("address")

        if not address:
            return jsonify({"message": "Invalid address"}), 400
        
        # jangan register diri sendiri
        if address == blockchain.node.address:
            return jsonify({
                "message": "Cannot register itself",
                "nodes": list(blockchain.node.nodes)
            }), 200

        # hanya tambah kalau belum ada
        if address not in blockchain.node.nodes:
            blockchain.register_node(address)

            print("New node registered :", address)
            print("Current peers :", blockchain.node.nodes)

             # 🔥 Kirim semua peer yang sudah ada ke node baru
            for peer in blockchain.node.nodes:
                if peer != address:
                    try:
                        requests.post(
                            f"{address}/api/register-node",
                            json={"address": peer}
                        )
                    except:
                        pass


            # sebarkan node baru ke semua peer lain
            for peer in blockchain.node.nodes:
                if peer != address:
                    # kirim balik agar dua arah (tanpa loop)
                    try:
                        requests.post(
                            f"{address}/api/register-node",
                            json={"address": address}
                        )
                    except:
                        pass

        return jsonify({
            "message": "Node registered successfully",
            "nodes": list(blockchain.node.nodes)
        }), 200

    @app.route("/api/receive-block", methods=["POST"])
    def receive_block():
        data = request.json

        last_block = blockchain.get_last_block()

        if data["previous_hash"] != last_block.hash:
            replaced = blockchain.replace_chain()
            if replaced:
                return jsonify({"message": "Chain replaced"}), 200
            return jsonify({"message": "Invalid previous hash"}), 400


        new_block = Block(
            data["index"],
            data["transactions"],
            data["timestamp"],
            data["previous_hash"],
            data["nonce"]
        )

        if data["index"] != last_block.index + 1:
            return jsonify({"message": "Invalid index"}), 400

        if data["previous_hash"] != last_block.hash:
            replaced = blockchain.replace_chain()
            if replaced:
                return jsonify({"message": "Chain replaced"}), 200
            return jsonify({"message": "Invalid previous hash"}), 400

        if new_block.calculate_hash() != data["hash"]:
            return jsonify({"message": "Invalid hash"}), 400

        if not data["hash"].startswith('0' * Config.DIFFICULTY):
            return jsonify({"message": "Invalid proof of work"}), 400

        new_block.hash = data["hash"]

        blockchain.chain.append(new_block)

        blockchain.replace_chain()

        return jsonify({"message": "Block accepted"}), 201


