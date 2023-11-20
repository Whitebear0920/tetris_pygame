# 創建右下角的分數框
from setting import*
from os.path import join
class Score:
    def __init__(self) -> None:
        self.surface = pygame.Surface((SideBar_Width, Game_Height * Score_Height_Fraction - Padding))
        self.rect = self.surface.get_rect(bottomright = (Window_Width - Padding, Window_Height - Padding))
        self.display_surface = pygame.display.get_surface()

        #font 
        self.font = pygame.font.Font(join(".", "graphic", "Russo_One.ttf"), 30)#(font, size)

        #increment
        self.increment_height = self.surface.get_height() / 3 

        #data
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f"{text[0]}: {text[1]}", True, "white")
        text_rext = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rext)

    def run(self):

        self.surface.fill(Gray)
        for i, text in enumerate([("Score", self.score), ("level", self.level), ("lines", self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x ,y), text)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, Line_Color, self.rect, 2, 2)