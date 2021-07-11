import keyboard
import mouse
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
            if mouse.is_pressed('left') == False:
                if isPressed == True:
                    isPressed = False

            if mouse.is_pressed('left') == True:
                if isPressed == False:
                    key = True
                    isPressed = True

            if key:
                keyboard.press_and_release('l')
                print("Pressed")
                key = False
            
if __name__ == "__main__":
    macro = Macro()
    macro.start()