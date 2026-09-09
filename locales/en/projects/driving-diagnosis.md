## Goal

Validate technology and propose an MVP for post-drive diagnosis in driver training. Front-facing and cabin video would help instructors review turns and lane changes using traceable teaching evidence.

I handled requirements decomposition, key vision experiments, system direction and sensor-option assessment. Instead of asking a model to decide whether driving was safe, I clarified the evidence needed and the judgments that should remain with the instructor.

## Inputs

- Front-facing and cabin video showing the road and driver behavior.
- Maneuver windows and annotation requirements for head pose, gaze and checking behavior.
- Video clips for pairing, preprocessing and grid-based annotation.
- Installation conditions, camera calibration information and compute resources.

There was no GPS, CAN or IMU input and no standardized calibration. The limits of dual-camera evidence and gaps in ground truth had to remain explicit.

## User flow

This was the proposed MVP teaching workflow, not a completed production product:

1. Import paired video from a driving session.
2. Locate maneuvers for review and associate road objects, structure and rules.
3. Analyze cabin head pose, gaze, mirror checks and blind-spot checks.
4. Organize both streams into temporal evidence, including visual gaze directions.
5. Let instructors review the original footage, verify evidence and give feedback.

## Outputs

I decomposed the problem into maneuver windows, road risks and rules, driver checking behavior, temporal evidence and human review.

Key experiments used L2CS-Net and MediaPipe Iris to visualize gaze direction with arrows. Looking ahead during straight driving provided an anchor for correcting global installation offsets. I preprocessed and paired clips, created grid annotations, and evaluated conditions including masks, glasses and head movements.

The system design combined optical flow, road structure, detection and tracking, and traffic-light and sign recognition. I compared dual-camera-only, CAN-assisted and IMU-assisted options to inform PoC scope, deployment and sensor investment.

## Scope

- Completed work included requirements, gaze-related experiments, data processing and an MVP proposal. The multi-module design does not mean every module was implemented.
- Outputs support post-drive teaching, not real-time vehicle control or replacement of instructors’ safety judgments.
- Gaze projection and behavior interpretation require validation under calibration and sensor limitations.
- Client names, original driving footage and internal evaluation records remain private.

## Acceptance criteria

These apply to validation and proposal work, not completed product acceptance.

- Verifiable pairing, preprocessing and annotation of dual-camera clips.
- Gaze arrows shown alongside footage, with offset correction and failure conditions explained.
- Separate analysis of masks, glasses and head movement.
- Explicit MVP inputs, outputs, human review and missing evidence.
- Sensor comparisons that cover information gained, deployment complexity and investment requirements.

## Iteration

I reframed broad safety judgments as reviewable evidence tasks, then tested feasible gaze capabilities under dual-camera constraints. I organized further modules around maneuver windows and road understanding, checking which information needed additional sensors or annotations.

The next priority should be ground truth and critical-scenario evaluation before expanding system commitments. Visualization helps instructors participate in validation and identifies what engineering should improve next.
