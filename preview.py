#創建左上角的框

from setting import*
from pygame.image import load
from os import path 

class Preview:
    def __init__(self):
        #general
        self.surface = pygame.Surface((SideBar_Width, Game_Height * Preview_Height_Fraction ))
        self.rect = self.surface.get_rect(topright = (Window_Width - Padding, Padding))
        self.display_surface = pygame.display.get_surface()

        # self.shape_surfaces = {shape: load(".."#上一層級一層,"file name","T.png") for shape in Tetorminos.keys()}
        self.shape_surfaces = {shape: load(path.join(".", "graphic", f"{shape}.png")).convert_alpha() for shape in Tetorminos.keys()}
        
        #image position data
        self.increment_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape] 
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            rect = shape_surface.get_rect(center = (x, y))#定會shape中心點
            self.surface.blit(shape_surface, rect)

    def run(self, next_shapes):
        self.surface.fill(Gray)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, Line_Color, self.rect, 2, 30)