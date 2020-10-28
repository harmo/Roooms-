class Pen:

    _ink = 0

    def __init__(self, cell):
        cell.set_as_pen()
        self.cell = cell
        self.x = cell.x
        self.y = cell.y
        self.refill()

    @property
    def ink(self):
        return '*' * self._ink

    @property
    def is_empty(self):
        return self._ink == 0

    def draw(self):
        self._ink -= 1

    def refill(self, ink=1):
        self._ink += ink
