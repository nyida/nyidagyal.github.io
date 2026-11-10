# Breadth-first search on static occupancy graphs

SnakeGuide · Technical note · November 2026

## Abstract

Breadth-first search provides a shortest route on an unweighted graph through FIFO expansion. We specify the graph induced by a frozen Snake board, trace the distance wave, and separate route optimality from post-growth safety. The interactive comparison makes the objective mismatch visible when entering some cells incurs additional cost.

## Key point

BFS certifies a shortest path in the graph you give it. It does not certify the future safety of the snake.

## 1. Choose the graph before choosing the algorithm

Represent each currently traversable cell by a vertex. Connect cells that share an edge, provided the rules allow that move. With unit movement cost, this graph captures the question: how many moves separate the head from a target while the blocked cells remain fixed? NetworkX's unweighted shortest-path interface solves this graph problem. The important qualification is the frozen obstacle model. Snake changes that model after every move.

For a simple baseline, remove the body except the head from the graph. A more permissive baseline may release the current tail when a nongrowing move removes it. Document that choice: the two graphs can return different routes for the same displayed board. Neither convention alone describes the entire future body.

## 2. A queue creates a distance wave

Breadth-first search uses a first-in, first-out queue. Discover the starting cell at distance zero, then discover its unvisited neighbors at distance one. Every later layer is one move farther away. Mark a vertex when it enters the queue, not when it leaves; otherwise several parents may enqueue the same cell and inflate the work.

Store a predecessor for each discovered cell. Once the food is reached, follow those predecessors backward and reverse the sequence. A four-neighbor board with N cells has at most four outgoing neighbor checks per cell, so a full traversal uses linear time and linear storage. A rectangular obstacle-free board has an especially useful sanity check: the returned distance equals the Manhattan distance.

```text
d(v) = d(parent(v)) + 1
```

```text
queue = [start]
parent = {start: None}
for cell in queue:
    if cell == goal:
        break
    for nxt in neighbors(cell):
        if nxt not in blocked and nxt not in parent:
            parent[nxt] = cell
            queue.append(nxt)
```

## 3. Shortest is local to the objective

Consider two entrances to a pocket containing food. One takes four moves, the other six. BFS selects the four-move route if both are legal in its graph. But eating may leave the head facing a wall while its own body closes the only exit. The algorithm has answered its specified question correctly; the objective omitted the continuation.

Replanning after each move does not retroactively repair an irreversible entry into that pocket. A one-step controller can repeatedly select locally valid moves until no valid successor remains. The distinction is between reaching a target vertex in a snapshot and finding a sequence of complete game states that remains viable.

## 4. Use the baseline to expose assumptions

Inspect the returned path before executing it. Count its edges, confirm every edge is legal, and compare it with an independent distance calculation on small boards. Then replay the route through the actual transition function, including growth. If the replay fails, the graph abstraction was too permissive or the engine and planner disagree.

When BFS finds no static path, this does not necessarily establish that food is unreachable in the real game. Waiting through a legal detour may let the tail uncover a corridor. Conversely, finding a path says little about survival after the meal. These are concrete limits of the model, not shortcomings of the queue.

## 5. Measure the useful things

For an algorithm comparison, retain the same board, neighbor order, target, and blocking convention. Report path length, expanded cells, and decision latency separately. A shorter route and a cheaper search are different accomplishments. For a game evaluation, add food collected, failure cause, and the number of truncated episodes. A search diagram should make the frontier, explored cells, and final route distinguishable.

## References

1. NetworkX developers. [Single-source shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.single_source_shortest_path.html). Official documentation.
2. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/bfs
