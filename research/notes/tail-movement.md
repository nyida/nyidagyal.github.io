# Tail release, growth, and collision constraints

SnakeGuide · Technical note · November 2026

## Abstract

Collision legality depends on the order of movement and growth. We analyze entry into a vacating tail cell, derive conditional release times for body segments, and identify cases in which a static occupancy test rejects a legal move. The accompanying transition figure computes both a non-growing tail entry and a growing move from the same ordered body.

## Key point

A cell is not simply occupied or empty: its availability depends on transition timing and growth.

## 1. A collision check is a timing decision

Consider the four-cell body [(3,3),(2,3),(2,2),(3,2)], listed head first. Moving upward proposes (3,2), the current tail. In our immediate-growth model, this is legal if that cell is not food: the tail vacates during the same transition. Checking membership in the whole old body would reject a legal move.

The opposite error is to delete the tail unconditionally before evaluating growth. If a game permits food or a growth event at the destination, the tail may need to remain. Collision and growth logic must agree on the body that persists into the next state.

## 2. Release times are conditional

Suppose the current length is ℓ and growth never occurs. The segment initially at index i, counting the head as zero, leaves the body after ℓ−i moves. The initial tail leaves after one move. A release-time map can therefore show when initially occupied cells might become available.

This map is conditional on the future. Eating delays releases. Newly visited head cells become occupied even though they were empty in the initial map. A planner that records only initial release times may accept a route that crosses its own newly created body.

```text
release(bᵢ) = ℓ − i    under no growth and continued legal movement
```

## 3. A moving target is not a safety proof

Searching for a route to the current tail is a useful heuristic because the tail often opens space. But a static path to that cell is not necessarily a route to the tail’s future position. Every intermediate move changes the geometry and may change which escape routes remain available.

A stronger check simulates a proposed route using the real transition function, then evaluates the resulting body. Even this proves only what was checked: successful execution of a finite prefix does not imply indefinite survival, and a static continuation check does not prove a dynamic continuation.

## 4. Implement the boundary cases

Test entering the vacating tail, entering a non-tail segment, eating at the boundary, filling the final free cell, and requesting an immediate reversal. These cases reveal semantic disagreements that a high average score can conceal.

The diagram toggles an exact non-growing transition in the four-cell example. The playable lab uses this same convention. Battlesnake’s documented growth uses tail duplication, so do not import its timing assumptions into this engine without translating the rules.

## References

1. Battlesnake. [Battlesnake Game Rules](https://docs.battlesnake.com/rules). Official rules.
2. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/tail-movement
