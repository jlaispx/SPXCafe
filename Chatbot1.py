from Avatar import Avatar
from NLP import NLP
from rapidfuzz import fuzz, process
from rapidfuzz.fuzz import partial_ratio
from CustomerDemo import Customer

class Chatbot():

    def __init__(self,restaurant="Italia"):
        self.__waiter = Avatar("Luigi")
        self.__restaurant = restaurant
        self.say("Welcome to {self.__restaurant} Chatbot!")

    def getUserName(self):
        self.userName = self.listen("Please enter your username: ",useSR=False)
        self.say(f"Ok. Checking your username: {self.userName}. Please wait...")
        self.customer = Customer.findUser(self.userName)
        if self.customer:
            self.say(f"Welcome back! {sef.customer.getName()}")
            return
        else:
            getNewCustomer(userName)


    def getCustomer(self):
        self.getUserName()



def main():
    c = Chatbot()
    c.getCustomer()

if __name__ == "__main__":
    main()