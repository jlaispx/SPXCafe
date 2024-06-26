from SPXCafe import SPXCafe
import OrderItem
from datetime import datetime

class Order(SPXCafe):
    '''
        Order Class:  Stores Order details for a Customer
    '''

    # def __init__(self,orderId=None, orderDate=None, customerId=None):
    def __init__(self,orderId=None, orderDate=None, customer=None):
        '''
            Constructor method
            - database data is retrieved into order object on construction if an orderId is provided
            - otherwise a new object is created and loaded with attribute information passed on construction
            - Note: a list of OrderItem objects are also retrieved - if they exist in the database.
        '''
        super().__init__()

        self.setOrderId(orderId)
        self.setOrderDate(orderDate)
        # get customer object and retrieve customer Id
        # cannot use customer object as circular referencing when
        # creating a new Customer when retrieving data from database
        self.setCustomer(customer)
        self.setOrderItems()

        # If order exists, then get attributes from Database
        if self.existsDB():
            if not self.setOrder(self.orderId):
                print(f"Order: Order Id <{self.getOrderId()}> is invalid ")

    def existsDB(self):
        '''Checks if order exists in database'''
        retcode=False

        if self.getOrderId():
            sql = f"SELECT count(*) AS count FROM orders WHERE orderId={self.getOrderId()}"
            # print(sql)
            countData = self.dbGetData(sql)
            if countData:
                for countData in self.dbGetData(sql):
                    count = int(countData['count'])
                if count > 0:
                    retcode = True
        return retcode


    ##  DATABASE GETS/SETS ##
    def setOrder(self, orderId):
        '''
            Set Order - retrieves data from database into the Object Attributes
            for an OrderId if exists.

            Returns True or False if DB data found or not.
        '''
        retCode = False
        if orderId:
            sql = f"SELECT orderId, orderDate, customerId FROM orders WHERE orderId = {orderId}"
            # print(sql)
            orderData = self.dbGetData(sql)  # should only be one
            if orderData:
                for order in orderData:
                    self.setOrderId(order['orderId'])
                    # self.setCustomerId(order['customerId'])
                    self.setCustomerId(order['customerId'])
                    self.setOrderDate(order['orderDate'])

                    # Using OOP Aggregation - we store a list of OrderItem objects with the Order.
                    # information for OrderItem is delegated to the OrderItem Objects
                    print("Getting orderitems - passing Order object")
                    self.setOrderItems(OrderItem.OrderItem.getOrderItems(self))
                retCode = True

        return retCode

    def saveOrder(self):
        ''' Save Order Method:
            Saves the Order details back to the database
            If existing Order: then UPDATES the data in the database
            If not existing Order: then INSERTS the data into database

            returns True or False if successful updated or inserted
        '''
        retcode = False
        # validate compulsory data before saving
        if not (self.orderDate and self.customer):
            print("Order: Save: missing mandatory data")
            print(self)
        # if orderId exists - then update record otherwise insert new record
        else:
            # Update Existing
            if self.orderId:
                sql = f"UPDATE orders SET customerId={self.getCustomerId()}, orderDate='{self.orderDate}' WHERE orderId = {self.orderId}"
                self.dbChangeData(sql)
                retcode = True
            else:
            # Insert NEW
                sql = f"INSERT INTO orders (customerId, orderDate) VALUES ({self.getCustomerId()},'{self.orderDate}')"
                self.orderId = self.dbPutData(sql)
                retcode = True

        return retcode

    def __str__(self):
        ''' returns object as a string for human reading
        '''
        return f"Order: {self.orderId:2d} - CustId: {self.getCustomerId():2d} - Order Date: '{self.orderDate}'"

    def display(self):

        print(self)
        if self.orderItems:
            for orderItem in self.orderItems:
                orderItem.display()
            print(f"{'-'*55} Order Total: ${self.getOrderTotal():6.2f}")
        else:
            print(f"{"-"*25} No Order Items {"-"*25}")

    # Get Lists of Orders for a Customer
    # - FACTORY METHOD THAT RETURNS A LIST OF INSTANCES OF THIS CLASS - takes the cls as the first parameter
    @classmethod
    def getOrders(cls, customer):

        sql = "SELECT orderId, orderDate, customerId FROM orders "
        if customer.getCustomerId():
            sql += f"WHERE customerId = {customer.getCustomerId()} "
        sql += "ORDER BY orderDate, orderId"
        ordersData = SPXCafe().dbGetData(sql)

        # Build a list of Order objects and return them
        orders = []
        for order in ordersData:
            newOrder =cls.__new__(cls)
            newOrder.orderId    = order['orderId']
            newOrder.orderDate  = order['orderDate']
            newOrder.customerId = order['customerId']
            newOrder.setOrderItems(OrderItem.OrderItem.getOrderItems(newOrder))
            orders.append(newOrder)
        return orders


    ## Object GETS/SETS
    def getOrderId(self):
        return self.orderId

    def getCustomer(self):
        '''return customer object related to this order'''
        return self.customer

    def getCustomerId(self):
        return self.customerId

    def getOrderDate(self):
        return self.orderDate

    def getOrderItems(self):
        return self.orderItems

    def getOrderTotal(self):
        total = 0
        if self.orderItems:
            for orderItem in self.orderItems:
                total += orderItem.getMealPrice()
        return total

    #-----------------------------------
    def setOrderId(self,orderId):
        self.orderId = orderId

    def setCustomer(self,customer):
        '''store customer object for order - use customer id from now '''
        self.customer = customer
        self.setCustomerId(self.customer.getCustomerId())

    def setCustomerId(self, customerId):
        self.customerId = customerId

    def setOrderDate(self,orderDate):
        self.orderDate = orderDate

    def setOrderItems(self,orderItems=None):
        '''
            Store a list of OrderItem objects with Order or empty list.
            Note: OrderItems List is retrieved by calling OrderItem Factory Method called getOrderItems()
        '''
        if orderItems:
            self.orderItems = orderItems
        else:
            self.orderItems = []
        # print(f"Set Order Items: {self.orderItems}")


def main():
# retrieve an order
    print("Getting Order 1 details")
    order = Order(1)
    print(order)
    order.display()

# create a new order
    print("Creating NEW order")
    order = Order()
    order.setCustomerId(1)
    order.setOrderDate(self.getToday())
    order.saveOrder()
    print(order)

if __name__ == "__main__":
    main()