
from hashlib import sha256


class Block:

    def __init__(self, index, transactions, date=None, nounce=0, pr_hash=None):
        self.index = index
        self.transactions = transactions
        self.date = date
        self.nounce = nounce
        self.pr_hash = pr_hash
        self.hash = ''.join(['2300', '0' * (len(sha256(''.encode()).hexdigest()) - 4)])

    @property
    def transactions(self):
        return self.__transactions

    @transactions.setter
    def transactions(self, value):
        if value:
            self.__transactions = [str(e) for e in value]
            
    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date(self, value):
        
        if value is None:
            self.__date = ', '.join(t for t in self.transactions)

    
    def __str__(self):
        return f'Block N:{self.index}\n date: {self.date}\n nounce:{self.nounce}\n pr_hash:{self.pr_hash}\n hash:{self.hash}'

