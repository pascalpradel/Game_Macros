import keyboard
import time

class Macro(object):
    def __init__(self):
        print("Init started..")

    def start(self):
        time.sleep(5)
        print("Started..")
        key = False
        isPressed = False

        while True:
            if keyboard.is_pressed('ctrl') == False:
                if isPressed == True:
                    key = True
                    isPressed = False

            if keyboard.is_pressed('ctrl') == True:
                if isPressed == False:
                    key = True
                    isPressed = True

            time.sleep(0.02)
            if key:
                keyboard.release('ctrl')
                keyboard.press_and_release('ctrl')
                print("Pressed")
                key = False
            
            
            

if __name__ == "__main__":
    macro = Macro()
    macro.start()