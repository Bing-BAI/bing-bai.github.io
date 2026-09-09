## Goal

Deliver a visual localization model for a Qualcomm edge environment, reducing model size while retaining day and night localization capability. The client’s existing INT8 path had degraded performance, requiring error diagnosis and a reproducible alternative.

I handled conversion and quantization validation, localization error analysis, and delivery of code, results and reports. Retraining was unavailable and the schedule was tight, so the remedy had to work with the existing model.

## Inputs

- The original HF-Net model, existing INT8 approach and conversion configuration.
- Day and night evaluation data, error thresholds and baseline results.
- PyTorch, ONNX, QNN SDK and target backends including CPU and HTP.
- Requirements for model size, runtime resources and delivery timing.

Consistent evaluation conditions were essential to distinguish conversion issues, quantization effects and backend differences.

## User flow

1. Reproduce the original model and existing quantization path under one evaluation protocol.
2. Check whether calibration data or inference backends explain or remedy the degradation.
3. Apply an alternative quantization strategy and run the same evaluation.
4. Compare day/night success rates, model size and failure cases for deployment suitability.
5. Deliver model-related code, results and instructions for integration engineers to reproduce.

## Outputs

I reproduced the PyTorch → ONNX → QNN SDK INT8 path and checked different calibration data and CPU/HTP backends. Those changes did not resolve the localization degradation.

I then used Cross-Layer Equalization and per-channel quantization to address dynamic-range issues, delivering an alternative that better preserved localization than the conventional INT8 path while retaining compression benefits.

The edge deployment package combined quantization code, comparative results and a report. It needed to be runnable and explain the limitations of the original path and the conditions in which the alternative worked.

## Scope

- The work covered conversion, quantization, evaluation and delivery of an existing localization model, not the complete perception and control stack of an automated parking system.
- Retraining was outside this phase, so the approach had to be validated on the existing model.
- Recovery on the day/night evaluation set is not a guarantee across all locations, cameras or conditions.
- Client models, data and internal evaluation numbers are not public.

## Acceptance criteria

- Compare original, conventional INT8 and alternative models using identical data and localization error criteria, reporting day and night performance separately.
- Verify localization capability as well as size; successful conversion alone does not establish deployment suitability.
- Record conversion and quantization settings so results can be reproduced.
- Keep code, results and instructions consistent and explain tested and untested conditions to integrators.

Client sign-off terms are not public, and no additional production performance guarantees are implied.

## Iteration

I reproduced the degradation, tested calibration and backend differences, then investigated quantization strategies related to dynamic range. Each step used the same evaluation protocol.

Further work should validate new scenarios and continue assessing resources, accuracy and maintenance costs. Model optimization should be judged by the capability the business needs; size is only one measure.
