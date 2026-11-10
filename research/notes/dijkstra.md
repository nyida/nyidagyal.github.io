# Weighted shortest paths and risk-sensitive objectives

SnakeGuide · Technical note · November 2026

## Abstract

Dijkstra’s algorithm finds minimum-cost paths under nonnegative edge weights. We derive relaxation, distinguish movement cost from a learned reward, and show why a manually chosen penalty is not a calibrated probability of failure. A shared weighted-grid example compares the fewest-move path with the minimum-cost path and exposes their different objectives.

## Key point

Dijkstra makes a weighted objective precise. The credibility of the resulting move still depends on the objective and state representation.

## 1. A longer route may be cheaper

Breadth-first search treats every move equally. Dijkstra's algorithm is useful when legal moves have different nonnegative costs. The goal is a path with minimum total cost, which may contain more steps than the shortest unweighted route. NetworkX's Dijkstra interface supports weights stored on edges or computed by a function.

Suppose a five-step route crosses two hazardous cells and a seven-step route avoids them. If a normal step costs one and entering a hazardous cell adds three, the first route costs eleven and the second costs seven. The detour is optimal for that cost model. It is not automatically optimal for score, survival, or wall-clock time.

```text
cost(P) = Σ cost(v_i, v_(i+1))
```

## 2. Relaxation is the central operation

Maintain the best known cost to each vertex. When expanding u, consider whether reaching a neighbor v through u improves its current value. If so, update the value and predecessor. A minimum-priority queue chooses the next unsettled vertex. With nonnegative edge weights, a removed minimum has no undiscovered cheaper route through a more expensive frontier vertex.

For a sparse grid, a binary-heap implementation typically takes O((V + E) log V) time. The precise bound depends on queue operations and how duplicate entries are handled. BFS is simpler when every edge has identical cost; replacing its queue with a heap then adds machinery without changing the optimization problem.

```text
d(v) ← min(d(v), d(u) + w(u,v))
```

```text
if distance[u] + weight(u, v) < distance[v]:
    distance[v] = distance[u] + weight(u, v)
    parent[v] = u
    push(priority_queue, (distance[v], v))
```

## 3. Design costs that answer a defensible question

A Snake planner might penalize proximity to a wall, entry into a narrow region, or a predicted collision threat. These penalties are design choices. A cost of five does not mean a five-percent death probability. If the weights are heuristic, describe them as heuristic and evaluate the resulting policy against alternatives.

Some costs cannot be represented by a cell alone. Charging for a turn requires the incoming direction, so the node should include direction. Charging for a corridor becoming occupied after several moves requires time or a richer state. If two arrivals at the same cell have different relevant futures, merging them can discard the better plan.

## 4. Keep reward and route cost separate

Do not insert a negative edge whenever food is encountered and expect ordinary Dijkstra to remain valid. Negative costs break its settling argument, and negative cycles may make a minimum undefined. A reward-maximizing sequential game is not automatically a shortest-path problem. Define a finite objective or use an algorithm suited to the resulting model.

Even nonnegative risk penalties can conceal hard constraints. An actually illegal move should be absent from the graph, not merely expensive. Otherwise a planner may select it when all legal routes cost more. Conversely, treating every mildly risky cell as forbidden can prevent useful escape routes.

## 5. Audit weighted results

Display both route length and total weighted cost. Show the contribution of each penalty so readers can explain why a detour was chosen. Check the algorithm against BFS when all weights are one and against manually computed tiny examples when weights differ. Repeat sensitivity experiments with several penalty scales. If a small coefficient change reverses the policy, that sensitivity is a substantive result about the model.

## References

1. NetworkX developers. [Dijkstra path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html). Official documentation.
2. NetworkX developers. [Single-source shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.single_source_shortest_path.html). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/dijkstra
