from Meal import Meal
import Order
from SPXCafe import SPXCafe

class OrderItem(SPXCafe):
    '''OrderItem Class extend SPXCafe Class'''

    def __init__(self, orderItemId=None, orderId=None, mealId=None, quantity=None, mealPrice=None):
        '''
        # Constructor Method
        # Creates a blank orderItem if no orderItemId
        # else Retrieves existing orderItem from Database
        '''

        super().__init__()

        self.setOrderItemId(orderItemId)
        self.setOrderId(orderId)
        self.setMealId(mealId)
        self.setQuantity(quantity)
        self.setMealPrice(mealPrice)

        # RETRIEVE EXISTING from Database IF OrderItem PK is passed in
        if self.getOrderItemId():
            if not self.setOrderItem(self.getOrderItemId()):
                print(f"Order Item: Order Item Id <{self.__orderItemId}> is invalid")

    # def __del__(self):
    #     ''' Destructor Method - save object to db on departure '''
    #     print(f"Deleting OrderItem: {self.getOrderItemId()}")
    #     try:
    #         if not self.saveOrderItem():
    #             print(f"OrderItem: {self.getOrderItemId()} - Failed save to database")
    #     except Exception as e:
    #         print(f"Order Item: Error {type(e)} - Failed Save: {e}")

    def __str__(self):
        ''' "To String" Method - returns an object as a string for human reading
'''
        return f"Order Item: {self.getOrderItemId():2d} - OrderId: {self.orderId:2d}, MealId: {self.mealId:2d} - Quantity: {self.quantity:2d} - MealPrice: ${self.mealPrice:6.2f}"

    def setOrderItem(self, orderItemId):
        '''Gets the Order Item details for an OrderItem from the database and sets the Object attributes with those values'''

        retCode = False
        if orderItemId:
            sql = f"SELECT orderItemId, orderId, mealId, quantity, mealPrice FROM orderItems WHERE orderItemId = {orderItemId}"
            orderItemData = self.dbGetData(sql)
            if orderItemData:
                for orderItem in orderItemData:
                    self.setOrderItemId(orderItem['orderItemId'])
                    self.setOrderId(orderItem['orderId'])
                    self.setMealId(orderItem['mealId'])
                    self.setQuantity(orderItem['quantity'])
                    self.setMealPrice(orderItem['mealPrice'])
                    print(f"Retrieve Order Item: {self.__orderItemId}, {self.orderId}, {self.mealId}, {self.quantity}, {self.mealPrice}")
                retCode = True
        return retCode

    def saveOrderItem(self):
        '''Saves Order Item to datbase - either as an Update for existing orderItem or an Insert of a new OrderItem (no orderItemId set yet)'''

        retCode = False
        # validate fields before saving
        if not(self.orderId and self.mealId and self.quantity and self.mealPrice):
            print("OrderItem: Save: Missing mandatory data")
            print(self)
        else:
            print(f"Saving Order Item: {self.__orderItemId}, {self.orderId}, {self.mealId}, {self.quantity}, {self.mealPrice}")
            # Update Existing
            if self.__orderItemId:
                sql = f"UPDATE orderItems SET orderId={self.orderId}, mealId={self.mealId}, quantity={self.quantity},mealPrice={self.mealPrice} WHERE orderItemId = {self.__orderItemId}"
                self.dbChangeData(sql)
                retCode = True
            else:
            # Insert New
                sql = f"INSERT INTO orderItems (orderId, mealId, quantity, mealPrice) VALUES {self.orderId, self.mealId, self.quantity, self.mealPrice}"
                print(f"Insert SQL: <{sql}>")
                self.setOrderItemId(self.dbPutData(sql))
                retCode = True
        return retCode

    def delete(self):
        '''Delete the current OrderItem from database '''

        if self.getOrderItemId():
            sql = "DELETE FROM orderItems WHERE orderItemId = {self.getOrderItemId()}"
            self.dbChangeData(sql)
            # Now initialise object to prevent further updates
            self.setOrderItemId(None)
            self.setOrderId(None)
            self.setMealId(None)
            self.setQuantity(None)
            self.setMealPrice(None)

    def display(self):
        '''formal display of orderItem'''
        # print("DISPLAY ORDER ITEM")
        # print(self)
        meal = Meal()
        if meal.setMeal(self.getMealId()):
            mealName = meal.getMealName().title()
        else:
            mealName = "<Unknown>"
        print(f"<{self.getOrderId():2d}-{self.getOrderItemId():2d}> ({self.getMealId():2d}) {mealName:30s} - ${self.getMealPrice():5.2f} ")

    # Get Lists of OrderItems for an Order
    # - FACTORY METHOD THAT RETURNS A LIST OF INSTANCES OF THIS CLASS - takes the cls as the first parameter
    @classmethod
    def getOrderItems(cls, order):
        '''
        input:      Order instance
        process:    Get order items for Order and build a OrderItem object list to return
        output:     a list of orderItems
        '''
        sql = f"SELECT orderItemId, orderId, mealId, quantity, mealPrice FROM orderItems WHERE orderId = {order.getOrderId()} ORDER BY orderItemId"

        orderItemsData = SPXCafe().dbGetData(sql)

        orderItems = []
        for orderItem in orderItemsData:
            newOrderItem = cls.__new__(cls)

            newOrderItem.setOrderItemId(orderItem['orderItemId'])
            newOrderItem.setOrderId(orderItem['orderId'])
            newOrderItem.setMealId(orderItem['mealId'])
            newOrderItem.setQuantity(orderItem['quantity'])
            newOrderItem.setMealPrice(orderItem['mealPrice'])
            # print(f"Class :Retrieve Order Item: {newOrderItem.orderItemId}, {newOrderItem.orderId}, {newOrderItem.mealId}, {newOrderItem.quantity}, {newOrderItem.mealPrice}")

            orderItems.append(newOrderItem)
        return orderItems

    ## Object GETS/SETS methods
    def getOrderItemId(self):
        return self.__orderItemId

    def getOrderId(self):
        return self.orderId

    def getMealId(self):
        return self.mealId

    def getQuantity(self):
        return self.quantity

    def getMealPrice(self):
        return self.mealPrice

    def setOrderItemId(self, orderItemId):
        self.__orderItemId = orderItemId

    def setOrderId(self, orderId):
        self.orderId = orderId

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setMealId(self, mealId):
        self.mealId = mealId

    def setMealPrice(self, mealPrice):
        self.mealPrice = mealPrice


def main():
    '''Test Harness for the OrderItem Class'''
# retrieve an order
    print("Retrieve Order Item 1:")
    orderItem = OrderItem(1)
    orderItem.display()
#    print(orderItem)

    print("Update Order Item")
    orderItem.setMealPrice(3.99)
    orderItem.saveOrderItem()
    orderItem.display()
#    print(orderItem)

# create a new order
    print("Create new OrderItem")
    orderItem = OrderItem()
    orderItem.setOrderId(6)
    orderItem.setMealId(1)
    orderItem.setQuantity(2)
    orderItem.setMealPrice(2.99)
    orderItem.saveOrderItem()
    orderItem.display()
#    print(orderItem)

if __name__ == "__main__":
    main()