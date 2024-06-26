import pyttsx4
import speech_recognition as sr

class Avatar:
    '''
    Class: Avatar

    Description:
    Our Avatar is responsible for:
    1. Saying things - using text to speech
    2. Listening for things - using Speech Recognition

    It has its own personal instance data:
     1. Name / Gender to select voice
     2. Flags to display to screen or use manual input when needed

     -------------------------------------------------------------------
    # We use Text to Speech and Speech Recognition

    Pre-requisites:
    # Need to pre-install: pyttsx4, SpeechRecognition


    '''
    def __init__(self, name="Elsa"):
        ''' Constructor method - run when object first instantiated
            - Calls to Initialse TTS and SR
        '''
        self.name = name
        self.initVoice()
        self.initSR()
        # self.introduce()

    def initSR(self):
        ''' Intialise Speech Recognition '''
        self.sample_rate = 48000
        self.chunk_size = 2048
        self.r = sr.Recognizer()
        self.useSR = True  # set this to True if using Speech Recognition

    def initVoice(self):
        '''
        Method: Initialise Text to Speech
        '''
        self.__engine = pyttsx4.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1
        self.__voice = self.__voices[self.__vix].id
        self.__engine.setProperty('voice', self.__voice)
        self.__engine.setProperty('rate', 150)
        self.__engine.setProperty('volume', 1.0)

    def say(self, words, display=False):
        if display:
            print(words)
        self.__engine.say(words, self.name)
        self.__engine.runAndWait()

    def listen(self, prompt="I am listening, please speak:",useSR=None):
        words = ""
        if useSR==None:
            useSR = self.useSR

        if useSR:
            try:
                #print(sr.Microphone.list_microphone_names())
                with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
                    # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    self.r.adjust_for_ambient_noise(source)
                    self.say(prompt)
                    audio = self.r.listen(source)
                try:
                    #print("You said: '" + r.recognize_google(audio)+"'")
                    words = self.r.recognize_google(audio)
                except sr.UnknownValueError:
                    self.say("Could not understand what you said.")
                except sr.RequestError as e:
                    self.say("Could not request results; {0}".format(e))

            except:
                self.say(prompt, False)
                words = input(f"{prompt}")
        else:
            self.say(prompt, False)
            words = input(prompt)
        return words

    def introduce(self):
        self.say(f"Hello. My name is {self.name}")

# This is our test harness - that tests the Avatar functions to see if they work properly
def main():
    teacher = Avatar("Bob")
    # help(Avatar)
    # help(pyttsx4)
    teacher.say("How are you today?")
    # #word = "hello"
    # #for letter in word:
    # #    teacher.say(letter)
    teacher.say(f"You said: {teacher.listen("say something: ")}")

if __name__ == "__main__":
    main()