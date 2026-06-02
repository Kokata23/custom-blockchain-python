
from hashlib import sha256
from single_block import Block


class Miners:
    def __init__(self, miner_address, rewards=0):
        self.miner_address = miner_address
        self.rewards = rewards

    def mine(self, block, stop):
        if block.index == 0:
            block.pr_hash = block.hash

        while True:
            if stop:
                break
            block.nounce += 1
            block_data = f"{block.index}{block.date}{block.transactions}{block.nounce}{block.pr_hash}"
            try_hash = sha256(block_data.encode()).hexdigest()

            if try_hash.startswith('2300'):
                block.hash = try_hash
                return block

    def __str__(self):
        return f'Miners address:{self.miner_address}, miners rewards: {self.rewards}'

