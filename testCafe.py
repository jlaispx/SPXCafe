# Import business classes
from Avatar import Avatar
from Customer import Customer
from SPXCafe import SPXCafe
from Order import Order
from OrderItem import OrderItem
from Menu import Menu
from Course import Course
from Meal import Meal
# Import system packages
from NLP import NLP
from rapidfuzz import fuzz, process, utils
from rapidfuzz.fuzz import partial_ratio

class Cafe(SPXCafe):

    def __init__(self, cafeName):

        self.waiter = Avatar("Luigi")
        self.setCafeName(cafeName)
        self.menu = Menu('Dinner Menu')

    def setCafeName(self,cafeName):
        if cafeName:
            self.cafeName = cafeName
        else:
            self.cafeName = "Cafe Unknown"

    def getCafeName(self):
        if self.cafeName:
            return self.cafeName
        else:
            return "Cafe Unknown"

    def addOrder(self,order):
        if self.getCustomer():
            self.order = Order(orderDate=self.getToday(),customerId=self.getCustomer().getCustomerId())
            self.order.save()
        else:
            print("Cannot order if there is Customer.")




    # def getChoice(self,choice=None, options=None):
    #     [results = process.extract(choice, options, scorer=fuzz.partial_ratio, processor=utils.default_process)

    # def getChoices(self,choice=None, options=None):

    #     results = process.extract(choice, options, scorer=fuzz.partial_ratio, processor=utils.default_process)

    #     return results


    def welcomeCustomer(self):
        self.waiter.say(f"Buon Giorno!  Welcome to {self.getCafeName()}")

        while True:

            userName = "bloggs"
            # self.waiter.say("Can you please enter your username?")
            # userName = self.waiter.listen("Please enter a User Name: ",useSR=False).lower().strip()

            self.customer = Customer(userName=userName)

            self.waiter.say(f"Welcome back {self.customer.firstName} {self.customer.lastName}")

            # isCustomer = (self.waiter.listen("Have you ordered with us before? Y/N").strip().lower()[0])=="y"
            # if self.customer.existsDB():
            #     if isCustomer:
            #         print(f"Welcome back {customer.getCustomerName()!}")
            #     else:
            #         print("Sorry Username {userName} already exists. Please try again! ")
            # else:
            #     if isCustomer:
            #         print(f"Sorry, '{userName}' is not a valid User Name. Please Try again.")
            #     else:
            #         self.customer.setFirstName(self.waiter.listen("Please give me your First Name: ").lower().strip())
            #         self.customer.setLastName(self.waiter.listen("Please give me your Last Name: ").lower().strip())
            #         self.customer.save()
            #         print(f"Welcome{customer.getCustomerName()}. Your customer number is {self.customer.getCustomerId()}")

    def getMainMenuOption(self):
        mainOptions = ["history","menu","order","exit"]

        self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do?")
        self.waiter.say("You can View Your Order History, View the Menu or Order Food or leave/exit")
        response = self.waiter.listen("Please tell me your choice").strip().lower()


def main():
    cafeItalia = Cafe("Cafe Italia")
    useCase = 1

    while True:
        match useCase:
            case 1:                             # Use Case 1: Get a Customer
                cafeItalia.welcomeCustomer()
                useCase = 2

            case 2:                             # Use Case 2: Get Main Menu choices
                continue




if __name__=="__main__":
    main()