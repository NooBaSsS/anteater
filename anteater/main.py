import keyboard
import os
import random

COLS = 7
ROWS = 7
EMPTY = '.'
PLAYER = 'P'
ANTHILL = 'A'
ANT = 'a'
ANTHILLS_MIN = 1
ANTHILL_MAX = 1
PLAYER_Y = 0
PLAYER_X = 0
ANTS_MIN = 2
ANTS_MAX = 8


class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = [
            [Cell(y, x) for x in range(self.cols)] for y in range(self.rows)
        ]
        self.player = Player(Field, PLAYER_Y, PLAYER_X)
        self.anthills = []
        self.ants = []

    def draw(self) -> None:
        for row in self.cells:
            for cell in row:
                if self.player is not None and cell.y == self.player.y and cell.x == self.player.x:
                    print(PLAYER, end=' ')
                elif any(cell.y == anthill.y and cell.x == anthill.x for anthill in self.anthills):
                    print(ANTHILL, end=' ')
                elif cell.content is not None:  # Add this condition to display the content of the cell
                    print(cell.content, end=' ')
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

    def get_neighbours(self, y, x):
        neighbours_coords = []
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                if row == 0 and col == 0:
                    continue
                neighbours_coords.append(
                    (y + row, x + col)
                )
        return neighbours_coords

    def spawn_ants(self) -> None:
        for anthill in self.anthills:
            if not anthill.num_ants:
                continue
            neighbours_coords = self.get_neighbours(
                anthill.y,
                anthill.x
            )

            if not neighbours_coords:
                continue
            for y, x in neighbours_coords:
                if y < 0 or y > self.rows - 1:
                    if x < 0 or x > self.cols - 1:
                        continue
                if self.cells[y][x].content:
                    continue
                ant = Ant(y, x)
                self.cells[y][x].content = ant
                self.ants.append(ant)
                anthill.num_ants -= 1
                break

    def move_ants(self):
        for ant in self.ants:
            neighbours_coords = self.get_neighbours(ant.y, ant.x)
            if not neighbours_coords:
                continue
            for y, x in neighbours_coords:
                if y < 0 or y > self.rows - 1:
                    if x < 0 or x > self.cols - 1:
                        self.ants.remove(ant)
                        self.cells[ant.y][ant.x].content = None
                        break

                new_cell = self.cells[y][x]
                if new_cell.content:
                    continue
                self.cells[ant.y][ant.x].content = None
                new_cell.content = ant
                ant.y = y
                ant.x = x

class Ant:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.image = ANT

    def __str__(self) -> str:
        return self.image


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
        self.num_ants = random.randint(ANTS_MIN, ANTS_MAX)

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
            self.field.spawn_ants()
            self.field.move_ants()
            os.system('cls')  # Draw and clear
            self.field.draw()


field = Field()
player = Player(field, PLAYER_Y, PLAYER_X)
Game(field)
