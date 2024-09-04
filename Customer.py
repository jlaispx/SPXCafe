import Order
# import Meal
# from OrderItem import OrderItem
from Basket import Basket, BasketItem
from SPXCafe import SPXCafe

class Customer(SPXCafe):
    '''Customer Class'''

    def __init__(self, userName=None, customerId=None,firstName=None,lastName=None):
        ''' Constructor Method:
            Arguments:
                - must be either userName or customerId if existing
                - no customerId if new Customer requested
                - first name and last name can be passed in constructor to update or insert
                - more
        '''
        super().__init__()

        self.setCustomerId(customerId)
        self.setUserName(userName)
        self.setFirstName(firstName)
        self.setLastName(lastName)
        self.setOrders()

        # If customer exists in database - retrieve data
        if self.existsDB():
            if not self.setCustomer():
                print(f"Existing Customer: Either Customer Id <{self.getCustomerId()}> or UserName <{self.getUserName()}> is invalid ")


    # ------------ set up customer object data ------------

    def existsDB(self):
        '''Check if object already exists in database'''
        retcode = False
        sql = None
        if self.getCustomerId():
            sql = f"SELECT count(*) AS count FROM customers WHERE customerId={self.getCustomerId()}"
            # print(sql)
        elif self.getUserName():
            sql = f"SELECT count(*) AS count FROM customers WHERE userName='{self.getUserName()}'"
        if sql:
            countData = self.dbGetData(sql)
            if countData:
                for countRec in countData:
                    count = int(countRec['count'])
                if count > 0:
                    retcode = True
        return retcode

    @classmethod
    def findCustomer(cls, userName):
        ''' Uses the Username to find a customer and return a Customer object matching it
            findCustomer is a Class Method - that returns an object.

            This is because we do not have a ready list of customer objects to scan through.

            So we need to rely on a DB SQL search to find the customer by userName - similar to existsDB method which is an instance method not a class method.

            Once we are sure it exists in the database, we can then create a new customer object
            passing it the userName - that customer object retrieves all the order information as part of
            its construction
        '''
        customer = None
        spxcafe = SPXCafe()
        if userName:
            sql = f"SELECT count(*) AS count FROM customers WHERE userName='{userName}'"
            if sql:
                countData = spxcafe.dbGetData(sql)
                if countData:
                    for countRec in countData:
                        count = int(countRec['count'])
                    if count > 0:
                        # create a customer object for the username if found
                        customer = Customer(userName=userName)
        return customer

    def setCustomer(self,userName=None,customerId=None):
        ''' Creates Customer Object from database info
            Arguments: either userName or customerId
        '''
        retcode = False
        if userName:
            self.setUserName(userName)
        if customerId:
            self.customerId(customerId)
        customerData = None
        if self.getCustomerId():  #customer must exist
            sql = f'''
                SELECT customerId, userName, firstName, lastName
                FROM customers
                WHERE customerId = {self.getCustomerId()}
                ORDER BY customerId
            '''
        # either NEW customer or EXISTING get using userName
        elif self.getUserName():
            sql = f'''
                SELECT customerId, userName, firstName, lastName
                FROM customers
                WHERE userName = '{self.getUserName()}'
                ORDER BY customerId
            '''
        # print(sql)
        customerData = self.dbGetData(sql)

        if customerData:
            # Exiting Customer - should only be ONE customer
            for customer in customerData:
                self.setCustomerId(customer['customerId'])
                self.setUserName(customer['userName'])
                self.setFirstName(customer['firstName'])
                self.setLastName(customer['lastName'])
                # Call ORDER factory method to return a list of Order objects/instances - pass self to it
                self.setOrders(Order.Order.getOrders(self))
                retcode = True

        return retcode

    def save(self):
        '''Save Customer to Database'''

        if self.existsDB():
            sql = f'''UPDATE customers SET
                customerId = {self.getCustomerId()},
                userName = '{self.getUserName()}',
                firstName = '{self.getFirstName()}',
                lastName = '{self.getLastName()}'
            WHERE customerId={self.getCustomerId()}'''
            self.dbChangeData(sql)
        else:
            sql = f'''INSERT INTO customers (userName, firstName, lastName) VALUES
                ('{self.getUserName()}','{self.getFirstName()}','{self.getLastName()}')'''
            print(sql)
            # self.customerId = self.dbPutData(sql)
            self.setCustomerId(self.dbPutData(sql))

    # ----- get/sets customer data  -------

    def getCustomerName(self):
        ''' get the customer full name for reporting, display etc'''
        return f"{self.firstName} {self.lastName}"

    def getFirstName(self):
        return f"{self.firstName}"

    def getLastName(self):
        return f"{self.lastName}"

    def getCustomerId(self):
        return self.customerId

    def getUserName(self):
        return self.userName

    def getOrders(self):
        '''return a list of order obects for this customer'''
        return self.orders

    def setCustomerId(self,customerId):
        self.customerId = customerId

    def setUserName(self,userName):
        self.userName = userName

    def setFirstName(self,firstName):
        self.firstName = firstName

    def setLastName(self,lastName):
        self.lastName = lastName

    def setOrders(self,orders=None):
        '''orders contain a list of existing orders or an empty list'''
        if orders:
            self.orders = orders
        else:
            self.orders = []

    def addOrder(self, order):
        self.orders.append(order)

    # ----- formatted displays -------
    # str function allows you to simply print(customerInstance)
    def __str__(self):
        return f"Customer: ({self.getCustomerId():2d}) - <{self.userName}> {self.getFirstName()} {self.getLastName()} "

    # this requires customerInstance.displayCustomer()
    def display(self):
        '''formal display of the customer'''
        print(f"{"-"*25} Customer Details  {"-"*25}")
        print(f"Customer: {self.getCustomerId()}")
        print(f"Name: <{self.getUserName()}> {self.getCustomerName():50s}")
        # print(self)

    # Go through list of orders and
    # use the Order object to print itself
    def displayOrders(self):
        self.display()

        heading = " Customer Order History  "
        print(f"\n{"-"*22}{heading}{"-"*22}\n")
        if self.orders:
            for order in self.orders:
                order.display()
        else:
            print("Customer: No orders for customer")

    # ----- Adhoc methods

    def newOrder(self, basket=None):
        ''' create a new Order and ask it to add the meals'''
        if basket:
            order = Order.Order(customer=self)
            order.save()
            # For each meal object ask the Order to add an OrderItem
            order.addBasket(basket=basket)

            # rebuild the customer's orders list
            self.setOrders(Order.Order.getOrders(self))
            # return the order for further processing
        else:
            order = None
        return order


def main():
    bloggs = Customer.findCustomer("bloggs")
    bloggs.display()
    bloggs.displayOrders()

    # #new customer called jim jones - if exists returns existing customer
    # jones = Customer(userName="jonesj4",firstName="Jim",lastName="Jones")
    # jones.save()
    # jones.display()

    # # Simulate getting a list of meals to add to an Order
    # basket = Basket()
    # items = 3
    # quantity=0
    # for mealId in range(3,items+4):
    #     meal = Meal.Meal(mealId=mealId)
    #     quantity += 1
    #     basketItem = BasketItem(meal, quantity)
    #     basket.addItem(basketItem)

    # basket.displayBasket()

    # order = jones.newOrder(basket)
    # order.display()

    # orders = jones.getOrders()
    # for order in orders:
    #     order.display()

if __name__=="__main__":
    main()
