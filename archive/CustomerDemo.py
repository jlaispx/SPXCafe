from SPXCafe import SPXCafe
from NLP import NLP
from Avatar import Avatar

class Customer(SPXCafe):

    def __init__(self, waiter=None):
        super().__init__()
        if waiter:
            self.waiter = waiter
        else:
            self.waiter("Luigi")
        self.nlp = NLP()

    @classmethod
    def findUser(cls, userName=None):
        if not userName:
            self.userName =

