# Hamiltonian cycle invariants for collision avoidance

SnakeGuide · Technical note · November 2026

## Abstract

A board-spanning cycle replaces repeated route selection with a fixed cyclic order. We state the rectangular parity condition and the body-order assumptions behind collision avoidance, then examine why shortcuts need additional checks. The interactive figure changes body length and head position while preserving the cyclic order; it is a geometric illustration rather than a food-completion experiment.

## Key point

A Hamiltonian policy is powerful because its safety follows from an invariant. Its assumptions belong beside the result.

## 1. Replace repeated planning with a fixed order

A Hamiltonian cycle visits every vertex exactly once before returning to its start. On a board of N traversable cells, label this cycle 0 through N − 1. Following it means repeatedly advancing to the next label modulo N. Tapsell's Snake implementation explains a practical use of this ordering, including shortcuts that preserve the relative order of body segments.

The basic version needs no food search. Every free food cell lies somewhere ahead on the cycle, so a snake that keeps following the cycle eventually reaches it. This trades route efficiency for a simple invariant. The food may be geometrically nearby while still far away in the chosen cyclic order.

```text
next(i) = (i + 1) mod N
```

## 2. Parity tells you when a rectangle admits a cycle

Color a four-neighbor rectangular grid like a chessboard. Every edge changes color, so every cycle alternates colors and has even length. A Hamiltonian cycle is therefore impossible when the board has an odd number of cells. A one-cell-wide nonwrapping board also cannot contain such a cycle under the ordinary simple-graph definition.

For an unobstructed m by n rectangle, a Hamiltonian cycle exists when both dimensions exceed one and at least one is even. A constructive route reserves an edge column as a return corridor and snakes through the remaining cells. The grid-graph literature distinguishes this structured case from general grids with missing vertices, where finding Hamilton paths and circuits is computationally harder.

## 3. State the invariant before claiming safety

Assume the initial body is a contiguous, consistently oriented segment of the cycle; every nongrowing step removes its tail; eating adds exactly one segment; there are no changing obstacles; and filling the board ends the episode. Before the board is full, the next cycle cell is outside that contiguous body. Moving the head forward and updating the tail preserves contiguity. Induction gives freedom from self-collision while these assumptions hold.

This argument is about the specified engine. A starvation timer may expire before distant food is reached. Newly spawned walls may sever the cycle. A different initial body can already violate its order. A cycle drawn on top of a screenshot is not sufficient evidence that the snake can safely join it.

## 4. Shortcuts require a stronger check

A shortcut can reach food sooner by leaving the next cycle edge while preserving cyclic body order. But geometric adjacency is not the only condition. The move must not overtake occupied body positions, and growth must not let the head catch the tail. A correct implementation needs a precise convention for cyclic distance and for whether the tail moves on the chosen step.

Before enabling shortcuts, test the pure cycle controller. Then compare a shortcut controller against a complete transition replay on adversarial states near the tail and near full occupancy. A successful animation on a sparse board exercises the easiest regime, where many incorrect shortcut rules appear safe.

## 5. Interpret completion and efficiency separately

A controller can reliably fill a compatible board and still take many moves per apple. Report completion rate and step cost separately. If the cycle is randomly generated, record its seed and construction algorithm. Never describe a fixed-cycle guarantee as a solution to every wall-mode instance: the moment the traversable graph changes, its certificate must be revalidated or replaced.

## References

1. Alon Itai, Christos H. Papadimitriou, Jayme Luiz Szwarcfiter. [Hamilton Paths in Grid Graphs](https://csaws.cs.technion.ac.il/~itai/publications/Algorithms/Hamilton-paths.pdf). 1982.
2. John Tapsell. [Nokia 6110 Part 3 — Algorithms](https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/). 2015.
3. Battlesnake. [Battlesnake Game Rules](https://docs.battlesnake.com/rules). Official rules.

Figures and interactive controls are available at https://snakeguide.org/articles/hamiltonian-cycles
