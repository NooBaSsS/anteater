import keyboard
import os
import random

COLS = 7
ROWS = 7
EMPTY = '.'
PLAYER = 'P'
ANTHILL = 'A'
ANT = 'a'
ANTHILLS_MIN = 3
ANTHILL_MAX = 5
PLAYER_Y = 3
PLAYER_X = 3
ANTS_MIN = 4
ANTS_MAX = 8
IS_DEBUG = True


class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = [
            [Cell(y, x) for x in range(self.cols)] for y in range(self.rows)
        ]
        self.player = Player(Field, PLAYER_Y, PLAYER_X)
        self.ants_escaped = 0
        self.anthills = []
        self.ants = []

    def draw(self) -> None:
        for row in self.cells:
            for cell in row:
                if self.player is not None and cell.y == self.player.y and cell.x == self.player.x:
                    print(PLAYER, end=' ')
                elif any(cell.y == anthill.y and cell.x == anthill.x for anthill in self.anthills):
                    print(ANTHILL, end=' ')
                elif cell.content is not None:
                    print(cell.content, end=' ')
                else:
                    print(cell, end=' ')
            print()

    def move_player(self) -> None:
        pass

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

    def get_total_ants(self) -> int:
        ants_in_anthills = 0  # + [i.num_ants for i in self.anthills][0]
        for anthill in self.anthills:
            ants_in_anthills += anthill.num_ants
        total_ants = len(self.ants) + ants_in_anthills
        return total_ants

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
                    continue
                if x < 0 or x > self.cols - 1:
                    continue
                if self.cells[y][x].content:
                    continue
                ant = Ant(y, x)
                self.cells[y][x].content = ant
                self.ants.append(ant)
                anthill.num_ants -= 1
                break

    def is_on_field(self, y: int, x: int) -> bool:
        return (y > -1 and y < ROWS) and (x > -1 and x < COLS)

    def move_ants(self):
        for ant in self.ants:
            neighbours_coords = self.get_neighbours(ant.y, ant.x)
            random.shuffle(neighbours_coords)

            if IS_DEBUG:
                print(f'У муравья {ant.y} {ant.x} соседи:')
                print(*neighbours_coords)
            if not neighbours_coords:
                continue
            for y, x in neighbours_coords:
                if not self.is_on_field(y, x):
                    self.ants.remove(ant)
                    self.cells[ant.y][ant.x].content = None
                    self.ants_escaped += 1
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
        self.total_ants = self.field.get_total_ants()
        print(self.total_ants)
        self.ants_ate = 0
        self.field.draw()
        while self.game:
            self.field.get_total_ants()
            key = keyboard.read_event()  # Move and check
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'right' and self.field.player.x < COLS - 1:
                    if isinstance(self.field.cells[self.field.player.y][self.field.player.x + 1].content, Anthill):
                        continue
                    if isinstance(self.field.cells[self.field.player.y][self.field.player.x + 1].content, Ant):
                        self.field.ants.remove(self.field.cells[self.field.player.y][self.field.player.x + 1].content)
                        self.field.cells[self.field.player.y][self.field.player.x + 1].content = None
                        self.ants_ate += 1
                    self.field.player.x += 1
                if key.name == 'left' and self.field.player.x:
                    if isinstance(self.field.cells[self.field.player.y][self.field.player.x - 1].content, Anthill):
                        continue
                    if isinstance(self.field.cells[self.field.player.y][self.field.player.x - 1].content, Ant):
                        self.field.ants.remove(self.field.cells[self.field.player.y][self.field.player.x - 1].content)
                        self.field.cells[self.field.player.y][self.field.player.x - 1].content = None
                        self.ants_ate += 1
                    self.field.player.x -= 1
                if key.name == 'up' and self.field.player.y:
                    if isinstance(self.field.cells[self.field.player.y - 1][self.field.player.x].content, Ant):
                        self.field.ants.remove(self.field.cells[self.field.player.y - 1][self.field.player.x].content)
                        self.field.cells[self.field.player.y - 1][self.field.player.x].content = None
                        self.ants_ate += 1
                    if isinstance(self.field.cells[self.field.player.y - 1][self.field.player.x].content, Anthill):
                        continue
                    self.field.player.y -= 1
                if key.name == 'down' and self.field.player.y < ROWS - 1:
                    if isinstance(self.field.cells[self.field.player.y + 1][self.field.player.x].content, Ant):
                        self.field.ants.remove(self.field.cells[self.field.player.y + 1][self.field.player.x].content)
                        self.field.cells[self.field.player.y + 1][self.field.player.x].content = None
                        self.ants_ate += 1
                    if isinstance(self.field.cells[self.field.player.y + 1][self.field.player.x].content, Anthill):
                        continue
                    self.field.player.y += 1
                if key.name == 'esc':
                    input('_enter_')
                    break
            print('')
            self.field.move_ants()
            self.field.spawn_ants()
            os.system('cls')  # Draw and clear
            self.field.draw()

            if not self.field.get_total_ants():
                print('игра окончена!')
                print(f'муравьев всего: {self.total_ants}')
                print(f'муравьев съедено: {self.ants_ate}')
                print(f'муравьев сбежало: {self.total_ants - self.ants_ate}')
                input('_enter_')
                break

            if IS_DEBUG:
                print(f'муравьев всего: {self.total_ants}')
                print(f'муравьев съедено: {self.ants_ate}')
                print(f'муравьев сбежало: {self.field.ants_escaped}')


field = Field()
player = Player(field, PLAYER_Y, PLAYER_X)
Game(field)
