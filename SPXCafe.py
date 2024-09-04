from Database import Database
from datetime import datetime

class SPXCafe(Database):
    '''# Wrapper Class around Database specific for SPXCafe Database
    '''
    def __init__(self):
        '''Constructor Method - defaults SPXCafe database'''

        self.setConfidenceLevel(80)
        self.__dbname = "SPXCafe.db"
        super().__init__(self.__dbname)
        # print("Created SPXCafe Database")

    # === Assorted Utility Methods for ALL child classes

    def getToday(self):
        return datetime.today().date().strftime('%Y-%m-%d') #ISO format for dates - how sqlite as well mysql physically stores dates

    def setConfidenceLevel(self,confidenceLevel=80):
        self.__confidenceLevel = confidenceLevel

    def getConfidenceLevel(self):
        return self.__confidenceLevel

