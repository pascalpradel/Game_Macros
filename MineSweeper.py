import time
import pyautogui

class MineSweeperBot(object):
    def __init__(self):
        print("Init started..")
        self.count_rows = 9
        self.count_lines = 9

        #self.board = [[False] * self.count_rows,[False] * self.count_lines]
        
        self.board = [[0 for x in range(self.count_rows)] for y in range(self.count_lines)] 
        self.prob_board = [[0 for x in range(self.count_rows)] for y in range(self.count_lines)] 

        self.color_blue = [124,210,255]
        self.color_board = [255,255,255]
        self.color_flag = [250,211,62]
        self.color_one = [25,289,224]
        self.color_two = [134,165,60]
        self.color_three = [216,26,101]

        self.start_point = [580,136]

        self.box_size = [113,110]
        self.abstand_x = 6.5
        self.abstand_y = 9

        self.abweichung = [25,25,25] #in Pixeln

        print("Init ready..")
        

    def start(self):
        time.sleep(2)
        print("Started..")
        self.fill()
        self.screen_read()
        #print(self.board)

        self.fill_probability()
        print(self.prob_board)


    def fill_probability(self):
        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                self.prob_board[j][i] = 0
                j += 1
            i += 1
            j = 0

        i = 0
        j = 0
        
        while i < self.count_rows:
            while j < self.count_lines:
                percentage = 0
                box = self.board[i][j]

                x = i
                y = j
                item_id = box[2]
                

                if item_id >= 2:
                    if item_id == 2:
                        percentage = 100
                    elif item_id == 3:
                        percentage = 200
                    elif item_id == 4:
                        percentage = 300
                    ##USW

                    box_field = [[0 for x in range(3)] for y in range(3)]
                    
                    counter_x = -1
                    counter_y = -1

                    blue_counter = 0

                    while counter_x < 2:
                        while counter_y < 2:
                            if x+counter_x >= 0 and y+counter_y >= 0 and x+counter_x <= self.count_rows and y+counter_y <= self.count_lines:
                                box_data = self.board[x+counter_x][y+counter_y]
                                field_input = [x+counter_x, y+counter_y, box_data[2]]
                                box_field[counter_x+1][counter_y+1] = field_input
                                if box_data[2] == 0:
                                    blue_counter += 1
                            else:
                                box_field[counter_x+1][counter_y+1] = [404,404,404]

                            counter_y += 1
                        counter_y = -1
                        counter_x += 1

                    if blue_counter > 0:
                        a_iterator = 0
                        b_iteraror = 0

                        while a_iterator < 3:
                            while b_iteraror < 3:
                                box_field_data = box_field[a_iterator][b_iteraror]
                                if box_field_data[2] == 0:
                                    self.prob_board[box_field_data[0]][box_field_data[1]] += int(percentage/blue_counter)
                                b_iteraror += 1
                            a_iterator += 1
                            b_iteraror = 0
                    
                    #print("X: " + str(x) + " " + "Y: " + str(y))
                    #print(box)
                    #print(box_field)

                j += 1
            i += 1
            j = 0



    def fill(self):
        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                x = int((self.start_point[0]) + (self.box_size[0]/2) + (i*self.box_size[0]) + (i*self.abstand_x))
                y = int((self.start_point[1]) + (self.box_size[1]/2) + (j*self.box_size[1]) + (j*self.abstand_y))

                input_data = [x,y,0]
                self.board[j][i] = input_data

                j += 1
            i += 1
            j = 0

    
    def screen_read(self):
        screen = pyautogui.screenshot()
        i = 0
        j = 0
        
        while i < self.count_rows:
            while j < self.count_lines:
                box = self.board[j][i]
                pixel = screen.getpixel((box[0],box[1]))
                
                if self.check_pixel(pixel, self.color_blue, self.abweichung):
                    box_id = 0 #"BLAU"
                elif self.check_pixel(pixel, self.color_board, self.abweichung):
                    box_id = 1 #"WEIß" 
                elif self.check_pixel(pixel, self.color_one, [25,120,25]):
                    box_id = 2 #"EINS"
                elif self.check_pixel(pixel, self.color_two, [80,70,130]):
                    box_id = 3 #"ZWEI"
                elif self.check_pixel(pixel, self.color_three, self.abweichung):
                    box_id = 4 #"DREI"
                else:
                    print("Error: Color not found at: " + str(i+1) + "/" + str(j+1))
                    print(pixel)
                    box_id = 404

                box[2] = box_id
                self.board[j][i] = box

                j += 1
            i += 1
            j = 0


    def check_pixel(self, pixel, color_to_find, abweichung):
        if pixel[0] > color_to_find[0] - abweichung[0] and pixel[0] < color_to_find[0] + abweichung[0]:
            if pixel[1] > color_to_find[1] - abweichung[1] and pixel[1] < color_to_find[1] + abweichung[1]:
                if pixel[2] > color_to_find[2] - abweichung[2] and pixel[2] < color_to_find[2] + abweichung[2]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def leftclick(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click(button='left')

    def rightclick(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click(button='right')



if __name__ == "__main__":
    bot = MineSweeperBot()
    bot.start()