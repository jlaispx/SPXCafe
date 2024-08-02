# Import business classes
from Avatar import Avatar
from Customer import Customer
from SPXCafe import SPXCafe
# from Order import Order
# from OrderItem import OrderItem
from Menu import Menu
# from Course import Course
# from Meal import Meal
# # Import system packages
from NLP import NLP
from rapidfuzz import fuzz, process, utils
from rapidfuzz.fuzz import partial_ratio

class Cafe(SPXCafe):

    def __init__(self, cafeName):
        ''' Constructor method
        '''
        self.waiter = Avatar("Luigi")
        self.setCafeName(cafeName)
        self.menu = Menu('Dinner Menu')

        # Main Menu Options #
        self.viewOrderHistory = ["history","past"]
        self.viewMenu = ["menu"]
        self.orderFood = ["order","buy"]
        self.exit = ["exit","leave","bye"]
        self.mainOptions = self.viewOrderHistory + self.viewMenu + self.orderFood + self.exit



    def setCafeName(self,cafeName):
        '''Set the cafe name'''
        if cafeName:
            self.cafeName = cafeName
        else:
            self.cafeName = "Cafe Unknown"

    def getCafeName(self):
        ''' get cafe name'''
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


    def getChoice(self,request=None, options=None):
        ''' Check of "Choice" is in one of the "Options'''
        results = process.extractOne(request, options, scorer=fuzz.partial_ratio, processor=utils.default_process)
        # return [choice, cofidence]
        return results

    def getChoices(self,request=None, options=None):
        ''' This returns multiple values that match your request'''
        results = process.extract(request, options, scorer=fuzz.partial_ratio, processor=utils.default_process)
        # return an set of choices [(choice,confidence),(choice,confidence)...]
        return results


    def welcomeCustomer(self):
        ''' Keep looping until we find a customer record or create a new customer record '''
        self.waiter.say(f"Buon Giorno!  Welcome to {self.getCafeName()}")

        self.customer = None
        while not self.customer:
            self.waiter.say("If you are an existing customer, please type in your username or leave it blank if you are a new customer.")
            userName = self.waiter.listen("Enter Username or leave blank for a new Customer or 'exit' to leave:", useSR=False).lower().strip()

            [exitRequest, confidence] = self.getChoice(userName, self.exit)
            if confidence > 60:
                self.waiter.say("Oh, you have changed your mind? Ok, no problems.")
                return False

            # If a Username is provided, then retrieve information
            if userName:
                self.customer = Customer.findCustomer(userName=userName)
                if self.customer:
                    self.waiter.say(f"Welcome back {self.customer.getFirstName()} {self.customer.getLastName()}")
                else:
                    self.waiter.say(f"I am sorry, we cannot find '{userName}' in our records. Please try again")
            else:
                self.createNewCustomer()

        return True

    def createNewCustomer(self,userName=None):

        self.waiter.say(f"Ah, ok this is your first time!")

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

    def processMainMenuChoice(self):

        running = True
        while running:
            self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do?")
            self.waiter.say("You can View Your Order History, View the Menu or Order Food or leave/exit")
            response = self.waiter.listen("Please tell me your choice").strip().lower()

            [choice, confidence] = getChoice(response, self.mainOptions)

            if confidence > 60:
                match choice:
                    case a if a in self.viewOrderHistory:
                        self.viewOrderHistory()
                    case a if a in self.viewMenu:
                        self.viewMenu()
                    case a if a in self.orderFood:
                        self.orderFood()
                    case a if a in self.exit:
                        self.exit()
                        running = False
            else:
                self.waiter.say(f"I am sorry, I do not understand '{response}'. Please try again.")

            self.waiter.say(f"Thank you {self.customer.getFirstName()}")

    def sayGoodbye(self):
        if self.customer:
            self.waiter.say(f"Thank you for joining us today, {self.customer.getFirstName()}.  Goodbye for now from {self.cafeName}")
        else:
            self.waiter.say(f"Sorry to see you go. We hope you order food with us next time. Goodbye from {self.cafeName}")



def main():
    cafeItalia = Cafe("Cafe Italia")
    useCase = 1

    while True:
        match useCase:
            case 1:                             # Use Case 1: Get a Customer
                if cafeItalia.welcomeCustomer():
                    useCase = 2
                else:
                    useCase = 3

            case 2:                             # Use Case 2: Get Main Menu choices
                choice = cafeItalia.processMainMenuChoice()
                useCase = 3

            case 3:                             # Use Case 3: exit
                cafeItalia.sayGoodbye()
                break


if __name__=="__main__":
    main()