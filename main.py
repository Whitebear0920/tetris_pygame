from setting import *
from sys import exit
import threading
import json

# Components
from game import Game
from score import Score
from preview import Preview
from time import sleep
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

    def recv_message(self):
        print("start")
        self.game.connect()
        print("recv_message Start")
        while(True):
            # 接收來自Server傳來的訊息
            self.Recdata, self.address = self.game.sock.recvfrom(self.game.Max_Bytes)
            self.Recdata = json.loads(self.Recdata.decode('utf-8'))
            if self.Recdata["type"] == "GameOver": #GameOver
                if self.Recdata["value"] == True:
                    self.game.gameover = True
                    print("win")
            elif self.Recdata["type"] == "Attack": #Attack Line
                print("got attack! {}".format(self.Recdata["value"]))
                self.game.attack_rows += self.Recdata["value"]

    def main_run(self):
        Pause = False
        self.Dispay_Surface.fill(Gray)
        while True:
            while not Pause:
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
                self.game.level_up()
                #updatating the game
                pygame.display.update()
                self.clock.tick(60) #控制遊戲幀數

                #gameover
                if self.game.gameover:
                    Pause = True
                    print("press 'Q' to exit the game")
                
                #pause
                
                opkey = pygame.key.get_pressed()
                if (opkey[pygame.K_p]):
                    Pause = True
                    print(Pause)
                
                #attack test
                #if(opkey[pygame.K_a]):
                #    x = choice([1,2,3,4])
                #    print(x)
                #    sleep(1)
                #    self.game.check_attack_row(x)
                #    print("i got attack!!")


            while ((Pause)and (not self.game.gameover)):
                for event in pygame.event.get(): #pygame.event.get() 取得當前發生的事件

                    if event.type == pygame.QUIT: #當遊戲狀態為停止時 離開遊戲
                        pygame.quit() #exit everything 
                        exit()
                opkey = pygame.key.get_pressed()
                if (opkey[pygame.K_o]):
                    Pause = False
                    print(Pause)
            while self.game.gameover:
                for event in pygame.event.get(): #pygame.event.get() 取得當前發生的事件

                    if event.type == pygame.QUIT: #當遊戲狀態為停止時 離開遊戲
                        pygame.quit() #exit everything 
                        exit()
                opkey = pygame.key.get_pressed()
                if (opkey[pygame.K_q]):
                    print("END!")
                    pygame.quit()
                    exit()

    def start(self):
        self.threadRec = threading.Thread(target = self.recv_message)
        self.threadRec.start()
        self.thredMain = threading.Thread(target = self.main_run())
        self.thredMain.start()
        self.threadRec.join()
        self.thredMain.join()
if __name__ == "__main__":
    main = Main()
    main.start()
    