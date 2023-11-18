#遊戲畫面
from random import choice
from setting import * 
from timer import Timer
class Game:
    def __init__(self):

        #general setup
        self.surface = pygame.Surface((Game_Width, Game_Height)) #創建一個對象
        self.display_surface = pygame.display.get_surface() #取得當前視窗
        self.rect = self.surface.get_rect(topleft = (Padding, Padding))
        self.sprites = pygame.sprite.Group()
        
        #lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))#將顏色轉為透明
        self.line_surface.set_alpha(120)
        
        #tetromino
        self.tetromino = Tetromino(choice(list(Tetorminos.keys())), self.sprites)

        #timer
        self.timers = {
            "vertical move" : Timer(Update_Start_Speed, True, self.move_down),
            "horizontal move" : Timer(Move_Wait_Time)
        }
        self.timers["vertical move"].activate()

    def tmier_update(self):
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
        

    def input(self):
        key = pygame.key.get_pressed()

        if not self.timers["horizontal move"].active:
            if(key[pygame.K_LEFT]):
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if(key[pygame.K_RIGHT]):
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()

    
    def run(self):
        #update
        self.input()
        self.tmier_update()
        self.sprites.update()

        # #drawing
        self.surface.fill(Gray)
        self.sprites.draw(self.surface)#畫磚塊精靈

        self.draw_grid()
        self.display_surface.blit(self.surface, (Padding, Padding))
        
        #畫外框
        pygame.draw.rect(self.display_surface, Line_Color, self.rect, 2, 2)

class Tetromino: #磚塊
    def __init__(self, shape, group):
        #setup
        self.block_positions = Tetorminos[shape]["shape"]
        self.color = Tetorminos[shape]["color"]

        #create blocks
        self.blocks =[Block(group, pos, self.color) for pos in self.block_positions]

    def move_horizontal(self, amount):
         for block in self.blocks:
             block.pos.x += amount

    def move_down(self):
        for block in self.blocks:
            block.pos.y += 1

    #collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horinotal for block in self.blocks]
    #movement

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

    def update(self):
        # self.rect = self.image.get_rect(topleft = self.pos * Cell_Size)
        self.rect.topleft = self.pos * Cell_Size # 兩句話是一樣的意思


