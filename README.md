# 🐍 Python Mini-Games Collection

## Overview
A collection of classic games built entirely in Python. This repository serves as a practical playground for software engineering concepts, no AI has been used, it's just hours of debugging and enjoying developing.

## Available Games

### 1. Blackjack Simulator (`/blackjack`)
A fully functional CLI Blackjack game featuring:
- Core hitting, standing, and dealer logic (dealer stands at 17).
- Dynamic betting system and state management.
- Persistent local leaderboard (File I/O).

### 2. Wordle Clone (`/wordle`)
A Python implementation of the popular word-guessing game. *(Currently procedural, scheduled for OOP refactoring).*

## Roadmap & Architecture
Currently, the games operate independently using a procedural approach. The next architectural phase involves refactoring the codebase into an Object-Oriented structure, extracting shared entities (e.g., `Card`, `Deck`, `GameEngine`) to support additional games like Texas Hold'em with high code reusability.

---
*Developed by Nicole Betto.*
