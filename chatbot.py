from Avatar import Avatar
from Menu import Menu
from Customer2 import Customer
from NLP import NLP
from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract, extractOne



class Chatbot():

    def __init__(self):
        ''' Constructor Method '''
        self.waiter = Avatar("Luigi")
        self.waiter.say("Welcome to Italiabot.")
        self.menu = Menu("Italia Forever Lunch Menu")

        #  These are the keywords for each option and the corresponding response when choosing that option
        self.exitRequest =      {
                "keywords":      ["exit","leave","bye"],
                "response":      "leave us now"
        }

        self.historyRequest =   {
                "keywords":     ["history", "previous"],
                "response":     "see your previous orders"
        }
        self.menuRequest =      [["menu", "course", "meal","choice","options"],     "see the menu"]
        self.orderRequest =     [["order", "buy","food"],                           "order some food"]
        # self.exitRequest =      [["exit","leave","bye"],                            "leave us now"]
        self.historyRequest =   [["history", "previous"],                           "see your previous orders"]
        self.menuRequest =      [["menu", "course", "meal","choice","options"],     "see the menu"]
        self.orderRequest =     [["order", "buy","food"],                           "order some food"]
        self.mainOptions = self.exitRequest["keywords"] + self.historyRequest[0] + self.menuRequest[0] + self.orderRequest[0]


    def getOptions(self,choice=None, options=None):
        ''' choose from a list options'''
        matches = []
        maxConfidence = 0

        while len(matches)==0:
            if not choice:
                choice = self.waiter.listen().strip().lower()
                if not choice:
                    break

            results = extract(choice, options, scorer=partial_ratio, processor=default_process)

            for result in results:
                (match, confidence, index) = result
                print(f"Checking: {result}")
                if confidence > maxConfidence:
                    maxConfidence = confidence
                    matches = [match]
                elif confidence == maxConfidence:
                    matches.append(match)

            print(f"You have matched: {','.join(matches)} with confidence level {maxConfidence}% {len(matches)}")

            # if len(matches)>1:
            #     self.waiter.say(f"Sorry, I am not sure if you wanted {' or '.join(matches)}. Please try again.")
            #     options = matches
            #     matches = []
            #     maxConfidence = 0

        return matches[0] if len(matches)>0 else []

    def getCustomer(self):
        '''Get a customer - using username typed in for accuracy '''
        # get user name - typed
        self.waiter.say("Italiabot",display=True)
        username = self.waiter.listen("Please enter your username: ",useSR=False)
        print(".... Checking our customer database.....")
        # lookup customer -> new or existing?
        self.customer = Customer(username)

        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}.  May I call your {self.customer.getFirstName()}?")

    def getRequest(self):
        response = None

        while not response:
            self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do? ")

            option = self.waiter.listen("Order food? See the menu? Look at your order history? or Exit?")

            choice = self.getOptions(option, self.mainOptions)

            if choice in self.exitRequest["keywords"]:
                response = self.exitRequest["response"]
            elif choice in self.historyRequest[0]:
                response = self.historyRequest[1]
            elif choice in self.menuRequest[0]:
                response = self.menuRequest[1]
            elif choice in self.orderRequest[0]:
                response = self.orderRequest[1]
            else:
                self.waiter.say(f"I am sorry, I don't understand your choice. You said: '{option}. Please try again.")

        self.waiter.say(f"Right, You chose to {response}.")
        return choice

    def displayOrderHistory(self):
        self.waiter.say(f"Ok, {self.customer.getFirstName()}. Let's show your previous orders. ")

    def displayMenu(self):
        self.waiter.say(f"Alright, {self.customer.getFirstName()}. Let's see the menu. ")
        self.menu.display()

    def orderFood(self):
        self.waiter.say(f"Prego, {self.customer.getFirstName()}. Let's order some food. ")




    def run(self):
        # get the customer
        self.getCustomer()

        # LOOP - 1) Order? 2) View Menu 3) Order History 4) Leave/Exit
        running = True
        while running:

            choice = self.getRequest()
            print(choice)

            if choice in self.exitRequest["keywords"]:
                self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for ordering with Italiabot today. Bye bye")
                running = False

            elif choice in self.historyRequest[0]:
                self.displayOrderHistory()
            elif choice in self.menuRequest[0]:
                self.displayMenu()
            elif choice in self.orderRequest[0]:
                self.orderFood()

def main():

    italiabot = Chatbot()

    italiabot.run()


if __name__ == "__main__":
    main()