import curses
import os

from curses import wrapper

from .game import Game


stdscr = curses.initscr()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.noecho()


def main(stdscr):
    difficulty = 'normal'
    if os.environ.get('HARD', False):
        difficulty = 'hard'

    stdscr.clear()

    game = Game(stdscr, difficulty)
    game.run()

    stdscr.refresh()


try:
    wrapper(main)
except KeyboardInterrupt:
    pass
