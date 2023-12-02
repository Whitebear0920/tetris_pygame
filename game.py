#遊戲畫面
from random import choice
from pygame.sprite import Group
from timer import Timer
from setting import * 
from sys import exit
import json
import socket
from random import randint
from time import sleep

class Game:
    def __init__(self, get_next_shape, update_score):

        #connection
        self.Max_Bytes = 65565
        self.is_entered = False
        #server
        self.Server_IP="127.0.0.1"
        self.Server_port = 57414
        self.Server_addr = ((self.Server_IP,self.Server_port))
        #socket 初始化
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #general setup
        self.surface = pygame.Surface((Game_Width, Game_Height)) #創建一個對象
        self.display_surface = pygame.display.get_surface() #取得當前視窗
        self.rect = self.surface.get_rect(topleft = (Padding, Padding))
        self.sprites = pygame.sprite.Group()
        #game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        self.attack_rows = 0
        #lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))#將顏色轉為透明
        self.line_surface.set_alpha(120)
        
        #attack
        self.attack_bimu = 0
        #tetromino
        self.field_data = [[0 for x in range(Columns)] for y in range(Row)]
        self.tetromino = Tetromino(
            choice(list(Tetorminos.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

        #timer
        self.down_speed = Update_Start_Speed
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            "rotate" : Timer(Rotate_Wait_Time),
            "horizontal move" : Timer(Move_Wait_Time),
            "vertical move" : Timer(Update_Start_Speed, True, self.move_down), 
        }
        self.timers["vertical move"].activate()
        self.start_time = Timer(0)
        self.start_time.activate()

        #score
        self.current_level = 0
        self.current_score = 0
        self.current_lines = 0

        #pause
        self.Start = False
        self.gameover = False

        #GameStart
        self.GameStartMsg = "waitting for connect"

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += Score_Data[num_lines] * self.current_level

        #every 10 lines += level by 1
        # if self.current_lines / 10 > self.current_level:
        #     self.current_level += 1
        #     self.down_speed * 0.75
        #     self.down_speed_faster = self.down_speed * 0.3
        #     self.timers["vertical move"].duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)
        
    
    def level_up(self):
        # print((self.start_time.timecheak() - self.start_time.first_start_time ) // 1000 % 60, "S")
        if ((self.start_time.timecheak() - self.start_time.first_start_time ) // 1000)  % 60 == 0 and self.start_time.active:
            self.current_level += 1
            self.down_speed * 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers["vertical move"].duration = self.down_speed
            self.update_score(self.current_lines, self.current_score, self.current_level)
            self.start_time.active = False
        elif((self.start_time.timecheak() - self.start_time.first_start_time ) // 1000 % 60 == 1):
            self.start_time.active = True
            


    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                self.gameover = True
                self.send_message("GameOver",True)
                self.GameStartMsg = "You Lose \nPress 'Q' to exit the game"
                print("Lose")

    def create_new_tetromino(self):
        
        self.check_game_over()
        self.check_finished_rows()
        self.check_attack_row(self.attack_rows)
        self.tetromino = Tetromino(
            self.get_next_shape(), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)
        
    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()


    def draw_grid(self): #畫格子
        for col in range(1,Columns):
            x = col * Cell_Size
            pygame.draw.line(self.surface, Line_Color, (x ,0), (x, self.surface.get_height()), 1) #(在哪裡, 顏色, 開始位置, 結束位置, 線條粗細)
        for ro in range(1,Row):
            y = ro * Cell_Size
            pygame.draw.line(self.surface, Line_Color, (0, y), (self.surface.get_width(), y), 1)
    
    def check_finished_rows(self):

        # get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)
                self.attack_bimu += 1
        self.send_message("Attack",self.attack_bimu)
        self.attack_bimu = 0
        if delete_rows:
            for delete_row in delete_rows: #要刪除的行

                #deletee full rows
                for block in self.field_data[delete_row]: #迭代每個精靈並刪除該精靈
                    block.kill()
                #move down blocks
                for row in self.field_data: #這邊有點不懂
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
                    
            #rebuild the field data
            self.field_data = [[0 for x in range(Columns)] for y in range(Row)]
            for block in self.sprites: #更新field_data
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            #update score
            self.calculate_score(len(delete_rows))

    def check_attack_row(self, nums):
        dig_block = randint(0,9)
        now_row = Row - 1
        while nums:
            
            
            self.field_data = [[0 for x in range(Columns)] for y in range(Row)]
            for i in self.sprites:
                i.pos.y -= 1
                # if i.pos.y - nums < 0 :
                #     self.gameover = True
                # else:
            # if not self.gameover:
            
            for i in range(Columns):
                if i != dig_block:
                    Block_two(self.sprites, (i , now_row), stack_block)
                
            # for i in self.sprites:
            #     print(i.pos.x, i.pos.y)
            for block in self.sprites: #更新field_data
                # if  0 <= block.pos.y < Row and 0 <= block.pos.x < Columns:s
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            nums -= 1
            print(self.field_data)
        self.attack_rows = 0
          
    def connect(self):
        self.msgdict = {
            "type": "connecting"
        }
        self.data = json.dumps(self.msgdict).encode('utf-8')
        # 將Enter Request送到Server
        self.sock.sendto(self.data, self.Server_addr)

        # 等待並接收Server傳回來的訊息，若為Enter Response則繼續下一步，否則繼續等待
        while not self.is_entered:
            try:
                self.data, self.address = self.sock.recvfrom(self.Max_Bytes)
                self.msgdict = json.loads(self.data.decode('utf-8'))
                if self.msgdict['type'] == "connected":
                    self.is_entered = True
                    print('connect successfully!!!')
                    self.GameStartMsg = 'connect successfully!!! \n\n waitting for other player!'
            except:
                print("Server connection failed, try again in 5 seconds")
                for i in range(5):
                    sleep(1)
                    self.GameStartMsg += "."
                    print(".", end="",flush = True)
                print()
                self.GameStartMsg = self.GameStartMsg.replace(".","",5)
                data = json.dumps(self.msgdict).encode("utf-8")
                self.sock.sendto(data, self.Server_addr)
    
    def send_message(self,type,value):
        self.Senddata ={
            "type" : type,
            "value" : value
        }
        self.Senddata = json.dumps(self.Senddata).encode()
        self.sock.sendto(self.Senddata,self.Server_addr)
    
    def input(self):
        key = pygame.key.get_pressed()


        #checking horizontal movement
        if not self.timers["horizontal move"].active:
            if(key[pygame.K_LEFT]):
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if(key[pygame.K_RIGHT]):
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()

        #check for rotation
        if not self.timers["rotate"].active:
            if key[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers["rotate"].activate()
                
        


        #down speed update
        if not self.down_pressed and key[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers["vertical move"].duration = self.down_speed_faster
            
        if self.down_pressed and not key[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers["vertical move"].duration = self.down_speed

    def GameStart(self): #遊戲開始跟結束時的文字顯示
        self.GameStart_font = pygame.font.Font(None, 36)

        # 分解文字為多行
        self.GameStart_lines = self.GameStartMsg.split('\n')

        # 計算總高度
        self.GameStart_total_height = sum([self.GameStart_font.render(GameStart_line, True, Red).get_height() for GameStart_line in self.GameStart_lines])

        # 設定總高度和行數的偏移量
        self.GameStart_offset_y = (Window_Height - self.GameStart_total_height) // 2
        self.GameStart_line_spacing = 5  # 設定行間距

        # 逐行繪製文字
        for self.GameStart_line in self.GameStart_lines:
            self.GameStart_text_surface = self.GameStart_font.render(self.GameStart_line, True, Red)
            self.GameStart_text_rect = self.GameStart_text_surface.get_rect()
            self.GameStart_text_rect.center = (Window_Width // 2, self.GameStart_offset_y + self.GameStart_text_rect.height // 2)
            self.display_surface.blit(self.GameStart_text_surface, self.GameStart_text_rect)
            self.GameStart_offset_y += self.GameStart_text_rect.height + self.GameStart_line_spacing
        
    def run(self):
        #update
        self.input()
        self.timer_update()
        self.sprites.update()

        # #drawing
        self.surface.fill(Gray)
        self.sprites.draw(self.surface)#畫磚塊精靈

        self.draw_grid()
        self.display_surface.blit(self.surface, (Padding, Padding))
        
        #畫外框
        pygame.draw.rect(self.display_surface, Line_Color, self.rect, 2, 2)

class Tetromino: #一個形狀
    def __init__(self, shape, group, create_new_tetromino, field_data):
        #setup
        self.shape = shape
        self.block_positions = Tetorminos[shape]["shape"]
        self.color = Tetorminos[shape]["color"]
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        #create blocks
        self.blocks =[Block(group, pos, self.color) for pos in self.block_positions]

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_down(self.blocks):
            for block in self.blocks:
                block.pos.y += 1
        else:

            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block # 使用int()的原因是因為Vector2預設的資料型態是float
            self.create_new_tetromino()

    #collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    #movement
    def next_move_down(self, blocks):
        collision_list = [block.down_collide(int(block.pos.y + 1), self.field_data) for block in blocks] 
        return True if any(collision_list) else False
    
    #rotate
    def rotate(self):
        if self.shape != "O":
            #1. pivot point
            pivot_pos = self.blocks[0].pos

            #2.new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            #3. collision check
            for pos in new_block_positions:
                #horizontal 
                if pos.x < 0 or pos.x >= Columns:
                    return 

                #field check -> collisiton with other pieces
                if (self.field_data[int(pos.y)][int(pos.x)]):
                    return 
                #vertival / floor check
                if  pos.y >=  Row:
                    return
            #4. implement new positions

            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

class Block(pygame.sprite.Sprite):#單一個磚塊
    def __init__(self, group, pos, color):
        #general
        super().__init__(group)
        self.image = pygame.Surface((Cell_Size, Cell_Size))
        self.image.fill(color)

        #position
        self.pos = pygame.Vector2(pos) + Block_Offset
        # x = self.pos.x * Cell_Size
        # y = self.pos.y * Cell_Size
        self.rect = self.image.get_rect(topleft = self.pos * Cell_Size)
   
    def rotate(self, pivot_pos):
        # distance = self.pos - pivot_pos
        # rotated = distance.rotate(90)
        # new_pos = pivot_pos + rotated
        # return new_pos
        return pivot_pos + (self.pos - pivot_pos).rotate(90) # .rotate(90) 是Vector2的函數

    def horizontal_collide(self, x, field_data): #邊界判斷
        if not 0 <= x < Columns:
            return True
        if x >= 0 and field_data[int(self.pos.y)][x]:
            return True


    def down_collide(self, y, field_data):
        if  y >=  Row:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        # self.rect = self.image.get_rect(topleft = self.pos * Cell_Size)
        self.rect.topleft = self.pos * Cell_Size # 兩句話是一樣的意思

class Block_two(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        #general
        super().__init__(group)
        self.image = pygame.Surface((Cell_Size, Cell_Size))
        self.image.fill(color)

        #position
        self.pos = pygame.Vector2(pos)
        # x = self.pos.x * Cell_Size
        # y = self.pos.y * Cell_Size
        self.rect = self.image.get_rect(topleft = self.pos * Cell_Size)
    
    def update(self):
        # self.rect = self.image.get_rect(topleft = self.pos * Cell_Size)
        self.rect.topleft = self.pos * Cell_Size # 兩句話是一樣的意思


