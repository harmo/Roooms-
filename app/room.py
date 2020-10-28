import random

from . import (
    EAST_RATIO,
    NORTH_RATIO,
    SOUTH_RATIO,
    WEST_RATIO,
)
from .ink import Ink, NoInk
from .pen import Pen


class Room:

    cells = []
    _min_x = None
    _max_x = 0
    _min_y = None
    _max_y = 0
    pen = None
    has_exit = False
    is_visible = False
    is_open = False

    def __init__(self, width, height, cells, get_cell_from_pos):
        self.w = width
        self.h = height
        self.cells = cells

        self._get_cell_from_pos = get_cell_from_pos

        self.set_corners()
        self.decorate()

    def __repr__(self):
        return 'Room: %s, %s [%s] (min %s) (max %s)' % (
            self.w, self.h, self.size,
            (self._min_x, self._min_y),
            (self._max_x, self._max_y),
        )

    @property
    def size(self):
        return self.w * self.h

    def set_corners(self):
        for cell in self.cells:
            if cell.x > self._max_x:
                self._max_x = cell.x
            if self._min_x is None or cell.x < self._min_x:
                self._min_x = cell.x
            if cell.y > self._max_y:
                self._max_y = cell.y
            if self._min_y is None or cell.y < self._min_y:
                self._min_y = cell.y

    def decorate(self):
        for cell in self.cells:
            if cell.x == self._min_x or cell.y == self._min_y:
                cell.set_as_wall()
            elif cell.x == self._max_x or cell.y == self._max_y:
                cell.set_as_wall()
            else:
                cell.set_as_floor()

    def add_cells(self, cells):
        self.cells += cells
        self.cells.sort()
        self.set_corners()
        self.w = self._max_x - self._min_x + 1
        self.h = self._max_y - self._min_y + 1
        self.decorate()

    def get_north_wall(self):
        return [
            cell for cell in self.cells
            if cell.y == self._min_y
        ]

    def get_south_wall(self):
        return [
            cell for cell in self.cells
            if cell.y == self._max_y
        ]

    def get_west_wall(self):
        return [
            cell for cell in self.cells
            if cell.x == self._min_x
        ]

    def get_east_wall(self):
        return [
            cell for cell in self.cells
            if cell.x == self._max_x
        ]

    def get_walls(self):
        return self.get_north_wall() \
            + self.get_south_wall() \
            + self.get_west_wall() \
            + self.get_east_wall()

    @property
    def is_opened(self):
        for cell in self.get_walls():
            if cell.is_floor:
                return True
        return False

    def expand(self):
        directions = {
            'north': NORTH_RATIO,
            'south': SOUTH_RATIO,
            'east': EAST_RATIO,
            'west': WEST_RATIO
        }
        for direction, ratio in directions.items():
            neighboors = []
            wall = getattr(self, 'get_%s_wall' % direction)()

            for cell in wall:
                next_cell = self._get_cell_from_pos(
                    cell.x + ratio[0],
                    cell.y + ratio[1]
                )

                if next_cell and next_cell.is_expandable:
                    neighboors.append(next_cell)

            if len(neighboors) == len(wall):
                self.add_cells(neighboors)

    def get_random_cell(self):
        cell = random.choice(self.cells)
        if cell.is_floor:
            return cell

        return self.get_random_cell()

    def open(self, cell):
        cell.set_as_floor()
        self.is_open = True

    def hide(self):
        for cell in self.cells:
            cell.hide()
        self.is_visible = False

    def show(self):
        for cell in self.cells:
            cell.show()
        self.is_visible = True

    def visit(self):
        for cell in self.cells:
            cell.set_as_visited()

    def unvisit(self):
        for cell in self.cells:
            cell.set_as_unvisited()

    def put_pen(self):
        cell = self.get_random_cell()

        self.pen = Pen(cell)

    def put_ink(self):
        if self.is_open:
            return

        cell = self.get_random_cell()

        try:
            Ink(cell)
        except NoInk:
            pass

    def remove_ink(self):
        for cell in self.cells:
            if cell.is_ink:
                cell.set_as_floor()

    @property
    def has_ink(self):
        for cell in self.cells:
            if cell.is_ink:
                return True
        return False
