from Avatar import Avatar
import time

class Chatbot():

    def __init__(self):
        self.waiter = Avatar()
        self.waiter.say("Hi how are you?")

def main():
    st1 = round(time.time() * 1000)
    c = Chatbot()
    et1 = round(time.time() * 1000)
    print(f"{et1-st1}")

if __name__ == "__main__":
    main()