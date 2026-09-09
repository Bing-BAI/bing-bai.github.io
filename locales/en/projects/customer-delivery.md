## Goal

Validate video analytics SaaS at manufacturing and logistics sites through PoC deployment, issue resolution and product review. Client evidence would inform which capabilities deserved further investment.

I handled backend-related work, deployment and technical troubleshooting, and helped translate limits in models, data and workflows into product decisions. Value included usable delivery and recognizing approaches that would not scale.

## Inputs

- Factory or warehouse video, with questions about process duration, differences in worker efficiency and time away from workstations.
- Work areas, action definitions, annotations and local training data.
- Platform, model, database and deployment dependencies.
- Network, hardware and privacy constraints, plus clients’ configuration and maintenance capacity.

Video could include variable frame rates, blind spots, occlusion and rapid consecutive actions. Some data had to stay onsite for training and validation.

## User flow

1. Prepare the platform and dependencies onsite, upload video and check input requirements.
2. Prepare and annotate data, training locally when needed.
3. Run inference and configure workflows; inspect timelines, statistics and detections.
4. Compare results with original footage and report missed detections, misalignment or configuration difficulties.
5. Resolve tractable issues and review scenarios that need changes, simplification or discontinued investment.

## Outputs

I supported local training and PoC delivery, investigating model, data and configuration issues behind missed detections and field feedback. Evaluation distinguished relatively usable absence statistics from process-time analysis affected by overlapping regions, rapid actions and blind spots.

Troubleshooting identified variable frame rates as a cause of playback/detection timeline mismatch. I used FFmpeg to normalize frame rates and documented offline Windows deployment packages, video requirements and troubleshooting procedures.

Product review showed that complex self-service configuration transferred algorithmic and operational burdens to clients without AI experience. My analysis supported the team’s decision to stop investment that could not scale, and proposed controlled templates, guided flows and preset workflows.

## Scope

- My contribution was deployment, backend and troubleshooting work, PoC evaluation and product review, not independent development of the whole SaaS product.
- Useful statistics in one area do not establish reliable recognition of all actions. Input fixes do not eliminate model errors.
- Controlled templates and related ideas were proposed directions, not released features.
- Investment decisions were made by the team; I contributed analysis and delivery feedback.

## Acceptance criteria

These summarize client validation practices; specific sign-off conditions are not public.

- Compare each business metric with human results and identify reliable and failing conditions.
- Verify detection timelines against video, reproduce issues and check fixes.
- Run local preparation, annotation, training and validation within the agreed environment with documented dependencies.
- Evaluate client configuration and maintenance effort alongside model quality.
- Support investment recommendations with evidence and identify necessary changes to scenarios, workflows or features.

## Iteration

The focus expanded from whether models and systems ran to whether results were trustworthy, clients could use them and delivery could be repeated affordably. Camera changes, work-area adjustments, merged process steps, more annotations and dual cameras all required benefit/cost comparisons.

The experience reinforced collaborative validation, attention to user burden, and willingness to change or stop a technical approach while documenting lessons for more explainable and maintainable delivery.
