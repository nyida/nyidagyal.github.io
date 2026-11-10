# Value-based and policy-gradient methods for Snake

SnakeGuide · Technical note · November 2026

## Abstract

A learning formulation must specify observations, actions, transitions, rewards, and episode boundaries. We connect DQN’s action-value learning and PPO’s policy updates to that formulation, with attention to termination, truncation, and evaluation. The cited papers establish general methods; their reported results do not measure the Snake environment implemented here.

## Key point

The neural network is only one component. Observation semantics, episode boundaries, and evaluation determine what learning success means.

## 1. Write the task before training the model

A learning environment needs a state, an observation, an action set, a transition rule, and a reward. For Snake, the environment can retain the ordered body even if the agent sees only an image. Actions might be absolute directions or relative turns. These are not interchangeable interfaces: a relative action depends on current orientation, while an absolute action may include an illegal reversal.

Choose the evaluation target independently of the training reward. Maximizing discounted food reward, maximizing final length, and maximizing survival time can induce different behavior. A controller that circles forever may score well under a survival bonus while making no progress toward filling the board.

## 2. DQN learns action values

A Q network estimates expected discounted return for each action. A common temporal-difference target combines the observed reward with the largest predicted next-state value, except at true terminal states. Mnih and colleagues' 2013 work learns action values from images and uses experience replay. Those Atari experiments motivate an algorithmic approach; they are not evidence that a particular Snake implementation works.

In a Snake experiment, replay records should retain the observation, selected action, reward, successor observation, and termination information. Check them by decoding several transitions back into board states. A single coordinate transposition can produce plausible loss curves while training on the wrong movement relationship.

```text
y = r + γ(1 − terminal) max_a Q_target(o_next, a)
```

## 3. PPO updates a policy directly

PPO uses trajectories to update a parameterized action distribution. Its clipped surrogate limits the incentive to change a sampled action's probability ratio too far in one update. This is an optimization mechanism, not a guarantee that the policy avoids collisions. The original paper describes a family of policy-gradient methods and evaluates them on several control benchmarks.

For Snake, an action mask can eliminate moves known to be immediately illegal. Apply the same mask when sampling actions and calculating their probabilities during training. Otherwise the logged policy probability and the behavior that generated the data disagree. State whether the baseline controller receives the same legality information; a comparison can be distorted by unequal interfaces.

## 4. Do not let episode bookkeeping redefine the task

Gymnasium separates termination from truncation. A collision or a declared full-board win can be a true terminal event. A diagnostic step limit may instead truncate an otherwise continuing task. Value targets should reflect that distinction; treating every cutoff as death changes the learning problem.

A finite-horizon task is different: if the rules genuinely end after a fixed number of moves, the remaining time belongs in a fully observed state. Write down whether a maximum-step setting is part of the game or merely an experimental budget. The same numeric cutoff can have either meaning.

## 5. Make improvement falsifiable

Compare against random legal play, a static path planner, and a compatible cycle policy where applicable. Hold evaluation seeds apart from tuning seeds. Record multiple independent training runs, not just many games from one favorable model. Plot the distribution of final length and report collision causes and decision cost. Without measured runs, describe the learning system as a design or implementation, not a trained result.

Inspect counterexamples: the first missed reachable apple, the first avoidable pocket entry, and the first action-mask disagreement often explain more than a smooth average-reward curve. A useful research artifact connects its numerical result back to a reproducible sequence of states.

## References

1. Volodymyr Mnih et al.. [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602). 2013.
2. John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov. [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347). 2017.
3. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.
4. Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, David Meger. [Deep Reinforcement Learning That Matters](https://arxiv.org/abs/1709.06560). 2018.

Figures and interactive controls are available at https://snakeguide.org/articles/reinforcement-learning
