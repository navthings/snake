# snake-game

A clean, minimal terminal snake game, in the spirit of Emacs' `snake.el`.

## Install

```
brew install navthings/tap/snake-game
```

or from source:

```
pip install .
```

## Play

```
snake
```

## Controls

| Key            | Action        |
| -------------- | ------------- |
| Arrows / hjkl / wasd | move    |
| p              | pause / resume |
| q / Esc        | quit          |
| r              | restart (game over screen) |

High score is saved between sessions to `~/.local/share/snake-game/highscore.json`.

## Requirements

Unix-like terminal with `curses` support (Linux, macOS). No external dependencies.
