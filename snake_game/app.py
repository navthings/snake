from __future__ import annotations

import curses
import sys
import time

from . import __version__
from .game import Direction, GameState
from .render import Renderer
from .store import load_high_score, save_high_score

KEY_DIRECTIONS = {
    curses.KEY_UP: Direction.UP,
    curses.KEY_DOWN: Direction.DOWN,
    curses.KEY_LEFT: Direction.LEFT,
    curses.KEY_RIGHT: Direction.RIGHT,
    ord("k"): Direction.UP,
    ord("j"): Direction.DOWN,
    ord("h"): Direction.LEFT,
    ord("l"): Direction.RIGHT,
    ord("w"): Direction.UP,
    ord("s"): Direction.DOWN,
    ord("a"): Direction.LEFT,
    ord("d"): Direction.RIGHT,
}


def main(stdscr: "curses._CursesWindow") -> None:
    renderer = Renderer(stdscr)
    high_score = load_high_score()

    while True:
        term_h, term_w = stdscr.getmaxyx()
        board_h, board_w, oy, ox = renderer.board_geometry(term_h, term_w)
        renderer.origin_y, renderer.origin_x = oy, ox

        state = GameState(width=board_w, height=board_h, high_score=high_score)
        state.reset()

        last_tick = time.monotonic()
        restart_requested = False

        # Play
        while state.alive:
            try:
                key = stdscr.getch()
            except curses.error:
                key = -1

            turned = False
            while key != -1:
                if key in (ord("q"), 27):
                    save_high_score(high_score)
                    return
                elif key == ord("p"):
                    state.paused = not state.paused
                elif key in KEY_DIRECTIONS and not state.paused and not turned:
                    state.turn(KEY_DIRECTIONS[key])
                    turned = True
                key = stdscr.getch()

            now = time.monotonic()
            if not state.paused and (now - last_tick) >= state.speed:
                state.step()
                last_tick = now

            if state.score > high_score:
                high_score = state.score
                state.high_score = high_score
                save_high_score(high_score)

            renderer.draw_frame(state, *stdscr.getmaxyx())
            time.sleep(0.01)

        # Over
        renderer.draw_frame(state, *stdscr.getmaxyx())
        while not restart_requested:
            try:
                key = stdscr.getch()
            except curses.error:
                key = -1
            if key in (ord("q"), 27):
                save_high_score(high_score)
                return
            elif key == ord("r"):
                restart_requested = True
            time.sleep(0.02)


USAGE = """usage: snake [-h] [--version]

Controls:
  arrows / hjkl / wasd   move
  p                      pause / resume
  q / Esc                quit
  r                      restart (game over screen)
"""


def run() -> None:
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE)
        return
    if "--version" in args:
        print(__version__)
        return
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
