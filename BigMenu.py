from SPXCafe import SPXCafe
from Menu import Menu
from Course import Course
from Meal import Meal


def main():

    menu = Menu(menuName="SPX Big Cafe")
    menu.displayCourses()
    courses = menu.getCourses()
    for course in courses:
        course.display()

    meal = Meal(mealId=1)                       # retrieve an existing Meal
    meal.display()                              # show existing values
    meal.setMealPrice(meal.getMealPrice()+1)    # update Meal data demo
    meal.save()                                 # save changes back to database
    meal = Meal(mealId=1)                       # get same meal again from DB
    meal.display()                              # show amended meal

    # Create a NEW Meal completetly
    course = Course(courseId=1)
    meal = Meal(mealName="Salata2",mealPrice=3.45,course=course)
    meal.save()
    meal.display()

    meal = Meal(mealName="Salata3",mealPrice=3.45,courseId=1)
    meal.save()
    meal.display()


if __name__=="__main__":
    main()