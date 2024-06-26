
class Menu:

    menu = {
        "starter": {
            "pumpkin soup" : 3.50,
            "garlic bread" : 2.50,
            "prawns": 7.50
        },
        "main" : {
            "steak" : 30.00,
            "fish" : 27.00,
            "salad" : 25.00,
            "minestrone" : 15.00
        },
        "dessert" : {
            "pavlova": 10.50,
            "ice cream": 9.75,
            "tiramisu": 15.00
        }
    }
    # Constructor - run when an instance of a class is requested
    def __init__(self):
        pass

    def getCourses(self):
        courses = list(self.menu.keys())  # get dict keys and convert to list
        return courses

    def showCourses(self):
        courses = self.getCourses()  # return list of courses
        for courseName in courses:   # print each course out
            print(f"> {courseName.title()}")

    def getMeals(self,course):
        meals = self.menu[course]
        return meals

    def showMealsForCourse(self, course):
        print(f"Meals in {course.title()} course are:")
        # returns a dict containing the meals and their price
        meals = self.getMeals(course)
        for mealName in meals:
            mealPrice = self.menu[course][mealName]
            print(f">>> {mealName.title():20s} ${mealPrice:.2f}")

    def chooseCourse(self):
        while True:
            choice = input("Which course do you want? (X to exit): ").lower().strip()
            if choice == "x":
                break
            print("------ MENU ------")
            if choice not in self.getCourses():
                print(f"{choice} is not a valid course. Try again")
                print(f"Choose from these courses:")
                self.showCourses()
            else:
                self.showMeals(choice)
                break

    def showMeals(self):
        print("------ MENU ------")
        for courseName in self.getCourses():
            print(f"Course: {courseName.title()}")
            self.showMealsForCourse(courseName)



# Create an instance/object of the Class: Menu
def main():
    m = Menu() # create an instance of a menu
    print(m.getCourses())   #call the instance method
    m.showCourses()
    m.showMealsForCourse('starter')
    m.showMeals()


if __name__=="__main__":
    main()

