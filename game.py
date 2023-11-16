from setting import * 

class Game:
    def __init__(self):

        #general setup
        self.surface = pygame.Surface((Game_Width, Game_Height)) #創建一個對象
        print(self.surface)
        self.display_surface = pygame.display.get_surface() #取得當前視窗
        print(self.display_surface)
        self.rect = self.surface.get_rect(topleft = (Padding, Padding))
        #lines
        self.line_surface = self.surface.copy()


    def draw_grid(self): #畫格子
        for col in range(1,Columns):
            x = col * Cell_Size
            pygame.draw.line(self.surface, Line_Color, (x ,0), (x, self.surface.get_height()), 1) #(在哪裡, 顏色, 開始位置, 結束位置, 線條粗細)
        for ro in range(1,Row):
            y = ro * Cell_Size
            pygame.draw.line(self.surface, Line_Color, (0, y), (self.surface.get_width(), y), 1)

    def run(self):
        self.display_surface.blit(self.surface, (Padding, Padding))
        pygame.draw.rect(self.display_surface, Line_Color, self.rect, 2, 2)