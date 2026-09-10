## Goal

CONFIDE WA is a video analysis platform for factory and warehouse operations. It turns observations such as body and hand positions into verifiable work events and time statistics. This case focuses on inspection and sorting at an Elecom logistics warehouse: could automated statistics reduce manual video review and timing, and provide evidence for process improvement?

Using Corpy's CONFIDE Workflow Analysis platform, the team evaluated operation durations, differences in the composition of two workers' activities, and time at or away from the workstation. I contributed to backend development, workflow troubleshooting and the customer proof of concept (PoC), working with the team to check results and applicability.

## Inputs

Inputs included videos of two workers, a manually defined list of business activities, body and hand annotations, work regions and action conditions. Selected short clips supported detailed operation analysis; longer original videos supported absence statistics. Each analysis was checked against manual records.

Challenges included variable frame rates, occlusion, blind spots and rapid consecutive actions. Activities with different business meanings could take place in the same region with very similar hand trajectories.

## User flow

Project staff first confirmed the activities and timing definitions with the site manager, inspected the videos and established manual references. They then selected models, configured detection regions and workflows, ran analysis, and reviewed video overlays, timelines and aggregate statistics.

Visual detection supplied body and hand observations. Region and persistence conditions produced candidate actions, which a state machine organized into measurable work states. Reviewing errors against the original footage helped distinguish input, detection and workflow configuration problems.

## Outputs

I contributed to backend and data migration work, workflow fixes, and video preprocessing, configuration and validation for Elecom. When variable frame rates caused analysis results to drift from the playback timeline, I used FFmpeg to standardize frame rates and checked alignment against the video.

The PoC produced operation timings, comparisons between the two workers, presence and absence statistics, validation recordings and reports. Results varied by task: absence statistics performed relatively well under the test conditions, while detailed operation timing remained limited by shared regions, rapid actions and blind spots.

For example, a hand passing through the same region might be placing a product or one of several trays. A state machine cannot recover missing object information from hand position alone. Improvement options included camera and work-region adjustments, grouping indistinguishable actions, adding object annotations, and assessing the benefit and cost of multiple views.

## Scope

This was a warehouse workstation analysis PoC using object detection and state machines to organize business events. Similar aggregate durations do not establish that individual event timestamps are correct. Comparisons of worker efficiency also require item counts, product mix and work paths.

The Elecom validation ran on Corpy servers. I also supported offline Windows deployment and local training for a separate Canon customer project with different data and deployment constraints. The findings here apply to the Elecom validation.

## Acceptance criteria

Validation compared each business metric with manual results and documented usable conditions, failure cases and improvement costs. Further acceptance checks should cover event start and end times, missed and false events, performance across workstations, and the effort required for staff to review results.

## Iteration

I first reduced “improve operational efficiency” to “obtain trustworthy work records,” connecting the problem to visual events and state transitions. When results fell short, I reconsidered whether the footage could distinguish the actions, then separated timing, detection, regions, states and statistics. Working backward from verifiable results helped define input and annotation requirements and preserve configuration and troubleshooting lessons for the next workstation.
