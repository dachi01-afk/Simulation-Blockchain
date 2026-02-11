# PyChain-Sim 🔗
<!-- portfolio:desc -->
**PyChain-Sim** is a lightweight, distributed blockchain network simulation built with **Python** and **Flask**. It demonstrates the fundamental concepts of blockchain technology, including Proof-of-Work (PoW), peer-to-peer networking, and consensus algorithms.
<!-- portfolio:desc:end -->
---

## 📌 Overview

This project serves as an educational implementation of a decentralized ledger. It allows users to spin up multiple nodes, simulate transactions, mine blocks, and visualize the propagation of data across the network via a web interface.

### Key Features
* **Block Structure:** Implements standard block attributes (Index, Timestamp, Transactions, Previous Hash, Nonce).
* **Proof-of-Work (PoW):** A mining algorithm with adjustable difficulty settings.
* **P2P Networking:** Nodes can register with each other and broadcast new blocks.
* **Consensus Algorithm:** Implements the "Longest Chain Rule" to resolve conflicts and synchronize nodes.
* **Web Dashboard:** A simple UI to view the chain, manage transactions, and monitor nodes.

---

## 📂 Project Structure

* `run.py`: Entry point for the application. Accepts a port number as an argument.
* `config.py`: Global configuration (Mining Difficulty, Bootstrap Nodes).
* `app/`: Core application logic.
    * `routes.py`: API endpoints and web views.
    * `blockchain/`: Logic for the blockchain, blocks, and consensus.
    * `network/`: Logic for node registration and broadcasting.
* `templates/` & `static/`: Frontend assets for the web dashboard.

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.8+
* pip (Python Package Manager)

### Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/dachi01-afk/Simulation-Blockchain.git](https://github.com/dachi01-afk/Simulation-Blockchain.git)
    cd Simulation-Blockchain
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Linux / macOS
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Node**
    You can run multiple nodes on different terminals/ports to simulate a network.
    
    * **Node 1 (Port 5000):**
        ```bash
        python run.py 5000
        ```
    * **Node 2 (Port 5001):**
        ```bash
        python run.py 5001
        ```

---

## 🔌 API Documentation

The application exposes several RESTful endpoints for interacting with the blockchain.

### 1. Get Chain
Retrieves the full blockchain data from the local node.
* **URL:** `/api/chain`
* **Method:** `GET`

### 2. Create Transaction
Adds a new transaction to the pending pool.
* **URL:** `/api/transactions`
* **Method:** `POST`
* **Payload:**
    ```json
    {
        "sender": "Alice",
        "recipient": "Bob",
        "amount": 10
    }
    ```

### 3. Mine Block
Triggers the mining process to pack pending transactions into a new block.
* **URL:** `/api/mine`
* **Method:** `GET`

### 4. Register Node
Registers a new peer node to the network.
* **URL:** `/api/register-node`
* **Method:** `POST`
* **Payload:**
    ```json
    {
        "address": "http://localhost:5001"
    }
    ```

### 5. Consensus / Validation
Checks if the local chain is valid according to the cryptographic rules.
* **URL:** `/api/validate`
* **Method:** `GET`

---

## 🌐 Web Interface

You can interact with the blockchain visually by visiting the dashboard in your browser:

* **Dashboard:** `http://localhost:5000/`
* **View Chain:** `http://localhost:5000/chain-page`
* **Mining Interface:** `http://localhost:5000/mine-page`
* **Network Manager:** `http://localhost:5000/nodes`

---

## ⚡ Simulation Scenario: Multi-Node Network

To see the distributed nature in action, follow these steps:

1.  **Start Node A** on port 5000: `python run.py 5000`
2.  **Start Node B** on port 5001: `python run.py 5001`
3.  **Register Node B to Node A:**
    ```bash
    curl -X POST "http://localhost:5000/api/register-node" \
         -H "Content-Type: application/json" \
         -d '{"address":"http://localhost:5001"}'
    ```
    *(Node A will share its peer list with Node B automatically)*.
4.  **Mine on Node A:** Visit `http://localhost:5000/mine-page` and click "Mine".
5.  **Check Node B:** Visit `http://localhost:5001/chain-page`. You will see that Node B has automatically synchronized and received the block mined by Node A.

---

## ⚙️ Configuration

You can adjust the network settings in `config.py`:
* `DIFFICULTY`: Integer. Higher values increase mining time.
* `BOOTSTRAP_NODES`: List of initial nodes to connect to upon startup.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Developed by [Dachi](https://github.com/dachi01-afk)**
