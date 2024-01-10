import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.is_game = True
        self.square = Square()
        self.main_loop()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_game = False
            if event.type == pygame.K_ESCAPE:
                self.is_game = False

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def main_loop(self):
        while self.is_game:
            self.handle_events()
            self.render()


class Square(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(, (255, 0, 0), pygame.rect(0, 0, 100, 100))


if __name__ == '__main__':
    Game()
