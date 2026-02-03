def serialize_block(block):
    return {
        "index" : block.index,
        "transactions" : block.transactions,
        "timestamp" : block.timestamp,
        "previous_hash" : block.previous_hash,
        "nonce" : block.nonce,
        "hash" : block.hash,
    }