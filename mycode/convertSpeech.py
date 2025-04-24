import speech_recognition
import pyttsx3

#יצירת אוביקט שיזהה את השמע
recognizer = speech_recognition.Recognizer()

while True:

    try:

        print("im listening")
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio=recognizer.listen(mic)

            text=recognizer.recognize_google(audio)#לא צריך לשלוח אנגלית זה הברירת מחדל
            text=text.lower()

            print(f"Recognized: {text}")
    except speech_recognition.UnknownValueError:
        recognizer=speech_recognition.Recognizer()
        #print("Could not understand the audio")
        continue
    except speech_recognition.RequestError as e:
        recognizer=speech_recognition.Recognizer()
        print(f"Could not request results; {e}")
        continue






# import speech_recognition as sr

# recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     print("I am listening...")
#     recognizer.adjust_for_ambient_noise(source, duration=0.1)
#     audio = recognizer.listen(source)

#     print("i finished listening")
#     try:
#         text = recognizer.recognize_google(audio)
#         print("זוהה: " + text)
#     except sr.UnknownValueError:
#         print("I dont understand what you said")
#     except sr.RequestError:
#         print("שגיאה בחיבור למנוע ההכרה של גוגל")