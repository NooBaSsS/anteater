COLS = 5
ROWS = 5

class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = [[Cell(y, x) for x in range(self.cols)] for y in range(self.rows)]

    def draw(self) -> None:
        for row in self.cells:
            for cell in row:
                print(cell, end=' ')
            print()


class Cell:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.image = '.'

    def __str__(self) -> str:
        return self.image


field = Field()
field.draw()
