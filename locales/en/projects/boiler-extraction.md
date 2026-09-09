## Goal

Extract manufacturing year and manufacturer from field equipment nameplates to support verification. With blur, reflections or missing labels, the system should preserve uncertainty and return empty values for information it cannot confirm.

I handled data preparation, VLM fine-tuning, cloud deployment, and quality and cost evaluation. The goal was a repeatable structured extraction pipeline with an explicit role for human review.

## Inputs

- Field nameplate images spanning different levels of clarity, reflection and completeness.
- Year and manufacturer annotations, with reference answers for independent evaluation.
- LoRA training data and multimodal models of different sizes.
- GCP GPU resources, Docker configuration, VRAM limits and cloud costs.

Training feasibility was part of model selection. A larger model could not be the default simply because of its size if it could not be fine-tuned within available resources.

## User flow

1. Submit a nameplate image.
2. Extract year and manufacturer in a defined format, leaving uncertain fields empty.
3. Normalize year formats and align outputs with verification data.
4. Review the original image when results are missing, unclear or potentially wrong.
5. Record failure types to guide data collection and the next evaluation.

## Outputs

I prepared the LoRA dataset and built structured outputs, year normalization, ground-truth alignment, batch inference and failure review.

I fine-tuned Qwen2.5-VL-3B with LoRA and reproduced experiments using a GCP VM and Docker. VRAM constraints on larger models meant that selection considered capability, training feasibility and cloud costs together.

Evaluation separated exact matches across both fields from year and manufacturer correctness. Failures were traced to input conditions such as blur, reflection and incomplete labels, helping clients distinguish usable results from those needing review.

## Scope

- The task extracts specified image fields; it is not a safety inspection or final equipment identity certification.
- Outputs support verification. Missing information is not inferred.
- My contribution covered data, fine-tuning, runtime and evaluation, rather than the entire equipment verification process.
- Original client images, internal field records and specific experiment metrics are not public.

## Acceptance criteria

These are evaluation criteria, not disclosed client acceptance thresholds.

- Consistent fields and formats, explicit year normalization and inspectable empty-value handling.
- Separate training and independent evaluation data; report joint and individual field performance.
- Evidence for failure conditions and a clear scope for human review.
- Reproducible inference and evaluation in the recorded GPU and container environment, with resource requirements stated.

## Iteration

I first defined correct extraction, then connected data, inference and reference answers. VRAM limits informed model size, followed by runnable fine-tuning experiments, independent evaluation and error review.

Further improvements should target observed failure types and compare quality gains with resource costs. Explainable failure categories and a clear empty-value policy matter alongside average accuracy.
