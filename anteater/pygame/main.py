import pygame
import sys
from random import randint

ROWS = 30
COLS = 30
CELL_SIZE = 10

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Pygame OOP Template")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.cells = [
                [Cell(y=row, x=col) for col in range(COLS)] for row in range(ROWS)
        ]
        self.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def update(self):
        # Логика игры
        pass

    def render(self):
        self.screen.fill((255, 255, 255))
        for row in self.cells:
            for cell in row:
                self.screen.blit(cell.image, (cell.x * CELL_SIZE, cell.y * CELL_SIZE))

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

class Cell(pygame.sprite.Sprite):
    def __init__(self, y=0, x=0):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        self.image.fill((r, g, b))



if __name__ == "__main__":
    game = Game()
