import pyautogui

x = 818
y = 493

flag = pyautogui.locateOnScreen('two.PNG', region=(x, y, 110, 110), grayscale=True, confidence=0.9)
screen = pyautogui.screenshot('test.png',region=(x, y, 110, 110))
#flag = pyautogui.locateOnScreen('flag.PNG', grayscale=True)

print(flag)
