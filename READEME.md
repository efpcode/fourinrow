# Four-in-a-Row (Python)

A modular, terminal-based implementation of the classic Four-in-a-Row game, built with Python. This project features flexible game modes (Freeform wihout Gravity vs. Classical Gravity), configurable win conditions, and support for CPU players.

## Features

- **Customizable Rules:** Set your own board size, number of rounds, and tokens required to win.
- **Game Modes:**
  - **Classical:** Gravity-based play where tokens fall to the lowest available slot.
  - **Freeform:** Place tokens in any empty coordinate on the board.
- **Modular Architecture:** Clean separation of concerns between board state, game rules, and user/CPU interaction.
- **Smart Validation:** Robust error handling for invalid moves, occupied slots, and out-of-bounds attempts.

## Getting Started

### Prerequisites

- Python 3.x

### Running the Game

1. Clone the repository to your machine:
   ```bash
   git clone git@github.com:efpcode/fourinrow.git
   cd fourinrow
   ```
