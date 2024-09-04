from SPXCafe import SPXCafe

class Customer(SPXCafe):

    def __init__(self,username=None):
        self.setFirstName("Joe")
        self.setLastName("Bloggs")
        self.setUsername(username)

    def setFirstName(self, firstName=None):
        self.__firstName = firstName

    def setLastName(self, lastName=None):
        self.__lastName = lastName

    def setUsername(self, username=None):
        self.__username = username

    def getFirstName(self):
        return self.__firstName

    def getLastName(self):
        return self.__lastName

    def getUsername(self):
        return self.__username
