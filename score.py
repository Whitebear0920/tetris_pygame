from setting import*

class Score:
    def __init__(self) -> None:
        self.surface = pygame.Surface((SideBar_Width, Game_Height * Score_Height_Fraction - Padding))
        self.rect = self.surface.get_rect(bottomright = (Window_Width - Padding, Window_Height - Padding))
        self.display_surface = pygame.display.get_surface()
        print(self.rect)

    def run(self):
        self.display_surface.blit(self.surface, self.rect)