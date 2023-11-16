import pygame


#繪製俄羅斯方塊遊戲尺寸
Columns = 10
Row = 20
Cell_Size = 40 #每個格子的大小 尺寸單位 pixel
Game_Width, Game_Height = Columns * Cell_Size, Row * Cell_Size #

#記分板尺寸
SideBar_Width = 200 
Preview_Height_Fraction = 0.7 # 70 %的高
Score_Height_Fraction = 1 - Preview_Height_Fraction # 30% 的高

#視窗(window)
Padding = 20 #視窗邊框與遊戲畫面間的距離
Window_Width = Game_Width + SideBar_Width + Padding * 3
Window_Height = Game_Height + Padding * 2 

#Game Behaviour
Update_Start_Speed = 800
Move_Wait_Time = 200
Rotate_Wait_Time = 200
Block_Offset = pygame.Vector2(Columns // 2, 5)

#Colors
Yellow = "#f1e60d"
Red = "#e51b20"
Blue = "#204b9b"
Green = "#65b32e"
Purple = "#7b217f"
Cyan = "#6cc6d9"
Orange = "#f07e13"
Gray = "#262626"
Line_Color = "#ffffff"


#shapes

Tetorminos = {
    "T" : {"shape" : [(0,0), (-1,0), (1,0), (0,-1)], "color":Purple},
    "O" : {"shape" : [(0,0), (0,-1), (1,0), (1,-1)], "color":Yellow},
    "J" : {"shape" : [(0,0), (0,-1), (0,1), (-1,1)], "color":Blue},
    "L" : {"shape" : [(0,0), (0,-1), (0,1), (1,1)], "color":Orange},
    "I" : {"shape" : [(0,0), (0,-1), (0,-2), (0,1)], "color":Cyan},
    "S" : {"shape" : [(0,0), (-1,0), (0,-1), (1,-1)], "color":Green},
    "Z" : {"shape" : [(0,0), (1,0), (0,-1), (-1,-1)], "color":Red}
}