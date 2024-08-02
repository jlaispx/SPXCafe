class Basket():
    '''Basket Class:
        This is used to collect Meals and Quantities
        This is then processed to create an Order once complete
    '''

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
        self.basketTotal = 0
        for basketItem in self.__basket:
            print(basketItem)
            self.basketTotal += basketItem.getCost()
        print(f"Basket Total: ${self.basketTotal:.2f}")

    def getBasketCount(self):
        return len(self.__basket)

    def minOrderLevel(self):
        if self.getBasketCount() >= 3:
            return True
        else:
            return False

class BasketItem():
    ''' BasketItem Class:
        Stores details about each meal in a basket, including quantities
    '''

    def __init__(self, meal=None, quantity=None):
        '''BasketItem Constructor: requeires a meal and quantity'''
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

    def getCost(self):
        return self.getMeal().getMealPrice() * self.getQuantity()

    def __str__(self):
        return f"Meal: {self.getMeal()}, Quantity: {self.getQuantity()}  Cost: ${self.getCost():.2f}"