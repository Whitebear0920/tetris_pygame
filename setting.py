import pygame


#繪製俄羅斯方塊遊戲尺寸
Columns = 10
Row = 20
Cell_Size = 40 #尺寸單位 pixel
Game_Width, Game_Height = Columns * Cell_Size, Row * Cell_Size


#記分板尺寸
SideBar_Width = 200 
Preview_Height_Fraction = 0.7 # 70 %的高
Score_Height_Fraction = 1 - Preview_Height_Fraction # 30% 的高

#視窗(window)
Padding = 20 #視窗邊框與遊戲畫面間的距離
Window_width = Game_Width 
