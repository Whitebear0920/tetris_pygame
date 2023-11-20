#遊戲畫面
from random import choice
from timer import Timer
from setting import * 
from sys import exit

class Game:
    def __init__(self, get_next_shape, update_score):

        #general setup
        self.surface = pygame.Surface((Game_Width, Game_Height)) #創建一個對象
        self.display_surface = pygame.display.get_surface() #取得當前視窗
        self.rect = self.surface.get_rect(topleft = (Padding, Padding))
        self.sprites = pygame.sprite.Group()
        
        #game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score


        #lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))#將顏色轉為透明
        self.line_surface.set_alpha(120)
        
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
            "vertical move" : Timer(Update_Start_Speed, True, self.move_down),
            "horizontal move" : Timer(Move_Wait_Time),
            "rotate" : Timer(Rotate_Wait_Time)
        }
        self.timers["vertical move"].activate()

        #score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += Score_Data[num_lines] * self.current_level

        #every 10 lines += level by 1
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed * 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers["vertical move"].duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)
                

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                print("Game Over")
                exit()

    def create_new_tetromino(self):
        self.check_game_over()
        self.check_finished_rows()
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

class Tetromino: #單一個磚塊
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

class Block(pygame.sprite.Sprite):
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


