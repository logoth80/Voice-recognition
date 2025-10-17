import speech_recognition
import pyttsx3
from pynput.keyboard import Controller
import time

recognizer = speech_recognition.Recognizer()
engine = pyttsx3.init()
keyboard = Controller()

known_words = {
    "one": "q",
    "two": "w",
    "three": "e",
    "four": "r",
    "five": "t",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "house": "shift+d"
}

def press_keyboard(button, modifier=None, duration=0.1):
        
    keyboard.press(button)
    time.sleep(duration)
    keyboard.release(button)

    print(f"pressing {button}, for {duration} seconds")

def press_combo(modifier, button, duration=0.1):

    print(f"pressing {modifier} + {button}")

while True:
    try:
        with speech_recognition.Microphone(device_index=2) as mic:
            print("listening...")
            #recognizer.adjust_for_ambient_noise(mic,duration=0.2)
            #audio=recognizer.listen(mic)
            audio=recognizer.listen(mic, phrase_time_limit=2)
            text=recognizer.recognize_google(audio)
            print(text)

            if not text:
                continue

            last_char = text[-1]

            # 1) If the last character is a digit
            if last_char.isdigit():
                if last_char=="1":
                    press="q"
                elif last_char=="2":
                    press="w"
                elif last_char=="3":
                    press="e"
                elif last_char=="4":
                    press="r"
                elif last_char=="5":
                    press="t"
                else:
                    press=last_char

                press_keyboard(press)

            # 2) Otherwise, check the last word
            else:
                last_word = text.split()[-1]
                if last_word in known_words:
                    key = known_words[last_word]
                    press_keyboard(key)
                    print(f"Pressed key: {key}")
                    
    except speech_recognition.UnknownValueError:
        recognizer=speech_recognition.Recognizer()
