# Import business classes
from Avatar import Avatar
from Customer import Customer
from SPXCafe import SPXCafe
# from Order import Order
# from OrderItem import OrderItem
from Menu import Menu
# from Course import Course
# from Meal import Meal
from Basket import Basket, BasketItem
# # Import system packages
from NLP import NLP
from rapidfuzz import fuzz, process, utils
from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.utils import default_process

class Cafe(SPXCafe):

    def __init__(self, cafeName):
        ''' Constructor method - This method runs when we create a new Cafe
        '''
        self.waiter = Avatar("Luigi")
        self.setCafeName(cafeName)
        self.setMenu(Menu('Dinner Menu'))
        self.nlp = NLP()

        # Main Menu Options #
        #  These are the keywords for each option and the corresponding response when choosing that option
        self.exitRequest =      {
                "keywords":      ["exit","leave","bye"],
                "response":      "leave us now"
        }

        self.historyRequest =   {
                "keywords":     ["history", "previous"],
                "response":     "see your previous orders"
        }
        self.menuRequest =      {
                "keywords":     ["menu", "course", "meal","choice","options"],
                "response":     "see the menu"
        }
        self.orderRequest =     {
                "keywords":     ["order", "buy","food"],
                "response":     "order some food"
        }

        self.mainOptions = self.exitRequest["keywords"] + self.historyRequest["keywords"] + self.menuRequest["keywords"] + self.orderRequest["keywords"]

        self.setConfidenceLevel(80)

        self.yesOptions = ["yes","sure","definitely","yup","yeah","positive"]
        self.noOptions = ["no","never","nope","negative"]
        self.yes = "yes"
        self.no = "no"

    def setCafeName(self,cafeName):
        '''Set the cafe name'''
        if cafeName:
            self.__cafeName = cafeName
        else:
            self.__cafeName = "Cafe Unknown"

    def getCafeName(self):
        ''' get cafe name'''
        if self.__cafeName:
            return self.__cafeName
        else:
            return "Cafe Unknown"

    def setMenu(self,menu=None):
        ''' Set Menu '''
        self.__menu = menu

    def getMenu(self):
        ''' Get Menu '''
        return self.__menu

    def setConfidenceLevel(self, confidence):
        self.__confidenceLevel = confidence

    def getConfidenceLevel(self):
        return self.__confidenceLevel

    # def addOrder(self,order):
    #     if self.getCustomer():
    #         self.order = Order(orderDate=self.getToday(),customerId=self.getCustomer().getCustomerId())
    #         self.order.save()
    #     else:
    #         print("Cannot order if you are not a Customer.")


    def getChoice(self,request=None, options=None):

        choice = None

        ''' Check of "Choice" is in one of the "Options'''
        result = process.extractOne(request, options, scorer=partial_ratio, processor=default_process)
        (foundChoice, confidence, ix) = result
        # return [choice, cofidence, index]

        if confidence > self.getConfidenceLevel():
            choice = foundChoice

        return choice

    def getChoices(self,request=None, options=None):
        ''' This returns multiple values that match your request'''
        choices = []
        results = process.extract(request, options, scorer=partial_ratio, processor=default_process)
        # return an set of choices [(choice,confidence, index),(choice,confidence, index)...]

        for result in results:
            (foundChoice,confidence,index) = result
            if confidence > self.getConfidenceLevel():
                choices.append(foundChoice)

        return choices

    def getYesNo(self,request=None):
        if request:
            if self.getChoice(request, self.yesOptions):
                return self.yes
            if self.getChoice(request, self.noOptions):
                return self.no
        else:
            return None

    ''' CUSTOMER PROCESSING  - USE CASE 1 '''

    def welcomeCustomer(self):
        ''' Keep looping until we find a customer record or create a new customer record '''
        self.waiter.say(f"Buon Giorno!  Welcome to {self.getCafeName()}")

        self.setCustomer()  # Set customer to none

        while not self.getCustomer():

            self.waiter.say("If you are an existing customer, please type in your username or leave it blank if you are a new customer.")
            userName = self.waiter.listen("Enter Username or leave blank for a new Customer or 'exit' to leave:", useSR=False).lower().strip()

            # If a Username is provided, then retrieve information
            if userName:
                ''' First check of exit requested '''
                choice = self.getChoice(userName, self.exitRequest["keywords"])

                if choice:
                    self.waiter.say("Oh, you have changed your mind? Ok, no problems.")
                    return False


                self.setCustomer(Customer.findCustomer(userName=userName))
                if self.getCustomer():
                    self.waiter.say(f"Welcome back {self.getCustomer().getFirstName()} {self.getCustomer().getLastName()}")
                else:
                    self.waiter.say(f"I am sorry, we cannot find '{userName}' in our records. Please try again")
            else:
                self.createNewCustomer()

        return True

    def createNewCustomer(self):

        self.waiter.say(f"Ah, ok this is your first time! Let's get some of your details.")

        userName = None
        while not userName:
            userName = self.waiter.listen(f"Please enter your new UserName: ", useSR=False).lower().strip()
            if  Customer.findCustomer(userName=userName):
                self.waiter.say(f"I am sorry, '{userName}' has already been used, please choose another.")
                self.userName = None

        firstName = self.nlp.getNameByPartsOfSpeech(self.waiter.listen("Please tell me your first name.")).title()
        lastName = self.nlp.getNameByPartsOfSpeech(self.waiter.listen("Please tell me your last name.")).title()

        self.waiter.say(f"Alright. Creating a new custmer")
        self.setCustomer(Customer(userName=userName, firstName=firstName, lastName=lastName))
        self.getCustomer().save()

        self.waiter.say(f"Ok {self.getCustomer().getCustomerName()}. Your new customer id is {self.getCustomer().getCustomerId()}, but please use your user name '{self.getCustomer().getUserName()}' when ordering in the future.")

    def getCustomer(self):
        return self.__customer

    def setCustomer(self,customer=None):
        self.__customer = customer

    ''' END CUSTOMER PROCESSING - USE CASE 1 '''


    ''' MAIN MENU PROCESSING - USE CASE 2 '''

    def processMainMenuChoice(self):
        ''' LOOP PROCESSING MAIN MENU CHOICES UNTIL EXIT REQUESTED '''
        if self.getCustomer():
            running = True
            while running:
                self.waiter.say(f"Ok {self.getCustomer().getFirstName()}. What would you like to do?")
                self.waiter.say("You can View Your Order History, View the Menu or Order Food or leave/exit")
                response = self.waiter.listen("Please tell me your choice").strip().lower()

                choice = self.getChoice(response, self.mainOptions)
                if choice:
                    match choice:
                        case a if a in self.historyRequest["keywords"]:
                            response = self.historyRequest["response"]
                            self.waiter.say(f"Right, You chose to {response}.")
                            self.viewOrderHistory()

                        case a if a in self.menuRequest["keywords"]:
                            response = self.menuRequest["response"]
                            self.waiter.say(f"Right, You chose to {response}.")
                            self.viewMenu()

                        case a if a in self.orderRequest["keywords"]:
                            response = self.orderRequest["response"]
                            self.waiter.say(f"Right, You chose to {response}.")
                            self.orderFood()

                        case a if a in self.exitRequest["keywords"]:
                            response = self.exitRequest["response"]
                            self.waiter.say(f"Right, You chose to {response}.")
                            running = False
                else:
                    self.waiter.say(f"I am sorry, I do not understand '{response}'. Please try again.")

                self.waiter.say(f"Thank you {self.getCustomer().getFirstName()}")
            return True
        else:
            return False


    def viewMenu(self):
        ''' VIEW MENU PROCESSING '''
        allCourses = "all"
        courses = self.getMenu().getCourses()
        courseNameList = ([c.getCourseName().title() for c in courses])

        # Keep repeating to get a valid choice
        while True:
            request = self.waiter.listen(f"Please choose from '{', '.join(courseNameList)} or All' to view.").lower()

            if request:
                courseName = self.getChoice(request, courseNameList+["All"]).lower() # use fuzzy logic
                if courseName:
                    self.waiter.say("Ok, let's see the Menu...")
                    break

            self.waiter.say(f"I am sorry, I don't understand your choice.  Please try again")

        if courseName==allCourses:
            courseName = None

        self.getMenu().display(courseName)

    def viewOrderHistory(self):
        ''' VIEW CUSTOMER ORDER HISTORY '''
        self.waiter.say("Viewing order history")
        self.getCustomer().displayOrders()



    def orderFood(self):
        ''' PROCESS CUSTOMER ORDERING FOOD '''

        # Initialise sub requests used only during ordering of food
        self.stopRequest =     {
            "keywords":     ["finish", "stop","complete"],
            "response":     "finish ordering food"
        }
        self.viewBasketRequest = {
            "keywords":     ["basket","status"],
            "response":     "view the basket"
        }

        self.orderingOptions = self.menuRequest["keywords"] + self.stopRequest["keywords"] + self.viewBasketRequest["keywords"]

        # Initialise an empty basket
        self.basket = Basket()

        self.waiter.say(f"{self.getCustomer().getFirstName()}, let's order some food. Please choose at least 3 meals, view the menu, basket or finish ordering> ")

        # ORDERING LOOP - ORDER, MENU or FINISH ==================================================
        finishOrdering = False
        while not finishOrdering:
            request = self.waiter.listen(f"{self.getCustomer().getFirstName()}, What meal would you like? or do you want to finish or see menu?")


            choice = self.getChoice(request,self.orderingOptions)
            if choice:  # did the request match one of the ordering options?
                match choice:
                    # ''' FINISH ORDERING '''
                    case a if a in self.stopRequest["keywords"]:
                        self.waiter.say(f"You have requested to {self.stopRequest["response"]}")
                        finishOrdering = self.stopOrdering()
                        # if finishOrdering:
                        #     self.addBasketToOrder(self.basket)

                    # ''' VIEW MENU '''
                    case a if a in self.menuRequest["keywords"]:
                        response = self.menuRequest["response"]
                        self.waiter.say(f"Right, You chose to {response}.")
                        self.viewMenu()

                    # DISPLAY BASKET
                    case a if a in self.viewBasketRequest["keywords"]:
                        response = self.viewBasketRequest["response"]
                        self.waiter.say(f"Sure {self.getCustomer().getFirstName()}, here is the current Basket contents...")
                        self.basket.displayBasket()
            else:
                # ''' ASSUME A MEAL ORDERED '''
                # check if choice is a meal
                self.addMealToBasket(request)


    def addMealToBasket(self,searchMeal=None):
        '''
            1.  Search for mealName is a valid Meal by asking Menu to FindMeal().
                This returns a list of meals.

                a. If no meal found - error message
                b. If more than one meal found - ask user to only enter ONE meal
                c. Process the ONE meal -
                    i) Ask for quantity
                    2) Build a BasketItem
                    3) Add BasketItemt o Basket
        '''
        searchMeal = self.nlp.getNounsByPartsOfSpeech(searchMeal) # just retrieve nouns from the search criteria
        print(f"searching for: {searchMeal}")
        meals = self.getMenu().findMeal(searchMeal)  # search Menu for a meal name - returns a list of meals

        if len(meals) == 0:  # no meals found
            self.waiter.say(f"'{searchMeal} is not a valid request. Please try again.")
        elif len(meals)>1:   # too many meals found
            self.waiter.say(f"Please be more precise. Which of the following do you want? {', '.join([meal.getMealName() for meal in meals])}")
        else:
            # Add a single meal and quantity to BasketItem and Basket
            meal = meals[0]
            quantity = None
            while not quantity:
                quantity = self.waiter.listen(f"How many '{meal.getMealName()}' do you want?")
                if quantity.isdigit() and int(quantity)>0:
                    quantity = int(quantity)
                    break
                else:
                    self.waiter.say(f"'{quantity}' is not a valid quantity. Try again.")
                    quantity=None

            self.basket.addItem(BasketItem(meal, quantity))
            self.waiter.say(f"Ok, {quantity} {meal.getMealName()} added to your basket")

    def addBasketToOrder(self,basket=None):
        order = self.getCustomer().newOrder(basket)
        self.waiter.say(f"Here is your finished order:")
        order.display()

    def stopOrdering(self):
        ''' Checks and Processing before finalising an Order
        '''
        finishOrdering = True
        self.waiter.say("Right, this is what is in your basket at the moment....")
        self.basket.displayBasket()

        if self.basket.checkMinOrderLevel():
            request = self.waiter.listen("You have enough items in your basket to finish your order.  Do you want to finalise your order?")
            if self.getYesNo(request) == self.yes:
                order = self.getCustomer().newOrder(self.basket)
                self.waiter.say(f"Done. You new order number is {order.getOrderId()}")
            else:
                self.waiter.say("Right, you have changed your mind about the order. Order is now cancelled.")
        else:
            self.waiter.say(f"Sorry {self.getCustomer().getFirstName()}, you do not have enough items in your basket to finalise your order.")
            request = self.waiter.listen(f"{self.getCustomer().getFirstName()}, Do you want to continue ordering?")
            if self.getYesNo(request) == self.yes:
                self.waiter.say("Let's continue ordering.")
                finishOrdering = False
            else:
                self.waiter.say("I understand. You have changed your mind about ordering food. Order is now cancelled")
        return finishOrdering


    ''' END MAIN MENU PROCESSING - USE CASE 2 '''

    ''' EXIT PROCESSING - Use Case 3 '''
    def exitProcessing(self):
        if self.confirmExit():
            self.sayGoodbye()
            return True
        else:
            return False

    def confirmExit(self):
        if self.getCustomer():
            request = self.waiter.listen(f"Are you sure you want to leave, {self.getCustomer().getFirstName()}?")
            choice = self.getChoice(request, "yes")
        else:
            choice = "yes"

        if choice:
            return True
        else:
            return False

    def sayGoodbye(self):
        if self.getCustomer():
            self.waiter.say(f"Thank you for joining us today, {self.getCustomer().getFirstName()}.  Goodbye for now from {self.__cafeName}")
        else:
            self.waiter.say(f"Sorry to see you go. We hope you order food with us next time. Goodbye from {self.__cafeName}")


def main():
    cafeItalia = Cafe("Cafe Italia")
    useCase = 1

    while True:
        match useCase:
            case 1:                             # Use Case 1: Get a Customer
                if cafeItalia.welcomeCustomer():
                    '''Valid Customer'''
                    useCase = 2
                else:
                    '''Exit - changed mind '''
                    useCase = 3

            case 2:                             # Use Case 2: Get Main Menu choices
                if cafeItalia.processMainMenuChoice():
                    useCase = 3
                else:
                    '''No Customer'''
                    useCase = 1

            case 3:                             # Use Case 3: exit
                exit = cafeItalia.exitProcessing()
                if exit:
                    break
                else:
                    useCase = 2


if __name__=="__main__":
    main()