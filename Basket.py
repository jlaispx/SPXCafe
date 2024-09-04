class Basket():
    '''Basket Class:
        This is used to collect BasketItems - containing Meals and Quantities
        This is then processed to create an Order once complete
    '''

    def __init__(self):
        self.__basket = []
        self.setBasketTotal(0)
        self.setMinOrderLevel(3)

    '''GETTERS AND SETTERS '''
    def setBasket(self,basket=None):
        self.__basket = basket

    def setBasketTotal(self,total=None):
        if total:
            self.__basketTotal = total
        else:
            self.__basketTotal = 0

    def setMinOrderLevel(self,minOrderLevel=0):
        self.__minOrderLevel = minOrderLevel


    def getBasket(self):
        return self.__basket

    def getBasketTotal(self):
        return self.__basketTotal

    def getBasketCount(self):
        return len(self.__basket)

    def getMinOrderLevel(self):
        return self.__minOrderLevel

    def addBasketTotal(self,cost):
        if cost:
            self.setBasketTotal(self.getBasketTotal()+cost)


    def addItem(self,basketItem=None):
        if basketItem:
            self.__basket.append(basketItem)
            self.addBasketTotal(basketItem.getCost())

    def displayBasket(self):
        print(f"{'-'*10} Basket {'-'*10}")
        if self.getBasketCount()>0:
            for basketItem in self.__basket:
                print(basketItem)
            print(f"Basket Total: ${self.getBasketTotal():.2f}")
        else:
            print("Basket currently has no items")

    def checkMinOrderLevel(self):
        if self.getBasketCount() >= self.getMinOrderLevel():
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
        if self.getMeal():
            return self.getMeal().getMealPrice() * self.getQuantity()
        else:
            return 0

    def __str__(self):
        return f"Meal: {self.getMeal()}, Quantity: {self.getQuantity()}  Cost: ${self.getCost():.2f}"