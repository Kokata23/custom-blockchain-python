# Custom Blockchain — Python

A from-scratch blockchain implementation in Python featuring Proof-of-Work mining, multi-process miner competition, SHA-256 hashing, and transaction batching.

---

## How It Was Built

### Core Data Structure — `single_block.py`

Each block in the chain is represented by the `Block` class and holds:

- `index` — position in the chain
- `transactions` — list of transaction strings for this block
- `date` — derived from the transaction list at creation time
- `nonce` — the number incremented during mining to find a valid hash
- `pr_hash` — the hash of the previous block (creates the chain link)
- `hash` — the SHA-256 hash of this block's data

The initial hash is seeded with the prefix `2300` followed by zeros, matching the target difficulty pattern. The `transactions` setter coerces all values to strings, and the `date` setter derives a human-readable timestamp string from the transaction list.

---

### Proof-of-Work Mining — `mine.py`

The `Miners` class implements the Proof-of-Work algorithm:

1. A miner takes a `Block` and a shared `stop` flag.
2. On each iteration it increments `block.nonce` by 1.
3. It concatenates the block fields into a single string and runs `sha256()` on it.
4. If the resulting hex digest starts with `'2300'`, the hash is accepted and the mined block is returned.
5. If another miner has already solved the block (`stop` is truthy), the loop exits immediately.

The difficulty target is the 4-character prefix `'2300'` — statistically, a miner must try roughly 65,000 nonces on average before finding a valid hash.

Each miner also tracks a `rewards` counter and a `miner_address` string used to identify it.

---

### Competitive Multi-Process Mining — `blockchain.py`

The `Blockchain` class orchestrates everything:

**Data**
- `blockchain` — the ordered list of confirmed blocks
- `miners` — registered `Miners` objects
- `transactions` — the current pool of pending transactions
- `shared_winner` — a `multiprocessing.Manager().list()` used as shared memory across processes to hold the winning block
- `queen` — a `multiprocessing.Queue()` used to pass the winning miner's address back to the main process

**Mining loop (main block)**

```
While True:
  1. Prompt to add miners (one or more addresses)
  2. Collect transactions from stdin; wait until at least 3 are entered
  3. Create a new Block from the current transaction pool
  4. Spawn one Process per miner, each calling start_mining()
  5. Fire a multiprocessing.Event so all processes start simultaneously
  6. Join all processes (wait for all to finish)
  7. Read the winner's address from the Queue
  8. Increment that miner's reward counter
  9. Append the winning block to the chain (linking its pr_hash to the last block)
  10. Print the full chain and miner stats
```

**Race condition handling**

The `shared_winner` list is the mutex. Inside `start_mining()`:

```python
if mining and not sh:       # only the first miner to finish enters here
    sh.append(mining)       # write the winning block to shared memory
    q.put(miner_address)    # record the winner
```

Because `sh` is a managed list, only one process can write to it — all other miners see `sh` as truthy and break out of their loop.

**Chain linking**

When `add_block()` is called, it sets the new block's `pr_hash` to the hash of the last block in the chain, forming the tamper-evident linked list that gives a blockchain its integrity.

---

## Project Structure

```
.
├── blockchain.py     # Main Blockchain class and CLI entry point
├── mine.py           # Miner class with Proof-of-Work algorithm
├── single_block.py   # Block data structure with SHA-256 hashing
├── Node.py           # Placeholder for future peer-to-peer node networking
└── requirements.txt  # No third-party dependencies (stdlib only)
```

---

## How to Run

**Requirements:** Python 3.8+

```bash
python blockchain.py
```

Follow the prompts:

1. Enter one or more miner addresses (e.g. `alice bob charlie`)
2. Enter at least 3 transactions (one per line)
3. Watch the miners race to mine the block
4. The chain state and miner rewards are printed after each block

To add a new miner between blocks, type `+` when prompted.

---

## Key Design Decisions

| Decision | Detail |
|---|---|
| **Difficulty target** | Hash must start with `2300` (~65k average attempts per block) |
| **Multiprocessing over threading** | True CPU parallelism — each miner runs in its own OS process, bypassing Python's GIL |
| **Event-based race start** | `multiprocessing.Event` ensures all miners start simultaneously rather than staggering |
| **Shared memory via Manager** | `Manager().list()` is process-safe; the first miner to write wins the race |
| **Queue for winner identity** | A `Queue` communicates the winning address back to the main process cleanly |
| **No external dependencies** | Uses only Python stdlib (`hashlib`, `multiprocessing`, `logging`) |

---

## Concepts Demonstrated

- SHA-256 cryptographic hashing with `hashlib`
- Proof-of-Work consensus mechanism
- Block chaining via previous-hash linkage
- Parallel computation with `multiprocessing`
- Inter-process communication (shared memory + queues)
- Transaction batching before block creation
