# A taxonomy of Snake rule variants

SnakeGuide · Technical note · November 2026

## Abstract

Boundary wrapping, growth timing, simultaneous opponents, and obstacle events change the computational task. We compare their effects on distance functions, collision resolution, and the state required for planning. A matched comparison must preserve the complete ruleset rather than assuming that implementations sharing the name Snake define the same environment.

## Key point

Changing one rule can invalidate a heuristic, a proof, or a benchmark comparison.

## 1. Boundary topology changes distance

On a solid rectangular board, reaching a cell on the opposite edge requires traversing the intervening columns. On a wrapping board, crossing the edge may be a single move. A heuristic derived for one topology can overestimate distance in the other.

For a W by H toroidal board without obstacles, the shortest four-neighbor distance uses the smaller wrapped displacement in each coordinate. Obstacles can only increase that distance, so it remains a lower bound for routing under the same motion rules.

```text
h = min(|Δx|, W−|Δx|) + min(|Δy|, H−|Δy|)
```

## 2. Growth is part of the dynamics

Immediate growth retains the tail on the food-eating move. Other games can store pending growth or duplicate the tail and reveal the extension later. These implementations change when cells become traversable.

Multiple food cells, changing food values, and timed obstacles add further state. The phrase “standard Snake” is not a complete environment specification. Store the precise rule parameters with every evaluation.

## 3. Multiplayer introduces simultaneous decisions

In simultaneous multiplayer, another snake’s next head position is not known when choosing an action. A cell empty in the current frame may be contested on the next turn. Modeling every opponent as a static wall omits this interaction.

Battlesnake documents a concrete ruleset with health, simultaneous movement, body collisions, and head-to-head resolution. Its official rules are a primary reference for that game. They should not be treated as a universal rulebook for all Snake variants.

## 4. Compare methods on matched tasks

A completion guarantee on a fixed empty rectangle cannot be transferred to changing obstacles, adversarial opponents, or a starvation limit. Similarly, an average score from one board size says little about another without normalization and the full experimental setup.

A comparison table should include board topology, initial length, food process, growth semantics, collision order, time limits, and opponent policy. Keep the software version or ruleset identifier. The linked Battlesnake ruleset object is a practical example of recording both names and versioned settings.

## References

1. Battlesnake. [Battlesnake Game Rules](https://docs.battlesnake.com/rules). Official rules.
2. Battlesnake. [Battlesnake Ruleset API object](https://docs.battlesnake.com/api/objects/ruleset). Official documentation.
3. NetworkX developers. [A* path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/variants
