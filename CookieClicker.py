import keyboard
import time
import pyautogui

class CookieBot(object):
    def __init__(self):
        print("Init started..")
        self.pos_cookie = [390,628]

        self.pos_upgrade_cursor = [2272,279]
        self.pos_achievement_x = [1410,1341]

        self.color_available = [154,152,137]
        self.color_not_available = [98,106,102]

        self.color_backround = [20,50,70]

        #Database:
        self.start_max = 25
        # X / Y / counter / max_buy
        self.building_cursor = [2470,380,0,self.start_max]
        self.building_grandma = [2470,447,0,self.start_max]
        self.building_farm = [2470,510,0,self.start_max]
        self.building_mine = [2470,575,0,self.start_max]
        self.building_factory = [2470,640,0,self.start_max]

        self.buy_upgrades = True
        self.buy_buildings = True

        self.last_buy = 0
        self.last_buy_max = 20

        self.round_since_buy = 0
        self.round_value_when_skipped = 10
        self.color_last_upgrade = [0,0,0]

        self.klicks_per_run = 60
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
                    self.click(self.building_cursor[0], self.building_cursor[1], 1)
                    self.building_cursor[2] +=1
                elif screen_data[1] == 1 and screen_data[2]:
                    self.click(self.building_grandma[0], self.building_grandma[1], 1)
                    self.building_grandma[2] +=1
                elif screen_data[1] == 2 and screen_data[2]:
                    self.click(self.building_farm[0], self.building_farm[1], 1)
                    self.building_farm[2] +=1
                elif screen_data[1] == 3 and screen_data[2]:
                    self.click(self.building_mine[0], self.building_mine[1], 1)
                    self.building_mine[2] +=1
                elif screen_data[1] == 4 and screen_data[2]:
                    self.click(self.building_factory[0], self.building_factory[1], 1)
                    self.building_factory[2] +=1

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

        if self.building_cursor[2] < self.building_cursor[3]:
            item_id = 0
            pixel = screen.getpixel((self.building_cursor[0],self.building_cursor[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.building_grandma[2] < self.building_grandma[3]:
            item_id = 1
            pixel = screen.getpixel((self.building_grandma[0],self.building_grandma[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.building_farm[2] < self.building_farm[3]:
            item_id = 2
            pixel = screen.getpixel((self.building_farm[0],self.building_farm[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.building_mine[2] < self.building_mine[3]:
            item_id = 3
            pixel = screen.getpixel((self.building_mine[0],self.building_mine[1]))
            cursorIsAvailable = self.check_pixel(pixel,self.color_available)
            cursorIsNotAvailable = self.check_pixel(pixel,self.color_not_available)
        elif self.building_factory[2] < self.building_factory[3]:
            item_id = 4
            pixel = screen.getpixel((self.building_factory[0],self.building_factory[1]))
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

        """
        try:
            gc_location = screen.locateOnScreen('Golden_Cookie.png', grayscale=True)
            x = gc_location[0] + 30
            y = gc_location[1] + 30
            self.click(x,y,1)
        except:
            pass
        """

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
        if self.building_grandma[2] == self.start_max:
            self.building_cursor[3] = 40
        if self.building_farm[2] == self.start_max:
            self.building_cursor[3] = 55
            self.building_grandma[3] = 40
        if self.building_mine[2] == self.start_max:
            self.building_cursor[3] = 70
            self.building_grandma[3] = 55
            self.building_farm[3] = 40
        if self.building_factory[2] == self.start_max:
            self.building_cursor[3] = 85
            self.building_grandma[3] = 70
            self.building_farm[3] = 55
            self.building_mine[3] = 40



if __name__ == "__main__":
    bot = CookieBot()
    bot.start()