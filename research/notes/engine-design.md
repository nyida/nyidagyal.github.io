# Deterministic simulation and reproducible transitions

SnakeGuide · Technical note · November 2026

## Abstract

Reproducibility begins with an explicit transition function. We separate simulation ticks from rendering, describe seeded food placement and its limitations, and enumerate invariants for collision, growth, and full-board completion. The reference implementation makes each rule inspectable; replayability additionally requires actions, rules, generator details, and event order.

## Key point

A reproducible engine is a specification you can execute. Rendering should not decide the rules.

## 1. Make the transition function the center

A reliable engine accepts a state and an action and returns the next state. Rendering, keyboard handling, and animation should sit outside this function. This separation allows the same rules to support interactive play, search, replay, and evaluation.

SnakeGuide’s lab uses integer coordinates, an ordered body array, a direction vector, one food cell, and explicit generator state. A collision ends the episode. Filling the last available cell produces a win, avoiding an infinite retry loop when spawning food.

## 2. Use one logical clock

The game advances by discrete ticks. Input is queued between ticks, and only one requested direction change is consumed per tick. Otherwise, two rapid turns can bypass a reversal check that was written for a single update.

Animation may interpolate between cells, but collision logic should remain tied to discrete states. A frame-rate-dependent engine can change behavior when a browser tab slows down. The visual frame clock and the rules clock are different concerns.

## 3. Make food sampling explicit

The lab enumerates free cells in row-major order and selects an index using a 32-bit linear congruential generator. The generator is deterministic and suitable for an educational replay; it is not a cryptographic generator. The modulo selection has slight distribution bias, so this demo should not be presented as a statistically exact uniform sampler.

Identical seed, action sequence, and engine version reproduce a run. The seed alone does not: different actions change when food is consumed and which cells are available. The exported JSON contains a state snapshot, rather than a complete action replay.

```text
ξ′ = (1664525·ξ + 1013904223) mod 2³²
```

## 4. Test properties that define the game

After each valid transition, all body cells must be inside the board, consecutive segments must be adjacent, and distinct segments must occupy distinct cells. Length increases by one exactly when food is eaten. Newly placed food must not overlap the body.

Boundary tests should include tail entry, reversal requests, immediate growth, full-board completion, and collision. If exposing a learning API, distinguish task termination from an artificial time-limit truncation. That distinction affects learning targets and evaluation reports, as the Gymnasium API makes explicit.

## References

1. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.
2. NumPy developers. [Random-number compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html). Official documentation.
3. Battlesnake. [Battlesnake Game Rules](https://docs.battlesnake.com/rules). Official rules.

Figures and interactive controls are available at https://snakeguide.org/articles/engine-design
