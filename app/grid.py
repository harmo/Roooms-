import random

from . import (
    GRID_WIDTH,
    GRID_HEIGHT,
    ROOM_CREATION_MAX_ATTEMPTS,
    ROOM_OPTIMIZATION_MAX_ATTEMPTS,
    NORTH_RATIO,
    SOUTH_RATIO,
    EAST_RATIO,
    WEST_RATIO,
    MIN_ROOM_WIDTH,
    MAX_ROOM_WIDTH,
    MIN_ROOM_HEIGHT,
    MAX_ROOM_HEIGHT,
)

from .cell import Cell
from .room import Room
from .player import Player


class Grid:

    matrix = {}
    _grid = []
    _rooms = []
    _attempts = 0
    resolved = False
    game_over = False

    def __init__(self, stdscr, difficulty):
        self._stdscr = stdscr
        self._difficulty = difficulty
        self.debug('     Difficulty      ' + self._difficulty)

        self.init_matrix()

        self.init_rooms()
        self.expand_rooms()

        self.set_indestructible_cells()

        self.distribute_ink()

        self.player = self.make_player()

        self.put_hammer()

        self.hide_rooms()

    def debug(self, what):
        self._stdscr.addstr(str(what))

    def init_matrix(self):
        for y in range(GRID_HEIGHT + 1):
            for x in range(GRID_WIDTH + 1):
                cell = Cell(x, y)
                if self._is_border(x, y):
                    cell.set_as_border()

                self.matrix.setdefault(y, {})[x] = cell

                self._grid.append(cell)

    def init_rooms(self):
        while self._attempts < ROOM_CREATION_MAX_ATTEMPTS:
            try:
                self.generate_rooms()
            except CellError:
                self._attempts += 1
                self.init_rooms()

    def _is_border(self, x, y):
        return x in [0, GRID_WIDTH] or y in [0, GRID_HEIGHT]

    def get_random_free_cell(self):
        cell = random.choice(self._grid)
        if not cell.is_floor:
            return cell

        return self.get_random_free_cell()

    def get_random_floor_cell(self):
        cell = random.choice(self._grid)
        if cell.is_floor:
            return cell

        return self.get_random_floor_cell()

    def get_room_from_cell(self, cell):
        for room in self._rooms:
            if cell in room.cells:
                return room

    def get_output(self):
        output = ''

        for y, columns in self.matrix.items():
            output += '\n'

            for x, cell in columns.items():
                output += cell.icon

        output += '\n  '

        return output

    def get_cell_from_pos(self, x, y):
        try:
            return self.matrix[y][x]
        except KeyError:
            pass

    def get_random_room_size(self):
        max_width = MAX_ROOM_WIDTH
        if self._difficulty == 'hard':
            max_width /= 2

        max_height = MAX_ROOM_HEIGHT
        if self._difficulty == 'hard':
            max_height /= 2

        return (
            random.randrange(MIN_ROOM_WIDTH, max_width),
            random.randrange(MIN_ROOM_HEIGHT, max_height)
        )

    def generate_rooms(self):
        width, height = self.get_random_room_size()
        free_cell = self.get_random_free_cell()
        elligible_cells = []

        for y in range(free_cell.y, free_cell.y + height):
            for x in range(free_cell.x, free_cell.x + width):
                new_cell = self.get_cell_from_pos(x, y)
                if new_cell is None or new_cell.is_floor:
                    raise CellError()

                elligible_cells.append(new_cell)

        new_room = Room(width, height, elligible_cells, self.get_cell_from_pos)
        self._rooms.append(new_room)

        self.init_rooms()

    def expand_rooms(self):
        optimization_attempts = 0
        while optimization_attempts < ROOM_OPTIMIZATION_MAX_ATTEMPTS:

            for i, room in enumerate(self._rooms):
                room.expand()
                self._rooms[i] = room

            optimization_attempts += 1

    def distribute_ink(self):
        for room in self._rooms:
            room.put_ink()

    def set_indestructible_cells(self):
        for cell in self._grid:
            floor_neighboors = []

            for ratio in [NORTH_RATIO, SOUTH_RATIO, EAST_RATIO, WEST_RATIO]:
                next_cell = self.get_cell_from_pos(
                    cell.x + ratio[0],
                    cell.y + ratio[1]
                )
                if next_cell and next_cell.is_floor:
                    floor_neighboors.append(next_cell)

            if len(floor_neighboors) < 2:
                cell.set_as_border()

    def make_player(self):
        cell = self.get_random_floor_cell()

        return Player(
            grid=self,
            room=self.get_room_from_cell(cell),
            cell=cell
        )

    def hide_rooms(self):
        for cell in self._grid:
            if cell not in self.player.room.cells:
                cell.hide()

    def put_hammer(self):
        cell = self.get_random_floor_cell()
        room = self.get_room_from_cell(cell)
        if self.player.room == room:
            return self.put_hammer()

        cell.set_as_hammer()
        room.hammer = cell
        room.remove_ink()

    def get_visible_rooms(self):
        return [
            room for room in self._rooms
            if room.is_visible
        ]

    def ink_available(self):
        for room in self.get_visible_rooms():
            if room.has_ink:
                return True
        return False


class CellError(Exception):
    pass
