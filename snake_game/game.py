from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @property
    def opposite(self) -> "Direction":
        return _OPPOSITES[self]


_OPPOSITES = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

STARTING_LENGTH = 4
STARTING_SPEED = 0.11
MIN_SPEED = 0.045
SPEED_STEP = 0.003


@dataclass
class GameState:
    width: int
    height: int
    snake: deque = field(default_factory=deque)
    direction: Direction = Direction.RIGHT
    pending_direction: Direction = Direction.RIGHT
    food: tuple[int, int] = (0, 0)
    score: int = 0
    high_score: int = 0
    speed: float = STARTING_SPEED
    alive: bool = True
    paused: bool = False

    # Setup
    def reset(self) -> None:
        cy, cx = self.height // 2, self.width // 2
        self.snake = deque([(cy, cx - i) for i in range(STARTING_LENGTH)])
        self.direction = Direction.RIGHT
        self.pending_direction = Direction.RIGHT
        self.score = 0
        self.speed = STARTING_SPEED
        self.alive = True
        self.paused = False
        self.food = self._spawn_food()

    def _spawn_food(self) -> tuple[int, int]:
        occupied = set(self.snake)
        free = [
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            if (y, x) not in occupied
        ]
        return random.choice(free) if free else (0, 0)

    # Input
    def turn(self, new_dir: Direction) -> None:
        if new_dir.opposite != self.direction:
            self.pending_direction = new_dir

    # Tick
    def step(self) -> str | None:
        if not self.alive or self.paused:
            return None

        self.direction = self.pending_direction
        head_y, head_x = self.snake[0]
        dy, dx = self.direction.value
        new_head = (head_y + dy, head_x + dx)
        ny, nx = new_head

        if not (0 <= ny < self.height and 0 <= nx < self.width):
            self.alive = False
            return "game_over"

        will_grow = new_head == self.food
        body_check = self.snake if will_grow else deque(list(self.snake)[:-1])
        if new_head in body_check:
            self.alive = False
            return "game_over"

        self.snake.appendleft(new_head)

        if will_grow:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.speed = max(MIN_SPEED, self.speed - SPEED_STEP)
            self.food = self._spawn_food()
            return "ate"

        self.snake.pop()
        return None
