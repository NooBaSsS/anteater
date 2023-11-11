COLS = 5
ROWS = 10


class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = []

    def draw() -> None:
        print()


class Cell:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.image = '.'

    def __str__(self) -> str:
        return self.image

field = Field()
