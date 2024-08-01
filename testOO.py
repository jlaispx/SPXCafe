import abstractmethod

class Parent1():

    def out(self):
        print("out1")

    @abstractmethod
    def abs(self):
        pass

class Parent2():

    def out(self):
        print("out2")

class Child(Parent1, Parent2):

    # not necessary but
    def out(self):
        super().out()

    def abs(self):
        print("abs")

c = Child()
c.out()
c.abs()

# Output:
# out1