class Basket():

    def __init__(self):
        self.__basket = []

    def addItem(self,basketItem=None):
        if basketItem:
            self.__basket.append(basketItem)

    def setBasket(self,basket=None):
        self.__basket = basket

    def getBasket(self):
        return self.__basket

    def __str__(self):
        print("Basket")

    def displayBasket(self):
        print("Basket")
        for basketItem in self.__basket:
            print(basketItem)

class BasketItem():

    def __init__(self, meal=None, quantity=None):
        self.setMeal(meal)
        self.setQuantity(quantity)

    def getMeal(self):
        return self.__meal

    def getQuantity(self):
        return self.__quantity

    def setMeal(self,meal=None):
        self.__meal = meal

    def setQuantity(self,quantity=None):
        if quantity:
            self.__quantity = int(quantity)
        else:
            self.__quantity = 0

    def __str__(self):
        return f"Meal: {self.getMeal()}, Quantity: {self.getQuantity()}"