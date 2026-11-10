# Observation sufficiency and the Markov property

SnakeGuide · Technical note · November 2026

## Abstract

An observation can merge simulator states whose legal successors differ. We examine information lost by occupancy-only images and compact local features, including body order and pending growth. Channel definitions must be tied to the transition semantics; a recurrent controller may infer hidden state, but recurrence alone does not establish observability or a safety guarantee.

## Key point

Before increasing model capacity, verify that the observation retains the information the decision requires.

## 1. The simulator state and agent observation differ

The simulator may store an ordered list of body cells, direction, food locations, obstacles, pending growth, and rule-specific counters. The agent receives an observation derived from that state. A screenshot is one possible observation; a tensor of semantic board channels is another. Neither is automatically complete.

A fully informative observation must retain the variables needed to predict the next-state distribution after an action. If a finite game ends when a clock expires, the remaining clock matters. If growth is delayed, the growth state matters. If future food is sampled independently according to a known distribution, the agent need not see the random-number generator's internal bits to model that distribution.

## 2. Occupancy alone can merge different futures

An occupied-cell mask says where the body is but not necessarily the order in which cells will be released. Consider a body that touches itself without crossing: adjacency in the displayed occupied region does not uniquely identify the body's consecutive segments. Two valid ordered bodies can therefore have indistinguishable occupancy while their future tail releases differ.

Adding head and tail channels improves the representation but does not, in general, resolve every interior ordering ambiguity. An ordered coordinate list is explicit. A board channel that encodes each segment's position along the body also preserves the order, provided repeated positions permitted by a variant are handled separately. Battlesnake's initial overlapping segments illustrate why a universal single-value-per-cell encoding needs care.

## 3. Compact features trade convenience for information

A small vector containing immediate danger, current direction, and the direction of food can be convenient for a first agent. It can also map a wide-open board and a nearly sealed pocket to the same observation. A policy using that vector must choose the same action distribution for both unless it has memory. No larger feed-forward network can reconstruct information that the encoding discarded.

This is a testable limitation. Construct two board states with identical feature vectors but different safe continuations. If such a pair exists, the representation aliases those states. The experiment identifies a representational constraint, not necessarily a defect in the optimizer. Recurrent memory may help, but only when the observation history contains the missing information.

## 4. Use channels with precise semantics

For a structured board input, separate walls, food, head, body, and any hazards. Specify the coordinate origin and which tensor axis represents width. Encode orientation and scalar counters explicitly. If board sizes vary, define padding and a valid-cell mask so a padded zero cannot be mistaken for traversable space.

Rotation augmentation requires transforming actions as well as boards. A north move in the original state becomes a different move after rotation. Test the transition correspondence: transforming a successor should agree with stepping the transformed state using the transformed action. A failure exposes an implementation inconsistency before it becomes a training anomaly.

## 5. Choose a research question the observation can support

Pixel-based learning asks an agent to infer useful visual structure; semantic channels provide some of that structure in advance. DQN's original image-based experiments illustrate the former approach, but do not make it obligatory. Compare controllers with matching access to state, or disclose the difference as part of the experiment.

Gymnasium formalizes observation spaces and environment interfaces; it does not prove that an observation is sufficient. Document exactly what is exposed, hidden, normalized, and remembered. Then use state-pair counterexamples and replay inspection to establish the practical limits of the representation.

## References

1. Farama Foundation. [Gymnasium Env API](https://gymnasium.farama.org/api/env/). Official documentation.
2. Volodymyr Mnih et al.. [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602). 2013.
3. Battlesnake. [Battlesnake Game Rules](https://docs.battlesnake.com/rules). Official rules.

Figures and interactive controls are available at https://snakeguide.org/articles/observation-design
