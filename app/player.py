from . import NORTH_RATIO, SOUTH_RATIO, WEST_RATIO, EAST_RATIO
from .cell import CellType


class Player:

    pen_found = False
    moving_at = None
    pen = None
    hammer = None

    def __init__(self, grid, room, cell):
        self.grid = grid
        self.room = room
        self.cell = cell
        cell.set_as_player()
        self.is_moving = False

        self.room.put_pen()
        self.room.remove_ink()
        self.room.visit()

    @property
    def x(self):
        return self.cell.x

    @property
    def y(self):
        return self.cell.y

    @property
    def inventory(self):
        inventory = '~~ '

        if self.has_pen:
            inventory += '[ %s  %s ]' % (CellType.pen, self.pen.ink)

        if self.has_hammer:
            inventory += '[ %s  ]' % CellType.hammer

        inventory += ' ~~'

        return inventory

    @property
    def has_pen(self):
        return self.pen is not None

    @property
    def can_draw(self):
        return self.has_pen and not self.pen.is_empty

    def take_pen(self, pen):
        self.pen = pen
        self.pen_found = True

    @property
    def has_hammer(self):
        return self.hammer is not None

    def take_hammer(self, hammer):
        self.hammer = hammer

    def move_up(self):
        self.moving_at = NORTH_RATIO
        next_cell = self.grid.get_cell_from_pos(self.x, self.y - 1)
        self.move(next_cell)

    def move_down(self):
        self.moving_at = SOUTH_RATIO
        next_cell = self.grid.get_cell_from_pos(self.x, self.y + 1)
        self.move(next_cell)

    def move_left(self):
        self.moving_at = WEST_RATIO
        next_cell = self.grid.get_cell_from_pos(self.x - 1, self.y)
        self.move(next_cell)

    def move_right(self):
        self.moving_at = EAST_RATIO
        next_cell = self.grid.get_cell_from_pos(self.x + 1, self.y)
        self.move(next_cell)

    def move(self, next_cell):
        if next_cell.is_floor:
            self.is_moving = True

        elif next_cell.is_pen:
            self.take_pen(self.room.pen)
            self.is_moving = True

        elif next_cell.is_ink:
            self.pen.refill(next_cell.ink_quantity)
            self.is_moving = True

        elif next_cell.is_wall:
            if self.can_draw:
                self.room.open(next_cell)
                hidden_cell = self.grid.get_cell_from_pos(
                    next_cell.x + self.moving_at[0],
                    next_cell.y + self.moving_at[1]
                )
                next_room = self.grid.get_room_from_cell(hidden_cell)
                next_room.show()

                self.pen.draw()

            elif self.pen_found:
                self.grid.game_over = not self.grid.ink_available()

        elif next_cell.is_hammer:
            self.take_hammer(self.room.hammer)
            self.is_moving = True

        elif (
            self.grid._is_border(next_cell.x, next_cell.y) and
            self.has_hammer
        ):
            self.grid.resolved = True

        self.move_to(next_cell, self.grid.get_room_from_cell(next_cell))

    def move_to(self, cell, room):
        if not self.is_moving:
            return

        self.room.unvisit()
        room.visit()

        self.cell.set_as_floor()

        self.cell = cell
        self.room = room
        self.room.show()
        cell.set_as_player()
        self.is_moving = False
