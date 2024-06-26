from Course import Course
from Meal import Meal
from SPXCafe import SPXCafe

class Menu(SPXCafe):

    def __init__(self,menuName=None):
        '''Constructor Method for the Menu '''

        super().__init__()
        self.setMenuName(menuName)

        # Set the Menu to database values
        self.setMenu()

    # Getters and Setters for Menu -----------------------------------

    def setMenu(self):
        '''Setup Menu from database'''

        # Add Course Aggregations for this Menu - i.e. a list of Courses
        self.setCourses(Course.getCourses(self))

    def setMenuName(self,menuName=None):
        '''set the Menu Name - or default to "The Menu" '''
        if menuName:
            self.__menuName = menuName
        else:
            self.__menuName = "Lunch"

    def setCourses(self,courses=None):
        '''Set courses aggregation to list of courses or empty list'''
        if courses:
            self.__courses = courses
        else:
            self.__courses = []

    def getMenuName(self):
        '''return the Menu name'''
        return f"{self.__menuName}"

    def getCourses(self):
        '''return a list of courses available for this Menu'''
        return self.__courses

    # -------- output related methods -----------------
    def __str__(self):
        '''returns a string for the Menu object for printing this object'''
        return f"{self.getMenuName()} Menu"

    def display(self):
        '''Display this Menu instance more formally'''
        print(f"{'-'*25} {self.getMenuName()} {'-'*25}\n")

        if self.getCourses():
            for course in self.getCourses():
                course.display()

    def displayCourses(self):
        '''Display all the Courses in a comma-separated string '''
        print(f"Course List: ",end="")
        courseNames = []
        for course in self.getCourses():
            courseNames.append(course.getCourseName().title())
        print(", ".join(courseNames))
        print()

    # Adhoc Methods for Menu and aggregated Courses

    def findMeal(self, searchMeal=None):
        meals = []
        if searchMeal:
            for course in self.getCourses():
                meals += course.findMeal(searchMeal)
        return meals

    def findCourse(self, searchCourse=None):
        courses = []
        if searchCourse:
            for course in self.getCourses():
                courses.append(course.findCourse(searchCourse))
        return courses

def main():
    '''Test Harness to make sure all methods work'''
    menu = Menu("Ristorante Italia")
    menu.display()

    menu.displayCourses()

    # Find a meal - using fuzzy logic - finds partial
    searchMeal = input("What meal do you want? ")
    meals = menu.findMeal(searchMeal)
    if meals:
        print("We have found the following meals:")
        for meal in meals:
            meal.display()
    else:
        print(f"{searchMeal}' not found")

    searchCourse = input("What course do you want?")
    courses = menu.findCourse(searchCourse)
    if courses:
        print("We have found the following course(s): ")
        for course in courses:
            course.display()
    else:
        print(f"'{searchCourse}' not found")

if __name__=="__main__":
    main()