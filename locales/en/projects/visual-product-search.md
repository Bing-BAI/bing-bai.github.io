## Goal

Help store staff find possible product specifications from a phone photograph of an unidentified part. Visual results must become candidates that people can verify, supported by user management, search history and an operational foundation.

As technical lead, I connected client constraints, algorithm validation, business system design and cost assessment. The central question was how to use existing specifications when most catalog entries had no product photographs.

## Inputs

- Photos of parts and a reference object for scale conversion.
- Structured catalog specifications, including dimensions and thread pitch, and attributes that could form retrieval text.
- Annotations and reference specifications for detection, segmentation, measurement and matching.
- Store information, user roles and search history.

Camera angles, lighting and reflections varied, and the client could not photograph the entire catalog. A complete product image library was therefore not a viable prerequisite.

## User flow

The basic store workflow was:

1. Submit a photograph; detect the target and segment the part and reference object.
2. Align orientation, convert scale and estimate thread pitch to obtain comparable measurements.
3. Match specifications and return the top three candidates for the user to check.
4. Record searches; allow authorized managers to review history and audit information.

A later design introduced VLM-based visual attributes, retrieval from a vector index of specification text, and measurement-based reranking. This was architecture and feasibility work, separate from the implemented basic features.

## Outputs

I developed detection, segmentation, PCA-based orientation correction, reference-based scale conversion, DFT thread-pitch estimation and specification matching, then evaluated measurement and recommendation performance.

Engineering outputs included a containerized demo, a FastAPI and PostgreSQL backend, role-based permissions, JWT, search history and auditing. These gave the visual demo a manageable, traceable business foundation.

I also designed a layered RAG architecture and estimated token usage and costs for several image-model APIs to support budget and commercialization decisions.

## Scope

- My work covered client constraints, technical direction, algorithm validation, system design and related development, and cost assessment.
- A containerized demo and backend do not imply production deployment across all scenarios. VLM and vector retrieval work remained design and feasibility work.
- Recommendations assist product lookup and still require specification checks. Sample results are not guarantees for arbitrary photography conditions.

## Acceptance criteria

These summarize the documented validation approach; client sign-off terms and experiment metrics are not public.

- Check dimension and pitch errors and top-three matches against reference specifications, with sample and photography conditions stated.
- Reproduce the image-to-candidate flow, verify structured outputs, search history and permissions.
- State image assumptions and token estimates when comparing API costs.
- Evaluate future RAG work against the existing approach on the same dataset for recall, reranking, latency and cost.

## Iteration

I first built a CV pipeline around measurable geometry, then added users, permissions and history to connect results to a business workflow. Missing catalog photos then prompted a different product representation: specification text combined with visual attribute extraction.

The experience reinforced two questions: what data do we actually have, and how can someone verify the result? Further value should be explained through recommendation quality and cost, rather than the number of models added.
