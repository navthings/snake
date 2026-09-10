from __future__ import annotations

import curses

from .game import GameState

BORDER = {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"}
HEAD_CHAR = "@"
BODY_CHAR = "o"
FOOD_CHAR = "*"

COLOR_SNAKE_HEAD = 2
COLOR_SNAKE_BODY = 3
COLOR_FOOD = 4
COLOR_BORDER = 5
COLOR_TEXT = 6
COLOR_TEXT_DIM = 7
COLOR_ACCENT = 8


class Renderer:
    # Setup
    def __init__(self, stdscr: "curses._CursesWindow") -> None:
        self.stdscr = stdscr
        self._init_colors()
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        self.origin_y = 0
        self.origin_x = 0

    def _init_colors(self) -> None:
        curses.start_color()
        try:
            curses.use_default_colors()
            bg = -1
        except curses.error:
            bg = curses.COLOR_BLACK

        curses.init_pair(COLOR_SNAKE_HEAD, curses.COLOR_GREEN, bg)
        curses.init_pair(COLOR_SNAKE_BODY, curses.COLOR_CYAN, bg)
        curses.init_pair(COLOR_FOOD, curses.COLOR_YELLOW, bg)
        curses.init_pair(COLOR_BORDER, curses.COLOR_WHITE, bg)
        curses.init_pair(COLOR_TEXT, curses.COLOR_WHITE, bg)
        curses.init_pair(COLOR_TEXT_DIM, curses.COLOR_BLUE, bg)
        curses.init_pair(COLOR_ACCENT, curses.COLOR_MAGENTA, bg)

    # Layout
    def board_geometry(self, term_h: int, term_w: int) -> tuple[int, int, int, int]:
        margin_top = 3
        margin_bottom = 2
        margin_side = 4

        board_h = max(10, term_h - margin_top - margin_bottom - 2)
        board_w = max(20, term_w - margin_side * 2 - 2)
        board_h = min(board_h, 28)
        board_w = min(board_w, 70)

        total_h = board_h + 2 + margin_top + margin_bottom
        total_w = board_w + 2 + margin_side * 2
        origin_y = max(0, (term_h - total_h) // 2) + margin_top
        origin_x = max(0, (term_w - total_w) // 2) + margin_side

        return board_h, board_w, origin_y, origin_x

    # Draw
    def draw_frame(self, state: GameState, term_h: int, term_w: int) -> None:
        stdscr = self.stdscr
        stdscr.erase()

        board_h, board_w = state.height, state.width
        oy, ox = self.origin_y, self.origin_x

        self._draw_title(state, oy, ox, board_w)
        self._draw_border(oy, ox, board_h, board_w)
        self._draw_food(state, oy, ox)
        self._draw_snake(state, oy, ox)
        self._draw_footer(oy, ox, board_h, board_w)

        if not state.alive:
            self._draw_game_over(state, oy, ox, board_h, board_w)
        elif state.paused:
            self._draw_paused(oy, ox, board_h, board_w)

        stdscr.noutrefresh()
        curses.doupdate()

    def _safe_addstr(self, y: int, x: int, text: str, attr=0) -> None:
        term_h, term_w = self.stdscr.getmaxyx()
        if 0 <= y < term_h and 0 <= x < term_w:
            max_len = term_w - x
            if max_len <= 0:
                return
            try:
                self.stdscr.addstr(y, x, text[:max_len], attr)
            except curses.error:
                pass

    def _draw_title(self, state: GameState, oy: int, ox: int, board_w: int) -> None:
        title = "SNAKE"
        self._safe_addstr(
            oy - 3, ox + (board_w - len(title)) // 2 + 1, title,
            curses.color_pair(COLOR_ACCENT) | curses.A_BOLD,
        )

        score_txt = f"score {state.score:>3}"
        best_txt = f"best {state.high_score:>3}"
        line = f"{score_txt}    {best_txt}"
        base_x = ox + (board_w - len(line)) // 2 + 1
        self._safe_addstr(oy - 2, base_x, score_txt, curses.color_pair(COLOR_TEXT) | curses.A_BOLD)
        self._safe_addstr(oy - 2, base_x + len(score_txt) + 4, best_txt, curses.color_pair(COLOR_TEXT_DIM))

    def _draw_border(self, oy: int, ox: int, h: int, w: int) -> None:
        attr = curses.color_pair(COLOR_BORDER)
        top = BORDER["tl"] + BORDER["h"] * w + BORDER["tr"]
        bot = BORDER["bl"] + BORDER["h"] * w + BORDER["br"]
        self._safe_addstr(oy - 1, ox - 1, top, attr)
        self._safe_addstr(oy + h, ox - 1, bot, attr)
        for row in range(h):
            self._safe_addstr(oy + row, ox - 1, BORDER["v"], attr)
            self._safe_addstr(oy + row, ox + w, BORDER["v"], attr)

    def _draw_snake(self, state: GameState, oy: int, ox: int) -> None:
        body_attr = curses.color_pair(COLOR_SNAKE_BODY)
        head_attr = curses.color_pair(COLOR_SNAKE_HEAD) | curses.A_BOLD
        for i, (y, x) in enumerate(state.snake):
            ch = HEAD_CHAR if i == 0 else BODY_CHAR
            attr = head_attr if i == 0 else body_attr
            self._safe_addstr(oy + y, ox + x, ch, attr)

    def _draw_food(self, state: GameState, oy: int, ox: int) -> None:
        y, x = state.food
        self._safe_addstr(oy + y, ox + x, FOOD_CHAR, curses.color_pair(COLOR_FOOD) | curses.A_BOLD)

    def _draw_footer(self, oy: int, ox: int, h: int, w: int) -> None:
        hint = "hjkl/arrows move   p pause   q quit"
        self._safe_addstr(
            oy + h + 1, ox + max(0, (w - len(hint)) // 2) + 1,
            hint, curses.color_pair(COLOR_TEXT_DIM),
        )

    def _draw_box(self, oy: int, ox: int, h: int, w: int, lines: list[tuple[str, int]]) -> None:
        box_w = max(len(t) for t, _ in lines) + 4
        box_h = len(lines) + 2
        start_y = oy + (h - box_h) // 2
        start_x = ox + (w - box_w) // 2

        attr = curses.color_pair(COLOR_BORDER)
        self._safe_addstr(start_y, start_x, BORDER["tl"] + BORDER["h"] * (box_w - 2) + BORDER["tr"], attr)
        for i in range(box_h - 2):
            self._safe_addstr(start_y + 1 + i, start_x, BORDER["v"], attr)
            self._safe_addstr(start_y + 1 + i, start_x + box_w - 1, BORDER["v"], attr)
        self._safe_addstr(start_y + box_h - 1, start_x, BORDER["bl"] + BORDER["h"] * (box_w - 2) + BORDER["br"], attr)

        for i, (text, color) in enumerate(lines):
            tx = start_x + (box_w - len(text)) // 2
            self._safe_addstr(start_y + 1 + i, tx, text, curses.color_pair(color) | curses.A_BOLD)

    def _draw_game_over(self, state: GameState, oy: int, ox: int, h: int, w: int) -> None:
        lines = [
            ("GAME OVER", COLOR_FOOD),
            (f"score: {state.score}", COLOR_TEXT),
            ("r restart   q quit", COLOR_TEXT_DIM),
        ]
        self._draw_box(oy, ox, h, w, lines)

    def _draw_paused(self, oy: int, ox: int, h: int, w: int) -> None:
        lines = [("PAUSED", COLOR_ACCENT), ("p to resume", COLOR_TEXT_DIM)]
        self._draw_box(oy, ox, h, w, lines)
