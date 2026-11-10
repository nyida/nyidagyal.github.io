# Reachable-space heuristics and their limitations

SnakeGuide · Technical note · November 2026

## Abstract

Flood fill measures the size of a connected free-space component in a frozen board. We explain its linear graph-search cost and show why the count does not certify that a moving snake can occupy or leave that region. Connectivity, bottlenecks, body order, and future growth must be considered separately when interpreting a space heuristic.

## Key point

Reachable area measures a static component. Survival depends on how the body can move through it.

## 1. Turn open cells into a component

A flood fill starts at a cell and repeatedly visits each traversable neighbor. On a grid, a queue gives breadth-first traversal and a stack gives depth-first traversal. Both recover the same connected component when they use the same obstacle set.

To evaluate a candidate Snake move, first simulate that move. Then construct a snapshot of blocked cells and flood from the new head. This ordering matters: evaluating the old board can miss the new head’s obstruction or a tail cell that has just become free.

## 2. Use the count with care

A component with many open cells gives the head room to maneuver. A small component is a warning about confinement. One common heuristic compares reachable cells with body length, but the comparison depends on whether the head is counted and which body cells were removed from the graph.

Even a region larger than the body can have a dead end or a narrow passage that prevents safe traversal. Conversely, a small frozen region may expand as the tail moves. The count is neither a universal sufficient condition nor a universal necessary condition for eventual survival.

```text
R(s) = |reachable vertices from the head in the chosen snapshot graph|
```

## 3. Distinguish connectivity from route structure

A connected component guarantees a path between pairs of its vertices in the static graph. It does not guarantee a simple route visiting every vertex, a closed route, or an order compatible with a moving body. Those are stronger properties.

For example, a chamber attached through a one-cell neck can contribute many cells to the count. Entering it may still seal the exit behind the head. Articulation analysis exposes this neck; simulation reveals when the body might release it. Neither should be replaced by an unexplained threshold.

## 4. Make it an interpretable baseline

A transparent controller can reject immediate collisions, compute a flood-fill score for each remaining move, and use food distance to break ties. Document the score ordering and neighbor tie-break so the behavior can be reproduced. Such a controller is a baseline, not an optimal policy.

Measure failures by geometry: cul-de-sac entry, premature closure, starvation when applicable, and collision after growth. This turns a scalar score into a useful diagnostic. The article’s reasoning is an application of graph connectivity; the sources provide the underlying traversal and cut-vertex definitions.

## References

1. NetworkX developers. [Single-source shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.single_source_shortest_path.html). Official documentation.
2. NetworkX developers. [Articulation points](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/flood-fill
