#amatourish atempt to get VoiceAttack alternative for linux. Hardcoded functions and no GUI

import speech_recognition
import pyautogui
from pynput.keyboard import Controller, Key
import time
import keyboard as kb
import threading # 👈 **Import the threading module**
import pygame

recognizer = speech_recognition.Recognizer()
keyboard = Controller()
# 👇 **Global variable to control the clicking thread**
clicking_thread_running = False 
# 👇 **Global variable to store the clicking thread instance**
clicking_thread = None

pygame.init() #for sounds

known_words_nomod = {
    "one": "q",
#    "two": "w",
    "three": "e",
    "four": "r",
    "for": "r",
    "five": "t",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "portal":"8",
    "nine": "9",
    "inventory": "i",
    "options": "o",
    "character": "c",
    "stats": "c",
    "potion": "1",
    "mana": "5",
    "speed": "4"
}

known_words_control={
    "price": "d",
    "track": "d"
}

def play_sound(what_sound):
    sound = pygame.mixer.Sound(what_sound)
    sound.play()

def press_keyboard(button, duration=0.1, contineous=False, mod=None):
    if not contineous:
        if mod == "control":
            keyboard.press(Key.ctrl)
            keyboard.press(button)
            time.sleep(duration)
            keyboard.release(button)
            keyboard.release(Key.ctrl)
            print(f"pressing {mod}+{button}, for {duration} seconds") 
        else:
            keyboard.press(button)
            print(f"pressing {button}, for {duration} seconds") 
            time.sleep(duration)
            keyboard.release(button)
    else:
        if kb.is_pressed(button):
            keyboard.release(button)
            print(f"released {button}")
            play_sound("released w.wav")
        else:
            keyboard.press(button)
            print(f"pressed {button}")
            play_sound("pressed w.wav")


def press_mouse(b="left"):
    pyautogui.click(button=b)

def vc_cancel():
    global clicking_thread_running, clicking_thread
    print("releasing alt+alt_gr+shift+ctrl+q+w")
    keyboard.release(Key.alt)
    keyboard.release(Key.alt_gr)
    keyboard.release(Key.shift)
    keyboard.release(Key.ctrl)
    keyboard.release("q")
    keyboard.release("w")
    if clicking_thread_running:
        # If running, stop it
        clicking_thread_running = False
    #pyautogui.mouseUp(button="secondary")
    play_sound("released w.wav")

def clicking_task(): # 👈 **Renamed the loop function for clarity**
    """The actual clicking loop function to be run in a thread."""
    global clicking_thread_running
    print("keep clicking: loop started")
    maxTime=20
    startTime=time.time()
    # 👇 **Use the global flag to control the loop**
    while clicking_thread_running and not kb.is_pressed('space'):
        pyautogui.click(button="left")
        time.sleep(0.05)
        if time.time()-startTime>maxTime:
            print('timed out')
            break # Exit the loop if time limit reached
    
    # 👇 **Ensure the flag is set to False when the loop exits naturally**
    clicking_thread_running = False 
    print("keep clicking: loop stopped")


def vc_keepclicking():
    """Starts or stops the continuous clicking thread."""
    global clicking_thread_running, clicking_thread

    if clicking_thread_running:
        # If running, stop it
        clicking_thread_running = False
        if clicking_thread and clicking_thread.is_alive():
            clicking_thread.join(timeout=0.2) # Wait a bit for the thread to stop
            print("Stopped continuous clicking.")
    else:
        # If not running, start it
        clicking_thread_running = True
        # 👇 **Create and start a new thread**
        clicking_thread = threading.Thread(target=clicking_task) 
        clicking_thread.daemon = True # Make it a daemon thread (optional, but good practice)
        clicking_thread.start()
        print("Started continuous clicking.")


def vc_escape():
    vc_cancel()
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)

def vc_priceCheck():
    print("check price")
    keyboard.press(Key.ctrl)
    keyboard.press(Key.alt_gr)
    keyboard.press('d')
    keyboard.release('d')
    keyboard.release(Key.alt_gr)
    keyboard.release(Key.ctrl)

def vc_map():
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)

def vc_control():
    print("ctrl")
    if keyboard.ctrl_pressed:
        print("released ctrl")
        keyboard.release(Key.ctrl)
        play_sound("released control.wav")
    else:
        print("pressed ctrl")
        keyboard.press(Key.ctrl)
        play_sound("pressed control.wav")


def vc_shift():
    print("shift")
    if keyboard.shift_pressed:
        print("released shift")
        keyboard.release(Key.shift)
        play_sound("released shift.wav")
    else:
        print("pressed shift")
        keyboard.press(Key.shift)
        play_sound("pressed shift.wav")

while True:
    try:
        with speech_recognition.Microphone(device_index=2) as mic:
            print("listening...")
            # 👇 **Check if a clicking thread is running and print its status**
            if clicking_thread_running:
                print("Continuous clicking is active. Press SPACE or say 'cancel' to stop.")
            
            audio=recognizer.listen(mic, phrase_time_limit=1.8)
            text=recognizer.recognize_google(audio).lower()

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
                    press_keyboard(press, contineous=True)
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
                last_word = last_word.lower()
                if last_word in known_words_nomod:
                    key = known_words_nomod[last_word]
                    press_keyboard(key)
                    print(f"Pressed key: {key}")
                elif last_word in known_words_control:
                    key = known_words_control[last_word]
                    press_keyboard(key, mod="control")

            # 3) If the last word requires a specific action
                elif last_word in {"control", "central"}:
                    vc_control()
                elif last_word=="enchanting":
                    vc_shift()
                elif last_word=="two":
                    press_keyboard("w", contineous=True)
                elif last_word=="cancel":
                    vc_cancel()
                elif last_word=="house":
                    vc_keepclicking() # **This now manages the thread**
                elif last_word=="check":
                    vc_priceCheck()
                elif last_word=="map":
                    vc_map()
                elif last_word=="escape":
                    vc_escape()



                    
                    
    except speech_recognition.UnknownValueError:
        recognizer=speech_recognition.Recognizer()
    # 👇 **Handle the program termination gracefully**
    except KeyboardInterrupt:
        print("\nExiting program...")
        clicking_thread_running = False # Stop the clicking loop
        if clicking_thread and clicking_thread.is_alive():
            clicking_thread.join(timeout=0.2)
        break