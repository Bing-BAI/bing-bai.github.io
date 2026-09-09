## Goal

Investigate whether training-time optimization could reduce both sensor requirements and model memory while retaining activity recognition capability.

Building on an existing compressed edge model, the research made two questions trainable and testable: which inputs were essential, and which network filters could be removed?

## Inputs

- Multi-sensor time-series data, activity labels and a baseline model.
- Group definitions for sensor channels and convolutional filters.
- Sparse regularizers, including Group Lasso and Hoyer-square, added to the training loss.
- Metrics for accuracy, sensor count, selection time and model size.

Reducing inputs and capacity can both affect recognition. Evaluation needed consistent data and baselines and separate accounting for gains at each stage.

## User flow

This was a researcher-facing training and evaluation workflow:

1. Train or reproduce the baseline and define comparison data and metrics.
2. Group sensor channels and apply sparse constraints so the model learns input importance.
3. Select sensors and evaluate recognition and selection cost with fewer inputs.
4. Apply grouping to convolutional filters, train with sparsity, remove all-zero filters and fine-tune.
5. Compare size and recognition across stages and analyze the method’s assumptions.

## Outputs

For sensor selection, I added sparse regularization to training, replacing stepwise search with learned importance. The approach reduced sensor requirements while retaining recognition performance, with selection time also compared.

For compression, I reused the regularization idea with groups of convolutional filters instead of input channels. Pruning and fine-tuning further reduced the existing model. Outputs included training methods, comparative experiments and accuracy/resource analysis.

Both parts followed the same principle: identify effective structure, then test whether the remaining burden can be removed.

## Scope

- This was master’s research and experimentation, not a general production service guarantee.
- Fewer sensors do not automatically reduce hardware costs proportionally; device changes need separate assessment.
- Smaller models do not necessarily run faster on every device; latency must be measured on target hardware.
- Transfer to other datasets and networks requires renewed evaluation of grouping, sparsity strength and task performance.

## Acceptance criteria

- Compare full-input, sensor-selected and filter-pruned models using the same data splits and recognition criteria.
- Report sensor requirements, selection time and model size with their experimental conditions.
- Distinguish the existing compressed baseline from sensor selection and subsequent pruning stages.
- Examine fine-tuning after pruning and accuracy/resource trade-offs.

This account describes methods and validation without untested claims of cross-device benefits.

## Iteration

Starting from an existing edge model, I questioned whether every sensor was necessary, then extended useful sparse-training ideas to network filters. Induction and generalization formed a loop: find a reusable structure and test its applicability through new experiments.

Product use would require further validation of input acquisition costs, target-device latency and field data changes, turning research compression gains into usable system value.
