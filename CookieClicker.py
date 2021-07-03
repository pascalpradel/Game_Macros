import keyboard
import time
import pyautogui

class CookieBot(object):
    def __init__(self):
        print("Init started..")
        self.pos_cookie = [390,628]
        self.pos_cursor = [2470,380]
        self.pos_grandma = [2470,447]
        self.pos_farm = [2470,510]
        self.pos_mine = [2470,575]
        self.pos_factory = [2470,640]
        self.pos_upgrade_cursor = [2272,279]
        self.pos_achievement_x = [1410,1341]

        self.color_available = [154,152,137]
        self.color_not_available = [98,106,102]

        self.color_backround = [20,50,70]

        self.counter_cursor = 0
        self.counter_grandma = 0
        self.counter_farm = 0
        self.counter_mine = 0
        self.counter_factory = 0

        self.buy_upgrades = True
        self.buy_buildings = True

        self.last_buy = 0
        self.last_buy_max = 20

        self.round_since_buy = 0
        self.round_value_when_skipped = 10
        self.color_last_upgrade = [0,0,0]

        self.klicks_per_run = 60
        self.max_buy = 25
        self.abweichung = [25,25,25] #in Pixeln pro wert
        print("Init ready..")
        

    def start(self):
        run_counter = 1
        skip_buy = False

        time.sleep(2)
        print("Started..")

        while True:
            skip_buy = False

            if keyboard.is_pressed('esc') == True:
                print("Bye..")
                exit()

            screen_data = self.screen_read()

            #self.click(self.pos_achievement_x[0], self.pos_achievement_x[1], 1)

            print("Run: " + str(run_counter) + " Skip: " + str(self.round_since_buy) + "/" + str(self.round_value_when_skipped))
            print(screen_data)

            if self.round_since_buy <= self.round_value_when_skipped:
                if screen_data[0] and self.buy_upgrades:
                    skip_buy = True
                    self.click(self.pos_upgrade_cursor[0], self.pos_upgrade_cursor[1], 1)

            if skip_buy == False:
                if screen_data[1] == 0 and screen_data[2]:
                    self.click(self.pos_cursor[0], self.pos_cursor[1], 1)
                    self.counter_cursor +=1
                elif screen_data[1] == 1 and screen_data[2]:
                    self.click(self.pos_grandma[0], self.pos_grandma[1], 1)
                    self.counter_grandma +=1
                elif screen_data[1] == 2 and screen_data[2]:
                    self.click(self.pos_farm[0], self.pos_farm[1], 1)
                    self.counter_farm +=1
                elif screen_data[1] == 3 and screen_data[2]:
                    self.click(self.pos_mine[0], self.pos_mine[1], 1)
                    self.counter_mine +=1
                elif screen_data[1] == 4 and screen_data[2]:
                    self.click(self.pos_factory[0], self.pos_factory[1], 1)
                    self.counter_factory +=1

            if screen_data[3] == True:
                self.last_buy += 1
            else:
                self.last_buy = 0
            
            if self.last_buy >= self.last_buy_max:
                self.last_buy = 0
                self.round_since_buy = 0

            self.click(self.pos_cookie[0], self.pos_cookie[1], self.klicks_per_run)

            run_counter += 1

            self.game_rule()


    def screen_read(self):
        item_id = 0
        screen = pyautogui.screenshot()

        if self.counter_cursor < self.max_buy:
            item_id = 0
            pixel = screen.getpixel((self.pos_cursor[0],self.pos_cursor[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.counter_grandma < self.max_buy:
            item_id = 1
            pixel = screen.getpixel((self.pos_grandma[0],self.pos_grandma[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.counter_farm < self.max_buy:
            item_id = 2
            pixel = screen.getpixel((self.pos_farm[0],self.pos_farm[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.counter_mine < self.max_buy:
            item_id = 3
            pixel = screen.getpixel((self.pos_mine[0],self.pos_mine[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.counter_factory < self.max_buy:
            item_id = 4
            pixel = screen.getpixel((self.pos_factory[0],self.pos_factory[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)


        upgradeCursorIsAvailable = False
        pixel = screen.getpixel((self.pos_upgrade_cursor[0],self.pos_upgrade_cursor[1]))
        if self.check_pixel(pixel,self.color_backround) == False:
            upgradeCursorIsAvailable = True

        if  self.check_pixel_ohne_abweichung(pixel,self.color_last_upgrade) == True:
            self.round_since_buy += 1
        else:
            self.round_since_buy = 0
        
        self.color_last_upgrade = [pixel[0],pixel[1],pixel[2]]

        try:
            gc_location = screen.locateOnScreen('Golden_Cookie.png', grayscale=True)
            x = gc_location[0] + 30
            y = gc_location[1] + 30
            self.click(x,y,1)
        except:
            pass

        returnvalue = [upgradeCursorIsAvailable, item_id, cursorIsAvailable, cursorIsNotAvailable]
        return returnvalue

        
    def check_pixel(self, pixel, color_to_find):
        if pixel[0] > color_to_find[0] - self.abweichung[0] and pixel[0] < color_to_find[0] + self.abweichung[0]:
            if pixel[1] > color_to_find[1] - self.abweichung[1] and pixel[1] < color_to_find[1] + self.abweichung[1]:
                if pixel[2] > color_to_find[2] - self.abweichung[2] and pixel[2] < color_to_find[2] + self.abweichung[2]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def check_pixel_ohne_abweichung(self, pixel, color_to_find):
        if pixel[0] == color_to_find[0]:
            if pixel[1] == color_to_find[1]:
                if pixel[2] == color_to_find[2]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    def click(self, x, y, count):
        counter = 0
        pyautogui.moveTo(x, y)
        while counter < count:
            pyautogui.click()
            counter +=1

    def game_rule(self):
        if self.counter_grandma >= 20: ##mx buy modifikator hinzufügen
            self.counter_cursor = 35
        if self.counter_farm >= 20:
            self.counter_cursor = 50
            self.counter_grandma = 35
        if self.counter_mine >= 20:
            self.counter_cursor = 65
            self.counter_grandma = 50
            self.counter_farm = 35
        if self.counter_factory >= 20:
            self.counter_cursor = 80
            self.counter_grandma = 65
            self.counter_farm = 50
            self.counter_mine = 35



if __name__ == "__main__":
    bot = CookieBot()
    bot.start()