# State-space growth and computational complexity

SnakeGuide · Technical note · November 2026

## Abstract

A grid with N cells does not imply a Snake planning problem with only N states. Ordered body configurations and planning horizons expand the search space. We distinguish loose counting bounds from hardness results, explain why general grid Hamiltonicity does not settle the unobstructed rectangular case, and specify measurements that expose practical search costs.

## Key point

Complexity belongs to a precisely defined problem. A small visual board can encode many ordered-body states.

## 1. The board is the small part

A W by H board has N = WH cells and at most four neighbors per cell. Static breadth-first search on this graph is linear in the number of cells and edges. That makes finding an ordinary shortest route a modest computation.

Snake planning is different because the body changes the legal moves. Each ordered body configuration can be a different search state. Counting only the N possible head positions hides nearly all of this structure.

## 2. A loose upper bound is still informative

For a body of fixed length ℓ, choosing an ordered sequence of distinct cells gives at most N!/(N−ℓ)! possibilities. Most of these sequences are not legal connected bodies, so this is a deliberately loose upper bound, not an exact count.

A geometric bound starts with N choices for the head and at most four choices for each next segment; forbidding immediate backtracking gives at most N·4·3^(ℓ−2) for ℓ≥2. Boundaries and self-avoidance reduce it further. Both bounds illustrate why storing complete bodies can be expensive.

```text
# bodies ≤ min{N!/(N−ℓ)!, N·4·3^(ℓ−2)}    for ℓ ≥ 2
```

## 3. A theorem needs the right problem

Hamiltonian path and circuit problems on general grid graphs have established hardness results. An unobstructed rectangle is a special graph family with much more structure. It is incorrect to transfer a general-grid hardness statement to every rectangular instance without qualification.

It is also incorrect to treat a theorem about a Hamiltonian path as automatically proving a theorem about a stochastic Snake objective. The input, permitted actions, objective, and decision question must match. The classic grid paper is useful precisely because it distinguishes graph families and problems.

## 4. Measure the actual computational burden

For a planner, report expanded states, maximum frontier size, time per action, and the search budget. For a learned controller, report training resources separately from inference resources. A fast action selection does not imply cheap training.

Use the simplest representation that supports the desired claim. Snapshot search is suitable for static routing. Full-state search is appropriate for exact short-horizon legality. Structured policies such as cycle following can bypass large searches by maintaining a strong invariant under restrictive assumptions.

## References

1. Alon Itai, Christos H. Papadimitriou, Jayme Luiz Szwarcfiter. [Hamilton Paths in Grid Graphs](https://csaws.cs.technion.ac.il/~itai/publications/Algorithms/Hamilton-paths.pdf). 1982.
2. NetworkX developers. [Single-source shortest paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.single_source_shortest_path.html). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/complexity
