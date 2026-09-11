# snake

A clean, minimal terminal snake game, in the spirit of Emacs' `snake.el`.



https://github.com/user-attachments/assets/0bfa431b-80a9-4c77-8281-89b4267a04e4


the official snake game used in dusky https://github.com/dusklinux/dusky

## Install

```
brew trust navthings/tap && brew install navthings/tap/snake
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

| Key                  | Action                     |
| --------------------- | -------------------------- |
| Arrows / hjkl / wasd  | move                       |
| p                     | pause / resume             |
| q / Esc               | quit                       |
| r                     | restart (game over screen) |

High score is saved between sessions to `~/.local/share/snake-game/highscore.json`.

## Requirements

Unix-like terminal with `curses` support (Linux, macOS). No external dependencies.
