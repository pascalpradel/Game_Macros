import time
import pyautogui
import keyboard

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
        self.color_flag = [230,210,65]
        self.color_flag_2 = [230,160,50]
        self.color_one = [25,289,224]
        self.color_one_2 = [50,190,218]
        self.color_two = [134,165,60]
        self.color_three = [216,26,101]

        self.start_point = [580,136]

        self.box_size = [113,110]
        self.abstand_x = 6.5
        self.abstand_y = 9

        self.abweichung = [25,25,25] #in Pixeln

        self.rounds_since_last_klick = 0

        print("Init ready..")
        

    def start(self):
        time.sleep(2)
        print("Started..")

        self.leftclick(int(self.start_point[0]+self.box_size[0]/2),int(self.start_point[1]+self.box_size[1]/2))

        while True:
            if keyboard.is_pressed('esc') == True:
                    print("Bye..")
                    exit()

            self.fill()
            self.screen_read()
            self.fill_probability()

            #print(self.board)
            #print(self.prob_board)

            self.execute_order()

            time.sleep(0.25)


    def fill_probability(self):
        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                self.prob_board[j][i] = [0,0]
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
                    if item_id == 3:
                        percentage = 100
                    elif item_id == 4:
                        percentage = 200
                    elif item_id == 5:
                        percentage = 300
                    ##USW

                    box_field = [[0 for x in range(3)] for y in range(3)]
                    
                    counter_x = -1
                    counter_y = -1

                    blue_counter = 0
                    flag_counter = 0

                    while counter_x < 2:
                        while counter_y < 2:
                            if x+counter_x >= 0 and y+counter_y >= 0 and x+counter_x < self.count_rows and y+counter_y < self.count_lines:
                                box_data = self.board[x+counter_x][y+counter_y]
                                field_input = [x+counter_x, y+counter_y, box_data[2]]
                                box_field[counter_x+1][counter_y+1] = field_input
                                if box_data[2] == 0:
                                    blue_counter += 1
                                elif box_data[2] == 2:
                                    flag_counter += 1
                            else:
                                box_field[counter_x+1][counter_y+1] = [404,404,404]

                            counter_y += 1
                        counter_y = -1
                        counter_x += 1

                    if blue_counter > 0:
                        a_iterator = 0
                        b_iteraror = 0

                        temp_percentage = percentage - (flag_counter * 100)

                        
                        while a_iterator < 3:
                            while b_iteraror < 3:
                                box_field_data = box_field[a_iterator][b_iteraror]
                                if box_field_data[2] == 0:
                                    prob_board_data = self.prob_board[box_field_data[0]][box_field_data[1]]
                                    if percentage != 0:
                                        prob_board_data[0] = prob_board_data[0]+int(temp_percentage/blue_counter)
                                    prob_board_data[1] += 1
                                    self.prob_board[box_field_data[0]][box_field_data[1]] = prob_board_data
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
                elif self.check_pixel(pixel, self.color_flag, [30,30,200]):
                    box_id = 2 #"FLAG"
                elif self.check_pixel(pixel, self.color_flag_2, self.abweichung):
                    box_id = 2 #"FLAG"
                elif self.check_pixel(pixel, self.color_one, [25,120,25]):
                    box_id = 3 #"EINS"
                elif self.check_pixel(pixel, self.color_one_2, self.abweichung):
                    box_id = 3 #"EINS"
                elif self.check_pixel(pixel, self.color_two, [80,70,130]):
                    box_id = 4 #"ZWEI"
                elif self.check_pixel(pixel, self.color_three, [80,70,130]):
                    box_id = 5 #"DREI"
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


    def execute_order(self):
        highest_number = [0,0,0,0] #x,y,perc,menge an bestätigungen
        lowest_number = [0,0,1000,0]

        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                prob_board_data = self.prob_board[j][i]
                
                if prob_board_data[1] != 0:
                    if highest_number[2] <= prob_board_data[0]:
                        if highest_number[3] <= prob_board_data[1]:
                            highest_number = [j,i,prob_board_data[0],prob_board_data[1]]
                    if lowest_number[2] >= prob_board_data[0]:
                        if lowest_number[3] <= prob_board_data[1]:
                            lowest_number = [j,i,prob_board_data[0],prob_board_data[1]]
                j += 1
            i += 1
            j = 0

        if lowest_number[3] == 0 and lowest_number[2] > 2:
            data = self.board[lowest_number[0]][lowest_number[1]]
            print("Left-Klick: " + str(lowest_number[0]) + " /" +  str(lowest_number[1]))
            self.leftclick(data[0],data[1])
        else:
            if highest_number[3] > lowest_number[3]:
                data = self.board[highest_number[0]][highest_number[1]]
                print("Right-Klick: " + str(highest_number[0]) + " /" +  str(highest_number[1]))
                self.rightclick(data[0],data[1])
            elif highest_number[3] < lowest_number[3]:
                data = self.board[lowest_number[0]][lowest_number[1]]
                print("Left-Klick: " + str(lowest_number[0]) + " /" +  str(lowest_number[1]))
                self.leftclick(data[0],data[1])
            else:
                data = self.board[highest_number[0]][highest_number[1]]
                print("Right-Klick: " + str(highest_number[0]) + " /" +  str(highest_number[1]))
                self.rightclick(data[0],data[1])


        #print(lowest_number)
        #print(highest_number)
        #exit()
        


    def leftclick(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click(button='left')

    def rightclick(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click(button='right')



if __name__ == "__main__":
    bot = MineSweeperBot()
    bot.start()