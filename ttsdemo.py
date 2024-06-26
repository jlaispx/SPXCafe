import pyttsx4

engine = pyttsx4.init()

voices = engine.getProperty('voices')

for voice in voices:
    engine.setProperty('voice', voice.id)
    engine.say('this is an english text to voice test.')
    print(voice)
    engine.runAndWait()