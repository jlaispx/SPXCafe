from Database import Database
from datetime import datetime
from Customer import Customer

class Order(Database):

    # constructor - database data is retrieved into order object on construction
    def __init__(self,orderId=None, customer=None,dbName=None):
        if dbname:
            self.dbName = dbName #
        else:
            self.dbName = "SPXCafe.db"
        super().__init__(self.dbName)
        self.customer = customer # customer instance
        self.getOrder(orderId)

    # destructor - database is update at the completion/ending of the object life
    def __del__(self):
        if not self.saveOrder():
            print("Order: {self.orderId} failed saved")

    ## return object as a string for human reading
    def __str__(self):
         return f"Order: {self.orderId} - CustId: {self.customerId} - Order Date: '{self.orderDate}'"

    ##  DATABASE GETS/SETS ##
    def getOrder(self, orderId):
        if orderId:
            sql = f"SELECT orderId, customerId, orderDate FROM orders WHERE orderId = {orderId}"
            print(sql)
            orders = self.dbGetData(sql)
            for order in orders:
                self.orderId    = order['orderId']
                self.customerId = order['customerId']
                self.orderDate  = order['orderDate']
                self.customer = Customer(self.customerId)
        else:
            self.orderId = None
            self.customerId = None
            self.orderDate = None

    def saveOrder(self):
        retcode = False
        # validate compulsory data before saving
        if not self.orderDate:
            print("Order: Save: missing orderDate")
        elif not self.customerId:
            print("Order: Save: missing customerId")

        # if orderId exists - then update record otherwise insert new record
        if self.orderId:
            sql = f"UPDATE orders SET customerId={self.customerId}, orderDate='{self.orderDate}' WHERE orderId = {self.orderId}"
            self.dbChangeData(sql)
            retcode = True
        else:
            sql = f"INSERT INTO orders (customerId, orderDate) VALUES ({self.customerId},'{self.orderDate}')"
            self.orderId = self.dbPutData(sql)
            retcode = True

        return retcode

    # Get Lists of Orders for a Customer
    def getOrders(self):
        self.customerId = self.customer.getCustomerId()
        self.orders = []
        sql = "SELECT orderId, orderDate, customerId FROM orders "
        if self.customerId:
            sql += f"WHERE customerId = {self.customerId} "
        sql += "ORDER BY orderDate, orderId"
        orderData = self.dbGetData(sql)
        for order in orderData:
            self.orderId    = order['orderId']
            self.orderDate  = order['orderDate']
            self.customer.addOrder(self)


    ## Object GETS/SETS
    def getOrderId(self):
        return self.orderId

    def getCustomerId(self):
        return self.customerId

    def getOrderDate(self):
        return self.orderDate

    def setOrderId(self,orderId):
        self.orderId = orderId

    def setCustomerId(self, customerId):
        self.customerId = customerId

    def setOrderDate(self,orderDate):
        self.orderDate = orderDate


def main():
    dbname = "SPXCafe.db"
    order = Order(1)
    print(order)

    order = Order()
    order.setCustomerId(1)
    order.setOrderDate(datetime.today().date().strftime('%Y-%m-%d'))
    order.saveOrder()
    print(order)

if __name__ == "__main__":
    main()