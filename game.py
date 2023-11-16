from setting import * 

class Game:
    def __inin__(self):

        #general setup
        self.surface = pygame.Surface((Game_Width, Game_Height)) #創建一個對象
        self.display_surface = pygame.display.get_surface() #取得當前視窗

    def run(self):
        self.display_surface.blit(self.surface, (0, 0))
