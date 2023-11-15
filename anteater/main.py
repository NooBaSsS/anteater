COLS = 5
ROWS = 5


class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = [[Cell(y, x) for x in range(self.cols)] for y in range(self.rows)]
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
        self.image = '.'

    def __str__(self) -> str:
        return self.image


class Player:
    def __init__(self, field, y, x) -> None:
        self.y = y
        self.x = x
        self.field = field
        self.field.player = self
        self.image = 'P'

    def __str__(self) -> str:
        return self.image


field = Field()
player = Player(field, 0, 0) # y и x игрока
field.draw()
