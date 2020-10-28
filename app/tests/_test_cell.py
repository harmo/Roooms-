from unittest.mock import sentinel

from .utils import PatchedTestCase
from app.app import (
    __name__ as module_name,
    Cell, CellType
)


class CellTest(PatchedTestCase(module_name)):

    def test_when_instanciated_it_loads_given_x(self):
        cell = Cell(x=sentinel.x)

        self.assertEqual(cell.x, sentinel.x)

    def test_when_instanciated_it_loads_given_y(self):
        cell = Cell(y=sentinel.y)

        self.assertEqual(cell.y, sentinel.y)

    def test_when_instanciated_it_loads_given_icon(self):
        cell = Cell(icon=sentinel.icon)

        self.assertEqual(cell.icon, sentinel.icon)


class CellPosTest(PatchedTestCase(module_name)):

    def test_it_returns_tuple_of_given_positions(self):
        cell = Cell(sentinel.x, sentinel.y)

        self.assertTupleEqual(cell.pos, (sentinel.x, sentinel.y))


class CellIsFreeTest(PatchedTestCase(module_name)):

    def test_when_cell_isnt_free_it_returns_false(self):
        cell = Cell(icon=CellType.wall)

        self.assertFalse(cell.is_free)

    def test_when_cell_is_free_it_returns_true(self):
        cell = Cell(icon=CellType.free)

        self.assertTrue(cell.is_free)
