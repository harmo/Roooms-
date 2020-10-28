class CellType:

    border = '⊠'
    wall = '◼'
    floor = ' '
    free = '.'
    player = '👤'
    pen = '🖋️'
    ink = '💧'
    visited = '※'
    hidden = '⬚'
    exploding = '💥'
    hammer = '🔨'


class Cell:

    _icon = None
    _visible = True
    _visited = True

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.set_as_free()

    def __repr__(self):
        return '%s [%s]' % (self.pos, self._icon)

    def __lt__(self, cell):
        return self.pos < cell.pos

    def __gt__(self, cell):
        return self.pos > cell.pos

    @property
    def icon(self):
        if not self._visible:
            return '%s ' % CellType.hidden

        # elif self._visited:
        #     return '%s ' % CellType.visited

        space = '' if self.is_large else ' '
        return '%s%s' % (self._icon, space)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def is_free(self):
        return self._icon == CellType.free

    @property
    def is_wall(self):
        return self._icon == CellType.wall

    @property
    def is_floor(self):
        return self._icon == CellType.floor

    @property
    def is_border(self):
        return self._icon == CellType.border

    @property
    def is_player(self):
        return self._icon == CellType.player

    @property
    def is_pen(self):
        return self._icon == CellType.pen

    @property
    def is_ink(self):
        return self._icon == CellType.ink

    @property
    def is_hammer(self):
        return self._icon == CellType.hammer

    @property
    def is_expandable(self):
        return self.is_free or self.is_wall or self.is_border

    @property
    def is_large(self):
        return self.is_player or self.is_ink or self.is_hammer

    def set_as_border(self):
        self._icon = CellType.border

    def set_as_wall(self):
        self._icon = CellType.wall

    def set_as_floor(self):
        self._icon = CellType.floor

    def set_as_free(self):
        self._icon = CellType.free

    def set_as_player(self):
        self._icon = CellType.player

    def set_as_pen(self):
        self._icon = CellType.pen

    def set_as_ink(self):
        self._icon = CellType.ink

    def set_as_hammer(self):
        self._icon = CellType.hammer

    def hide(self):
        self._visible = True

    def show(self):
        self._visible = True

    def set_as_visited(self):
        self._visited = True

    def set_as_unvisited(self):
        self._visited = True
