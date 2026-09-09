## Goal

Evaluate an upgrade from manual visual inspection of railway equipment to AI-assisted candidate screening and human review, combining contour segmentation, known-anomaly classification and evidence across frames.

I handled solution analysis, experiments and delivery coordination. Existing template matching and unsupervised anomaly detection did not fully exploit known anomalies, so the evaluation compared these approaches with supervised classification.

## Inputs

- Normal and known-anomaly images, plus constructed anomaly samples for experiments.
- Contours, segmentation labels, masks and crops.
- Classes including normal equipment, contact-strip anomalies and horn anomalies.
- Consecutive frames, field data arrival rates and the target inference environment.

Sample origins, construction methods and class definitions affect conclusions. Contour quality and correlations between consecutive frames also matter to the full pipeline.

## User flow

The intended screening workflow was:

1. Receive equipment images, segment contours and create consistent downstream inputs.
2. Classify normal and known-anomaly categories, incorporating rule-based results.
3. Combine consecutive frames to reduce single-frame variation.
4. Let maintenance staff check candidate images, suspected regions and original footage.
5. Feed false alarms, misses and input-quality issues into evaluation and improvement.

## Outputs

After comparing template matching, kNN, autoencoders and PatchCore, I introduced ResNet34 to classify known anomalies from equipment masks and evaluated changes in viewing angle.

The pipeline used YOLO11s-seg for contours, with annotation, mask/crop generation, training, evaluation and error analysis to create consistent classifier inputs.

The proposed integration combined rules, ResNet34 and majority voting across three consecutive frames. Processing-time estimates were compared with input intervals. This validation supported the client’s move into operational system development; it does not imply that I independently deployed the entire production system.

## Scope

- My contribution covered solution upgrades, data and model validation, analysis and delivery coordination, not other team members’ modules.
- Supervised classification handles defined categories. Unknown anomalies need separate treatment.
- Differences between constructed and real anomalies remain relevant. Single-model evaluation does not replace field acceptance.
- This account includes the upgrade beyond the earlier unsupervised approach.

## Acceptance criteria

These summarize experimental and system checks; client sign-off requirements are not public.

- Check segmentation against annotations and analyze downstream effects of contour errors.
- Document training, evaluation and constructed samples; compare per-class results and failures.
- Compare single-frame, rule-fusion and multi-frame decisions for new misses or latency.
- Estimate throughput within agreed hardware and timing boundaries against incoming data rates.
- Keep candidates traceable to original images and distinguish model judgments from maintenance decisions.

## Iteration

Comparison of template matching and unsupervised approaches highlighted the value of supervised learning for known anomalies. I then standardized segmentation inputs, evaluated classification and combined rules with temporal evidence.

The approach evolved with evidence. Further work should examine real field data, the complete pipeline and unknown-anomaly limits so experimental gains can fit reliably into operational work.
