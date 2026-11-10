# Formal state representation and transition semantics

SnakeGuide · Technical note · November 2026

## Abstract

A Snake configuration is an ordered body embedded in a board, together with food, direction, and any ruleset-specific state. This note specifies legal transitions under immediate growth and solid boundaries, then distinguishes the simulator state from the information available in a rendered board. The model provides a common vocabulary for planning, collision detection, and reproducible evaluation.

## Key point

Write the transition function before choosing the planner. Body order and update order are part of the problem.

## 1. Start with a ruleset

Snake is a family of games. A proof about one member need not hold for another. Our reference model uses a finite rectangular grid, four-neighbor movement, solid boundaries, one food cell, and immediate growth by one cell when food is eaten. There is no starvation timer. Obstacles, when present, are fixed unless a rule explicitly changes them.

Let the board be V = {0,…,W−1} × {0,…,H−1}. A body B is an ordered sequence of distinct vertices, starting at the head and ending at the tail. Consecutive vertices share a grid edge. A set of occupied cells cannot substitute for this sequence: it tells you where the body is, but not which cell leaves next.

```text
s = (B, d, f, O, ξ),    B = (b₀, b₁, …, bℓ₋₁)
```

## 2. What belongs in the state

The direction d determines which reversal is prohibited. The food location f affects growth, and O stores obstacles. The symbol ξ represents the pseudorandom generator state when exact replay matters. An environment with queued growth, health, timed walls, or simultaneous opponents needs additional variables.

For a stochastic model, the transition law may sample food without exposing the generator state. For an exact implementation replay, the generator state or the full sequence of random outcomes must be retained. These are distinct modeling goals. “Markov state” means sufficient information for the transition distribution, not necessarily access to hidden random bits.

## 3. Derive a transition

An action proposes a neighboring head cell q. Reject the action if it leaves the board or enters an obstacle. Determine whether q contains food before deciding which body cells block it. On a growing move, all current body cells remain occupied; on a non-growing move, the old tail is removed.

The next body is formed by prepending q, retaining the tail only on a growing move. This convention allows entry into the old tail on a non-growing step. A game that checks all collisions before removing the tail implements a different transition function. Neither convention should be silently assumed.

```text
B′ = (q, b₀, …, bℓ₋₂)  without food;    B′ = (q, b₀, …, bℓ₋₁)  with food
```

## 4. Why the distinction matters

Two states can have the same occupied set and different body order. Their next vacant cells can differ, so an occupancy-only planner may give them the same action even when their legal continuations differ. This is a state-aliasing problem, not a weakness of a particular search algorithm.

The practical consequence is a disciplined separation: an image or feature vector is an observation, while the simulator maintains the complete state. Any claim that an observation is sufficient must be justified by the selected rules. The equations here specify SnakeGuide’s educational model; the linked Battlesnake rules document a different, concrete implementation.

## References

1. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.
2. Battlesnake. [Battlesnake Game Rules](https://docs.battlesnake.com/rules). Official rules.

Figures and interactive controls are available at https://snakeguide.org/articles/formal-state
