import keyboard
import os

COLS = 10
ROWS = 5
EMPTY = '.'
PLAYER = 'P'
ANTHILL = 'A'
ANT = 'a'


class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = [
            [Cell(y, x) for x in range(self.cols)] for y in range(self.rows)
        ]
        self.player = None

    def draw(self) -> None:
        for row in self.cells:
            for cell in row:
                if self.player is not None and cell.y == self.player.y and cell.x == self.player.x:
                    print(player, end=' ')  # Player(image='P') - игрок
                else:
                    print(cell, end=' ')
            print()


class Cell:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.image = EMPTY

    def draw(self):
        if self.content:
            print(self.content.image)
        else:
            print(self.image)

    def __str__(self) -> str:
        return self.image


class Player:
    def __init__(self, field, y, x) -> None:
        self.y = y
        self.x = x
        self.field = field
        self.field.player = self
        self.image = PLAYER

    def __str__(self) -> str:
        return self.image

    def move_player(self):
        pass


class Game:
    def __init__(self, field) -> None:
        self.field = field
        self.game = True
        self.run()

    def run(self):
        while self.game:
            key = keyboard.read_event()  # перемещение + проверка
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'right' and self.field.player.x < COLS - 1:
                    self.field.player.x += 1
                if key.name == 'left' and self.field.player.x:
                    self.field.player.x -= 1
                if key.name == 'up' and self.field.player.y:
                    self.field.player.y -= 1
                if key.name == 'down' and self.field.player.y < ROWS - 1:
                    self.field.player.y += 1
            print('')
            os.system('cls')  # отрисовка + очистка
            self.field.draw()


field = Field()
player = Player(field, 2, 2)
Game(field)
