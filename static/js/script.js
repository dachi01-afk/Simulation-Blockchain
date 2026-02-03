// DASHBOARD LOAD
if (window.location.pathname === "/") {
    fetch("/api/chain")
        .then(res => res.json())
        .then(data => {
            document.getElementById("totalBlocks").innerText = data.length;
        });

    fetch("/api/validate")
        .then(res => res.json())
        .then(data => {
            document.getElementById("chainStatus").innerText =
                data.is_valid ? "VALID ✅" : "INVALID ❌";
        });
}

// LOAD BLOCKCHAIN
if (window.location.pathname === "/chain-page") {
    fetch("/api/chain")
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("blockContainer");
            container.innerHTML = "";

            data.forEach(block => {

                let transactionsHTML = "";

                if (block.transactions.length === 0) {
                    transactionsHTML = "<p><em>No Transactions</em></p>";
                } else {
                    block.transactions.forEach(tx => {
                        transactionsHTML += `
                            <div class="tx-box">
                                <p><strong>Sender:</strong> ${tx.sender}</p>
                                <p><strong>Receiver:</strong> ${tx.receiver}</p>
                                <p><strong>Amount:</strong> ${tx.amount}</p>
                            </div>
                        `;
                    });
                }

                container.innerHTML += `
                    <div class="card">
                        <h3>Block #${block.index}</h3>
                        <p><strong>Nonce:</strong> ${block.nonce}</p>
                        <p><strong>Hash:</strong> ${block.hash}</p>
                        <p><strong>Previous:</strong> ${block.previous_hash}</p>
                        <hr>
                        <h4>Transactions:</h4>
                        ${transactionsHTML}
                    </div>
                `;
            });
        });
}


// TRANSACTION
const txForm = document.getElementById("txForm");
if (txForm) {
    txForm.addEventListener("submit", function(e) {
        e.preventDefault();

        fetch("/api/transactions", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                sender: sender.value,
                receiver: receiver.value,
                amount: amount.value
            })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("txMessage").innerText = data.message;
        });
    });
}

// MINE
const mineBtn = document.getElementById("mineBtn");
if (mineBtn) {
    mineBtn.addEventListener("click", function() {
        mineBtn.innerText = "Mining...";
        fetch("/api/mine")
            .then(res => res.json())
            .then(data => {
                document.getElementById("mineResult").innerHTML =
                    `<div class="card">
                        <h3>Block #${data.index}</h3>
                        <p><strong>Hash:</strong> ${data.hash}</p>
                        <p><strong>Nonce:</strong> ${data.nonce}</p>
                    </div>`;
                mineBtn.innerText = "⛏ Start Mining";
            });
    });
}
