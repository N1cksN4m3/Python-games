# 🐍 Python Mini-Games Collection

## Overview
A collection of classic games built entirely in Python. This repository serves as a practical playground for software engineering concepts, no AI has been used, it's just hours of debugging and enjoying developing.

## Available Games

## 1. Blackjack Simulator (`/blackjack`)

## Python Blackjack: From Procedural (v1) to OOP (v2)

![Tests](https://github.com/N1cksN4m3/Python-games/actions/workflows/tests.yml/badge.svg)

A command-line Blackjack game written in Python. Here a showcase of the refactoring of a procedural script (`blackjack_v1.py`) into a clean Object-Oriented architecture (`blackjack_v2_0.py`), complete with an automated unit test suite (`black_jack_unit_test.py`).

---

### Evolution: v1.0 vs v2.0

| Feature | Version 1.0 (`blackjack_v1.py`) | Version 2.0 (`blackjack_v2_0.py`) |
| :--- | :--- | :--- |
| **Architecture** | Procedural functions passing multiple tuples | Object-Oriented (`Deck`, `Hand`, `Wallet`, `User`) |
| **Game Rules** | Hit, Stand, Double Down | Added **Recursive Split**, **Fold**, and **All-In** |
| **Ace Logic** | Recomputed manually inside functions | Encapsulated dynamically in `Hand.create_handvalue()` |
| **Save System** | Simple file append (`mode="a"`, creates duplicates) | Dictionary-based **Upsert** (updates existing players cleanly) |
| **Testing** | Manual gameplay only | 14 automated unit tests with `unittest` and `tempfile` |

---

### Core Classes (`blackjack_v2_0.py`)

* **`Deck`**: Manages a 52-card deck with automatic reset and reshuffling when cards run out.
* **`Hand`**: Handles card drawing, split initialization (`starting_cards`), and dynamic Ace valuation (`11` or `1`).
* **`Wallet`**: Manages player balance, bets, payouts (3:2 for Natural Blackjack, 1:1 standard, 2:1 on Double), and prevents negative balances.
* **`User`**: Handles saving and loading player profiles and leaderboards (`leaderboard_bj.txt`) without duplicating records.

---

### Unit Testing (`black_jack_unit_test.py`)

The project includes **14 unit tests** built with Python's standard `unittest` library:

* **`DeckTest`**: Verifies the 52-card distribution (16 tens, 4 Aces) and auto-reset on the 53rd draw.
* **`HandTest`**: Tests soft-to-hard hand transitions, multiple Aces (`[11, 11, 11, 11] -> 14`), and distinguishes 2-card Natural Blackjacks from 3-card 21s.
* **`WalletTest`**: Tests standard payouts, Blackjack payouts, draws, splits, and All-In edge cases.
* **`UserTest`**: Uses `tempfile.TemporaryDirectory` to test file creation, duplicate-free updates, and 0-byte file resilience in an isolated sandbox.

---

### How to Run

**1. Play the Game (v2.0 OOP):**

    python3 blackjack_v2_0.py

**2. Run the Automated Unit Tests:**

    python3 -m unittest -v black_jack_unit_test.py

## 2. Wordle Clone (`/wordle`)
A Python implementation of the popular word-guessing game. *(Currently procedural, scheduled for OOP refactoring).*

## Roadmap & Architecture
Currently, the games operate independently using a procedural approach. The next architectural phase involves refactoring the codebase into an Object-Oriented structure, extracting shared entities (e.g., `Card`, `Deck`, `GameEngine`) to support additional games like Texas Hold'em with high code reusability.

---
*Developed by Nicole Betto.*
