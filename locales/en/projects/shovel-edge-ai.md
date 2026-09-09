## Goal

Deploy machinery activity recognition on field devices with limited memory and processing power, retaining recognition quality while meeting real-time time-series processing requirements.

In this industry research collaboration, I handled model search, compression and edge performance validation, testing algorithm choices against actual hardware and runtime constraints and participating in field validation.

## Inputs

- Time-series sensor data, activity labels and a baseline recognition model.
- Target device memory, processor and runtime constraints.
- Candidate architectures, search parameters and pruning configurations.
- Recognition results and processing times from offline and field evaluation.

Resources were constrained, and runtime support limited quantization options. Feasible alternatives had to come from architecture choices and pruning.

## User flow

1. Collect and prepare sensor data in the windows required by the model.
2. Run recognition on the target device to obtain activity categories.
3. Check predictions against labels and field observations while measuring processing time and resource use.
4. Revise architecture or compression settings based on quality and real-time performance.
5. Use the validated model and runtime approach in field application trials.

## Outputs

The research used neural architecture search, Bayesian optimization and structured pruning to compress the model without quantization in the target runtime, evaluating both recognition and time-series processing speed.

The work reached application validation at an overseas construction site and a first-author RSJ2022 publication on activity recognition, model search and compression. This public account presents the approach and my research contribution without client data or specific internal metrics.

## Scope

- The work concerned sensor-based activity recognition and edge deployment research, not autonomous control of an entire machine.
- Model search and compression had to respect the target runtime. Development-machine support does not establish field compatibility.
- Field validation covered specific devices, data and tasks, not every machine or operating condition.
- The publication and engineering validation were outputs of this phase; no assumptions are made about subsequent long-term operations.

## Acceptance criteria

- Compare baseline and compressed models on clearly defined data splits.
- Measure time-series window processing on the actual device rather than substituting development-machine performance.
- Check size and runtime resources against constraints and document unsupported approaches.
- Use field validation to examine differences from offline inputs and retain interpretable failure examples.

Commercial acceptance thresholds are not disclosed.

## Iteration

I first established which methods the device could execute, then reduced model burden through search and pruning and checked real-time and field performance. This led to the next research questions: could the model become smaller, and could fewer sensors suffice?

Turning device constraints into research questions and using field results to evaluate research value became an important connection between my model research and engineering delivery.
