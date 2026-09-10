## Goal

Extract manufacturing year and manufacturer brand from photographs of nameplates on customers' water heaters, providing equipment information for KEPCO's replacement screening and after-sales inspections. The task focused on converting images into fields; subsequent business processes would combine those fields with other records to make decisions.

I was responsible for data preparation, VLM fine-tuning validation, cloud execution and evaluation. The focus was reproducible verification and clear handling of photographs that did not support a reliable answer.

## Inputs

Inputs included field photographs, year and brand annotations linked to filenames, and the model and container environment needed for training and evaluation. Images varied in clarity, reflections and label completeness.

Unknown values needed separate annotation for brand and year. Resource availability was also a constraint: experiments had to run within the available GPU memory and environment, rather than selecting a model by parameter count alone.

## User flow

Given a photo, the model was instructed to return `YEAR; BRAND`, using `None` for fields it could not confirm. Code parsed and normalized the fields for comparison with reference information. Missing, ambiguous or potentially fabricated values should be checked against the original image by a person before supporting business screening.

During development, batch predictions, field-level comparisons and failure reviews identified reliable inputs and remaining problems. A complete business workbench and downstream integration were separate from this model validation task.

## Outputs

I worked on annotation conversion, Qwen2.5-VL-3B LoRA validation, GCP/Docker execution and batch evaluation. The 7B model exceeded available memory under the training configuration used, so I selected a 3B configuration that could complete training and be reproduced.

Evaluation considered year, brand, joint matches and whether genuinely unknown fields were left empty, retaining predictions and error cases. These deliverables helped explain model capabilities, input limitations and priorities for further investment.

## Scope

Manufacturing year is not installation date or remaining service life. Field extraction does not itself constitute a safety inspection, fault diagnosis or final replacement decision. The images depict customers' existing equipment; extracted information supports the energy-service business.

An instruction to return an empty value does not eliminate fabricated answers. Evaluation must normalize unknown values and year formats and define brand matching rules, distinguishing strict matches from accepted name variants. Results from different model versions and experiment stages should not be merged directly.

## Acceptance criteria

Acceptance should cover fields and output format, performance on known and unknown values, failure conditions, runtime environment and resource requirements. Data, model and processing rules need to be fixed, and training/evaluation separation checked, before deciding which outputs can be accepted automatically and which require human review.

## Iteration

I first narrowed equipment understanding to two verifiable fields and related the task to structured information extraction. I then asked whether the business needed an apparently complete answer or evidence that could be checked. This led to separate work on annotation, training, parsing and evaluation. Working backward from review requirements shaped outputs and data conditions. The resulting data and evaluation process could extend to new equipment fields, with renewed validation for different brands, image quality and operating contexts.
