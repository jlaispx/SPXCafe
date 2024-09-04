from Database import Database
from datetime import datetime
from Order import Order

class Orders(Database):

    def __init__(self,orderId=None, customerId=None):
        super().__init__(dbname)
        self.orders = None
        self.customerId = customerId
        if customerId:
            self.orders = self.getOrders()

        #print(f"Construct Orders for Customer: {self.customerId}")

    def getOrders(self):

        sql = f"SELECT customerId, orderId, orderDate FROM orders WHERE customerId = {self.customerId} ORDER BY orderId"
        self.orders = self.dbGetData(sql)

        return self.orders

    def getOrder(self, orderId):

        sql = f"SELECT customerId, orderId, orderDate FROM orders WHERE orderId = {orderId}"
        self.order = self.dbGetData(sql)
        return self.order

    def getOrderItems(self, orderId=0):

        sql = f'''
            SELECT oi.orderId, oi.orderItemId, oi.mealId,m.mealName, oi.quantity, oi.mealPrice
            FROM orderItems AS oi, meals AS m
            WHERE oi.mealId = m.mealId AND
                orderId = {orderId}
            ORDER BY oi.orderId, oi.orderItemId
        '''
        # print(sql)

        self.orderItems = self.dbGetData(sql)

        return self.orderItems

    def displayDate(self,dbDate):
        #convert string date from db -> YYYY-MM-DD format to a Date object
        format = '%Y-%m-%d'
        dateObj = datetime.strptime(dbDate,format)
        format = '%d %b %Y'
        dateStr = dateObj.strftime(format)
        # newDate = datetime.datetime.strftime(dateStr,format)
        return dateStr

    def displayOrders(self):

        if self.customerId:
            #print(f"Customer Orders for Customer: {self.customerId}")

            # always get a fresh orders list in case a new order added
            orders = self.getOrders()

            for order in orders:
                orderId         = order['orderId']
                orderDate       = order['orderDate']
                print(f"Order #: {orderId} - Date Ordered: {self.displayDate(orderDate)}")
                orderItems = self.getOrderItems(orderId)
                orderTotal = 0
                rowId = 0
                for orderItem in orderItems:
                    rowId += 1
                    orderItemId = orderItem.getOrderItemId() #['orderItemId']
                    mealId      = orderItem['mealId']
                    mealName    = orderItem['mealName']
                    quantity    = orderItem['quantity']
                    mealPrice   = orderItem['mealPrice']
                    mealTotal   = quantity * mealPrice
                    orderTotal += mealTotal
                    print(f"Item# {rowId} <{orderItemId:2d}> : ({mealId}) {mealName.title():20s} ${mealPrice:6.2f} x {quantity} = ${mealTotal:6.2f}")
                print(f"{"-"*40} Order Total: ${orderTotal:6.2f} {"-"*7}")
        else:
            print("Orders: Customer not identified. Cannot show orders")

    def insertNewOrder(self):

        self.orderDate = datetime.today().date().strftime('%Y-%m-%d')
        if self.customerId:
            sql = f"INSERT INTO orders (customerId, orderDate) VALUES {self.customerId}, '{self.orderDate}'"
            newOrderId = self.dbPutData(sql)

    def insertNewOrderItem(self, orderId=None, mealId=None):
        pass



def main():
    customerId = 1
    orders = Orders('SPXCafe.db', customerId)
    orders.displayOrders()

if __name__=="__main__":
    main()