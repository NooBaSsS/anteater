import keyboard
import os
import random

COLS = 2
ROWS = 2
EMPTY = '.'
PLAYER = 'P'
ANTHILL = 'A'
ANT = 'a'
ANTHILLS_MIN = 1
ANTHILL_MAX = 4
PLAYER_Y = 0
PLAYER_X = 0


class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = [
            [Cell(y, x) for x in range(self.cols)] for y in range(self.rows)
        ]
        self.player = Player(Field, PLAYER_Y, PLAYER_X)
        self.anthills = []

    def draw(self) -> None:
        for row in self.cells:
            for cell in row:
                if self.player is not None and cell.y == self.player.y and cell.x == self.player.x:
                    print(PLAYER, end=' ')
                elif any(cell.y == anthill.y and cell.x == anthill.x for anthill in self.anthills):
                    print(ANTHILL, end=' ')
                else:
                    print(cell, end=' ')
            print()

    def get_empty_cells(self) -> list:
        empty_cells = [
            cell for row in self.cells for cell in row
            if cell.x is not self.player.x and cell.y is not self.player.y and not any(cell.y == anthill.y and cell.x == anthill.x for anthill in self.anthills)
        ]
        return empty_cells

    def spawn_anthills(self, num_anthills: int) -> None:
        for i in range(num_anthills):
            empty_cells = self.get_empty_cells()
            random.shuffle(empty_cells)
            if i < len(empty_cells):
                anthill = Anthill(empty_cells[i].y, empty_cells[i].x)
                print(anthill.x, anthill.y)
                print()
                self.anthills.append(anthill)
                empty_cells[i].content = anthill


        '''empty_cells = [
            cell for row in self.cells for cell in row
            if cell is not self.player and not any(cell.y == anthill.y and cell.x == anthill.x for anthill in self.anthills)
        ]
        random.shuffle(empty_cells)
        for i in range(num_anthills):
            if i < len(empty_cells):
                anthill = Anthill(empty_cells[i].y, empty_cells[i].x)
                self.anthills.append(anthill)
                empty_cells[i].content = anthill'''


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


class Anthill:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.image = ANTHILL

    def __str__(self):
        return self.image


class Game:
    def __init__(self, field) -> None:
        self.field = field
        self.game = True
        self.run()

    def run(self):
        self.field.spawn_anthills(random.randint(ANTHILLS_MIN, ANTHILL_MAX))
        self.field.draw()
        while self.game:
            key = keyboard.read_event()  # Move and check
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
            os.system('cls')  # Draw and clear
            self.field.draw()


field = Field()
player = Player(field, PLAYER_Y, PLAYER_X)
Game(field)
