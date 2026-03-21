# 🐟 Flappy Vis
A Dutch-language Flappy Bird-inspired game built with Pygame, set in an underwater ocean world. Guide your fish through coral reef obstacles while dodging sharks!

## Gameplay
Tap **SPACE** to make the fish swim upward. Gravity pulls it back down if you don't intervene. Navigate through gaps in the coral reefs without hitting the walls, the coral, or any sharks.

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Start game / Swim up |
| `SPACE` | Restart after game over |

## Obstacles

- **Coral Reefs** — Vertical barriers with a randomised gap to swim through
- **Regular Sharks** — Swim straight across the screen at varying speeds
- **Zigzag Sharks** — Swim in a sine-wave pattern, making them harder to dodge

## Installation

**Requirements:** Python 3 and Pygame

```bash
pip install pygame
python flappy_vis.py
```

## Project Structure

| Class | Description |
|-------|-------------|
| `Vis` | The player fish — movement, jumping, and rendering |
| `Koraalrif` | Coral reef obstacle with a randomised gap position |
| `Haai` | Base class for all sharks |
| `GewoneHaai` | Straight-swimming shark |
| `ZigzagHaai` | Wave-pattern shark |
| `Scherm` | Handles all screen rendering (start, game, game over) |

## Configuration

Key constants at the top of the file can be tuned to adjust difficulty:

| Constant | Default | Effect |
|----------|---------|--------|
| `RIF_GAT_HOOGTE` | `180` | Size of the gap in coral reefs |
| `RIF_SNELHEID` | `4` | How fast reefs scroll left |
| `RIF_INTERVAL` | `1800ms` | Time between new reefs |
| `HAAI_INTERVAL` | `3000ms` | Time between new sharks |
| `ZWAARTEKRACHT` | `0.5` | Downward pull on the fish |
| `SPRONG_KRACHT` | `-8` | Upward force on jump |

## Known Issues

- `maak_haai()` is called in `main()` but not defined in the source — add this function before running.
