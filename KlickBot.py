import keyboard
import time
import pyautogui

class Macro(object):
    def __init__(self):
        print("Init started..")

    def start(self):
        time.sleep(5)
        print("Started..")

        while True:
            time.sleep(0.001)
            pyautogui.click()
            if keyboard.is_pressed('esc') == True:
                exit()

if __name__ == "__main__":
    macro = Macro()
    macro.start()