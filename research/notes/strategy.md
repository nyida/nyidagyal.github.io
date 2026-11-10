# From local heuristics to policy-level evaluation

SnakeGuide · Technical note · November 2026

## Abstract

A local score is useful only when its intended claim is explicit. We translate space, distance, and escape intuitions into measurable features, construct failure cases, and distinguish legal-move checks from long-horizon policy evaluation. The resulting framework supports interpretable baselines without attributing survival guarantees to unverified heuristics.

## Key point

A strategy becomes testable when its objective, state features, action rule, and failure criterion are explicit.

## 1. Name the decision you are making

A player may describe a move as “safe” because it avoids immediate collision, preserves open space, or follows a familiar pattern. These are different claims. Begin by deciding whether the objective is immediate legality, eventual food collection, long survival, or full-board completion.

A route that minimizes steps to food may be poor for survival. A cycle policy can preserve a collision-free traversal yet take a long route to food. Strategy is partly the choice of objective, not only the choice of movement rule.

## 2. Turn intuition into features

“Leave yourself room” can become a reachable-area score. “Keep an exit” can become a test for a path to a chosen target. “Do not cut yourself off” can become a component or bottleneck analysis. Each translation is an abstraction with a specific scope.

Write down how a candidate action is simulated and how its resulting state is scored. If several moves tie, specify a deterministic ordering. Otherwise, two implementations with the same verbal strategy may behave differently.

## 3. Construct counterexamples

A spacious chamber with one entrance challenges area-based reasoning. Food at the end of a narrow corridor challenges greedy distance minimization. A body about to vacate a passage challenges a frozen obstacle model. Small examples reveal the assumptions behind a strategy more clearly than a single impressive run.

Save the complete ordered body, food, obstacles, and intended action. A screenshot alone may omit direction, growth state, or timing. The lab’s state export can preserve these details for its own rules, while other games need their own recording formats.

## 4. Evaluate the claim you actually made

For immediate collision avoidance, count illegal proposed actions. For survival, report termination causes and episode lengths. For food efficiency, report moves per food alongside completion and failure rates. No single score captures all three objectives.

Human speedrunning introduces additional constraints such as input speed, game version, and category rules. Algorithm demonstrations here use explicitly documented educational rules; they do not establish a leaderboard record or reproduce a particular competitive category. A useful technical guide keeps those interpretations separate.

## References

1. NetworkX developers. [Articulation points](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html). Official documentation.
2. John Tapsell. [Nokia 6110 Part 3 — Algorithms](https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/). 2015.
3. Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, Marc G. Bellemare. [Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://arxiv.org/abs/2108.13264). 2021.

Figures and interactive controls are available at https://snakeguide.org/articles/strategy
