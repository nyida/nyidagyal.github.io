# Experimental design for reproducible Snake evaluation

SnakeGuide · Technical note · November 2026

## Abstract

A comparison requires complete rules, explicit randomness, and a defined sampling unit. We distinguish variation across training runs from repeated games by one trained model, specify failure and efficiency metrics, and discuss distributional reporting. The protocol emphasizes reconstructable counterexamples and qualified claims rather than a leaderboard based only on a mean score.

## Key point

A credible comparison is a recoverable experiment: rules, code, randomness, raw outcomes, and uncertainty travel together.

## 1. Define the experiment, not just its name

A result labeled Snake score is underspecified. Record board dimensions, boundary behavior, initial body, reversal rules, food count and placement policy, growth timing, obstacle schedule, win condition, and any step limit. A change to one field can alter which strategies are feasible. Include a versioned engine or commit identifier so the transition function can be recovered.

Battlesnake's API illustrates this principle by carrying a ruleset name, version, and settings. For a custom single-player engine, provide an equivalent configuration record. Do not infer that two programs implement identical rules simply because both draw a green snake and red food.

## 2. A seed is necessary metadata, not a complete recipe

Record the pseudorandom generator, seed list, generator version, and the sequence in which random choices are requested. NumPy's compatibility policy explicitly conditions reproducible streams on details beyond a seed. A saved sequence of food placements and actions can be more robust for debugging than expecting a future software stack to regenerate it.

Using the same seed across controllers does not guarantee the same food cells: different bodies can leave different valid spawn sets. Describe the coupling precisely. For instance, use the same random draw stream with a fixed ordering of free cells. This pairs the random inputs while allowing the realized game states to diverge.

## 3. Separate the sources of variation

For a deterministic planner, repeated environment seeds measure variation in game instances. For a learned controller, training initialization and data order introduce another layer. Many evaluation episodes from one trained model do not substitute for several independent training runs. Henderson and colleagues emphasize the reproducibility problems created by such experimental variation.

Retain training seeds and evaluation seeds separately. Tune parameters on a development set, then freeze them before evaluating held-out seeds. If the same difficult boards repeatedly guide improvements, those boards have become part of development even when the file is called test. Maintain a fresh evaluation set for the final comparison.

## 4. Report distributions and failures

Food collected, final occupancy, moves per food, completion rate, and decision latency answer different questions. Report collision categories and truncations rather than hiding them inside a single average. A controller that survives until the step cap without eating should remain visible as a stalled run.

Agarwal and colleagues show why limited-run RL comparisons need uncertainty estimates rather than point estimates alone. Choose intervals and resampling units that match the design. If comparing learned methods, preserve the hierarchy of training runs and episodes; if comparing fixed planners on paired boards, retain that pairing. A narrow interval from incorrectly treating dependent observations as independent is misleading.

## 5. Publish enough to replay a counterexample

A useful result bundle contains the configuration, algorithm version, seeds, per-episode metrics, and replay traces for representative failures. Include exact commands and a machine-readable schema. Preserve an action's requested direction separately from the engine's applied move if invalid inputs are normalized. This allows a reviewer to determine whether a failure came from planning, action handling, or simulation.

Every chart should identify whether it shows measured runs, a constructed example, or an illustrative diagram. Until experiments have actually been executed, a benchmark page should present a protocol and runnable tools rather than fabricated performance numbers.

## References

1. Battlesnake. [Battlesnake Ruleset API object](https://docs.battlesnake.com/api/objects/ruleset). Official documentation.
2. NumPy developers. [Random-number compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html). Official documentation.
3. Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, David Meger. [Deep Reinforcement Learning That Matters](https://arxiv.org/abs/1709.06560). 2018.
4. Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, Marc G. Bellemare. [Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://arxiv.org/abs/2108.13264). 2021.
5. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.

Figures and interactive controls are available at https://snakeguide.org/articles/reproducible-evaluation
