# Escape the Dungeon of Doom

A first-person medieval action game in the style of DOOM. Escape from 5 dungeon levels with stealth and melee combat mechanics.

## 🎮 Game Overview

**Escape the Dungeon of Doom** is a first-person action game where the player must escape from 5 increasingly difficult levels:

| Level | Name | Description |
|-------|------|-------------|
| 1 | Dungeon | Underground dungeon |
| 2 | Castle | Castle ground floor |
| 3 | Camp | Camp around the castle |
| 4 | Forest | Wide forest |
| 5 | Mountain Pass | Mountain pass |

### Features

- **Movement**: WASD (4 directions) + Arrow keys (rotation)
- **Combat**: Melee attacks with different weapons
- **Stealth**: Enemies patrol and chase the player
- **Items**: Weapons and armor to equip
- **Progression**: 5 levels to complete

## 🚀 Quick Start

### Requirements

- Python 3.12+
- UV (package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd EscapeTheDungeonOfDoom
```

2. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Run the Game

```bash
# Using the launch script
./run.sh

# Or directly with UV
uv run python -m src.main
```

## ⌨️ Controls

| Key | Action |
|-----|--------|
| W/A/S/D | Move forward/left/back/right |
| ← / → | Rotate view |
| Space | Attack |
| E | Interact / Pick up item |
| I | Drop weapon |
| J | Drop armor |
| TAB | Show health |
| ESC | Pause / Menu |
| F3 | Debug overlay |

## ⚔️ Combat System

### Weapons

| Weapon | Damage | Speed |
|--------|--------|-------|
| Fists | 10% | 1.0x |
| Sword | 25% | 0.9x |
| Axe | 40% | 0.7x |
| Hammer | 70% | 0.5x |

### Armor

| Armor | Reduction | Speed |
|-------|-----------|-------|
| None | 1.0x | 1.0x |
| Light | 0.75x | 0.8x |
| Medium | 0.5x | 0.6x |
| Heavy | 0.25x | 0.3x |

### Damage Formula

```
damage = weapon_damage × armor_penetration
backstab: +25% damage when attacking from behind
```

## 👾 Enemies

Enemies have three states:

1. **Patrol**: Follow patrol routes
2. **Chase**: Chase player when detected
3. **Attack**: Attack when close enough

- Detection: Distance-based (varies by level)
- Field of view: 120°
- Attack cooldown: 1 second
- Attack damage: 10% of player health

## 🧪 Testing

```bash
# Run unit tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Lint code
uv run pylint src/
```

## 📂 Project Structure

```
EscapeTheDungeonOfDoom/
├── src/
│   ├── main.py           # Entry point
│   ├── core/             # Game loop, scenes, constants
│   ├── entities/         # Player, Enemy, Items, TileMap
│   ├── systems/          # Input, Physics, AI, Combat
│   ├── scenes/           # Menu, Game, Pause, etc.
│   └── loaders/          # Map, Enemy, Item loaders
├── data/
│   ├── maps/             # CSV level maps
│   ├── patrols/          # Enemy patrol routes
│   ├── enemies/          # Enemy definitions
│   └── items/            # Item definitions
├── tests/                # Unit tests
├── config/               # Game configuration
├── docs/                 # Technical documentation
└── run.sh                # Launch script
```

## 🔧 Development

### Running Tests

```bash
# All tests
uv run pytest -v

# Specific test file
uv run pytest tests/test_player.py -v

# With detailed output
uv run pytest -vv
```

### Code Style

The project follows these conventions:
- English naming (snake_case)
- Type hints on public functions
- Google-style docstrings (one line)
- Constants in `constants.py`

### Contributing

1. Make your changes
2. Run tests: `uv run pytest`
3. Ensure linting passes: `uv run pylint src/`
4. Commit with clear message

## 📄 License

This is a game project for educational purposes.

## 🎯 Game States

| State | Description |
|-------|-------------|
| Menu | Main menu (Start, Options, Exit) |
| Playing | Active gameplay |
| Paused | ESC pressed during game |
| Level Transition | Between levels |
| Game Over | Player died (2s → restart) |
| Victory | Completed level 5 (5s → menu) |

---

**Objective**: Escape all 5 levels. Good luck, adventurer!
