from setting import *
from sys import exit

# Components
from game import Game
from score import Score
from preview import Preview

from random import choice 

class Main:
    def __init__(self):
        
        #general 
        pygame.init() #初始化
        self.Dispay_Surface = pygame.display.set_mode((Window_Width, Window_Height)) #執行遊戲外框
        self.clock = pygame.time.Clock() #遊戲時刻

        pygame.display.set_caption("Tetris") #設定視窗標題名稱

        #shapes
        self.next_shapes = [choice(list(Tetorminos.keys())) for shape in range(3)]


        #components 
        self.game = Game(self.get_next_shape, self.update_score) 
        self.score  = Score()
        self.preview = Preview()


    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(Tetorminos.keys())))
        return next_shape

    def run(self):
        while(True):
            for event in pygame.event.get(): #pygame.event.get() 取得當前發生的事件

                if event.type == pygame.QUIT: #當遊戲狀態為停止時 離開遊戲
                    pygame.quit() #exit everything 
                    exit()
            #display
            self.Dispay_Surface.fill(Gray) #設定背景顏色
            self.game.run()
            self.game.draw_grid()
            self.score.run()
            self.preview.run(self.next_shapes)
            #updatating the game
            pygame.display.update()
            self.clock.tick(60) #控制遊戲幀數

if __name__ == "__main__":
    main = Main()
    main.run()