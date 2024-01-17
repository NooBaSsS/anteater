import pygame
import sys
from random import randint

ROWS = 30
COLS = 25
CELL_SIZE = 20
PLAYER_X = 20
PLAYER_Y = 20


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
        self.player = Player(x=PLAYER_X, y=PLAYER_Y)
        self.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                else:
                    self.update(key=event.key)

    def update(self, key=None):
        # Логика игры
        if key == pygame.K_RIGHT:
            if self.player.x + 1 < COLS:
                self.player.x += 1
        elif key == pygame.K_LEFT:
            if self.player.x - 1 >= 0:
                self.player.x -= 1
        elif key == pygame.K_UP:
            if self.player.y - 1 >= 0:
                self.player.y -= 1
        elif key == pygame.K_DOWN:
            if self.player.y + 1 < ROWS:
                self.player.y += 1

    def render(self):
        self.screen.fill((255, 255, 255))
        for row in self.cells:
            for cell in row:
                if cell.x == self.player.x and cell.y == self.player.y:
                    cell.image.fill((110, 110, 110))
                    self.screen.blit(cell.image, (cell.x * CELL_SIZE + 10, cell.y * CELL_SIZE + 10))
                elif cell.x == self.ants.ant.x and cell.y == self.ants.ant.y:
                    cell.image.fill((255, 0, 0))
                    self.screen.blit(cell.image, (cell.x * CELL_SIZE + 10, cell.y * CELL_SIZE + 10))
                else:
                    cell.image.fill((10, 10, 10))
                    self.screen.blit(cell.image, (cell.x * CELL_SIZE + 10, cell.y * CELL_SIZE + 10))

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


class Player():
    def __init__(self, y=0, x=0):
        self.x = x
        self.y = y


class Ant():
    def __init__(self, y=0, x=0):
        self.x = x
        self.y = y


class Anthill():
    def __init__(self, y=0, x=0):
        self.x = x
        self.y = y


if __name__ == "__main__":
    game = Game()
