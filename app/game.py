import time
import curses

from . import FPS
from .grid import Grid


class Game:

    need_refresh = True
    _tick = 0

    def __init__(self, stdscr, difficulty='normal'):
        self._stdsrc = stdscr
        self.grid = Grid(stdscr, difficulty)

        self._running = True

    def run(self):
        while self._running:
            if self.grid.resolved:
                self.win()

            elif self.grid.game_over:
                self.fail()

            else:
                self.tick()

                self._stdsrc.addstr(1, 0, self.grid.get_output())

                self.watch_events()

                self._stdsrc.addstr(self.grid.player.inventory)

            self._stdsrc.addstr('\n\n')
            self._stdsrc.refresh()

            time.sleep(FPS)

    def tick(self):
        self._tick += 1
        tick = '⌚ {0:.1f}'.format(self._tick * FPS)
        self._stdsrc.addstr(0, 0, tick)

    def watch_events(self):
        event = self._stdsrc.getch()

        if event == curses.KEY_UP:
            self.grid.player.move_up()
        if event == curses.KEY_DOWN:
            self.grid.player.move_down()
        if event == curses.KEY_LEFT:
            self.grid.player.move_left()
        if event == curses.KEY_RIGHT:
            self.grid.player.move_right()

    def win(self):
        curses.beep()
        self._stdsrc.clear()
        self._stdsrc.addstr(
            8, 10, 'VICTORY !', curses.A_BLINK | curses.A_BOLD
        )
        self.display_stats()

        visited_rooms = len(self.grid.get_visible_rooms())
        total_rooms = len(self.grid._rooms)
        score = 100 - (100 / total_rooms * visited_rooms)
        self._stdsrc.addstr(14, 10, 'SCORE : {0:.0f}'.format(score))

    def fail(self):
        curses.beep()
        self._stdsrc.clear()
        self._stdsrc.addstr(
            8, 10, 'GAME OVER !', curses.A_BLINK | curses.A_BOLD
        )
        self.display_stats()

    def display_stats(self):
        visited_rooms = len(self.grid.get_visible_rooms())
        self._stdsrc.addstr(
            10, 10, 'ROOMS VISITED : %s' % visited_rooms
        )
