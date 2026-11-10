# Potential-based reward shaping and policy invariance

SnakeGuide · Technical note · November 2026

## Abstract

Additional rewards can change the task an agent optimizes. We introduce potential-based shaping and its telescoping structure, then analyze discounting, terminal potentials, and finite episode boundaries. A distance bonus inherits no policy-preservation guarantee unless its construction satisfies the relevant assumptions; training signals should therefore remain separately observable.

## Key point

Calculate the incentives on short trajectories. When using potential shaping, preserve its discount and boundary assumptions in code.

## 1. An intuitive bonus defines a new incentive

Suppose the intended task rewards food and penalizes collision. Adding a small reward for every surviving step can make endless circling attractive. Rewarding every move toward food can encourage repeated approach-and-retreat patterns if retreat is not charged consistently. These are direct consequences of the return calculation, not evidence that an agent has misunderstood its instructions.

Audit a proposed reward by constructing short trajectories before training. Compare a direct meal, a safe detour, a useless loop, and an early collision. Sum the discounted rewards explicitly. If the wrong trajectory already wins this calculation, additional compute will not fix the objective.

## 2. Use a potential when policy preservation matters

Ng, Harada, and Russell identify potential-based shaping as a policy-preserving transformation under their stated MDP assumptions. Add F(s,s′) = γΦ(s′) − Φ(s) to the base reward, using the same discount γ as the task. Along a trajectory, the shaping return telescopes to −Φ(s₀) + γ^TΦ(s_T). For bounded potentials and discount below one, the final term vanishes in the infinite-horizon limit. For an episodic construction, setting terminal potential to zero removes the endpoint dependence.

This is a structural guarantee about the objective, not a guarantee of faster learning or finite-sample convergence. Arbitrary distance bonuses do not qualify merely because they appear to encourage progress.

```text
r_shaped(s,a,s′) = r_base(s,a,s′) + γΦ(s′) − Φ(s)
```

## 3. A Snake potential has edge cases

A candidate potential is negative distance to the current food. On a finite board, Manhattan distance is bounded and easy to calculate. However, the goal changes after eating. Compute Φ on the actual successor state, including newly spawned food, rather than silently retaining the old target. The resulting jump can look surprising while still being consistent with a state potential.

If no food remains after a full-board win, define the terminal potential explicitly instead of calling a distance function with a missing target. If a path-based potential uses infinity for unreachable food, it is no longer bounded; replace that with a documented finite value or choose another potential. An implementation detail can invalidate the assumptions behind the formula.

## 4. Keep training signals visible

Log base reward and shaping reward separately. A rising shaped return may reflect different state potentials rather than more food. Evaluate the final policy on the original game metrics, and retain the shaping configuration as part of the experiment. The evaluation code should not need to reverse-engineer what a large aggregate reward means.

For a concrete unit-level audit, choose a fixed sequence of valid states and compare the explicit discounted sum of shaping terms with the telescoping expression. Test sequences containing a food respawn, a collision, and a full-board terminal state. These checks examine mathematical consistency rather than asserting that training will succeed.

## 5. Do not confuse truncation with a terminal boundary

A training rollout can stop before the task ends. Forcing the final potential to zero at every arbitrary rollout boundary changes the shaping calculation unless the continuing value is handled consistently. Decide whether a limit ends the actual game or only the collected sample. Then use that decision in both the return target and potential treatment.

Potential shaping remains a design choice. A simple sparse reward may be adequate for a small controlled experiment. The reason to introduce a potential is a specified learning problem, accompanied by an audit that preserves the evaluation objective.

## References

1. Andrew Y. Ng, Daishi Harada, Stuart Russell. [Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping](https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf). 1999.
2. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/reward-shaping
