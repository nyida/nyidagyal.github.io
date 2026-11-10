# Boundary conditions and wall-mode topology

SnakeGuide · Technical note · November 2026

## Abstract

The phrase wall mode can denote solid boundaries, fixed internal obstacles, or obstacles introduced during play. These cases produce different transition systems. We separate board geometry from temporary body occupancy, describe how dynamic events alter reachability, and organize positions by constraints that can be inspected without assuming a universal game implementation.

## Key point

Wall geometry, body timing, and wall-generation rules must be specified independently.

## 1. Three different meanings of wall

A solid boundary forbids leaving the rectangle. An interior obstacle removes a vertex or forbids traversal through it. A dynamic wall changes the available graph during play. These mechanisms are often grouped under “wall mode,” but they create different planning problems.

Our pathfinding lab uses editable interior obstacles that remain fixed during a search. It is not a reproduction of a proprietary game’s wall-spawning rules. An analysis of a particular game needs its exact version, placement process, timing, and collision convention.

## 2. Separate geometry from body occupancy

Let G be the four-neighbor board graph. Removing obstacle vertices gives the traversable terrain graph. Removing the body, subject to the tail convention, gives a momentary free-space graph. The terrain may stay fixed while the free-space graph changes at every move.

This distinction explains why two visually similar bottlenecks behave differently. A passage blocked by a fixed wall never opens under the current rules. A passage blocked by the tail may open on the next move. A component analysis must identify which of these graphs it analyzes.

```text
Gterrain = G[V ∖ O]    and    Gsnapshot = G[V ∖ (O ∪ Bblocked)]
```

## 3. Specify dynamic wall events

A wall-spawning model needs a candidate set, a sampling distribution, an event trigger, and exclusions. For example, “spawn after each food” leaves unanswered whether the new food, body, and essential passages can be covered. A connectivity-preserving sampler defines a different task from unrestricted sampling.

If wall placement is stochastic, a policy’s safety can be probabilistic even when its movement is deterministic. A guarantee based on one fixed Hamiltonian cycle expires when an inserted wall removes a vertex on that cycle. Replanning is an additional obligation, not a consequence of the old proof.

## 4. A useful position taxonomy

Describe a position by traversable components, narrow passages, body occupancy, head and tail placement, and the available exit directions. Then distinguish immediate illegal moves, finite-horizon traps, and states merely rejected by a heuristic. These labels carry different evidential strength.

A practical case study should retain the full ordered body and wall set, show the failed action, and replay the transition. Calling a state “unavoidable” requires a proof or exhaustive analysis under a precisely bounded ruleset. A failed agent run alone establishes only that the tested agent failed.

## References

1. NetworkX developers. [Articulation points](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html). Official documentation.
2. Battlesnake. [Battlesnake Ruleset API object](https://docs.battlesnake.com/api/objects/ruleset). Official documentation.
3. Alon Itai, Christos H. Papadimitriou, Jayme Luiz Szwarcfiter. [Hamilton Paths in Grid Graphs](https://csaws.cs.technion.ac.il/~itai/publications/Algorithms/Hamilton-paths.pdf). 1982.

Figures and interactive controls are available at https://snakeguide.org/articles/wall-mode
