# Articulation points and dynamic escape routes

SnakeGuide · Technical note · November 2026

## Abstract

Removing a cut vertex disconnects a static graph, but the occupied cells of Snake change over time. This note relates articulation points to pockets and return paths, then separates a geometric warning from a survival guarantee. An interactive figure recomputes reachable cells when the only corridor between two board regions is closed.

## Key point

A bottleneck marks a dependence on one passage. Whether it becomes fatal is a question about time and body order.

## 1. Identify the hinge

An articulation vertex is a vertex whose removal increases the number of connected components. In a grid, it can represent the only passage between two chambers. The definition is about a particular graph; always state whether that graph includes the body as blocked terrain.

The figure shows a wall dividing two regions except for one opening. Removing the opening disconnects the terrain graph. Occupying it with the body may temporarily have the same effect, but the timing of that occupation matters.

## 2. A pocket is a geometric description

A pocket is an informal name for a region with restricted access. Its danger depends on the entrance width, internal routes, food position, body length, and how long the entrance remains occupied. A large pocket can be dangerous, while a small one can be harmless to a short snake.

Before entering, ask where the head can turn, where the tail will be, and whether the body blocks the only return route. A one-cell corridor is especially restrictive because a body longer than one cannot simply reverse through its neck.

## 3. Static decomposition, dynamic reasoning

Cut vertices can be found by a depth-first traversal that tracks discovery times and low-link values. For a graph with V vertices and E edges, standard articulation analysis takes O(V+E) time. On a four-neighbor grid, E grows linearly with V.

The decomposition helps prioritize danger, but a cut in the current free-space graph may disappear after a tail release. Conversely, a move can create a new cut by occupying an open cell. Recompute or update the graph after simulating the candidate action instead of treating its topology as permanent.

## 4. A defensible escape test

One conservative procedure is to simulate a food route, inspect its terminal state, and reject it if a separately specified continuation test fails. This makes the criterion reviewable: the route simulation, graph construction, and continuation search can each be inspected.

It is still possible to reject safe moves or accept moves that fail beyond the searched horizon. Report the horizon and the abstraction. Reserve “trap” for a demonstrable claim such as “all legal action sequences die within k steps”; use “risk” for a geometric warning without that proof.

## References

1. NetworkX developers. [Articulation points](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html). Official documentation.
2. NetworkX developers. [Single-source shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.single_source_shortest_path.html). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/bottlenecks
