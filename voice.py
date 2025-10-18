import speech_recognition
#import pyttsx3
import pyautogui
from pynput.keyboard import Controller, Key
import time

recognizer = speech_recognition.Recognizer()
# engine = pyttsx3.init()
keyboard = Controller()

known_words_nomod = {
    "one": "q",
    "two": "w",
    "three": "e",
    "four": "r",
    "five": "t",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}
known_words_control={
    "check": "d"
}

def press_keyboard(button, duration=0.1):        
    keyboard.press(button)
    print(f"pressing {button}, for {duration} seconds") 
    time.sleep(duration)
    keyboard.release(button)

def press_mouse(b="left"):
    pyautogui.click(button=b)

def vc_control():
    print("ctrl")
    if keyboard.ctrl_pressed:
        print("released ctrl")
        keyboard.release(Key.ctrl)
    else:
        print("pressed ctrl")
        keyboard.press(Key.ctrl)

def vc_shift():
    print("shift")
    if keyboard.shift_pressed:
        print("released shift")
        keyboard.release(Key.shift)
    else:
        print("pressed shift")
        keyboard.press(Key.shift)

while True:
    try:
        with speech_recognition.Microphone(device_index=2) as mic:
            print("listening...")
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
                    press_keyboard(press)
                elif last_char=="2":
                    press="w"
                    press_keyboard(press)
                elif last_char=="3":
                    press="e"
                    press_keyboard(press)
                elif last_char=="4":
                    press="r"
                    press_keyboard(press)
                elif last_char=="5":
                    press="t"
                    press_keyboard(press)
                elif last_char=="6":
                    press_mouse("middle")
                elif last_char=="7":
                    press_mouse("right")
                else:
                    press=last_char
                    press_keyboard(press)

            # 2) Otherwise, check the last word
            else:
                last_word = text.split()[-1]
                if last_word in known_words_nomod:
                    key = known_words_nomod[last_word]
                    press_keyboard(key)
                    print(f"Pressed key: {key}")
                elif last_word=="control":
                    vc_control()
                elif last_word=="enchanting":
                    vc_shift()
                    
                    
    except speech_recognition.UnknownValueError:
        recognizer=speech_recognition.Recognizer()
