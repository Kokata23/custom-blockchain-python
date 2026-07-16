
import logging
import multiprocessing

from mine import Miners
from single_block import Block

logging.basicConfig(filename='mining.log', level=logging.DEBUG)



def start_mining(miner, block, e, sh, q):
    e.wait()
    mining = miner.mine(block, sh)
    if mining and not sh:
        sh.append(mining)
        q.put(miner.miner_address)



class Blockchain:
    def __init__(self):
        self.blockchain = []
        self.miners = []
        self.transactions = []
        self.proccesses = []
        self.manager = multiprocessing.Manager()
        self.shared_winner = self.manager.list()
        self.queen = multiprocessing.Queue()


    def add_block(self, block):
        self.blockchain.append(block)


if __name__ == '__main__':
    bl = Blockchain()
    block_made = 0
    num_to_start = 3


    while True:
        if not bl.miners:
            miners = (input('Attach miner/s address: ')).split()
            for m in miners:
                bl.miners.append(Miners(m))
            if not miners:
                print('Attach miner to start!')
                continue

        if block_made >= 0:
            var = input("For attaching miner type '+':")
            if var == '+':
                miner = (input('Attach miner/s address: ')).split()
                for m in miner:
                    bl.miners.append(Miners(m))
            # else:
            #     bl.transactions.append(var)


        print('Transactions..')
        while True:
            t = input()
            bl.transactions.append(t)
            if len(bl.transactions) >= num_to_start:
                break

        block = Block(block_made, bl.transactions)
        if bl.blockchain:                              
            block.pr_hash = bl.blockchain[-1].hash  

        e = multiprocessing.Event()
        bl.proccesses = [multiprocessing.Process(target=start_mining, args=(bl.miners[el], block, e, bl.shared_winner, bl.queen)) for el in range(len(bl.miners))]

        for p in bl.proccesses:
            p.start()

        e.set()

        for p in bl.proccesses:
            p.join()

        # print(bl.queen.empty())
        address = bl.queen.get()
        # print(bl.queen.empty())
        for m in bl.miners:
            if m.miner_address == address:
                m.rewards += 1


        bl.add_block(bl.shared_winner[0])
        block_made += 1
        bl.shared_winner.pop(0)
        bl.transactions = []

        for b in bl.blockchain:
            print(b)
            print()

        for m in bl.miners:
            print(m)
            print()

























































#
#
# class Blockchain:
#
#     def __init__(self):
#         self.blockchain = []
#         self.miners = []
#         self.transaction_pool = []
#         self.block_mined = False
#         self.MIN_TRANSACTIONS = 2
#         self.CHECK_INTERVAL = 3
#
#
#     def add_block(self, block):
#         self.blockchain.append(block)
#
#     def add_transaction(self, transaction):
#         self.transaction_pool.append(transaction)
#
#     def register_miner(self, address):
#         m = Miners(address)
#         self.miners.append(m)
#
#     def mine_blocks(self):
#         while True:
#             if len(self.transaction_pool) >= self.MIN_TRANSACTIONS:
#                 new_block = Block(len(self.blockchain), time.time(), self.transaction_pool)
#                 self.start_mining(new_block)
#                 self.transaction_pool = []  # Reset the transaction pool
#
#             time.sleep(self.CHECK_INTERVAL)
#
#     def mine_block(self, miner, block):
#         while not self.block_mined:
#             miner.mine(block)  # The miner attempts to mine the block
#             if block.hash.startswith('2300'):  # Example condition for a successfully mined block
#                 self.block_mined = True
#                 self.add_block(block)
#                 print(f"Block mined by {miner.miner_address}. Block Hash: {block.hash}")
#                 break
#
#     def start_mining(self, block):
#         self.block_mined = False  # Reset for the new block
#         mining_threads = []
#         for miner in self.miners:
#             thread = threading.Thread(target=self.mine_block, args=(miner, block))
#             mining_threads.append(thread)
#             thread.start()
#
#         for thread in mining_threads:
#             thread.join()
#
#
#
#
# if __name__ == '__main__':
#     bl = Blockchain()
#     mining_thread = threading.Thread(target=bl.mine_blocks)
#     mining_thread.start()
#
#     while True:
#         miner_address = input('Attach new miner (or press enter to skip): ')
#         if miner_address:
#             bl.register_miner(miner_address)
#
#         t = input("Enter transaction (or 'exit' to quit): ")
#         if t == 'exit':
#             break
#         bl.add_transaction(t)