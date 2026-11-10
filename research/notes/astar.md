# A* search: admissibility, consistency, and state design

SnakeGuide · Technical note · November 2026

## Abstract

A* combines accumulated path cost with a lower bound on remaining cost. We derive Manhattan distance from four-neighbor movement, examine consistency and node reopening, and explain how tie-breaking changes expansion patterns. Guarantees apply to the chosen search state: a static food route, a timed path, and a complete body trajectory are different planning problems.

## Key point

A heuristic is useful only relative to explicit movement rules and a correctly implemented search state.

## 1. Separate the cost paid from the cost predicted

A* prioritizes a candidate using the cost already paid to reach it plus a heuristic estimate of the remaining cost. With h equal to zero, the priority becomes Dijkstra's. With a useful lower bound, the frontier tends to favor cells pointing toward the target. The foundational work by Hart, Nilsson, and Raphael establishes heuristic search as a principled graph-search method rather than an arbitrary attraction toward the goal.

For Snake, first specify what a node means. It may be a cell in a frozen board, a cell with an arrival time, or an entire ordered body configuration. The same priority formula can search these different spaces, but the meaning and cost of a successor change dramatically.

```text
f(n) = g(n) + h(n)
```

## 2. Derive a heuristic from the movement rules

On a nonwrapping four-neighbor board with unit step cost, Manhattan distance is a lower bound: every horizontal coordinate difference requires a horizontal move, and every vertical difference requires a vertical move. Obstacles cannot make the route shorter than this bound. For example, from (2, 3) to (7, 5), any route needs at least seven moves. A wall may make the true route longer.

This derivation is conditional. If the board wraps, moving across a boundary can shorten the route, so ordinary Manhattan distance may overestimate. If diagonal moves are permitted, its interpretation changes again. If every edge costs at least c, multiply the Manhattan lower bound by c; arbitrary risk bonuses do not justify using a larger multiplier.

```text
h(x,y) = |x − x_goal| + |y − y_goal|
```

## 3. Admissibility is not the whole implementation

A heuristic is admissible when it never exceeds the true remaining minimum cost. It is consistent when h(u) is at most the edge cost from u to v plus h(v), for every edge. Consistency supports settling nodes without later reopening them in the usual graph-search implementation. With an admissible but inconsistent heuristic, a correct implementation may need to reopen a node after discovering a better route.

NetworkX explicitly warns that overestimating heuristics can return nonshortest paths. Its implementation also caches a node's first heuristic value. If an estimate changes with the evolving snake state, encode that state in the node or restart the search. Updating a visual board while reusing stale search values is a different algorithm from static A*.

## 4. Tie-breaking changes the picture

Many grid cells share the same f value. Choosing larger g first often produces a more directed-looking expansion, whereas a different tie-break can spread the frontier. Both may return equally short paths. Therefore a visually narrow search is not, by itself, evidence of a superior heuristic. Fix tie-breaking before comparing expanded-node counts.

A priority queue may contain an obsolete entry after a better g value is found. Ignore entries whose stored cost no longer matches the best known cost. Keep predecessor updates aligned with cost improvements. These details matter more than adding visual motion to the frontier.

## 5. Apply the guarantee to the correct problem

A* on the static food graph optimizes that graph's route cost. It does not guarantee that growth will leave an escape route. A* over complete body states can model those transitions, but the state space is much larger and a finite planning horizon can still miss later traps. Report the search model, termination condition, expansion budget, and fallback move. If a budget is exhausted, label the result as incomplete rather than unreachable.

## References

1. Peter E. Hart, Nils J. Nilsson, Bertram Raphael. [A Formal Basis for the Heuristic Determination of Minimum Cost Paths](https://www.cs.auckland.ac.nz/courses/compsci709s2c/resources/Mike.d/astarNilsson.pdf). 1968.
2. NetworkX developers. [A* path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html). Official documentation.
3. NetworkX developers. [Dijkstra path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/astar
