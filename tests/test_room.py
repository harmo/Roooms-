import unittest

from app.cell import Cell
from app.room import Room


class TestRoomInit(unittest.TestCase):

    def test_it_sets_its_width(self):
        width = 0

        room = Room(width, 0, [])

        self.assertEqual(room.w, width)

    def test_it_sets_its_height(self):
        height = 0

        room = Room(0, height, [])

        self.assertEqual(room.h, height)

    def test_it_sets_its_cells(self):
        cells = []

        room = Room(0, 0, cells)

        self.assertEqual(room.cells, cells)

    def test_it_sets_min_x(self):
        cell = Cell(0, 0)

        room = Room(1, 1, [cell, Cell(1, 0)])

        self.assertEqual(room._min_x, cell.x)

    def test_it_sets_max_x(self):
        cell = Cell(1, 0)

        room = Room(1, 1, [cell, Cell(0, 0)])

        self.assertEqual(room._max_x, cell.x)

    def test_it_sets_min_y(self):
        cell = Cell(0, 0)

        room = Room(1, 1, [cell, Cell(0, 1)])

        self.assertEqual(room._min_y, cell.y)

    def test_it_sets_max_y(self):
        cell = Cell(0, 1)

        room = Room(1, 1, [cell, Cell(0, 0)])

        self.assertEqual(room._max_y, cell.y)


class TestRoomCorners(unittest.TestCase):

    def test_it_sets_expected_top_left_corner(self):
        cell = Cell(0, 0)
        cells = [cell, Cell(1, 0), Cell(0, 1), Cell(1, 1)]
        room = Room(2, 2, cells)

        self.assertEqual((room._min_x, room._min_y), (cell.x, cell.y))

    def test_it_sets_expected_bottom_left_corner(self):
        cell = Cell(0, 1)
        cells = [Cell(0, 0), Cell(1, 0), cell, Cell(1, 1)]
        room = Room(2, 2, cells)

        self.assertEqual((room._min_x, room._max_y), (cell.x, cell.y))

    def test_it_sets_expected_top_right_corner(self):
        cell = Cell(1, 0)
        cells = [Cell(0, 0), cell, Cell(0, 1), Cell(1, 1)]
        room = Room(2, 2, cells)

        self.assertEqual((room._max_x, room._min_y), (cell.x, cell.y))

    def test_it_sets_expected_bottom_right_corner(self):
        cell = Cell(1, 1)
        cells = [Cell(0, 0), Cell(1, 0), Cell(0, 1), cell]
        room = Room(2, 2, cells)

        self.assertEqual((room._max_x, room._max_y), (cell.x, cell.y))


class TestRoomGetWall(unittest.TestCase):

    def setUp(self):
        self.cell1 = Cell(0, 0)
        self.cell2 = Cell(1, 0)
        self.cell3 = Cell(0, 1)
        self.cell4 = Cell(1, 1)
        self.room = Room(2, 2, [self.cell1, self.cell2, self.cell3, self.cell4])

    def test_it_returns_expected_north_wall(self):
        north_wall = self.room.get_north_wall()

        self.assertListEqual(north_wall, [self.cell1, self.cell2])

    def test_it_returns_expected_south_wall(self):
        south_wall = self.room.get_south_wall()

        self.assertListEqual(south_wall, [self.cell3, self.cell4])

    def test_it_returns_expected_east_wall(self):
        east_wall = self.room.get_east_wall()

        self.assertListEqual(east_wall, [self.cell2, self.cell4])

    def test_it_returns_expected_west_wall(self):
        west_wall = self.room.get_west_wall()

        self.assertListEqual(west_wall, [self.cell1, self.cell3])

    def test_it_returns_expected_walls(self):
        walls = self.room.get_walls()

        self.assertListEqual(
            walls,
            self.room.get_north_wall() +
            self.room.get_south_wall() +
            self.room.get_west_wall() +
            self.room.get_east_wall()
        )


class RoomTestCase(unittest.TestCase):

    def setUp(self):
        self.cell1 = Cell(10, 10)
        self.cell2 = Cell(11, 10)
        self.cell3 = Cell(10, 11)
        self.cell4 = Cell(11, 11)
        self.room = Room(2, 2, [self.cell1, self.cell2, self.cell3, self.cell4])


class TestRoomAddCells(RoomTestCase):

    def test_top_left_corner_is_updated(self):
        cell = Cell(9, 10)
        new_cells = [cell, Cell(9, 11)]

        self.room.add_cells(new_cells)

        self.assertEqual(
            (self.room._min_x, self.room._min_y),
            (cell.x, cell.y)
        )

    def test_bottom_left_corner_is_updated(self):
        cell = Cell(10, 12)
        new_cells = [cell, Cell(11, 12)]

        self.room.add_cells(new_cells)

        self.assertEqual(
            (self.room._min_x, self.room._max_y),
            (cell.x, cell.y)
        )

    def test_top_right_corner_is_updated(self):
        cell = Cell(12, 10)
        new_cells = [cell, Cell(12, 11)]

        self.room.add_cells(new_cells)

        self.assertEqual(
            (self.room._max_x, self.room._min_y),
            (cell.x, cell.y)
        )

    def test_bottom_right_corner_is_updated(self):
        cell = Cell(12, 11)
        new_cells = [cell, Cell(12, 10)]

        self.room.add_cells(new_cells)

        self.assertEqual(
            (self.room._max_x, self.room._max_y),
            (cell.x, cell.y)
        )

    def test_room_width_is_updated(self):
        cell = Cell(9, 10)
        new_cells = [cell, Cell(9, 11)]

        self.room.add_cells(new_cells)

        self.assertEqual(self.room.w, 3)

    def test_room_height_is_updated(self):
        cell = Cell(10, 12)
        new_cells = [cell, Cell(11, 12)]

        self.room.add_cells(new_cells)

        self.assertEqual(self.room.h, 3)


class TestDecorate(RoomTestCase):

    def add_cells(self):
        self.cell5 = Cell(9, 10)
        self.cell6 = Cell(9, 11)
        self.room.add_cells([self.cell5, self.cell6])

    def test_it_decorate_wall_cell_as_expected(self):
        self.add_cells()

        self.assertIs(self.cell5.is_wall, True)

    def test_it_decorate_floor_cell_as_expected(self):
        self.room.add_cells([
            Cell(12, 10),
            Cell(12, 11),
            Cell(12, 12),
            Cell(12, 13)
        ])

        self.assertIs(self.cell4.is_floor, True)
