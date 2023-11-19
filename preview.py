#創建左上角的框

from setting import*

class Preview:
    def __init__(self, next_shape):
        #general
        self.surface = pygame.Surface((SideBar_Width, Game_Height * Preview_Height_Fraction ))
        self.rect = self.surface.get_rect(topright = (Window_Width - Padding, Padding))
        self.display_surface = pygame.display.get_surface()

        # shapes
        self.next_shapes= next_shape
        self.shape_surfaces = {"L": }

    def run(self):
        self.display_surface.blit(self.surface, self.rect)