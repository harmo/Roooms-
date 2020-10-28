from random import choice

from . import INK_PROBALITIES


class Ink:

    def __init__(self, cell):
        quantity = choice(INK_PROBALITIES)
        if quantity == 0:
            raise NoInk()

        cell.set_as_ink()
        cell.ink_quantity = quantity

        self.cell = cell
        self.y = cell.y
        self.x = cell.x


class NoInk(Exception):
    pass
