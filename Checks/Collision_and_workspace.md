# Collision and workspace checks

The released assembly has 101 CAD occurrences. The working pose is [90, 100, 90, 90, 0, 0, 0]° left and [−90, 100, −90, 90, 0, 0, 0]° right. Both triggers start open in the displayed STEP. The staged path from the nominal hanging posture passed the rigid-body screen. The straight interpolation struck the two grips together at five sampled positions. Use the staged path as a starting point for an unpowered fit check. [Geometry hashes](geometry_hashes.json) · [Pose-by-pose results](pose_screen.csv)

| Test | Poses | With surface crossings | Outcome |
|---|---:|---:|---|
| Working and nominal hanging poses | 2 | 0 | Both clear for the screened pairs. |
| Five two-hand tasks | 85 | 0 | 17 samples each for forward reach, lowering, widening, approaching the center and one-handed reach. |
| Staged park to working | 34 | 0 | From hanging, first turn only J3 to +90° left and −90° right. Then move on to the working pose. 17 samples per stage. |
| Direct park to working | 17 | 5 | Palm bodies overlap by 890.886 mm³ at step 7 of 16. |
| Independent local joint draws | 128 | 3 | Palm/palm or trigger/palm interference. |
| Independent full-range joint draws | 128 | 2 | Left forearm intersects the mast by 181.269 mm³ at sample 79. Left palm intersects the arch by 10.759 mm³ at sample 83. |
| Both palms targeting the same point | 1 | 1 | Palm reference points approach within 0.006 mm and the solid palms overlap by 6,281.388 mm³. |

Of 395 sampled configurations, 11 had surface crossings. The two independent sets use scrambled 14-dimensional Sobol draws with open triggers. Local joint half-widths are [15, 15, 25, 20, 25, 15, 20]°. Task and parking trajectories interpolate linearly in joint angle. At each task and on the first park stage, the left trigger sweeps 0° to 30° and the right 30° to 0°. The second park stage reverses the trigger sweeps. Shared endpoints appear in multiple rows. [Task coordinates](task_targets.csv) · [Exact solid-intersection examples](exact_examples.csv)

The broad phase includes left/right pairs, moving arm groups against the stationary frame, and same-arm pairs separated by at least two joints. FCL tests surface crossings on CAD triangles tessellated at 0.10 mm and 0.18 rad. The screen omits rigid and directly adjacent same-arm pairs. Exact OpenCascade intersections confirmed selected positive cases. Surface touching and complete enclosure can give different results in triangle and solid tests. Separate checks cover the [shoulder](Shoulder_interfaces.md), [arm interfaces](Arm_joint_interfaces.csv) and [grip](Grip_and_wrist_clearances.csv).

## Continuous clearances

- Along the seven task and staged parking segments, interval bounds keep the arms separated horizontally and all moving hardware at least **66.48 mm** above the table. On the center-reaching segment the bounds are **44.57 mm** horizontal separation and **259.55 mm** table clearance. The palm centers start 220.05 mm apart and finish 100.01 mm apart. At the target, the grip exteriors are 69.87 mm apart for the tested trigger positions. [Segment bounds](continuous_arm_separation.csv) · [Grip surface distances](Bilateral_grip_clearance.csv)
- With each arm joint independently within ±[2.5, 2.5, 4, 4, 5, 4, 5]° of its working angle and each trigger anywhere from 0° to 30°, the bounds give **47.15 mm** of bilateral separation and **195.62 mm** above the table for moving components. This test covers arm-to-arm and table clearance. [Per-component bounds](independent_joint_box_bounds.csv)

The center-reaching segment also passed a continuous check of all **4,089** bilateral pairs, nonadjacent same-arm pairs, and group J2-or-higher pairs against the stationary frame. The algorithm canceled shared rotations, projected the enclosing boxes onto 13 directions and used exact OpenCascade distances for close pairs. It completed in two angular intervals with 36 exact distance checks and zero unproven pairs. This applies to the specified joint and trigger interpolation. [Path certificate](trajectory_certificate.csv)

For the axis-aligned clearance bounds, each component fits inside an exact-shape enclosing box. For each corner and joint, a rotation of at most α moves the corner at most 2r sin(α/2), where r is its perpendicular distance to the current joint axis. Summing the relevant displacement bounds and allowing another 0.02 mm per component gives a lower bound on separation. The paths use 32 equal angular intervals. The independent ranges use 256 sub-boxes per arm. The machine-readable values are rounded.

The measurements cover rigid nominal geometry. They cannot predict operator hand size, harness motion, fit tolerances, flex under load or arbitrary whole-arm movements. The URDF joint limits alone allow the confirmed collisions above.
